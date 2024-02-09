# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
class RequestforPayment(Document):
	pass

@frappe.whitelist()
def set_emp(arr):
	doc=frappe.db.get_value('Employee', {'user_id': arr}, 'name')
	return doc

@frappe.whitelist()
def make_request_payment(source_name, target_doc=None):
	def postprocess(source, target):
		target.party_type="Supplier"
	doc = get_mapped_doc("Purchase Invoice", source_name, {
		"Purchase Invoice": {
			"doctype": "Request for Payment",
			"field_map": {
				"supplier":"party"
			},
			"validation": {
				"docstatus": ["=", 1]
			}
		}
	}, target_doc,postprocess)
	return doc
	
@frappe.whitelist()
def farmemp(nn):
	doc=frappe.get_value("Farm Employee",nn,"employee_name")
	return doc