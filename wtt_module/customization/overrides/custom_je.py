import frappe
from frappe import _, msgprint, scrub
from frappe.utils import cint, cstr, flt, fmt_money, formatdate, get_link_to_form, nowdate

from datetime import date,datetime,timedelta
import functools
import re
from erpnext.accounts.doctype.journal_entry.journal_entry import JournalEntry

class customJE(JournalEntry):
	def validate(self):
		super().validate()
	def on_submit(self):
		super().on_submit()
		if(self.create_petty_cash_entry==1):
			self.make_prejournal()
	def on_cancel(self):
		super().on_cancel()
		frappe.db.sql("UPDATE `tabPre Journal Entry` set docstatus=0,workflow_state='Rejected' WHERE journal_name='"+str(self.name)+"' ")

	def make_prejournal(self):
		arr=[]
		if(frappe.db.exists({'doctype': 'Pre Journal Entry','journal_name': self.name})):
			doc = frappe.get_last_doc('Pre Journal Entry',filters={'journal_name': self.name})
			doc.company=self.company
			doc.journal_name=self.name
			doc.title=self.title
			doc.voucher_type="Cash Entry"
			doc.payment_type=self.payment_type
			doc.posting_date=self.posting_date
			if(self.payment_type=='Pay'):
				doc.paid_date=self.paid_date
			elif(self.payment_type=='Receive'):
				doc.received_date=self.received_date
			doc.sites=self.sites
			for vals in self.accounts:
				arr.append(vals)
			doc.append('accounts',arr)
			doc.cheque_no=self.cheque_no
			doc.cheque_date=self.cheque_date
			doc.user_remark=self.user_remark
			doc.total_credit=self.total_credit
			doc.total_debit=self.total_debit
			doc.remark=self.remark
			doc.buill_no=self.bill_no
			doc.bill_date=self.bill_date
			doc.due_date=self.due_date
			doc.mode_of_payment=self.mode_of_payment
			doc.save()

		else:
			doc=frappe.new_doc('Pre Journal Entry')
			doc.journal_name=self.name
			doc.company=self.company
			doc.title=self.title
			doc.voucher_type=self.voucher_type
			doc.payment_type=self.payment_type
			doc.posting_date=self.posting_date
			if(self.payment_type=='Pay'):
				doc.paid_date=self.paid_date
			elif(self.payment_type=='Receive'):
				doc.received_date=self.received_date
			doc.sites=self.sites
			
			for vals in self.accounts:
				doc.append('accounts',{
					"account":vals.account,
					"party_type":vals.party_type,
					"debit":vals.debit,
					"credit":vals.credit,
					"debit_in_account_currency":vals.debit_in_account_currency,
					"credit_in_account_currency":vals.credit_in_account_currency,
					"account_currency":vals.account_currency,
					"is_advance":vals.is_advance,
					"exchange_rate":vals.exchange_rate,
					"cost_center":vals.cost_center
					})
			doc.cheque_no=self.cheque_no
			doc.cheque_date=self.cheque_date
			doc.user_remark=self.user_remark
			doc.total_credit=self.total_credit
			doc.total_debit=self.total_debit
			doc.remark=self.remark
			doc.buill_no=self.bill_no
			doc.bill_date=self.bill_date
			doc.due_date=self.due_date
			doc.mode_of_payment=self.mode_of_payment
			doc.save()

	def del_prejournal(self):
		# frappe.msgprint("done")
		pass
	@frappe.whitelist()
	def get_address(self):
		from frappe.contacts.doctype.address.address import get_address_display, get_condensed_address

		filters = [
			["Dynamic Link", "link_doctype", "=", "Supplier"],
			["Dynamic Link", "link_name", "=", self.supplier],
			["Dynamic Link", "parenttype", "=", "Address"],
		]
		address_list = frappe.get_list("Address", filters=filters, fields=["*"], order_by="creation asc")

		address_list = [a.update({"display": get_address_display(a)}) for a in address_list]

		address_list = sorted(
			address_list,
			key=functools.cmp_to_key(
				lambda a, b: (int(a.is_primary_address - b.is_primary_address))
				or (1 if a.modified - b.modified else 0)
			),
			reverse=True,
		)

		self.set_onload("addr_list", address_list)
		test=''
		for i in address_list:
			test="<b>"+str(i["address_title"])+"</b><br>"+str(i["address_line1"])+"<br>"+str(i["address_line2"])+"<br>"+str(i["city"])+"<br>"+str(i["county"])+"<br>"+str(i["state"])+"<br>"+str(i["country"])
		return test