from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime
import math

def execute(filters=None):
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
		"width": 180
		},
		{
		"label": _("Employee Name"),
		"fieldname": "employee_name",
		"fieldtype": "Data",
		"width": 180
		},
		{
		"label": _("Total Days"),
		"fieldname": "total_days",
		"fieldtype": "Float",
		"width": 180
		},
		{
		"label": _("Total Earned Leave"),
		"fieldname": "total_earn",
		"fieldtype": "Float",
		"width": 180
		},
	]

	return columns

def get_data(conditions,data, filters):
	data=[]
	for i in frappe.db.sql("""SELECT name,employee_name FROM `tabEmployee` WHERE status='Active' AND department!='MD - WTT' and department!='House keeping - WTT'{conditions}""".format(conditions=conditions), as_dict=1):
		ful_sun=[]
		half_sun=[]
		ful_sun_count=0
		half_sun_count=0
		for k in frappe.db.sql("SELECT attendance_date FROM `tabAttendance` WHERE attendance_date>='2023-01-01' and attendance_date<='2023-12-31' AND DAYOFWEEK(attendance_date) = 1 and status='Present' and employee='"+str(i.name)+"'",as_dict=1):
			ful_sun.append(k.attendance_date)

		for l in frappe.db.sql("SELECT attendance_date FROM `tabAttendance` WHERE attendance_date>='2023-01-01' and attendance_date<='2023-12-31' AND DAYOFWEEK(attendance_date) = 1 and status='Half Day' and employee='"+str(i.name)+"'",as_dict=1):
			half_sun.append(l.attendance_date)

		ful_sun_count = len(ful_sun)
		half_sun_count = len(half_sun)
		total_ded = ful_sun_count + (half_sun_count/2)
		query1=frappe.db.sql("SELECT count(name) as count FROM `tabAttendance` where status='Present' and docstatus=1 and employee='"+str(i.name)+"' and attendance_date>='2023-01-01' and attendance_date<='2023-12-31'",as_dict=1)
		query2=frappe.db.sql("SELECT count(name) as count FROM `tabAttendance` where status='Half Day' and docstatus=1 and employee='"+str(i.name)+"' and attendance_date>='2023-01-01' and attendance_date<='2023-12-31'",as_dict=1)
		pr=query1[0]["count"]
		ab=query2[0]["count"]/2
		present_days = ((pr+ab)-total_ded)
		if(present_days>23.3):
			act_date=((pr+ab)-total_ded)/23.3
			vv = 0.5 * math.floor(float(act_date)/0.5)
			if(vv>12):
				vv=12
		else:
			vv=0
		data.append({
			'employee':i.name,
			'employee_name':i.employee_name,
			'total_days':present_days,
			'total_earn':vv
		})

	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("employee"):
		conditions += " AND name='%s'" % filters.get('employee')

	if filters.get("department"):
		conditions += " AND department='%s'" % filters.get('department')

	if filters.get("branch"):
		conditions += " AND branch='%s'" % filters.get('branch')

	return conditions