# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class KaizenEvaluationSheet(Document):
	def validate(self):
		frappe.db.sql("UPDATE `tabKaizen` SET evaluation_process='"+str(self.name)+"' WHERE name='"+str(self.kaizen_id)+"' ",as_dict=1)