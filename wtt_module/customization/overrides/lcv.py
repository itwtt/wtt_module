import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.meta import get_field_precision
from frappe.utils import flt

import erpnext
from erpnext.controllers.taxes_and_totals import init_landed_taxes_and_totals
from erpnext.stock.doctype.serial_no.serial_no import get_serial_nos
from erpnext.stock.doctype.landed_cost_voucher.landed_cost_voucher import LandedCostVoucher

class custom_lcv(LandedCostVoucher):
	def on_submit(self):
		super().on_submit()
		pass
		# datas=self.get_datas_from_lcv()
		# doc=frappe.new_doc("Payment Module")
		# doc.payment_type="Landed Cost Voucher"
		# doc.naming_series="LAN-COST-"
		# doc.landed_cost_no=self.name
		# for i in datas:
		# 	doc.append("landed_table",i)
		# doc.total_amount=i.amount	
		# doc.submit()


	def get_datas_from_lcv(self):
		ar=[]
		total = self.total_taxes_and_charges
		tds = self.tds_amount
		amount = self.amount
		for i in self.purchase_receipts:
			ar.append({
				"voucher_no":i.receipt_document,
				"project":frappe.db.get_value(i.receipt_document_type,i.receipt_document,"project"),
				"supplier":frappe.db.get_value("Landed Cost Taxes and Charges",{"parent":self.name},"supplier"),
				"total":total,
				"tds":tds,
				"amount":amount
				})
		return ar
