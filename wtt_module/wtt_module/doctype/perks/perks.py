# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import datetime
import time
from datetime import datetime 
class Perks(Document):
	def on_submit(self):
		for i in self.get("salary_table"):
			if(i.amount!=0):
				gug=frappe.get_doc("Salary Slip",i.salary_id)
				gug.append("earnings",{
					"salary_component":"Perks",
					"amount":i.amount
					})
				gug.save()
				frappe.db.commit()


@frappe.whitelist()
def update_salary(fr_date,to_date):

	salary=0
	ot=0
	gug1=0
	hr=0
	arr=[]
	lst=[]
	item=[]
	count=0
	lst1=[]
	item1=[]

	tt=[]
	otdate1 = datetime.strptime(str(fr_date), '%Y-%m-%d')
	otdate2 = datetime.strptime(str(to_date), '%Y-%m-%d')
	otdate3 = otdate2.replace(hour=23,minute=00,second=0,microsecond=0)
	for i in frappe.db.sql("SELECT employee,employee_name,hours FROM `tabOT request`  WHERE from_time>='"+str(otdate1)+"' AND to_time<='"+str(otdate3)+"' AND docstatus=0 ORDER BY employee_name ASC",as_dict=1):
		
		tt.append({
			"employee_name":i.employee_name,
			"hrs":i.hours
		})

	for hh in tt:
		if hh["employee_name"] not in lst:
			item.append(hh)
			lst.append(hh["employee_name"])
		else:
			item[lst.index(hh["employee_name"])]["hrs"] += hh["hrs"]

		
	for q in item:
		salary=0
		for k in frappe.db.sql("SELECT salary_structure FROM `tabSalary Slip` WHERE start_date>='"+str(fr_date)+"' AND end_date<='"+str(to_date)+"' AND employee_name='"+str(q["employee_name"])+"'",as_dict=1):
			for i in frappe.db.sql("SELECT amount FROM `tabSalary Detail` WHERE parenttype='Salary Structure' AND parentfield='earnings' AND parent='"+str(k.salary_structure)+"'",as_dict=1):
				salary+=float(i.amount)

		ot=(int(salary)/30)
		mul=(q["hrs"]*(ot/8))
		arr.append({
		"employee_name":q["employee_name"],
		"ot_hrs":q["hrs"],
		"salary_1":ot,
		"ot_amount":mul
		})

	v=[]
	for vv in arr:
		v.append(vv["employee_name"])	

	ar=[]
	for i in frappe.db.sql("SELECT name,employee_name,rounded_total FROM `tabSalary Slip` WHERE start_date>='"+str(fr_date)+"' AND end_date<='"+str(to_date)+"' ORDER BY employee_name ASC",as_dict=1):
		if(i.employee_name not in v):
			ar.append({
				"employee_name":i.employee_name,
				"rounded_total":i.rounded_total,
				"salary_id":i.name
			})
		else:
			for j in arr:
				if(i.employee_name==j["employee_name"]):
					ar.append({
						"employee_name":i.employee_name,
						"rounded_total":i.rounded_total,
						"salary_id":i.name,
						"ot_hrs":j["ot_hrs"],
						"salary_1":j["salary_1"],
						"ot_amount":j["ot_amount"]
					});
	return ar

		# ar.append({
		# 	"employee_name":i.employee_name,
		# 	"rounded_total":i.rounded_total,
		# 	"salary_id":i.name
		# })
	# return ar

	'''
	salary=0
	ot=0
	gug1=0
	hr=0
	arr=[]
	lst=[]
	item=[]
	count=0
	lst1=[]
	item1=[]

	tt=[]
	otdate1 = datetime.strptime(str(fr_date), '%Y-%m-%d')
	otdate2 = datetime.strptime(str(to_date), '%Y-%m-%d')
	otdate3 = otdate2.replace(hour=23,minute=00,second=0,microsecond=0)
	for i in frappe.db.sql("SELECT employee,employee_name,hours FROM `tabOT request`  WHERE from_time>='"+str(otdate1)+"' AND to_time<='"+str(otdate3)+"' AND workflow_state='Approved' AND branch='HEAD OFFICE' ORDER BY employee_name ASC",as_dict=1):
		tt.append({
			"employee_name":i.employee_name,
			"hrs":i.hours
		})

	for hh in tt:
		if hh["employee_name"] not in lst:
			item.append(hh)
			lst.append(hh["employee_name"])
		else:
			item[lst.index(hh["employee_name"])]["hrs"] += hh["hrs"]

		
	for q in item:
		salary=0
		for k in frappe.db.sql("SELECT salary_structure FROM `tabSalary Slip` WHERE start_date>='"+str(fr_date)+"' AND end_date<='"+str(to_date)+"' AND employee_name='"+str(q["employee_name"])+"'",as_dict=1):
			for i in frappe.db.sql("SELECT amount FROM `tabSalary Detail` WHERE parenttype='Salary Structure' AND parentfield='earnings' AND parent='"+str(k.salary_structure)+"'",as_dict=1):
				salary+=float(i.amount)

		ot=(int(salary)/30)
		mul=(q["hrs"]*(ot/8))
		arr.append({
		"employee_name":q["employee_name"],
		"ot_hrs":q["hrs"],
		"salary_1":ot,
		"ot_amount":mul
		})
	return arr
		# if hh["employee_name"] not in lst:
		# 	item.append(hh)
		# 	lst.append(hh["employee_name"])
		# else:
		# 	item[lst.index(hh["employee_name"])]["hrs"] += hh["hrs"]

	# for q in item:
	# 	if q["hrs"]>8.00:
	# 		ot=(q["amt"]/30)
	# 	arr.append({
	# 		"employee_name":q["employee_name"],
	# 		"ot_hrs":q["hrs"],
	# 		"ot_amount":ot
	# 		})
	# return arr

				# if i.employee_name not in lst:
				# 	item.append(i)
				# 	lst.append(i.employee_name)
				# else:
				# 	item[lst.index(i.employee_name)].hours += i.hours
				# 	item[lst.index(i.employee_name)].amount += k.amount
	# for q in item:
	# 	frappe.msgprint(q)
	# 	arr.append({
	# 		"employee_name":q.employee_name,
	# 		"ot_hrs":q.hours,
	# 		})

	# 			frappe.msgprint(str(str(i.employee_name)+"-"+str(k.amount)))
	# return arr
	'''