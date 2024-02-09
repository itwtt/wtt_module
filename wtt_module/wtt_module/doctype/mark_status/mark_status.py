# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime,timedelta,date
from frappe.model.document import Document

class MarkStatus(Document):
	pass


	# @frappe.whitelist()
	# def mark_half_day(self):

	# 	query=frappe.db.sql("""SELECT employee_name,attendance_date,name
	# 		from `tabAttendance` 
	# 		where 
	# 		docstatus=1 and 
	# 		attendance_date>='"""+str(self.from_date)+"""' and
	# 		attendance_date<='"""+str(self.to_date)+"""' and
	# 		late_entry=1 and 
	# 		status='Present' and
	# 		CASE DAYNAME(attendance_date)
	# 			WHEN 'Saturday' THEN in_time>CONCAT(attendance_date,' 10:00:00')
	# 		ELSE in_time>CONCAT(attendance_date,' 10:30:00')
	# 		END 
	# 		""",as_dict=1)
	# 	for i in query:
	# 		frappe.db.sql("UPDATE `tabAttendance` set status='Half Day',too_late='In Time>10:30' where name='"+str(i.name)+"' ")

	# 	return str(query)
