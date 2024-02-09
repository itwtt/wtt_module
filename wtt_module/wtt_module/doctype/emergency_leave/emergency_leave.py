# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from datetime import date,datetime,timedelta
from frappe.model.document import Document

class EmergencyLeave(Document):
	def validate(self):
		mr=[]
		temp_list=[]
		val=0
		for i in self.leave_table:
			if(i.status!='Rejected'):
				val=val+i.no_of_days
		for i in self.leave_table:
			if(i.status!='Rejected'):
				d = datetime.strptime(str(i.from_date), '%Y-%m-%d')
				e = datetime.strptime(str(i.to_date), '%Y-%m-%d')
				v=date.strftime(d,"%d-%m")
				u=date.strftime(e,"%d-%m")
				temp_list.append(str(v))
		unique_item = set(temp_list)

		for j in unique_item:
			mr.append(j)

		str1 = ','.join(str(e) for e in mr)

		self.date=str1
