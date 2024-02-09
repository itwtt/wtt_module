# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from datetime import datetime
from datetime import date,timedelta
from num2words import num2words
from pytz import timezone
from wtt_module.wtt_module.doctype.final_bank_statement.final_bank_statement import Finalbankstatement
from erpnext.accounts.utils import get_account_currency, get_balance_on, get_outstanding_invoices
class PaymentModule(Document):
	def validate(self):
		# if(frappe.session.user == 'salamon@wttindia.com' or frappe.session.user=='ramanathan@wttindia.com'):
		# 	if(self.payment_type == 'Request for Payment'):
		# 		frappe.throw("Purchase team restrict to raise the request for payment")
		# at=ft=[]
		# for i in self.advance_table:
		# 	at.append(i.order_no)
		# set_at=set(at)
		# if(len(set_at)!=len(at)):
		# 	frappe.throw("POs repeating")
		# for i in self.freight_table:
		# 	ft.append(i.order_no)
		# set_ft=set(ft)
		# if(len(set_ft)!=len(ft)):
		# 	frappe.throw("POs repeating")

		if(self.payment_type == 'Advance Payment'):
			pro=[]
			order=[]
			project=[]
			order_no=[]
			val=0
			for i in self.advance_table:
				project.append(i.pro)
				order_no.append(i.order_no)
			project_uni = set(project)
			order_uni = set(order_no)

			for j in project_uni:
				pro.append(j)

			for k in order_uni:
				order.append(k)

			str1 = ','.join(str(e) for e in pro)
			str2 = ','.join(str(f) for f in order)

			self.project=str1
			self.order=str2
		elif(self.payment_type == 'Freight Payment'):
			pro=[]
			order=[]
			project=[]
			order_no=[]
			val=0
			for i in self.freight_table:
				project.append(i.project)
				order_no.append(i.order_no)
			project_uni = set(project)
			order_uni = set(order_no)

			for j in project_uni:
				pro.append(j)

			for k in order_uni:
				order.append(k)

			str1 = ','.join(str(e) for e in pro)
			str2 = ','.join(str(f) for f in order)

			self.project=str1
			self.order=str2


		# if(frappe.session.user=="Administrator"):
		# 	self.create_bank_statement()
		if(self.naming_series=='PO-ADV-PAY-'): #for advance payment
			for i in self.advance_table:
				if(float(i.outstanding) == float(i.final_amount)):
					pass
				elif(float(i.outstanding)<float(i.final_amount)):
					frappe.throw('Advance Amount not Greater than PO Outstanding Amount')
				else:
					pass
			if(self.workflow_state=='Approved by HOD'):
				for i in self.advance_table:
					gug=frappe.get_doc("Purchase Order",i.order_no)
					gug.submit()

		elif(self.naming_series=='PO-FRE-PAY-'): # for freight advance
			for i in self.freight_table:
				if(float(i.amount)<float(i.final_amount)):
					frappe.msgprint('Warning Advance Amount not Greater than PO Amount');
				else:
					pass
			if(self.workflow_state=='Approved by HOD'):
				for i in self.advance_table:
					gug=frappe.get_doc("Purchase Order",i.order_no)
					gug.submit()

		elif(self.naming_series=='INV-PAY-'): # for payment consolidate
			for i in self.final_table:
				if((round(float(i.credit_amount)))<(round(float(i.outstanding_amount)))):
					# pass
					frappe.throw('Amount not Greater than Outstanding Amount')
				else:
					pass


		if(frappe.session.user!='Administrator'):
			self.check_prev_request()
	


	def check_prev_request(self):
		local = timezone("Asia/Kolkata")
		localtime=datetime.now(local)
		currenttime=localtime.strftime("%Y-%m-%d %H:%M:%S.%f")
		dd = datetime.strptime(currenttime,"%Y-%m-%d %H:%M:%S.%f")
		date_before_2_days=dd-timedelta(days=2)
		date_before_4_days=dd-timedelta(days=4)

		if(date_before_2_days.strftime("%A") == 'Saturday'):
			date_before_2_days=dd-timedelta(days=3)
			
		if(date_before_4_days.strftime("%A") in ['Thursday','Friday','Saturday']):
			date_before_4_days=dd-timedelta(days=5)


		# if(self.workflow_state=="Created"):
		# 	query=frappe.db.sql("SELECT count(name) as count FROM `tabPayment Module` where docstatus=0 and workflow_state='Approved by HOD' and payment_type='"+str(self.payment_type)+"' and name !='"+str(self.name)+"' and hod_approved_on<='"+str(date_before_2_days)+"' ",as_dict=1)
		# 	if(self.payment_type in ["Advance Payment","Freight Payment","Invoice Payment"] and self.workflow_state!='Rejected'):

		# 		if(query[0]["count"]>1):
		# 			frappe.throw("Some Payment Module pending for Management Approval")

		# 	query2=frappe.db.sql("SELECT count(name) as count FROM `tabPayment Module` where docstatus=0 and workflow_state='Created' and payment_type='"+str(self.payment_type)+"' and name !='"+str(self.name)+"' and creation<='"+str(date_before_4_days)+"' ",as_dict=1)
		# 	if(self.payment_type in ["Advance Payment","Freight Payment","Invoice Payment"] and self.workflow_state!='Rejected'):

		# 		if(query2[0]["count"]>1):
		# 			frappe.throw("Some Payment Module pending for Management Approval")


		# if(self.workflow_state=="Approved by HOD"):
		# 	query3=frappe.db.sql("SELECT count(name) as count FROM `tabPayment Module` where docstatus=0 and workflow_state='Created' and payment_type='"+str(self.payment_type)+"' and name !='"+str(self.name)+"' and creation<='"+str(date_before_2_days)+"' ",as_dict=1)
		# 	if(self.payment_type in ["Advance Payment","Freight Payment","Invoice Payment"] and self.workflow_state!='Rejected'):

		# 		if(query3[0]["count"]>1):
		# 			frappe.throw("Some Payment Module pending for Management Approval")
		# 		else:
		# 			self.hod_approved=frappe.session.user_fullname
		# 			self.hod_approved_on=dd


	def on_submit(self):

		# self.create_bank_statement()


		if(self.naming_series=='PO-ADV-PAY-'): #for advance payment
			for i in self.advance_table:
				gug=frappe.get_doc("Purchase Order",i.order_no)
				gug.append("purchase_advance",{
					"type":"Advance Payment",
					"paid_date":date.today(),
					"advance_type":i.advance,
					"percentage":i.percentage,
					"paid_amount":i.final_amount,
					"table_name":i.name,
					"parent_name":self.name
					})
				gug.total_advance=float(gug.total_advance)+float(i.final_amount)
				gug.submit()

			

		elif(self.naming_series=='PO-FRE-PAY-'): # for freight advance
			for i in self.freight_table:
				if(float(i.amount)<float(i.final_amount)):
					frappe.msgprint('Warning Freight Amount not Greater than PO Amount');
				else:
					pass
			for i in self.freight_table:
				gug=frappe.get_doc("Purchase Order",i.order_no)
				gug.append("purchase_advance",{
					"type":"Freight Advance",
					"paid_date":date.today(),
					"advance_type":str(i.account_head)+"-"+str(i.transport),
					"percentage":'-',
					"paid_amount":i.final_amount,
					"table_name":i.name,
					"parent_name":self.name
					})
				gug.freight_advance=float(gug.freight_advance)+float(i.final_amount)
				gug.submit()

		elif(self.naming_series=='INV-PAY-'): # for purchase invoice
			for i in self.final_table:
				if(float(i.credit_amount)<float(i.outstanding_amount)):
					frappe.msgprint('Warning Outstanding Amount not Greater than Invoiced Amount');
				else:
					pass
			for i in self.final_table:
				gug=frappe.get_doc("Purchase Invoice",i.invoice_no)
				gug.append("payment_approved_to_be_paid_by_management",{
					"type":"Invoice Payment",
					"paid_date":date.today(),
					"advance_type":"Invoice Payment",
					"percentage":'-',
					"paid_amount":i.outstanding_amount,
					"table_name":i.name,
					"parent_name":self.name
					})
				gug.approved_amount=float(gug.approved_amount)+float(i.outstanding_amount)
				gug.submit()

			


		elif(self.payment_type=="Internal Transfer"):
			payment_entry=frappe.new_doc("Payment Entry")
			payment_entry.date=date.today()
			payment_entry.payment_type=self.payment_type
			payment_entry.mode_of_payment=self.mode_of_payment_it
			payment_entry.paid_from=self.accounts_paid_from
			payment_entry.paid_to=self.accounts_paid_to
			payment_entry.paid_amount=self.paid_amount
			payment_entry.received_amount=self.received_amount
			payment_entry.cheque_party=self.cheque_party
			payment_entry.reference_no=self.cheque_no
			payment_entry.reference_date=self.cheque_date
			payment_entry.in_words=num2words(self.total_amount, lang='en_IN')
			payment_entry.save()
	
	def create_bank_statement(self):
		if frappe.db.exists("Final bank statement", {"posting_date": str(date.today()),"docstatus":0}):
			frappe.msgprint("already existes")
		else:
			item=[]
			charge=amt1=amt2 = 0
			target=frappe.new_doc("Final bank statement")
			target.bank_name = "Indian Bank - INDIAN BANK"
			target.paid_from = "6475173650 - INDIAN BANK-OD - WTT"
			if (self.payment_type=="Advance Payment"):
				for i in self.get('advance_consolidate_table'):
					for j in frappe.db.sql("SELECT bank_account_no,ifsc_code,bank,branch FROM `tabBank Account` WHERE party='"+str(i.supplier)+"'",as_dict=1):
						if(float(i.advance_amount)<=float(10000)):
							crg=2
						elif(float(i.advance_amount)>float(10000) and float(i.advance_amount)<=float(100000)):
							crg=5
						elif(float(i.advance_amount)>float(100000) and float(i.advance_amount)<=float(200000)):
							crg=13
						elif(float(i.advance_amount)>float(200000) and float(i.advance_amount)<=float(500000)):
							crg=28
						elif(float(i.advance_amount)>float(500000)):
							crg=56
						if(j.bank=='INDIAN BANK'):
							crg=0
						item.append({
							"benificiary_name":i.supplier,
							"account_no":j.bank_account_no,
							"ifsc_code":j.ifsc_code,
							"bank_name":j.bank,
							"branch":j.branch,
							"charges":crg,
							"amount":i.advance_amount,
							"request_no":i.parent,
							"line":i.name,
							"module_name":"Advance Payment"
							})

			
			elif(self.payment_type=="Freight Payment"):
				for i in self.get('freight_consolidate_table'):
					for j in frappe.db.sql("SELECT bank_account_no,ifsc_code,bank,branch FROM `tabBank Account` WHERE party='"+str(i.supplier)+"'",as_dict=1):
						if(float(i.advance_amount)<=float(10000)):
							crg=2
						elif(float(i.advance_amount)>float(10000) and float(i.advance_amount)<=float(100000)):
							crg=5
						elif(float(i.advance_amount)>float(100000) and float(i.advance_amount)<=float(200000)):
							crg=13
						elif(float(i.advance_amount)>float(200000) and float(i.advance_amount)<=float(500000)):
							crg=28
						elif(float(i.advance_amount)>float(500000)):
							crg=56
						if(j.bank=='INDIAN BANK'):
							crg=0
						item.append({
							"benificiary_name":i.supplier,
							"account_no":j.bank_account_no,
							"ifsc_code":j.ifsc_code,
							"bank_name":j.bank,
							"branch":j.branch,
							"charges":crg,
							"amount":i.advance_amount,
							"request_no":i.parent,
							"line":i.name,
							"module_name":"Advance Payment"
							})
			elif(self.payment_type=="Invoice Payment"):
				for i in self.get('consolidate_table'):
					for j in frappe.db.sql("SELECT bank_account_no,ifsc_code,bank,branch FROM `tabBank Account` WHERE party='"+str(i.supplier)+"'",as_dict=1):
						if(float(i.advance_amount)<=float(10000)):
							crg=2
						elif(float(i.advance_amount)>float(10000) and float(i.advance_amount)<=float(100000)):
							crg=5
						elif(float(i.advance_amount)>float(100000) and float(i.advance_amount)<=float(200000)):
							crg=13
						elif(float(i.advance_amount)>float(200000) and float(i.advance_amount)<=float(500000)):
							crg=28
						elif(float(i.advance_amount)>float(500000)):
							crg=56
						if(j.bank=='INDIAN BANK'):
							crg=0

						item.append({
							"benificiary_name":i.supplier,
							"account_no":j.bank_account_no,
							"ifsc_code":j.ifsc_code,
							"bank_name":j.bank,
							"branch":j.branch,
							"charges":crg,
							"amount":i.advance_amount,
							"request_no":i.parent,
							"line":i.name,
							"module_name":"Advance Payment"
							})
			elif(self.payment_type=="Request for Payment"):
				for i in frappe.db.sql("SELECT party_type,party,bank_account_no,ifsc_code,bank,branch,total_amount FROM `tabPayment Module` where name='"+str(self.name)+"' ",as_dict=1):
					if(float(i.total_amount)<=float(10000)):
						crg=2
					elif(float(i.total_amount)>float(10000) and float(i.total_amount)<=float(100000)):
						crg=5
					elif(float(i.total_amount)>float(100000) and float(i.total_amount)<=float(200000)):
						crg=13
					elif(float(i.total_amount)>float(200000) and float(i.total_amount)<=float(500000)):
						crg=28
					elif(float(i.total_amount)>float(500000)):
						crg=56
					if(i.bank=='INDIAN BANK'):
						crg=0
					if(i.party_type=='Farm Employee'):
						item.append({
							"benificiary_name":frappe.get_value("Farm Employee",i.party,"employee_name"),
							"party_type":i.party_type,
							"account_no":i.bank_account_no,
							"ifsc_code":i.ifsc_code,
							"bank_name":i.bank,
							"branch":i.branch,
							"charges":crg,
							"amount":i.total_amount,
							"request_no":self.name,
							"line":i.name,
							"module_name":"Request for Payment for Purchase"
							})
					else:
						item.append({
							"benificiary_name":i.party,
							"party_type":i.party_type,
							"account_no":i.bank_account_no,
							"ifsc_code":i.ifsc_code,
							"bank_name":i.bank,
							"branch":i.branch,
							"charges":crg,
							"amount":i.total_amount,
							"request_no":self.name,
							"line":i.name,
							"module_name":"Request for Payment for Purchase"
							})
				for i in item:
					if(i["bank_name"]=='INDIAN BANK'):
						target.append("ib_amount_table",i)
					else:
						target.append("amount_table",i)


			
				

			for i in item:
				if(i["bank_name"]=='INDIAN BANK'):
					amt1+=float(i["amount"])
					
					target.append("approved_payment_ib",i)
				else:
					amt2+=float(i["amount"])
					charge+=i["charges"]
					target.append("approved_payment",i)
			target.grand_total=amt2
			target.ib_grand_total=amt1
			target.total_charge=charge
			target.ib_total_charge=0
			target.net_total=amt2+charge
			target.ib_net_total=amt1
			target.save()




	def on_cancel(self):
		if(self.naming_series=='PO-ADV-PAY-'): #for advance payment
			for j in self.advance_table:
				gug=frappe.get_doc("Purchase Order",j.order_no)
				gug.total_advance=float(gug.total_advance)-float(j.final_amount)
				gug.submit()
				val=frappe.db.sql("DELETE FROM `tabPurchase Advance` WHERE table_name='"+str(j.name)+"' AND parent='"+str(j.order_no)+"'")
		elif(self.naming_series=='PO-FRE-PAY-'): # for freight advance
			for j in self.freight_table:
				gug=frappe.get_doc("Purchase Order",j.order_no)
				gug.freight_advance=float(gug.freight_advance)-float(j.final_amount)
				gug.submit()
				val=frappe.db.sql("DELETE FROM `tabPurchase Advance` WHERE table_name='"+str(j.name)+"' AND parent='"+str(j.order_no)+"'")
		elif(self.naming_series=='INV-PAY-'): # for freight advance
			for j in self.final_table:
				gug=frappe.get_doc("Purchase Invoice",j.invoice_no)
				gug.approved_amount=float(gug.approved_amount)-float(j.outstanding_amount)
				gug.submit()
				val=frappe.db.sql("DELETE FROM `tabPurchase Advance` WHERE table_name='"+str(j.name)+"' AND parent='"+str(j.invoice_no)+"'")

