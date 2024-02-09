import frappe
@frappe.whitelist()
def getDatas(variety):
	arr=[]
	query=frappe.db.sql("SELECT * FROM `tabRicemill Entries` WHERE docstatus!=2 ",as_dict=1)
	for i in query:
		arr.append({
			"id":i.name,
			"date":i.date,
			"vehicle_no":i.vehicle_no,
			"weight":i.net_weight
			})
	return arr

@frappe.whitelist()
def updateValues(date,weight,vehicle_no,id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.date=date
	doc.net_weight=weight
	doc.vehicle_no=vehicle_no
	doc.save()
	return doc

@frappe.whitelist()
def deleteRecord(id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.delete()
	return doc

@frappe.whitelist()
def createNewRecord(date,weight,vehicle_no):
	doc = frappe.new_doc("Ricemill Entries")
	doc.date = date
	doc.net_weight = weight
	doc.vehicle_no = vehicle_no
	doc.save()
	return doc

