# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CasualLeave(Document):
	def validate(self):
		ar=[]
		for i in self.casual_leave_table:
			ar.append(i.leave_approved)
		self.total=sum(ar)