# FREIGHT ADVANCE
@frappe.whitelist()
def fp_update_status(go):
	q=frappe.db.sql("SELECT * FROM `tabAdvance Table` INNER JOIN `tabPayment Module` ON `tabPayment Module`.`name`=`tabAdvance Table`.`parent` WHERE `tabAdvance Table`.`order_no`='"+str(go)+"' and `tabAdvance Table`.`docstatus`=0 and `tabPayment Module`.`workflow_state`!='Rejected'",as_dict=1)
	p=frappe.db.sql("SELECT * FROM `tabFreight Table` INNER JOIN `tabPayment Module` ON `tabPayment Module`.`name`=`tabFreight Table`.`parent` WHERE `tabFreight Table`.`order_no`='"+str(go)+"' and `tabFreight Table`.`docstatus`=0 and `tabPayment Module`.`workflow_state`!='Rejected'",as_dict=1)
	if(q):
		frappe.throw("Already this PO NO is linked with payment module. Please finalize the payment then create new one")
	elif(p):
		frappe.throw("Already this PO NO is linked with payment module. Please finalize the payment then create new one")
	else:
		ar=[]
		for i in frappe.db.sql("SELECT name,supplier,base_rounded_total,project FROM `tabPurchase Order` WHERE name='"+str(go)+"' and workflow_state!='Cancelled' and workflow_state!='Rejected'",as_dict=1):
			ar.append({
				"name":i.name,
				"project":i.project,
				"supplier":i.supplier,
				"amount":i.base_rounded_total
			})
	return ar

