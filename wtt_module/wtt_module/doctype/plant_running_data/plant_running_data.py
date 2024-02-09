# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from datetime import date,datetime,timedelta
from frappe.model.document import Document

class PlantRunningData(Document):
	def validate(self):
		to_remove = []
		for d in self.get("main_ro"):
			if d.col0 == "Date_Time":
				to_remove.append(d)
		[self.remove(d) for d in to_remove]

		for i in self.get("main_ro"):
			if(i.col0!="Date_Time"):
				dd=i.col0
				aa=datetime.strptime(dd,"%d/%m/%Y %H:%M")
				i.col27=aa

		to_remove1 = []
		for d in self.get("rsl_table"):
			if d.col0 == "Date_Time":
				to_remove1.append(d)
		[self.remove(d) for d in to_remove1]

		for i in self.get("rsl_table"):
			if(i.col0!="Date_Time"):
				dd=i.col0
				aa=datetime.strptime(dd,"%d/%m/%Y %H:%M")
				i.col21=aa
			
	

