# # Copyright (c) 2013, wtt_module and contributors
# # For license information, please see license.txt

# from __future__ import unicode_literals
# import frappe
# from frappe import _
# import numpy as np
# from datetime import datetime,timedelta
# from frappe.desk.reportview import build_match_conditions

# def execute(filters=None):
# 	data = []
# 	columns = get_columns(filters)
# 	# conditions = get_conditions(filters)
# 	data = get_data(data,filters)
# 	return columns, data

# def get_columns(filters):
# 	columns=[
# 		{
# 		"label":"Creater by",
# 		"fieldname":"creator",
# 		"fieldtype":"Data",
# 		"width":10
# 		},
# 		{
# 		"label":"Material Request",
# 		"fieldname":"material_request",
# 		"fieldtype":"Link",
# 		"options":"Material Request",
# 		"width":150
# 		},
# 		{
# 		"label":"MR Row",
# 		"fieldtype":"Int",
# 		"fieldname":"mr_row",
# 		"width":50
# 		},
# 		{
# 		"label":"Freeze Qty",
# 		"fieldtype":"Float",
# 		"fieldname":"fre_qty",
# 		"width":80
# 		},
# 		{
# 		"label":"Item Code",
# 		"fieldtype":"Link",
# 		"fieldname":"item_code",
# 		"options":"Item",
# 		"width":150
# 		},
# 		{
# 		"label":"Item Group",
# 		"fieldtype":"Data",
# 		"fieldname":"item_group",
# 		"width":150
# 		},
# 		{
# 		"label":"Description",
# 		"fieldname":"description",
# 		"fieldtype":"Data",
# 		"width":100
# 		},
# 		{
# 		"label":"Technical Description",
# 		"fieldname":"technical_description",
# 		"fieldtype":"Small Text",
# 		"width":100
# 		},
# 		{
# 		"label":"MR Qty",
# 		"fieldname":"mr_qty",
# 		"fieldtype":"HTML",
# 		"width":100
# 		},
# 		{
# 		"label":"MI Qty",
# 		"fieldname":"mi_qty",
# 		"fieldtype":"HTML",
# 		"width":50
# 		},
# 		{
# 		"label":"MI NUM",
# 		"fieldname":"mi_num",
# 		"fieldtype":"Data",
# 		"width":100
# 		},
# 		{
# 		"label":"Purchase Order",
# 		"fieldname":"purchase_order",
# 		"fieldtype":"Link",
# 		"options":"Purchase Order",
# 		"width":150
# 		},
# 		{
# 		"label":"PO workflow",
# 		"fieldname":"po_workflow",
# 		"fieldtype":"Data",
# 		"width":100
# 		},
# 		{
# 		"label":"PO Row",
# 		"fieldtype":"Int",
# 		"fieldname":"po_row",
# 		"width":50
# 		},
# 		{
# 		"label":"PO Qty",
# 		"fieldname":"po_qty",
# 		"fieldtype":"Data",
# 		"width":100
# 		},
# 		{
# 		"label":"rate",
# 		"fieldname":"po_rate",
# 		"fieldtype":"Float",
# 		"width":100
# 		},
# 		{
# 		"label":"Amount",
# 		"fieldname":"po_amt",
# 		"fieldtype":"Float",
# 		"width":100
# 		},
# 		{
# 		"label":"Purchase Receipt",
# 		"fieldname":"purchase_receipt",
# 		"fieldtype":"Link",
# 		"options":"Purchase Receipt",
# 		"width":150
# 		},
# 		{
# 		"label":"PR Row",
# 		"fieldtype":"Int",
# 		"fieldname":"pr_row",
# 		"width":50
# 		},
# 		{
# 		"label":"PR Qty",
# 		"fieldname":"pr_qty",
# 		"fieldtype":"Data",
# 		"width":100
# 		},
# 		{
# 		"label": _("DC Date"),
# 		"fieldname": "dc_date",
# 		"fieldtype": "Date",
# 		"width": 100
# 		},
# 		{
# 		"label": _("DC row"),
# 		"fieldname": "dc_row",
# 		"fieldtype": "Data",
# 		"width": 80
# 		},
# 		{
# 		"label": _("DC No"),
# 		"fieldname": "dc_no",
# 		"fieldtype": "Link",
# 		"width": 170,
# 		"options":"Delivery Note"
# 		},
# 		{
# 		"label": _("DC Qty"),
# 		"fieldname": "dc_qty",
# 		"fieldtype": "Float",
# 		"width": 80
# 		},
# 		{
# 		"label": _("Status"),
# 		"fieldname": "dc_status",
# 		"fieldtype": "HTML",
# 		"width": 120
# 		}
# 	]
# 	if(filters.club==1):
# 		columns=[
# 			{
# 			"label":"Creater by",
# 			"fieldname":"creator",
# 			"fieldtype":"Data",
# 			"width":10
# 			},
# 			{
# 			"label":"Material Request",
# 			"fieldname":"material_request",
# 			"fieldtype":"Link",
# 			"options":"Material Request",
# 			"width":150
# 			},
# 			{
# 			"label":"MR Row",
# 			"fieldtype":"Int",
# 			"fieldname":"mr_row",
# 			"width":50
# 			},
# 			{
# 			"label":"Item Code",
# 			"fieldtype":"Link",
# 			"fieldname":"item_code",
# 			"options":"Item",
# 			"width":150
# 			},
# 			{
# 			"label":"Item Group",
# 			"fieldtype":"Data",
# 			"fieldname":"item_group",
# 			"width":150
# 			},
# 			{
# 			"label":"Description",
# 			"fieldname":"description",
# 			"fieldtype":"Data",
# 			"width":100
# 			},
# 			{
# 			"label":"Technical Description",
# 			"fieldname":"technical_description",
# 			"fieldtype":"Small Text",
# 			"width":100
# 			},
# 			{
# 			"label":"MR Qty",
# 			"fieldname":"mr_qty",
# 			"fieldtype":"Float",
# 			"width":100
# 			},
# 			{
# 			"label":"UOM",
# 			"fieldname":"uom",
# 			"fieldtype":"Data",
# 			"width":100
# 			}
# 		]
	
