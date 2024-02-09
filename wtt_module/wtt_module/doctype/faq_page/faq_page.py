# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FAQPage(Document):
	pass


@frappe.whitelist()
def get_ans(dept,ques):
	val = frappe.db.get_value("FAQ Table",{"parent":dept,"question":ques},"answer")
	val2 = frappe.db.get_value("FAQ Table",{"parent":dept,"question":ques},"name")
	val3 = frappe.db.get_value("FAQ Table",{"parent":dept,"question":ques},"comment")
	return val,val2,val3