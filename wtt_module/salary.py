import frappe
@frappe.whitelist()
def getDatas(variety):
	arr=[]
	query=frappe.db.sql("SELECT * FROM `tabRicemill Entries` WHERE docstatus!=2 ",as_dict=1)
	for i in query:
		arr.append(i)
	return arr

@frappe.whitelist()
def updateValues(date,employee_name,no_of_working_days,per_day_salary,amount,paid_on,id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.date=date
	doc.employee_name=employee_name
	doc.no_of_working_days=no_of_working_days
	doc.per_day_salary=per_day_salary
	doc.amount=amount
	doc.paid_on=paid_on
	doc.save()
	return doc

@frappe.whitelist()
def deleteRecord(id_name):
	doc=frappe.get_doc("Ricemill Entries",str(id_name))
	doc.delete()
	return doc

@frappe.whitelist()
def createNewRecord(date,employee_name,no_of_working_days,per_day_salary,amount,paid_on):
	doc = frappe.new_doc("Ricemill Entries")
	doc.date = date
	doc.employee_name = employee_name
	doc.no_of_working_days = no_of_working_days
	doc.per_day_salary = per_day_salary
	doc.amount = amount
	doc.paid_on = paid_on
	doc.save()
	return doc