# 	return columns
# def get_data(data,filters):
# 	data=[]
# 	mr=[]
# 	mr_t=[]
# 	query=frappe.db.sql(" SELECT mri.parent,mri.name,mri.idx,mri.item_code,mri.mi_qty,mri.description,mri.technical_description,mri.qty,mri.uom,mri.freeze_qty FROM `tabMaterial Request`as mr,`tabMaterial Request Item`as mri where mr.name=mri.parent and mr.docstatus=1 and mr.project=%(project)s ORDER BY mr.name,mri.idx", filters, as_dict=1)
# 	for i in query:

# 		po=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"parent")
# 		po_workflow=frappe.db.get_value("Purchase Order",po,"workflow_state")
# 		po_name=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"name")
# 		poq=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"qty")
# 		uom=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"uom")
# 		idx=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"idx")
# 		po_amt=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"base_net_amount")
# 		po_rate=frappe.db.get_value("Purchase Order Item",{"material_request":i.parent,"material_request_item":i.name},"base_net_rate")


# 		pr=frappe.db.get_value("Purchase Receipt Item",{"purchase_order":po,"purchase_order_item":po_name},"parent")
# 		pr_name=frappe.db.get_value("Purchase Receipt Item",{"purchase_order":po,"purchase_order_item":po_name},"name")
# 		prq=frappe.db.get_value("Purchase Receipt Item",{"purchase_order":po,"purchase_order_item":po_name},"qty")
# 		pr_uom=frappe.db.get_value("Purchase Receipt Item",{"purchase_order":po,"purchase_order_item":po_name},"uom")
# 		pr_idx=frappe.db.get_value("Purchase Receipt Item",{"purchase_order":po,"purchase_order_item":po_name},"idx")
# 		if(pr==None or po==None):
# 			pr=pr_name=pr_uom=pr_idx="-"
# 			prq=0
# 		ar=[]
# 		for k in frappe.db.sql("SELECT aa.name FROM `tabMaterial Issue` as aa,`tabMaterial Issue Item`as bb WHERE aa.name=bb.parent and bb.material_request='"+str(i.parent)+"' and bb.material_request_item='"+str(i.name)+"' and aa.docstatus=1 ",as_dict=1):
# 			ar.append(k.name)
# 		mi_name=""
# 		for j in ar:
# 			if(mi_name==""):
# 				mi_name+=str(j)
# 			else:
# 				mi_name+=","+str(j)
# 		po_am = 0.0
# 		if(po_amt!=None  and frappe.db.get_value("Purchase Order",po,"workflow_state")=="Approved"):
# 			po_am=po_amt

