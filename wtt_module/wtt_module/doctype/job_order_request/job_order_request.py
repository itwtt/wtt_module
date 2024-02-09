# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class JobOrderRequest(Document):
	def validate(self):
		for d in self.get("items"):
			d.t_warehouse1=self.to_warehouse




# @frappe.whitelist()
# def make_mr_request(source_name, target_doc=None):
# 	doc = get_mapped_doc("Nesting Module", source_name, {
# 		"Nesting Module": {
# 			"doctype": "Job Order Request",
# 			"validation": {
# 				"docstatus": ["=", 1]
# 			},
# 		},
# 		"Sheet Material Table": {
# 			"doctype": "Job Order Table",
# 			"field_map": {
# 				"stock_accepted": "qty",
# 				"t_warehouse":"s_warehouse1",
# 				"parent":"against_stock_entry",
# 				"name":"ste_detail"
# 			}
# 		}
# 	}, target_doc)
# 	return doc


@frappe.whitelist()
def make_entry(source_name, target_doc=None):
	doc = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Job Order Request",
			"validation": {
				"docstatus": ["=", 1]
			},
		},
		"Material Request Item": {
			"doctype": "Job Order Table",
			"field_map": {
				"item_code": "fg_item",
			}
		}
	}, target_doc)
	return doc
