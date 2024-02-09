# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from frappe.utils.pdf import get_pdf,cleanup
from PyPDF2 import PdfFileWriter, PdfFileReader

class PartyName(Document):
	pass


@frappe.whitelist()
def update_supplier(supplier_name,country,tax_id,tax_category,supplier_group,supplier_type,gst_category,pan,iban,bank,ifsc_code,branch,branch_code,bank_account_no):
	if(pan!=None and iban!=None):
		doc=frappe.new_doc("Supplier")
		doc.supplier_name=supplier_name
		doc.country=country
		doc.tax_id=tax_id
		doc.tax_category=tax_category
		doc.supplier_group=supplier_group
		doc.supplier_type=supplier_type
		doc.gst_category=gst_category
		doc.pan=pan
		doc.iban=iban
		doc.bank=bank
		doc.ifsc_code=ifsc_code
		doc.branch=branch
		doc.branch_code=branch_code
		doc.bank_account_no=bank_account_no
		doc.append('accounts',{
			"company":"W.t.t technology Services India Pvt Ltd",
			"account":"Trade Payables - WTT"
			})
		doc.save()

	return supplier_name
@frappe.whitelist()
def update_customer(customer_name,territory,type1,customer_group,tax_id,tax_category,gst_category,pan,iban,bank,ifsc_code,branch,branch_code,bank_account_no):
	if(pan!=None and iban!=None):
		doc=frappe.new_doc("Customer")
		doc.customer_name=customer_name
		doc.territory=territory
		doc.type=type1
		doc.tax_id=tax_id
		doc.customer_group=customer_group
		doc.tax_category=tax_category
		doc.gst_category=gst_category
		doc.pan=pan
		doc.iban=iban
		doc.bank=bank
		doc.ifsc_code=ifsc_code
		doc.branch=branch
		doc.branch_code=branch_code
		doc.bank_account_no=bank_account_no
		doc.save()

	return customer_name

@frappe.whitelist()
def update_address(address_title,address_type,address_line1,address_line2,city,state,address_country,pincode,ars):
	if(address_title!=None and address_type!=None and address_line1!=None and address_line2!=None and city!=None and state!=None and address_country!=None and pincode!=None and ars!=None):
		to_python = json.loads(ars)
		item = []
		doc=frappe.new_doc("Address")
		doc.address_title=address_title
		doc.address_type=address_type
		doc.address_line1=address_line1
		doc.address_line2=address_line2
		doc.city=city
		doc.state=state
		doc.address_country=address_country
		doc.pincode=pincode
		for i in to_python:
			doc.append("links",i)
		doc.save()

@frappe.whitelist()
def update_contact(first_name,middle_name,last_name,email_id,user,address,status,salutation,designation,gender,phone,mobile_no,company_name,email_ids,contact_nos,links,is_primary_contact):
	if(first_name!=None and middle_name!=None and last_name!=None and email_id!=None and user!=None and address!=None and salutation!=None and designation!=None and gender!=None and phone!=None and mobile_no!=None and company_name!=None):
		ar1=json.loads(email_ids)
		ar2=json.loads(contact_nos)
		ar3=json.loads(links)
		doc=frappe.new_doc("Contact")
		doc.first_name=first_name
		doc.middle_name=middle_name
		doc.last_name=last_name
		doc.email_id=email_id
		doc.user=user
		doc.address=address
		doc.status=status
		doc.salutation=salutation
		doc.designation=designation
		doc.gender=gender
		doc.phone=phone
		doc.mobile_no=mobile_no
		doc.company_name=company_name
		for i in ar1:
			doc.append("email_ids",i)
		for i in ar2:
			doc.append("phone_nos",i)
		for i in ar3:
			doc.append("links",i)
		doc.is_primary_contact=is_primary_contact
		doc.save()
		frappe.msgprint("done")



@frappe.whitelist()
def download_pdf(doctype, name, format=None, doc=None, no_letterhead=0):
	html = frappe.get_print(doctype, name, format, doc=doc, no_letterhead=no_letterhead)
	frappe.local.response.filename = "{name}.pdf".format(name=name.replace(" ", "-").replace("/", "-"))
	frappe.local.response.filecontent = get_pdf(html)
	frappe.local.response.type = "download"


frappe.whitelist()
def create_supplier(supplier_name,gst_category,tax_id,pan,supplier_group,supplier_type,bank,ifsc_code,branch,bank_account_no,adress_title,address_type,address_line1,address_line2,city,country,postal_code,first_name,last_name,party_gstin,is_billing_contact,is_primary_contact,company_name,mobile_no,email_id,phone):
	doc1=frappe.new_doc("Supplier")
	doc1.supplier_name=supplier_name
	doc1.country=country
	doc1.tax_id=tax_id
	doc1.tax_category=tax_category
	doc1.supplier_group=supplier_group
	doc1.supplier_type=supplier_type
	doc1.gst_category=gst_category
	doc1.pan=pan
	doc1.bank=bank
	doc1.ifsc_code=ifsc_code
	doc1.branch=branch
	doc1.bank_account_no=bank_account_no
	doc1.append('accounts',{
		"company":"W.t.t technology Services India Pvt Ltd",
		"account":"Trade Payables - WTT"
		})
	doc1.save()

	doc2=frappe.new_doc("Address")
	doc2.address_title=address_title
	doc2.address_type=address_type
	doc2.address_line1=address_line1
	doc2.address_line2=address_line2
	doc2.city=city
	doc2.country=country
	doc2.address_country=address_country
	doc2.postal_code=postal_code
	doc2.save()

	doc=frappe.new_doc("Contact")
	doc.first_name=first_name
	doc.middle_name=middle_name
	doc.last_name=last_name
	doc.party_gstin=party_gstin
	doc.email_id=email_id
	doc.phone=phone
	doc.mobile_no=mobile_no
	doc.company_name=company_name
	doc.is_billing_contact=is_billing_contact
	doc.is_primary_contact=is_primary_contact
	doc.save()
