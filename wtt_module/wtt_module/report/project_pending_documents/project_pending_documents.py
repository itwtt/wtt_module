# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from datetime import datetime,timedelta
from frappe.desk.reportview import build_match_conditions
from urllib.parse import urlencode

def execute(filters=None):
	data = []
	columns = get_columns(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	columns=[
		{
		"label":"Project",
		"fieldname":"project",
		"fieldtype":"Link",
		"options":"Project",
		"width":100,
		"hidden":1
		},
		{
		"label":"Project",
		"fieldname":"project_name",
		"fieldtype":"Data",
		"width":270
		},
		{
		"label": _("MR Created"),
		"fieldname": "mr_created",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("MR Created Link"),
		"fieldname": "mr_cre_link",
		"fieldtype": "HTML",
		"width": 80
		},
		{
		"label": _("MR HOD"),
		"fieldname": "mr_hod",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("MR HOD Link"),
		"fieldname": "mr_hod_link",
		"fieldtype": "HTML",
		"width": 80
		},
		{
		"label": _("PO Created"),
		"fieldname": "po_created",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("PO Created Link"),
		"fieldname": "po_cre_link",
		"fieldtype": "HTML",
		"width": 80
		},
		{
		"label": _("PO HOD"),
		"fieldname": "po_hod",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("PO HOD Link"),
		"fieldname": "po_hod_link",
		"fieldtype": "HTML",
		"width": 80
		},
		{
		"label": _("PR Draft"),
		"fieldname": "pr_draft",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("PR Draft Link"),
		"fieldname": "pr_cre_link",
		"fieldtype": "HTML",
		"width": 80
		}
	]	
	return columns
def get_data(data,filters):
	data=[]
	for i in frappe.db.sql("SELECT name,project_name FROM `tabProject` WHERE status='On going' and name NOT IN ('WTT-0408','WTT-0206','INT-HHT','HHT-INT','HO00001','HO-INT01','TTH00001','WTT-SALES','MDH00001','WTT-RD0002','SAL-0001','HOF00001','SATHY00001','OM00001')",as_dict=1):
		mr_cre=frappe.db.count('Material Request', {'workflow_state': 'Created','project':i.name})
		mr_hod=frappe.db.count('Material Request', {'workflow_state': 'Approved by HOD','project':i.name})
		po_cre = frappe.db.count('Purchase Order', {'workflow_state': 'Created','project':i.name})
		po_hod = frappe.db.count('Purchase Order', {'workflow_state': 'Approved by HOD','project':i.name})
		pr_draft = frappe.db.count('Purchase Receipt', {'status': 'Draft','project':i.name})

		base_url = "https://erp.wttindia.com/app/material-request"
		query_params = {
		'workflow_state': 'Created',
		'project': str(i.name)
		}
		mr_cre_link = base_url + '?' + urlencode(query_params)


		base_url = "https://erp.wttindia.com/app/material-request"
		query_params = {
		'workflow_state': 'Approved by HOD',
		'project': str(i.name)
		}
		mr_hod_link = base_url + '?' + urlencode(query_params)


		base_url = "https://erp.wttindia.com/app/purchase-order"
		query_params = {
		'workflow_state': 'Created',
		'project': str(i.name)
		}
		po_cre_link = base_url + '?' + urlencode(query_params)

		base_url = "https://erp.wttindia.com/app/purchase-order"
		query_params = {
		'workflow_state': 'Approved by HOD',
		'project': str(i.name)
		}
		po_hod_link = base_url + '?' + urlencode(query_params)

		base_url = "https://erp.wttindia.com/app/purchase-receipt"
		query_params = {
		'status': 'Draft',
		'project': str(i.name)
		}
		pr_cre_link = base_url + '?' + urlencode(query_params)

		if(mr_cre == 0):
			mr_cre = '-'
		if(mr_hod == 0):
			mr_hod = '-'
		if(po_cre == 0):
			po_cre = '-'
		if(po_hod == 0):
			po_hod = '-'
		if(pr_draft == 0):
			pr_draft = '-'
		data.append({
			"project":i.name,
			"project_name":i.project_name,
			"mr_created":mr_cre,
			"mr_cre_link":"<a href='"+str(mr_cre_link)+"'><b style='color:blue'>MR</b></a>",
			"mr_hod":mr_hod,
			"mr_hod_link":"<a href='"+str(mr_hod_link)+"'><b style='color:orange'>MR</b></a>",
			"po_created":po_cre,
			"po_cre_link":"<a href='"+str(po_cre_link)+"'><b style='color:blue'>PO</b></a>",
			"po_hod":po_hod,
			"po_hod_link":"<a href='"+str(po_hod_link)+"'><b style='color:orange'>PO</b></a>",
			"pr_draft":pr_draft,
			"pr_cre_link":"<a href='"+str(pr_cre_link)+"'><b style='color:blue'>PR</b></a>",
		})
	return data
