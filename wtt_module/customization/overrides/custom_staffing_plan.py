
from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint, flt, getdate, nowdate
from frappe.utils.nestedset import get_descendants_of
from datetime import date,datetime
from hrms.hr.doctype.staffing_plan.staffing_plan import StaffingPlan

class SubsidiaryCompanyError(frappe.ValidationError): pass
class ParentCompanyError(frappe.ValidationError): pass

class customStaffingPlan(StaffingPlan):
	def on_submit(self):
		task = frappe.new_doc('Task Allocation')
		task.user=frappe.db.get_value("Employee",self.employee,"user_id")
		task.employee='WTT1301'
		for i in self.get("staffing_details"):
			task.append("works_table",{
				"type_of_work":i.designation,
				"description":i.remarks,
				"from_time":str(datetime.now()),
				"to_time":self.to_date,
				"status":"Pending",
				"staffing_plan":self.name
				})
		task.save()