# FREIGHT ADVANCE
@frappe.whitelist()
def fa_update_items(gok):
	to_python = json.loads(gok)
	lst = []
	item = []
	mr=[]
	v=[]
	for i in to_python:
		if i["transport"] not in lst:
			item.append(i)
			lst.append(i["transport"])
		else:
			item[lst.index(i["transport"])]["amount"] += i["amount"]
			item[lst.index(i["transport"])]["final_amount"] += i["final_amount"]
	v=[]
	for q in item:
		v.append({
			"transport":q['transport'],
			"amount":q['amount'],
			"account_head":q["account_head"],
			"final_amount":q["final_amount"]
			})
	return v

# PAYMENT CONSILiDATE AGINDT PURCHASE INVOIVE
@frappe.whitelist()
def pc_update_status(go,comp):
	ar=[]
	acc='Trade Payables - WTT'
	if(comp=="HARSINI HI TEC"):acc='Trade Payables - HHT'
	for k in frappe.db.sql("SELECT name FROM `tabAccount` WHERE parent_account='"+str(acc)+"' ",as_dict=1):
		for i in frappe.db.sql("SELECT name,status,supplier,posting_date,grand_total,outstanding_amount-approved_amount as outstanding_amount,project FROM `tabPurchase Invoice` WHERE docstatus=1 and is_return=0 and status='Overdue' AND credit_to='"+k.name+"' ORDER BY supplier ASC",as_dict=1):
			today = date.today()
			f_date = datetime.strptime(str(i.posting_date), '%Y-%m-%d')
			l_date = datetime.strptime(str(today), '%Y-%m-%d')
			delta = l_date - f_date
			age=delta.days
			ar.append({
				"name":i.name,
				"project":i.project,
				"supplier":i.supplier,
				"status":i.status,
				"age":age,
				"credit_amount":i.grand_total,
				"outstanding_amount":i.outstanding_amount
			})

		for j in frappe.db.sql("SELECT name,status,supplier,posting_date,grand_total,outstanding_amount-approved_amount as outstanding_amount,project FROM `tabPurchase Invoice` WHERE docstatus=1 and is_return=0 and status='Unpaid' AND credit_to='"+k.name+"' ORDER BY supplier ASC",as_dict=1):
			today1 = date.today()
			f_date1 = datetime.strptime(str(j.posting_date), '%Y-%m-%d')
			l_date1 = datetime.strptime(str(today1), '%Y-%m-%d')
			delta1 = l_date1 - f_date1
			age1=delta1.days
			ar.append({
				"name":j.name,
				"project":j.project,
				"supplier":j.supplier,
				"status":i.status,
				"age":age1,
				"credit_amount":j.grand_total,
				"outstanding_amount":j.outstanding_amount
			})
		for j in frappe.db.sql("SELECT name,status,supplier,posting_date,grand_total,outstanding_amount-approved_amount as outstanding_amount,project FROM `tabPurchase Invoice` WHERE docstatus=1 and is_return=0 and status='Partly Paid' AND credit_to='"+k.name+"' ORDER BY supplier ASC",as_dict=1):
			today2 = date.today()
			f_date2 = datetime.strptime(str(j.posting_date), '%Y-%m-%d')
			l_date2 = datetime.strptime(str(today2), '%Y-%m-%d')
			delta2 = l_date2 - f_date2
			age2=delta2.days
			ar.append({
				"name":j.name,
				"project":j.project,
				"supplier":j.supplier,
				"status":j.status,
				"age":age2,
				"credit_amount":j.grand_total,
				"outstanding_amount":j.outstanding_amount
			})
	return ar

