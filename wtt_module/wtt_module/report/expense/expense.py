from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
import json
from datetime import date,datetime,timedelta

def execute(filters=None):
	data = []
	columns = get_columns()
	conditions = get_conditions(filters)
	data = get_data(conditions,data,filters)
	return columns, data

def get_columns():
	columns=[
	{
		"label":"JOURNAL NUMBER",
		"fieldtype":"Data",
		"fieldname":"journal_name",
		"width":200
	},
	{
		"label":"DATE",
		"fieldtype":"Data",
		"fieldname":"date",
		"width":100
	},
	{
		"label":"EXPENSE HEAD",
		"fieldtype":"Data",
		"fieldname":"account",
		"width":200
	},
	{
		"label":"AMOUNT",
		"fieldtype":"Currency",
		"fieldname":"amount",
		"width":100
	},
	{
		"label":"REMARKS",
		"fieldtype":"Data",
		"fieldname":"user_remark",
		"width":380
	},
	{
		"label":"REF",
		"fieldname":"ref",
		"fieldtype":"Link",
		"options":"Pre Journal Entry",
		"width":10
	}
	]
	return columns

def get_data(conditions,data, filters):
	data=[]
	je = []
	pa=[]
	entries = frappe.db.sql(""" select pjt.account,pjt.debit_in_account_currency,pj.posting_date,pj.journal_name,pj.name,pj.user_remark
	from `tabPre Journal Entry` as pj, `tabPre Journal Entry Table` as pjt where 
	pjt.parent = pj.name and %s order by pj.posting_date"""%(conditions), filters, as_dict=1)
	for j in frappe.db.sql("SELECT name FROM `tabAccount` WHERE parent_account='Expenses - WTT' ",as_dict=1):
		pa.append(j.name)
		for k in frappe.db.sql("SELECT name FROM `tabAccount` WHERE parent_account='"+str(j.name)+"' ",as_dict=1):
			pa.append(k.name)
	for i in entries:
		acc=frappe.db.get_value("Account",i.account,"parent_account")		
		if(acc in pa):
			if(i.name not in je):			
				je.append(i.name)
				data.append({
					"journal_name":i.journal_name,
					"account":i.account,
					"date":i.posting_date,
					"ref":i.name,
					"amount":i.debit_in_account_currency,
					"user_remark":i.user_remark
					})
			else:
				data.append({
					"account":i.account,
					"date":i.posting_date,
					"amount":i.debit_in_account_currency,
					"user_remark":i.user_remark
					})
		
	return data

def get_conditions(filters):
	conditions = "pj.docstatus = 0"
	if filters.get("from_date"):
		conditions += " and pj.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " and pj.posting_date <= %(to_date)s"
	if filters.get("account"):
		conditions += " and pj.account = %(account)s"

	match_conditions = build_match_conditions("Pre Journal Entry")
	if match_conditions:
		conditions += " and %s" % match_conditions
	return conditions

@frappe.whitelist()
def function(lr_name):
	user=frappe.session.user
	if(user=='venkat@wttindia.com' or user=='priya@wttindia.com' or user=='sarnita@wttindia.com' or user=='Administrator'):
		doc=frappe.get_doc("Pre Journal Entry",lr_name)
		doc.submit()
	else:
		frappe.throw("Not Permitted")
	return user

@frappe.whitelist()
def func(lt_name):
	user=frappe.session.user
	if(user=='venkat@wttindia.com' or user=='priya@wttindia.com' or user=='sarnita@wttindia.com' or user=='Administrator'):
		doc=frappe.get_doc("Pre Journal Entry",lr_name)
		doc.submit()
		doc=frappe.get_doc("Pre Journal Entry",lr_name)
		doc.cancel()
	else:
		frappe.throw("Not Permitted")
	return user