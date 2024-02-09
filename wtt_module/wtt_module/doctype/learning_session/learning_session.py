# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LearningSession(Document):
	pass
@frappe.whitelist()
def set_dept(emp):
	ar=[]
	query=frappe.db.sql("SELECT department FROM `tabKaizen Allocated Department` WHERE name='"+str(emp)+"' ",as_dict=1)
	if(query):
		for i in query:
			ar.append(i.department)

	return ar