# PAYMENT CONSOLIDATE AGAINST PURCHASE INVOICE
@frappe.whitelist()
def ap_update_items(gok):
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

# ADVANCE PAYMENT AGAINST PURCHASE ORDER
@frappe.whitelist()
def search_po1(go):
	ar=[]
	for i in frappe.db.sql("SELECT name,supplier,transaction_date,base_rounded_total,payment_terms,total_advance FROM `tabPurchase Order` WHERE workflow_state='Approved' and supplier='"+str(go)+"' ",as_dict=1):
		today = date.today()
		f_date = datetime.strptime(str(i.transaction_date), '%Y-%m-%d')
		l_date = datetime.strptime(str(today), '%Y-%m-%d')
		delta = l_date - f_date
		age=delta.days
		if(i.total_advance!=None):
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"age":age,
				"advance":i.payment_terms,
				"amount":i.base_rounded_total,
				"total_advance":i.total_advance
			})
		else:
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"age":age,
				"advance":i.payment_terms,
				"amount":i.base_rounded_total
			})
	return ar

# ADVANCE PAYMENT AGAINST PURCHASE ORDER
@frappe.whitelist()
def search_po2(go):
	q=frappe.db.sql("SELECT * FROM `tabAdvance Table` INNER JOIN `tabPayment Module` ON `tabPayment Module`.`name`=`tabAdvance Table`.`parent` WHERE `tabAdvance Table`.`order_no`='"+str(go)+"' and `tabAdvance Table`.`docstatus`=0 and `tabPayment Module`.`workflow_state`!='Rejected'",as_dict=1)
	p=frappe.db.sql("SELECT * FROM `tabFreight Table` INNER JOIN `tabPayment Module` ON `tabPayment Module`.`name`=`tabFreight Table`.`parent` WHERE `tabFreight Table`.`order_no`='"+str(go)+"' and `tabFreight Table`.`docstatus`=0 and `tabPayment Module`.`workflow_state`!='Rejected'",as_dict=1)
	if(q):
		frappe.throw("Already this PO NO is linked with payment module. Please finalize the payment then create new one")
	elif(p):
		frappe.throw("Already this PO NO is linked with payment module. Please finalize the payment then create new one")
	else:
		ar=[]
		for i in frappe.db.sql("SELECT name,supplier,transaction_date,base_rounded_total,rounded_total,currency,payment_terms,total_advance FROM `tabPurchase Order` WHERE workflow_state='Approved' and name='"+str(go)+"' ",as_dict=1):
			today = date.today()
			f_date = datetime.strptime(str(i.transaction_date), '%Y-%m-%d')
			l_date = datetime.strptime(str(today), '%Y-%m-%d')
			delta = l_date - f_date
			age=delta.days
			if(i.total_advance!=None):
				ar.append({
					"name":i.name,
					"supplier":i.supplier,
					"age":age,
					"advance":i.payment_terms,
					"amount":i.base_rounded_total,
					"total_advance":i.total_advance,
					"total":i.rounded_total,
					"currency":i.currency
				})
			else:
				ar.append({
					"name":i.name,
					"supplier":i.supplier,
					"age":age,
					"advance":i.payment_terms,
					"amount":i.base_rounded_total,
					"total":i.rounded_total,
					"currency":i.currency
				})
	return ar