# 		if(poq!=None and frappe.db.get_value("Purchase Order",po,"workflow_state")=="Approved"):
# 			if(prq!=None and poq<=prq):
# 				po_q='<p style="background-color:yellow">'+str(poq)+' - '+str(uom)+'</p>'
				
# 			else:
# 				po_q='<p>'+str(poq)+' - '+str(uom)+'</p>'
# 		else:
# 			po_q='<b>-</b>'
# 		if(poq==i.qty and frappe.db.get_value("Purchase Order",po,"workflow_state")=="Approved"):
# 			ht1='<p style="background-color:lightgreen">'+str(i.qty)+' - '+str(i.uom)+'</p>'
# 		else:
# 			ht1='<p>'+str(i.qty)+' - '+str(i.uom)+'</p>'


# 		if(filters.not_received!=None):
# 			if(po!=None and pr==None):
# 				if(i.parent not in mr):
# 					mr.append(i.parent)
# 					data.append({})
# 					data.append({
# 						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
# 						"material_request":i.parent,
# 						"fre_qty":i.freeze_qty,
# 						"item_code":i.item_code,
# 						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
# 						"description":i.description,
# 						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
# 						"mr_qty":ht1,
# 						"mi_qty":i.mi_qty,
# 						"mi_num":mi_name,
# 						"purchase_order":po,
# 						"po_workflow":po_workflow,
# 						"po_qty":po_q,
# 						"po_amt":po_am,
# 						"mr_row":i.idx,
# 						"po_row":idx,
# 						"purchase_receipt":"-",
# 						"pr_qty":"-"
# 						})
# 				else:
# 					data.append({
# 						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
# 						"material_request":i.parent,
# 						"fre_qty":i.freeze_qty,
# 						"item_code":i.item_code,
# 						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
# 						"description":i.description,
# 						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
# 						"mr_qty":ht1,
# 						"mi_qty":i.mi_qty,
# 						"mi_num":mi_name,
# 						"purchase_order":po,
# 						"po_workflow":po_workflow,
# 						"po_qty":po_q,
# 						"po_amt":po_am,
# 						"mr_row":i.idx,
# 						"po_row":idx,
# 						"purchase_receipt":"-",
# 						"pr_qty":"-"
# 						})

