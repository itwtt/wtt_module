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
	# conditions = get_conditions(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	
	columns=[
		{
		"label":"Material Request",
		"fieldname":"material_request",
		"fieldtype":"Link",
		"options":"Material Request",
		"width":150
		},
		{
		"label":"Item Group",
		"fieldtype":"Data",
		"fieldname":"item_group",
		"width":150
		},
		{
		"label":"MR Qty",
		"fieldname":"mr_qty",
		"fieldtype":"Float",
		"width":100
		},
		{
		"label":"UOM",
		"fieldname":"uom",
		"fieldtype":"Data",
		"width":100
		},
		{
		"label":"PO Qty",
		"fieldname":"po_qty",
		"fieldtype":"Float",
		"width":100
		},
		{
		"label":"Reference",
		"fieldname":"po_ref",
		"fieldtype":"Small Text",
		"width":100
		},
		{
		"label":"Draft PO Qty",
		"fieldname":"draft_po_qty",
		"fieldtype":"Float",
		"width":100
		},
		{
		"label":"Reference",
		"fieldname":"draft_po_ref",
		"fieldtype":"Small Text",
		"width":100
		},
		{
		"label":"Receipt",
		"fieldname":"pr_ref",
		"fieldtype":"Small Text",
		"width":100
		},
	]
	
	return columns
def get_data(data,filters):
	data=[]
	if(filters.group_by=="Item Group"):
		query=frappe.db.sql("""SELECT mri.item_group,sum(mri.qty)as mr_qty,mr.name as material_request,mri.uom
			FROM `tabMaterial Request Item`as mri, `tabMaterial Request` as mr 
			WHERE mri.parent=mr.name and mr.docstatus!=2 and mr.workflow_state!='Rejected' and mr.project='"""+str(filters.project)+"""' GROUP BY mr.name,mri.item_group
			""",as_dict=1)

		for i in query:
			po_qty=frappe.db.sql("SELECT sum(poi.qty)as qty FROM `tabPurchase Order Item`as poi,`tabPurchase Order`as po WHERE po.name=poi.parent and po.docstatus=1 and poi.project='"+str(filters.project)+"' and poi.material_request='"+str(i.material_request)+"' and poi.item_group='"+str(i.item_group)+"' ",as_dict=1)
			po_ref=frappe.db.sql("SELECT GROUP_CONCAT(distinct(po.name))as name FROM `tabPurchase Order Item`as poi,`tabPurchase Order`as po WHERE po.name=poi.parent and po.docstatus=1 and poi.project='"+str(filters.project)+"' and poi.material_request='"+str(i.material_request)+"' and poi.item_group='"+str(i.item_group)+"' ",as_dict=1)
			draft_po_qty=frappe.db.sql("SELECT sum(poi.qty)as qty FROM `tabPurchase Order Item`as poi,`tabPurchase Order`as po WHERE po.name=poi.parent and po.docstatus=0 and po.workflow_state!='Rejected' and poi.project='"+str(filters.project)+"' and poi.material_request='"+str(i.material_request)+"' and poi.item_group='"+str(i.item_group)+"' ",as_dict=1)
			draft_po_ref=frappe.db.sql("SELECT GROUP_CONCAT(distinct(po.name))as name FROM `tabPurchase Order Item`as poi,`tabPurchase Order`as po WHERE po.name=poi.parent and po.docstatus=0 and po.workflow_state!='Rejected' and poi.project='"+str(filters.project)+"' and poi.material_request='"+str(i.material_request)+"' and poi.item_group='"+str(i.item_group)+"' ",as_dict=1)
			pr_ref=frappe.db.sql("SELECT GROUP_CONCAT(distinct(pr.name))as name FROM `tabPurchase Receipt`as pr,`tabPurchase Receipt Item`as pri WHERE pri.parent=pr.name and pri.description='"+str(i.item_group)+"' and pri.project='"+str(filters.project)+"' and pri.material_request='"+str(i.material_request)+"' ",as_dict=1)
			data.append({
				"material_request":i.material_request,
				"mr_qty":i.mr_qty,
				"uom":i.uom,
				"item_group":i.item_group,
				"po_qty":po_qty[0]["qty"],
				"po_ref":po_ref[0]["name"],
				"draft_po_ref":draft_po_ref[0]["name"],
				"draft_po_qty":draft_po_qty[0]["qty"],
				"pr_ref":pr_ref[0]["name"]
				})
	elif(filters.group_by=="Description"):
		query=frappe.db.sql("""SELECT mri.description,sum(mri.qty)as mr_qty,mr.name as material_request,mri.uom
			FROM `tabMaterial Request Item`as mri, `tabMaterial Request` as mr 
			WHERE mri.parent=mr.name and mr.docstatus!=2 and mr.workflow_state!='Rejected' and mr.project='"""+str(filters.project)+"""' GROUP BY mr.name,mri.description
			""",as_dict=1)

		for i in query:
			po_qty=frappe.db.sql("SELECT sum(poi.qty)as qty FROM `tabPurchase Order Item`as poi,`tabPurchase Order`as po WHERE po.name=poi.parent and po.docstatus=1 and poi.project='"+str(filters.project)+"' and poi.material_request='"+str(i.material_request)+"' and poi.description='"+str(i.description)+"' ",as_dict=1)
			po_ref=frappe.db.sql("SELECT GROUP_CONCAT(distinct(po.name))as name FROM `tabPurchase Order Item`as poi,`tabPurchase Order`as po WHERE po.name=poi.parent and po.docstatus=1 and poi.project='"+str(filters.project)+"' and poi.material_request='"+str(i.material_request)+"' and poi.description='"+str(i.description)+"' ",as_dict=1)
			draft_po_qty=frappe.db.sql("SELECT sum(poi.qty)as qty FROM `tabPurchase Order Item`as poi,`tabPurchase Order`as po WHERE po.name=poi.parent and po.docstatus=0 and po.workflow_state!='Rejected' and poi.project='"+str(filters.project)+"' and poi.material_request='"+str(i.material_request)+"' and poi.description='"+str(i.description)+"' ",as_dict=1)
			draft_po_ref=frappe.db.sql("SELECT GROUP_CONCAT(distinct(po.name))as name FROM `tabPurchase Order Item`as poi,`tabPurchase Order`as po WHERE po.name=poi.parent and po.docstatus=0 and po.workflow_state!='Rejected' and poi.project='"+str(filters.project)+"' and poi.material_request='"+str(i.material_request)+"' and poi.description='"+str(i.description)+"' ",as_dict=1)
			pr_ref=frappe.db.sql("SELECT GROUP_CONCAT(distinct(pr.name))as name FROM `tabPurchase Receipt`as pr,`tabPurchase Receipt Item`as pri WHERE pri.parent=pr.name and pri.description='"+str(i.description)+"' and pri.project='"+str(filters.project)+"' and pri.material_request='"+str(i.material_request)+"' ",as_dict=1)
			data.append({
				"material_request":i.material_request,
				"mr_qty":i.mr_qty,
				"uom":i.uom,
				"item_group":i.description,
				"po_qty":po_qty[0]["qty"],
				"po_ref":po_ref[0]["name"],
				"draft_po_ref":draft_po_ref[0]["name"],
				"draft_po_qty":draft_po_qty[0]["qty"],
				"pr_ref":pr_ref[0]["name"]
				})

	return data