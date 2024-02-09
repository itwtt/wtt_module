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
		"fieldtype": "Data",
		"fieldname": "employee_name",
		"width": 180
		},
		{
		"label": ("Department"),
		"fieldtype": "Data",
		"fieldname": "department",
		"width": 180
		},
		{
		"label": ("Total Hours"),
		"fieldtype": "HTML",
		"fieldname": "total_hours",
		"width": 150
		},
		{
		"label": ("Productive Hours"),
		"fieldtype": "HTML",
		"fieldname": "productive_hours",
		"width": 150
		},
		{
		"label": ("Idle Hours"),
		"fieldtype": "HTML",
		"fieldname": "idle_hours",
		"width": 150
		}
		]
	return columns

def get_data(conditions, data, filters):
	data = []
	for i in frappe.db.sql("""SELECT * FROM `tabMonitoring Record` WHERE docstatus=0{conditions} ORDER BY productive_hours DESC""".format(conditions=conditions), as_dict=1):
		data.append({
			"employee_name":i.employee_name,
			"department":i.department,
			"total_hours":i.total_hours,
			"productive_hours":i.productive_hours,
			"idle_hours":i.idle_hours
		})
	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("date"):
		conditions += " AND date='%s'" % filters.get('date')

	if filters.get("emp"):
		conditions += " AND employee='%s'" % filters.get('emp')

	if filters.get("dept"):
		conditions += " AND department='%s'" % filters.get('dept')

	return conditions