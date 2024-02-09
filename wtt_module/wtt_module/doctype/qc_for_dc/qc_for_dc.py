# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc
# from erpnext.controllers.selling_controller import SellingController
from frappe.model.document import Document

class QCforDC(Document):
	pass

@frappe.whitelist()
def make_note(source_name, target_doc=None):
	doc = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "QC for DC",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Material Request Item": {
			"doctype": "QC for DC Item",
			"field_map": [
				["qty","out_of"],
				["parent", "material_request"],
				["name","material_request_item"]
			]
		}
	}, target_doc)
	return doc

@frappe.whitelist()
def make_dnr(source_name, target_doc=None):
	doc = get_mapped_doc("Purchase Order", source_name, {
		"Purchase Order": {
			"doctype": "QC for DC",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Purchase Order Item": {
			"doctype": "QC for DC Item",
			"field_map": {
				"stock_accepted":"out_of",
				"material_request":"material_request",
				"material_request_item":"material_request_item",
				"parent":"purchase_order",
				"name":"purchase_order_item"
			}
		}
	}, target_doc)
	return doc
