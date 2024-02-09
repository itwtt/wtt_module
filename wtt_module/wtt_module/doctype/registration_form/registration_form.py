# Copyright (c) 2021, wtt_custom and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue


class RegistrationForm(Document):
	def validate(self):
		if(self.send_mail==1):
			self.email_salary_slip()
	def email_salary_slip(self):
		receiver = self.email
		message=self.template
		password = None		

		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": message,
				"subject": "Mail Regarding an Interview"
				}
			if not frappe.flags.in_test:
				enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
		else:
			msgprint(_("{0}: Email not found, hence email not sent").format(self.applicant_name))