# ADVANCE PAYMENT AGAINST PURCHASE ORDER
@frappe.whitelist()
def search_po(go,run):
	ar=[]
	for i in frappe.db.sql("SELECT name,supplier,transaction_date,base_rounded_total,rounded_total,currency,payment_terms,total_advance FROM `tabPurchase Order` WHERE workflow_state='Approved' and supplier='"+str(go)+"' or name='"+str(run)+"' ",as_dict=1):
		today = date.today()
		f_date = datetime.strptime(str(i.transaction_date), '%Y-%m-%d')
		l_date = datetime.strptime(str(today), '%Y-%m-%d')
		delta = l_date - f_date
		age=delta.days
		if(i.total_advance!=None):
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"age":age,
				"advance":i.payment_terms,
				"amount":i.base_rounded_total,
				"total_advance":i.total_advance,
				"total":i.rounded_total,
				"currency":i.currency
			})
		else:
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"age":age,
				"advance":i.payment_terms,
				"amount":i.base_rounded_total,
				"total":i.rounded_total,
				"currency":i.currency
			})
	return ar
# ADVANCE PAYMENT AGAINST PURCHASE ORDER
@frappe.whitelist()
def search_all(go):
	ar=[]
	for i in frappe.db.sql("SELECT name,supplier,transaction_date,base_rounded_total,currency,rounded_total,payment_terms,total_advance FROM `tabPurchase Order` WHERE workflow_state='Approved' ",as_dict=1):
		today = date.today()
		f_date = datetime.strptime(str(i.transaction_date), '%Y-%m-%d')
		l_date = datetime.strptime(str(today), '%Y-%m-%d')
		delta = l_date - f_date
		age=delta.days
		if(i.total_advance!=None):
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"age":age,
				"advance":i.payment_terms,
				"amount":i.base_rounded_total,
				"currency":i.currency,
				"total":i.rounded_total,
				"total_advance":i.total_advance
			})
		else:
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"age":age,
				"advance":i.payment_terms,
				"currency":i.currency,
				"total":i.rounded_total,
				"amount":i.base_rounded_total
			})
	return ar
