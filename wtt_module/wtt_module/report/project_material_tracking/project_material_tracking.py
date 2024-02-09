# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime

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
		"label": _("Item Code"),
		"fieldname": "item_code",
		"fieldtype": "Link",
		"options":"Item",
		"width": 150,
		"hidden":1
		},
		{
		"label": _("Description"),
		"fieldname": "description",
		"fieldtype": "Data",
		"width": 150
		},
		{
		"label": _("Technical Description"),
		"fieldname": "technical_description",
		"fieldtype": "Data",
		"width": 150
		},
		{
		"label": _("MR Row"),
		"fieldname": "mr_row",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("MR Qty"),
		"fieldname": "mr_qty",
		"fieldtype": "Float",
		"width": 80
		},
		{
		"label": _("MR No"),
		"fieldname": "mr_no",
		"fieldtype": "Link",
		"options":"Material Request",
		"width": 120
		},
		{
		"label": _("Freeze Row"),
		"fieldname": "freeze_row",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("Freeze Qty"),
		"fieldname": "freeze_qty",
		"fieldtype": "Float",
		"width": 80
		},
		{
		"label": _("Freeze No"),
		"fieldname": "freeze_no",
		"fieldtype": "Link",
		"options":"Freeze Items",
		"width": 120
		},
		{
		"label": _("PO Row"),
		"fieldname": "po_row",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("PO No"),
		"fieldname": "po_no",
		"fieldtype": "Link",
		"options":"Purchase Order",
		"width": 120
		},
		{
		"label": _("PO Status"),
		"fieldname": "po_status",
		"fieldtype": "Data",
		"width": 120
		},
		{
		"label": _("PR Row"),
		"fieldname": "pr_row",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("PR No"),
		"fieldname": "pr_no",
		"fieldtype": "Data",
		"width": 120
		},
		{
		"label": _("PR Status"),
		"fieldname": "pr_status",
		"fieldtype": "Data",
		"width": 120
		},
		{
		"label": _("DC Date"),
		"fieldname": "dc_date",
		"fieldtype": "Date",
		"width": 100
		},
		{
		"label": _("DC row"),
		"fieldname": "dc_row",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("DC No"),
		"fieldname": "dc_no",
		"fieldtype": "Link",
		"width": 170,
		"options":"Delivery Note"
		},
		{
		"label": _("DC Qty"),
		"fieldname": "dc_qty",
		"fieldtype": "Float",
		"width": 80
		},
		{
		"label": _("Status"),
		"fieldname": "status",
		"fieldtype": "HTML",
		"width": 120
		}
	]

	return columns

def get_data(conditions,data, filters):
	data=[]
	for i in frappe.db.sql("""SELECT * FROM `tabMaterial Request Item` WHERE docstatus=1{conditions}""".format(conditions=conditions), as_dict=1):
		dc=frappe.db.sql("SELECT * FROM `tabDelivery Note Item` WHERE docstatus=1 and material_request_item='"+str(i.name)+"'",as_dict=1)
		if(dc):
			for q in dc:
				dc_date = frappe.db.get_value('Delivery Note', q.parent, 'posting_date')

				poi_idx = frappe.db.get_value('Purchase Order Item', {'material_request_item': i.name}, 'idx')
				poi_no = frappe.db.get_value('Purchase Order Item', {'material_request_item': i.name}, 'parent')
				poi_status = frappe.db.get_value('Purchase Order',poi_no, 'workflow_state')

				pri_idx = frappe.db.get_value('Purchase Receipt Item', {'material_request_item': i.name}, 'idx')
				pri_no = frappe.db.get_value('Purchase Receipt Item', {'material_request_item': i.name}, 'parent')
				pri_status = frappe.db.get_value('Purchase Receipt',pri_no, 'status')

				data.append({
				"item_code":i.item_code,
				"description":i.description,
				"technical_description":i.technical_description,
				"mr_row":i.idx,
				"mr_qty":i.qty,
				"mr_no":i.parent,
				"po_row": poi_idx,
				"po_no": poi_no,
				"po_status":poi_status,
				"pr_row": pri_idx,
				"pr_no": pri_no,
				"pr_status":pri_status,
				"dc_date":dc_date,
				"dc_row":q.idx,
				"dc_no":q.parent,
				"dc_qty":q.qty,
				"status":"<b style='color:green'>Delivered</b>"
				})
		else:
			poi_idx = frappe.db.get_value('Purchase Order Item', {'material_request_item': i.name}, 'idx')
			poi_no = frappe.db.get_value('Purchase Order Item', {'material_request_item': i.name}, 'parent')
			poi_status = frappe.db.get_value('Purchase Order',poi_no, 'workflow_state')

			pri_idx = frappe.db.get_value('Purchase Receipt Item', {'material_request_item': i.name}, 'idx')
			pri_no = frappe.db.get_value('Purchase Receipt Item', {'material_request_item': i.name}, 'parent')
			pri_status = frappe.db.get_value('Purchase Receipt',pri_no, 'status')

			data.append({
			"item_code":i.item_code,
			"description":i.description,
			"technical_description":i.technical_description,
			"mr_row":i.idx,
			"mr_qty":i.qty,
			"mr_no":i.parent,
			"po_row":poi_idx,
			"po_no":poi_no,
			"po_status":poi_status,
			"pr_row": pri_idx,
			"pr_no": pri_no,
			"pr_status":pri_status,
			"dc_date":"-",
			"dc_row":"-",
			"dc_no":"-",
			"dc_qty":"-",
			"status":"<b style='color:red'>Not Delivered</b>"
			})
	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("material_request"):
		conditions += " AND parent='%s'" % filters.get('material_request')

	if filters.get("project"):
		conditions += " AND project='%s'" % filters.get('project')

	return conditions
