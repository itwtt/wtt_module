from __future__ import unicode_literals

import frappe

def get_context(context):
	# do your magic here
	pass
@frappe.whitelist(allow_guest=True)
def func(arr):
	ar=[]
	for i in arr:
		ar.append({
			"tank":i
			})
	# ar=[]
	# for i in frappe.db.sql("SELECT name,employee_name,rounded_total FROM `tabSalary Slip` WHERE start_date>='"+str(fr_date)+"' AND end_date<='"+str(to_date)+"'",as_dict=1):
	# 	ar.append({
	# 		"employee_name":i.employee_name,
	# 		"rounded_total":i.rounded_total,
	# 		"salary_id":i.name
	# 	})
	return ar