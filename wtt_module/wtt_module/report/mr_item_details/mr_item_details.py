from __future__ import unicode_literals
import frappe
from datetime import date
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import date,datetime,timedelta
import calendar

def execute(filters=None):
	if not filters:
		return [], []
	data = []
	columns = get_columns(filters)
	data = get_data(data,filters)
	return columns, data

def get_columns(filters):
	columns=[]
	#report1column
	if(filters.module=='Material Request'):
		if(filters.item==None and filters.item_code==None and filters.item_group==None):
			columns=[
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 150
				},
				{
					"label": _("ITEM GROUP"),
					"fieldtype": "Data",
					"fieldname": "item_group",
					"width": 150
				},
				{
					"label": _("TECHNICAL DESCRIPTION"),
					"fieldtype": "Data",
					"fieldname": "technical_description",
					"width": 350
				},
				{
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 150
				},
				{
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 150
				}
				]
		
		elif(filters.item_group!=None):
			columns=[
				{
					"label": _("MATERIAL REQUEST"),
					"fieldtype": "Link",
					"fieldname": "mr",
					"width": 150,
					"options":"Material Request"
				},
				{
					"label": _("ROW"),
					"fieldtype": "Data",
					"fieldname": "row",
					"width": 50
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 90
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 150
				},
				{
					"label": _("ITEM GROUP"),
					"fieldtype": "Data",
					"fieldname": "item_group",
					"width": 150
				},
				{
					"label": _("TECHNICAL DESCRIPTION"),
					"fieldtype": "Data",
					"fieldname": "technical_description",
					"width": 350
				},
				{
					"label": _("REMARKS"),
					"fieldtype": "Data",
					"fieldname": "remarks",
					"width": 180
				},
				{
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 150
				},
				{
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 150
				}
				]


		elif(filters.mr_name==None and filters.item!=None):
			columns=[
				{
					"label": _("MATERIAL REQUEST"),
					"fieldtype": "Link",
					"fieldname": "mr",
					"width": 150,
					"options":"Material Request"
				},
				{
					"label": _("ROW"),
					"fieldtype": "Data",
					"fieldname": "row",
					"width": 80
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				{
					"label": _("STATUS"),
					"fieldtype": "Data",
					"fieldname": "status",
					"width": 100
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 100
				},
				{
					"label": _("ITEM GROUP"),
					"fieldtype": "Data",
					"fieldname": "item_group",
					"width": 150
				}
				]
			ref=frappe.get_doc("Item",filters.item)
			for i in ref.attributes:
				columns.append({
					"fieldname": frappe.scrub(i.attribute),
					"label": i.attribute,
					"fieldtype":"Data",
					"width":100
					})
			columns.append({
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 100
				})
			columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 100
				})
		elif(filters.mr_name==None and filters.item_code!=None):
			columns=[
				{
					"label": _("MATERIAL REQUEST"),
					"fieldtype": "Link",
					"fieldname": "mr",
					"width": 150,
					"options":"Material Request"
				},
				{
					"label": _("ROW"),
					"fieldtype": "Data",
					"fieldname": "row",
					"width": 80
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				{
					"label": _("STATUS"),
					"fieldtype": "Data",
					"fieldname": "status",
					"width": 100
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 100
				},
				{
					"label": _("ITEM GROUP"),
					"fieldtype": "Data",
					"fieldname": "item_group",
					"width": 150
				}
				]
			ref2=frappe.db.get_value("Item",filters.item_code,"variant_of")
			ref=frappe.get_doc("Item",ref2)
			for i in ref.attributes:
				columns.append({
					"fieldname": frappe.scrub(i.attribute),
					"label": i.attribute,
					"fieldtype":"Data",
					"width":100
					})
			columns.append({
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 100
				})
			columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 100
				})
			
				
		elif(filters.mr_name!=None):
			if(filters.item!=None):
				columns=[
					{
						"label": _("ITEM CODE"),
						"fieldtype": "Data",
						"fieldname": "item_code",
						"width": 150
					},
					{
						"label": _("ITEM NAME"),
						"fieldtype": "Data",
						"fieldname": "item_name",
						"width": 150
					},
					{
					"label": _("ITEM GROUP"),
					"fieldtype": "Data",
					"fieldname": "item_group",
					"width": 150
					},
					{
						"label": _("PROJECT"),
						"fieldtype": "Data",
						"fieldname": "project",
						"width": 100
					},
					
					]
				ref=frappe.get_doc("Item",filters.item)
				for i in ref.attributes:
					columns.append({
						"fieldname": frappe.scrub(i.attribute),
						"label": i.attribute,
						"fieldtype":"Data",
						"width":100
						})
				columns.append({
					"label": _("QUANTITY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 150
					})
				columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 150
					})
			elif(filters.item_code!=None):
				columns=[
					{
						"label": _("ITEM CODE"),
						"fieldtype": "Data",
						"fieldname": "item_code",
						"width": 150
					},
					{
						"label": _("ITEM NAME"),
						"fieldtype": "Data",
						"fieldname": "item_name",
						"width": 150
					},
					{
					"label": _("ITEM GROUP"),
					"fieldtype": "Data",
					"fieldname": "item_group",
					"width": 150
					},
					{
						"label": _("PROJECT"),
						"fieldtype": "Data",
						"fieldname": "project",
						"width": 100
					},
					]
				ref2=frappe.db.get_value("Item",filters.item_code,"variant_of")
				ref=frappe.get_doc("Item",ref2)
				for i in ref.attributes:
					columns.append({
						# "label":i.attribute,
						# "fieldname":"field"+str(i.idx),
						"fieldname": frappe.scrub(i.attribute),
						"label": i.attribute,
						"fieldtype":"Data",
						"width":100
						})
				columns.append({
					"label": _("QUANTITY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 150
					})
				columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 150
					})

		elif(filters.item_code!=None):
			columns=[
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 150
				},
				{
					"label": _("ITEM GROUP"),
					"fieldtype": "Data",
					"fieldname": "item_group",
					"width": 150
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				
				]
			ref2=frappe.db.get_value("Item",filters.item_code,"variant_of")
			ref=frappe.get_doc("Item",ref2)
			for i in ref.attributes:
				columns.append({
					"fieldname": frappe.scrub(i.attribute),
					"label": i.attribute,
					"fieldtype":"Data",
					"width":100
					})
			columns.append({
				"label": _("QUANTITY"),
				"fieldtype": "Data",
				"fieldname": "qty",
				"width": 150
				})
			columns.append({
				"label": _("UOM"),
				"fieldtype": "Data",
				"fieldname": "uom",
				"width": 150
				})



	#report2column
	elif(filters.module=='Purchase Order'):
		if(filters.item_group!=None):
			columns=[
				{
					"label": _("Purchase Order"),
					"fieldtype": "Link",
					"fieldname": "po",
					"width": 150,
					"options":"Purchase Order"
				},
				{
					"label": _("ROW"),
					"fieldtype": "Data",
					"fieldname": "po_row",
					"width": 50
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 90
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 150
				},
				{
					"label": _("TECHNICAL DESCRIPTION"),
					"fieldtype": "Data",
					"fieldname": "technical_description",
					"width": 350
				},
				{
					"label": _("PO QTY"),
					"fieldtype": "Data",
					"fieldname": "po_qty",
					"width": 150
				},
				{
					"label": _("MR QTY"),
					"fieldtype": "Data",
					"fieldname": "mr_qty",
					"width": 150
				},
				{
					"label": _("MATERIAL REQUEST"),
					"fieldtype": "Link",
					"fieldname": "mr",
					"width": 150,
					"options":"Material Request"
				},
				{
					"label": _("ROW"),
					"fieldtype": "Data",
					"fieldname": "mr_row",
					"width": 50
				}
				]
		elif(filters.item==None and filters.item_code==None):
			columns=[
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 150
				},
				{
					"label": _("TECHNICAL DESCRIPTION"),
					"fieldtype": "Data",
					"fieldname": "technical_description",
					"width": 350
				},
				{
					"label": _("RATE"),
					"fieldtype": "Data",
					"fieldname": "po_rate",
					"width": 150
				},
				{
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 150
				},
				{
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 150
				}
				]
		
		elif(filters.mr_name==None and filters.item!=None):
			columns=[
				{
					"label": _("Purchase Order"),
					"fieldtype": "Link",
					"fieldname": "mr",
					"width": 150,
					"options":"Purchase Order"
				},
				{
					"label": _("ROW"),
					"fieldtype": "Data",
					"fieldname": "row",
					"width": 80
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				{
					"label": _("STATUS"),
					"fieldtype": "Data",
					"fieldname": "status",
					"width": 100
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 100
				},{
					"label": _("RATE"),
					"fieldtype": "Data",
					"fieldname": "po_rate",
					"width": 100
				}
				]
			ref=frappe.get_doc("Item",filters.item)
			for i in ref.attributes:
				columns.append({
					# "label":i.attribute,
					# "fieldname":"field"+str(i.idx),
					"fieldname": frappe.scrub(i.attribute),
					"label": i.attribute,
					"fieldtype":"Data",
					"width":100
					})
			columns.append({
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 100
				})
			columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 100
				})
		elif(filters.mr_name==None and filters.item_code!=None):
			columns=[
				{
					"label": _("PURCHASE ORDER"),
					"fieldtype": "Link",
					"fieldname": "mr",
					"width": 150,
					"options":"Purchase Order"
				},
				{
					"label": _("ROW"),
					"fieldtype": "Data",
					"fieldname": "row",
					"width": 80
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				{
					"label": _("STATUS"),
					"fieldtype": "Data",
					"fieldname": "status",
					"width": 100
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 100
				}
				]
			ref2=frappe.db.get_value("Item",filters.item_code,"variant_of")
			ref=frappe.get_doc("Item",ref2)
			for i in ref.attributes:
				columns.append({
					# "label":i.attribute,
					# "fieldname":"field"+str(i.idx),
					"fieldname": frappe.scrub(i.attribute),
					"label": i.attribute,
					"fieldtype":"Data",
					"width":100
					})
			columns.append({
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 100
				})
			columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 100
				})
			
				
		elif(filters.mr_name!=None):
			if(filters.item!=None):
				columns=[
					{
						"label": _("ITEM CODE"),
						"fieldtype": "Data",
						"fieldname": "item_code",
						"width": 150
					},
					{
						"label": _("ITEM NAME"),
						"fieldtype": "Data",
						"fieldname": "item_name",
						"width": 150
					},
					{
						"label": _("PROJECT"),
						"fieldtype": "Data",
						"fieldname": "project",
						"width": 100
					},
					
					]
				ref=frappe.get_doc("Item",filters.item)
				for i in ref.attributes:
					columns.append({
						# "label":i.attribute,
						# "fieldname":"field"+str(i.idx),
						"fieldname": frappe.scrub(i.attribute),
						"label": i.attribute,
						"fieldtype":"Data",
						"width":100
						})
				columns.append({
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 150
					})
				columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 150
					})
			elif(filters.item_code!=None):
				columns=[
					{
						"label": _("ITEM CODE"),
						"fieldtype": "Data",
						"fieldname": "item_code",
						"width": 150
					},
					{
						"label": _("ITEM NAME"),
						"fieldtype": "Data",
						"fieldname": "item_name",
						"width": 150
					},
					{
						"label": _("PROJECT"),
						"fieldtype": "Data",
						"fieldname": "project",
						"width": 100
					},
					
					]
				ref2=frappe.db.get_value("Item",filters.item_code,"variant_of")
				ref=frappe.get_doc("Item",ref2)
				for i in ref.attributes:
					columns.append({
						# "label":i.attribute,
						# "fieldname":"field"+str(i.idx),
						"fieldname": frappe.scrub(i.attribute),
						"label": i.attribute,
						"fieldtype":"Data",
						"width":100
						})
				columns.append({
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 150
					})
				columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 150
					})
		elif(filters.item_code!=None):
			columns=[
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 150
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				
				]
			ref2=frappe.db.get_value("Item",filters.item_code,"variant_of")
			ref=frappe.get_doc("Item",ref2)
			for i in ref.attributes:
				columns.append({
					# "label":i.attribute,
					# "fieldname":"field"+str(i.idx),
					"fieldname": frappe.scrub(i.attribute),
					"label": i.attribute,
					"fieldtype":"Data",
					"width":100
					})
			columns.append({
				"label": _("QTY"),
				"fieldtype": "Data",
				"fieldname": "qty",
				"width": 150
				})
			columns.append({
				"label": _("UOM"),
				"fieldtype": "Data",
				"fieldname": "uom",
				"width": 150
				})


	#REPORT3COLUMN
	elif(filters.module=='Purchase Receipt'):
		if(filters.item==None and filters.item_code==None):
			columns=[
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 150
				},
				{
					"label": _("TECHNICAL DESCRIPTION"),
					"fieldtype": "Data",
					"fieldname": "technical_description",
					"width": 350
				},
				{
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 150
				},
				{
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 150
				}
				]
		
		elif(filters.mr_name==None and filters.item!=None):
			columns=[
				{
					"label": _("Purchase Receipt"),
					"fieldtype": "Link",
					"fieldname": "mr",
					"width": 150,
					"options":"Purchase Receipt"
				},
				{
					"label": _("ROW"),
					"fieldtype": "Data",
					"fieldname": "row",
					"width": 80
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				{
					"label": _("STATUS"),
					"fieldtype": "Data",
					"fieldname": "status",
					"width": 100
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 100
				}
				]
			ref=frappe.get_doc("Item",filters.item)
			for i in ref.attributes:
				columns.append({
					# "label":i.attribute,
					# "fieldname":"field"+str(i.idx),
					"fieldname": frappe.scrub(i.attribute),
					"label": i.attribute,
					"fieldtype":"Data",
					"width":100
					})
			columns.append({
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 100
				})
			columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 100
				})
		elif(filters.mr_name==None and filters.item_code!=None):
			columns=[
				{
					"label": _("PURCHASE RECEIPT"),
					"fieldtype": "Link",
					"fieldname": "mr",
					"width": 150,
					"options":"Purchase Receipt"
				},
				{
					"label": _("ROW"),
					"fieldtype": "Data",
					"fieldname": "row",
					"width": 80
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				{
					"label": _("STATUS"),
					"fieldtype": "Data",
					"fieldname": "status",
					"width": 100
				},
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 100
				}
				]
			ref2=frappe.db.get_value("Item",filters.item_code,"variant_of")
			ref=frappe.get_doc("Item",ref2)
			for i in ref.attributes:
				columns.append({
					# "label":i.attribute,
					# "fieldname":"field"+str(i.idx),
					"fieldname": frappe.scrub(i.attribute),
					"label": i.attribute,
					"fieldtype":"Data",
					"width":100
					})
			columns.append({
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 100
				})
			columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 100
				})
			
				
		elif(filters.mr_name!=None):
			if(filters.item!=None):
				columns=[
					{
						"label": _("ITEM CODE"),
						"fieldtype": "Data",
						"fieldname": "item_code",
						"width": 150
					},
					{
						"label": _("ITEM NAME"),
						"fieldtype": "Data",
						"fieldname": "item_name",
						"width": 150
					},
					{
						"label": _("PROJECT"),
						"fieldtype": "Data",
						"fieldname": "project",
						"width": 100
					},
					
					]
				ref=frappe.get_doc("Item",filters.item)
				for i in ref.attributes:
					columns.append({
						# "label":i.attribute,
						# "fieldname":"field"+str(i.idx),
						"fieldname": frappe.scrub(i.attribute),
						"label": i.attribute,
						"fieldtype":"Data",
						"width":100
						})
				columns.append({
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 150
					})
				columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 100
				})
			elif(filters.item_code!=None):
				columns=[
					{
						"label": _("ITEM CODE"),
						"fieldtype": "Data",
						"fieldname": "item_code",
						"width": 150
					},
					{
						"label": _("ITEM NAME"),
						"fieldtype": "Data",
						"fieldname": "item_name",
						"width": 150
					},
					{
						"label": _("PROJECT"),
						"fieldtype": "Data",
						"fieldname": "project",
						"width": 100
					},
					
					]
				ref2=frappe.db.get_value("Item",filters.item_code,"variant_of")
				ref=frappe.get_doc("Item",ref2)
				for i in ref.attributes:
					columns.append({
						# "label":i.attribute,
						# "fieldname":"field"+str(i.idx),
						"fieldname": frappe.scrub(i.attribute),
						"label": i.attribute,
						"fieldtype":"Data",
						"width":100
						})
				columns.append({
					"label": _("QTY"),
					"fieldtype": "Data",
					"fieldname": "qty",
					"width": 150
					})
				columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 100
				})
		elif(filters.item_code!=None):
			columns=[
				{
					"label": _("ITEM CODE"),
					"fieldtype": "Data",
					"fieldname": "item_code",
					"width": 150
				},
				{
					"label": _("ITEM NAME"),
					"fieldtype": "Data",
					"fieldname": "item_name",
					"width": 150
				},
				{
					"label": _("PROJECT"),
					"fieldtype": "Data",
					"fieldname": "project",
					"width": 100
				},
				
				]
			ref2=frappe.db.get_value("Item",filters.item_code,"variant_of")
			ref=frappe.get_doc("Item",ref2)
			for i in ref.attributes:
				columns.append({
					# "label":i.attribute,
					# "fieldname":"field"+str(i.idx),
					"fieldname": frappe.scrub(i.attribute),
					"label": i.attribute,
					"fieldtype":"Data",
					"width":100
					})
			columns.append({
				"label": _("QTY"),
				"fieldtype": "Data",
				"fieldname": "qty",
				"width": 150
				})
			columns.append({
					"label": _("UOM"),
					"fieldtype": "Data",
					"fieldname": "uom",
					"width": 100
				})

		
	return columns

