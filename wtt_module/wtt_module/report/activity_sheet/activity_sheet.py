# from __future__ import unicode_literals
# import frappe
# from frappe import _
# import numpy as np
# from frappe.desk.reportview import build_match_conditions
# from datetime import datetime

# def execute(filters=None):
#     if not filters:
#         return [], []
#     data = []
#     columns = get_columns(filters)
#     conditions = get_conditions(filters)
#     data = get_data(conditions,data,filters)
#     return columns, data

# @frappe.whitelist()
# def get_columns(filters):
#     v=filters.get('dc')
#     if(v=='Activity Sheet'):
#         columns=[
#             {
#                 "label": _("Employee Name"),
#                 "fieldtype": "Data",
#                 "fieldname": "employee_name",
#                 "width": 150
#             },
#             {
#                 "label": _("From time"),
#                 "fieldtype": "Datetime",
#                 "fieldname": "from_time",
#                 "width": 170
#             },
#             {
#                 "label": _("To time"),
#                 "fieldtype": "Datetime",
#                 "fieldname": "to_time",
#                 "width": 170
#             },
#             {
#                 "label": _("Tasks"),
#                 "fieldtype": "Data",
#                 "fieldname": "description",
#                 "width": 400
#             },
#             {
#                 "label": _("Hours"),
#                 "fieldtype": "Data",
#                 "fieldname": "hrs",
#                 "width": 100
#             }

#         ]
#         return columns

#     elif(v=="Daily Activity"):
#         columns=[
#             {
#                 "label": _("Employee Name"),
#                 "fieldtype": "Data",
#                 "fieldname": "employee_name",
#                 "width": 150
#             },
#             {
#                 "label": _("From time"),
#                 "fieldtype": "Datetime",
#                 "fieldname": "from_time",
#                 "width": 170
#             },
#             {
#                 "label": _("To time"),
#                 "fieldtype": "Datetime",
#                 "fieldname": "to_time",
#                 "width": 170
#             },
#             {
#                 "label": _("Projects"),
#                 "fieldtype": "Link",
#                 "fieldname": "pro",
#                 "options":"Project",
#                 "width": 100
#             },
#             {
#                 "label": _("System"),
#                 "fieldtype": "Data",
#                 "fieldname": "sys",
#                 "width": 250
#             },
#             {
#                 "label": _("Task name"),
#                 "fieldtype": "Data",
#                 "fieldname": "tsk",
#                 "width": 200
#             },
#             {
#                 "label": _("Hours"),
#                 "fieldtype": "Data",
#                 "fieldname": "hrs",
#                 "width": 100
#             },
#             {
#                 "label": _("Pending"),
#                 "fieldtype": "Data",
#                 "fieldname": "pending",
#                 "width": 100
#             },
#             {
#                 "label": _("Pending Reason"),
#                 "fieldtype": "Data",
#                 "fieldname": "pending_reason",
#                 "width": 250
#             },
#             {
#                 "label": _("Completed"),
#                 "fieldtype": "Data",
#                 "fieldname": "completed",
#                 "width": 100
#             },
#             {
#                 "label": _("Completed Reason"),
#                 "fieldtype": "Data",
#                 "fieldname": "completed_reason",
#                 "width": 250
#             },
#             {
#                 "label": _("Incompleted"),
#                 "fieldtype": "Data",
#                 "fieldname": "incompleted",
#                 "width": 100
#             },
#             {
#                 "label": _("Incompleted Reason"),
#                 "fieldtype": "Data",
#                 "fieldname": "incompleted_reason",
#                 "width": 250
#             }
#         ]
#         return columns
#     else:
#         columns=[
#             {
#                 "label": _("Employee Name"),
#                 "fieldtype": "Data",
#                 "fieldname": "employee_name",
#                 "width": 150
#             },
#             {
#                 "label": _("From time"),
#                 "fieldtype": "Datetime",
#                 "fieldname": "from_time",
#                 "width": 170
#             },
#             {
#                 "label": _("To time"),
#                 "fieldtype": "Datetime",
#                 "fieldname": "to_time",
#                 "width": 170
#             },
#             {
#                 "label": _("Hours"),
#                 "fieldtype": "Data",
#                 "fieldname": "hrs",
#                 "width": 100
#             }

