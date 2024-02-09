# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date,datetime,timedelta
from pytz import timezone
from frappe.utils.background_jobs import enqueue
from frappe.model.mapper import get_mapped_doc

class RecruitmentTracker(Document):
	def validate(self):
		pass
	@frappe.whitelist()
	def send_mail(self):
		recipients_=self.email
		cc_=[]
		msg=self.message
		message=self.message
		password = None
		email_args = {
			"sender":"HR-WTT <hr@wttindia.com>",
			"recipients": recipients_,
			"reply_to":"hr@wttindia.com",
			"message": message
			}
		frappe.sendmail(**email_args)
		frappe.msgprint("Mail Sent to "+self.candidate_name)

	@frappe.whitelist()
	def create_job_applicant(self):
		doc = frappe.new_doc('Job Applicant')
		doc.applicant_name = self.candidate_name
		doc.email_id=self.email
		doc.phone_number=self.contact
		doc.job_title=self.job_opening
		doc.designation=self.designation
		doc.resume_attachment=self.candidate_resume
		doc.religion=self.religion
		doc.applicant_photo=self.candidate_photo
		doc.caste=self.caste
		doc.community=self.community
		doc.experience=self.experience_status
		doc.save()

		dd = frappe.get_doc('Recruitment Tracker',self.name)
		dd.job_applicant = doc.name
		dd.save()
		self.reload()
		frappe.msgprint("Job Applicant Created")

@frappe.whitelist()
def schedule_interview(source_name, target_doc=None):
	doclist = get_mapped_doc(
	"Recruitment Tracker",
	source_name,
	{
		"Recruitment Tracker": {
			"doctype": "Interview Schedule",
			"field_map": {
				"name":"recruitment_tracker"
			}
		},
	},
	target_doc,
	)

	return doclist

@frappe.whitelist()
def get_data(source_name, target_doc=None):
	doclist = get_mapped_doc(
	"Recruitment Database",
	source_name,
	{
		"Recruitment Database": {
			"doctype": "Recruitment Tracker",
			"field_map": {
				"name":"recruitment_reference",
				"suitable_for_the_post":"designation"
			},
		},
	},
	target_doc,
	)

	return doclist