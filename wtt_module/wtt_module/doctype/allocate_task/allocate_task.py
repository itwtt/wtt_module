# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date,datetime,timedelta
from pytz import timezone

class AllocateTask(Document):
	# pass
	def validate(self):
		local = timezone("Asia/Kolkata")
		_time=datetime.now(local)
		tt=_time.replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
		ttime=datetime.strptime(tt,"%Y-%m-%d %H:%M:%S")
		# frappe.msgprint("test")
		if(self.tasks):
			for i in self.tasks:
				task=frappe.new_doc("Task Allocation")
				task.user=frappe.session.user
				task.employee=i.employee
				task.append("works_table",{
					"type_of_work":i.task,
					"from_time":ttime,
					"to_time":i.expected_time,
					"hours":(i.expected_time-ttime).total_seconds()/3600
					})
				task.save()

				self.append("allocated_tasks",{
					"employee":i.employee,
					"employee_name":i.employee_name,
					"task":i.task,
					"expected_time":i.expected_time,
					"task_ref":task.name
					})
			(self.tasks).clear()



