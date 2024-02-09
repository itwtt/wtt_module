# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class SalaryFitment(Document):
	def on_submit(self):
		self.valid_from=date.today()
		if(self.revised_from):
			val = frappe.db.set_value("Salary Fitment",self.revised_from,'workflow_state','Previous Fitment')
			val1 = frappe.db.set_value("Salary Fitment",self.revised_from,'docstatus',0)
			val2 = frappe.db.set_value("Salary Fitment",self.revised_from,'revised_on',date.today())
			frappe.db.commit()
@frappe.whitelist()
def revision(name):
	val = frappe.db.set_value("Salary Fitment",name,'workflow_state','Previous Fitment')
	val1 = frappe.db.set_value("Salary Fitment",name,'docstatus',0)
	val2 = frappe.db.set_value("Salary Fitment",name,'revised_on',date.today())
	frappe.db.commit()