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
		"width": 100
		},
		{
		"label": _("Technical Description"),
		"fieldname": "technical_description",
		"fieldtype": "Data",
		"width": 200
		},
		{
		"label": _("Project"),
		"fieldname": "project",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("Supplier"),
		"fieldname": "supplier",
		"fieldtype": "Data",
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
		"width": 100
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
		"label": _("Status"),
		"fieldname": "item_status",
		"fieldtype": "HTML",
		"width": 100
		},
		{
		"label": _("PR Status"),
		"fieldname": "pr_status",
		"fieldtype": "Data",
		"width": 100
		}
	]

	return columns

def get_data(conditions,data, filters):
	data=[]
	for i in frappe.db.sql("""SELECT pri.item_code,pri.description,pri.technical_description,pri.project,pr.supplier,pri.qty,pri.idx,pri.parent,pr.status,pri.inspection_status,pri.purchase_order_item FROM `tabPurchase Receipt Item` as pri INNER JOIN `tabPurchase Receipt` as pr ON pr.name=pri.parent WHERE pri.inspection_status='Debit' and pr.docstatus=1{conditions}""".format(conditions=conditions), as_dict=1):
		poi_idx = frappe.db.get_value('Purchase Order Item', {'name': i.purchase_order_item}, 'idx')
		poi_no = frappe.db.get_value('Purchase Order Item', {'name': i.purchase_order_item}, 'parent')
		poi_status = frappe.db.get_value('Purchase Order',poi_no, 'workflow_state')

		data.append({
		"item_code":i.item_code,
		"description":i.description,
		"technical_description":i.technical_description,
		"po_row": poi_idx,
		"po_no": poi_no,
		"po_status":poi_status,
		"project":i.project,
		"supplier":i.supplier,
		"pr_row": i.idx,
		"pr_no": i.parent,
		"pr_status":i.status,
		"item_status":"<b style='color:red'>"+str(i.inspection_status)+"</b>"
		})
	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " AND pr.posting_date>='%s'" % filters.get('from_date')

	if filters.get("to_date"):
		conditions += " AND pr.posting_date<='%s'" % filters.get('to_date')

	if filters.get("project"):
		conditions += " AND pr.project='%s'" % filters.get('project')

	if filters.get("supplier"):
		conditions += " AND pr.supplier='%s'" % filters.get('supplier')

	if filters.get("purchase_order"):
		conditions += " AND pri.purchase_order='%s'" % filters.get('purchase_order')

	return conditions