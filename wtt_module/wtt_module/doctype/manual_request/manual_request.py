# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import calendar
import datetime
import time
from datetime import datetime 
from datetime import  date,timedelta

class ManualRequest(Document):
	def on_submit(self):
		dd=datetime.strptime(str(self.from_time), '%Y-%m-%d %H:%M:%S')
		dodo=datetime.strptime(str(self.to_time), '%Y-%m-%d %H:%M:%S')
		pdate=dd.date()	
		tdate=date.today()
		if(pdate==tdate):
			frappe.throw("Attendance is not marked Today")
		query=frappe.db.sql("SELECT name,in_time,out_time FROM `tabAttendance` WHERE employee='"+self.employee+"' and attendance_date='"+str(pdate)+"' and docstatus=1 ",as_dict=1)
		if query:
			for i in query:
				frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(self.hours)+"',status='"+str(self.att_status)+"',shift='"+str(self.shift)+"',late_entry=0,early_exit=0 WHERE name='"+str(i.name)+"' ")

		# 	for i in query:
		# 		frappe.msgprint(str(i.in_time)+str(i.out_time)+i.name)
		# 		if (i.in_time==None and i.out_time==None):
		# 			doc=frappe.get_doc("Attendance",i.name)
		# 			doc.shift=self.shift
		# 			doc.in_time=self.from_time
		# 			doc.out_time=self.to_time
		# 			doc.working_hours=self.hours
		# 			doc.status=self.att_status
		# 			doc.submit()
		# 		elif (i.in_time!=None and i.out_time!=None):
		# 			doc=frappe.get_doc("Attendance",i.name)
		# 			doc.shift=self.shift
		# 			doc.in_time=self.from_time
		# 			doc.out_time=self.to_time
		# 			doc.working_hours=self.hours
		# 			doc.status=self.att_status
		# 			doc.submit()
		# 		elif(i.in_time==None):
		# 			if (i.out_time<dodo):
		# 				doc=frappe.get_doc("Attendance",i.name)
		# 				doc.shift=self.shift
		# 				doc.in_time=self.from_time
		# 				doc.out_time=self.to_time
		# 				doc.working_hours=self.hours
		# 				doc.status=self.att_status
		# 				doc.submit()
		# 			else:
		# 				diff = i.out_time-self.from_time
		# 				hrs = diff.total_seconds() / 3600
		# 				doc=frappe.get_doc("Attendance",i.name)
		# 				doc.shift=self.shift
		# 				doc.in_time=self.from_time
		# 				doc.working_hours=hrs
		# 				doc.status=self.att_status
		# 				doc.submit()
		# 		else:
		# 			pass
		# else:
		# 	doc=frappe.get_doc("Attendance")
		# 	doc.employee=self.employee
		# 	doc.in_time=self.from_time
		# 	doc.out_time=self.to_time
		# 	doc.working_hours=self.hours
		# 	doc.shift=self.shift
		# 	doc.attendance_date=pdate
		# 	doc.status=self.att_status
		# 	doc.submit()