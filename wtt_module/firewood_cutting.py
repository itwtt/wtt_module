import frappe
@frappe.whitelist()
def getDatas(variety):
	arr=[]
	query=frappe.db.sql("SELECT * FROM `tabRicemill Entries` WHERE docstatus!=2 ",as_dict=1)
	for i in query:
		arr.append(i)
	return arr

@frappe.whitelist()
def updateValues(date,ton,hours,amount,payment_date,mode_of_payment,id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.date=date
	doc.ton=ton
	doc.hours=hours
	doc.amount=amount
	doc.payment_date=payment_date
	doc.mode_of_payment=mode_of_payment
	doc.save()
	return doc

@frappe.whitelist()
def deleteRecord(id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.delete()
	return doc

@frappe.whitelist()
def createNewRecord(date,ton,hours,amount,payment_date,mode_of_payment):
	doc = frappe.new_doc("Ricemill Entries")
	doc.date = date
	doc.ton = ton
	doc.hours = hours
	doc.amount = amount
	doc.payment_date = payment_date
	doc.mode_of_payment = mode_of_payment
	doc.save()
	return doc

