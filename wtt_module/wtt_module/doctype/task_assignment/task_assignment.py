# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from datetime import date,datetime,timedelta
from frappe.model.document import Document
from frappe.utils import add_days, cint, cstr, flt, getdate, date_diff, money_in_words, formatdate, get_first_day
import calendar
class TaskAssignment(Document):
	def validate(self):
		for i in self.works_table:
			i.no_mercy=1
		if(self.user==frappe.session.user or frappe.session.user=='Administrator'):
			pass
		else:
			frappe.throw("This Task Assigned by "+str(self.user)+" your are not permitted to Change")
		arr=[]
		arr2=[]
		for i in self.get("works_table"):
			if(i.total_points!=None):
				arr2.append(round(i.total_points,2))
			if i.status=='Completed':
				arr.append(round(i.gained_points,2))
		self.out_of=sum(arr2)
		self.total=sum(arr)

	def on_submit(self):
		if(frappe.session.user!=self.user):
			frappe.throw('Not Permitted')
		for i in self.get("works_table"):
			if(i.status=='Completed'):
				pass
			else:
				frappe.throw("Please, Make Sure all the Tasks were Completed.")

@frappe.whitelist()
def gain_points(e_date,a_date,points):
	arr=[]
	pnt=0
	count=0
	count2=0
	# while(getdate(a_date)<=getdate(e_date)):
	# 	a_date=getdate(a_date)+timedelta(days=1)
	# 	# frappe.msgprint(str(count)+"c1")
	# 	gug = getdate(a_date).weekday()
	# 	sun=calendar.day_name[gug]
	# 	if(sun=="Sunday"):
	# 		count+=1
	# while(getdate(e_date)<=date.today()):
	# 	a_date=getdate(e_date)+timedelta(days=1)
	# 	# frappe.msgprint(str(count2)+"c2")
	# 	gug = getdate(e_date).weekday()
	# 	sun=calendar.day_name[gug]
	# 	if(sun=="Sunday"):
	# 		count2+=1
	
	# # frappe.msgprint("tt")
	
	if(getdate(e_date)<date.today()):
		diff = getdate(e_date) - getdate(a_date)
		cc=diff.days-count
		if(diff.days>0):
			point = cint(points)/diff.days
			diff2 = date.today() - getdate(e_date)
			point2 = point*diff2.days
			fp = cint(points)-round(point2,2)
			# frappe.msgprint(str(fp))
			if(fp>0):
				pnt+=round(fp,2)
			else:
				pnt=pnt
		elif(diff.days<0):
			pnt+=cint(points)
		elif(diff.days==0):
			if(date.today()==getdate(e_date)):
				pnt+=cint(points)
			else:
				pnt=pnt
	else:
		pnt+=cint(points)
	# frappe.msgprint(str(pnt))
	return pnt
# @frappe.whitelist()
# def make_taskpoints():
# 	arr=[]
# 	doc=frappe.db.sql("SELECT p.employee,p.employee_name,p.department,c.name,c.parent,c.type_of_work,c.description,c.assign_date,c.expected_date,c.total_points,c.gained_points,c.status from `tabTask Assignment`as p,`tabWork table`as c WHERE p.name=c.parent and p.docstatus=0 and c.status!='Completed' ",as_dict=1)
# 	for i in doc:
# 		if(i.expected_date is not None):
# 			diff = i.expected_date - i.assign_date
# 			if(diff.days>0):
# 				point = i.total_points/diff.days
# 				diff2 = date.today() - i.expected_date
# 				point2 = point*diff2.days
# 				fp = i.total_points-round(point2,2)
# 				if(fp>0):
# 					pnt=round(fp,2)
# 				else:
# 					pnt=0
# 			else:
# 				pnt=i.total_points
# 			if(i.expected_date<date.today()):
# 				dot=frappe.get_doc("Work table",i.name)
# 				dot.gained_points=pnt
# 				dot.save()
# 			else:
# 				dot=frappe.get_doc("Work table",i.name)
# 				dot.gained_points=i.total_points
# 				dot.save()

# 	