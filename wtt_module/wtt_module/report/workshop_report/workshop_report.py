from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
    if not filters:
        return [], []
    data = []
    columns = get_columns()
    conditions = get_conditions(filters)
    data = get_data(conditions,data,filters)
    return columns, data

def get_columns():
    columns=[
        {
            "label": _("Employee Name"),
            "fieldtype": "Data",
            "fieldname": "employee_name",
            "width": 150
        },
        {
            "label": _("From time"),
            "fieldtype": "Datetime",
            "fieldname": "from_time",
            "width": 170
        },
        {
            "label": _("To time"),
            "fieldtype": "Datetime",
            "fieldname": "to_time",
            "width": 170
        },
        {
            "label": _("Projects"),
            "fieldtype": "Link",
            "fieldname": "pro",
            "options":"Project",
            "width": 100
        },
        {
            "label": _("Skid"),
            "fieldtype": "Data",
            "fieldname": "skid",
            "width": 250
        },
        {
            "label": _("Nature of Job"),
            "fieldtype": "Data",
            "fieldname": "nature_of_job",
            "width": 250
        },
        {
            "label": _("Task name"),
            "fieldtype": "Data",
            "fieldname": "tsk",
            "width": 200
        },
        {
            "label": _("Hours"),
            "fieldtype": "Data",
            "fieldname": "hrs",
            "width": 100
        },
        {
            "label": _("Completed"),
            "fieldtype": "Data",
            "fieldname": "completed",
            "width": 100
        },
        {
            "label": _("Incompleted"),
            "fieldtype": "Data",
            "fieldname": "incompleted",
            "width": 100
        },
        {
            "label": _("Pending"),
            "fieldtype": "Data",
            "fieldname": "pending",
            "width": 100
        },
        {
            "label": _("Completed Reason"),
            "fieldtype": "Data",
            "fieldname": "completed_reason",
            "width": 100
        },
        {
            "label": _("Incompleted Reason"),
            "fieldtype": "Data",
            "fieldname": "incompleted_reason",
            "width": 100
        },
        {
            "label": _("Pending Reason"),
            "fieldtype": "Data",
            "fieldname": "pending_reason",
            "width": 100
        }
    ]
    return columns

def get_data(conditions,data, filters):
    data=[]
    emp_list = []
    time_sheet = frappe.db.sql(""" select ac.name_of_employee, ac.employee_name,
        act.from_time,act.to_time,
        ac.project,ac.skid,ac.nature_of_job,act.task_name,act.hours,
        act.completed,act.incompleted,act.pending,act.completed_reason,act.incompleted_reason,act.pending_reason
        from `tabWorkshop Table` as act, `tabWorkshop Activity` as ac where
        act.parent = ac.name and %s order by ac.name_of_employee"""%(conditions), filters, as_dict=1) 
    for i in time_sheet:
        if i.name_of_employee not in emp_list:
            emp_list.append(i.name_of_employee)
            data.append({})
            if(i.completed==1):
                val="yes"
            else:
                val="no"
            if(i.incompleted==1):
                valu="yes"
            else:
                valu="no"
            if(i.pending==1):
                vau="yes"
            else:
                vau="no"
            data.append({
                "employee_name": i.employee_name,
                "from_time": i.from_time,
                "to_time": i.to_time,
                "pro": i.project,
                "skid": i.skid,
                "nature_of_job":i.nature_of_job,
                "tsk": i.task_name,
                "hrs": i.hours,
                "completed":val,
                "incompleted":valu,
                "pending":vau,
                "completed_reason":i.completed_reason,
                "incompleted_reason":i.incompleted_reason,
                "pending_reason":i.pending_reason
                })
        else:
            if(i.completed==1):
                val="yes"
            else:
                val="no"
            if(i.incompleted==1):
                valu="yes"
            else:
                valu="no"
            if(i.pending==1):
                vau="yes"
            else:
                vau="no"
            data.append({
                "from_time": i.from_time,
                "to_time": i.to_time,
                "pro": i.project,
                "skid": i.skid,
                "nature_of_job":i.nature_of_job,
                "tsk": i.task_name,
                "hrs": i.hours,
                "completed":val,
                "incompleted":valu,
                "pending":vau,
                "completed_reason":i.completed_reason,
                "incompleted_reason":i.incompleted_reason,
                "pending_reason":i.pending_reason
                })
    return data

def get_conditions(filters):
    conditions = "ac.docstatus = 1"
    if filters.get("from_date"):
        conditions += " and act.from_time >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and act.to_time <= %(to_date)s"
    if filters.get("emp"):
        conditions += " and ac.name_of_employee = %(emp)s"
    if filters.get("pro"):
        conditions += " and ac.project = %(pro)s"
    if filters.get("skid"):
        conditions += " and ac.skid = %(skid)s"
    if filters.get("nature_of_job"):
        conditions += " and ac.nature_of_job = %(nature_of_job)s"


    match_conditions = build_match_conditions("Workshop Activity")
    if match_conditions:
        conditions += " and %s" % match_conditions
    return conditions