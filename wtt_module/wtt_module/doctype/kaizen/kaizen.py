# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime,date,timedelta

class Kaizen(Document):
	def validate(self):
		if(self.remarks!=None):
			frappe.db.sql("UPDATE `tabKaizen Evaluation Sheet` SET waiting_for='"+str(self.waiting_for)+"',remarks='"+str(self.remarks)+"' WHERE kaizen_id='"+str(self.name)+"' ",as_dict=1)
			
		if(self.workflow_state=='Accepted'):
			if(frappe.db.exists({"doctype":"Kaizen Evaluation Sheet","kaizen_id":self.name})):
				frappe.db.sql("UPDATE `tabKaizen Evaluation Sheet` SET baseline='"+str(self.baseline)+"' WHERE kaizen_id='"+str(self.name)+"' ",as_dict=1)
			else:
				doc=frappe.new_doc("Kaizen Evaluation Sheet")
				doc.kaizen_id=self.name
				doc.employee=self.employee
				doc.baseline=self.baseline
				doc.date=date.today()
				doc.save()
			if(self.evaluation_process==None):
				task = frappe.get_last_doc("Kaizen Evaluation Sheet")
				self.evaluation_process=task.name


	def on_submit(self):
		frappe.db.sql("UPDATE `tabKaizen` SET points=10,status='Approved' WHERE name='"+str(self.name)+"' ")
		self.reload()

	def on_cancel(self):
		frappe.db.sql("UPDATE `tabKaizen` SET points=5,status='Denied by MD' WHERE name='"+str(self.name)+"' ")
		self.reload()
				
@frappe.whitelist()
def evaluation(name):
	ar=[]
	br=[]
	doc=frappe.get_doc("Kaizen Evaluation Sheet",name)
	for i in doc.hod_remarks:
		ar.append(i)
	for i in doc.kaizen_lead_remarks:
		br.append(i)
	return ar,br