# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import itertools
class EmployeeTTB(Document):
	pass
@frappe.whitelist()
def get_score(val):
	emp=[]
	query1 = frappe.db.sql("SELECT p.employee,p.employee_name,ch.criteria,ch.your_points from `tabTTB Criteria`as p,`tabAttitude Table`as ch Where p.name=ch.parent ",as_dict=1)
	for i in query1:
		if(i.criteria=='Anger Management'):
			emp.append({
				"employee":i.employee,
				"employee_name":i.employee_name
				})
	return emp

		
	
@frappe.whitelist()
def get_attitude_score(val):
	emp=[]
	en=[]
	a1=[]
	a2=[]
	a3=[]
	a4=[]
	a5=[]
	a6=[]
	query1 = frappe.db.sql("SELECT p.employee,p.employee_name,ch.criteria,ch.your_points from `tabTTB Criteria`as p,`tabAttitude Table`as ch Where p.name=ch.parent ",as_dict=1)
	for i in query1:
		if(i.criteria=='Anger Management'):
			emp.append(i.employee)
			en.append(i.employee_name)
			a1.append(i.your_points)

		if(i.criteria=='Goal Oriented'):
			a2.append(i.your_points)

		if(i.criteria=='Initiative'):
			a3.append(i.your_points)

		if(i.criteria=='Positivity'):
			a4.append(i.your_points)

		if(i.criteria=='Responsible'):
			a5.append(i.your_points)

		if(i.criteria=='Sense of Humour'):
			a6.append(i.your_points)

	ar=[]
	for (i,j,k,l,m,n,o,p) in itertools.zip_longest(emp,a1,a2,a3,a4,a5,a6,en):
		ar.append({
			"employee":i,
			"employee_name":p,
			"anger_management":j,
			"goal_oriented":k,
			"initiative":l,
			"positivity":m,
			"responsible":n,
			"sense_of_humour":o
			})

	return ar
	

@frappe.whitelist()
def get_personal_score(val):
	emp=[]
	en=[]
	a1=[]
	a2=[]
	a3=[]
	
	query1 = frappe.db.sql("SELECT p.employee,p.employee_name,ch.criteria,ch.your_points from `tabTTB Criteria`as p,`tabPersonal Table`as ch Where p.name=ch.parent ",as_dict=1)
	for i in query1:
		if(i.criteria=='Discipline (Healthy practises)'):
			emp.append(i.employee)
			en.append(i.employee_name)
			a1.append(i.your_points)

		if(i.criteria=='Hygiene'):
			a2.append(i.your_points)

		if(i.criteria=='Professional Attire'):
			a3.append(i.your_points)


	ar=[]
	for (i,j,k,l,p) in itertools.zip_longest(emp,a1,a2,a3,en):
		ar.append({
			"employee":i,
			"employee_name":p,
			"discipline":j,
			"hygiene":k,
			"attire":l
			})

	return ar

@frappe.whitelist()
def get_personal_score(val):
	emp=[]
	en=[]
	a1=[]
	a2=[]
	a3=[]
	
	query1 = frappe.db.sql("SELECT p.employee,p.employee_name,ch.criteria,ch.your_points from `tabTTB Criteria`as p,`tabPersonal Table`as ch Where p.name=ch.parent ",as_dict=1)
	for i in query1:
		if(i.criteria=='Discipline (Healthy practises)'):
			emp.append(i.employee)
			en.append(i.employee_name)
			a1.append(i.your_points)

		if(i.criteria=='Hygiene'):
			a2.append(i.your_points)

		if(i.criteria=='Professional Attire'):
			a3.append(i.your_points)


	ar=[]
	for (i,j,k,l,p) in itertools.zip_longest(emp,a1,a2,a3,en):
		ar.append({
			"employee":i,
			"employee_name":p,
			"discipline":j,
			"hygiene":k,
			"attire":l
			})

	return ar
	
