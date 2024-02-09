# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions
from datetime import datetime, timedelta

def execute(filters=None):
    if not filters:
        return [], []
    data = []
    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(conditions, data, filters)
    return columns, data

@frappe.whitelist()
def get_columns(filters):
    columns = [
        {
            "label": _("Employee"),
            "fieldname": "employee",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 150
        },
        {
            "label": _("Employee Name"),
            "fieldname": "employee_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Green Flags"),
            "fieldname": "green_flags",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Red Flags"),
            "fieldname": "red_flags",
            "fieldtype": "Int",
            "width": 100
        }
    ]

    start_date = datetime.strptime(filters.get('from_date'), "%Y-%m-%d")
    end_date = datetime.strptime(filters.get('to_date'), "%Y-%m-%d")
    date_increment = timedelta(days=1)
    current_date = start_date

    while current_date <= end_date:
        current_date_str = current_date.strftime("%d-%m-%y")
        columns.append({
            "fieldname": str(current_date_str) + "",
            "label": "" + str(current_date_str),
            "fieldtype": "HTML",
            "width": 120
        })
        current_date += date_increment

    return columns

def get_data(conditions, data, filters):
    emp = []
    for q in frappe.db.sql("SELECT employee FROM `tabEmployee` WHERE status='Active' and date_of_joining<='2023-01-01'", as_dict=1):
        emp.append(q.employee)
    data = []
    ar = []
    to_be_compared_items = frappe.db.sql(
        """SELECT actual_completion_time, professional_completion_time, date, employee, employee_name, department from `tabSay It Do It` WHERE docstatus=0{conditions}""".format(conditions=conditions),
        as_dict=1)
    
    items_dict = {}
    temp_list = []
    dummy_rate = []
    low_amt = []
    
    for item in to_be_compared_items:
        if item.employee in emp:
            temp_list.append(item.employee)
    
    unique_item = set(temp_list)

    for item in unique_item:
        column = {
            "employee": item,
            "employee_name": None,
            "green_flags": 0,
            "red_flags": 0
        }

        for datum in to_be_compared_items:
            if item == datum.employee:
                column['employee_name'] = datum.employee_name
                current_date_str = datum.date.strftime("%d-%m-%y")
                ddpro = 0
                ddact = 0

                if datum.professional_completion_time is not None:
                    ddpro = datum.professional_completion_time
                if datum.actual_completion_time is not None:
                    ddact = datum.actual_completion_time

                if ddact == 0:
                    column[str(current_date_str) + ''] = "-"
                else:
                    if ddpro > ddact:
                        column[str(current_date_str) + ''] = "<img width='20' src='https://erp.wttindia.com/files/flaggre.png'>"
                        column['green_flags'] += 1
                    else:
                        if ddact == 0 or ddpro == 0:
                            column[str(current_date_str) + ''] = "-"
                        else:
                            column[str(current_date_str) + ''] = "<img width='20' src='https://erp.wttindia.com/files/flagred.png'>"
                            column['red_flags'] += 1

        data.append(column)

    return data

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND date>='%s'" % filters.get('from_date')

    if filters.get("to_date"):
        conditions += " AND date<='%s'" % filters.get('to_date')

    if filters.get("employee"):
        conditions += " AND employee='%s'" % filters.get('employee')

    return conditions
