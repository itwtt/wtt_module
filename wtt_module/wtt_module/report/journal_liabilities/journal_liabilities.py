from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
import json
from frappe.model.mapper import get_mapped_doc
from datetime import date,datetime,timedelta

def execute(filters=None):
	data = []
	columns = get_columns(filters)
	data = get_data(data , filters)
	return columns, data

def get_columns(filters):
	ar=[]
	columns=[{
			"label": _("Date"),
			"fieldtype": "Data",
			"fieldname": "posting_date"
		},		
		{
			"label": _("Journal Entry"),
			"fieldtype": "Link",
			"fieldname": "journal_entry",
			"options":"Journal Entry"
		},
		{
			"label": _("Total Credit"),
			"fieldtype": "Data",
			"fieldname": "total_credit"
		},
		{
			"label": _("Total Debit"),
			"fieldtype": "Data",
			"fieldname": "total_debit"
		},
		{
			"label": _("Remarks"),
			"fieldtype": "Data",
			"fieldname": "user_remark"
		}
	]
	for i in frappe.db.sql("SELECT DISTINCT(name) FROM `tabAccount` WHERE parent_account='Duties and Taxes - WTT' ",as_dict=1):
		sql = frappe.db.sql("SELECT DISTINCT(p.name) FROM `tabJournal Entry Account`as ch,`tabJournal Entry`as p WHERE ch.account='"+str(i.name)+"' AND p.name=ch.parent and p.docstatus=1 AND p.posting_date>='"+str(filters.from_date)+"' AND p.posting_date<='"+str(filters.to_date)+"'",as_dict=1)
		for k in sql:
			for q in frappe.db.sql("SELECT DISTINCT(ch.account) FROM `tabJournal Entry Account`as ch,`tabJournal Entry`as p WHERE p.name='"+str(k.name)+"' AND p.name=ch.parent and p.docstatus=1 AND p.posting_date>='"+str(filters.from_date)+"' AND p.posting_date<='"+str(filters.to_date)+"'",as_dict=1):
				ar.append(q.account)
	unique_acc = set(ar)
	for val_acc in unique_acc:
		columns.append({
			"label": val_acc,
			"fieldtype": "Data",
			"fieldname": val_acc
			})
	return columns

def get_data(data, filters):
	data = []
	sing = []
	arj=[]
	for i in frappe.db.sql("SELECT DISTINCT(name) FROM `tabAccount` WHERE parent_account='Duties and Taxes - WTT' ",as_dict=1):
		sql = frappe.db.sql("SELECT ch.account,ch.debit_in_account_currency,ch.credit_in_account_currency,p.name,p.posting_date FROM `tabJournal Entry Account`as ch,`tabJournal Entry`as p WHERE ch.account='"+str(i.name)+"' AND p.name=ch.parent and p.docstatus=1 AND p.posting_date>='"+str(filters.from_date)+"' AND p.posting_date<='"+str(filters.to_date)+"'",as_dict=1)
		for k in sql:
			sing.append(k.name)
	uniq=set(sing)
	for vv in uniq:
		column={}
		v_query = frappe.db.sql("SELECT ch.account,ch.debit_in_account_currency,ch.credit_in_account_currency,p.name,p.user_remark,p.posting_date,p.total_debit,p.total_credit FROM `tabJournal Entry Account`as ch,`tabJournal Entry`as p WHERE p.name='"+str(vv)+"' AND p.name=ch.parent and p.docstatus=1 AND p.posting_date>='"+str(filters.from_date)+"' AND p.posting_date<='"+str(filters.to_date)+"'",as_dict=1)
		for d in v_query:
			column["posting_date"]=d.posting_date
			column["journal_entry"]=d.name
			column["user_remark"]=d.user_remark
			column["total_credit"]=d.total_credit
			column["total_debit"]=d.total_debit
			if(d.debit_in_account_currency>0):
				column[d.account]=d.debit_in_account_currency
			elif(d.credit_in_account_currency>0):
				column[d.account]=d.credit_in_account_currency
			else:
				column[d.account]="0"
		data.append(column)
	return data