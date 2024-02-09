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
			"width": 160
		},
		{
			"label": _("Request Purpose"),
			"fieldname": "req_pur",
			"fieldtype": "Data",
			"width": 160
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
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Item Qty as per MR"),
			"fieldname": "mr_quantity",
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
			"label": _("Item Qty as per PO"),
			"fieldname": "po_quantity",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("PO Rate"),
			"fieldname": "po_rate",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("PO Base Rate"),
			"fieldname": "base_rate",
			"fieldtype": "Float",
			"width": 150
		},
		{
			"label": _("Supplier"),
			"options": "Supplier",
			"fieldname": "supplier",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("PR Date"),
			"fieldname": "pr_date",
			"fieldtype": "Date",
			"width": 140
		},
		{
			"label": _("PR No"),
			"options": "Purchase Receipt",
			"fieldname": "purchase_receipt",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Item Qty as per PR"),
			"fieldname": "pr_qty",
			"fieldtype": "Float",
			"width": 100
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
		conditions += " AND mr.company=%s" % frappe.db.escape(filters.get('company'))

	# if filters.get("cost_center") or filters.get("project"):
	# 	conditions += """
	# 		AND (mri.`cost_center`=%s OR mri.`project`=%s)
	# 		""" % (frappe.db.escape(filters.get('cost_center')), frappe.db.escape(filters.get('project'))) 

	return conditions

def get_data(filters):
	conditions = get_conditions(filters)
	procurement_record=[]
	for i in frappe.db.sql("SELECT mr.transaction_date,mr.request_purpose,mr.status,mri.project,mri.item_group,mr.owner,mri.name,mri.parent,mri.item_code,mri.description,mri.technical_description,mri.qty FROM `tabMaterial Request` AS mr INNER JOIN `tabMaterial Request Item` AS mri ON mri.parent=mr.name WHERE mr.docstatus=1 AND mr.transaction_date>=%(from_date)s AND mr.transaction_date<=%(to_date)s {conditions}".format(conditions=conditions),filters, as_dict=1):
		created_po=frappe.db.get_value("User",i.owner,"first_name")
		po_doc=frappe.db.sql("SELECT mri.schedule_date,mr.transaction_date,mr.supplier,mr.owner,mri.name,mri.parent,mri.item_code,mri.description,mri.technical_description,mri.qty,mri.rate,mri.base_rate FROM `tabPurchase Order` AS mr INNER JOIN `tabPurchase Order Item` AS mri ON mri.parent=mr.name WHERE mri.material_request_item='"+str(i.name)+"' AND mri.material_request='"+str(i.parent)+"' AND mr.workflow_state!='Rejected' AND mr.docstatus!=2 AND mr.transaction_date>=%(from_date)s AND mr.transaction_date<=%(to_date)s {conditions}".format(conditions=conditions),filters, as_dict=1)
		pr_doc=frappe.db.sql("SELECT mr.posting_date,mri.qty,mri.parent FROM `tabPurchase Receipt` AS mr INNER JOIN `tabPurchase Receipt Item` AS mri ON mri.parent=mr.name WHERE mri.material_request_item='"+str(i.name)+"' AND mri.material_request='"+str(i.parent)+"' AND mr.docstatus!=2 AND mr.posting_date>=%(from_date)s AND mr.posting_date<=%(to_date)s {conditions}".format(conditions=conditions),filters, as_dict=1)
		if po_doc and pr_doc:
			for j in po_doc:
				for k in pr_doc:
					procurement_detail = {
						"material_request_date": i.transaction_date,
						"project": i.project,
						"item_group":i.item_group,
						"requestor": created_po,
						"material_request_no": i.parent,
						"req_pur":i.request_purpose,
						"item_code": i.item_code,
						"description":i.description,
						"technical_description":i.technical_description,
						"mr_quantity": flt(i.qty),
						"po_quantity": flt(j.qty),
						"po_rate": flt(j.rate),
						"base_rate": flt(j.base_rate),
						"status": i.status,
						"purchase_order_date": j.transaction_date,
						"purchase_order": j.parent,
						"pr_date":k.posting_date,
						"purchase_receipt":k.parent,
						"pr_qty":flt(k.qty),
						"supplier": j.supplier,
						"expected_delivery_date": j.schedule_date,
						"actual_delivery_date":k.posting_date
						}
					procurement_record.append(procurement_detail)
		elif po_doc:
			for j in po_doc:
				procurement_detail = {
				"material_request_date": i.transaction_date,
				"project": i.project,
				"item_group":i.item_group,
				"requestor": created_po,
				"material_request_no": i.parent,
				"req_pur":i.request_purpose,
				"item_code": i.item_code,
				"description":i.description,
				"technical_description":i.technical_description,
				"mr_quantity": flt(i.qty),
				"po_quantity": flt(j.qty),
				"po_rate": flt(j.rate),
				"base_rate": flt(j.base_rate),
				"status": i.status,
				"purchase_order_date": j.transaction_date,
				"purchase_order": j.parent,
				"supplier": j.supplier,
				"expected_delivery_date": j.schedule_date
				}
				procurement_record.append(procurement_detail)
		elif pr_doc:
			for k in pr_doc:
				procurement_detail = {
				"material_request_date": i.transaction_date,
				"project": i.project,
				"item_group":i.item_group,
				"requestor": created_po,
				"material_request_no": i.parent,
				"req_pur":i.request_purpose,
				"item_code": i.item_code,
				"description":i.description,
				"technical_description":i.technical_description,
				"mr_quantity": flt(i.qty),
				"status": i.status,
				"pr_date":k.posting_date,
				"purchase_receipt":k.parent,
				"pr_qty":flt(k.qty),
				"supplier": k.supplier
				}
				procurement_record.append(procurement_detail)
		else:
			procurement_detail = {
				"material_request_date": i.transaction_date,
				"project": i.project,
				"item_group":i.item_group,
				"requestor": created_po,
				"material_request_no": i.parent,
				"req_pur":i.request_purpose,
				"item_code": i.item_code,
				"description":i.description,
				"technical_description":i.technical_description,
				"mr_quantity": flt(i.qty),
				"status": i.status
				}
			procurement_record.append(procurement_detail)

	return procurement_record