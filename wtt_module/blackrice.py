import frappe
@frappe.whitelist()
def getDatas(variety):
	arr=[]
	query=frappe.db.sql("SELECT * FROM `tabRicemill Entries` WHERE docstatus!=2 ",as_dict=1)
	for i in query:
		arr.append(i)
	return arr

@frappe.whitelist()
def updateValues(date,rate,no_of_bags,weight,amount,received_date,bank_name,id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.date=date
	doc.rate=rate
	doc.no_of_bags=no_of_bags
	doc.weight=weight
	doc.amount=amount
	doc.received_date=received_date
	doc.bank_name=bank_name
	doc.save()
	return doc

@frappe.whitelist()
def deleteRecord(id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.delete()
	return doc

@frappe.whitelist()
def createNewRecord(date,rate,no_of_bags,weight,amount,received_date,bank_name):
	doc = frappe.new_doc("Ricemill Entries")
	doc.date = date
	doc.rate = rate
	doc.no_of_bags = no_of_bags
	doc.weight = weight
	doc.amount = amount
	doc.received_date = received_date
	doc.bank_name = bank_name
	doc.save()
	return doc

