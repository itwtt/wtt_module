# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
class QuestionsforInterview(Document):
	pass


@frappe.whitelist()
def make_candidate_list(source_name, target_doc=None):
	doclist = get_mapped_doc("Job App", source_name, 	{
		"Job App": {
			"doctype": "Questions for Interview",
			"validation": {
				"docstatus": ["=", 0]
			},
			"field_map": {
				"name":"job_id",
				"applying_post":"position"
			}
		},
	}, target_doc)
	return doclist

@frappe.whitelist()
def make_query():
	ar=[]
	query1=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Behavioral' ORDER BY RAND() LIMIT 2",as_dict=1)
	for i in query1:
		ar.append({
			"question1":i.questions
		})

	query2=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Communication Skills' ORDER BY RAND() LIMIT 2",as_dict=1)
	for j in query2:
		ar.append({
			"question1":j.questions
		})

	query3=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Emotional Intelligence' ORDER BY RAND() LIMIT 2",as_dict=1)
	for k in query3:
		ar.append({
			"question1":k.questions
		})

	query4=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Leadership' ORDER BY RAND() LIMIT 2",as_dict=1)
	for l in query4:
		ar.append({
			"question1":l.questions
		})

	query5=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Situational' ORDER BY RAND() LIMIT 1",as_dict=1)
	for m in query5:
		ar.append({
			"question1":m.questions
		})

	query6=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Stress' ORDER BY RAND() LIMIT 1",as_dict=1)
	for n in query6:
		ar.append({
			"question1":n.questions
		})
	return ar


@frappe.whitelist()
def make_query_managers():
	arr=[]
	query0=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Manager Level' ORDER BY RAND() LIMIT 2",as_dict=1)
	for u in query0:
		arr.append({
			"question2":u.questions
		})

	query1=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Behavioral' ORDER BY RAND() LIMIT 2",as_dict=1)
	for i in query1:
		arr.append({
			"question2":i.questions
		})

	query2=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Communication Skills' ORDER BY RAND() LIMIT 2",as_dict=1)
	for j in query2:
		arr.append({
			"question2":j.questions
		})

	query3=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Emotional Intelligence' ORDER BY RAND() LIMIT 1",as_dict=1)
	for k in query3:
		arr.append({
			"question2":k.questions
		})

	query4=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Leadership' ORDER BY RAND() LIMIT 1",as_dict=1)
	for l in query4:
		arr.append({
			"question2":l.questions
		})

	query5=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Situational' ORDER BY RAND() LIMIT 1",as_dict=1)
	for m in query5:
		arr.append({
			"question2":m.questions
		})

	query6=frappe.db.sql("SELECT questions FROM `tabInterview Questions` WHERE question_type='Stress' ORDER BY RAND() LIMIT 1",as_dict=1)
	for n in query6:
		arr.append({
			"question2":n.questions
		})
	return arr