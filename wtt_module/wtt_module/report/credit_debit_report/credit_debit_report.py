# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime

def execute(filters=None):
	if not filters:
		return [], []
	data = []
	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data = get_data(conditions,data,filters)
	return columns, data

@frappe.whitelist()
def get_columns(filters):
	columns = [
		{
		"label": _("SUPPLIER"),
		"fieldname": "account_name",
		"fieldtype": "Data",
		"width": 150,
		},
		{
		"label": _("VOUCHER TYPE"),
		"fieldname": "voucher_type",
		"fieldtype": "Data",
		"width": 150,
		},
		{
		"label": _("DATE"),
		"fieldname": "date",
		"fieldtype": "Date",
		"width": 150,
		},
		{
		"label": _("BILL NO"),
		"fieldname": "bill_no",
		"fieldtype": "Data",
		"width": 150,
		},
		{
		"label": _("GST NO"),
		"fieldname": "gst_no",
		"fieldtype": "Data",
		"width": 150,
		},
		{
		"label": _("Taxable"),
		"fieldname": "taxable",
		"fieldtype": "Currency",
		"width": 150,
		},
		{
		"label": _("%"),
		"fieldname": "gst_per",
		"fieldtype": "Data",
		"width": 150,
		},
		{
		"label": _("SGST"),
		"fieldname": "gst_sgst",
		"fieldtype": "Data",
		"width": 150,
		},
		{
		"label": _("CGST"),
		"fieldname": "gst_cgst",
		"fieldtype": "Data",
		"width": 150,
		},
		{
		"label": _("IGST"),
		"fieldname": "igst",
		"fieldtype": "Data",
		"width": 150,
		},
		{
		"label": _("Invoice_value"),
		"fieldname": "invoice_value",
		"fieldtype": "Data",
		"width": 150,
		},
		{
		"label": _("Debit"),
		"fieldname": "debit",
		"fieldtype": "Currency",
		"width": 150,
		},
		{
		"label": _("Credit"),
		"fieldname": "credit",
		"fieldtype": "Currency",
		"width": 150,
		}
	]

	return columns

def get_data(conditions,data, filters):
	data=[]
	for i in frappe.db.sql("""SELECT jea.account,je.voucher_type,je.posting_date,je.cheque_no,je.total_credit,jea.credit,jea.debit FROM `tabJournal Entry Account` as jea INNER JOIN `tabJournal Entry` as je WHERE je.docstatus=1{conditions}""".format(conditions=conditions),as_dict=1):
		data.append({
			"account_name":i.account,
			"voucher_type":i.voucher_type,
			"date":i.posting_date,
			"bill_no":i.cheque_no,
			"invoice_value":i.total_credit,
			"debit":i.debit,
			"credit":i.credit
		})
	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("en_type"):
		conditions += " AND je.voucher_type='%s'" % filters.get('en_type')

	if filters.get("from_date"):
		conditions += " AND je.posting_date>='%s'" % filters.get('from_date')

	if filters.get("to_date"):
		conditions += " AND je.posting_date<='%s'" % filters.get('to_date')

	return conditions