# ADVANCE PAYMENT AGAINST PURCHASE ORDER
@frappe.whitelist()
def searched_item(gok):
	to_python = json.loads(gok)
	item = []
	v=[]
	for i in to_python:
		item.append(i)
	v=[]
	for q in item:
		# v=q["order_no"]
		# sl=v[-5:]
		v.append({
			"order_no":q["order_no"],
			#"po_no":sl,
			"project":frappe.db.get_value("Purchase Order",q["order_no"],"project"),
			"supplier":q['supplier'],
			"age":q["age"],
			"advance":q['advance'],
			"outstanding":q["outstanding"],
			"amount":q['amount'],
			"currency":q['currency'],
			"amount_in_po":q['amount_in_po']
			})
	return v
# ADVANCE PAYMENT AGAINST PURCHASE ORDER
@frappe.whitelist()
def consolidate(gok):
	to_python = json.loads(gok)
	item=[]
	lst = []
	v=[]
	for i in to_python:
		if i["supplier"] not in lst:
			lst.append(i["supplier"])
			item.append(i)
		else:
			item[lst.index(i["supplier"])]["amount"] += i["amount"]
			item[lst.index(i["supplier"])]["final_amount"] += i["final_amount"]
	v=[]
	for q in item:
		v.append({
			"supplier":q['supplier'],
			"amount":q['amount'],
			"final_amount":q["final_amount"]
			})
	return v
