# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date,timedelta

class Licenserenewal(Document):
	pass



@frappe.whitelist()
def create_license(ss):
	today = date.today()
	sev = today + timedelta(days=8)
	for i in frappe.db.sql("SELECT * FROM `tabLicense renewal` WHERE end_date='"+str(today)+"' ORDER BY end_date DESC LIMIT 1",as_dict=1):
		frappe.msgprint(str(i.end_date))
	# 	doc = frappe.new_doc('License renewal')
	# 	doc.from_date = today
	# 	doc.end_date = sev
	# 	doc.save()
	# return ss