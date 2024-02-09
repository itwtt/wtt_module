from __future__ import unicode_literals

import frappe


@frappe.whitelist()
def get_value(fr_date,to_date):
	arr=[]
	query=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE workflow_state='Created' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
	for i in query:
		arr.append({
			"created":i
			})
	query2=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE workflow_state='Approved by HOD' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
	for i in query2:
		arr.append({
			"approved_hod":i
			})

	query3=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE workflow_state='Approved' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
	for i in query3:
		arr.append({
			"approved":i
			})
	return arr

@frappe.whitelist()
def get_value1(emp,fr_date,to_date):
	arr=[]
	for k in frappe.db.sql("SELECT user_id FROM `tabEmployee` WHERE employee='"+emp+"'",as_dict=1):
		query=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE owner='"+str(k.user_id)+"' and workflow_state='Created' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
		for i in query:
			arr.append({
				"created":i
				})
		query2=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE owner='"+str(k.user_id)+"' and workflow_state='Approved by HOD' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
		for i in query2:
			arr.append({
				"approved_hod":i
				})

		query3=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE owner='"+str(k.user_id)+"' and workflow_state='Approved' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
		for i in query3:
			arr.append({
				"approved":i
				})
	return arr

@frappe.whitelist()
def get_value2(project,fr_date,to_date):
	arr=[]
	query=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE project='"+str(project)+"' and workflow_state='Created' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
	for i in query:
		arr.append({
			"created":i
			})
	query2=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE project='"+str(project)+"' and workflow_state='Approved by HOD' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
	for i in query2:
		arr.append({
			"approved_hod":i
			})

	query3=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE project='"+str(project)+"' and workflow_state='Approved' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
	for i in query3:
		arr.append({
			"approved":i
			})
	return arr

@frappe.whitelist()
def get_value3(emp,project,fr_date,to_date):
	arr=[]
	for k in frappe.db.sql("SELECT user_id FROM `tabEmployee` WHERE employee='"+emp+"'",as_dict=1):
		query=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE owner='"+str(k.user_id)+"' and project='"+str(project)+"' and workflow_state='Created' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
		for i in query:
			arr.append({
				"created":i
				})
		query2=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE owner='"+str(k.user_id)+"' and project='"+str(project)+"' and workflow_state='Approved by HOD' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
		for i in query2:
			arr.append({
				"approved_hod":i
				})

		query3=frappe.db.sql("SELECT count(name) FROM `tabMaterial Request` WHERE owner='"+str(k.user_id)+"' and project='"+str(project)+"' and workflow_state='Approved' and creation between '"+str(fr_date)+"' and '"+str(to_date)+"'")
		for i in query3:
			arr.append({
				"approved":i
				})
	return arr