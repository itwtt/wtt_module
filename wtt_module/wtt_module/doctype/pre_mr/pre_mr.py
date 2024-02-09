# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class PreMR(Document):
	def validate(self):
		for i in self.items:
			i.required_by=self.required_by
			i.project=self.project
			if(i.pre_mr_uom=="Millimeter"):
				i.qty=round((float(i.pre_mr_qty)/1000),2)
				i.uom="Meter"

			else:
				i.qty=i.pre_mr_qty
				i.uom=i.pre_mr_uom

	def on_submit(self):
		ar=[]
		query = frappe.db.sql("SELECT item_code,sum(qty) as qty,uom,GROUP_CONCAT(idx)as idx,GROUP_CONCAT(DISTINCT(drawing_no))as drawing_no,GROUP_CONCAT(DISTINCT(remarks))as remarks FROM `tabPre MR Table` WHERE parent='"+(str(self.name))+"' GROUP BY item_code",as_dict=1)
		doc=frappe.new_doc("Material Request")
		doc.request_purpose = self.purpose
		doc.title=self.title
		doc.system_name=self.system_name
		doc.schedule_date = self.required_by
		doc.project = self.project
		doc.set_warehouse = self.set_warehouse
		for i in query:
			if(i.drawing_no==None):
				i.drawing_no=""
			if(i.remarks==None):
				i.remarks==""
			doc.append("items",{
				"item_code":i.item_code,
				"qty":i.qty,
				"bal_qty":i.qty,
				"project":self.project,
				"pre_mr":self.name,
				"pre_mr_line_item":i.idx,
				"drawing_no":i.drawing_no,
				"remarks":i.remarks
				})
		doc.save()

@frappe.whitelist()
def get_item_list(ar):
	items=[]
	to_python=json.loads(ar)
	for i in to_python:
		if(frappe.db.exists("Combo Items",str(i["item_code"]))):
			doc=frappe.get_doc("Combo Items",i["item_code"])
			for j in doc.items:
				if(j.technical_description!=None):
					items.append({
						"item_code":j.item_code,
						"item_name":j.item_name,
						"description":j.description,
						"technical_description":j.technical_description,
						"qty":j.qty*i["qty"],
						"uom":j.uom,
						"stock_uom":j.stock_uom,
						"conversion_factor":j.conversion_factor,
						"drawing_no":i["drawing_no"],
						"remarks":i["remarks"]
						})
				else:
					items.append({
						"item_code":j.item_code,
						"item_name":j.item_name,
						"description":j.description,
						"qty":j.qty*i["qty"],
						"uom":j.uom,
						"stock_uom":j.stock_uom,
						"conversion_factor":j.conversion_factor,
						"drawing_no":i["drawing_no"],
						"remarks":i["remarks"]
						})
		else:
			items.append({
				"item_code":i["item_code"],
				"qty":i["qty"],
				"uom":i["uom"],
				"drawing_no":i["drawing_no"],
				"remarks":i["remarks"]
			})
	return items


@frappe.whitelist()
def from_bom(source_name, target_doc=None):
	def postprocess(source, target):
		pass
	doc = get_mapped_doc("BOM", source_name, {
		"BOM": {
			"doctype": "Pre MR",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"BOM Item": {
			"doctype": "Combo Table",
			"field_map": {
				"bom":"parent"
			}
		}
	}, target_doc,postprocess)
	return doc

@frappe.whitelist()
def from_product_bundle(source_name, target_doc=None):
	def postprocess(source, target):
		pass
	doc = get_mapped_doc("Product Bundle", source_name, {
		"Product Bundle": {
			"doctype": "Pre MR",
			"validation": {
				"docstatus": ["=", 0]
			}
		},
		"Product Bundle Item": {
			"doctype": "Combo Table"
		}
	}, target_doc,postprocess)
	return doc
