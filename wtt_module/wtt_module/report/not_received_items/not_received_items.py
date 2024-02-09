# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	# if not filters:
	# 	return [],[]
	data = []
	columns = get_columns(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	columns=[
		{
		"label":"Description",
		"fieldname":"description",
		"fieldtype":"Data",
		"width":100
		},
		{
		"label":"Technical Description",
		"fieldname":"technical_description",
		"fieldtype":"Small Text",
		"width":200
		},
		{
		"label":"Purchase Order",
		"fieldname":"purchase_order",
		"fieldtype":"Link",
		"options":"Purchase Order",
		"width":150
		},
		{
		"label":"Supplier",
		"fieldname":"supplier",
		"fieldtype":"Link",
		"options":"Supplier",
		"width":150
		},
		{
		"label":"PO Row",
		"fieldtype":"Int",
		"fieldname":"po_row",
		"width":100
		},
		{
		"label":"PO Qty",
		"fieldname":"po_qty",
		"fieldtype":"Data",
		"width":100
		},
		{
		"label":"Item Group",
		"fieldtype":"Data",
		"fieldname":"item_group",
		"width":100
		},
		{
		"label":"Item Code",
		"fieldtype":"Link",
		"fieldname":"item_code",
		"options":"Item",
		"width":50
		}
		]
	return columns

def get_data(data,filters):
	data=[]
	po_query=frappe.db.sql("SELECT po.supplier,poi.item_code,poi.description,poi.technical_description,poi.item_group,poi.idx,poi.qty,poi.parent,poi.name FROM `tabPurchase Order` as po INNER JOIN `tabPurchase Order Item` as poi WHERE po.name=poi.parent AND po.workflow_state='Approved'",as_dict=1)
	if(filters.project!=None):
		po_query=frappe.db.sql("SELECT po.supplier,poi.item_code,poi.description,poi.technical_description,poi.item_group,poi.idx,poi.qty,poi.parent,poi.name FROM `tabPurchase Order` as po INNER JOIN `tabPurchase Order Item` as poi WHERE po.name=poi.parent AND po.workflow_state='Approved' and poi.project='"+str(filters.project)+"' ",as_dict=1)

	for i in po_query:
		doc=frappe.db.sql("SELECT * FROM `tabPurchase Receipt Item` WHERE purchase_order='"+str(i.parent)+"' and purchase_order_item='"+str(i.name)+"'",as_dict=1)
		if doc:
			pass
		else:
			data.append({
					'item_code':i.item_code,
					'description':i.description,
					'technical_description':i.technical_description,
					'item_group':i.item_group,
					'purchase_order':i.parent,
					'supplier':i.supplier,
					'po_row':i.idx,
					'po_qty':i.qty
					})
	return data