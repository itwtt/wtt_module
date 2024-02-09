from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime

def execute(filters=None):
	data = []
	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data = get_data(conditions,data,filters)
	return columns, data

@frappe.whitelist()
def get_columns(filters):
	columns = [
		{
		"label": _("Supplier Name"),
		"fieldname": "supplier",
		"fieldtype": "Data",
		"width": 250
		},
		{
		"label": _("Items"),
		"fieldname": "description",
		"fieldtype": "Data",
		"width": 300
		},
		{
		"label": _("Email ID"),
		"fieldname": "email_id",
		"fieldtype": "Data",
		"width": 180
		},
		{
		"label": _("Phone"),
		"fieldname": "phone",
		"fieldtype": "Data",
		"width": 150
		},
		{
		"label": _("Tax ID"),
		"fieldname": "tax_id",
		"fieldtype": "Data",
		"width": 150
		},
		{
		"label": _("Category"),
		"fieldname": "tax_category",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("Bank"),
		"fieldname": "bank",
		"fieldtype": "Data",
		"width": 200
		},
		{
		"label": _("Account No"),
		"fieldname": "bank_account_no",
		"fieldtype": "Data",
		"width": 150
		},
		{
		"label": _("IFSC"),
		"fieldname": "ifsc",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("Branch"),
		"fieldname": "branch",
		"fieldtype": "Data",
		"width": 150
		},
		{
		"label": _("Address 1"),
		"fieldname": "address_line1",
		"fieldtype": "Data",
		"width": 150
		},
		{
		"label": _("Address 2"),
		"fieldname": "address_line2",
		"fieldtype": "Data",
		"width": 150
		},
		{
		"label": _("City"),
		"fieldname": "city",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("State"),
		"fieldname": "state",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("Country"),
		"fieldname": "country",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("Pincode"),
		"fieldname": "pincode",
		"fieldtype": "Data",
		"width": 80
		}
	]

	return columns

def get_data(conditions,data, filters):
	data=[]
	for i in frappe.db.sql("""SELECT name,tax_id,tax_category,bank,bank_account_no,ifsc_code,branch FROM `tabSupplier` WHERE disabled=0{conditions}""".format(conditions=conditions), as_dict=1):
		for k in frappe.db.sql("select GROUP_CONCAT(distinct(poi.description)) as 'aab' FROM `tabPurchase Order Item`as poi INNER JOIN `tabPurchase Order`as po ON po.name=poi.parent WHERE po.supplier='"+str(i.name)+"' and po.docstatus=1",as_dict=1):
			if(k):
				for j in frappe.db.sql("SELECT ads.email_id,ads.phone,ads.address_line1,ads.address_line2,ads.city,ads.state,ads.country,ads.pincode FROM `tabAddress` AS ads INNER JOIN `tabDynamic Link` as dl ON ads.name=dl.parent WHERE dl.link_doctype='Supplier' and dl.link_name='"+str(i.name)+"'",as_dict=1):
					data.append({
						"supplier":i.name,
						"description":k.aab,
						"tax_id":i.tax_id,
						"tax_category":i.tax_category,
						"bank":i.bank,
						"bank_account_no":i.bank_account_no,
						"ifsc":i.ifsc_code,
						"branch":i.branch,
						"email_id":j.email_id,
						"phone":j.phone,
						"address_line1":j.address_line1,
						"address_line2":j.address_line2,
						"city":j.city,
						"state":j.state,
						"country":j.country,
						"pincode":j.pincode
					})
			else:
				for j in frappe.db.sql("SELECT ads.email_id,ads.phone,ads.address_line1,ads.address_line2,ads.city,ads.state,ads.country,ads.pincode FROM `tabAddress` AS ads INNER JOIN `tabDynamic Link` as dl ON ads.name=dl.parent WHERE dl.link_doctype='Supplier' and dl.link_name='"+str(i.name)+"'",as_dict=1):
					data.append({
						"supplier":i.name,
						"description":'-',
						"tax_id":i.tax_id,
						"tax_category":i.tax_category,
						"bank":i.bank,
						"bank_account_no":i.bank_account_no,
						"ifsc":i.ifsc_code,
						"branch":i.branch,
						"email_id":j.email_id,
						"phone":j.phone,
						"address_line1":j.address_line1,
						"address_line2":j.address_line2,
						"city":j.city,
						"state":j.state,
						"country":j.country,
						"pincode":j.pincode
					})
	return data

def get_conditions(filters):
	conditions = ""
	if filters.get("supplier"):
		conditions += " AND name='%s'" % filters.get('supplier')

	return conditions