# Copyright (c) 2021, wtt_custom and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
class JobApp(Document):
	# def before_insert(self):
	# 	frappe.db.sql("DELETE FROM `tabJob App` WHERE email_id='"+str(self.email_id)+"' and date_of_birth='"+str(self.date_of_birth)+"' ")

	def on_submit(self):
		if(self.job_status=='Shortlisted'):
			doc=frappe.new_doc('Job Applicant')
			doc.applicant_name=self.applicant_name
			doc.email_id=self.email_id
			doc.phone_number=self.mobile_
			doc.status='Accepted'
			doc.save()


@frappe.whitelist()
def make_candidate(source_name, target_doc=None):
	def postprocess(source, target_doc):
		target_doc.naming_series="HR-INT-"
	doclist = get_mapped_doc("Job App", source_name, 	{
		"Job App": {
			"doctype": "HR interview",
			"validation": {
				"docstatus": ["=", 0]
			},
			"field_map": {
				"name":"job_id",
				"applicant_name": "candidate_name",
				"applying_post":"position"
			}
		},
	}, target_doc,postprocess)
	return doclist


@frappe.whitelist()
def make_job_candidate(source_name, target_doc=None):
	def postprocess(source, target_doc):
		target_doc.naming_series="TECH-INT-"
	doclist = get_mapped_doc("Job App", source_name, 	{
		"Job App": {
			"doctype": "Technical Interview",
			"validation": {
				"docstatus": ["=", 0]
			},
			"field_map": {
				"name":"job_id",
				"applicant_name": "candidate_name",
				"applying_post":"position",
			}
		},
	}, target_doc,postprocess)
	return doclist	
