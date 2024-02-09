# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MaterialsforEnquiry(Document):
	def on_submit(self):
		# ar=[]
		# for i in frappe.db.sql("SELECT item_code,item_name,description,technical_description,sum(qty)as qty,uom,0 as rate,0 as amount FROM `tabMaterials Table` where parent='"+str()+"' ",as_dict=1):
		# 	ar.append(i)
		# enq=frappe.new_doc("Received Quotation")
		# enq.date=self.date
		# enq.enquiry_materials=ar
		# enq.tax_percentage=0
		# enq.save()
		pass
