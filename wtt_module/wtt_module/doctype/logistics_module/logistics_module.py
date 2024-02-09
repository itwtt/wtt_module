# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LogisticsModule(Document):
	pass


@frappe.whitelist()
def get_bc(sup):
	ar=[]
	for i in frappe.db.sql("SELECT * FROM `tabBank Account` WHERE party='"+str(sup)+"'",as_dict=1):
		ar.append({
			"bank_acc":i.name
		})
	return ar