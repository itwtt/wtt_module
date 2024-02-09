# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class PartyDetails(Document):
	def validate(self,target_doc=None):
		if(self.create==1):
			if(self.party_type=="Supplier"):
				source_name = self.name
				def postprocess(source, target_doc):
					pass
				doclist = get_mapped_doc("Party Details", source_name, {
					"Party Details": {
						"doctype": "Supplier",
						"validation": {
							"docstatus": ["=", 0]
						},
						"field_map": {
							"party_name": "supplier_name"
						}
					}
				}, target_doc, postprocess)
				doclist.pan=self.pan
				doclist.save()
				frappe.msgprint("Supplier Created")
				frappe.msgprint("Bank Account Linked")


			elif(self.party_type=="Customer"):
				source_name = self.name
				def postprocess(source, target_doc):
					pass
				doclist = get_mapped_doc("Party Details", source_name, {
					"Party Details": {
						"doctype": "Customer",
						"validation": {
							"docstatus": ["=", 0]
						},
						"field_map": {
							"party_name": "customer_name"
						}
					}
				}, target_doc, postprocess)
				doclist.save()
				frappe.msgprint("Customer Created")

				doclist2 = get_mapped_doc("Party Details", source_name, {
					"Party Details": {
						"doctype": "Bank Account",
						"validation": {
							"docstatus": ["=", 0]
						}
					}
				}, target_doc, postprocess)
				doclist2.account_name = self.party_name
				doclist2.party=self.party_name
				doclist2.save()
				frappe.msgprint("Bank Account Linked")

		
			source_name = self.name
			def postprocess(source, target_doc):
				pass
			###########Address################################
			doclist = get_mapped_doc("Party Details", source_name, {
				"Party Details": {
					"doctype": "Address",
					"validation": {
						"docstatus": ["=", 0]
					}
				}
			}, target_doc, postprocess)
			doclist.append("links",{
				"link_doctype":self.party_type,
				"link_name":self.party_name
				})
			doclist.save()
			frappe.msgprint("Address Created")
			############Contact################################
			doclist2 = get_mapped_doc("Party Details", source_name, {
				"Party Details": {
					"doctype": "Contact",
					"validation": {
						"docstatus": ["=", 0]
					}
				}
			}, target_doc, postprocess)
			doclist2.append("links",{
				"link_doctype":self.party_type,
				"link_name":self.party_name
				})
			doclist2.save()
			frappe.msgprint("Contact Created")