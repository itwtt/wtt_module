# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SentEnquiry(Document):
	pass


@frappe.whitelist()
def club_items(doc):
	query = frappe.db.sql("SELECT distinct(item_code)as item_code,item_name,description,technical_description,sum(qty)as qty,uom FROM `tabMaterials Table` where parent='"+str(doc)+"' GROUP BY item_code ",as_dict=1)
	rfq=frappe.get_doc("Sent Enquiry",str(doc))
	rfq.enquiry_materials=[]
	for i in query:
		rfq.append("enquiry_materials",i)
	rfq.save()

	return rfq
		

@frappe.whitelist()
def fill_web_form(enquiry):
	ar=[]
	arr=[]
	project=frappe.db.get_value("Sent Enquiry",str(enquiry),'project')
	for i in frappe.db.sql("SELECT item_code,item_name,description,technical_description,qty,uom,0 as rate,0 as amount,'-'as supplier_description FROM `tabEnquiry Materials` where parent='"+str(enquiry)+"' ",as_dict=1):
		ar.append(i)
	return ar,project