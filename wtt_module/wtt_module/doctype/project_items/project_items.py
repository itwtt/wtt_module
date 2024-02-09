# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProjectItems(Document):
	def validate(self):
		if(frappe.db.exists({"doctype": "Stock Ledger Entry", "item_code": str(self.item_code), "warehouse":"Stores - WTT", "is_cancelled":0})):
			bl = frappe.get_last_doc('Stock Ledger Entry',filters={"item_code": str(self.item_code), "warehouse":"Stores - WTT", "is_cancelled":0})
			bl_qty = bl.qty_after_transaction
			for i in frappe.db.sql("SELECT sum(qty)as qty FROM `tabProject Items` WHERE item_code='"+str(self.item_code)+"' and name!='"+str(self.name)+"' GROUP BY item_code ",as_dict=1):
				if(i.qty+self.qty>bl_qty):
					frappe.throw("Total qty available is "+str(bl_qty)+" right now")

		else:
			frappe.throw("Check if the Items are available in stock")