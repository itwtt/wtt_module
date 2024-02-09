# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class QueryReply(Document):
	def validate(self):
		frappe.db.sql("UPDATE `tabProject Queries` SET reply='"+str(self.name)+"' WHERE name='"+str(self.query)+"' ")
	