# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, timedelta
class Dailysheet(Document):
	pass

@frappe.whitelist()
def get_filter():
	query = frappe.db.sql("""select da.name_of_designer, da.employee_name,da.project,
		da.system,da.task_name,da.from_time,da.to_time,da.hours,da.work_status,da.pending_reason
        from `tabDaily sheet` as da where da.docstatus=0 and da.work_status='Pending'""", as_dict=1)
	presentday = datetime.now()
	tomorrow = presentday + timedelta(1)
	for i in query:
		d=frappe.new_doc("Daily sheet")
		d.name_of_designer=i.name_of_designer
		d.date=tomorrow.strftime('%Y-%m-%d')
		d.project=i.project
		d.system=i.system
		d.work_status=i.work_status
		d.insert()
