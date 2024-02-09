# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from datetime import datetime,timedelta
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
	data = []
	columns = get_columns(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	columns=[
		{
		"label":"Invoice No",
		"fieldname":"invoice_no",
		"fieldtype":"Link",
		"options":"Purchase Invoice",
		"width":100
		},
		{
		"label":"Supplier DC",
		"fieldname":"supplier_dc",
		"fieldtype":"Data",
		"width":200
		},
		{
		"label":"Invoice Date",
		"fieldname":"invoice_date",
		"fieldtype":"Date",
		"width":100
		},
		{
		"label":"Supplier",
		"fieldtype":"Data",
		"fieldname":"supplier",
		"width":200
		},
		{
		"label":"Tax ID",
		"fieldname":"tax_id",
		"fieldtype":"Data",
		"width":200
		},
		{
		"label":"Total",
		"fieldname":"total",
		"fieldtype":"Data",
		"width":100
		},
		{
		"label":"Taxable Value",
		"fieldname":"taxable_value",
		"fieldtype":"Data",
		"width":100
		},
	]
	for i in frappe.db.sql("SELECT distinct(account_name)as account_name from `tabGST Table` where parent='"+str(filters.reconcile_number)+"' ",as_dict=1):
		columns.append({
			"label":i.account_name,
			"fieldname":i.account_name,
			"fieldtype":"HTML",
			"width":100
			})
	
	return columns
def get_data(data,filters):
	data=[]
	unique_line=[]
	unique_invoice=[]
	query=frappe.db.sql("""SELECT 
			distinct(gt.`name`)as 'name',
			gt.`supplier_dc`,
			gt.`invoice_no`,
			gt.`invoice_date`,
			gt.`supplier`,
			gt.`tax_id`,
			gt.`account_name`,
			gt.`tax`,
			ut.`tax_name`,
			gt.`amount`as 'amount_in_erp',
			ut.`amount` as 'amount',
			gt.`taxable_value`,
			gt.`invoice_amount`
			FROM `tabGST Upload Table` as ut,`tabGST Table`as gt 
			INNER JOIN `tabGST reconcilation` as gr 
			ON gt.`parent`='"""+str(filters.reconcile_number)+"""' 
			WHERE  ut.`tax_name`=gt.`tax` and ut.`supplier_dc`=gt.`supplier_dc` and gt.`amount`!=ut.`amount` 
			ORDER BY gt.`invoice_no`
			""",as_dict=1)

	for i in query:
		if(i.name not in unique_line):
			unique_line.append(i.name)
			column={}
			column2={}
			if(i.invoice_no not in unique_line):
				unique_invoice.append(i.invoice_no)
				column['invoice_no']=i.invoice_no
				column['supplier_dc']=i.supplier_dc
				column['invoice_date']=i.invoice_date
				column['tax_id']=i.tax_id
				column['supplier']=i.supplier
				column['taxable_value']=i.taxable_value
				column['total']=i.invoice_amount
				column[i.account_name]='<p style="background-color:lightgreen">'+str(i.amount_in_erp)+'</p>'
				column2[i.account_name]='<p style="background-color:tomato">'+str(i.amount)+'</p>'
			else:
				column[i.account_name]='<p style="background-color:lightgreen">'+str(i.amount_in_erp)+'</p>'
				column2[i.account_name]='<p style="background-color:tomato">'+str(i.amount)+'</p>'
			data.append(column)
			data.append(column2)

		else:
			pass


	
	return data