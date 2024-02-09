# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Bonus(Document):
	pass


@frappe.whitelist()
def get_bonus(fr_date,to_date):
	emp=[]
	for q in frappe.db.sql("SELECT employee FROM `tabEmployee` WHERE status='Active' and date_of_joining<='"+str(to_date)+"'",as_dict=1):
		emp.append(q.employee)
	data=[]
	ar=[]
	to_be_compared_items = frappe.db.sql("SELECT s.posting_date,s.name,s.employee,s.employee_name,s.branch,s.rounded_total,s.payment_days,sd.amount from `tabSalary Slip` as s INNER JOIN `tabSalary Detail` as sd ON s.name=sd.parent where sd.salary_component='Basic Salary' and s.workflow_state='Approved' and s.posting_date>='"+str(fr_date)+"' and s.posting_date<='"+str(to_date)+"'", as_dict=1)
	items_dict = {}
	temp_list = []
	dummy_rate=[]
	low_amt=[]
	for item in to_be_compared_items:
		if item.employee in emp:
			temp_list.append(item.employee)
	unique_item = set(temp_list)

	employee_totals = {}
	
	for item in to_be_compared_items:
		if item.employee in emp:
			if item.employee not in employee_totals:
				employee_totals[item.employee] = 0
			employee_totals[item.employee] += item.amount

	total_present = {}

	for item in to_be_compared_items:
		if item.employee in emp:
			if item.employee not in total_present:
				total_present[item.employee] = 0
			total_present[item.employee] += item.payment_days

	for item in unique_item:
		column = {}
		for datum in to_be_compared_items:
			if item == datum.employee:
				column['employee'] = datum.employee
				column['employee_name'] = datum.employee_name
				column['branch'] = datum.branch
				column[str(datum.posting_date)+''] = datum.amount
				column['basic_total'] = '-'
				if(datum.employee == 'WTT1278' or datum.employee == 'WTT1301'):
					column['basic_total'] = round(employee_totals[item],2)
				if(datum.employee == 'WTT1278'):
					rr = (employee_totals[item] - 45000) + 11250
					column['total_basic'] = round(rr,2)
					column['bonus'] = round((rr * 0.0833),2)
				elif(datum.employee == 'WTT1301'):
					cc = (employee_totals[item] - 40500)+10125
					column['total_basic'] = round(cc,2)
					column['bonus'] = round((cc * 0.0833),2)
				else:
					column['total_basic'] = round(employee_totals[item],2)
					column['bonus'] = round((employee_totals[item] * 0.0833),2)
				column['total_present'] = round(total_present[item],2)
		data.append(column)
	return data