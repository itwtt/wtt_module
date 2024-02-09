
from __future__ import unicode_literals
import frappe
from datetime import date
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import date,datetime,timedelta
from num2words import num2words
import json

def execute(filters=None):
	data = []
	columns = get_columns(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	columns=[
		{
			"label": _("Employee Code"),
			"fieldtype": "Link",
			"fieldname": "employee",
			"options":"Farm Employee",
			"width": 100
		},
		{
			"label": _("Employee Name"),
			"fieldtype": "Data",
			"fieldname": "employee_name",
			"width": 150
		},
		{
			"label": _("Total Days"),
			"fieldtype": "Data",
			"fieldname": "total_days",
			"width": 50
		},
		{
			"label": _("Present"),
			"fieldtype": "Data",
			"fieldname": "present",
			"width": 50
		},
		{
			"label": _("Absent"),
			"fieldtype": "Data",
			"fieldname": "absent",
			"width": 50
		},
		{
			"label": _("Half Day"),
			"fieldtype": "Data",
			"fieldname": "half_day",
			"width": 50
		},
		{
			"label": _("Approval Leave"),
			"fieldtype": "Data",
			"fieldname": "approval_leave",
			"width": 50
		},
		{
			"label": _("Payment Days"),
			"fieldtype": "Data",
			"fieldname": "payment_days",
			"width": 50
		},
		{
			"label": _("Salary"),
			"fieldtype": "Currency",
			"fieldname": "salary",
			"width": 100
		},
		{
			"label": _("Rounded"),
			"fieldtype": "Currency",
			"fieldname": "rounded",
			"width": 100
		},
		{
			"label": _("Posting Date"),
			"fieldtype": "Date",
			"fieldname": "posting_date",
			"width": 100
		}
		]
	return columns

def get_data(data, filters):
	data=[]
	trail_data=[]
	daysut=[]
	dd=[]
	emp=[]
	aate=datetime.strptime(str(filters.to_date),"%Y-%m-%d")
	bbte=datetime.strptime(str(filters.from_date),"%Y-%m-%d")
	ttr=((aate+timedelta(days=1))-bbte).days
	doc=frappe.db.sql("SELECT * from `tabFarm Attendance` WHERE attendance_date between %(from_date)s and %(to_date)s and docstatus=1",filters,as_dict=1)
	for i in doc:
		if(i.status=='Present'):
			aa=1
		else:
			aa=0
		if(i.status=='Absent'):
			bb=1
		else:
			bb=0
		if(i.status=='Half Day'):
			cc=1
		else:
			cc=0
		if(frappe.get_value("Farm Employee",i.employee,"status")=='Active'):
			daysut.append({
				"employee":i.employee,
				"employee_name":i.employee_name,
				"present":aa,
				"absent":bb,
				"half_day":cc,
				"payment_days":aa+(cc/2)
				})

	for i in daysut:
		if(i["employee"] not in emp):
			trail_data.append(i)
			emp.append(i["employee"])
		else:
			trail_data[emp.index(i["employee"])]["present"] += i["present"]
			trail_data[emp.index(i["employee"])]["absent"] += i["absent"]
			trail_data[emp.index(i["employee"])]["half_day"] += i["half_day"]
			trail_data[emp.index(i["employee"])]["payment_days"] += i["payment_days"]
	arv=[]
	for i in trail_data:
		sal=frappe.db.get_value('Farm Employee',i["employee"],'salary')
		pd=i["payment_days"]
		al=0
		if(ttr>pd):
			al=frappe.db.get_value('Farm Employee',i["employee"],'approval_leave')
			if(i['half_day']>0):
				al=al-(i['half_day']/2)
				pd=i["payment_days"]+al
			else:
				pd=i["payment_days"]+al
		

		ss=(sal/ttr)*float(pd)

		data.append({
			"employee":i["employee"],
			"employee_name":i["employee_name"],
			"total_days":ttr,
			"present":str(i["present"]),
			"absent":str(i["absent"]),
			"half_day":str(i["half_day"]),
			"payment_days":str(pd),
			"salary":ss,
			"approval_leave":str(al),
			"posting_date":aate.date(),
			"rounded":round(ss)
			})
	return data

@frappe.whitelist()
def create_salary_slip(emp,emp_name,present,absent,half_day,payment_days,salary,posting_date,rounded,approval_leave):
	if not frappe.db.exists({"doctype":"Farm Salary Slip","employee":emp,"posting_date":posting_date}):
		doc=frappe.new_doc("Farm Salary Slip")
		doc.employee=emp
		doc.employee_name=emp_name
		doc.working_days=31
		doc.present_days=str(present)
		doc.absent_days=str(absent)
		doc.payment_days=str(payment_days)
		doc.total=salary
		doc.approval_leave=str(approval_leave)
		doc.posting_date=str(posting_date)
		doc.net_total=rounded
		doc.in_words=num2words(rounded)
		doc.save()
	return []

@frappe.whitelist()
def function(emp,emp_name,posting_date):
	frappe.db.sql("UPDATE `tabFarm Salary Slip` set docstatus=1,workflow_state='Approved' WHERE employee='"+str(emp)+"' and posting_date='"+str(posting_date)+"' ")

@frappe.whitelist()
def additionals(emp,posting_date):
	dialogue=[]
	for i in frappe.db.sql("SELECT * FROM `tabFarm Salary Slip` WHERE employee='"+str(emp)+"' and posting_date='"+str(posting_date)+"' and docstatus!=2 and workflow_state!='Rejected' ",as_dict=1):
		dialogue.append({
		"employee":i.employee,
		"employee_name":i.employee_name,
		"payment_days":i.payment_days,
		"total":i.total
		})
		return dialogue

@frappe.whitelist()
def salary(name):
	to_python = json.loads(name)
	for i in to_python:
		sal = frappe.get_doc("Farm Salary Slip",str(i))
		sal.verified_by = frappe.session.user
		sal.submit()
	frappe.msgprint("Approved")