from __future__ import unicode_literals
import frappe
from datetime import date
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions

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
            "label": _("Status"),
            "fieldtype": "Data",
            "fieldname": "status",
            "width": 150
        }
    ]
    return columns

def get_data(data, filters):

    data=[]
    emp=["MANAGING DIRECTOR","Sarnita","Harshini"]
    act=[]
    check = frappe.db.sql(""" select c.employee,c.employee_name,c.time from  `tabEmployee Checkin` as c where time between %(from_date)s and %(to_date)s """,filters, as_dict=1) 
    vis=frappe.db.sql("SELECT employee_name,department FROM `tabEmployee` WHERE status='Active'",as_dict=1)
    for name in check:
        emp.append(name.employee_name)#array of empcheckin
    for at in vis:
        act.append(at.employee_name)#array of active employee
    #for i in vis:
    for ab in act:
        if ab not in emp:
            data.append({
                "employee_name":ab,
                "status":"Absent"
                })
    return data