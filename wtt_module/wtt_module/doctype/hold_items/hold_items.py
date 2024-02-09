# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class HoldItems(Document):
	def on_submit(self):
		if(self.request=="Material Request"):
			for i in self.items:
				frappe.db.sql("UPDATE `tabMaterial Request Item` set holded=1,hold_reason='"+str(i.hold_reason)+"' WHERE name='"+str(i.child)+"' ")
		elif(self.request=="Purchase Order"):
			for i in self.items:
				frappe.db.sql("UPDATE `tabPurchase Order Item` set holded=1,hold_reason='"+str(i.hold_reason)+"' WHERE name='"+str(i.child)+"' ")
		elif(self.request=="Purchase Receipt"):
			for i in self.items:
				frappe.db.sql("UPDATE `tabPurchase Receipt Item` set holded=1,hold_reason='"+str(i.hold_reason)+"' WHERE name='"+str(i.child)+"' ")

	def on_cancel(self):
		if(self.request=="Material Request"):
			for i in self.items:
				frappe.db.sql("UPDATE `tabMaterial Request Item` set holded=0,hold_reason=NULL WHERE name='"+str(i.child)+"' ")
		elif(self.request=="Purchase Order"):
			for i in self.items:
				frappe.db.sql("UPDATE `tabPurchase Order Item` set holded=0,hold_reason=NULL WHERE name='"+str(i.child)+"' ")
		elif(self.request=="Purchase Receipt"):
			for i in self.items:
				frappe.db.sql("UPDATE `tabPurchase Receipt Item` set holded=0,hold_reason=NULL WHERE name='"+str(i.child)+"' ")



@frappe.whitelist()
def get_items(doc,num):
	ar=[]
	
	doc1=frappe.get_doc(doc,num)
	for i in doc1.items:
		ar.append({
			"item_code":i.item_code,
			"item_name":i.item_name,
			"description":i.description,
			"technical_description":i.technical_description,
			"qty":i.qty,
			"uom":i.uom,
			"parent1":num,
			"child":i.name,
			"project":i.project
			})

	return ar

