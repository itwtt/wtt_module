# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TechnicalInterview(Document):
	def on_submit(self):
		doc=frappe.db.sql("SELECT * FROM `tabInterview process` WHERE job_id='"+self.job_id+"'")
		if(doc):
			query=frappe.db.sql("UPDATE `tabInterview process` SET prior_work_experience='"+str(self.prior_work_experience)+"',comments_about_prior_work_experience='"+str(self.comments_about_prior_work_experience)+"',technical_qualification='"+str(self.technical_qualification)+"',comments_about_technical_qualification='"+str(self.comments_about_technical_qualification)+"',tech_overall_impression_and_recommendation='"+str(self.overall_impression_and_recommendation)+"',tech_comments_about_overall_impression_and_recommendation='"+str(self.comments_about_overall_impression_and_recommendation)+"',tech_result='"+str(self.result)+"' WHERE job_id='"+str(self.job_id)+"'")
		else:	
			d=frappe.new_doc("Interview process")
			d.candidate_name=self.candidate_name
			d.position=self.position
			d.other_post=self.other_post
			d.date=self.date
			d.job_id=self.job_id
			d.technical_interview_id=self.name
			d.technical_interviewer=self.technical_interviewer
			d.technical_interviewer_name=self.technical_interviewer_name
			d.prior_work_experience=self.prior_work_experience
			d.comments_about_prior_work_experience=self.comments_about_prior_work_experience
			d.technical_qualification=self.technical_qualification
			d.comments_about_technical_qualification=self.comments_about_technical_qualification
			d.tech_overall_impression_and_recommendation=self.tech_overall_impression_and_recommendation
			d.tech_comments_about_overall_impression_and_recommendation=self.tech_comments_about_overall_impression_and_recommendation
			d.tech_result=self.tech_result
			d.insert()


@frappe.whitelist()
def make_technical(source_name, target_doc=None):
	def postprocess(source, target_doc):
		target_doc.naming_series="HR-INT-"
	doclist = get_mapped_doc("Technical Interview", source_name, 	{
		"Technical Interview": {
			"doctype": "HR interview",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"name":"technical_interview_id"
			}
		},
	}, target_doc,postprocess)
	return doclist