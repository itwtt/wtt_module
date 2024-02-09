# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from datetime import date ,datetime ,timedelta
from frappe.model.document import Document
import sys


class WorkUpdates(Document):
	def validate(self):
		pass


@frappe.whitelist()
def work_update():
	data=[]
	tod=date.today()-timedelta(days=1)
	dop=frappe.db.sql("SELECT w.department,w.remarks,w.time FROM `tabWork Updates`as w WHERE meeting_date='"+str(tod)+"'",as_dict=1)
	for j in dop:
		work=frappe.new_doc("Work Updates")
		work.meeting_date=date.today()
		work.department=j.department
		work.time=j.time
		work.remarks=j.remarks
		doc=frappe.db.sql("SELECT w.meeting_date,w.department,w.time,wt.employee,wt.task_name,wt.description,wt.status,wt.pending_from,wt.target_date,wt.target_time FROM `tabWork Updates`as w,`tabVirtual Table`as wt WHERE wt.parent=w.name and wt.status!='Completed' and w.meeting_date='"+str(tod)+"' and w.department='"+str(j.department)+"' and meeting_date='"+str(tod)+"' ",as_dict=1)
		for j in doc:
			if(j.pending_from==None):
				due=datetime.now()
			else:
				due=j.pending_from
			work.append("virtual_table",{
				"employee":j.employee,
				"task_name":j.task_name,
				"description":j.description,
				"target_date":j.target_date,
				"target_time":j.target_time,
				"pending_from":due.strftime("%m/%d/%y")
				})
		work.save()