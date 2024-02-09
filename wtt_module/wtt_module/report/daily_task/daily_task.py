from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from datetime import datetime,timedelta
from frappe.desk.reportview import build_match_conditions
from frappe.utils import getdate

def execute(filters=None):
    if not filters:
        return [], []
    data = []
    columns = get_columns(filters)
    data = get_data(data,filters)
    return columns, data

def get_columns(filters):
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
        },
        {
            "label": _("Assigned Date"),
            "fieldtype": "Data",
            "fieldname": "assigned_date",
            "width": 150
        },
        {
            "label": _("Expected Date"),
            "fieldtype": "Data",
            "fieldname": "expected_date",
            "width": 150
        },
        {
            "label": _("Task"),
            "fieldtype": "Data",
            "fieldname": "task",
            "width": 250
        },
        {
            "label": _("Task Description"),
            "fieldtype": "Data",
            "fieldname": "task_description",
            "width": 200
        },
        {
            "label": _("Status"),
            "fieldtype": "Data",
            "fieldname": "status",
            "width": 150
        },

    ]
    
    return columns
def get_data(data,filters):
    data=[]
    emp=[]
    if(filters.employee==None):
        if(filters.status==None):
            if(filters.department==None):
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assign_date,bb.status,bb.expected_date,bb.type_of_work,bb.description from `tabTask Assignment`as aa,`tabWork table`as bb WHERE aa.name=bb.parent AND bb.assign_date>=%(from_date)s and bb.assign_date<=%(to_date)s ORDER BY aa.employee_name",filters,as_dict=1)
            else:
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assign_date,bb.status,bb.expected_date,bb.type_of_work,bb.description from `tabTask Assignment`as aa,`tabWork table`as bb WHERE aa.name=bb.parent AND bb.assign_date>=%(from_date)s and bb.assign_date<=%(to_date)s and aa.department=%(department)s ORDER BY aa.employee_name",filters,as_dict=1)
        else:
            if(filters.department==None):
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assign_date,bb.status,bb.expected_date,bb.type_of_work,bb.description from `tabTask Assignment`as aa,`tabWork table`as bb WHERE aa.name=bb.parent AND bb.assign_date>=%(from_date)s and bb.assign_date<=%(to_date)s and bb.status=%(status)s ORDER BY aa.employee_name",filters,as_dict=1)
            else:
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assign_date,bb.status,bb.expected_date,bb.type_of_work,bb.description from `tabTask Assignment`as aa,`tabWork table`as bb WHERE aa.name=bb.parent AND bb.assign_date>=%(from_date)s and bb.assign_date<=%(to_date)s and bb.status=%(status)s and aa.department=%(department)s ORDER BY aa.employee_name",filters,as_dict=1)
    else:
        if(filters.status==None):
            if(filters.department==None):
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assign_date,bb.status,bb.expected_date,bb.type_of_work,bb.description from `tabTask Assignment`as aa,`tabWork table`as bb WHERE aa.name=bb.parent AND bb.assign_date>=%(from_date)s and bb.assign_date<=%(to_date)s and aa.employee=%(employee)s ORDER BY aa.employee_name",filters,as_dict=1)
            else:
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assign_date,bb.status,bb.expected_date,bb.type_of_work,bb.description from `tabTask Assignment`as aa,`tabWork table`as bb WHERE aa.name=bb.parent AND bb.assign_date>=%(from_date)s and bb.assign_date<=%(to_date)s and aa.employee=%(employee)s and aa.department=%(department)s ORDER BY aa.employee_name",filters,as_dict=1)
        else:
            if(filters.department==None):
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assign_date,bb.status,bb.expected_date,bb.type_of_work,bb.description from `tabTask Assignment`as aa,`tabWork table`as bb WHERE aa.name=bb.parent AND bb.assign_date>=%(from_date)s and bb.assign_date<=%(to_date)s and aa.employee=%(employee)s and bb.status=%(status)s ORDER BY aa.employee_name",filters,as_dict=1)
            else:
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assign_date,bb.status,bb.expected_date,bb.type_of_work,bb.description from `tabTask Assignment`as aa,`tabWork table`as bb WHERE aa.name=bb.parent AND bb.assign_date>=%(from_date)s and bb.assign_date<=%(to_date)s and aa.employee=%(employee)s and bb.status=%(status)s and aa.department=%(department)s ORDER BY aa.employee_name",filters,as_dict=1)

    for i in query:
        if(i.employee_name not in emp):
            emp.append(i.employee_name)
            data.append({
                "employee_name":i.employee_name,
                "department":i.department,
                "assigned_date":getdate(i.assign_date).strftime("%d-%m-%Y"),
                "expected_date": getdate(i.expected_date).strftime("%d-%m-%Y"),
                "task":i.type_of_work,
                "task_description":i.description,
                "status":i.status
                })
        else:
            data.append({
                "assigned_date":getdate(i.assign_date).strftime("%d-%m-%Y"),
                "expected_date": getdate(i.expected_date).strftime("%d-%m-%Y"),
                "task":i.type_of_work,
                "task_description":i.description,
                "status":i.status
                })
    
    return data















# from __future__ import unicode_literals
# import frappe
# from frappe import _
# import numpy as np
# from frappe.desk.reportview import build_match_conditions

