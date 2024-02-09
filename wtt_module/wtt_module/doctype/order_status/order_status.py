# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OrderStatus(Document):
	pass



@frappe.whitelist()
def get_po(po_no):
	arr=[]
	for i in frappe.db.sql("SELECT * FROM `tabPurchase Order Item` WHERE parent='"+str(po_no)+"' ORDER BY idx ASC",as_dict=1):
		arr.append({
			"item_code":i.item_code,
			"description":i.description,
			"technical_description":i.technical_description,
			"qty":i.qty
		})
	return arr