# 		elif(filters.unlinked==None):
# 			if(pr!=None):
# 				if(i.parent not in mr):
# 					mr.append(i.parent)
# 					dc_no = frappe.db.get_value('Delivery Note Item', {'material_request_item': i.name}, 'parent')
# 					dc_date = frappe.db.get_value('Delivery Note',dc_no, 'posting_date')
# 					dc_idx = frappe.db.get_value('Delivery Note Item', {'material_request_item': i.name}, 'idx')
# 					dc_qty = frappe.db.get_value('Delivery Note Item', {'material_request_item': i.name}, 'qty')
# 					dc_status = frappe.db.get_value('Delivery Note',dc_no, 'status')
# 					data.append({})
# 					data.append({
# 						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
# 						"material_request":i.parent,
# 						"fre_qty":i.freeze_qty,
# 						"item_code":i.item_code,
# 						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
# 						"description":i.description,
# 						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
# 						"mr_qty":ht1,
# 						"mi_qty":i.mi_qty,
# 						"mi_num":mi_name,
# 						"purchase_order":po,
# 						"po_workflow":po_workflow,
# 						"po_qty":po_q,
# 						"po_amt":po_am,
# 						"po_rate":po_rate,
# 						"mr_row":i.idx,
# 						"po_row":idx,
# 						"purchase_receipt":pr,
# 						"pr_qty":str(prq),
# 						"dc_no":dc_no,
# 						"dc_date":dc_date,
# 						"dc_row":dc_idx,
# 						"dc_qty":dc_qty,
# 						"dc_status":dc_status
# 						})
# 				else:
# 					data.append({
# 						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
# 						"material_request":i.parent,
# 						"fre_qty":i.freeze_qty,
# 						"item_code":i.item_code,
# 						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
# 						"description":i.description,
# 						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
# 						"mr_qty":ht1,
# 						"purchase_order":po,
# 						"po_workflow":po_workflow,
# 						"po_qty":po_q,
# 						"po_amt":po_am,
# 						"po_rate":po_rate,
# 						"mr_row":i.idx,
# 						"mi_qty":i.mi_qty,
# 						"mi_num":mi_name,
# 						"po_row":idx,
# 						"purchase_receipt":pr,
# 						"pr_qty":str(prq)

# 						})
# 			else:
# 				if(i.parent not in mr):
# 					mr.append(i.parent)
# 					data.append({})
# 					data.append({
# 						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
# 						"material_request":i.parent,
# 						"fre_qty":i.freeze_qty,
# 						"item_code":i.item_code,
# 						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
# 						"description":i.description,
# 						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
# 						"mr_qty":ht1,
# 						"purchase_order":po,
# 						"po_workflow":po_workflow,
# 						"po_qty":po_q,
# 						"po_amt":po_am,
# 						"po_rate":po_rate,
# 						"mr_row":i.idx,
# 						"mi_qty":i.mi_qty,
# 						"mi_num":mi_name,
# 						"po_row":idx,
# 						"purchase_receipt":"-",
# 						"pr_qty":"-"
# 						})
# 				else:
# 					data.append({
# 						"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
# 						"material_request":i.parent,
# 						"fre_qty":i.freeze_qty,
# 						"item_code":i.item_code,
# 						"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
# 						"description":i.description,
# 						"technical_description":i.technical_description if(i.technical_description!=None) else " ",
# 						"mr_qty":ht1,
# 						"purchase_order":po,
# 						"po_workflow":po_workflow,
# 						"po_qty":po_q,
# 						"po_amt":po_am,
# 						"po_rate":po_rate,
# 						"mr_row":i.idx,
# 						"mi_qty":i.mi_qty,
# 						"mi_num":mi_name,
# 						"po_row":idx,
# 						"purchase_receipt":"-",
# 						"pr_qty":"-"
# 						})
# 		else:
# 			if(po==None):
# 				if(filters.club==1):
# 					mr_t.append(i.name)
# 				else:
# 					if(i.parent not in mr):
# 						mr.append(str(i.parent))
# 						data.append({})
# 						data.append({
# 							"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
# 							"material_request":i.parent,
# 							"fre_qty":i.freeze_qty,
# 							"item_code":i.item_code,
# 							"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
# 							"description":i.description,
# 							"technical_description":i.technical_description if(i.technical_description!=None) else " ",
# 							"mr_qty":ht1,
# 							"mi_qty":i.mi_qty,
# 							"mi_num":mi_name,
# 							"purchase_order":po,
# 							"po_workflow":po_workflow,
# 							"po_qty":po_q,
# 							"po_amt":po_am,
# 							"mr_row":i.idx,
# 							"po_row":idx
# 							})
# 					else:
# 						data.append({
# 							"creator":frappe.db.get_value("User",str(frappe.db.sql("SELECT owner FROM `tabMaterial Request` WHERE name='"+str(i.parent)+"'",as_dict=1)[0]["owner"]),"full_name"),
# 							"material_request":i.parent,
# 							"fre_qty":i.freeze_qty,
# 							"item_code":i.item_code,
# 							"item_group":frappe.db.get_value("Item",i.item_code,"item_group"),
# 							"description":i.description,
# 							"technical_description":i.technical_description if(i.technical_description!=None) else " ",
# 							"mr_qty":ht1,
# 							"mi_qty":i.mi_qty,
# 							"mi_num":mi_name,
# 							"purchase_order":po,
# 							"po_workflow":po_workflow,
# 							"po_qty":po_q,
# 							"po_amt":po_am,
# 							"mr_row":i.idx,
# 							"po_row":idx
# 							})

