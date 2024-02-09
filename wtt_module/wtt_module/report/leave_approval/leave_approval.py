from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
import json

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
            "label": _("From date"),
            "fieldtype": "Date",
            "fieldname": "from_date",
            "width": 120
        },
        {
            "label": _("To date"),
            "fieldtype": "Date",
            "fieldname": "to_date",
            "width": 120
        },
        {
            "label": _("Day"),
            "fieldtype": "Data",
            "fieldname": "day",
            "width": 100
        },
        {
            "label": _("No of days"),
            "fieldtype": "Data",
            "fieldname": "no_day",
            "width": 70
        },
        {
            "label": _("Leave type"),
            "fieldtype": "Data",
            "fieldname": "leave_type",
            "width": 100
        },
        {
            "label": _("Explanation"),
            "fieldtype": "Data",
            "fieldname": "exp",
            "width": 250
        },
        {
            "label": _("Status"),
            "fieldtype": "Data",
            "fieldname": "status",
            "width": 150
        },
        {
            "label": _("HOD Remarks"),
            "fieldtype": "Data",
            "fieldname": "hod",
            "width": 500
        },
        {
            "label": _("GM Remarks"),
            "fieldtype": "Data",
            "fieldname": "gm",
            "width": 500
        },
        {
            "label": _("MD Remarks"),
            "fieldtype": "Data",
            "fieldname": "md",
            "width": 500
        },
        {
            "label": _("Lr Name"),
            "fieldtype": "Data",
            "fieldname": "lr_name",
            "width": 100
        },
        {
            "label": _("Name"),
            "fieldtype": "Data",
            "fieldname": "name",
            "width": 100
        }


    ]
    return columns

def get_data(conditions,data, filters):
    data=[]
    emp_list = []
    leave_request = frappe.db.sql(""" select lt.parent,lt.name,lr.employee, lr.employee_name,
        lt.from_date,lt.to_date,lr.hod_remarks,lr.gm_remarks,lr.md_remarks,
        lt.day,lt.no_of_days,lt.leave_type,lt.explanation,lr.workflow_state
        from `tabLeave table` as lt, `tabLeave Request` as lr where lt.status!='Rejected' and
        lt.parent = lr.name and %s order by lr.employee"""%(conditions), filters, as_dict=1) 
    for i in leave_request:
        if i.employee not in emp_list:
            emp_list.append(i.employee)
            data.append({})
            data.append({
                "employee_name": i.employee_name,
                "from_date": i.from_date,
                "to_date": i.to_date,
                "day": i.day,
                "no_day": i.no_of_days,
                "leave_type": i.leave_type,
                "exp": i.explanation,
                "status":i.workflow_state,
                "hod":i.hod_remarks,
                "gm":i.gm_remarks,
                "md":i.md_remarks,
                "lr_name":i.parent,
                "name":i.name
         	})
        else:
            data.append({
              	"from_date": i.from_date,
                "to_date": i.to_date,
                "day": i.day,
                "no_day": i.no_of_days,
                "leave_type": i.leave_type,
                "exp": i.explanation,
                "status":i.workflow_state,
                "hod":i.hod_remarks,
                "gm":i.gm_remarks,
                "md":i.md_remarks,
                "lr_name":i.parent,
                "name":i.name
                })
    return data

def get_conditions(filters):
    conditions = "lr.docstatus = 0"
    if filters.get("from_date"):
        conditions += " and lt.from_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and lt.to_date <= %(to_date)s"
    if filters.get("emp"):
        conditions += " and lr.employee = %(emp)s"

    match_conditions = build_match_conditions("Leave Request")
    if match_conditions:
        conditions += " and %s" % match_conditions
    return conditions

@frappe.whitelist()
def function(lr_name):
    user=frappe.session.user
    if(user=='venkat@wttindia.com' or user=='priya@wttindia.com' or user=='sarnita@wttindia.com' or user=='Administrator'):
        doc=frappe.get_doc("Leave Request",lr_name)
        doc.submit()
    else:
        frappe.throw("Not Permitted")

@frappe.whitelist()
def func(lt_name):
    user=frappe.session.user
    if(user=='venkat@wttindia.com' or user=='priya@wttindia.com' or user=='sarnita@wttindia.com' or user=='Administrator'):
        frappe.db.sql("UPDATE `tabLeave table` set status='Rejected' where name='"+lt_name+"'")
    else:
        frappe.throw("Not Permitted")