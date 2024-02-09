# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Team(Document):
	def validate(self):
		ar=[]			
		for j in self.members:
			sql=frappe.db.sql("SELECT p.name FROM `tabTeam Child`as ch,`tabTeam`as p WHERE p.name=ch.parent and p.name!='"+str(self.name)+"' and ch.employee_name='"+str(j.employee_name)+"'",as_dict=1)
			if(sql):
				for i in sql:
					frappe.msgprint(j.employee_name+" already a member in "+i.name)
