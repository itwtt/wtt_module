# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue


class NewPlantEnquiry(Document):
	def validate(self):
		self.email_new_enq()
		self.receiver()
	def email_new_enq(self):
		receiver = self.email
		message="Dear <b>"+str(self.reference)+",</b><br>Thanks for considering WTT International Pvt. Ltd. for serving your water treatment related needs.<br>We have received your Enquiry and our representative will reach out to you shortly.<br><br>Thanks & Regards<br>WTT International Pvt. Ltd."
		password = None		

		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": message,
				"subject": "Thanks for the enquiry"
				}
			if not frappe.flags.in_test:
				enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
		else:
			frappe.msgprint(("{0}: Email not found, hence email not sent").format(self.reference))

	def receiver(self):
		receiver = "raghul@wttindia.com"
		message="Dear Sir,<br>New Enquiry is Received from "+str(self.industry_name)+"<br>Kindly Check it."
		password = None		

		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": message,
				"subject": "Received Enquiry"
				}
			if not frappe.flags.in_test:
				enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
		else:
			frappe.msgprint(("{0}: Email not found, hence email not sent").format(self.reference))
