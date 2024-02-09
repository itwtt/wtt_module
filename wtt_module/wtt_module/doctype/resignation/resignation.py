# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date,datetime,timedelta
from pytz import timezone
from frappe.utils.background_jobs import enqueue

class Resignation(Document):
	def validate(self):
		pass
	# @frappe.whitelist()
	# def send_mail(self):
	# 	recipients_=[]
	# 	cc_=[]
	# 	for i in self.to:
	# 		recipients_.append(i.user)
	# 	for j in self.cc:
	# 		cc_.append(j.user)
	# 	msg=self.message
	# 	message=self.message+'<br><br><br>https://erp.wttindia.com/app/resignation/'+str(self.name)
	# 	password = None
	# 	email_args = {
	# 		"sender":frappe.session.user,
	# 		"recipients": self.sender,
	# 		"cc":cc_,
	# 		"message": message,
	# 		"subject": self.subject
	# 		}
	# 	frappe.sendmail(**email_args)

	# 	self.append("conversation",{
	# 		"from":frappe.db.get_value("User",frappe.session.user,"full_name"),
	# 		"time":datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),
	# 		"conversations":"Subject: "+self.subject+"<br>"+msg
	# 		})
	# 	self.workflow_state="Sent"
	# @frappe.whitelist()
	# def reply_mail(self):
	# 	recipients_=[]
	# 	for i in self.to:
	# 		recipients_.append(i.user)
	# 	msg=self.message
	# 	message=self.message+'<br><br><br>https://erp.wttindia.com/app/resignation/'+str(self.name)
	# 	password = None
	# 	email_args = {
	# 		"sender":frappe.session.user,
	# 		"recipients": self.sender,
	# 		"message": message,
	# 		"subject": self.subject
	# 		}
	# 	frappe.sendmail(**email_args)

	# 	self.append("conversation",{
	# 		"from":frappe.db.get_value("User",frappe.session.user,"full_name"),
	# 		"time":datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'),
	# 		"conversations":"Subject: "+self.subject+"<br>"+msg
	# 		})
	# 	if(self.workflow_state=="Sent"):
	# 		self.workflow_state="Replied"



