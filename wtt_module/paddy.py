import frappe
@frappe.whitelist()
def getDatas(variety):
	arr=[]
	query=frappe.db.sql("SELECT * FROM `tabRicemill Entries` WHERE docstatus!=2 ",as_dict=1)
	for i in query:
		arr.append(i)
	return arr

@frappe.whitelist()
def updateValues(date,bags,ton,kg,bags1,ton1,kg1,bill_no,to_be_deposited,godown_expense,lorry_rent,payment_date,id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.date=date
	doc.bags=bags
	doc.ton=ton
	doc.kg=kg
	doc.bags1=bags1
	doc.ton1=ton1
	doc.kg1=kg1
	doc.bill_no=bill_no
	doc.to_be_deposited=to_be_deposited
	doc.godown_expense=godown_expense
	doc.lorry_rent=lorry_rent
	doc.payment_date=payment_date
	doc.save()
	return doc

@frappe.whitelist()
def deleteRecord(id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.delete()
	return doc

@frappe.whitelist()
def createNewRecord(date,bags,ton,kg,bags1,ton1,kg1,bill_no,to_be_deposited,godown_expense,lorry_rent,payment_date):
	doc=frappe.new_doc("Ricemill Entries")
	doc.date=date
	doc.bags=bags
	doc.ton=ton
	doc.kg=kg
	doc.bags1=bags1
	doc.ton1=ton1
	doc.kg1=kg1
	doc.bill_no=bill_no
	doc.to_be_deposited=to_be_deposited
	doc.godown_expense=godown_expense
	doc.lorry_rent=lorry_rent
	doc.payment_date=payment_date
	doc.save()
	return doc

