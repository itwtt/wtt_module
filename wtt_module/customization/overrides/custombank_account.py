import frappe
from frappe import _,msgprint

from erpnext.accounts.doctype.bank_account.bank_account import BankAccount


class customBankAccount(BankAccount):
	def validate(self):
		super().validate()
		if(self.bank_account_no!=None and self.iban==None):
			val=frappe.db.sql("SELECT * FROM `tabBank Account` WHERE bank_account_no='"+self.bank_account_no+"' and name!='"+str(self.name)+"'")
			if(val):
				frappe.msgprint("Bank Account No Already Exists")
			else:
				pass