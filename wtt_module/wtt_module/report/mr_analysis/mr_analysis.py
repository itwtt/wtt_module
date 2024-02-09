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
		"label":"Creater by",
		"fieldname":"creator",
		"fieldtype":"Data",
		"width":10
		},
		{
		"label":"Material Request",
		"fieldname":"material_request",
		"fieldtype":"Link",
		"options":"Material Request",
		"width":150
		},
		{
		"label":"MR Row",
		"fieldtype":"Int",
		"fieldname":"mr_row",
		"width":50
		},
		{
		"label":"Item Code",
		"fieldtype":"Link",
		"fieldname":"item_code",
		"options":"Item",
		"width":150
		},
		{
		"label":"Item Group",
		"fieldtype":"Data",
		"fieldname":"item_group",
		"width":150
		},
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
		"width":100
		},
		{
		"label":"MR Qty",
		"fieldname":"mr_qty",
		"fieldtype":"HTML",
		"width":100
		},
		{
		"label":"MI Qty",
		"fieldname":"mi_qty",
		"fieldtype":"HTML",
		"width":50
		},
		{
		"label":"MI NUM",
		"fieldname":"mi_num",
		"fieldtype":"Data",
		"width":100
		},
		{
		"label":"Purchase Order",
		"fieldname":"purchase_order",
		"fieldtype":"Link",
		"options":"Purchase Order",
		"width":150
		},
		{
		"label":"Supplier Description",
		"fieldname":"supplier_description",
		"fieldtype":"Data",
		"width":150
		},
		{
		"label":"PO Row",
		"fieldtype":"Int",
		"fieldname":"po_row",
		"width":50
		},
		{
		"label":"PO Qty",
		"fieldname":"po_qty",
		"fieldtype":"Data",
		"width":100
		},
		{
		"label":"rate",
		"fieldname":"po_rate",
		"fieldtype":"Float",
		"width":100
		},
		{
		"label":"Amount",
		"fieldname":"po_amt",
		"fieldtype":"Float",
		"width":100
		},
		{
		"label":"Purchase Receipt",
		"fieldname":"purchase_receipt",
		"fieldtype":"Link",
		"options":"Purchase Receipt",
		"width":150
		},
		{
		"label":"PR Row",
		"fieldtype":"Int",
		"fieldname":"pr_row",
		"width":50
		},
		{
		"label":"PR Qty",
		"fieldname":"pr_qty",
		"fieldtype":"Data",
		"width":100
		}
	]
	if(filters.club==1):
		columns=[
			{
			"label":"Creater by",
			"fieldname":"creator",
			"fieldtype":"Data",
			"width":10
			},
			{
			"label":"Material Request",
			"fieldname":"material_request",
			"fieldtype":"Link",
			"options":"Material Request",
			"width":150
			},
			{
			"label":"MR Row",
			"fieldtype":"Int",
			"fieldname":"mr_row",
			"width":50
			},
			{
			"label":"Item Code",
			"fieldtype":"Link",
			"fieldname":"item_code",
			"options":"Item",
			"width":150
			},
			{
			"label":"Item Group",
			"fieldtype":"Data",
			"fieldname":"item_group",
			"width":150
			},
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
			"width":100
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
			}
		]
	
	return columns
