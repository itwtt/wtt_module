# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
class DailyActivity(Document):
	pass

@frappe.whitelist()
def get_pending():
	query = frappe.db.sql(""" select da.name_of_designer, da.employee_name,da.project,da.date,
		da.system,da.system_iii,da.type_of_design,da.type_of_instrument,da.total_hours,
        dat.task_name,dat.exp_date,
        dat.expected_hrs,dat.from_time,dat.to_time,dat.hours,dat.pending,dat.pending_reason
        from `tabDaily Activity Table` as dat, `tabDaily Activity` as da where
        dat.parent = da.name and da.workflow_state='Created' and dat.pending=1 and dat.completed=0""", as_dict=1)
	
	presentday = datetime.now()
	tomorrow = presentday + timedelta(1)
	tt=tomorrow.strftime('%Y-%m-%d')
	
	for i in query:
		v=frappe.db.sql("SELECT da.date,da.name_of_designer FROM `tabDaily Activity` as da WHERE da.date='"+tt+"' and name_of_designer='"+i.name_of_designer+"'",as_dict=1)
		if not v:
			for i in query:
				d=frappe.new_doc("Daily Activity")
				d.name_of_designer=i.name_of_designer
				d.employee_name=i.employee_name
				d.date=tt
				d.project=i.project
				d.system=i.system
				d.system_iii=i.system_iii
				d.type_of_design=i.type_of_design
				d.type_of_instrument=i.type_of_instrument
				d.append('activity',{
					'task_name':i.task_name,
					'exp_date':i.exp_date,
					'expected_hrs':i.expected_hrs,
					'from_time':i.from_time,
					'to_time':i.to_time,
					'incompleted':1,
					'pending_reason':i.pending_reason
				});
				d.insert()
	

