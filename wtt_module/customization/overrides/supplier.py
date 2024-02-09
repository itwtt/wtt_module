import frappe
import frappe.defaults
from frappe import _, msgprint
import re

from erpnext.buying.doctype.supplier.supplier import Supplier

class customSupplier(Supplier):
	def validate(self):
		super().validate()
		self.check_gst()
		qv = frappe.db.sql("SELECT * FROM `tabSupplier` WHERE tax_id='"+str(self.tax_id)+"' and name!='"+self.name+"'")
		if(qv):
			frappe.throw("Tax ID Already exists")
		else:
			pass
	def after_insert(self):
		self.create_bank_account()
		# self.create_account()

	def on_update(self):
		super().on_update()
		self.create_bank_account()
		# self.create_account()

	def create_bank_account(self):
		if(self.bank_account_no):
			if frappe.db.exists({'doctype':'Bank Account','party':self.name}):
				if(self.bank and self.ifsc_code and self.branch):
					nn = frappe.db.get_value('Bank Account', {'party': self.name},'name')
					doc=frappe.get_doc("Bank Account", nn)
					doc.account_name=self.name
					doc.bank=self.bank
					doc.party_type='Supplier'
					doc.party=self.name
					doc.iban=self.iban
					doc.ifsc_code=self.ifsc_code
					doc.branch=self.branch
					doc.branch_code=self.branch_code
					doc.bank_account_no=self.bank_account_no
					doc.save()
				else:
					frappe.throw("Bank Name, IFSC, Branch Missing")
			else:
				if(self.bank and self.ifsc_code and self.branch):
					doc=frappe.new_doc("Bank Account")
					doc.account_name=self.name
					doc.bank=self.bank
					doc.party_type='Supplier'
					doc.party=self.supplier_name
					doc.iban=self.iban
					doc.ifsc_code=self.ifsc_code
					doc.branch=self.branch
					doc.branch_code=self.branch_code
					doc.bank_account_no=self.bank_account_no
					doc.save()
				else:
					frappe.throw("Bank IFSC, Branch, Bank Name Missing")
		else:
			frappe.throw("Bank Account is mandorary")

	def create_account(self):
		if (frappe.db.exists({'doctype':'Account','ref':self.name}) or frappe.db.exists('Account',self.supplier_name+" - WTT")):
			pass
		else:
			acc=frappe.new_doc("Account")
			acc.account_name=self.name
			acc.parent_account='Trade Payables - WTT'
			acc.ref=self.name
			acc.account_type="Payable"
			acc.party_type=self.doctype
			acc.party=self.name
			acc.save()

	def check_gst(self):
		regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}"+"[A-Z]{1}[1-9A-Z]{1}"+"Z[0-9A-Z]{1}$"
		p = re.compile(regex)
		if(self.tax_id!=None and self.tax_id!=''):
			if(re.search(p, self.tax_id)):
				pass
			else:
				frappe.throw("Invalid Tax ID")
		
