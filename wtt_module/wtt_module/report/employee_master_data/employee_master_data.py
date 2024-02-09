# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
import json
from datetime import datetime,date
from dateutil import relativedelta

def execute(filters=None):
    data = []
    columns = get_columns()
    conditions = get_conditions(filters)
    data = get_data(conditions,data,filters)
    return columns, data


def get_columns():
    columns=[
        {
            "label": _("Employee"),
            "fieldtype": "Data",
            "fieldname": "employee",
            "width": 100
        },
        {
            "label": _("Employee Name"),
            "fieldtype": "Data",
            "fieldname": "employee_name",
            "width": 180
        },
        {
            "label": _("Department"),
            "fieldtype": "Data",
            "fieldname": "dept",
            "width": 120
        },
        {
            "label": _("Branch"),
            "fieldtype": "Data",
            "fieldname": "branch",
            "width": 120
        },
        {
            "label": _("Grade"),
            "fieldtype": "Data",
            "fieldname": "grade",
            "width": 80
        },
        {
            "label": _("Date of Joining"),
            "fieldtype": "Date",
            "fieldname": "doj",
            "width": 120
        },
        {
            "label": _("Previous Experience"),
            "fieldtype": "Data",
            "fieldname": "total_work_experience",
            "width": 150
        },
        {
            "label": _("Current Work Experience"),
            "fieldtype": "Data",
            "fieldname": "work_experience",
            "width": 180
        },
        {
            "label": _("Permanent Address"),
            "fieldtype": "Data",
            "fieldname": "permanent_address",
            "width": 200
        },
        {
            "label": _("Current Address"),
            "fieldtype": "Data",
            "fieldname": "current_address",
            "width": 200
        },
        {
            "label": _("Mobile"),
            "fieldtype": "Data",
            "fieldname": "mobile",
            "width": 150
        },
        {
            "label": _("Personal Email"),
            "fieldtype": "Data",
            "fieldname": "personal_email",
            "width": 250
        }
        # {
        #     "label": _("Gross Amount"),
        #     "fieldtype": "Data",
        #     "fieldname": "gross_total",
        #     "width": 120
        # },
        # {
        #     "label": _("Total Salary"),
        #     "fieldtype": "Data",
        #     "fieldname": "total_salary",
        #     "width": 120
        # }
    ]
    return columns

def get_data(conditions,data, filters):
    data=[]
    emp_list = []
    emp_query = frappe.db.sql("""SELECT employee,employee_name,department,cell_number,personal_email,branch,permanent_address,current_address,total_work_experience,grade,total_salary,date_of_joining,gross_amount FROM `tabEmployee` WHERE status='Active' and employee!='WTT001' and %s order by employee_name asc"""%(conditions),filters,as_dict=1)
    for i in emp_query:
        date1=datetime.strptime(str(i.date_of_joining),"%Y-%m-%d")
        date2=datetime.strptime(str(date.today()),"%Y-%m-%d")
        diff = relativedelta.relativedelta(date2, date1)
        years = diff.years
        months = diff.months
        final='{} Year {} Month'.format(years, months)
        if(i.total_work_experience<0):
            data.append({
                "employee": i.employee,
                "employee_name": i.employee_name,
                "dept": i.department[:-6],
                "branch": i.branch,
                "grade":i.grade,
                "doj":i.date_of_joining,
                "total_work_experience":0,
                "permanent_address":i.permanent_address,
                "current_address":i.current_address,
                "mobile":i.cell_number,
                "personal_email":i.personal_email,
                "work_experience":final
                #"gross_total":i.gross_amount,
                #"total_salary":i.total_salary
            })
        else:
            to=round(i.total_work_experience, 1)
            data.append({
                "employee": i.employee,
                "employee_name": i.employee_name,
                "dept": i.department[:-6],
                "branch": i.branch,
                "grade":i.grade,
                "doj":i.date_of_joining,
                "total_work_experience":to,
                "permanent_address":i.permanent_address,
                "current_address":i.current_address,
                "mobile":i.cell_number,
                "personal_email":i.personal_email,
                "work_experience":final
                #"gross_total":i.gross_amount,
                #"total_salary":i.total_salary
            })
    return data

def get_conditions(filters):
    conditions = "docstatus = 0"
    if filters.get("emp"):
        conditions += " and employee = %(emp)s"
    if filters.get("dept"):
        conditions += " and department = %(dept)s"
    if filters.get("branch"):
        conditions += " and branch = %(branch)s"

    match_conditions = build_match_conditions("Employee")
    if match_conditions:
        conditions += " and %s" % match_conditions
    return conditions
