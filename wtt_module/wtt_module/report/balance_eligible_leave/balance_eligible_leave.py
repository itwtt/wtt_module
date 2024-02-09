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
    conditions = get_conditions(filters)
    data = get_data(conditions,data,filters)
    return columns, data

def get_columns(filters):
    columns=[
        {
            "label": _("employee"),
            "fieldtype": "Data",
            "fieldname": "employee",
            "width": 150
        },
        {
            "label": _("Employee Name"),
            "fieldtype": "Data",
            "fieldname": "employee_name",
            "width": 150
        },
        {
            "label": _("Month"),
            "fieldtype": "Data",
            "fieldname": "month",
            "width": 150
        },
        {
            "label": _("Balance Leave"),
            "fieldtype": "Data",
            "fieldname": "balance_leave",
            "width": 150
        }
    ]
    return columns

def get_data(conditions,data, filters):

    data=[]
    emp=[]
    doc=frappe.db.sql(""" select bl.employee, bl.employee_name,bl.date,
        blt.month,blt.balance_leave
        from `tabBalance Leave` as bl, `tabBalance Leave Table` as blt where 
        blt.parent = bl.name and %s order by bl.employee"""%(conditions), filters, as_dict=1)
    for i in doc:
        if i.employee not in emp:
            emp.append(i.employee)
            data.append({})
            data.append({
                "employee":i.employee,
                "employee_name":i.employee_name,
                "month":i.month,
                "balance_leave":i.balance_leave
                })
        else:
        	data.append({
        		"month":i.month,
                "balance_leave":i.balance_leave
        		})
    
    return data

def get_conditions(filters):
    conditions = "bl.docstatus = 0"
    if filters.get("from_date"):
        conditions += " and bl.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and bl.date <= %(to_date)s"
    if filters.get("employee"):
        conditions += " and bl.employee = %(employee)s"

    match_conditions = build_match_conditions("Balance Leave")
    if match_conditions:
        conditions += " and %s" % match_conditions
    return conditions