# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document
class WorkshopActivity(Document):
	pass
@frappe.whitelist()
def get_team_members(team):
	ar=[]
	for i in frappe.db.sql("SELECT GROUP_CONCAT(DISTINCT(employee_name))as emp_name FROM `tabTeam Child` WHERE parent='"+str(team)+"' ",as_dict=1):
		ar.append(i.emp_name)
	return ar[0]