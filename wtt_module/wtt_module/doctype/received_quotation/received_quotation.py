# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.model.document import Document

class ReceivedQuotation(Document):
	pass
@frappe.whitelist()
def make_quote(source_name, target_doc=None):
	doc = get_mapped_doc("Materials for Enquiry", source_name, {
		"Materials for Enquiry": {
			"doctype": "Received Quotation",
			"validation": {
				"docstatus": ["=", 1]
			},
		},
		"Materials Table": {
			"doctype": "Enquiry Materials",
			"field_map": [
				["parent","reference"],
				["name","reference_item"]
			]
		},
	}, target_doc)
	return doc