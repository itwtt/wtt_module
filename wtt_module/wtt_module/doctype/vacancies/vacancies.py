# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Vacancies(Document):
	def validate(self):
		ar=[]
		for i in self.vacancies:
			ar.append(i.positions)
		self.total_vacant=sum(ar)

