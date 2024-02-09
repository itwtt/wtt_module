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
	"label": _("Purchase Order"),
	"fieldname": "purchase_order",
	"fieldtype": "Link",
	"options":"Purchase Order",
	"width": 150
	},
	{
	"label": _("Supplier"),
	"fieldname": "supplier",
	"fieldtype": "Link",
	"options":"Supplier",
	"width": 150
	},
	{
	"label": _("Project"),
	"options": "Project",
	"fieldname": "project",
	"fieldtype": "Link",
	"width": 90
	},
	{
	"label": _("Item Code"),
	"fieldname": "item_code",
	"fieldtype": "Link",
	"options":"Item",
	"width": 150
	},
	{
	"label": _("Description"),
	"fieldname": "description",
	"fieldtype": "Data",
	"width": 150
	},
	{
	"label": _("Technical Description"),
	"fieldname": "technical_description",
	"fieldtype": "Data",
	"width": 300
	},
	{
	"label": _("Supplier Description"),
	"fieldname": "supplier_description",
	"fieldtype": "Data",
	"width": 200
	},
	{
	"label": _("Rate1"),
	"fieldname": "rate1",
	"fieldtype": "Data",
	"width": 220
	},
	{
	"label": _("Rate2"),
	"fieldname": "rate2",
	"fieldtype": "Data",
	"width": 220
	},
	{
	"label": _("Rate3"),
	"fieldname": "rate3",
	"fieldtype": "Data",
	"width": 220
	},
	]
	return columns

def get_data(conditions,data, filters):
	data=[]
	po_details = frappe.db.sql("""SELECT po.name,po.supplier,po.project,poi.item_code,poi.description,poi.technical_description,poi.supplier_description from `tabPurchase Order` as po INNER JOIN `tabPurchase Order Item` as poi ON po.name=poi.parent where po.naming_series='PO-.YY.-' and po.docstatus=1{conditions}""".format(conditions=conditions), as_dict=1)
	for i in po_details:
		doc=frappe.db.sql("SELECT (SELECT CONCAT(round(rate,2),' - ',parent) FROM `tabPurchase Order Item` WHERE item_code='"+str(i.item_code)+"' GROUP BY parent ORDER BY creation DESC LIMIT 1) as 'Rate1', (SELECT CONCAT(round(rate,2),' - ',parent) FROM `tabPurchase Order Item` WHERE item_code='"+str(i.item_code)+"' GROUP BY parent ORDER BY creation DESC LIMIT 1,1) as 'Rate2', (SELECT CONCAT(round(rate,2),' - ',parent) FROM `tabPurchase Order Item` WHERE item_code='"+str(i.item_code)+"' GROUP BY parent ORDER BY creation DESC LIMIT 2,1) as 'Rate3' FROM `tabPurchase Order Item` WHERE item_code='"+str(i.item_code)+"' GROUP BY parent ORDER BY creation DESC LIMIT 1",as_dict=1)
		if(doc):
			for j in doc:
				data.append({
				"purchase_order":i.name,
				"supplier":i.supplier,
				"project":i.project,
				"item_code":i.item_code,
				"description":i.description,
				"technical_description":i.technical_description,
				"supplier_description":i.supplier_description,
				"rate1":j.Rate1,
				"rate2":j.Rate2,
				"rate3":j.Rate3
				})
		else:
			data.append({
			"purchase_order":i.name,
			"supplier":i.supplier,
			"project":i.project,
			"item_code":i.item_code,
			"description":i.description,
			"technical_description":i.technical_description,
			"supplier_description":i.supplier_description,
			"rate1":"-",
			"rate2":"-",
			"rate3":"-"
			})
	return data

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND po.creation>='%s'" % filters.get('from_date')

    if filters.get("to_date"):
        conditions += " AND po.creation<='%s'" % filters.get('to_date')

    if filters.get("supplier"):
        conditions += " AND po.supplier='%s'" % filters.get('supplier')

    if filters.get("project"):
        conditions += " AND po.project='%s'" % filters.get('project')

    if filters.get("name"):
        conditions += " AND po.name='%s'" % filters.get('name')

    return conditions