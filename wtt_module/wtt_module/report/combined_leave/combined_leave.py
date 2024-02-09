from __future__ import unicode_literals
import frappe
from datetime import datetime,date,timedelta
from frappe.utils import getdate
import calendar
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
import json

def execute(filters=None):		
	# if not filters:
	# 	return [], []
	data = []
	columns = get_columns(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	columns=[
		{
			"label": _("Employee"),
			"fieldtype": "Data",
			"fieldname": "employee",
			"width": 150
		},
		{
			"label": _("Counts/ Dates"),
			"fieldtype": "Data",
			"fieldname": "count",
			"width": 200
		},
		# {
		# 	"label": _("Counts"),
		# 	"fieldtype": "Data",
		# 	"fieldname": "times",
		# 	"width": 200
		# }
	]
	
	return columns

def get_data(data, filters):
	data=[]
	datum=[]
	hoda=[]
	sat=[]
	mon=[]
	query=frappe.db.sql("SELECT distinct(holiday_date)as hd from `tabHoliday` where parent='Common Holidays for 2022' ",as_dict=1)
	for i in query:
		hoda.append(i)

	dt = date(2022, 1, 1) 
	df = date(2022, 1, 1) 
	dt += timedelta(days = 5 - dt.weekday())  
	df += timedelta(days = 7 - dt.weekday())  
	while dt.year == 2022:
		dt += timedelta(days = 7)
		sat.append(str(dt))
		df += timedelta(days = 7)
		mon.append(str(df))



	emp=[]
	for km in frappe.db.sql("SELECT distinct(name) as employee,employee_name from `tabEmployee` WHERE status='Active' ORDER BY employee_name",as_dict=1):
		cc=0
		
		for i in range(53):
				
			if(sat[i] in ['2022-01-15']):
				sat[i]=getdate(sat[i])-timedelta(days=1)
			if(mon[i] in ['2022-08-15','2022-10-24']):
				mon[i]=getdate(mon[i])+timedelta(days=1)
			if(filters.day_name=="Both"):
				if((frappe.db.exists("Attendance", {"employee": km.employee, "attendance_date": sat[i],"status":"Absent"})) and (frappe.db.exists("Attendance", {"employee": km.employee, "attendance_date": mon[i],"status":"Absent"}))):
					cc+=1
					if(km.employee_name not in emp):
						datum.append({})
						emp.append(km.employee_name)
						datum.append({
							"employee":km.employee_name,
							"count":str(getdate(sat[i]).strftime("%b %d"))+", "+str(getdate(mon[i]).strftime("%b %d"))
							})
					else:
						datum.append({"count":str(getdate(sat[i]).strftime("%b %d"))+", "+str(getdate(mon[i]).strftime("%b %d"))})
						
			elif(filters.day_name=="Saturday"):
				
				if((frappe.db.exists("Attendance", {"employee": km.employee, "attendance_date": sat[i],"status":"Absent"}))):
					cc+=1
					if(km.employee_name not in emp):
						datum.append({})
						emp.append(km.employee_name)
						datum.append({
							"employee":km.employee_name,
							"count":str(getdate(sat[i]).strftime("%b %d"))
							})
					else:
						datum.append({"count":str(getdate(sat[i]).strftime("%b %d"))})
						

			elif(filters.day_name=="Monday"):
				
				if((frappe.db.exists("Attendance", {"employee": km.employee, "attendance_date": mon[i],"status":"Absent"}))):
					cc+=1
					if(km.employee_name not in emp):
						datum.append({})
						emp.append(km.employee_name)
						datum.append({
							"employee":km.employee_name,
							"count":str(getdate(mon[i]).strftime("%b %d"))
							})
					else:
						datum.append({"count":str(getdate(mon[i]).strftime("%b %d"))})
		
		if(filters.total==1):
			if(cc>=1):
				data.append({"employee":km.employee_name,"count":str(cc)})
		else:
			data=datum


	

			
	return data

