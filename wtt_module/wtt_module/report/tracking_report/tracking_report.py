# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [
		{
			"label": _("MR Date"),
			"fieldname": "material_request_date",
			"fieldtype": "Date",
			"width": 140
		},
		{
			"label": _("MR No"),
			"options": "Material Request",
			"fieldname": "material_request_no",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Project"),
			"options": "Project",
			"fieldname": "project",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Requestor"),
			"options": "Employee",
			"fieldname": "requestor",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"label": _("Description"),
			"fieldname": "description",
			"fieldtype": "Data",
			"width": 180
		},
		{
			"label": _("Technical Description"),
			"fieldname": "technical_description",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Item Qty as per MR"),
			"fieldname": "mr_quantity",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Item Qty as per PO"),
			"fieldname": "po_quantity",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "data",
			"width": 140
		},
		{
			"label": _("PO Date"),
			"fieldname": "purchase_order_date",
			"fieldtype": "Date",
			"width": 140
		},
		{
			"label": _("PO No"),
			"options": "Purchase Order",
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Supplier"),
			"options": "Supplier",
			"fieldname": "supplier",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Expected Delivery Date"),
			"fieldname": "expected_delivery_date",
			"fieldtype": "Date",
			"width": 140
		},
		{
			"label": _("Actual Delivery Date"),
			"fieldname": "actual_delivery_date",
			"fieldtype": "Date",
			"width": 140
		},
	]
	return columns

def get_conditions(filters):
	conditions = ""

	if filters.get("company"):
		conditions += " AND parent.company=%s" % frappe.db.escape(filters.get('company'))

	if filters.get("cost_center") or filters.get("project"):
		conditions += """
			AND (child.`cost_center`=%s OR child.`project`=%s)
			""" % (frappe.db.escape(filters.get('cost_center')), frappe.db.escape(filters.get('project')))

	if filters.get("from_date"):
		conditions += " AND parent.transaction_date>='%s'" % filters.get('from_date')

	if filters.get("to_date"):
		conditions += " AND parent.transaction_date<='%s'" % filters.get('to_date')

	return conditions

def get_data(filters):
	conditions = get_conditions(filters)
	purchase_order_entry = get_po_entries(conditions)
	mr_records, procurement_record_against_mr = get_mapped_mr_details(conditions)
	pr_records = get_mapped_pr_records()
	pi_records = get_mapped_pi_records()

	procurement_record=[]
	if procurement_record_against_mr:
		procurement_record += procurement_record_against_mr
	for po in purchase_order_entry:
		# fetch material records linked to the purchase order item
		mr_record = mr_records.get(po.material_request_item, [{}])[0]
		val=mr_record.get('owner')
		created_po=frappe.db.get_value("User",val,"first_name")
		procurement_detail = {
			"material_request_date": mr_record.get('transaction_date'),
			"project": po.project,
			"requestor": created_po,
			"material_request_no": po.material_request,
			"item_code": po.item_code,
			"description":po.description,
			"technical_description":po.technical_description,
			"mr_quantity": mr_record.get('qty'),
			"po_quantity": flt(po.qty),
			"status": po.status,
			"purchase_order_date": po.transaction_date,
			"purchase_order": po.parent,
			"supplier": po.supplier,
			"expected_delivery_date": po.schedule_date,
			"actual_delivery_date": pr_records.get(po.name)
		}
		procurement_record.append(procurement_detail)
	return procurement_record

def get_mapped_mr_details(conditions):
	mr_records = {}
	mr_details = frappe.db.sql("""
		SELECT
			parent.transaction_date,
			parent.per_ordered,
			parent.owner,
			child.name,
			child.parent,
			child.amount,
			child.qty,
			child.item_code,
			child.description,
			child.technical_description,
			child.uom,
			parent.status,
			child.project,
			child.cost_center
		FROM `tabMaterial Request` parent, `tabMaterial Request Item` child
		WHERE
			parent.per_ordered>=0
			AND parent.name=child.parent
			AND parent.docstatus=1
			{conditions}
		""".format(conditions=conditions), as_dict=1) #nosec

	procurement_record_against_mr = []
	for record in mr_details:
		created=frappe.db.get_value("User",record.owner,"first_name")
		if record.per_ordered:
			mr_records.setdefault(record.name, []).append(frappe._dict(record))
		else:
			procurement_record_details = dict(
				material_request_date=record.transaction_date,
				material_request_no=record.parent,
				requestor=created,
				item_code=record.item_code,
				description=record.description,
				technical_description=record.technical_description,
				estimated_cost=flt(record.amount),
				quantity=flt(record.qty),
				unit_of_measurement=record.uom,
				status=record.status,
				purchase_order_amt_in_company_currency=0,
				project = record.project,
				cost_center = record.cost_center
			)
			procurement_record_against_mr.append(procurement_record_details)
	return mr_records, procurement_record_against_mr

def get_mapped_pi_records():
	return frappe._dict(frappe.db.sql("""
		SELECT
			pi_item.po_detail,
			pi_item.base_amount
		FROM `tabPurchase Invoice Item` as pi_item
		INNER JOIN `tabPurchase Order` as po
		ON pi_item.`purchase_order` = po.`name`
		WHERE
			pi_item.docstatus = 1
			AND po.status not in ("Closed","Completed","Cancelled")
			AND pi_item.po_detail IS NOT NULL
		"""))

def get_mapped_pr_records():
	return frappe._dict(frappe.db.sql("""
		SELECT
			pr_item.purchase_order_item,
			pr.posting_date
		FROM `tabPurchase Receipt` pr, `tabPurchase Receipt Item` pr_item
		WHERE
			pr.docstatus=1
			AND pr.name=pr_item.parent
			AND pr_item.purchase_order_item IS NOT NULL
			AND pr.status not in  ("Closed","Completed","Cancelled")
		"""))

def get_po_entries(conditions):
	return frappe.db.sql("""
		SELECT
			child.name,
			child.parent,
			child.cost_center,
			child.project,
			child.warehouse,
			child.material_request,
			child.material_request_item,
			child.item_code,
			child.description,
			child.technical_description,
			child.stock_uom,
			child.qty,
			child.amount,
			child.base_amount,
			child.schedule_date,
			parent.transaction_date,
			parent.supplier,
			parent.status,
			parent.owner
		FROM `tabPurchase Order` parent, `tabPurchase Order Item` child
		WHERE
			parent.docstatus = 1
			AND parent.name = child.parent
			AND parent.status not in  ("Closed","Completed","Cancelled")
			{conditions}
		GROUP BY
			parent.name, child.item_code
		""".format(conditions=conditions), as_dict=1) #nosec
