# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PreJournalEntry(Document):
	def on_cancel(self):
		# pass
		frappe.db.sql("UPDATE `tabJournal Entry` SET docstatus=2,workflow_state='Cancelled' WHERE name='"+str(self.journal_name)+"' ",as_dict=1)