@frappe.whitelist()
def get_skill_score(val):
	emp=[]
	en=[]
	a1=[]
	a2=[]
	a3=[]
	a4=[]
	a5=[]
	a6=[]
	a7=[]
	a8=[]
	a9=[]
	
	query1 = frappe.db.sql("SELECT p.employee,p.employee_name,ch.criteria,ch.your_points from `tabTTB Criteria`as p,`tabSkill Table`as ch Where p.name=ch.parent ",as_dict=1)
	for i in query1:
		if(i.criteria=='Analytical'):
			emp.append(i.employee)
			en.append(i.employee_name)
			a1.append(i.your_points)

		if(i.criteria=='Appreciation'):
			a2.append(i.your_points)

		if(i.criteria=='Consistancy'):
			a3.append(i.your_points)

		if(i.criteria=='Creativity'):
			a4.append(i.your_points)

		if(i.criteria=='Focus'):
			a5.append(i.your_points)

		if(i.criteria=='Language'):
			a6.append(i.your_points)

		if(i.criteria=='Organized working'):
			a7.append(i.your_points)

		if(i.criteria=='Proactiveness'):
			a8.append(i.your_points)

		if(i.criteria=='Time Management'):
			a9.append(i.your_points)


	ar=[]
	for (i,j,k,l,m,n,o,p,q,r,s) in itertools.zip_longest(emp,en,a1,a2,a3,a4,a5,a6,a7,a8,a9):
		ar.append({
			"employee":i,
			"employee_name":j,
			"a1":k,
			"a2":l,
			"a3":m,
			"a4":n,
			"a5":o,
			"a6":p,
			"a7":q,
			"a8":r,
			"a9":s
			})

	return ar

@frappe.whitelist()
def get_team_score(val):
	emp=[]
	en=[]
	a1=[]
	a2=[]
	a3=[]
	a4=[]
	a5=[]
	a6=[]
	a7=[]
	
	query1 = frappe.db.sql("SELECT p.employee,p.employee_name,ch.criteria,ch.your_points from `tabTTB Criteria`as p,`tabTeam Table`as ch Where p.name=ch.parent ",as_dict=1)
	for i in query1:
		if(i.criteria=='Caring Team Members'):
			emp.append(i.employee)
			en.append(i.employee_name)
			a1.append(i.your_points)

		if(i.criteria=='Commanding'):
			a2.append(i.your_points)

		if(i.criteria=='Ego Balancing'):
			a3.append(i.your_points)

		if(i.criteria=='Feed back in team'):
			a4.append(i.your_points)

		if(i.criteria=='Leadership'):
			a5.append(i.your_points)

		if(i.criteria=='Participation'):
			a6.append(i.your_points)

		if(i.criteria=='Relationship Maintenance'):
			a7.append(i.your_points)

	ar=[]
	for (i,j,k,l,m,n,o,p,q) in itertools.zip_longest(emp,en,a1,a2,a3,a4,a5,a6,a7):
		ar.append({
			"employee":i,
			"employee_name":j,
			"a1":k,
			"a2":l,
			"a3":m,
			"a4":n,
			"a5":o,
			"a6":p,
			"a7":q
			})

	return ar

@frappe.whitelist()
def get_knowledge_score(val):
	emp=[]
	en=[]
	a1=[]
	a2=[]
	a3=[]
	
	query1 = frappe.db.sql("SELECT p.employee,p.employee_name,ch.criteria,ch.your_points from `tabTTB Criteria`as p,`tabWork knowledge`as ch Where p.name=ch.parent ",as_dict=1)
	for i in query1:
		if(i.criteria=='Involvement'):
			emp.append(i.employee)
			en.append(i.employee_name)
			a1.append(i.your_points)

		if(i.criteria=='Learning Curve'):
			a2.append(i.your_points)

		if(i.criteria=='Update in Field'):
			a3.append(i.your_points)


	ar=[]
	for (i,j,k,l,m) in itertools.zip_longest(emp,en,a1,a2,a3):
		ar.append({
			"employee":i,
			"employee_name":j,
			"a1":k,
			"a2":l,
			"a3":m
			})

	return ar

@frappe.whitelist()
def get_performance_score(val):
	emp=[]
	en=[]
	a1=[]
	a2=[]
	a3=[]
	a4=[]
	a5=[]
	
	query1 = frappe.db.sql("SELECT p.employee,p.employee_name,ch.criteria,ch.your_points from `tabTTB Criteria`as p,`tabWork performance`as ch Where p.name=ch.parent ",as_dict=1)
	for i in query1:
		if(i.criteria=='Attendance'):
			emp.append(i.employee)
			en.append(i.employee_name)
			a1.append(i.your_points)

		if(i.criteria=='Punctuality'):
			a2.append(i.your_points)

		if(i.criteria=='Reporting'):
			a3.append(i.your_points)

		if(i.criteria=='Result Driven'):
			a4.append(i.your_points)

		if(i.criteria=='Safety'):
			a5.append(i.your_points)

	ar=[]
	for (i,j,k,l,m,n,o) in itertools.zip_longest(emp,en,a1,a2,a3,a4,a5):
		ar.append({
			"employee":i,
			"employee_name":j,
			"a1":k,
			"a2":l,
			"a3":m,
			"a4":n,
			"a5":o
			})

	return ar
	