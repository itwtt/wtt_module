# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from datetime import datetime,timedelta

def execute(filters=None):
	data = []
	columns = get_columns(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	columns=[
			{
			"label":"Project",
			"fieldname":"project",
			"fieldtype":"Link",
			"options":"Project",
			"width":150
			},
			{
			"label":"Cost of Order",
			"fieldname":"po_cost",
			"fieldtype":"Currency",
			"width":150
			},
			{
			"label":"Tax",
			"fieldname":"tax",
			"fieldtype":"Currency",
			"width":120
			},
			{
			"label":"Overall Cost",
			"fieldname":"ovv",
			"fieldtype":"Currency",
			"width":150
			},
			{
			"label":"Advance Paid",
			"fieldname":"ad_cost",
			"fieldtype":"Currency",
			"width":150
			},
			{
			"label":"Freight Advance Paid",
			"fieldname":"frd_cost",
			"fieldtype":"Currency",
			"width":120
			},
			{
			"label":"Total Advance Paid",
			"fieldname":"to_cost",
			"fieldtype":"Currency",
			"width":150
			},
			{
			"label":"Difference",
			"fieldname":"diff",
			"fieldtype":"HTML",
			"width":100
			}

			]
	return columns

def get_data(data,filters):
	ar=[]
	arr=[]
	arg=[]
	percentage=[]
	for i in frappe.db.sql("SELECT item_tax_template,base_amount as amount,name,parent from `tabPurchase Order Item` WHERE creation>='2022-11-26 03:45:56.419262' ",as_dict=1):
		if(i.item_tax_template!=None and i.item_tax_template!=''):
			arg.append({
				"name":i.name,
				"item_tax_template":i.item_tax_template,
				"amount":i.amount,
				"parent":str(i.parent)
				})
		elif(frappe.db.get_value("Purchase Order",str(i.parent),"taxes_and_charges")!=None and frappe.db.get_value("Purchase Order",str(i.parent),"taxes_and_charges")!=''):
			percentage.append({
				"name":i.name,
				"item_tax_template":frappe.db.get_value("Purchase Order",str(i.parent),"taxes_and_charges"),
				"amount":i.amount,
				"parent":str(i.parent)
				})

	# frappe.msgprint(str(arg))
	for j in percentage:
		if(j["item_tax_template"] not in ["GST - 0 - WTT","GST - 0% - WTT"]):
			if(frappe.db.exists("Purchase Taxes and Charges Template",str(j["item_tax_template"]))):
				for k in frappe.db.sql("SELECT sum(rate)as rate FROM `tabPurchase Taxes and Charges` WHERE parent='"+str(j["item_tax_template"])+"' ",as_dict=1):
					ar.append({
						"parent":str(j["parent"]),
						"name":j["name"],
						"tax":(float(j["amount"])*(float(k.rate)/100))
						})
					
					frappe.db.sql("UPDATE `tabPurchase Order Item` SET tax='"+str(float(j["amount"])*(float(k.rate)/100))+"' WHERE name='"+str(j["name"])+"' ")



	for i in frappe.db.sql("SELECT project as 'project',sum(base_net_amount) as 'sum',sum(tax)as tax FROM `tabPurchase Order Item` WHERE docstatus=1 GROUP BY project",as_dict=1):

		if(frappe.db.get_value("Project",i.project,"status")=="On going"):
			ar.clear()
			arr.clear()
			# for j in frappe.db.sql("SELECT final_amount FROM `tabAdvance Table` WHERE docstatus=1 and pro='"+str(i.project)+"'",as_dict=1):
			# 	ar.append(float(j.final_amount))

			# for k in frappe.db.sql("SELECT final_amount FROM `tabFreight Table` WHERE docstatus=1 and project='"+str(i.project)+"'",as_dict=1):
			# 	arr.append(float(k.final_amount))
			for i in frappe.db.sql("SELECT total_advance FROM `tabPurchase Order` where project LIKE '"+str(i.project)+"' ",as_dict=1):
				ar.append(float(i.total_advance))
			for j in frappe.db.sql("SELECT freight_advance FROM `tabPurchase Order` where project LIKE '"+str(i.project)+"' ",as_dict=1):
				arr.append(float(j.freight_advance))
			v=(i.sum - (sum(ar)+sum(arr)))
			if(i.tax!=None):
				v=(i.sum+round(i.tax,2)) - (sum(ar)+sum(arr))
			if(v<0):
				vs="<p style='background:red;color:white'>"+str(round(v,2))+"</p>"
			else:
				vs="<p style='background:green;color:white'>"+str(round(v,2))+"</p>"
			data.append({
				"project":i.project,
				"po_cost":i.sum,
				"ad_cost":sum(ar),
				"frd_cost":sum(arr),
				"to_cost":sum(ar)+sum(arr),
				"diff":vs,
				"tax":round(i.tax,2),
				"ovv":round(i.sum + round(i.tax,2),2)
			})
	return data