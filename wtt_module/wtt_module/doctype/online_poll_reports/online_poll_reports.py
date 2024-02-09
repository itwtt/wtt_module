# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OnlinePollReports(Document):
	pass
@frappe.whitelist()
def poll_report(aa):
	arr=[]
	arr2=[]
	query1=frappe.db.sql("SELECT name1,mobile_can_allowed_or_not,feedback FROM `tabOnline Poll` Where name1!='None' ",as_dict=1)
	for i in query1:

		
		arr.append({
			"emp":i.name1,
			"mob":i.mobile_can_allowed_or_not,
			"sug":i.feedback
			})
		
	return arr