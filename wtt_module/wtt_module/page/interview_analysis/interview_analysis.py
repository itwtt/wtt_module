from __future__ import unicode_literals

import frappe


@frappe.whitelist()
def get_interview(emp):
	val="success"
	return val
	'''
	arr=[]
	query=frappe.db.sql("SELECT candidate_name,position,other_post,hr_interviewer,technical_interviewer,educational_background,prior_work_experience,technical_qualification,verbal_communication,candidate_interest_5_out_of,knowledge_of_organization,teambuilding_interpersonal_skills,initiative,hr_overall_impression_and_recommendation,hr_comments_about_overall_impression_and_recommendation,hr_result,tech_overall_impression_and_recommendation,tech_comments_about_overall_impression_and_recommendation,tech_result FROM `tabInterview process` WHERE name='"+str(emp)+"'")
	for i in query:
		arr.append({
			"candidate_name":i.candidate_name
			"position":i.position
			"other_post":i.other_post
			"hr_interviewer":i.hr_interviewer
			"technical_interviewer":i.technical_interviewer
			"educational_background":i.educational_background
			"prior_work_experience":i.prior_work_experience
			"technical_qualification":i.technical_qualification
			"verbal_communication":i.verbal_communication
			"candidate_interest_5_out_of":i.candidate_interest_5_out_of
			"knowledge_of_organization":i.knowledge_of_organization
			"teambuilding_interpersonal_skills":i.teambuilding_interpersonal_skills
			"initiative":i.initiative
			"hr_overall_impression_and_recommendation":i.hr_overall_impression_and_recommendation
			"hr_comments_about_overall_impression_and_recommendation":i.hr_comments_about_overall_impression_and_recommendation
			"hr_result":i.hr_result
			"tech_overall_impression_and_recommendation":i.tech_overall_impression_and_recommendation
			"tech_comments_about_overall_impression_and_recommendation":i.tech_comments_about_overall_impression_and_recommendation
			"tech_result":i.tech_result
			})
	return arr
	'''