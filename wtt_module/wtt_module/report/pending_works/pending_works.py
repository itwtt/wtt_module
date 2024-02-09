from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime
from datetime import date
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
    columns=[
        {
            "label": _("Employee Name"),
            "fieldtype": "Data",
            "fieldname": "employee_name",
            "width": 150
        },
        {
            "label": _("Task Name"),
            "fieldtype": "Data",
            "fieldname": "type_work",
            "width": 200
        },
        {
            "label": _("Task Description"),
            "fieldtype": "Data",
            "fieldname": "des",
            "width": 400
        },
        {
            "label": _("Assigned date"),
            "fieldtype": "date",
            "fieldname": "assign_date",
            "width": 150
        },
        {
            "label": _("Expected date"),
            "fieldtype": "date",
            "fieldname": "exp_date",
            "width": 150
        },
        {
            "label": _("Workstatus"),
            "fieldtype": "Data",
            "fieldname": "wrk_status",
            "width": 180
        },
        {
            "label": _("Pending days"),
            "fieldname": "pending_days",
            "fieldtype": "Int",
            "width": 120
        }
    ]
    return columns

def get_data(conditions,data, filters):
    data=[]
    emp_list = []
    pending_work = frappe.db.sql(""" select ac.employee, ac.employee_name,ac.department,
        act.assign_date,act.expected_date,act.status,
        act.type_of_work,act.description
        from `tabWork table` as act, `tabTask Assignment` as ac where
        act.parent = ac.name and %s order by ac.employee"""%(conditions), filters, as_dict=1) 
    for i in pending_work:
        if(i.status!="Completed"):
            diff2=date.today()-i.assign_date
            days=int(diff2.days)
            #days=str(diff2.days)+" days"
        else:
            days=0
            #days="-"
        if i.employee not in emp_list:
            emp_list.append(i.employee)
            data.append({})
            data.append({
                "employee_name": i.employee_name,
                "assign_date": i.assign_date,
                "exp_date":i.expected_date,
                "type_work": i.type_of_work,
                "des":i.description,
                "wrk_status": i.status,
                "pending_days":days
                })
        else:
            data.append({
                "assign_date": i.assign_date,
                "exp_date":i.expected_date,
                "type_work": i.type_of_work,
                "des":i.description,
                "wrk_status": i.status,
                "pending_days":days
                })
    return data

def get_conditions(filters):
    conditions = "ac.docstatus = 0"
    if filters.get("from_date"):
        conditions += " and act.assign_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and act.assign_date <= %(to_date)s"
    if filters.get("emp"):
        conditions += " and ac.employee = %(emp)s"
    if filters.get("dept"):
        conditions += " and ac.department = %(dept)s"
    if filters.get("status"):
        conditions += " and act.status = %(status)s"

    match_conditions = build_match_conditions("Task Assignment")
    if match_conditions:
        conditions += " and %s" % match_conditions
    return conditions