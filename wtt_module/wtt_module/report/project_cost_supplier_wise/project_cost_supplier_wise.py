# Copyright (c) 2023, wtt_module and contributors
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
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	if(filters.report_type == 'PO Wise'):
		columns=[
				{
				"label":"Supplier",
				"fieldname":"supplier",
				"fieldtype":"Data",
				"width":320
				},
				{
				"label":"Name",
				"fieldname":"po_name",
				"fieldtype":"Link",
				"options":"Purchase Order",
				"width":100
				},
				{
				"label":"Project",
				"fieldname":"project",
				"fieldtype":"Link",
				"options":"Project",
				"width":100
				},
				{
				"label":"Total PO Cost",
				"fieldname":"total_po_cost",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"Total PO Tax",
				"fieldname":"total_po_tax",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"PR No",
				"fieldname":"pr_name",
				"fieldtype":"Link",
				"options":"Purchase Receipt",
				"width":100
				},
				{
				"label":"Total PR Cost",
				"fieldname":"total_pr_cost",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"Total PR Tax",
				"fieldname":"total_pr_tax",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"Difference",
				"fieldname":"diff",
				"fieldtype":"HTML",
				"width":150
				}
				]
	else:
		columns=[
				{
				"label":"Supplier",
				"fieldname":"supplier",
				"fieldtype":"Data",
				"width":320
				},
				{
				"label":"Project",
				"fieldname":"project",
				"fieldtype":"Link",
				"options":"Project",
				"width":100
				},
				{
				"label":"Total PO Cost",
				"fieldname":"total_po_cost",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"Total PO Tax",
				"fieldname":"total_po_tax",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"Total PR Cost",
				"fieldname":"total_pr_cost",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"Total PR Tax",
				"fieldname":"total_pr_tax",
				"fieldtype":"Currency",
				"width":150
				},
				{
				"label":"Difference",
				"fieldname":"diff",
				"fieldtype":"HTML",
				"width":150
				}
				]
	return columns

def get_data(data,filters):
	ar=[]
	if(filters.report_type == 'PO Wise'):
		for i in frappe.db.sql("SELECT poi.name,poi.parent as 'po_par',(SELECT supplier FROM `tabPurchase Order` WHERE name=poi.parent) as 'supplier',poi.project,sum(poi.base_net_amount) as 'sum',po.total_taxes_and_charges FROM `tabPurchase Order`as po,`tabPurchase Order Item` as poi WHERE poi.parent=po.name and po.docstatus=1 and poi.project='"+str(filters.project_name)+"' GROUP BY po.name ORDER BY sum DESC",as_dict=1):
			pr_total=0
			pr_tax=0
			parent=''
			for k in frappe.db.sql("SELECT name FROM `tabPurchase Order Item` WHERE parent='"+str(i.po_par)+"'",as_dict=1):
				for j in frappe.db.sql("SELECT pri.base_net_amount,pri.parent,pr.total_taxes_and_charges FROM `tabPurchase Receipt` as pr,`tabPurchase Receipt Item`as pri WHERE pr.name=pri.parent and pr.docstatus=1 and pri.project='"+str(filters.project_name)+"' and pri.purchase_order_item='"+str(k.name)+"'",as_dict=1):
					pr_total=pr_total+float(j.base_net_amount)
					pr_tax=pr_tax+float(j.total_taxes_and_charges)
					parent=j.parent
			vvs=float(i.sum) - float(pr_total)
			if(vvs<0):
				vvs='<p style="background:orange;color:black">'+str(round(vvs,2))+'</p>';
			elif(vvs>0):
				vvs='<p style="background:lightgreen;color:black">'+str(round(vvs,2))+'</p>';
			data.append({
				"supplier":i.supplier,
				"po_name":i.po_par,
				"project":i.project,
				"total_po_cost":i.sum,
				"total_po_tax":i.total_taxes_and_charges,
				"pr_name":parent,
				"total_pr_cost":pr_total,
				"total_pr_tax":pr_tax,
				"diff":vvs
			})
	else:
		for i in frappe.db.sql("SELECT poi.parent as 'po_par',po.supplier as 'supplier',poi.project,sum(poi.base_net_amount) as 'sum',sum(po.total_taxes_and_charges) as 'po_tax' FROM `tabPurchase Orer`as po, `tabPurchase Order Item`as poi WHERE po.docstatus=1 and poi.project='"+str(filters.project_name)+"' GROUP BY po.supplier ORDER BY sum DESC",as_dict=1):
			pr_total=0
			pr_tax=0
			parent=''
			for k in frappe.db.sql("SELECT supplier FROM `tabPurchase Order` WHERE name='"+str(i.po_par)+"'",as_dict=1):
				for j in frappe.db.sql("SELECT pri.base_net_amount,pri.parent,pr.total_taxes_and_charges FROM `tabPurchase Receipt` as pr INNER JOIN `tabPurchase Receipt Item` as pri ON pr.name=pri.parent WHERE pri.project='"+str(filters.project_name)+"' and pr.docstatus=1 and pr.supplier='"+str(k.supplier)+"'",as_dict=1):
					pr_total=pr_total+float(j.base_net_amount)
					pr_tax=pr_tax+float(j.total_taxes_and_charges)
					parent=j.parent
			vvs=float(i.sum) - float(pr_total)
			if(vvs<0):
				vvs='<p style="background:orange;color:white">'+str(round(vvs,2))+'</p>';
			elif(vvs>0):
				vvs='<p style="background:lightgreen;color:black">'+str(round(vvs,2))+'</p>';
			data.append({
					"supplier":i.supplier,
					"po_name":i.po_par,
					"project":i.project,
					"total_po_cost":i.sum,
					"pr_name":parent,
					"total_pr_cost":pr_total,
					"total_pr_tax":pr_tax,
					"diff":vvs
			})
	return data