#         ]
#         return columns

# def get_data(conditions,data, filters):
#     v=filters.get('dc')
#     if(v=='Activity Sheet'):
#         data=[]
#         emp_list = []
#         time_sheet = frappe.db.sql(""" select ac.employee, ac.employee_name,ac.department,
#             act.from_time,act.to_time,
#             act.projects,act.activity_type,act.hours
#             from `tabActivity Sheet Table` as act, `tabActivity Sheet` as ac where
#             act.parent = ac.name and %s order by ac.employee"""%(conditions), filters, as_dict=1) 
#         for i in time_sheet:
#             if i.employee not in emp_list:
#                 emp_list.append(i.employee)
#                 data.append({})
#                 data.append({
#                     "employee_name": i.employee_name,
#                     "from_time": i.from_time,
#                     "to_time": i.to_time,
#                     "description": i.activity_type,
#                     "hrs": i.hours
#                     })
#             else:
#                 data.append({
#                     "from_time": i.from_time,
#                     "to_time": i.to_time,
#                     "description": i.activity_type,
#                     "hrs": i.hours
#                     })
#         return data
#     elif(v=='Daily Activity'):
#         data=[]
#         emp_list = []
#         time_sheet = frappe.db.sql(""" select ac.name_of_designer, ac.employee_name,
#             act.from_time,act.to_time,
#             ac.project,ac.system,act.task_name,act.hours,act.completed,act.incompleted,act.pending,act.incompleted_reason,act.pending_reason
#             from `tabDaily Activity Table` as act, `tabDaily Activity` as ac where
#             act.parent = ac.name and %s order by ac.name_of_designer"""%(conditions), filters, as_dict=1) 
#         for i in time_sheet:
#             if i.name_of_designer not in emp_list:
#                 emp_list.append(i.name_of_designer)
#                 data.append({})
#                 if(i.pending==0):
#                     tt="No"
#                 else:
#                     tt="Yes"
#                 if(i.completed==0):
#                     tc="No"
#                 else:
#                     tc="Yes"
#                 if(i.incompleted==0):
#                     tic="No"
#                 else:
#                     tic="Yes"
#                 data.append({
#                     "employee_name": i.employee_name,
#                     "from_time": i.from_time,
#                     "to_time": i.to_time,
#                     "pro": i.project,
#                     "sys": i.system,
#                     "tsk": i.task_name,
#                     "hrs": i.hours,
#                     "pending":tt,
#                     "pending_reason":i.pending_reason,
#                     "completed":tc,
#                     "completed_reason":i.completed_reason,
#                     "incompleted":tic,
#                     "Incompleted Reason":i.incompleted_reason
#                     })
#             else:
#                 if(i.pending==0):
#                     tt="No"
#                 else:
#                     tt="Yes"
#                 if(i.completed==0):
#                     tc="No"
#                 else:
#                     tc="Yes"
#                 if(i.incompleted==0):
#                     tic="No"
#                 else:
#                     tic="Yes"
#                 data.append({
#                     "from_time": i.from_time,
#                     "to_time": i.to_time,
#                     "pro": i.project,
#                     "sys": i.system,
#                     "tsk": i.task_name,
#                     "hrs": i.hours,
#                     "pending":tt,
#                     "pending_reason":i.pending_reason,
#                     "completed":tc,
#                     "completed_reason":i.completed_reason,
#                     "incompleted":tic,
#                     "Incompleted Reason":i.incompleted_reason
#                     })
#         return data

