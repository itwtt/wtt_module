import frappe
@frappe.whitelist()
def getDatas(variety):
	arr=[]
	query=frappe.db.sql("SELECT * FROM `tabRicemill Entries` WHERE docstatus!=2 ",as_dict=1)
	for i in query:
		arr.append(i)
	return arr

@frappe.whitelist()
def updateValues(date,variety,weight,rate,amount,cheque,payment_date,id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.date=date
	doc.variety=variety
	doc.weight=weight
	doc.rate=rate
	doc.amount=amount
	doc.cheque=cheque
	doc.payment_date=payment_date
	doc.save()
	return doc

@frappe.whitelist()
def deleteRecord(id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.delete()
	return doc

@frappe.whitelist()
def createNewRecord(date,variety,weight,rate,amount,cheque,payment_date):
	doc = frappe.new_doc("Ricemill Entries")
	doc.date = date
	doc.variety = variety
	doc.weight = weight
	doc.rate = rate
	doc.amount = amount
	doc.cheque = cheque
	doc.payment_date = payment_date
	doc.save()
	return doc

