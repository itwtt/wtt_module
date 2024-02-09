# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class FarmAttendance(Document):
	def validate(self):
		if frappe.db.sql("SELECT * from `tabFarm Attendance` Where employee='"+str(self.employee)+"' and attendance_date='"+str(self.attendance_date)+"' and name!='"+str(self.name)+"' and docstatus!=2",as_dict=1):
			frappe.throw("Attendance for "+str(self.employee_name)+" already created for "+str(self.attendance_date))