# 	if(len(mr_t)>=1):
# 		tup = str(tuple(mr_t))
# 		qq = frappe.db.sql("""SELECT item_code, 
# 			GROUP_CONCAT(distinct(parent))as material_request,
# 			GROUP_CONCAT(idx)as mr_row, 
# 			item_group,description,technical_description,
# 			sum(qty)as mr_qty,uom 
# 			FROM `tabMaterial Request Item`
# 			WHERE name in """+tup+""" GROUP BY item_code
# 			""",as_dict=1)
# 		for i in qq:
# 			data.append(i)	
	
# 	return data

# # def get_conditions(filters):
# # 	conditions=''
# # 	if filters.get("project"):
# # 		conditions += " and mr.project = %(project)s"

# # 	match_conditions = build_match_conditions("Material Request")
# # 	if match_conditions:
# # 		conditions += " and %s" % match_conditions
# # 	return conditions


# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime,date


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
		"label": _("Item Code"),
		"fieldname": "item_code",
		"fieldtype": "Link",
		"options":"Item",
		"width": 150,
		"hidden":1
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
		"width": 150
		},
		{
		"label": _("MR Creation"),
		"fieldname": "mr_creation",
		"fieldtype": "Data",
		"width": 100
		},
		{
		"label": _("MR Row"),
		"fieldname": "mr_row",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("MR No"),
		"fieldname": "mr_no",
		"fieldtype": "Link",
		"options":"Material Request",
		"width": 120
		},
		{
		"label": _("MR Qty"),
		"fieldname": "mr_qty",
		"fieldtype": "Float",
		"width": 80
		},
		{
		"label": _("MR Status"),
		"fieldname": "mr_status",
		"fieldtype": "Data",
		"width": 120
		},
		{
		"label": _("Pending days"),
		"fieldname": "mr_pen",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("PO Row"),
		"fieldname": "po_row",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("PO No"),
		"fieldname": "po_no",
		"fieldtype": "Link",
		"options":"Purchase Order",
		"width": 120
		},
		{
		"label": _("PO Qty"),
		"fieldname": "po_qty",
		"fieldtype": "Float",
		"width": 80
		},
		{
		"label": _("PO Status"),
		"fieldname": "po_status",
		"fieldtype": "Data",
		"width": 120
		},
		{
		"label": _("PR Row"),
		"fieldname": "pr_row",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("PR No"),
		"fieldname": "pr_no",
		"fieldtype": "Data",
		"width": 120
		},
		{
		"label": _("PR Qty"),
		"fieldname": "pr_qty",
		"fieldtype": "Float",
		"width": 80
		},
		{
		"label": _("PR Status"),
		"fieldname": "pr_status",
		"fieldtype": "Data",
		"width": 120
		},
		{
		"label": _("DC Date"),
		"fieldname": "dc_date",
		"fieldtype": "Date",
		"width": 100
		},
		{
		"label": _("DC row"),
		"fieldname": "dc_row",
		"fieldtype": "Data",
		"width": 80
		},
		{
		"label": _("DC No"),
		"fieldname": "dc_no",
		"fieldtype": "Link",
		"width": 170,
		"options":"Delivery Note"
		},
		{
		"label": _("DC Qty"),
		"fieldname": "dc_qty",
		"fieldtype": "Float",
		"width": 80
		},
		{
		"label": _("DC Status"),
		"fieldname": "status",
		"fieldtype": "HTML",
		"width": 120
		}
	]

	return columns

