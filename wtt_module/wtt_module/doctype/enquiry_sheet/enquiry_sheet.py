# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.background_jobs import enqueue
import requests

class EnquirySheet(Document):
	pass
	# def validate(self):
	# 	self.email_enq()
	# 	self.receiver()
	# def email_enq(self):
	# 	receiver = self.email_id
	# 	# message="Dear <b>"+str(self.contact_person)+",</b><br>Thanks for considering WTT International Pvt. Ltd. for serving your water treatment related needs.<br>We have received your Enquiry and our representative will reach out to you shortly.<br><br>Thanks & Regards<br>WTT International Pvt. Ltd."
	# 	# message="Dear <b>"+str(self.contact_person)+",</b><br>Thanks for considering WTT International Pvt. Ltd. for serving your water treatment related needs.<br>We have received your Enquiry and our representative will reach out to you shortly.<br><br>Thanks & Regards<br>WTT International Pvt. Ltd."
	# 	message = '<div> Dear '+str(self.contact_person)+',<br><br>Greetings and Good wishes from WTT INTERNATIONAL!!!<br> We are pleased to receive your valuable enquiry through India ITME 2022. We will respond with our techno-commercial proposal at the earliest to fulfill your water treatment needs.<br><br>We are grateful for your consideration of WTT and awaiting to have a great relationship with your esteemed organization.<br><br>Kindly reach us for any other Zero liquid discharge (ZLD), Effluent treatment plant (ETP) & Sewage treatment plant (STP) requirements<br><br>Have a Happy day!!!<br><br>Thanks & Regards<br>Team WTT</div>'
	# 	password = None		

	# 	if receiver:
	# 		email_args = {
	# 			"recipients": [receiver],
	# 			"message": message,
	# 			"subject": "Thanks for the enquiry"
	# 			}
	# 		if not frappe.flags.in_test:
	# 			enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
	# 		else:
	# 			frappe.sendmail(**email_args)
	# 	else:
	# 		msgprint(_("{0}: Email not found, hence email not sent").format(self.contact_person))

	# 	url = "https://www.fast2sms.com/dev/bulkV2"
	# 	payload = "sender_id=WTTINT&message=148895&variables_values="+str(self.contact_person)+"&route=dlt&numbers="+str(self.mobile_number)+""
	# 	headers = {
	# 		'authorization': "WHdjuD5tzVrGeAMsZc6C0x8XKJR9yPwgqv43Uhink172fomIlbjHIvRsA436C2Xr90PW1dgh8x7aNSEt",
	# 		'Content-Type': "application/x-www-form-urlencoded",
	# 		'Cache-Control': "no-cache",
	# 		}

	# 	response = requests.request("POST", url, data=payload, headers=headers)

	# def receiver(self):
	# 	pass
	# 	# receiver = "raghul@wttindia.com"
	# 	# message="Dear Sir,<br>New Enquiry is Received from "+str(self.company_name)+"<br>Kindly Check it."
	# 	# password = None		

	# 	# if receiver:
	# 	# 	email_args = {
	# 	# 		"recipients": [receiver],
	# 	# 		"message": message,
	# 	# 		"subject": "Received Enquiry"
	# 	# 		}
	# 	# 	if not frappe.flags.in_test:
	# 	# 		enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
	# 	# 	else:
	# 	# 		frappe.sendmail(**email_args)
	# 	# else:
	# 	# 	msgprint(_("{0}: Email not found, hence email not sent").format(self.contact_person))