# def get_conditions(filters):
#     v=filters.get('dc')
#     if(v=="Activity Sheet"):
#         conditions = "ac.docstatus = 1"
#         if filters.get("from_date"):
#             conditions += " and ac.date >= %(from_date)s"
#         if filters.get("to_date"):
#             conditions += " and ac.date <= %(to_date)s"
#         if filters.get("emp"):
#             conditions += " and ac.employee = %(emp)s"
#         if filters.get("dept"):
#             conditions += " and ac.department = %(dept)s"

#         match_conditions = build_match_conditions("Activity Sheet")
#         if match_conditions:
#             conditions += " and %s" % match_conditions
#         return conditions
#     elif(v=="Daily Activity"):
#         conditions = "ac.docstatus = 0"
#         if filters.get("from_date"):
#             conditions += " and act.from_time >= %(from_date)s"
#         if filters.get("to_date"):
#             conditions += " and act.to_time <= %(to_date)s"
#         if filters.get("emp"):
#             conditions += " and ac.name_of_designer = %(emp)s"
#         if filters.get("pro"):
#             conditions += " and ac.project = %(pro)s"
#         if filters.get("sys1"):
#             conditions += " and ac.system = %(sys1)s"

#         match_conditions = build_match_conditions("Daily Activity")
#         if match_conditions:
#             conditions += " and %s" % match_conditions
#         return conditions


# Copyright (c) 2024, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime


def execute(filters=None):
    data = []
    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(conditions,data,filters)
    return columns, data

@frappe.whitelist()
def get_columns(filters):
    columns=[
        {
        "label": ("Employee Name"),
        "fieldtype": "HTML",
        "fieldname": "employee_name",
        "width": 150
        },
        {
        "label": ("From time"),
        "fieldtype": "Datetime",
        "fieldname": "from_time",
        "width": 170
        },
        {
        "label": ("To time"),
        "fieldtype": "Datetime",
        "fieldname": "to_time",
        "width": 170
        },
        {
        "label": ("Tasks"),
        "fieldtype": "Data",
        "fieldname": "description",
        "width": 400
        },
        {
        "label": ("Hours"),
        "fieldtype": "HTML",
        "fieldname": "hrs",
        "width": 100
        }
        ]
    return columns

def get_data(conditions, data, filters):
    data = []
    emp_list = []
    for i in frappe.db.sql("SELECT ac.employee,ac.employee_name,ac.department,ac.date,act.from_time,act.to_time,act.projects,act.activity_type,act.hours,ac.total_hours FROM `tabActivity Sheet` as ac INNER JOIN `tabActivity Sheet Table` as act ON ac.name=act.parent WHERE ac.docstatus!=2 {conditions}".format(conditions=conditions), as_dict=1):
        if i.employee not in emp_list:
            if emp_list:
                data.append({
                    "employee_name": "<b>Total hours</b>",
                    "hrs": "<b>"+str(round(emp_total_hours, 2))+"</b>"
                })

            emp_list.append(i.employee)
            emp_total_hours = 0
            data.append({
                "employee_name": i.employee_name,
                "from_time": i.from_time,
                "to_time": i.to_time,
                "description": i.activity_type,
                "hrs": round(i.hours, 2)
            })
        else:
            data.append({
                "from_time": i.from_time,
                "to_time": i.to_time,
                "description": i.activity_type,
                "hrs": round(i.hours, 2)
            })
        emp_total_hours += i.hours

    if emp_list and data:
        data.append({
            "employee_name": "<b>Total hours</b>",
            "hrs": "<b>"+str(round(emp_total_hours, 2))+"</b>"
        })

    return data

def get_conditions(filters):
    conditions = ""
    if filters.get("date"):
        conditions += " AND ac.date='%s'" % filters.get('date')

    if filters.get("emp"):
        conditions += " AND ac.employee='%s'" % filters.get('emp')

    if filters.get("dept"):
        conditions += " AND ac.department='%s'" % filters.get('dept')

    return conditions