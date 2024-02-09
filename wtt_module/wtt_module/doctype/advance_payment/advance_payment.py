# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from datetime import datetime
from datetime import date

class AdvancePayment(Document):
	def validate(self):
		for i in self.advance_table:
			if(float(i.amount)<float(i.final_amount)):
				frappe.throw('Advance Amount not Greater than PO Amount')
			else:
				pass
		if(self.workflow_state=='Approved by HOD'):
			for i in self.advance_table:
				gug=frappe.get_doc("Purchase Order",i.order_no)
				gug.submit()
				
	def on_submit(self):
		for i in self.advance_table:
			gug=frappe.get_doc("Purchase Order",i.order_no)
			gug.append("purchase_advance",{
				"type":"Advance Payment",
				"paid_date":date.today(),
				"advance_type":i.advance,
				"percentage":i.percentage,
				"paid_amount":i.final_amount,
				"table_name":i.name
				})
			gug.total_advance=float(gug.total_advance)+float(i.final_amount)
			gug.submit()

		for i in advance_table:
			doc=frappe.new_doc("Payment Entry")
			doc.payment_type='Pay'
			doc.mode_of_payment='NEFT/RTGS/IMPS'
			doc.party_type='Supplier'
			doc.party=i.supplier
			doc.paid_amount=i.final_amount
			doc.append("references",{
				"reference_doctype":"Purchase Order",
				"reference_name":i.order_no,
				"allocated_amount":i.final_amount
				})
			doc.reference_no='000000'
			doc.reference_date=date.today()
			doc.save()
			frappe.db.commit()

	
	def on_cancel(self):
		for j in self.advance_table:
			gug=frappe.get_doc("Purchase Order",j.order_no)
			gug.total_advance=float(gug.total_advance)-float(j.final_amount)
			gug.submit()
			val=frappe.db.sql("DELETE FROM `tabPurchase Advance` WHERE table_name='"+str(j.name)+"' AND parent='"+str(j.order_no)+"'")


@frappe.whitelist()
def update_status(go):
	ar=[]
	for i in frappe.db.sql("SELECT name,supplier,transaction_date,grand_total,payment_terms FROM `tabPurchase Order` WHERE workflow_state!='Cancelled' and workflow_state!='Rejected' ORDER BY supplier ASC",as_dict=1):
		today = date.today()
		f_date = datetime.strptime(str(i.transaction_date), '%Y-%m-%d')
		l_date = datetime.strptime(str(today), '%Y-%m-%d')
		delta = l_date - f_date
		age=delta.days
		ar.append({
			"name":i.name,
			"supplier":i.supplier,
			"age":age,
			"advance":i.payment_terms,
			"amount":i.grand_total
		})
	return ar

# @frappe.whitelist()
# def update_items(gok):
# 	to_python = json.loads(gok)
# 	lst = []
# 	item = []
# 	mr=[]
# 	v=[]
# 	for i in to_python:
# 		if i["supplier"] not in lst:
# 			item.append(i)
# 			lst.append(i["supplier"])
# 			lst.append()
# 		else:
# 			item[lst.index(i["supplier"])]["amount"] += flt(i["amount"])
# 			item[lst.index(i["supplier"])]["final_amount"] += flt(i["final_amount"])
# 	v=[]
# 	for q in item:
# 		v.append({
# 			"supplier":q['supplier'],
# 			"amount":q['amount'],
# 			"final_amount":q["final_amount"]
# 			})
# 	return v
@frappe.whitelist()
def search_po1(go):
	ar=[]
	for i in frappe.db.sql("SELECT name,supplier,transaction_date,grand_total,payment_terms,total_advance FROM `tabPurchase Order` WHERE workflow_state!='Cancelled' and workflow_state!='Rejected' and supplier='"+str(go)+"' ",as_dict=1):
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
				"amount":i.grand_total,
				"total_advance":i.total_advance
			})
		else:
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"age":age,
				"advance":i.payment_terms,
				"amount":i.grand_total
			})
	return ar
@frappe.whitelist()
def search_po2(go):
	ar=[]
	for i in frappe.db.sql("SELECT name,supplier,transaction_date,grand_total,payment_terms,total_advance FROM `tabPurchase Order` WHERE workflow_state!='Cancelled' and workflow_state!='Rejected' and name='"+str(go)+"' ",as_dict=1):
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
				"amount":i.grand_total,
				"total_advance":i.total_advance
			})
		else:
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"age":age,
				"advance":i.payment_terms,
				"amount":i.grand_total
			})
	return ar
@frappe.whitelist()
def search_po(go,run):
	ar=[]
	for i in frappe.db.sql("SELECT name,supplier,transaction_date,grand_total,payment_terms,total_advance FROM `tabPurchase Order` WHERE workflow_state!='Cancelled' and workflow_state!='Rejected' and supplier='"+str(go)+"' or name='"+str(run)+"' ",as_dict=1):
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
				"amount":i.grand_total,
				"total_advance":i.total_advance
			})
		else:
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"age":age,
				"advance":i.payment_terms,
				"amount":i.grand_total
			})
	return ar

@frappe.whitelist()
def search_all(go):
	ar=[]
	for i in frappe.db.sql("SELECT name,supplier,transaction_date,grand_total,payment_terms,total_advance FROM `tabPurchase Order` WHERE workflow_state!='Cancelled' and workflow_state!='Rejected' ",as_dict=1):
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
				"amount":i.grand_total,
				"total_advance":i.total_advance
			})
		else:
			ar.append({
				"name":i.name,
				"supplier":i.supplier,
				"age":age,
				"advance":i.payment_terms,
				"amount":i.grand_total
			})
	return ar

@frappe.whitelist()
def searched_item(gok):
	to_python = json.loads(gok)
	item = []
	v=[]
	for i in to_python:
		item.append(i)
	v=[]
	for q in item:
		v.append({
			"order_no":q["order_no"],
			"supplier":q['supplier'],
			"age":q["age"],
			"advance":q['advance'],
			"amount":q['amount']
			})
	return v

@frappe.whitelist()
def consolidate(gok):
	to_python = json.loads(gok)
	item=[]
	lst = []
	v=[]
	# for i in to_python:
	# 	if i["supplier"] in lst:
	# 		data[lst.index(i["supplier"])]["amount"]+=i["amount"]
	# 		data[lst.index(i["supplier"])]["final_amount"]+=i["final_amount"]
	# 	else:
	# 		lst.append(i["supplier"])
	# 		data.append({
	# 			"supplier": i["supplier"],
	# 			"amount": i["amount"],
	# 			"final_amount": i["final_amount"]
	# 		})
	# for q in data:
	# 	v.append({
	# 		"supplier":q['supplier'],
	# 		"amount":q['amount'],
	# 		"final_amount":q["final_amount"]
	# 		})
	# return v
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