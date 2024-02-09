from __future__ import unicode_literals
import frappe
from datetime import date
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import date,datetime,timedelta
import calendar

def execute(filters=None):
	if not filters:
		return [], []
	data = []
	columns = get_columns(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	if(filters.purpose=='Not applied for leave'):
		columns=[
			{
				"label": _("Employee Name"),
				"fieldtype": "Data",
				"fieldname": "employee_name",
				"width": 150
			},
			{
				"label": _("Department"),
				"fieldtype": "Data",
				"fieldname": "department",
				"width": 150
			}
			]
	else:
		columns=[
			{
				"label": _("Date"),
				"fieldtype": "Data",
				"fieldname": "date",
				"width": 150
			},
			{
				"label": _("Employee Name"),
				"fieldtype": "Data",
				"fieldname": "employee_name",
				"width": 150
			},
			{
				"label": _("Department"),
				"fieldtype": "Data",
				"fieldname": "department",
				"width": 150
			},
			{
				"label": _("Status"),
				"fieldtype": "Data",
				"fieldname": "status",
				"width": 150
			}
			]
	return columns

def get_data(data, filters):
	if(filters.purpose=='Not applied for leave'):
		if(filters.month==None):
			frappe.msgprint("oops! I can't get Month")
		else:
			data=[]
			emp=[]
			act=[]
			dd=date.today()
			cc=datetime.strptime(str(filters.month), "%B")
			mm=cc.month
			d1=dd.replace(day=1,month=mm)
			d0=(d1+timedelta(days=32)).replace(day=1)
			d2=d0-timedelta(days=1)
			if(filters.leavetype!=None):
				check = frappe.db.sql("SELECT * from  `tabLeave Request` as aa,`tabLeave table`as bb where aa.name=bb.parent and bb.from_date>='"+str(d1)+"' and bb.to_date<='"+str(d2)+"' and bb.leave_type=%(leavetype)s ",filters, as_dict=1) 
			else:
				check = frappe.db.sql("SELECT * from  `tabLeave Request` as aa,`tabLeave table`as bb where aa.name=bb.parent and bb.from_date>='"+str(d1)+"' and bb.to_date<='"+str(d2)+"' ",filters, as_dict=1) 
			vis=frappe.db.sql("SELECT employee_name,department FROM `tabEmployee` WHERE status='Active'",as_dict=1)
			for name in check:
				emp.append(name.employee_name)#array of Leave Request

			for at in vis:
				act.append(at.employee_name)#array of active employee
				
			for ab in act:
				if ab not in emp:
					if ab not in ["MANAGING DIRECTOR","Priya","Sarnita","Harshini"]:
						data.append({
						"employee_name":ab,
						"department":frappe.db.get_value("Employee",{"employee_name":ab},"department")
						})
	else:
		if(filters.month==None):
			frappe.msgprint("oops! I can't get Month")
		else:
			data=[]			
			dd=date.today()
			cc=datetime.strptime(str(filters.month), "%B")
			mm=cc.month
			d1=dd.replace(day=1,month=mm)-timedelta(days=1)
			d0=(d1+timedelta(days=33)).replace(day=1)
			d2=d0-timedelta(days=2)
			while d1<=d2:
				emp=[]
				act=[]
				d1=d1+timedelta(days=1)
				godf=calendar.day_name[d1.weekday()]
				if(godf!='Sunday'):
					if(filters.department==None):
						leave = frappe.db.sql("SELECT * from `tabAttendance` WHERE status='Absent' and docstatus=1 and attendance_date='"+str(d1)+"' ",filters,as_dict=1)
					else:
						leave = frappe.db.sql("SELECT * from `tabAttendance` WHERE status='Absent' and docstatus=1 and attendance_date='"+str(d1)+"' and department=%(department)s ",filters,as_dict=1)
					for check in leave:
						
						request = frappe.db.sql("SELECT * from `tabLeave Request`as lr,`tabLeave table`as lt WHERE lr.name=lt.parent and lt.from_date='"+str(check.attendance_date)+"' and lr.employee='"+str(check.employee)+"' ",filters,as_dict=1)
						request2 = frappe.db.sql("SELECT * from `tabEmergency Leave`as lr,`tabEmergency Table`as lt WHERE lr.name=lt.parent and lt.from_date='"+str(check.attendance_date)+"' and lr.employee='"+str(check.employee)+"' ",filters,as_dict=1)
						if not request and not request2:
							ddate=str(check.attendance_date)+" 00:00:00"
							ddate2=datetime.strptime(ddate,"%Y-%m-%d %H:%M:%S")
							ddate3=ddate2.replace(hour=23,minute=59,second=59)
							vvgg="Uninformed"
							if(frappe.db.sql("SELECT * FROM `tabOn duty request` WHERE employee='"+str(check.employee)+"' and from_time>'"+str(ddate2)+"' and to_time<'"+str(ddate3)+"' ",as_dict=1)):
								vvgg="On Duty"

							if(frappe.db.get_value("Employee",check.employee,"status")=='Active'):
								if(check.in_time==None and check.out_time==None):
									data.append({
										"employee_name":check.employee_name,
										"department":check.department,
										"status":vvgg,
										"date":str(d1)
										})
								else:
									data.append({
										"employee_name":check.employee_name,
										"department":check.department,
										"status":"Punch Missed",
										"date":str(d1)
										})
	return data