@frappe.whitelist()
def lcv_amount(go):
	# v=[]
	g=frappe.get_value("Landed Cost Voucher",go,"total_taxes_and_charges")
	s=frappe.get_value("Landed Cost Voucher",go,"supplier")
	v=[g,s]
	return v

@frappe.whitelist()
def get_pc_bal(act):
	bl=[]
	today_date=date.today()
	aa=today_date
	party_account=act
	bal=get_balance_on(party_account, aa, cost_center=None),
	bl.append({
		"date":today_date.strftime("%d/%m/%y"),
		"balance":bal
		})
	return bl
@frappe.whitelist()
def get_od_bal(act):
	bl=[]
	today_date=date.today()
	aa=today_date
	party_account=act
	bal=get_balance_on(party_account, aa, cost_center=None),
	bl.append({
		"date":today_date.strftime("%d/%m/%y"),
		"balance":bal
		})
	return bl
	
@frappe.whitelist()
def get_ca_bal(act):
	bl=[]
	today_date=date.today()
	aa=today_date
	party_account=act
	bal=get_balance_on(party_account, aa, cost_center=None),
	bl.append({
		"date":today_date.strftime("%d/%m/%y"),
		"balance":bal
		})
	return bl


@frappe.whitelist()
def get_landed_cost_voucher(number):
	ar=[]
	total = frappe.db.get_value("Landed Cost Voucher",number,"total_taxes_and_charges")
	tds = frappe.db.get_value("Landed Cost Voucher",number,"tds_amount")
	amount = frappe.db.get_value("Landed Cost Voucher",number,"amount")
	for i in frappe.db.sql("SELECT receipt_document_type,receipt_document FROM `tabLanded Cost Purchase Receipt` WHERE parent='"+str(number)+"' ",as_dict=1):
		ar.append({
			"voucher_no":i.receipt_document,
			"project":frappe.db.get_value(i.receipt_document_type,i.receipt_document,"project"),
			"supplier":frappe.db.get_value("Landed Cost Taxes and Charges",{"parent":number},"supplier"),
			"total":total,
			"tds":tds,
			"amount":amount
			})
	return ar


