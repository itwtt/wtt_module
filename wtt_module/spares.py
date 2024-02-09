import frappe
@frappe.whitelist()
def getDatas(variety):
	arr=[]
	query=frappe.db.sql("SELECT * FROM `tabRicemill Entries` WHERE docstatus!=2 ",as_dict=1)
	for i in query:
		arr.append(i)
	return arr

@frappe.whitelist()
def updateValues(date,particulars,from_whom,qty,amount,payment_mode,paid_on,gst_amount,id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.date=date
	doc.particulars=particulars
	doc.from_whom=from_whom
	doc.qty=qty
	doc.amount=amount
	doc.payment_mode=payment_mode
	doc.paid_on=paid_on
	doc.gst_amount = gst_amount
	doc.save()
	return doc

@frappe.whitelist()
def deleteRecord(id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.delete()
	return doc

@frappe.whitelist()
def createNewRecord(date,particulars,from_whom,qty,amount,payment_mode,paid_on,gst_amount):
	doc = frappe.new_doc("Ricemill Entries")
	doc.date = date
	doc.particulars = particulars
	doc.from_whom = from_whom
	doc.qty = qty
	doc.amount = amount
	doc.payment_mode = payment_mode
	doc.paid_on = paid_on
	doc.gst_amount = gst_amount
	doc.save()
	return doc

