from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime,date,timedelta
from dateutil.relativedelta import relativedelta
import math
import json

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
		"label": _("Joining Date"),
		"fieldname": "joining_date",
		"fieldtype": "Date",
		"width": 120
		},
		{
		"label": _("After 6 month"),
		"fieldname": "after_six",
		"fieldtype": "Date",
		"width": 120
		},
		{
		"label": _("Less 2023"),
		"fieldname": "less",
		"fieldtype": "Data",
		"width": 100
		},
				{
		"label": _("experience"),
		"fieldname": "experience",
		"fieldtype": "Data",
		"width": 120
		},
		{
		"label": _("Total Days"),
		"fieldname": "total_days",
		"fieldtype": "Float",
		"width": 120
		},
		{
		"label": _("Total Earned Leave"),
		"fieldname": "total_earn",
		"fieldtype": "Float",
		"width": 150
		},
		{
		"label": _("Total Sick Leave"),
		"fieldname": "total_sick",
		"fieldtype": "Float",
		"width": 150
		}
	]

	return columns

def get_data(conditions,data, filters):
	data=[]
	for i in frappe.db.sql("""SELECT name,employee_name,date_of_joining,experience FROM `tabEmployee` WHERE status='Active' AND department!='MD - WTT' and department!='House keeping - WTT'{conditions}""".format(conditions=conditions), as_dict=1):
		date="2023-01-01"
		dd = datetime.strptime(date,"%Y-%m-%d").date()
		new_date='2024-01-01'
		dt = datetime.strptime(new_date,"%Y-%m-%d").date()
		vvvs=''
		if(dd>i.date_of_joining + relativedelta(months=6)):
			vvvs='yes'
		else:
			vvvs='no'
		next_day =  i.date_of_joining + relativedelta(months=6)
		if(i.experience == 'Fresher'):
			if next_day<dd:
				total_sick=6
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
				else:
					vv=0

				if(vv>12):
					vv=12

				if(total_sick>6):
					total_sick=6

			elif next_day>=dt:
				ful_sun=[]
				half_sun=[]
				ful_sun_count=0
				half_sun_count=0

				start_date=next_day
				ed_date ='2024-12-31'
				end_date= datetime.strptime(ed_date,"%Y-%m-%d").date()

				present_days = 0
				work_days=0
				current_date = start_date
				while current_date <= end_date:
				 	# checking if the current day is a weekdays
	
					if current_date.weekday() < 6:
				 		work_days += 1
				 	# incrementing the current day by one day
					current_date += timedelta(days=1)

				# printing the result
				total_days=work_days
				vv=0
				# act_date=((pr+ab)-total_ded)/23.3
				# total_sick=math.floor(float(total_days)/46.6)


				# Get the relativedelta between two dates
				res = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)+1
				total_sick=res*0.5
				if(total_sick>6):
					total_sick=6

			else:
				ful_sun=[]
				half_sun=[]
				ful_sun_count=0
				half_sun_count=0
				for k in frappe.db.sql("SELECT attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(next_day)+"' and attendance_date<='2023-12-31' AND DAYOFWEEK(attendance_date) = 1 and status='Present' and employee='"+str(i.name)+"'",as_dict=1):
					ful_sun.append(k.attendance_date)

				for l in frappe.db.sql("SELECT attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(next_day)+"'  and attendance_date<='2023-12-31' AND DAYOFWEEK(attendance_date) = 1 and status='Half Day' and employee='"+str(i.name)+"'",as_dict=1):
					half_sun.append(l.attendance_date)

				ful_sun_count = len(ful_sun)
				half_sun_count = len(half_sun)
				total_ded = ful_sun_count + (half_sun_count/2)
				query1=frappe.db.sql("SELECT count(name) as count FROM `tabAttendance` where status='Present' and docstatus=1 and employee='"+str(i.name)+"' and attendance_date>='"+str(next_day)+"'  and attendance_date<='2023-12-31'",as_dict=1)
				query2=frappe.db.sql("SELECT count(name) as count FROM `tabAttendance` where status='Half Day' and docstatus=1 and employee='"+str(i.name)+"' and attendance_date>='"+str(next_day)+"'  and attendance_date<='2023-12-31'",as_dict=1)
				pr=query1[0]["count"]
				ab=query2[0]["count"]/2
				present_days = ((pr+ab)-total_ded)
				if(present_days>23.3):
					act_date=((pr+ab)-total_ded)/23.3
					vv = 0.5 * math.floor(float(act_date)/0.5)
				else:
					vv=0

				if(vv>12):
					vv=12

				total_sick=6


		else:
			if(i.experience == 'Experienced'):
				total_sick=6
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
				else:
					vv=0
				if(vv>12):
					vv=12
		data.append({
			'employee':i.name,
			'employee_name':i.employee_name,
			'joining_date':i.date_of_joining,
			'after_six': i.date_of_joining + relativedelta(months=6),
			'less':vvvs,
			'total_days':present_days,
			'total_earn':vv,
			'total_sick':total_sick,
			'experience':i.experience
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

@frappe.whitelist()
def function(rows):
	datas=json.loads(rows)
	for i in datas:
		if(float(i['total_sick'])>0):
			if(frappe.db.exists("Leave Allocation", {"employee":i['employee'],"from_date":(">=", "2024-01-01"),"to_date":("<=", "2024-12-31"),"leave_type":"Sick Leave"})):
				pass
			else:
				if(i['experience'] == 'Fresher'):
					doc=frappe.new_doc("Leave Allocation")
					doc.employee=i['employee']
					doc.leave_type='Sick Leave'
					doc.new_leaves_allocated=i['total_sick']
					doc.from_date=i['after_six']
					doc.to_date='2024-12-31'	
					doc.save()
					frappe.msgprint("Successfully Data Uploaded!")
				else:
					doc=frappe.new_doc("Leave Allocation")
					doc.employee=i['employee']
					doc.leave_type='Sick Leave'
					doc.new_leaves_allocated=i['total_sick']
					doc.from_date='2024-01-01'
					doc.to_date='2024-12-31'	
					doc.save()
					frappe.msgprint("Successfully Data Uploaded!")
		if(float(i['total_earn'])>0):
			if(frappe.db.exists("Leave Allocation", {"employee":i['employee'],"from_date":(">=", "2024-01-01"),"to_date":("<=", "2024-12-31"),"leave_type":"Earned Leave"})):
				pass
			else:
				if(i['experience'] == 'Fresher'):
					doc_2=frappe.new_doc("Leave Allocation")
					doc_2.employee=i['employee']
					doc_2.leave_type='Earned Leave'
					doc_2.new_leaves_allocated=i['total_earn']
					doc_2.from_date='2024-01-01'
					doc_2.to_date='2024-12-31'	
					doc_2.save()	
					frappe.msgprint("Successfully Data Uploaded!")
				else:
					doc_2=frappe.new_doc("Leave Allocation")
					doc_2.employee=i['employee']
					doc_2.leave_type='Earned Leave'
					doc_2.new_leaves_allocated=i['total_earn']
					doc_2.from_date=i['after_six']
					doc_2.to_date='2024-12-31'	
					doc_2.save()	
					frappe.msgprint("Successfully Data Uploaded!")
