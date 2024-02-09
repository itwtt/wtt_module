# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class BalanceLeave(Document):
	def validate(self):
		ar=[]
		ar1=[]
		for i in self.balance_leave_table:
			ar.append(i.balance_leave)
			ar1.append(i.taken_bl)
		self.total=sum(ar)-sum(ar1)
