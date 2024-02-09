from __future__ import unicode_literals
import frappe
from datetime import date
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import date,datetime,timedelta
import calendar

def execute(filters=None):
	data = []
	columns = get_columns(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	
	columns=[
		{
			"label": _("Supplier"),
			"fieldtype": "Data",
			"fieldname": "supplier",
			"width": 250
		},
		{
			"label": _("Grand Total"),
			"fieldtype": "Currency",
			"fieldname": "total",
			"width": 150
		},
		{
			"label": _("Rounded Total"),
			"fieldtype": "Currency",
			"fieldname": "rounded_total",
			"width": 150
		},
		{
			"label": _("Outstanding Amount"),
			"fieldtype": "Currency",
			"fieldname": "outstanding_amount",
			"width": 150
		},
		{
			"label": _("Paid Amount"),
			"fieldtype": "Currency",
			"fieldname": "paid_amount",
			"width": 150
		}
		]
	return columns

def get_data(data, filters):
	data=[]
	array1=[]
	array2=[]
	if(filters.supplier==None):
		query=frappe.db.sql("SELECT name,supplier,total,rounded_total,outstanding_amount FROM `tabPurchase Invoice` WHERE status!='Cancelled' and status!='Rejected' ",filters,as_dict=1)
	else:
		query=frappe.db.sql("SELECT name,supplier,total,rounded_total,outstanding_amount FROM `tabPurchase Invoice` WHERE status!='Cancelled' and status!='Rejected' and supplier=%(supplier)s ",filters,as_dict=1)
	for i in query:
		if(i.supplier not in array1):
			array1.append(i.supplier)
			array2.append(i)
		else:
			array2[array1.index(i["supplier"])]["total"]+=i["total"]
			array2[array1.index(i["supplier"])]["rounded_total"] += i["rounded_total"]
			array2[array1.index(i["supplier"])]["outstanding_amount"] += i["outstanding_amount"]
	for i in array2:
		data.append({
			"supplier":i["supplier"],
			"total":i["total"],
			"rounded_total":i["rounded_total"],
			"outstanding_amount":i["outstanding_amount"],
			"paid_amount":i["rounded_total"]-i["outstanding_amount"]
			})
	return data