@frappe.whitelist()
def get_log_details(log_name):
	ar_log=[]
	for i in frappe.db.sql("SELECT project,project_name,type,supplier,from_warehouse,to_warehouse,reference_doctype,reference_name,terms,rounded_total,bank_account,bank,bank_account_no,account,branch,iban,branch_code,ifsc_code FROM `tabLogistics Module` WHERE name='"+str(log_name)+"'",as_dict=1):
		ar_log.append({
			'project':i.project,
			'project_name':i.project_name,
			'type':i.type,
			'supplier':i.supplier,
			'from_warehouse':i.from_warehouse,
			'to_warehouse':i.to_warehouse,
			'reference_doctype':i.reference_doctype,
			'reference_name':i.reference_name,
			'terms':i.terms,
			'rounded_total':i.rounded_total,
			'log_bank_account':i.bank_account,
			'log_bank':i.bank,
			'log_bank_account_no':i.bank_account_no,
			'log_account':i.account,
			'log_branch':i.branch,
			'log_iban':i.iban,
			'log_branch_code':i.branch_code,
			'log_ifsc_code':i.ifsc_code
		})
	return ar_log
# @frappe.whitelist()
# def set_project(name):
# 	for i in frappe.db.sql("SELECT order_no,name FROM `tabAdvance Table` WHERE parent='"+str(name)+"' ",as_dict=1):
# 		pro = frappe.db.get_value("Purchase Order",str(i.order_no),"project")
# 		frappe.db.sql("UPDATE `tabAdvance Table` SET pro='"+str(pro)+"' WHERE name='"+str(i.name)+"' ")

	# for i in frappe.db.sql("SELECT order_no,name FROM `tabFreight Table` WHERE parent='"+str(name)+"' ",as_dict=1):
	# 	pro = frappe.db.get_value("Purchase Order",str(i.order_no),"project")
	# 	frappe.db.sql("UPDATE `tabFreight Table` SET project='"+str(pro)+"' WHERE name='"+str(i.name)+"' ")
	# 	# frappe.msgprint(str(i.order_no))


@frappe.whitelist()
def update_trans(ref_name):
	ar=[]
	frappe.db.sql("UPDATE `tabPayment Module` SET payment_status='Transferred' WHERE name='"+str(ref_name)+"'")
	return ar

@frappe.whitelist()
def update_inpro(ref_name):
	ar=[]
	frappe.db.sql("UPDATE `tabPayment Module` SET payment_status='In Progress' WHERE name='"+str(ref_name)+"'")
	return ar

@frappe.whitelist()
def update_not(ref_name):
	ar=[]
	frappe.db.sql("UPDATE `tabPayment Module` SET payment_status='Not Transferred' WHERE name='"+str(ref_name)+"'")
	return ar