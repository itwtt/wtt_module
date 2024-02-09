# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date,datetime,timedelta
import calendar
class Grievance(Document):
	def validate(self):
		if(self.investigated_by):
			pass
		else:
			if(self.to=="HR" and not frappe.db.sql("SELECT * FROM `tabWork Update` WHERE type_of_work='"+str(self.name)+"' ")):
				df=datetime.strptime(str(datetime.now().replace(microsecond=00)),'%Y-%m-%d %H:%M:%S')
				dt=datetime.strptime(str(df),'%Y-%m-%d %H:%M:%S')+timedelta(days=2)
				bb = dt.weekday()
				godfd=calendar.day_name[bb]
				if(godfd=="Sunday"):
					dt=datetime.strptime(str(df),'%Y-%m-%d %H:%M:%S')+timedelta(days=3)
				difference = dt - df
				hrs = difference.total_seconds() / 3600
				task=frappe.new_doc("Task Allocation")
				task.user=frappe.session.user
				task.employee='WTT1301'
				task.append("works_table",{
					"type_of_work":str(self.name),
					"description":"Grievance Raised, Kindly Check",
					"from_time":datetime.strptime(str(datetime.now().replace(microsecond=00)),'%Y-%m-%d %H:%M:%S'),
					"to_time":dt,
					"hours":hrs
					})
				task.save()
				frappe.db.commit()

		if(self.workflow_state=='Investigated'):
			if(self.investigated_by==None):
				frappe.throw("Investigator Name is Mandatory")
		if(self.workflow_state=='Resolved'):
			if(self.resolved_by==None):
				frappe.throw("Resolver Name is Mandatory")
