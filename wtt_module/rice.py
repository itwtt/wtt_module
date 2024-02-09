import frappe
@frappe.whitelist()
def getDatas(variety):
	arr=[]
	query=frappe.db.sql("SELECT * FROM `tabRicemill Entries` WHERE docstatus!=2 ",as_dict=1)
	for i in query:
		arr.append(i)
	return arr

@frappe.whitelist()
def updateValues(date,bags,ton,kg,bags1,ton1,kg1,bags2,ton2,kg2,godown,purchase,total,payment_date,rent,paid_on,id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.date=date
	doc.bags=bags
	doc.ton=ton
	doc.kg=kg
	doc.bags1=bags1
	doc.ton1=ton1
	doc.kg1=kg1
	doc.bags2=bags2
	doc.ton2=ton2
	doc.kg2=kg2
	doc.godown=godown
	doc.purchase=purchase
	doc.total=total
	doc.payment_date=payment_date
	doc.rent=rent
	doc.paid_on=paid_on
	doc.save()
	return doc

@frappe.whitelist()
def deleteRecord(id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.delete()
	return doc

@frappe.whitelist()
def createNewRecord(date,bags,ton,kg,bags1,ton1,kg1,bags2,ton2,kg2,godown,purchase,total,payment_date,rent,paid_on):
	doc=frappe.new_doc("Ricemill Entries")
	doc.date=date
	doc.bags=bags
	doc.ton=ton
	doc.kg=kg
	doc.bags1=bags1
	doc.ton1=ton1
	doc.kg1=kg1
	doc.bags2=bags2
	doc.ton2=ton2
	doc.kg2=kg2
	doc.godown=godown
	doc.purchase=purchase
	doc.total=total
	doc.payment_date=payment_date
	doc.rent=rent
	doc.paid_on=paid_on
	doc.save()
	return doc

