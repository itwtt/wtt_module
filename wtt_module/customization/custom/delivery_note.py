# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc
from erpnext.controllers.selling_controller import SellingController
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.stock.stock_balance import get_indented_qty, update_bin_qty

class DeliveryNote(SellingController):
	pass
	# def validate(self):
	# 	mr=""
	# 	po=""
	# 	dnr=""
	# 	for i in self.items
	# 		if(i.material_request):
	# 			mr+=i.material_request+', '
	# 		if(i.purchase_order):
	# 			po+=i.purchase_order+', '
	# 		if(i.delivery_note_request):
	# 			dnr+=i.delivery_note_request+', '
	# 	self.ref_mr = mr
	# 	self.ref_po = po
	# 	self.ref_se = dnr


@frappe.whitelist()
def make_note(source_name, target_doc=None):
	doc = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 0]
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

@frappe.whitelist()
def make_dnr(source_name, target_doc=None):
	def postprocess(source, target):
		target.schedule_date=target.posting_date
		# for i in target.get("items"):
		# 	i.schedule_date=target.transaction_date
	doc = get_mapped_doc("Purchase Order", source_name, {
		"Purchase Order": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Purchase Order Item": {
			"doctype": "Delivery Note Item",
			"field_map": {
				"stock_accepted": "qty",
				"material_request":"material_request",
				"material_request_item":"material_request_item",
				"parent":"purchase_order",
				"name":"purchase_order_item"
			}
		}
	}, target_doc,postprocess)
	return doc

@frappe.whitelist()
def make_job(source_name, target_doc=None):
	doc = get_mapped_doc("Job Order", source_name, {
		"Job Order": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Job Order Table": {
			"doctype": "Delivery Note Item",
			"field_map": [
				["basic_rate","rate"],
				["parent", "job_order"],
				["name","job_order_item"]
			]
		}
	}, target_doc)
	return doc

@frappe.whitelist()
def make_qc(source_name, target_doc=None):
	doc = get_mapped_doc("QC for DC", source_name, {
		"QC for DC": {
			"doctype": "Delivery Note",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"QC for DC Item": {
			"doctype": "Delivery Note Item",
			"field_map": [
				["parent","qc_for_dc"],
				["name","qc_for_dc_item"]
			],
			"condition": lambda doc: doc.status=="Approved"
		},
	}, target_doc)
	return doc


@frappe.whitelist()
def make_mat(source_name,target_doc=None,args=None):
	if args is None:
		args = {}
	if isinstance(args, str):
		args = json.loads(args)

	def select_item(d):
		filtered_items = args.get("filtered_children", [])
		child_filter = d.name in filtered_items if filtered_items else True

		return child_filter

	doclist = get_mapped_doc(
		"Material Request",
		source_name,
		{
			"Material Request": {
				"doctype": "Delivery Note",
				"validation": {"docstatus": ["=", 1]},
			},
			"Material Request Item": {
				"doctype": "Delivery Note Item",
				"field_map": [
					["name", "material_request_item"],
					["parent", "material_request"]
				],
				# "allow_child_item_selection": True
				"condition": select_item,
			},
		},
		target_doc)

	return doclist


# @frappe.whitelist()
# def make_mat(source_name,target_doc=None):
# 	doclist = get_mapped_doc(
# 		"Material Request",
# 		source_name,
# 		{
# 			"Material Request": {
# 				"doctype": "Delivery Note",
# 				"validation": {"docstatus": ["=", 1]},
# 			},
# 			"Material Request Item": {
# 				"doctype": "Delivery Note Item",
# 				"field_map": [
# 					["name", "material_request_item"],
# 					["parent", "material_request"]
# 				],
# 			},
# 		},
# 		target_doc)
# 	return doclist

def update_item(obj, target, source_parent):
	target.conversion_factor = obj.conversion_factor
	target.qty = flt(flt(obj.stock_qty) - flt(obj.ordered_qty)) / target.conversion_factor
	target.stock_qty = target.qty * target.conversion_factor
	if getdate(target.schedule_date) < getdate(nowdate()):
		target.schedule_date = None