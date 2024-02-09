# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class IncidentRecord(Document):
	def validate(self):
		if(self.workflow_state=='Investigated'):
			if(self.investigated_by==None or self.investigator_description==None):
				frappe.throw("Investigator Name is Mandatory")
