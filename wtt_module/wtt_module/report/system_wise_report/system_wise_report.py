# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

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
	columns=[
		{
		"label": _("BOM"),
		"fieldtype": "Link",
		"fieldname": "bom",
		"options": "BOM",
		"width": 180
		},
		{
		"label": _("System Name"),
		"fieldtype": "Data",
		"fieldname": "system_name",
		"width": 180
		},
		{
		"label": _("Total Cost"),
		"fieldtype": "Currency",
		"fieldname": "total_cost",
		"width": 180
		},
		{
		"label": _("BOM Link"),
		"fieldtype": "HTML",
		"fieldname": "bom_link",
		"width": 180
		}
	]
	return columns

def get_data(data, filters):
	data=[]
	query=frappe.db.sql("SELECT * FROM `tabBOM` WHERE is_default=1",as_dict=1)
	for i in query:
		column = {}
		rate_from_bom=[]
		column['bom'] = i.name
		column['system_name'] = i.title
		for bb in frappe.db.sql("SELECT distinct(name),item_code,parent,stock_qty,stock_uom,total_weight from `tabBOM Item` where parent='"+str(i.name)+"' ",as_dict=1):
			if(str(bb.item_code)[slice(3)]!="S60"):
				for rate in frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,`tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(bb.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
					rate_from_bom.append(rate.base_rate*bb.stock_qty)
			else:
				query_s6=frappe.db.sql("SELECT rate from `tabBOM Template for S6 Materials` where parent='BOM Template' and item_code='"+str(bb.item_code)+"' ",as_dict=1)
				if(query_s6):
					rate_from_bom.append(query_s6[0].rate*bb.total_weight)
		column['total_cost'] = round(sum(rate_from_bom),2)
		column['bom_link'] = "<a href='https://erp.wttindia.com/app/query-report/BOM?bom="+str(i.name)+"'><b style='color:blue'>Go to Cost</b></a>"
		# column['bom_link'] = "<p style=color:red><a href=https://erp.wttindia.com/app/query-report/BOM?bom='"+str(i.name)+"' target=_blank>Go to Report</a></p>"
		data.append(column)
	return data