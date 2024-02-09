# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class ComboItems(Document):
	pass
@frappe.whitelist()
def appendmr(ar):
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
						"conversion_factor":j.conversion_factor
						})
				else:
					items.append({
						"item_code":j.item_code,
						"item_name":j.item_name,
						"description":j.description,
						"qty":j.qty*i["qty"],
						"uom":j.uom,
						"stock_uom":j.stock_uom,
						"conversion_factor":j.conversion_factor
						})

	return items

