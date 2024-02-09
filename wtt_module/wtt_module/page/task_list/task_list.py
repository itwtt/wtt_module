# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
import functools

@frappe.whitelist()
def get_result(tkt):
	arr=[]
	val=frappe.db.sql("SELECT employee FROM `tabEmployee` WHERE user_id='"+tkt+"'",as_dict=1)
	for i in val:
		for j in frappe.db.sql("SELECT count(wt.type_of_work) FROM `tabTask Assignment` as aa,`tabWork table` as wt WHERE aa.name=wt.parent and wt.status='Pending' and aa.employee='"+i.employee+"'"):
			arr.append({
				"count":j
				})
	
	query=frappe.db.sql("SELECT employee FROM `tabEmployee` WHERE user_id='"+tkt+"'",as_dict=1)
	for i in query:
		for j in frappe.db.sql("SELECT wt.type_of_work,wt.description,wt.assign_date,wt.expected_date FROM `tabTask Assignment` as aa,`tabWork table` as wt WHERE aa.name=wt.parent and wt.status='Pending' and aa.employee='"+i.employee+"'",as_dict=1):
			arr.append({
				"type_of_work":j.type_of_work,
				"description":j.description,
				"assign_date":j.assign_date,
				"expected_date":j.expected_date
				})
						
	return arr