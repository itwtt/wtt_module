


from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, nowdate, add_days
from frappe.model.mapper import get_mapped_doc

from erpnext.controllers.buying_controller import BuyingController
from erpnext.buying.utils import validate_for_items
import json
import csv
import requests
from erpnext.buying.doctype.supplier_quotation.supplier_quotation import SupplierQuotation

class CustomSupplierQuotation(SupplierQuotation):
	def validate(self):
		super().validate()
		# if(self.combined_table==[] and self.supplier_data_table==[]):
		# 	for i in frappe.db.sql("SELECT item_code,sum(qty)as qty,uom,description,technical_description,rate,sum(amount)as amount,sum(price_list_rate)as price_list_rate,discount_percentage,discount_amount,item_tax_template,material_request FROM `tabSupplier Quotation Item` WHERE parent='"+str(self.name)+"' GROUP BY item_code ORDER BY technical_description",as_dict=1):
		# 		self.append("supplier_data_table",i)
		# 	for j in frappe.db.sql("SELECT item_code,sum(qty)as qty,uom,description,technical_description,rate as rate2,sum(amount)as amount2,sum(price_list_rate)as price_list_rate2,discount_percentage,discount_amount,item_tax_template,material_request FROM `tabSupplier Quotation Item` WHERE parent='"+str(self.name)+"' GROUP BY item_code ORDER BY technical_description",as_dict=1):
		# 		self.append("combined_table",j)