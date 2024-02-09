# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from datetime import datetime,timedelta
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
	data = []
	columns = get_columns(filters)
	# conditions = get_conditions(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	columns=[]
	if(filters.project==1):
		if(filters.group_by=="Supplier"):
			columns=[
				{
				"label":"Supplier",
				"fieldname":"supplier",
				"fieldtype":"Data",
				"width":200
				},
				{
				"label":"Project",
				"fieldname":"project",
				"fieldtype":"Data",
				"width":100
				},
				{
				"label":"Total",
				"fieldname":"amount",
				"fieldtype":"Currency",
				"width":200
				}

			]
		elif(filters.group_by=="Purchase Order"):
			columns=[
				{
				"label":"Purchase Order",
				"fieldname":"purchase_order",
				"fieldtype":"Data",
				"width":150
				},
				{
				"label":"Supplier",
				"fieldname":"supplier",
				"fieldtype":"Data",
				"width":200
				},
				{
				"label":"Project",
				"fieldname":"project",
				"fieldtype":"Data",
				"width":100
				},
				{
				"label":"Total",
				"fieldname":"amount",
				"fieldtype":"Currency",
				"width":200
				}

			]
	else:
		if(filters.group_by=="Supplier"):
			columns=[
				{
				"label":"Supplier",
				"fieldname":"supplier",
				"fieldtype":"Data",
				"width":200
				},
				{
				"label":"Project",
				"fieldname":"project",
				"fieldtype":"Data",
				"width":100
				},
				{
				"label":"Net Total",
				"fieldtype":"Currency",
				"fieldname":"total",
				"width":150
				},
				{
				"label":"Tax & Charges",
				"fieldname":"total_taxes_and_charges",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"Grand Total",
				"fieldname":"grand_total",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"Rounded Total",
				"fieldname":"rounded_total",
				"fieldtype":"Currency",
				"width":150
				}

			]
		elif(filters.group_by=="Purchase Order"):
			columns=[
				{
				"label":"Purchase Order",
				"fieldname":"purchase_order",
				"fieldtype":"Data",
				"width":150
				},
				{
				"label":"Supplier",
				"fieldname":"supplier",
				"fieldtype":"Data",
				"width":200
				},
				{
				"label":"Project",
				"fieldname":"project",
				"fieldtype":"Data",
				"width":100
				},
				{
				"label":"Net Total",
				"fieldtype":"Currency",
				"fieldname":"total",
				"width":100
				},
				{
				"label":"Tax & Charges",
				"fieldname":"total_taxes_and_charges",
				"fieldtype":"Currency",
				"width":100
				},
				{
				"label":"Grand Total",
				"fieldname":"grand_total",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"Rounded Total",
				"fieldname":"rounded_total",
				"fieldtype":"Currency",
				"width":150
				}

			]
	
	return columns
