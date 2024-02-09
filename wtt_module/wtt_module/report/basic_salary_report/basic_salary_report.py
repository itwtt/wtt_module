# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime

def execute(filters=None):
	if not filters:
		return [], []
	data = []
	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data = get_data(conditions,data,filters)
	return columns, data

@frappe.whitelist()
def get_columns(filters):
	columns = [
	{
	"label": _("Employee"),
	"fieldname": "employee",
	"fieldtype": "Link",
	"options":"Employee",
	"width": 150
	},
	{
	"label": _("Employee Name"),
	"fieldname": "employee_name",
	"fieldtype": "Data",
	"width": 150
	}
	]
	val=frappe.db.sql("SELECT posting_date FROM `tabSalary Slip` WHERE workflow_state='Approved' AND employee='WTT1199' and posting_date>=%(from_date)s and posting_date<=%(to_date)s",filters,as_dict=1)
	for i in val:
		columns.append({
		"fieldname": str(i.posting_date)+"",
		"label": ""+str(i.posting_date),
		"fieldtype": "HTML",
		"width": 120
		})

	columns.append({
	"label": _("Basic"),
	"fieldtype": "Data",
	"fieldname": "basic_total",
	"width": 100
	})
	
	columns.append({
	"label": _("Total Basic"),
	"fieldtype": "Data",
	"fieldname": "total_basic",
	"width": 100
	})

	columns.append({
	"label": _("Bonus"),
	"fieldtype": "Data",
	"fieldname": "bonus",
	"width": 100
	})

	return columns

def get_data(conditions,data, filters):
	emp=[]
	for q in frappe.db.sql("SELECT employee FROM `tabEmployee` WHERE status='Active' and date_of_joining<='2023-01-01'",as_dict=1):
		emp.append(q.employee)
	data=[]
	ar=[]
	to_be_compared_items = frappe.db.sql("""SELECT s.posting_date,s.name,s.employee,s.employee_name,s.rounded_total,sd.amount from `tabSalary Slip` as s INNER JOIN `tabSalary Detail` as sd ON s.name=sd.parent where sd.salary_component='Basic Salary' and s.workflow_state="Approved"{conditions}""".format(conditions=conditions), as_dict=1)
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


	for item in unique_item:
		column = {}
		for datum in to_be_compared_items:
			if item == datum.employee:
				column['employee'] = datum.employee
				column['employee_name'] = datum.employee_name
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
		data.append(column)
	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " AND s.posting_date>='%s'" % filters.get('from_date')

	if filters.get("to_date"):
		conditions += " AND s.posting_date<='%s'" % filters.get('to_date')

	if filters.get("employee"):
		conditions += " AND s.employee='%s'" % filters.get('employee')

	if filters.get("branch"):
		conditions += " AND s.branch='%s'" % filters.get('branch')

	return conditions