def get_data(conditions,data, filters):
	data=[]
	for i in frappe.db.sql("""SELECT mr.transaction_date,mri.item_code,mri.description,mri.technical_description,mri.idx,mri.qty,mri.parent,mr.workflow_state,mri.name as "ref_na" FROM `tabMaterial Request Item` as mri INNER JOIN `tabMaterial Request` as mr ON mr.name=mri.parent WHERE mr.workflow_state!="Cancelled" and mr.workflow_state!="Rejected"{conditions}""".format(conditions=conditions), as_dict=1):
		poi_no = frappe.db.get_value('Purchase Order Item', {'material_request_item': i.ref_na}, 'parent')
		poi_status = frappe.db.get_value('Purchase Order',poi_no, 'workflow_state')
		po_n=''
		po_st=''
		poi_idx=''
		poi_qty=0
		if(poi_status != 'Cancelled' or poi_status != 'Rejected'):
			po_n=poi_no
			po_st=poi_status
			poi_idx = frappe.db.get_value('Purchase Order Item', {'material_request_item': i.ref_na}, 'idx')
			poi_qty = frappe.db.get_value('Purchase Order Item', {'material_request_item': i.ref_na}, 'qty')

		pri_no = frappe.db.get_value('Purchase Receipt Item', {'material_request_item': i.ref_na}, 'parent')
		pri_status = frappe.db.get_value('Purchase Receipt',pri_no, 'status')
		pri_idx = ''
		if(pri_status!='Cancelled'):
			pr_n = pri_no
			pr_st = pri_status	
			pri_idx = frappe.db.get_value('Purchase Receipt Item', {'material_request_item': i.ref_na}, 'idx')

		dc=frappe.db.sql("SELECT parent,idx,qty FROM `tabDelivery Note Item` WHERE docstatus=1 and material_request_item='"+str(i.ref_na)+"'",as_dict=1)

		pend = '-'
		if(i.workflow_state != 'Approved'):
			d1 = datetime.strptime(str(i.transaction_date), "%Y-%m-%d")
			d2 = datetime.strptime(str(date.today()), "%Y-%m-%d")
			delta = d2 - d1
			pend = delta.days

		if(dc):
			for q in dc:
				dc_date = frappe.db.get_value('Delivery Note', q.parent, 'posting_date')
				data.append({
				"item_code":i.item_code,
				"description":i.description,
				"technical_description":i.technical_description,
				"mr_creation":i.transaction_date,
				"mr_row":i.idx,
				"mr_qty":i.qty,
				"mr_no":i.parent,
				"mr_status":i.workflow_state,
				"mr_pen":pend,
				"po_row": poi_idx,
				"po_no": po_n,
				"po_qty":poi_qty,
				"po_status":po_st,
				"pr_row": pri_idx,
				"pr_no": pr_n,
				"pr_status":pr_st,
				"dc_date":dc_date,
				"dc_row":q.idx,
				"dc_no":q.parent,
				"dc_qty":q.qty,
				"status":"<b style='color:green'>Delivered</b>"
				})
		else:
			data.append({
			"item_code":i.item_code,
			"description":i.description,
			"technical_description":i.technical_description,
			"mr_creation":i.transaction_date,
			"mr_row":i.idx,
			"mr_qty":i.qty,
			"mr_no":i.parent,
			"mr_status":i.workflow_state,
			"mr_pen":pend,
			"po_row":poi_idx,
			"po_no":po_n,
			"po_qty":poi_qty,
			"po_status":po_st,
			"pr_row": pri_idx,
			"pr_no": pr_n,
			"pr_status":pr_st,
			"dc_date":"-",
			"dc_row":"-",
			"dc_no":"-",
			"dc_qty":"-",
			"status":"<b style='color:red'>Not Delivered</b>"
			})
	return data

def get_conditions(filters):
	conditions = ""

	if filters.get("project"):
		conditions += " AND mr.project='%s'" % filters.get('project')

	return conditions