def get_data(data, filters):
	#report1
	if(filters.module=="Material Request"):
		if(filters.item_group!=None):
			if(filters.total!=1):
				dict1=[]
				data=[]
				ar=[]
				query=frappe.db.sql("SELECT mri.remarks,mr.name,mri.item_code,mri.idx,mri.project,mri.item_group,mri.description,mri.technical_description,mri.qty,mri.uom from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mri.item_group=%(item_group)s and mr.docstatus!=2 and mr.workflow_state!='Rejected' ORDER BY mr.name",filters,as_dict=1)
				if(filters.mr_name!=None):
					query=frappe.db.sql("SELECT mri.remarks,mr.name,mri.item_code,mri.idx,mri.project,mri.item_group,mri.description,mri.technical_description,mri.qty,mri.uom from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mr.name=%(mr_name)s and mri.item_group=%(item_group)s and mr.docstatus!=2 and mr.workflow_state!='Rejected' and mr.name=%(mr_name)s ORDER BY mri.idx",filters,as_dict=1)

				for det in query:
					data.append({
						"mr":det.name,
						"row":det.idx,
						"project":det.project,
						"item_code":det.item_code,
						"item_name":det.description,
						"item_group":det.item_group,
						"technical_description":det.technical_description,
						"remarks":det.remarks,
						"qty":str(det.qty),
						"uom":str(det.uom)
						})
			else:
				dict1=[]
				data=[]
				ar=[]
				query=frappe.db.sql("SELECT GROUP_CONCAT(DISTINCT(mr.name))as name,mri.item_code,GROUP_CONCAT(DISTINCT(mri.idx))as idx,mri.project,mri.item_group,mri.description,mri.technical_description,sum(mri.qty)as qty,mri.uom from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mri.item_group=%(item_group)s and mr.docstatus!=2 and mr.workflow_state!='Rejected' GROUP BY mri.item_code,mri.project",filters,as_dict=1)
				if(filters.mr_name!=None):
					query=frappe.db.sql("SELECT GROUP_CONCAT(DISTINCT(mr.name))as name,mri.item_code,GROUP_CONCAT(DISTINCT(mri.idx))as idx,mri.project,mri.item_group,mri.description,mri.technical_description,sum(mri.qty)as qty,mri.uom from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mr.name=%(mr_name)s and mri.item_group=%(item_group)s and mr.docstatus!=2 and mr.workflow_state!='Rejected' and mr.name=%(mr_name)s GROUP BY mri.item_code,mri.project ",filters,as_dict=1)

				for det in query:
					data.append({
						"mr":det.name,
						"row":det.idx,
						"project":det.project,
						"item_code":det.item_code,
						"item_name":det.description,
						"item_group":det.item_group,
						"technical_description":det.technical_description,
						"qty":str(det.qty),
						"uom":str(det.uom)
						})
		elif(filters.mr_name==None):
			# frappe.msgprint("oops! I can't get any MR")
			if(filters.item_code==None):
				item_dicts = []
				data=[]
				dict1=[]
				gug=[]

				variant_results = frappe.db.get_all(
					"Item",
					fields=["name"],
					filters={
						"variant_of": filters.item,
						"disabled": 0
					}
				)

				if not variant_results:
					#frappe.msgprint(_("There aren't any item variants for the selected item"))
					return []
				else:
					variant_list = [variant['name'] for variant in variant_results]
				for itemcode in variant_list:
					query1 = frappe.db.sql("SELECT DISTINCT(mr.name) from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mri.parent=mr.name and mri.item_code='"+str(itemcode)+"' and mr.workflow_state!='Cancelled' and mr.workflow_state!='Rejected'",as_dict=1)
					for i in query1:
						gug.append(i.name)
					if(filters.total==1):
						query=frappe.db.sql("SELECT GROUP_CONCAT(DISTINCT(mr.name))as parent,mri.project,mri.idx,mri.item_code,mri.item_group,mri.technical_description,sum(mri.qty)as qty,mri.uom,mri.description,mri.item_name from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mri.item_code='"+str(itemcode)+"' GROUP BY mri.item_code,mri.project",filters,as_dict=1)
						for det in query:
							hint=frappe.db.get_value("Item",det.item_code,"variant_of")
							if(hint==filters.item):
								ic=det.item_code
								attr_val_map = get_attribute_values_map(ic)
								attributes = frappe.db.get_all(
									"Item Variant Attribute",
									fields=["attribute"],
									filters={
										"parent": ic
									},
									group_by="attribute"
								)
								attribute_list = [row.get("attribute") for row in attributes]
								dict1.append({"item_code":det.item_code,"item_group":det.item_group,"mr":det.parent,"project":det.project,"status":det.workflow_state,"item_name":det.description,"qty":str(det.qty),"uom":str(det.uom),"row":str(det.idx)})
								for attribute in attribute_list:
									for item_dict in dict1:
										name = item_dict.get("item_code")
										attr_dict = attr_val_map.get(name)
										if attr_dict and attr_dict.get(attribute):
											item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
								data.append(item_dict)
				vis=set(gug)


				if(filters.total!=1):
					for i in vis:
						query=frappe.db.sql("SELECT * from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mr.name='"+str(i)+"' ",filters,as_dict=1)
						for det in query:
							hint=frappe.db.get_value("Item",det.item_code,"variant_of")
							if(hint==filters.item):
								ic=det.item_code
								attr_val_map = get_attribute_values_map(ic)
								attributes = frappe.db.get_all(
									"Item Variant Attribute",
									fields=["attribute"],
									filters={
										"parent": ic
									},
									group_by="attribute"
								)
								attribute_list = [row.get("attribute") for row in attributes]
								dict1.append({"item_code":det.item_code,"item_group":det.item_group,"mr":det.parent,"project":det.project,"status":det.workflow_state,"item_name":det.description,"qty":str(det.qty),"uom":str(det.uom),"row":str(det.idx)})
								for attribute in attribute_list:
									for item_dict in dict1:
										name = item_dict.get("item_code")
										attr_dict = attr_val_map.get(name)
										if attr_dict and attr_dict.get(attribute):
											item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
								data.append(item_dict)

			elif(filters.item==None):
				item_dicts = []
				data=[]
				dict1=[]
				gug=[]
				query1 = frappe.db.sql("SELECT DISTINCT(mr.name) from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mri.parent=mr.name and mr.workflow_state!='Cancelled' and mr.workflow_state!='Rejected' and mri.item_code=%(item_code)s ",filters,as_dict=1)
				
				for i in query1:
					gug.append(i.name)
				vis=set(gug)
				for i in vis:
					query=frappe.db.sql("SELECT * from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mr.name='"+str(i)+"' and mri.item_code=%(item_code)s ",filters,as_dict=1)
					for det in query:
						ic=det.item_code
						attr_val_map = get_attribute_values_map(ic)
						attributes = frappe.db.get_all(
							"Item Variant Attribute",
							fields=["attribute"],
							filters={
								"parent": ic
							},
							group_by="attribute"
						)
						attribute_list = [row.get("attribute") for row in attributes]
						dict1.append({"item_code":det.item_code,"item_group":det.item_group,"mr":det.parent,"project":det.project,"status":det.workflow_state,"item_name":det.description,"qty":str(det.qty),"uom":str(det.uom),"row":str(det.idx)})
						for attribute in attribute_list:
							for item_dict in dict1:
								name = item_dict.get("item_code")
								attr_dict = attr_val_map.get(name)
								if attr_dict and attr_dict.get(attribute):
									item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
						data.append(item_dict)	

		else:
			data=[]
			ar=[]
			dict1=[]
			if(filters.item_code!=None and filters.mr_name!=None):
				query=frappe.db.sql("SELECT * from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mr.name=%(mr_name)s and mri.item_code=%(item_code)s ",filters,as_dict=1)
				for det in query:
					ic=det.item_code
					attr_val_map = get_attribute_values_map(ic)
					attributes = frappe.db.get_all(
						"Item Variant Attribute",
						fields=["attribute"],
						filters={
							"parent": ic
						},
						group_by="attribute"
					)
					attribute_list = [row.get("attribute") for row in attributes]
					dict1.append({"variant_name":det.item_code})
					for item_dict in dict1:
						name = item_dict.get("variant_name")
						for attribute in attribute_list:
							attr_dict = attr_val_map.get(name)
							if attr_dict and attr_dict.get(attribute):
								item_dict["item_code"]=det.item_code
								item_dict["item_name"]=det.description
								item_dict["item_group"]=det.item_group
								item_dict["project"]=det.project
								item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
								item_dict["qty"]=str(det.qty)
								item_dict["uom"]=str(det.uom)
					data.append(item_dict)

			else:
				query=frappe.db.sql("SELECT * from `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mr.name=%(mr_name)s ",filters,as_dict=1)
				if(filters.item!=None):
					for det in query:
						hint=frappe.db.get_value("Item",det.item_code,"variant_of")
						if(hint==filters.item and det.parent==filters.mr_name):
							ic=det.item_code
							attr_val_map = get_attribute_values_map(ic)
							attributes = frappe.db.get_all(
								"Item Variant Attribute",
								fields=["attribute"],
								filters={
									"parent": ic
								},
								group_by="attribute"
							)
							attribute_list = [row.get("attribute") for row in attributes]
							dict1.append({"variant_name":det.item_code})
							for item_dict in dict1:
								name = item_dict.get("variant_name")
								for attribute in attribute_list:
									attr_dict = attr_val_map.get(name)
									if attr_dict and attr_dict.get(attribute):
										item_dict["item_code"]=det.item_code
										item_dict["item_name"]=det.description
										item_dict["item_group"]=det.item_group
										item_dict["project"]=det.project
										item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
										item_dict["qty"]=str(det.qty)
										item_dict["uom"]=str(det.uom)
							data.append(item_dict)

					

				else:
					for det in query:
						data.append({
							"item_code":det.item_code,
							"item_name":det.description,
							"item_group":det.item_group,
							"technical_description":det.technical_description,
							"project":det.project,
							"qty":str(det.qty),
							"uom":str(det.uom)
							})



	#report2
	elif(filters.module=='Purchase Order'):
		if(filters.item_group!=None):
			data=[]
			query = frappe.db.sql("SELECT * FROM `tabPurchase Order`as po,`tabPurchase Order Item`as poi WHERE poi.parent=po.name and poi.item_group=%(item_group)s and po.docstatus!=2 and po.workflow_state!='Rejected' ORDER BY po.name",filters,as_dict=1)
			if(filters.mr_name!=None):
				query = frappe.db.sql("SELECT * FROM `tabPurchase Order`as po,`tabPurchase Order Item`as poi WHERE poi.parent=po.name and poi.item_group=%(item_group)s and po.docstatus!=2 and po.workflow_state!='Rejected' and po.name=%(mr_name)s ORDER BY poi.idx",filters,as_dict=1)
			for i in query:
				
				mr_row="-"
				mr_qty="-"
				if(i.material_request_item!=None):
					mr_row=frappe.db.get_value("Material Request Item",i.material_request_item,"idx")
					mr_qty=str(frappe.db.get_value("Material Request Item",i.material_request_item,"qty"))+" - "+str(frappe.db.get_value("Material Request Item",i.material_request_item,"uom"))
				data.append({
					"item_code":i.item_code,
					"item_name":i.description,
					"project":i.project,
					"technical_description":i.technical_description,
					"po_qty":str(i.qty)+" - "+str(i.uom),
					"po":i.parent,
					"po_row":i.idx,
					"mr":i.material_request,
					"mr_row":mr_row,
					"mr_qty":mr_qty
					})



		elif(filters.mr_name==None):
			# frappe.msgprint("oops! I can't get any MR")
			if(filters.item_code==None):
				item_dicts = []
				data=[]
				dict1=[]
				gug=[]

				variant_results = frappe.db.get_all(
					"Item",
					fields=["name"],
					filters={
						"variant_of": filters.item,
						"disabled": 0
					}
				)

				if not variant_results:
					#frappe.msgprint(_("There aren't any item variants for the selected item"))
					return []
				else:
					variant_list = [variant['name'] for variant in variant_results]
				for itemcode in variant_list:
					query1 = frappe.db.sql("SELECT DISTINCT(mr.name) from `tabPurchase Order`as mr,`tabPurchase Order Item`as mri WHERE mri.parent=mr.name and mri.item_code='"+str(itemcode)+"' and mr.workflow_state!='Cancelled' and mr.workflow_state!='Rejected'",as_dict=1)
					
					for i in query1:
						gug.append(i.name)
				vis=set(gug)
				for i in vis:
					query=frappe.db.sql("SELECT * from `tabPurchase Order`as mr,`tabPurchase Order Item`as mri WHERE mr.name=mri.parent and mr.name='"+str(i)+"' ",filters,as_dict=1)
					for det in query:
						hint=frappe.db.get_value("Item",det.item_code,"variant_of")
						if(hint==filters.item):
							ic=det.item_code
							attr_val_map = get_attribute_values_map(ic)
							attributes = frappe.db.get_all(
								"Item Variant Attribute",
								fields=["attribute"],
								filters={
									"parent": ic
								},
								group_by="attribute"
							)
							attribute_list = [row.get("attribute") for row in attributes]
							dict1.append({"item_code":det.item_code,"mr":det.parent,"project":det.project,"status":det.workflow_state,"item_name":det.description,"po_rate":str(det.rate),"qty":str(det.qty),"uom":str(det.uom),"row":str(det.idx)})
							for attribute in attribute_list:
								for item_dict in dict1:
									name = item_dict.get("item_code")
									attr_dict = attr_val_map.get(name)
									if attr_dict and attr_dict.get(attribute):
										item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
							
							data.append(item_dict)

			elif(filters.item==None):
				item_dicts = []
				data=[]
				dict1=[]
				gug=[]
				query1 = frappe.db.sql("SELECT DISTINCT(mr.name) from `tabPurchase Order`as mr,`tabPurchase Order Item`as mri WHERE mri.parent=mr.name and mr.workflow_state!='Cancelled' and mr.workflow_state!='Rejected' and mri.item_code=%(item_code)s ",filters,as_dict=1)
				
				for i in query1:
					gug.append(i.name)
				vis=set(gug)
				for i in vis:
					query=frappe.db.sql("SELECT * from `tabPurchase Order`as mr,`tabPurchase Order Item`as mri WHERE mr.name=mri.parent and mr.name='"+str(i)+"' and mri.item_code=%(item_code)s ",filters,as_dict=1)
					for det in query:
						ic=det.item_code
						attr_val_map = get_attribute_values_map(ic)
						attributes = frappe.db.get_all(
							"Item Variant Attribute",
							fields=["attribute"],
							filters={
								"parent": ic
							},
							group_by="attribute"
						)
						attribute_list = [row.get("attribute") for row in attributes]
						dict1.append({"item_code":det.item_code,"mr":det.parent,"project":det.project,"status":det.workflow_state,"item_name":det.description,"qty":str(det.qty),"uom":str(det.uom),"row":str(det.idx)})
						for attribute in attribute_list:
							for item_dict in dict1:
								name = item_dict.get("item_code")
								attr_dict = attr_val_map.get(name)
								if attr_dict and attr_dict.get(attribute):
									item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
						
						data.append(item_dict)	

		else:
			data=[]
			ar=[]
			dict1=[]
			if(filters.item_code!=None and filters.mr_name!=None):
				query=frappe.db.sql("SELECT * from `tabPurchase Order`as mr,`tabPurchase Order Item`as mri WHERE mr.name=mri.parent and mr.name=%(mr_name)s and mri.item_code=%(item_code)s ",filters,as_dict=1)
				for det in query:
					ic=det.item_code
					attr_val_map = get_attribute_values_map(ic)
					attributes = frappe.db.get_all(
						"Item Variant Attribute",
						fields=["attribute"],
						filters={
							"parent": ic
						},
						group_by="attribute"
					)
					attribute_list = [row.get("attribute") for row in attributes]
					dict1.append({"variant_name":det.item_code})
					for item_dict in dict1:
						name = item_dict.get("variant_name")
						for attribute in attribute_list:
							attr_dict = attr_val_map.get(name)
							if attr_dict and attr_dict.get(attribute):
								item_dict["item_code"]=det.item_code
								item_dict["item_name"]=det.description
								item_dict["project"]=det.project
								item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
								item_dict["qty"]=str(det.qty)
								item_dict["uom"]=str(det.uom)
					data.append(item_dict)

			else:
				query=frappe.db.sql("SELECT * from `tabPurchase Order`as mr,`tabPurchase Order Item`as mri WHERE mr.name=mri.parent and mr.name=%(mr_name)s ",filters,as_dict=1)
				if(filters.item!=None):
					for det in query:
						hint=frappe.db.get_value("Item",det.item_code,"variant_of")
						if(hint==filters.item and det.parent==filters.mr_name):
							ic=det.item_code
							attr_val_map = get_attribute_values_map(ic)
							attributes = frappe.db.get_all(
								"Item Variant Attribute",
								fields=["attribute"],
								filters={
									"parent": ic
								},
								group_by="attribute"
							)
							attribute_list = [row.get("attribute") for row in attributes]
							dict1.append({"variant_name":det.item_code})
							for item_dict in dict1:
								name = item_dict.get("variant_name")
								for attribute in attribute_list:
									attr_dict = attr_val_map.get(name)
									if attr_dict and attr_dict.get(attribute):
										item_dict["item_code"]=det.item_code
										item_dict["item_name"]=det.description
										item_dict["project"]=det.project
										item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
										item_dict["qty"]=str(det.qty)
										item_dict["uom"]=str(det.uom)
							data.append(item_dict)

					

				else:
					for det in query:
						data.append({
							"item_code":det.item_code,
							"item_name":det.description,
							"technical_description":det.technical_description,
							"project":det.project,
							"qty":str(det.qty),
							"uom":str(det.uom)
							})
	

	#REPORT3
	elif(filters.module=='Purchase Receipt'):
		if(filters.mr_name==None):
			# frappe.msgprint("oops! I can't get any MR")
			if(filters.item_code==None):
				item_dicts = []
				data=[]
				dict1=[]
				gug=[]

				variant_results = frappe.db.get_all(
					"Item",
					fields=["name"],
					filters={
						"variant_of": filters.item,
						"disabled": 0
					}
				)

				if not variant_results:
					#frappe.msgprint(_("There aren't any item variants for the selected item"))
					return []
				else:
					variant_list = [variant['name'] for variant in variant_results]
				for itemcode in variant_list:
					query1 = frappe.db.sql("SELECT DISTINCT(mr.name) from `tabPurchase Receipt`as mr,`tabPurchase Receipt Item`as mri WHERE mri.parent=mr.name and mri.item_code='"+str(itemcode)+"' and mr.docstatus!='2'",as_dict=1)
					
					for i in query1:
						gug.append(i.name)
				vis=set(gug)
				for i in vis:
					query=frappe.db.sql("SELECT * from `tabPurchase Receipt`as mr,`tabPurchase Receipt Item`as mri WHERE mr.name=mri.parent and mr.name='"+str(i)+"' ",filters,as_dict=1)
					for det in query:
						hint=frappe.db.get_value("Item",det.item_code,"variant_of")
						if(hint==filters.item):
							ic=det.item_code
							attr_val_map = get_attribute_values_map(ic)
							attributes = frappe.db.get_all(
								"Item Variant Attribute",
								fields=["attribute"],
								filters={
									"parent": ic
								},
								group_by="attribute"
							)
							attribute_list = [row.get("attribute") for row in attributes]
							dict1.append({"item_code":det.item_code,"mr":det.parent,"project":det.project,"status":det.status,"item_name":det.description,"qty":str(det.qty),"uom":str(det.uom),"row":str(det.idx)})
							for attribute in attribute_list:
								for item_dict in dict1:
									name = item_dict.get("item_code")
									attr_dict = attr_val_map.get(name)
									if attr_dict and attr_dict.get(attribute):
										item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
							
							data.append(item_dict)

			elif(filters.item==None):
				item_dicts = []
				data=[]
				dict1=[]
				gug=[]
				query1 = frappe.db.sql("SELECT DISTINCT(mr.name) from `tabPurchase Receipt`as mr,`tabPurchase Receipt Item`as mri WHERE mri.parent=mr.name and mr.docstatus!='2' and mri.item_code=%(item_code)s ",filters,as_dict=1)
				
				for i in query1:
					gug.append(i.name)
				vis=set(gug)
				for i in vis:
					query=frappe.db.sql("SELECT * from `tabPurchase Receipt`as mr,`tabPurchase Receipt Item`as mri WHERE mr.name=mri.parent and mr.name='"+str(i)+"' and mri.item_code=%(item_code)s ",filters,as_dict=1)
					for det in query:
						ic=det.item_code
						attr_val_map = get_attribute_values_map(ic)
						attributes = frappe.db.get_all(
							"Item Variant Attribute",
							fields=["attribute"],
							filters={
								"parent": ic
							},
							group_by="attribute"
						)
						attribute_list = [row.get("attribute") for row in attributes]
						dict1.append({"item_code":det.item_code,"mr":det.parent,"project":det.project,"status":det.status,"item_name":det.description,"qty":str(det.qty),"uom":str(det.uom),"row":str(det.idx)})
						for attribute in attribute_list:
							for item_dict in dict1:
								name = item_dict.get("item_code")
								attr_dict = attr_val_map.get(name)
								if attr_dict and attr_dict.get(attribute):
									item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
						
						data.append(item_dict)	

		else:
			data=[]
			ar=[]
			dict1=[]
			if(filters.item_code!=None and filters.mr_name!=None):
				query=frappe.db.sql("SELECT * from `tabPurchase Receipt`as mr,`tabPurchase Receipt Item`as mri WHERE mr.name=mri.parent and mr.name=%(mr_name)s and mri.item_code=%(item_code)s ",filters,as_dict=1)
				for det in query:
					ic=det.item_code
					attr_val_map = get_attribute_values_map(ic)
					attributes = frappe.db.get_all(
						"Item Variant Attribute",
						fields=["attribute"],
						filters={
							"parent": ic
						},
						group_by="attribute"
					)
					attribute_list = [row.get("attribute") for row in attributes]
					dict1.append({"variant_name":det.item_code})
					for item_dict in dict1:
						name = item_dict.get("variant_name")
						for attribute in attribute_list:
							attr_dict = attr_val_map.get(name)
							if attr_dict and attr_dict.get(attribute):
								item_dict["item_code"]=det.item_code
								item_dict["item_name"]=det.description
								item_dict["project"]=det.project
								item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
								item_dict["qty"]=str(det.qty)
								item_dict["uom"]=str(det.uom)
					data.append(item_dict)

			else:
				query=frappe.db.sql("SELECT * from `tabPurchase Receipt`as mr,`tabPurchase Receipt Item`as mri WHERE mr.name=mri.parent and mr.name=%(mr_name)s ",filters,as_dict=1)
				if(filters.item!=None):
					for det in query:
						hint=frappe.db.get_value("Item",det.item_code,"variant_of")
						if(hint==filters.item and det.parent==filters.mr_name):
							ic=det.item_code
							attr_val_map = get_attribute_values_map(ic)
							attributes = frappe.db.get_all(
								"Item Variant Attribute",
								fields=["attribute"],
								filters={
									"parent": ic
								},
								group_by="attribute"
							)
							attribute_list = [row.get("attribute") for row in attributes]
							dict1.append({"variant_name":det.item_code})
							for item_dict in dict1:
								name = item_dict.get("variant_name")
								for attribute in attribute_list:
									attr_dict = attr_val_map.get(name)
									if attr_dict and attr_dict.get(attribute):
										item_dict["item_code"]=det.item_code
										item_dict["item_name"]=det.description
										item_dict["project"]=det.project
										item_dict[frappe.scrub(attribute)] = attr_val_map.get(name).get(attribute)
										item_dict["qty"]=str(det.qty)
										item_dict["uom"]=str(det.uom)
							data.append(item_dict)

					

				else:
					for det in query:
						data.append({
							"item_code":det.item_code,
							"item_name":det.description,
							"technical_description":det.technical_description,
							"project":det.project,
							"qty":str(det.qty),
							"uom":str(det.uom)
							})
	return data
	
def get_attribute_values_map(ic):
	attribute_list = frappe.db.get_all(
		"Item Variant Attribute",
		fields=[
			"attribute",
			"attribute_value",
			"parent"
		],
		filters={
			"parent": ic
		}
	)

	attr_val_map = {}
	for row in attribute_list:
		name = row.get("parent")
		if not attr_val_map.get(name):
			attr_val_map[name] = {}

		attr_val_map[name][row.get("attribute")] = row.get("attribute_value")

	return attr_val_map