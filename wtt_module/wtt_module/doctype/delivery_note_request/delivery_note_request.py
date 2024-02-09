from __future__ import unicode_literals

import json

import frappe
from frappe import _, msgprint
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cstr, flt, get_link_to_form, getdate, new_line_sep, nowdate
from six import string_types
from datetime import date,datetime,timedelta
from erpnext.buying.utils import check_on_hold_or_closed_status, validate_for_items
from erpnext.controllers.buying_controller import BuyingController
from erpnext.manufacturing.doctype.work_order.work_order import get_item_details
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.stock.stock_balance import get_indented_qty, update_bin_qty


class DeliveryNoteRequest(BuyingController):
	pass
@frappe.whitelist()
def update_status(name,status):
	material_request = frappe.get_doc('Delivery Note Request', name)
	material_request.check_permission('write')
	material_request.update_status(status)
@frappe.whitelist()
def make_request(source_name, target_doc=None):
	def postprocess(source, target):
		target.purpose="Delivery Note Request"
		target.schedule_date=target.transaction_date
		for i in target.get("items"):
			i.schedule_date=target.transaction_date
	doc = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Delivery Note Request",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"name": "mr_no",
				"title":"title",
				"set_warehouse":"set_from_warehouse"
			}
		},
		"Material Request Item": {
			"doctype": "Delivery Note Request Item",
			"field_map": {
				"stock_accepted": "qty",
				"t_warehouse":"from_warhouse",
				"parent":"material_request",
				"name":"material_request_item"
			}
		}
	}, target_doc,postprocess)
	return doc
@frappe.whitelist()
def make_receipt(source_name, target_doc=None):
	def postprocess(source, target):
		target.purpose="Delivery Note Request"
		target.schedule_date=target.transaction_date
		for i in target.get("items"):
			i.schedule_date=target.transaction_date
	doc = get_mapped_doc("Stock Entry", source_name, {
		"Stock Entry": {
			"doctype": "Delivery Note Request",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"to_warehouse":"set_from_warehouse",
				"title":"title"
			}
		},
		"Stock Entry Detail": {
			"doctype": "Delivery Note Request Item",
			"field_map": {
				"t_warehouse": "from_warehouse",
				"material_request":"material_request",
				"material_request_item":"material_request_item",
				"parent":"stock_entry",
				"name":"stock_entry_item"
			}
		}
	}, target_doc,postprocess)
	return doc

def create_work_order(source_name, target_doc=None):
	def postprocess(source, target):
		target.purpose="Work Order"
	doc = get_mapped_doc("Stock Entry", source_name, {
		"Stock Entry": {
			"doctype": "Work Order",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"source_warehouse":"Stores - WTT",
				"fg_warehouse":"Stores - WTT",
				"wip_warehouse":"SHOP FLOOR - WTT"
			}
		},
		"Stock Entry Detail": {
			"doctype": "Work Order Item"
		}
	}, target_doc,postprocess)
	return doc
@frappe.whitelist()
def make_delivery_note(source_name,target_doc=None):
	doc = get_mapped_doc("Delivery Note Request", source_name, {
		"Delivery Note Request": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Delivery Note Request Item": {
			"doctype": "Delivery Note Item",
			"field_map": [
				["parent", "delivery_note_request"],
				["name","delivery_note_request_item"]
			]
		}
	}, target_doc)
	return doc

@frappe.whitelist()
def make_mat(source_name,target_doc=None):
	doc = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Material Request Item": {
			"doctype": "Delivery Note Item",
			"field_map": [
				["parent", "material_request"],
				["name","material_request_item"]
			]
		}
	}, target_doc)
	return doc
