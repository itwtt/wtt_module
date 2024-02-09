# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import date,datetime,timedelta
import json
def execute(filters=None):
	data = []
	columns = get_colomns(filters)
	conditions = get_conditions(filters)
	data = get_data(conditions,data,filters)
	if(filters==None):
		columns=[]
		data=[]
	return columns, data


def get_colomns(filters):
	columns = [
	{
		"label":"Item Code",
		"fieldname":"item_code",
		"fieldtype":"Data",
		"width":100
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
		"fieldtype":"Data",
		"width":450
	},
	{
		"label":"Required Qty",
		"fieldtype":"Data",
		"fieldname":"req_qty",
		"width":100
	},
	{
		"label":" Received Qty",
		"fieldname":"qty",
		"fieldtype":"Data",
		"width":100
	},
	{
		"label":"UOM",
		"fieldname":"uom",
		"fieldtype":"Data",
		"width":100
	}]
	if(filters.track_boxes==1):
		columns.remove({
			"label":"Required Qty",
			"fieldtype":"Data",
			"fieldname":"req_qty",
			"width":100
		})
		columns.remove({
			"label":"Item Code",
			"fieldtype":"Data",
			"fieldname":"item_code",
			"width":100
		})
		columns.append({
			"label":"Date",
			"fieldtype":"Date",
			"fieldname":"shipment_date",
			"width":100
			})
		columns.append({
			"label":"Packing Slip",
			"fieldtype":"Link",
			"fieldname":"packing_slip",
			"options":"Packing Slip",
			"width":200
			})
		columns.append({
			"label":"Box No",
			"fieldtype":"Data",
			"fieldname":"box_no",
			"width":80
			})
	return columns

def get_data(conditions,data,filters):
	# frappe.msgprint(str(frappe.utils.now()))
	# frappe.msgprint(str(datetime.now()))

	data=[]
	ic=[]
	qq = []
	sys=filters.system
	get_items = frappe.db.sql("SELECT distinct(sti.item_code)as item_code,sum(sti.qty)as qty FROM `tabSystem Template`as st,`tabSystem Template Item`as sti WHERE st.name=sti.parent and st.system='"+str(sys)+"' GROUP BY item_code",filters,as_dict=1)
	for i in get_items:
		ic.append(i.item_code)
		qq.append({"item_code":i.item_code,"qty":i.qty})
 
	query = frappe.db.sql("""SELECT distinct(psi.item_code)as item_code,sum(psi.qty)as qty,psi.stock_uom as uom,psi.description,psi.technical_description
			from `tabPacking Slip` as ps,`tabPacking Slip Item`as psi where ps.name=psi.parent and ps.docstatus!=2
			{conditions} GROUP BY item_code
			""".format(conditions=conditions),as_dict=1)
	if (filters.track_boxes==1):
		query = frappe.db.sql("""SELECT distinct(psi.name)as name,psi.parent as packing_slip,ps.shipment_date,psi.box_no as box_no,psi.item_code,psi.qty,psi.stock_uom as uom,psi.description,psi.technical_description
			from `tabPacking Slip` as ps,`tabPacking Slip Item`as psi where ps.name=psi.parent and ps.docstatus!=2
			{conditions} GROUP BY item_code
			""".format(conditions=conditions),as_dict=1)
	for i in query:
		if(i.item_code in ic):
			if(filters.track_boxes==None):
				req_qty = sum([qt["qty"] if qt["item_code"] == i.item_code else 0 for qt in qq])
				html="<p style='background-color:tomato;color:black;'>"+str(i.qty)+"</p>"
				if(req_qty<=i.qty):
					html="<p style='background-color:lightgreen;color:black;'>"+str(i.qty)+"</p>"
				data.append({
					"item_code":i.item_code,
					"description":i.description,
					"technical_description":i.technical_description,
					"qty":html,
					"uom":i.uom,
					"req_qty":req_qty
					})
			else:
				data.append(i)
	# if(filters.track_boxes==1):
	# 	del data['req_qty']
	return data


def get_conditions(filters):
	conditions = ""
	if filters.get("project"):
		conditions += " AND ps.project='%s'" % filters.get('project')

	if filters.get("start_date"):
		conditions += " AND ps.shipment_date>='%s'" % filters.get('start_date')

	if filters.get("end_date"):
		conditions += " AND ps.shipment_date<='%s'" % filters.get('end_date')
	return conditions


@frappe.whitelist()
def get_details(datas):
	to_python = json.loads(datas)
	data = []
	for j in to_python:
		for i in frappe.db.sql("SELECT distinct(parent)as parent,idx,item_code,description,qty,stock_uom,box_no FROM `tabPacking Slip Item` WHERE item_code='"+str(j["item_code"])+"' ",as_dict=1):
			data.append(i)
	return data

