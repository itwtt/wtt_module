# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, date
from frappe.utils import date_diff
import datetime, math
import calendar
import datetime
import time
from datetime import datetime 
from datetime import  date,timedelta
from frappe.utils import cstr
from pytz import timezone 
from datetime import datetime


class WorkAllocation(Document):
	def on_submit(self):
		for i in self.task_table:
			user = frappe.db.get_value('Employee',i.given_by, 'user_id')
			doc=frappe.new_doc("Task Allocation")
			doc.user=user
			doc.employee=i.given_to
			doc.append("works_table",{
				"type_of_work":i.task_name,
				"description":i.task_description,
				"from_time":datetime.strptime(str(i.from_time),'%Y-%m-%d %H:%M:%S'),
				"to_time":datetime.strptime(str(i.to_time),'%Y-%m-%d %H:%M:%S')
				})
			doc.save()
