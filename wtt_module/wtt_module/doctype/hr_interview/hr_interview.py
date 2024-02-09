# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
class HRinterview(Document):
	def on_submit(self):
		doc=frappe.db.sql("SELECT * FROM `tabInterview process` WHERE job_id='"+self.job_id+"'",as_dict=1)
		if(doc):
			# frappe.msgprint(self.hr_result)
			query=frappe.db.sql("UPDATE `tabInterview process` SET hr_interview_id='"+self.name+"',hr_interviewer='"+self.hr_interviewer+"',educational_background='"+self.educational_background+"',comments_about_educational_background='"+self.comments_about_educational_background+"',verbal_communication='"+self.verbal_communication+"',comments_about_verbal_communication='"+comments_about_verbal_communication+"',candidate_interest_5_out_of='"+self.candidate_interest_5_out_of+"',comments_about_candidate_interest='"+self.comments_about_candidate_interest+"',knowledge_of_organization='"+self.knowledge_of_organization+"',comments_about_knowledge_of_organization='"+self.comments_about_knowledge_of_organization+"',teambuilding_interpersonal_skills='"+self.teambuilding_interpersonal_skills+"',comments_about_teambuildinginterpersonal_skills='"+self.comments_about_teambuildinginterpersonal_skills+"',initiative='"+self.initiative+"',hr_overall_impression_and_recommendation='"+self.overall_impression_and_recommendation+"',hr_comments_about_overall_impression_and_recommendation='"+self.comments_about_overall_impression_and_recommendation+"',hr_result='"+self.hr_result+"' WHERE job_id='"+self.job_id+"'",as_dict=1)
		else:
			d=frappe.new_doc("Interview process")
			d.candidate_name=self.candidate_name
			d.position=self.position
			d.other_post=self.other_post																					
			d.date=self.date
			d.job_id=self.job_id
			d.hr_interview_id=self.name
			d.hr_interviewer=self.hr_interviewer
			d.technical_interviewer=self.technical_interviewer
			d.technical_interviewer_name=self.technical_interviewer_name
			d.educational_background=self.educational_background
			d.comments_about_educational_background=self.comments_about_educational_background
			d.verbal_communication=self.verbal_communication
			d.comments_about_verbal_communication=self.comments_about_verbal_communication
			d.candidate_interest_5_out_of=self.candidate_interest_5_out_of
			d.comments_about_candidate_interest=self.comments_about_candidate_interest
			d.knowledge_of_organization=self.knowledge_of_organization
			d.comments_about_knowledge_of_organization=self.comments_about_knowledge_of_organization
			d.teambuilding_interpersonal_skills=self.teambuilding_interpersonal_skills
			d.comments_about_teambuildinginterpersonal_skills=self.comments_about_teambuildinginterpersonal_skills
			d.initiative=self.initiative
			d.comments_about_intiative=self.comments_about_intiative
			d.hr_overall_impression_and_recommendation=self.overall_impression_and_recommendation
			d.hr_comments_about_overall_impression_and_recommendation=self.comments_about_overall_impression_and_recommendation
			d.hr_result=self.hr_result
			d.insert()


@frappe.whitelist()
def make_shortlisted(source_name, target_doc=None):
	def postprocess(source, target_doc):
		target_doc.naming_series="TECH-INT-"
	doclist = get_mapped_doc("HR interview", source_name, 	{
		"HR interview": {
			"doctype": "Technical Interview",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"name":"hr_interview_id"
			}
		},
	}, target_doc,postprocess)
	return doclist
