# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime,date,timedelta

class DesignActivity(Document):
	def validate(self):
		aa=[]
		bb=[]
		for i in self.activities:
			aa.append(i.from_time)
			bb.append(i.to_time)
		t1=min(aa)
		t2=max(bb)

		date_to_str = '%Y-%m-%d %H:%M:%S'
		start = datetime.strptime(str(t1), date_to_str)
		end =   datetime.strptime(str(t2), date_to_str)

		diff = end - start
		diff_in_hours = diff.total_seconds() / 3600
		self.total_hours=str(diff_in_hours)
		