# def execute(filters=None):
#     if not filters:
#         return [], []
#     data = []
#     columns = get_columns()
#     conditions = get_conditions(filters)
#     data = get_data(conditions,data,filters)
#     return columns, data

# def get_columns():
#     columns=[
#         {
#             "label": _("Employee Name"),
#             "fieldtype": "Data",
#             "fieldname": "employee_name",
#             "width": 150
#         },
#         {
#             "label": _("From time"),
#             "fieldtype": "Datetime",
#             "fieldname": "from_time",
#             "width": 170
#         },
#         {
#             "label": _("To time"),
#             "fieldtype": "Datetime",
#             "fieldname": "to_time",
#             "width": 170
#         },
#         {
#             "label": _("Projects"),
#             "fieldtype": "Link",
#             "fieldname": "pro",
#             "options":"Project",
#             "width": 100
#         },
#         {
#             "label": _("System"),
#             "fieldtype": "Data",
#             "fieldname": "sys",
#             "width": 250
#         },
#         {
#             "label": _("Task name"),
#             "fieldtype": "Data",
#             "fieldname": "tsk",
#             "width": 200
#         },
#         {
#             "label": _("Hours"),
#             "fieldtype": "Data",
#             "fieldname": "hrs",
#             "width": 100
#         },
#         {
#             "label": _("Pending"),
#             "fieldtype": "Data",
#             "fieldname": "pending",
#             "width": 100
#         },
#         {
#             "label": _("Pending Reason"),
#             "fieldtype": "Data",
#             "fieldname": "pending_reason",
#             "width": 250
#         },
#         {
#             "label": _("Completed"),
#             "fieldtype": "Data",
#             "fieldname": "completed",
#             "width": 100
#         },
#         {
#             "label": _("Completed Reason"),
#             "fieldtype": "Data",
#             "fieldname": "completed_reason",
#             "width": 250
#         },
#         {
#             "label": _("Incompleted"),
#             "fieldtype": "Data",
#             "fieldname": "incompleted",
#             "width": 100
#         },
#         {
#             "label": _("Incompleted Reason"),
#             "fieldtype": "Data",
#             "fieldname": "incompleted_reason",
#             "width": 250
#         }
#     ]
#     return columns

# def get_data(conditions,data, filters):
#     data=[]
#     emp_list = []
#     time_sheet = frappe.db.sql(""" select ac.name_of_designer, ac.employee_name,
#         act.from_time,act.to_time,
#         ac.project,ac.system,act.task_name,act.hours,act.completed,act.incompleted,act.pending,act.incompleted_reason,act.pending_reason
#         from `tabDaily Activity Table` as act, `tabDaily Activity` as ac where
#         act.parent = ac.name and %s order by ac.name_of_designer"""%(conditions), filters, as_dict=1) 
#     for i in time_sheet:
#         if i.name_of_designer not in emp_list:
#             emp_list.append(i.name_of_designer)
#             data.append({})
#             if(i.pending==0):
#             	tt="No"
#             else:
#             	tt="Yes"
#             if(i.completed==0):
#             	tc="No"
#             else:
#             	tc="Yes"
#             if(i.incompleted==0):
#             	tic="No"
#             else:
#             	tic="Yes"
#             data.append({
#                 "employee_name": i.employee_name,
#                 "from_time": i.from_time,
#                 "to_time": i.to_time,
#                 "pro": i.project,
#                 "sys": i.system,
#                 "tsk": i.task_name,
#                 "hrs": i.hours,
#                 "pending":tt,
#                 "pending_reason":i.pending_reason,
#                 "completed":tc,
#                 "completed_reason":i.completed_reason,
#                 "incompleted":tic,
#                 "Incompleted Reason":i.incompleted_reason
#                 })
#         else:
#         	if(i.pending==0):
#         		tt="No"
#         	else:
#         		tt="Yes"
#         	if(i.completed==0):
#         		tc="No"
#         	else:
#         		tc="Yes"
#         	if(i.incompleted==0):
#         		tic="No"
#         	else:
#         		tic="Yes"
#         	data.append({
#         		"from_time": i.from_time,
#         		"to_time": i.to_time,
#         		"pro": i.project,
#         		"sys": i.system,
#         		"tsk": i.task_name,
#         		"hrs": i.hours,
#         		"pending":tt,
#         		"pending_reason":i.pending_reason,
#         		"completed":tc,
#         		"completed_reason":i.completed_reason,
#         		"incompleted":tic,
#         		"Incompleted Reason":i.incompleted_reason
#         		})
#     return data

# def get_conditions(filters):
#     conditions = "ac.docstatus = 0"
#     if filters.get("from_date"):
#         conditions += " and act.from_time >= %(from_date)s"
#     if filters.get("to_date"):
#         conditions += " and act.to_time <= %(to_date)s"
#     if filters.get("emp"):
#         conditions += " and ac.name_of_designer = %(emp)s"
#     if filters.get("pro"):
#         conditions += " and ac.project = %(pro)s"
#     if filters.get("sys1"):
#         conditions += " and ac.system = %(sys1)s"

#     match_conditions = build_match_conditions("Daily Activity")
#     if match_conditions:
#         conditions += " and %s" % match_conditions
#     return conditions