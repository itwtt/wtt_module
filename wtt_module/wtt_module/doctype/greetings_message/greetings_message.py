# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue

class GreetingsMessage(Document):
	def validate(self):
		if(self.message_status):
			pass
		else:
			self.email_salary_slip()
	def email_salary_slip(self):
		self.message_status="Sent"
		receiver = self.email_id
		message="Dear "+self.employee_name+",<br>A warm welcome from the whole team here at WTT INTERNATIONAL PVT LTD,<br>We’re so happy to have you on board with our team.<br>Congratulations and best wishes on your first day<br><br> Your Details:<br> Name: "+self.employee_name+"<br>Department: "+self.department+"<br>Designation: "+self.designation+"<br>System User ID: "+self.system_user_id+"<br>System Password: "+self.system_password+"<br>ERP Link: "+self.erp_link+"<br>ERP Username: "+self.erp_username+"<br>ERP Password: "+self.erp_password+""
		password = None		

		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": message,
				"subject": "Welcome to our Team"
				}
			if not frappe.flags.in_test:
				enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
		else:
			msgprint(_("{0}: Email not found, hence email not sent").format(self.applicant_name))

		frappe.msgprint("Email Sent Successfully..")
