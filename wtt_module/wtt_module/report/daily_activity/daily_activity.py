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