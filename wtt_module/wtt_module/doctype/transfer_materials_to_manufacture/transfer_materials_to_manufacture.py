# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class TransferMaterialstoManufacture(Document):
	pass






@frappe.whitelist()
def get_bom(bom):
	ar=[]
	query = frappe.db.sql("SELECT bt.item_code,bt.item_code,bt.description,bt.technical_description,bt.qty,bt.uom FROM `tabBOM`as bb,`tabBOM Item`as bt WHERE bb.name=bt.parent and bt.category='Assembly' and bb.name='"+str(bom)+"' ",as_dict=1)
	for i in query:
		ar.append(i)

	return ar

@frappe.whitelist()
def get_pr(pr):
	ar=[]
	query = frappe.db.sql("SELECT bt.item_code,bt.item_code,bt.description,bt.technical_description,bt.qty,bt.uom,bt.project,bt.conversion_factor,bt.material_request,bt.material_request_item,bt.purchase_order,bt.purchase_order_item,bt.name as pr_item,bb.name as reference_purchase_receipt FROM `tabPurchase Receipt`as bb,`tabPurchase Receipt Item`as bt WHERE bb.name=bt.parent and bb.name='"+str(pr)+"' ",as_dict=1)
	for i in query:
		ar.append(i)

	return ar

@frappe.whitelist()
def create_stock(items,warehouse):
	to_python = json.loads(items)
	doc=frappe.new_doc("Stock Entry")
	doc.stock_entry_type="Material Transfer for Manufacture"
	for i in to_python:
		doc.append("items",{
			"item_code":i["item_code"],
			"qty":i["qty"],
			"uom":i["uom"],
			"reference_purchase_receipt":i["reference_purchase_receipt"],
			"project":i["project"],
			"conversion_factor":i["conversion_factor"],
			"pr_item":i["pr_item"]
			})
	doc.from_warehouse = "Stores - WTT"
	doc.to_warehouse = warehouse
	doc.save()

@frappe.whitelist()
def get_stock(items,warehouse):
	to_python = json.loads(items)
	doc=frappe.new_doc("Stock Entry")
	doc.stock_entry_type="Material Receipt"
	for i in to_python:
		doc.append("items",{
			"item_code":i["item_code"],
			"qty":i["qty"],
			"uom":i["uom"],
			"reference_purchase_receipt":i["reference_purchase_receipt"],
			"project":i["project"],
			"conversion_factor":i["conversion_factor"],
			"pr_item":i["pr_item"]
			})
	doc.to_warehouse = warehouse
	doc.save()
	