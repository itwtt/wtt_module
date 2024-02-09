# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DailyFarmAttendance(Document):
	def on_cancel(self):
		for i in self.attendance:
			frappe.db.sql("UPDATE `tabFarm Attendance` set docstatus=2 WHERE attendance_date='"+str(self.date)+"' and employee='"+str(i.employee)+"' ")


