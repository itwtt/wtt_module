# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.utils import comma_and, cstr, getdate, has_gravatar, nowdate, validate_email_address
from erpnext.controllers.selling_controller import SellingController
from frappe.utils.background_jobs import enqueue

class Inquiries(SellingController):
	pass
# 	def get_feed(self):
# 		return '{0}: {1}'.format(_(self.status), self.lead_name)

# 	def onload(self):
# 		customer = frappe.db.get_value("Customer", {"lead_name": self.name})
# 		self.get("__onload").is_customer = customer
# 		load_address_and_contact(self)

# 	def before_insert(self):
# 		if self.address_title and self.address_type:
# 			self.address_doc = self.create_address()
# 		self.contact_doc = self.create_contact()

# 	def after_insert(self):
# 		self.update_links()

# 	def validate(self):
# 		self.set_prev()
# 		self.title = self.lead_name



# 	def on_update(self):
# 		self.add_calendar_event()
# 		for i in frappe.db.sql("SELECT conversation FROM `tabInquiries Follow up` WHERE parent='"+str(self.name)+"' ORDER BY idx DESC LIMIT 1 ",as_dict=1):
# 			frappe.db.set_value('Inquiries', self.name, 'last_conversation', str(i.conversation),update_modified=False)


# 	def update_links(self):
# 		# update address links
# 		if self.address_title and self.address_line1:
# 			address_fields = ["address_type", "address_title", "address_line1", "address_line2",
# 				"city", "county", "state", "country", "pincode"]
# 			address = frappe.new_doc("Address")
# 			address.address_line1 = self.address_line1
# 			address.address_line2 = self.address_line2
# 			address.address_title = self.address_title
# 			address.address_type = self.address_type
# 			address.city = self.city
# 			address.county = self.county
# 			address.state = self.state
# 			address.country = self.country
# 			address.pincode = self.pincode
# 			address.append("links", {
# 				"link_doctype": "Inquiries",
# 				"link_name": self.name,
# 				"link_title": self.lead_name
# 			})
# 			address.save()

# 		if self.contact_doc:
# 			self.contact_doc.append("links", {
# 				"link_doctype": "Inquiries",
# 				"link_name": self.name,
# 				"link_title": self.lead_name
# 			})
# 			self.contact_doc.save()

# 	def set_prev(self):
# 		if self.is_new():
# 			self._prev = frappe._dict({
# 				"contact_date": None,
# 				"ends_on": None,
# 				"contact_by": None
# 			})
# 		else:
# 			self._prev = frappe.db.get_value("Inquiries", self.name, ["contact_date", "ends_on", "contact_by"], as_dict=1)

# 	def add_calendar_event(self, opts=None, force=False):
# 		super(Inquiries, self).add_calendar_event({
# 			"owner": self.lead_owner,
# 			"starts_on": self.contact_date,
# 			"ends_on": self.ends_on or "",
# 			"subject": ('Contact ' + cstr(self.lead_name) +' - ' + cstr(self.company_name)),
# 			"description": ('Contact ' + cstr(self.lead_name) +' - ' + cstr(self.company_name)) + (self.contact_by and ('. By : ' + cstr(self.contact_by)) or '')
# 		}, force)

# 	def create_address(self):
# 		address_fields = ["address_type", "address_title", "address_line1", "address_line2",
# 			"city", "county", "state", "country", "pincode"]

# 		address=[]

# 		return address

# 	def create_contact(self):
# 		if not self.lead_name:
# 			self.set_lead_name()

# 		names = self.lead_name.strip().split(" ")
# 		if len(names) > 1:
# 			first_name, last_name = names[0], " ".join(names[1:])
# 		else:
# 			first_name, last_name = self.lead_name, None

# 		contact = frappe.new_doc("Contact")
# 		contact.update({
# 			"first_name": first_name,
# 			"last_name": last_name,
# 			"salutation": self.salutation,
# 			"gender": self.gender,
# 			"designation": self.designation,
# 			"company_name": self.company_name,
# 		})

# 		if self.email_id:
# 			contact.append("email_ids", {
# 				"email_id": self.email_id,
# 				"is_primary": 1
# 			})

# 		if self.phone:
# 			contact.append("phone_nos", {
# 				"phone": self.phone,
# 				"is_primary_phone": 1
# 			})

# 		if self.mobile_no:
# 			contact.append("phone_nos", {
# 				"phone": self.mobile_no,
# 				"is_primary_mobile_no":1
# 			})

# 		contact.insert()

# 		return contact
# @frappe.whitelist()
# def make_customer(source_name, target_doc=None):
# 	return _make_customer(source_name, target_doc)


# def _make_customer(source_name, target_doc=None, ignore_permissions=False):
# 	def set_missing_values(source, target):
# 		if source.company_name:
# 			target.customer_type = "Company"
# 			target.customer_name = source.company_name
# 		else:
# 			target.customer_type = "Individual"
# 			target.customer_name = source.lead_name

# 		target.customer_group = frappe.db.get_default("Customer Group")

# 	doclist = get_mapped_doc("Inquiries", source_name,
# 		{"Inquiries": {
# 			"doctype": "Customer",
# 			"field_map": {
# 				"name": "lead_name",
# 				"company_name": "customer_name",
# 				"contact_no": "phone_1",
# 				"fax": "fax_1"
# 			}
# 		}}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

# 	return doclist

# @frappe.whitelist()
# def send_mail(sender,receiver,cc,subject,message):

# 	if receiver:
# 		email_args = {
# 			"reply_to":sender,
# 			"recipients": receiver,
# 			"cc":cc,
# 			"message":message,
# 			"subject": subject
# 			}
# 		if not frappe.flags.in_test:
# 			enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
# 		else:
# 			frappe.sendmail(**email_args)
	
