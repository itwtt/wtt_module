import frappe
@frappe.whitelist(allow_guest=True)
def getitems():
	arr=[]
	query=frappe.db.sql("SELECT * FROM `tabItem` WHERE docstatus!=2 and item='SCF96.6M3/HR4BAR35-40C50M6TO8NILLSS316STSTEWVORFASME'",as_dict=1)
	for i in query:
		arr.append(i)
	return arr
