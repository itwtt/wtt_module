# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class StructureCalculation(Document):
	# def validate(self):
	# 	self.incremented_amount=float(self.ctcperannum)-float(self.old_ctc_as_per_annum)
	def on_submit(self):
		doc=frappe.new_doc("Salary Structure")
		doc.date=date.today()
		doc.name=self.employee
		doc.append("earnings",{
			"salary_component":"Basic Salary",
			"amount":self.basic_salary
			})
		doc.append("earnings",{
			"salary_component":"House Rent Allowance",
			"amount":self.hra
			})
		doc.append("earnings",{
			"salary_component":"Other Allowance",
			"amount":self.others
			})
		doc.append("deductions",{
			"salary_component":"Provident Fund"
			})
		doc.append("deductions",{
			"salary_component":"ESI"
			})
		doc.save()


@frappe.whitelist()
def get_bs(employee):
	ar=[]
	doc=frappe.get_doc("Employee",employee)
	for i in doc.education:
		ar.append(i.qualification)
	return ar




@frappe.whitelist()
def get_esi_pf(employee):
	ar=[]
	if(frappe.db.exists("Employee",employee)):
		esi=frappe.db.get_value("Employee",employee,"esi")
		pf=frappe.db.get_value("Employee",employee,"pf")
		ar.append({
			"esi":esi,
			"pf":pf
			})
	else:
		frappe.throw("Employee doesn't exists")
	return ar