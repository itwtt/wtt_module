# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from num2words import num2words
from frappe.utils.background_jobs import enqueue
from frappe.model.mapper import get_mapped_doc
class AppointmentOrder(Document):
	pass


@frappe.whitelist()
def get_status(cur):
	valword=num2words(cur, lang='en_IN')
	go=valword.capitalize()
	return go

@frappe.whitelist()
def create_from_employee(source_name, target_doc=None):
	doclist = get_mapped_doc(
	"Employee",
	source_name,
	{
		"Employee": {
			"doctype": "Appointment Order",
			"field_map": {
				"name":"employee",
				"applicant_address":"address_line1",
				"address1":"address_line2",
				"address2":"address_line3"
			}
		},
	},
	target_doc,
	)

	return doclist