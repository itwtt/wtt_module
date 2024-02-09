# Copyright (c) 2023, wtt_module and contributors
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
    },
    {
    "label": _("Leave Date"),
    "fieldname": "leave_date",
    "fieldtype": "Date",
    "width": 150
    },
    {
    "label": _("Leave Type"),
    "fieldname": "leave_type",
    "fieldtype": "Data",
    "width": 150
    },
    {
    "label": _("Attendance Status"),
    "fieldname": "att_status",
    "fieldtype": "Data",
    "width": 150
    }
    ]
    return columns

def get_data(conditions,data, filters):
    data=[]
    for i in frappe.db.sql("SELECT lr.employee,lr.employee_name,lt.from_date,lt.leave_type FROM `tabLeave Request` as lr INNER JOIN `tabLeave table` as lt ON lr.name=lt.parent WHERE lt.from_date>='2023-01-01' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled'{conditions}""".format(conditions=conditions), as_dict=1):
        att_status = frappe.db.get_value("Attendance",{'employee':i.employee,'attendance_date':i.from_date},'status')
        data.append({
            "employee":i.employee,
            "employee_name":i.employee_name,
            "leave_date":i.from_date,
            "leave_type":i.leave_type,
            "att_status":att_status
        })
    return data

def get_conditions(filters):
    conditions = ""
    if filters.get("employee"):
        conditions += " AND lr.employee='%s'" % filters.get('employee')

    if filters.get("leave_type"):
        conditions += " AND lt.leave_type='%s'" % filters.get('leave_type')

    return conditions