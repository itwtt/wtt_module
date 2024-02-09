# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from datetime import datetime
from datetime import date
class PaymentConsolidate(Document):
	# pass
	def on_submit(self):
		for i in final_table:
			doc=frappe.new_doc("Payment Entry")
			doc.payment_type='Pay'
			doc.mode_of_payment='NEFT/RTGS/IMPS'
			doc.party_type='Supplier'
			doc.party=i.supplier
			doc.paid_amount=i.outstanding_amount
			doc.reference_no='000000'
			doc.reference_date=date.today()
			doc.append("references",{
				"reference_doctype":"Purchase Invoice",
				"reference_name":i.invoice_no,
				"allocated_amount":i.outstanding_amount
				})
			doc.save()
			frappe.db.commit()
	# 	for i in final_table:
	# 		doc=frappe.get_doc("Purchase Invoice")
	# 		doc.is_paid=1
	# 		doc.submit()


@frappe.whitelist()
def update_status(go):
	ar=[]
	for k in frappe.db.sql("SELECT name FROM `tabAccount` WHERE parent_account='Accounts Payable - WTT'",as_dict=1):
		for i in frappe.db.sql("SELECT name,status,supplier,posting_date,grand_total,outstanding_amount FROM `tabPurchase Invoice` WHERE status='Overdue' AND credit_to='"+k.name+"' ORDER BY supplier ASC",as_dict=1):
			today = date.today()
			f_date = datetime.strptime(str(i.posting_date), '%Y-%m-%d')
			l_date = datetime.strptime(str(today), '%Y-%m-%d')
			delta = l_date - f_date
			age=delta.days
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"status":i.status,
				"age":age,
				"credit_amount":i.grand_total,
				"outstanding_amount":i.outstanding_amount
			})

		for j in frappe.db.sql("SELECT name,status,supplier,posting_date,grand_total,outstanding_amount FROM `tabPurchase Invoice` WHERE status='Unpaid' AND credit_to='"+k.name+"' ORDER BY supplier ASC",as_dict=1):
			today1 = date.today()
			f_date1 = datetime.strptime(str(j.posting_date), '%Y-%m-%d')
			l_date1 = datetime.strptime(str(today1), '%Y-%m-%d')
			delta1 = l_date1 - f_date1
			age1=delta1.days
			ar.append({
				"name":j.name,
				"supplier":j.supplier,
				"status":i.status,
				"age":age1,
				"credit_amount":j.grand_total,
				"outstanding_amount":j.outstanding_amount
			})
		'''
		for j in frappe.db.sql("SELECT jec.parent,jec.party,jec.debit_in_account_currency,jec.credit_in_account_currency,je.posting_date FROM `tabJournal Entry Account` as jec INNER JOIN `tabJournal Entry` as je ON je.name=jec.parent WHERE jec.account='"+k.name+"' AND je.voucher_type='Journal Entry' AND je.docstatus!=2 ORDER BY jec.party ASC",as_dict=1):
			today1 = date.today()
			f_date1 = datetime.strptime(str(j.posting_date), '%Y-%m-%d')
			l_date1 = datetime.strptime(str(today1), '%Y-%m-%d')
			delta1 = l_date1 - f_date1
			age1=delta1.days
			ar.append({
			"name":j.parent,
			"supplier":j.party,
			"age":age1,
			"credit_amount":j.credit_in_account_currency,
			"debit_amount":j.debit_in_account_currency
			})
		for u in frappe.db.sql("SELECT jec.parent,jec.party,jec.debit_in_account_currency,jec.credit_in_account_currency,je.posting_date FROM `tabJournal Entry Account` as jec INNER JOIN `tabJournal Entry` as je ON je.name=jec.parent WHERE jec.account='"+k.name+"' AND je.voucher_type='Opening Entry' AND je.docstatus!=2 ORDER BY jec.party ASC",as_dict=1):
			today4 = date.today()
			f_date4 = datetime.strptime(str(u.posting_date), '%Y-%m-%d')
			l_date4 = datetime.strptime(str(today4), '%Y-%m-%d')
			delta4 = l_date4 - f_date4
			age4=delta4.days
			ar.append({
			"name":u.parent,
			"supplier":u.party,
			"age":age4,
			"credit_amount":u.credit_in_account_currency,
			"debit_amount":u.debit_in_account_currency
			})
		for m in frappe.db.sql("SELECT name,party,posting_date,paid_amount FROM `tabPayment Entry` WHERE status!='Cancelled' and paid_to='"+k.name+"' ORDER BY party ASC",as_dict=1):
			today2 = date.today()
			f_date2 = datetime.strptime(str(m.posting_date), '%Y-%m-%d')
			l_date2 = datetime.strptime(str(today2), '%Y-%m-%d')
			delta2 = l_date2 - f_date2
			age2=delta2.days
			ar.append({
				"name":m.name,
				"supplier":m.party,
				"age":age2,
				"credit_amount":0,
				"debit_amount":m.paid_amount
			})
		for n in frappe.db.sql("SELECT name,party,posting_date,received_amount FROM `tabPayment Entry` WHERE status!='Cancelled' and paid_from='"+k.name+"' ORDER BY party ASC",as_dict=1):
			today3 = date.today()
			f_date3 = datetime.strptime(str(n.posting_date), '%Y-%m-%d')
			l_date3 = datetime.strptime(str(today3), '%Y-%m-%d')
			delta3 = l_date3 - f_date3
			age3=delta3.days
			ar.append({
				"name":n.name,
				"supplier":n.party,
				"age":age3,
				"credit_amount":n.received_amount,
				"debit_amount":0
			})
		'''
	return ar

@frappe.whitelist()
def update_items(gok):
	to_python = json.loads(gok)
	lst = []
	item = []
	mr=[]
	v=[]
	for i in to_python:
		if i["supplier"] not in lst:
			item.append(i)
			lst.append(i["supplier"])
		else:
			item[lst.index(i["supplier"])]["credit_amount"] += i["credit_amount"]
			item[lst.index(i["supplier"])]["outstanding_amount"] += i["outstanding_amount"]
	v=[]
	for q in item:
		v.append({
			"supplier":q['supplier'],
			"credit_amount":q['credit_amount'],
			"total":q['outstanding_amount']
			})
	return v
	#return item
	# 	frappe.msgprint(str(item))
	# 	sup=i["supplier"]
	# 	val=j["credit_amount"]-j["debit_amount"]
	# 	for k in frappe.db.sql("SELECT party,bank_account_no,ifsc_code,bank,branch FROM `tabBank Account` WHERE party='"+str(sup)+"' ",as_dict=1):
	# 		v.append({
	# 			"party":k.party,
	# 			"credit_amount":j["credit_amount"],
	# 			"debit_amount":j["debit_amount"],
	# 			"total":val
	# 			})
	# return v