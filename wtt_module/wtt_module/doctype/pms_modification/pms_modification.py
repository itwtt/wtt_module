# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PMSModification(Document):
	def on_submit(self):
		frappe.db.sql("DELETE from `tabTechnical Data` where employee='"+str(self.employee)+"' ")
		for i in self.criteria:
			tech_data=frappe.new_doc("Technical Data")
			tech_data.employee=self.employee
			tech_data.performance_index=i.type
			tech_data.technical__criteria=i.criteria
			tech_data.save()
@frappe.whitelist()
def update_technical(emp):
	arr=[]
	query=frappe.db.sql("SELECT performance_index,technical__criteria FROM `tabTechnical Data` WHERE employee='"+str(emp)+"' ORDER BY performance_index",as_dict=1)
	for i in query:
		arr.append({
			'perfor':i.performance_index,
			'techcri':i.technical__criteria
			})
	return arr