# Copyright (c) 2022, wtt_module and contributors
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
			"label":"Project",
			"fieldname":"project",
			"fieldtype":"Link",
			"options":"Project",
			"width":150
			},
			{
			"label":"Project Name",
			"fieldname":"project_name",
			"fieldtype":"Data",
			"width":300
			},
			{
			"label":"Cost of Order",
			"fieldname":"po_cost",
			"fieldtype":"Currency",
			"width":200
			},
			# {
			# "label":"Tax of Order",
			# "fieldname":"po_tax",
			# "fieldtype":"Currency",
			# "width":200
			# },
			{
			"label":"Cost of Receipt",
			"fieldname":"pr_cost",
			"fieldtype":"Currency",
			"width":200
			},
			# {
			# "label":"Tax of Receipt",
			# "fieldname":"pr_tax",
			# "fieldtype":"Currency",
			# "width":200
			# },
			# {
			# "label":"PO Reference",
			# "fieldname":"po_ref",
			# "fieldtype":"HTML",
			# "width":150
			# }
			]
	return columns

def get_data(data,filters):
	# for i in frappe.db.sql("SELECT parent as 'po_par',project as 'project',(SELECT project_name FROM `tabProject` WHERE name=project) as 'project_name',sum(base_net_amount) as 'sum' FROM `tabPurchase Order Item` WHERE docstatus=1 and project NOT IN ('INT-HHT','HHT-INT','HO00001','HO-INT01','TTH00001','WTT-SALES','MDH00001','WTT-RD0002','SAL-0001','HOF00001','SATHY00001','OM00001') GROUP BY project",as_dict=1):
	for i in frappe.db.sql("SELECT parent as 'po_par',project as 'project',(SELECT project_name FROM `tabProject` WHERE name=project) as 'project_name',sum(base_net_amount) as 'sum' FROM `tabPurchase Order Item` WHERE docstatus=1 and project NOT IN ('INT-HHT','SATHY00001','OM00001') GROUP BY project",as_dict=1):
	# for i in frappe.db.sql("SELECT distinct(po.name) as 'po_par',poi.project as 'project',(SELECT project_name FROM `tabProject` WHERE name=poi.project) as 'project_name',sum(poi.base_net_amount) as 'sum',sum(po.total_taxes_and_charges) as 'potax' FROM `tabPurchase Order`as po,`tabPurchase Order Item`as poi WHERE poi.parent=po.name and po.docstatus=1 GROUP BY poi.project",as_dict=1):
		if(frappe.db.get_value("Project",i.project,"status")=="On going"):
			ar=[]
			ar2=[]
			for j in frappe.db.sql("SELECT base_net_amount FROM `tabPurchase Receipt Item` WHERE docstatus=1 and project='"+str(i.project)+"'",as_dict=1):
				ar.append(j.base_net_amount)
			data.append({
				"project":i.project,
				"project_name":i.project_name,
				"po_cost":i.sum,
				"pr_cost":sum(ar)
				# "po_ref":"<a href='https://erp.wttindia.com/app/query-report/Project%20Cost%20Supplier%20Wise?project_name="+str(i.project)+"'><b style='color:blue'>Go to Reference</b></a>"
			})
	return data