def get_data(data,filters):
	data=[]
	mr=[]
	mr_t=[]
	query=frappe.db.sql(" SELECT mri.parent,mri.name,mri.idx,mri.item_code,mri.mi_qty,mri.description,mri.technical_description,mri.qty,mri.uom FROM `tabMaterial Request`as mr,`tabMaterial Request Item`as mri where mr.name=mri.parent and mr.docstatus=1 and mr.project=%(project)s ORDER BY mr.name,mri.idx", filters, as_dict=1)
	for i in query:
		sup_dep=''
		po=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"parent")
		po_name=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"name")
		sup_dep=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"supplier_description")
		poq=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"qty")
		uom=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"uom")
		idx=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"idx")
		po_amt=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"base_net_amount")
		po_rate=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"base_net_rate")


		pr=frappe.db.get_value("Purchase Receipt Item",{"purchase_order":po,"purchase_order_item":po_name},"parent")
		pr_name=frappe.db.get_value("Purchase Receipt Item",{"purchase_order":po,"purchase_order_item":po_name},"name")
		prq=frappe.db.get_value("Purchase Receipt Item",{"purchase_order":po,"purchase_order_item":po_name},"qty")
		pr_uom=frappe.db.get_value("Purchase Receipt Item",{"purchase_order":po,"purchase_order_item":po_name},"uom")
		pr_idx=frappe.db.get_value("Purchase Receipt Item",{"purchase_order":po,"purchase_order_item":po_name},"idx")
		if(pr==None or po==None):
			pr=pr_name=pr_uom=pr_idx="-"
			prq=0
		ar=[]
		for k in frappe.db.sql("SELECT aa.name FROM `tabMaterial Issue` as aa,`tabMaterial Issue Item`as bb WHERE aa.name=bb.parent and bb.material_request='"+str(i.parent)+"' and bb.material_request_item='"+str(i.name)+"' and aa.docstatus=1 ",as_dict=1):
			ar.append(k.name)
		mi_name=""
		for j in ar:
			if(mi_name==""):
				mi_name+=str(j)
			else:
				mi_name+=","+str(j)
		po_am = 0.0
		if(po_amt!=None  and frappe.db.get_value("Purchase Order",po,"workflow_state")=="Approved"):
			po_am=po_amt

		if(poq!=None and frappe.db.get_value("Purchase Order",po,"workflow_state")=="Approved"):
			if(prq!=None and poq<=prq):
				po_q='<p style="background-color:yellow">'+str(poq)+' - '+str(uom)+'</p>'
				
			else:
				po_q='<p>'+str(poq)+' - '+str(uom)+'</p>'
		else:
			po_q='<b>-</b>'
		if(poq==i.qty and frappe.db.get_value("Purchase Order",po,"workflow_state")=="Approved"):
			ht1='<p style="background-color:lightgreen">'+str(i.qty)+' - '+str(i.uom)+'</p>'
		else:
			ht1='<p>'+str(i.qty)+' - '+str(i.uom)+'</p>'


		if(filters.not_received!=None):
			if(po!=None and pr==None):
				if(i.parent not in mr):
					mr.append(i.parent)
					data.append({})
					data.append({
						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
						"material_request":i.parent,
						"item_code":i.item_code,
						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
						"description":i.description,
						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
						"mr_qty":ht1,
						"mi_qty":i.mi_qty,
						"mi_num":mi_name,
						"purchase_order":po,
						"supplier_description":sup_dep,
						"po_qty":po_q,
						"po_amt":po_am,
						"mr_row":i.idx,
						"po_row":idx,
						"purchase_receipt":"-",
						"pr_qty":"-"
						})
				else:
					data.append({
						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
						"material_request":i.parent,
						"item_code":i.item_code,
						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
						"description":i.description,
						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
						"mr_qty":ht1,
						"mi_qty":i.mi_qty,
						"mi_num":mi_name,
						"purchase_order":po,
						"supplier_description":sup_dep,
						"po_qty":po_q,
						"po_amt":po_am,
						"mr_row":i.idx,
						"po_row":idx,
						"purchase_receipt":"-",
						"pr_qty":"-"
						})

		elif(filters.unlinked==None):
			if(pr!=None):
				if(i.parent not in mr):
					mr.append(i.parent)
					data.append({})
					data.append({
						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
						"material_request":i.parent,
						"item_code":i.item_code,
						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
						"description":i.description,
						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
						"mr_qty":ht1,
						"mi_qty":i.mi_qty,
						"mi_num":mi_name,
						"purchase_order":po,
						"supplier_description":sup_dep,
						"po_qty":po_q,
						"po_amt":po_am,
						"po_rate":po_rate,
						"mr_row":i.idx,
						"po_row":idx,
						"purchase_receipt":pr,
						"pr_qty":str(prq)
						})
				else:
					data.append({
						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
						"material_request":i.parent,
						"item_code":i.item_code,
						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
						"description":i.description,
						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
						"mr_qty":ht1,
						"purchase_order":po,
						"supplier_description":sup_dep,
						"po_qty":po_q,
						"po_amt":po_am,
						"po_rate":po_rate,
						"mr_row":i.idx,
						"mi_qty":i.mi_qty,
						"mi_num":mi_name,
						"po_row":idx,
						"purchase_receipt":pr,
						"pr_qty":str(prq)

						})
			else:
				if(i.parent not in mr):
					mr.append(i.parent)
					data.append({})
					data.append({
						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
						"material_request":i.parent,
						"item_code":i.item_code,
						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
						"description":i.description,
						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
						"mr_qty":ht1,
						"purchase_order":po,
						"supplier_description":sup_dep,
						"po_qty":po_q,
						"po_amt":po_am,
						"po_rate":po_rate,
						"mr_row":i.idx,
						"mi_qty":i.mi_qty,
						"mi_num":mi_name,
						"po_row":idx,
						"purchase_receipt":"-",
						"pr_qty":"-"
						})
				else:
					data.append({
						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
						"material_request":i.parent,
						"item_code":i.item_code,
						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
						"description":i.description,
						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
						"mr_qty":ht1,
						"purchase_order":po,
						"supplier_description":sup_dep,
						"po_qty":po_q,
						"po_amt":po_am,
						"po_rate":po_rate,
						"mr_row":i.idx,
						"mi_qty":i.mi_qty,
						"mi_num":mi_name,
						"po_row":idx,
						"purchase_receipt":"-",
						"pr_qty":"-"
						})
		else:
			if(po==None):
				if(filters.club==1):
					mr_t.append(i.name)
				else:
					if(i.parent not in mr):
						mr.append(str(i.parent))
						data.append({})
						data.append({
							"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
							"material_request":i.parent,
							"item_code":i.item_code,
							"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
							"description":i.description,
							"technical_description":i.technical_description if(i.technical_description!=None) else " ",
							"mr_qty":ht1,
							"mi_qty":i.mi_qty,
							"mi_num":mi_name,
							"purchase_order":po,
							"supplier_description":sup_dep,
							"po_qty":po_q,
							"po_amt":po_am,
							"mr_row":i.idx,
							"po_row":idx
							})
					else:
						data.append({
							"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
							"material_request":i.parent,
							"item_code":i.item_code,
							"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
							"description":i.description,
							"technical_description":i.technical_description if(i.technical_description!=None) else " ",
							"mr_qty":ht1,
							"mi_qty":i.mi_qty,
							"mi_num":mi_name,
							"purchase_order":po,
							"supplier_description":sup_dep,
							"po_qty":po_q,
							"po_amt":po_am,
							"mr_row":i.idx,
							"po_row":idx
							})

	if(len(mr_t)>=1):
		tup = str(tuple(mr_t))
		qq = frappe.db.sql("""SELECT item_code, 
			GROUP_CONCAT(distinct(parent))as material_request,
			GROUP_CONCAT(idx)as mr_row, 
			item_group,description,technical_description,
			sum(qty)as mr_qty,uom 
			FROM `tabMaterial Request Item`
			WHERE name in """+tup+""" GROUP BY item_code
			""",as_dict=1)
		for i in qq:
			data.append(i)	
	return data

# def get_conditions(filters):
# 	conditions=''
# 	if filters.get("project"):
# 		conditions += " and mr.project = %(project)s"

# 	match_conditions = build_match_conditions("Material Request")
# 	if match_conditions:
# 		conditions += " and %s" % match_conditions
# 	return conditions
