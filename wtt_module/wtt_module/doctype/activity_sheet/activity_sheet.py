# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from datetime import date,datetime,timedelta
from pytz import timezone
from frappe.utils.background_jobs import enqueue
from frappe.model.document import Document


class ActivitySheet(Document):
	def on_submit(self):
		if(self.employee=="WTT1387"):
			message="Today Activities: (SUNITA A) "+str(self.date)+"<br><br><table border=1 style='border-collapse: collapse'>"
			for i in self.get('activity'):
				dd1 = datetime.strptime(str(i.from_time), '%Y-%m-%d %H:%M:%S')
				dd2 = datetime.strptime(str(i.to_time), '%Y-%m-%d %H:%M:%S')
				message+="<tr><td width='70%'>"+str(i.activity_type)+"</td><td width='10%'>"+str(dd1.time())+"</td><td width='10%'>"+str(dd2.time())+"</td><td width='10%'>"+str(round(i.hours,2))+"</td></tr>"
			
			s=0
			for i in self.get('activity'):
				s += float(i.hours)

			message+="</table><br>"
			message+="Total Hours: "+str(round(s,2))
			
			email_args = {
				"reply_to":"trading@wttindia.com",
				"recipients": "trading@wttindia.com",
				"cc":"purchase@wttindia.com",
				"message":message,
				"subject": "Activities"
				}
			if not frappe.flags.in_test:
				enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
