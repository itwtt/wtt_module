from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
import math
import json

def execute(filters=None):
	if not filters:
		return [], []
	data = []
	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data = get_data(conditions,data,filters)
	return columns, data

@frappe.whitelist()
def get_columns(filters):
	columns = [
		{
		"label": _("Pre MR No"),
		"fieldname": "pre_mr_no",
		"fieldtype": "Link",
		"options":"Pre MR",
		"width": 120,
		"hidden":1
		},
		{
		"label": _("Pre MR Row"),
		"fieldname": "pre_mr_row",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("Item Code"),
		"fieldname": "item_code",
		"fieldtype": "Link",
		"options":"Item",
		"width": 120
		},
		{
		"label": _("Description"),
		"fieldname": "description",
		"fieldtype": "Data",
		"width": 120
		},
		{
		"label": _("Technical Description"),
		"fieldname": "technical_description",
		"fieldtype": "Data",
		"width": 200
		},
		{
		"label": _("Qty"),
		"fieldname": "qty",
		"fieldtype": "Float",
		"width": 80,
		"hidden":1
		},
		{
		"label": _("UOM"),
		"fieldname": "uom",
		"fieldtype": "Data",
		"width": 80,
		"hidden":1
		},
		{
		"label": _("Qty"),
		"fieldname": "req_qty",
		"fieldtype": "Float",
		"width": 120
		},
		{
		"label": _("UOM"),
		"fieldname": "req_uom",
		"fieldtype": "Data",
		"width": 120
		},
		{
		"label": _("MR Row No"),
		"fieldname": "mr_row",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("MR Qty"),
		"fieldname": "mr_qty",
		"fieldtype": "Float",
		"width": 100
		},
		{
		"label": _("Drawing No"),
		"fieldname": "drawing_no",
		"fieldtype": "Data",
		"width": 250
		}
	]

	return columns

def get_data(conditions,data, filters):
	data=[]
	for i in frappe.db.sql("""SELECT parent,name,idx,item_code,description,technical_description,pre_mr_qty,qty,uom,pre_mr_uom,drawing_no FROM `tabPre MR Table` WHERE docstatus=1{conditions} ORDER BY idx ASC""".format(conditions=conditions), as_dict=1):
		v=frappe.db.get_value("Material Request Item",{'pre_mr':i.parent,'item_code':i.item_code},"idx")
		mr_qty = frappe.db.get_value("Material Request Item",{'pre_mr':i.parent,'item_code':i.item_code},"qty")
		data.append({
			"pre_mr_no":i.parent,
			"pre_mr_row":i.idx,
			"item_code":i.item_code,
			"description":i.description,
			"technical_description":i.technical_description,
			"qty":i.pre_mr_qty,
			"uom":i.pre_mr_uom,
			"req_qty":i.qty,
			"req_uom":i.uom,
			"mr_row":v,
			"drawing_no":i.drawing_no,
			"mr_qty":mr_qty
		})
	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("pre_mr"):
		conditions += " AND parent='%s'" % filters.get('pre_mr')

	return conditions