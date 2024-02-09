# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class POReferenceDocument(Document):
	def on_submit(self):
		frappe.db.sql("UPDATE `tabPurchase Order` SET reference_document='"+str(self.name)+"' WHERE name='"+str(self.purchase_order)+"'")
