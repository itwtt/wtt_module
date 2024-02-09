# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import json
from datetime import date
from frappe.utils import getdate
def execute(filters=None):
	if not filters:
		return [], []
	data = []
	columns = get_columns(filters)
	# conditions = get_conditions(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	columns=[
		{
			"label": _("Project"),
			"fieldtype": "Data",
			"fieldname": "project",
			"width": 100
		},
		{
			"label": _("Item Code"),
			"fieldtype": "Data",
			"fieldname": "item_code",
			"width": 150
		},
		{
			"label": _("Description"),
			"fieldtype": "Data",
			"fieldname": "description",
			"width": 150
		},
		{
			"label": _("Technical Description"),
			"fieldtype": "Data",
			"fieldname": "technical_description",
			"width": 350
		},
		{
			"label": _("Item Group"),
			"fieldtype": "Data",
			"fieldname": "item_group",
			"width": 150
		},
		{
			"label": _("Qty"),
			"fieldtype": "Data",
			"fieldname": "qty",
			"width": 150
		},
		{
			"label": _("UOM"),
			"fieldtype": "Data",
			"fieldname": "uom",
			"width": 150
		},
		{
			"label": _("MR No"),
			"fieldtype": "Data",
			"fieldname": "mr_no",
			"width": 150
		},
		{
			"label": _("Reference"),
			"fieldtype": "Data",
			"fieldname": "ref",
			"width": 10
		},
		{
			"label": _("Conversion Factor"),
			"fieldtype": "Data",
			"fieldname": "conversion_factor",
			"width": 10
		},
		{
			"label": _("Stock UOM"),
			"fieldtype": "Data",
			"fieldname": "stock_uom",
			"width": 10
		},
		{
			"label": _("Warehouse"),
			"fieldtype": "Data",
			"fieldname": "warehouse",
			"width": 100
		}
	]
	return columns
def get_data(data,filters=None):
	vtech=filters.get('tech')
	att1=[]


	query1 = frappe.db.sql("SELECT distinct(parent) FROM `tabItem Variant Attribute` WHERE docstatus=0 ",as_dict=1)
	if(filters.description!=None and filters.description!="--Select--"):
		query1 = frappe.db.sql("SELECT distinct(parent) FROM `tabItem Variant Attribute` WHERE docstatus=0 and attribute_value='"+str(filters.description)+"' ",as_dict=1)
		if(filters.tech!=None):
			query1 = frappe.db.sql("SELECT distinct(parent) FROM `tabItem Variant Attribute` WHERE docstatus=0 and attribute_value='"+str(filters.tech)+"' ",as_dict=1)
	elif(filters.tech!=None):
		query1 = frappe.db.sql("SELECT distinct(parent) FROM `tabItem Variant Attribute` WHERE docstatus=0 and attribute_value='"+str(filters.tech)+"' ",as_dict=1)
	
	for k in query1:

		if(filters.tech2==None and filters.tech1==None):
			att1.append(k.parent)

		elif(filters.tech1!=None):
			for l in frappe.db.sql("SELECT distinct(parent) FROM `tabItem Variant Attribute` WHERE docstatus=0 and attribute_value='"+str(filters.tech1)+"' and parent='"+str(k.parent)+"' ",as_dict=1):
				if(filters.tech2!=None):
					for m in frappe.db.sql("SELECT distinct(parent) FROM `tabItem Variant Attribute` WHERE docstatus=0 and attribute_value='"+str(filters.tech2)+"' and parent='"+str(l.parent)+"' ",as_dict=1):
						att1.append(m.parent)
				else:
					att1.append(l.parent)

		elif(filters.tech2!=None):
			for l in frappe.db.sql("SELECT distinct(parent) FROM `tabItem Variant Attribute` WHERE docstatus=0 and attribute_value='"+str(filters.tech2)+"' and parent='"+str(k.parent)+"' ",as_dict=1):		
				att1.append(l.parent)

		
			

	data=[]
	po=[]
	query=frappe.db.sql("SELECT mri.parent,mri.item_code,mri.project,mri.item_group,mri.description,mri.technical_description,mri.qty,mri.name,mri.uom,mri.stock_uom,mri.conversion_factor,mri.warehouse from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mri.item_group=%(item_group)s and mr.workflow_state='Approved' and mr.project=%(project)s",filters,as_dict=1)
	for det in query:
		for j in frappe.db.sql("SELECT material_request_item FROM `tabPurchase Order Item` WHERE material_request_item='"+str(det.name)+"'",as_dict=1):
			po.append(j.material_request_item)
		
	for d in query:
		if(d.name not in po):
			if(d.item_code in att1):
				data.append({
					"project":d.project,
					"item_code":d.item_code,
					"description":d.description,
					"technical_description":d.technical_description,
					"item_group":d.item_group,
					"qty":d.qty,
					"uom":d.uom,
					"mr_no":d.parent,
					"ref":d.name,
					"conversion_factor":d.conversion_factor,
					"stock_uom":d.stock_uom,
					"warehouse":d.warehouse
					})
	return data


# def get_conditions(filters):
# 	conditions = ""
# 	if filters.get("tech"):
# 		conditions += " AND attribute_value='%s'" % filters.get('tech')
# 	# if filters.get("tech1"):
# 	# 	conditions += " AND attribute_value='%s'" % filters.get('tech1')
# 	# if filters.get("tech2"):
# 	# 	conditions += " AND attribute_value='%s'" % filters.get('tech2')
# 	return conditions

@frappe.whitelist()
def get_value():
	ag=['']
	des=['--Select--']
	for i in frappe.db.sql("SELECT DISTINCT(attribute_value) FROM `tabItem Attribute Value` ORDER BY attribute_value",as_dict=1):
		ag.append(i.attribute_value)
	for j in frappe.db.sql("SELECT DISTINCT(description) FROM `tabItem` ORDER BY description",as_dict=1):
		des.append(j.description)
	return ag,des

@frappe.whitelist()
def create_po(supplier,schedule_date,items):
	python_items = json.loads(items)
	# frappe.msgprint(str(supplier))
	# frappe.msgprint(str(schedule_date))
	# frappe.msgprint(str(items))
	# for i in python_items:
	# 	frappe.msgprint(str(i['item_code']))
	rfq = frappe.new_doc("Request for Quotation")
	rfq.schedule_date = date.today()
	rfq.save()
	return supplier

@frappe.whitelist()
def create_existing_po(doc):
	ar = []
	query = frappe.db.sql("SELECT item_code,description,qty,stock_uom,uom,conversion_factor,warehouse,project_name,material_request,material_request_item,project_name FROM `tabRequest for Quotation Item` WHERE parent='"+str(doc)+"' ",as_dict=1)
	for i in query:
		ar.append(i)
	return ar