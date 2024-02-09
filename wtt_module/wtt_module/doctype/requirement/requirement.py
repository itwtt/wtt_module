# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue


class Requirement(Document):
	def validate(self):
		message="Greetings and Good wishes from WTT INTERNATIONAL!<br><br>With immense pleasure we share with you that, “WTT INTERNATIONAL” will exhibiting at INDIA ITME Exhibition 2022, held from 08th to 13th of December 2022 at India Exposition Mart Ltd, (IEML) Greater Noida.<br>We are delighted to present our innovative technologies to fulfill you water treatment needs.<br>"
		message+="Grand launch of our newest upgraded technology to meet your water treatment requirements.<br>"
		message+="WTT INTERNATIONAL proudly presents CaRe system.<br><br>It is our pleasure and privilege to invite you to join us.<br>Hall No: H7A<br>Stall No: H7AC4<br>We hope to see you at the India ITME 2022."
		password = None
		email_args = {
			"sender":"raghul@wttindia.com",
			"recipients": [self.email],
			"message": message,
			"subject": "Invitation from WTT INTERNATIONAL exhibition"
			}
		if not frappe.flags.in_test:
			enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
		else:
			frappe.sendmail(**email_args)
			
@frappe.whitelist()
def funct():
	frappe.msgprint("test")
