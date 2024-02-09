# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from datetime import date

class FreightAdvance(Document):
	def validate(self):
		for i in self.freight_table:
			if(float(i.amount)<float(i.final_amount)):
				frappe.throw('Advance Amount not Greater than PO Amount')
			else:
				pass
				
	def on_submit(self):
		for i in self.freight_table:
			gug=frappe.get_doc("Purchase Order",i.order_no)
			gug.append("purchase_advance",{
				"type":"Freight Advance",
				"paid_date":date.today(),
				"advance_type":str(i.account_head)+"-"+str(i.transport),
				"percentage":'-',
				"paid_amount":i.final_amount,
				"table_name":i.name
				})
			gug.freight_advance=float(gug.freight_advance)+float(i.final_amount)
			gug.submit()

		for i in freight_table:
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
		for j in self.freight_table:
			gug=frappe.get_doc("Purchase Order",j.order_no)
			gug.freight_advance=float(gug.freight_advance)-float(j.final_amount)
			gug.submit()
			val=frappe.db.sql("DELETE FROM `tabPurchase Advance` WHERE table_name='"+str(j.name)+"' AND parent='"+str(j.order_no)+"'")


@frappe.whitelist()
def update_status(go):
	ar=[]
	for i in frappe.db.sql("SELECT name,supplier,grand_total FROM `tabPurchase Order` WHERE name='"+str(go)+"' and workflow_state!='Cancelled' and workflow_state!='Rejected'",as_dict=1):
		ar.append({
			"name":i.name,
			"supplier":i.supplier,
			"amount":i.grand_total
		})
	return ar

@frappe.whitelist()
def update_items(gok):
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