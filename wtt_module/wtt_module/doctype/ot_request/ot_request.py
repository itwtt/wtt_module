# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
class OTrequest(Document):
	def validate(self):
		dd=getdate(self.from_time)
		# if(frappe.db.sql("SELECT ot.name FROM `tabOT Prior Information`as ot,`tabOvertime table`as ott WHERE ot.name=ott.parent and ot.date='"+str(dd)+"' ",as_dict=1)):
		# 	pass
		# else:
		# 	frappe.throw("Prior Information should be Passed")

		if(self.workflow_state=="Approved by HOD"):
			if(self.status==None):
				frappe.throw("Status Confirmation")

	# def on_submit(self):
	# 	dd=self.from_date
	# 	date1=dd.date()
	# 	if(self.status=='Present'):
	# 		frappe.db.sql("UPDATE `tabAttendance` SET status='"+str(self.status)+"',working_hours='9' WHERE attendance_date='"+str(self.date1)+"' and employee=='"+str(self.employee)+"'")
	# 	elif(self.status=="Half Day"):
	# 		frappe.db.sql("UPDATE `tabAttendance` SET status='"+str(self.status)+"',working_hours='4.5' WHERE attendance_date='"+str(self.date1)+"' and employee=='"+str(self.employee)+"'")
