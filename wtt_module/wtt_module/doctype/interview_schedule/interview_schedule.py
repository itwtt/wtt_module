# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class InterviewSchedule(Document):
	def on_submit(self):
		if(self.hr_result == 'SELECTED' and self.technical_result == 'SELECTED'):
			doc = frappe.get_doc('Job Applicant',self.job_applicant)
			doc.status = "Accepted"
			doc.save()

			dd = frappe.new_doc('Job Offer')
			dd.job_applicant = self.job_applicant
			dd.status = 'Accepted'
			dd.designation = frappe.db.get_value("Recruitment Tracker",self.recruitment_tracker,"designation")
			dd.save()

			frappe.msgprint("Job Offer Created")