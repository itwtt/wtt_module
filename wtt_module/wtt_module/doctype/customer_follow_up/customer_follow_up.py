# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from datetime import date,datetime,timedelta
from frappe.model.document import Document

class CustomerFollowUp(Document):
	pass

@frappe.whitelist()
def get_lead(obj):
	ar=[]
	for i in frappe.db.sql("SELECT fu.name,fu.parent,fu.date,fu.conversation,ll.organization,ll.location,fu.remarks.fu.result,ll.contact_date FROM `tabLead`as ll,`tabFollow Up`as fu WHERE ll.name=fu.parent and ll.status='"+str(obj)+"' ",as_dict=1):
		ar.append(i)
	return arr
