# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate

from num2words import num2words
from frappe.utils.background_jobs import enqueue
import erpnext
import re
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice


class customPI(PurchaseInvoice):
	def validate(self):
		super().validate()

		valword=num2words(self.rounded_total, lang='en_IN')
		if(self.is_return==1):
			valword=num2words((self.rounded_total*(-1)), lang='en_IN')

		self.in_words=valword.capitalize()
		if(self.tax_id!=None):
			if(self.validate_gst()==True):
				pass
			else:
				frappe.throw("Invalid Tax ID")
	def validate_gst(self):
		regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}" +"[A-Z]{1}[1-9A-Z]{1}" +"Z[0-9A-Z]{1}$"
		p = re.compile(regex)
		if (self.tax_id == None):
			return False
		if(re.search(p, self.tax_id)):
			return True
		else:
			return False

	def on_submit(self):
		super().on_submit()
		if self.is_return==1:
			receiver = str(self.contact_email)
			message=f"<html>Dear <b>"+str(self.supplier)+"</b>,<br><br>Please find the Debit note against "+str(self.supplier_delivery_note)
			password = None
			if receiver:
				email_args = {
					"recipients": [receiver],
					"message": message,
					"subject": 'Debit Note against {0}'.format(str(self.supplier_delivery_note)),
					"attachments": [frappe.attach_print("Purchase Invoice", str(self.name), file_name=str(self.name), password=password)],
					"reference_doctype": "Purchase Invoice",
					"reference_name": str(self.name)
					}
				if not frappe.flags.in_test:
					enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
				else:
					frappe.sendmail(**email_args)
			else:
				pass
	@frappe.whitelist()
	def get_not_received_items(self):
		datas = []
		pr=[]
		for i in self.items:
			if(i.purchase_receipt not in pr):
				pr.append(i.purchase_receipt)

		query = frappe.db.sql("SELECT * from `tabNot Received Items` where parent='"+str(pr[0])+"' and docstatus=1 ",as_dict=1)
		if query:
			for i in query:
				datas.append(i)

		return datas