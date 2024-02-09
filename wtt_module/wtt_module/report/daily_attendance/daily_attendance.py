# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np

def execute(filters=None):
	if not filters:
		return [], []
	data = []
	columns = get_columns(filters)
	data = get_data(data , filters)
	return columns, data

def get_columns(filters):
    columns=[
        {
            "label": _("Present"),
            "fieldtype": "Data",
            "fieldname": "present",
            "width": 150
        },
        {
            "label": _("Absent"),
            "fieldtype": "Data",
            "fieldname": "absent",
            "width": 150
        }
    ]
    return columns

def get_data(data, filters):
    data=[]
    query=frappe.db.sql("""SELECT employee,employee_name FROM `tabEmployee Checkin` WHERE time between %(from_date)s and %(to_date)s and shift='Day Shift'""",filters,as_dict=1)
    for i in query:
        for val in frappe.db.sql("SELECT name FROM `tabEmployee` WHERE name !='"+i.employee+"'",as_dict=1):
            frappe.msgprint(str(val.name))
        #row=[i.employee_name,0]
    	#data.append(row)
    #return data