import frappe
@frappe.whitelist(allow_guest=True)
def getemp(emp):
	arr=[]
	query=frappe.db.sql("SELECT employee_name,department FROM `tabEmployee` WHERE name="+str(emp)+"",as_dict=1)
	for i in query:
		arr.append(i)
	return arr