def get_data(data,filters):
	data=[]
	arr=[]
	ar=[]
	if(filters.project==1):
		if(filters.group_by=="Supplier"):
			if(filters.project_name==None):
				query=frappe.db.sql("SELECT po.supplier,poi.base_amount as amount,poi.project FROM `tabPurchase Order`as po,`tabPurchase Order Item`as poi WHERE po.name=poi.parent and po.transaction_date>=%(from_date)s and po.transaction_date<=%(to_date)s and  po.docstatus=1 and po.naming_series!='JOB-.YY.-' ",filters,as_dict=1)
				for i in query:
					arr.append({
						"supplier":i.supplier,
						"amount":i.amount,
						"project":i.project
						})
				for i in arr:
					if(i["supplier"] not in ar):
						ar.append(i["supplier"])
						data.append(i)
					else:
						data[ar.index(i["supplier"])]["amount"]+=i["amount"]
			else:
				query=frappe.db.sql("SELECT po.supplier,poi.base_amount as amount,poi.project FROM `tabPurchase Order`as po,`tabPurchase Order Item`as poi WHERE po.name=poi.parent and po.transaction_date>=%(from_date)s and po.transaction_date<=%(to_date)s and  po.docstatus=1 and po.naming_series!='JOB-.YY.-' and poi.project=%(project_name)s ",filters,as_dict=1)
				for i in query:
					arr.append({
						"supplier":i.supplier,
						"amount":i.amount,
						"project":i.project
						})
				for i in arr:
					if(i["supplier"] not in ar):
						ar.append(i["supplier"])
						data.append(i)
					else:
						data[ar.index(i["supplier"])]["amount"]+=i["amount"]

		elif(filters.group_by=="Purchase Order"):
			if(filters.project_name==None):
				query=frappe.db.sql("SELECT po.name,po.supplier,poi.base_amount as amount,poi.project FROM `tabPurchase Order`as po,`tabPurchase Order Item`as poi WHERE po.name=poi.parent and po.transaction_date>=%(from_date)s and po.transaction_date<=%(to_date)s and  po.docstatus=1 and po.naming_series!='JOB-.YY.-' ORDER BY po.supplier",filters,as_dict=1)
				for i in query:
					arr.append({
						"purchase_order":i.name,
						"supplier":i.supplier,
						"amount":i.amount,
						"project":i.project
						})
				for i in arr:
					if(i["purchase_order"] not in ar):
						ar.append(i["purchase_order"])
						data.append(i)
					else:
						data[ar.index(i["purchase_order"])]["amount"]+=i["amount"]
			else:
				query=frappe.db.sql("SELECT po.name,po.supplier,poi.base_amount as amount,poi.project FROM `tabPurchase Order`as po,`tabPurchase Order Item`as poi WHERE po.name=poi.parent and po.transaction_date>=%(from_date)s and po.transaction_date<=%(to_date)s and  po.docstatus=1 and po.naming_series!='JOB-.YY.-' and poi.project=%(project_name)s ORDER BY po.supplier",filters,as_dict=1)
				for i in query:
					arr.append({
						"purchase_order":i.name,
						"supplier":i.supplier,
						"amount":i.amount,
						"project":i.project
						})
				for i in arr:
					if(i["purchase_order"] not in ar):
						ar.append(i["purchase_order"])
						data.append(i)
					else:
						data[ar.index(i["purchase_order"])]["amount"]+=i["amount"]

	else:	
		if(filters.group_by=="Supplier"):
			query=frappe.db.sql("SELECT supplier,project,total,total_taxes_and_charges,grand_total,base_rounded_total as rounded_total FROM `tabPurchase Order` WHERE transaction_date>=%(from_date)s and transaction_date<=%(to_date)s and  docstatus=1 and naming_series!='JOB-.YY.-' ",filters,as_dict=1)
			for i in query:
				arr.append({
					"supplier":i.supplier,
					"project":i.project,
					"total":i.total,
					"total_taxes_and_charges":i.total_taxes_and_charges,
					"grand_total":i.grand_total,
					"rounded_total":i.rounded_total
					})
			for i in arr:
				if(i["supplier"] not in ar):
					ar.append(i["supplier"])
					data.append(i)
				else:
					data[ar.index(i["supplier"])]["total"]+=i["total"]
					data[ar.index(i["supplier"])]["total_taxes_and_charges"]+=i["total_taxes_and_charges"]
					data[ar.index(i["supplier"])]["grand_total"]+=i["grand_total"]
					data[ar.index(i["supplier"])]["rounded_total"]+=i["rounded_total"]
				
		elif(filters.group_by=="Purchase Order"):
			query=frappe.db.sql("SELECT name,supplier,project,total,total_taxes_and_charges,grand_total,base_rounded_total as rounded_total FROM `tabPurchase Order` WHERE transaction_date>=%(from_date)s and transaction_date<=%(to_date)s and  docstatus=1 and naming_series!='JOB-.YY.-' ORDER BY supplier",filters,as_dict=1)
			for i in query:
				arr.append({
					"purchase_order":i.name,
					"supplier":i.supplier,
					"project":i.project,
					"total":i.total,
					"total_taxes_and_charges":i.total_taxes_and_charges,
					"grand_total":i.grand_total,
					"rounded_total":i.rounded_total
					})
			for i in arr:
				if(i["purchase_order"] not in ar):
					ar.append(i["purchase_order"])
					data.append(i)
				else:
					data[ar.index(i["purchase_order"])]["total"]+=i["total"]
					data[ar.index(i["purchase_order"])]["total_taxes_and_charges"]+=i["total_taxes_and_charges"]
					data[ar.index(i["purchase_order"])]["grand_total"]+=i["grand_total"]
					data[ar.index(i["purchase_order"])]["rounded_total"]+=i["rounded_total"]
				

		
	return data

# def get_conditions(filters):
# 	conditions=''
# 	if filters.get("date"):
# 		conditions += " and lt.date = %(date)s"
# 	if filters.get("organization"):
# 		conditions += " and lr.company_name = %(organization)s"
# 	if filters.get("next_follow_up_date"):
# 		conditions += " and lr.contact_date = %(next_follow_up_date)s"

# 	match_conditions = build_match_conditions("Lead")
# 	if match_conditions:
# 		conditions += " and %s" % match_conditions
# 	return conditions
