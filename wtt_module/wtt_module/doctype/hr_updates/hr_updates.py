# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from datetime import datetime 
from datetime import  date,timedelta

class HRUpdates(Document):
	def on_submit(self):
		if(self.category=="Daily"):
			for i in self.get("att_employee"):
				doc=frappe.new_doc("Absentees")
				doc.employee=i.employee
				doc.employee_name=i.employee_name
				doc.department=i.department
				doc.status=i.status
				doc.reason=i.remarks
				doc.title= str(i.employee_name)+"-"+str(i.status)
				doc.save()
			
			for j in self.get("late_entries"):
				doc=frappe.new_doc("Absentees")
				doc.employee=j.employee
				doc.employee_name=j.employee_name
				doc.department=j.department
				doc.status=j.status
				doc.reason=j.remarks
				doc.title= str(j.employee_name)+"-"+str(j.status)+"-"+str(j.time)
				doc.save()


@frappe.whitelist()
def update_employee(go):
	ar=[]
	arr=[]
	ag=[]
	vv=frappe.db.sql("SELECT sti.employee FROM `tabHR Updates Table2` as sti INNER JOIN `tabHR Updates` as st ON sti.parent=st.name WHERE st.date=CURDATE()",as_dict=1)
	for ss in vv:
		ag.append(ss.employee)
	if(ag):
		val=frappe.db.sql(""" SELECT distinct(employee) FROM `tabEmployee` WHERE status='Active' AND employee!='WTT001' AND employee!='WTT002' AND employee!='WTT003' EXCEPT SELECT distinct(employee) FROM `tabEmployee Checkin` WHERE time>=CONCAT(CURDATE()," 04:00:00") AND time<=CONCAT(CURDATE()," 11:00:00") """,as_dict=1)
		for i in val:
			if i.employee not in ag:
				ar.append({
					'emp':i.employee
					})
		
		lt=frappe.db.sql(""" SELECT `tabEmployee Checkin`.`employee`,`tabEmployee Checkin`.`time` FROM `tabEmployee Checkin` INNER JOIN `tabEmployee` `tabEmployee` ON `tabEmployee Checkin`.`employee` = `tabEmployee`.`employee` WHERE time>=CONCAT(CURDATE()," 9:01:00") AND time<=CONCAT(CURDATE()," 11:00:00") GROUP BY `tabEmployee Checkin`.`employee` ORDER BY `tabEmployee Checkin`.`time` """,as_dict=1)
		for k in lt:
			cc=datetime.strptime(str(k.time),"%Y-%m-%d %H:%M:%S")
			vs = cc.strftime("%H:%M")
			arr.append({
				'lt':k.employee,
				'tt':vs
				})
	else:
		val=frappe.db.sql(""" SELECT distinct(employee) FROM `tabEmployee` WHERE status='Active' AND employee!='WTT001' AND employee!='WTT002' AND employee!='WTT003' EXCEPT SELECT distinct(employee) FROM `tabEmployee Checkin` WHERE time>=CONCAT(CURDATE()," 04:00:00") AND time<=CONCAT(CURDATE()," 11:00:00") """,as_dict=1)
		for i in val:
			ar.append({
				'emp':i.employee
				})
		
		lt=frappe.db.sql(""" SELECT `tabEmployee Checkin`.`employee`,`tabEmployee Checkin`.`time` FROM `tabEmployee Checkin` INNER JOIN `tabEmployee` `tabEmployee` ON `tabEmployee Checkin`.`employee` = `tabEmployee`.`employee` WHERE time>=CONCAT(CURDATE()," 9:01:00") AND time<=CONCAT(CURDATE()," 11:00:00") GROUP BY `tabEmployee Checkin`.`employee` ORDER BY `tabEmployee Checkin`.`time` """,as_dict=1)
		for k in lt:
			cc=datetime.strptime(str(k.time),"%Y-%m-%d %H:%M:%S")
			vs = cc.strftime("%H:%M")
			arr.append({
				'lt':k.employee,
				'tt':vs
				})
	return ar,arr


