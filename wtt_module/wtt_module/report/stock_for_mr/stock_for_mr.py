# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import date,datetime,timedelta

def execute(filters):
	data = []
	columns = get_colomns(filters)
	conditions = get_conditions(filters)
	data = get_data(conditions,data,filters)
	return columns, data


def get_colomns(filters):
	columns = [
	{
		"label":"Material Request",
		"fieldtype":"Data",
		"fieldname":"mr",
		"width":80
	},
	# {
	# 	"label":"Row",
	# 	"fieldtype":"Data",
	# 	"fieldname":"idx",
	# 	"width":100
	# },
	{
		"label":"Item Code",
		"fieldname":"item_code",
		"fieldtype":"Data",
		"width":80
	},
	{
		"label":"Description",
		"fieldname":"description",
		"fieldtype":"Data",
		"width":80
	},
	{
		"label":"Technical Description",
		"fieldname":"technical_description",
		"fieldtype":"Data",
		"width":300
	},
	{
		"label":"Required Qty",
		"fieldtype":"Data",
		"fieldname":"qty",
		"width":80
	},
	{
		"label":"UOM",
		"fieldname":"uom",
		"fieldtype":"Data",
		"width":80
	},
	{
		"label":"Balance Qty",
		"fieldtype":"HTML",
		"fieldname":"bal_qty",
		"width":80
	}
	]
	for i in frappe.db.sql("SELECT distinct(project) from `tabProject Items` ",as_dict=1):
		columns.append({
			"label":i.project,
			"fieldtype":"Data",
			"fieldname":i.project,
			"width":80
			})
	return columns

def get_data(conditions,data,filters):
	data=[]
	query = frappe.db.sql("SELECT distinct(mri.item_code)as item_code,mr.name as mr,mri.idx,mri.qty,mri.description,mri.technical_description,mri.uom FROM `tabMaterial Request`as mr,`tabMaterial Request Item` as mri WHERE mr.name=mri.parent and mr.name=%(material_request)s ",filters,as_dict=1)
	query = frappe.db.sql("""SELECT distinct(mri.item_code)as item_code,mr.name as mr,mri.idx,mri.qty,mri.description,mri.technical_description,mri.uom
			from `tabMaterial Request`as mr,`tabMaterial Request Item` as mri WHERE mr.name=mri.parent and mr.docstatus=1
			{conditions} GROUP BY mri.idx
			""".format(conditions=conditions),as_dict=1)
	proj=[]
	for j in frappe.db.sql("SELECT distinct(project) from `tabProject Items` ",as_dict=1):
		proj.append(j.project)
	proj=set(proj)
	for i in query:
		column={}
		bl_qty = 0
		if(frappe.db.exists({"doctype": "Stock Ledger Entry", "item_code": str(i.item_code), "warehouse":"Stores - WTT", "is_cancelled":0})):
			bl = frappe.get_last_doc('Stock Ledger Entry',filters={"item_code": str(i.item_code), "warehouse":"Stores - WTT", "is_cancelled":0})
			bl_qty = bl.qty_after_transaction
		column['mr'] = str(i.mr)
		column['idx'] = str(i.idx)
		column['item_code'] = str(i.item_code)
		column['description'] = str(i.description)
		column['technical_description'] = str(i.technical_description)
		column['qty'] = str(i.qty)
		column['uom'] = str(i.uom)
		column['bal_qty'] = "<p style='background-color:tomato'>"+str(bl_qty)+"</p>" if(bl_qty<i.qty) else "<p>"+str(bl_qty)+"</p>"
		for j in proj:
			qt=str(frappe.db.get_value("Project Items",{"item_code":i.item_code,"project":str(j)},"qty")) if(frappe.db.exists({"doctype":"Project Items","item_code":i.item_code,"project":str(j)})) else 0
			column[j]=qt
		data.append(column)

	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("material_request"):
		conditions += " AND mr.name='%s'" % filters.get('material_request')
	return conditions

@frappe.whitelist()
def get_value():
	ar=[]
	query = frappe.db.sql("SELECT distinct(description)as description FROM `tabItem` ORDER BY description DESC ",as_dict=1)
	for i in query:
		ar.append(i.description)
	return ar

@frappe.whitelist()
def func(item_code,project,qty,uom):
	ar=[]
	if(frappe.db.exists({"doctype":"Project Items","item_code":str(item_code),"project":str(project)})):
		doc=frappe.get_doc("Project Items",{'item_code':str(item_code),'project':str(project)})
		doc.qty=str(qty)
		doc.uom=str(uom)
		doc.save()

	else:
		doc=frappe.new_doc("Project Items")
		doc.item_code=str(item_code)
		doc.project=str(project)
		doc.qty=str(qty)
		doc.uom=str(uom)
		doc.save()

	return ar