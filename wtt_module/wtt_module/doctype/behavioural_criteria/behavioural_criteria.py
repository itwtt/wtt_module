# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import calendar
from datetime import date,datetime,timedelta
from frappe.utils import getdate
class BehaviouralCriteria(Document):
	def validate(self):
		if(self.year is None or self.year==''):
			self.year=getdate(self.date).year
		# self.reduce_points()
		self.allocate_hod_points()
		self.attendance_percentage()
	def reduce_points(self):
		mname=self.month
		bb=datetime.strptime(mname, '%B').month
		date1=date.today().replace(day=3,month=bb+1)
		date2=date.today().replace(day=4,month=bb+1)
		date3=date.today().replace(day=5,month=bb+1)
		date4=date.today().replace(day=6,month=bb+1)
		date5=date.today().replace(day=7,month=bb+1)
		if(self.workflow_state in ("Created") and frappe.session.user not in ('harshini@wttindia.com','sarnita@wttindia.com','venkat@wttindia.com','Administrator','gm_admin@wttindia.com')):
			# if(frappe.db.sql("SELECT * from `tabAttendance` WHERE attendance_date='"+str(date1)+"' AND status='Present' or status='Half Day' ",as_dict=1)):
			if(self.created_date):
				pass
			else:
				self.created_date=str(date.today())
				# if(date.today()>date5):
				# 	for i in self.attitude:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.5),2)
				# 	for i in self.personal:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.5),2)
				# 	for i in self.skill:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.5),2)
				# 	for i in self.team:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.5),2)
				# 	for i in self.work_performance:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.5),2)
				# 	for i in self.work_knowledge:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.5),2)
				# elif(date.today()>date4):
				# 	for i in self.attitude:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.4),2)
				# 	for i in self.personal:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.4),2)
				# 	for i in self.skill:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.4),2)
				# 	for i in self.team:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.4),2)
				# 	for i in self.work_performance:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.4),2)
				# 	for i in self.work_knowledge:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.4),2)
				# elif(date.today()>date3):
				# 	for i in self.attitude:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.3),2)
				# 	for i in self.personal:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.3),2)
				# 	for i in self.skill:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.3),2)
				# 	for i in self.team:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.3),2)
				# 	for i in self.work_performance:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.3),2)
				# 	for i in self.work_knowledge:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.3),2)
				# elif(date.today()>date2):
				# 	for i in self.attitude:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.2),2)
				# 	for i in self.personal:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.2),2)
				# 	for i in self.skill:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.2),2)
				# 	for i in self.team:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.2),2)
				# 	for i in self.work_performance:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.2),2)
				# 	for i in self.work_knowledge:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.2),2)
				# elif(date.today()>date1):
				# 	for i in self.attitude:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.1),2)
				# 	for i in self.personal:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.1),2)
				# 	for i in self.skill:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.1),2)
				# 	for i in self.team:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.1),2)
				# 	for i in self.work_performance:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.1),2)
				# 	for i in self.work_knowledge:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.1),2)
	def allocate_hod_points(self):
		if(self.workflow_state=="Approved by HOD"):
			for i in self.attitude:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.personal:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.skill:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.team:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.work_performance:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.work_knowledge:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points

		if(self.workflow_state=="Approved by TD"):
			for i in self.attitude:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.personal:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.skill:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.team:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.work_performance:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.work_knowledge:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points

		if(self.workflow_state=="Approved by ED"):
			for i in self.attitude:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.personal:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.skill:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.team:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.work_performance:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
			for i in self.work_knowledge:
				if(i.hod_points==None or i.hod_points==""):
					i.hod_points=i.your_points
		
	def on_submit(self):
		self.attendance_percentage_on_submit()

	@frappe.whitelist()
	def proceed(self):
		frappe.db.sql("UPDATE `tabAttitude Table`as cc set cc.hod_points=cc.your_points where cc.parent='"+str(self.name)+"' and cc.hod_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabTeam Table`as cc set cc.hod_points=cc.your_points where cc.parent='"+str(self.name)+"' and cc.hod_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabSkill Table`as cc set cc.hod_points=cc.your_points where cc.parent='"+str(self.name)+"' and cc.hod_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabPersonal Table`as cc set cc.hod_points=cc.your_points where cc.parent='"+str(self.name)+"' and cc.hod_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabWork knowledge`as cc set cc.hod_points=cc.your_points where cc.parent='"+str(self.name)+"' and cc.hod_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabWork performance`as cc set cc.hod_points=cc.your_points where cc.parent='"+str(self.name)+"' and cc.hod_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabAttitude Table`as cc set cc.management_points=cc.hod_points where cc.parent='"+str(self.name)+"' and cc.management_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabTeam Table`as cc set cc.management_points=cc.hod_points where cc.parent='"+str(self.name)+"' and cc.management_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabSkill Table`as cc set cc.management_points=cc.hod_points where cc.parent='"+str(self.name)+"' and cc.management_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabPersonal Table`as cc set cc.management_points=cc.hod_points where cc.parent='"+str(self.name)+"' and cc.management_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabWork knowledge`as cc set cc.management_points=cc.hod_points where cc.parent='"+str(self.name)+"' and cc.management_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")
		frappe.db.sql("UPDATE `tabWork performance`as cc set cc.management_points=cc.hod_points where cc.parent='"+str(self.name)+"' and cc.management_points='0' and docstatus=1 and owner='"+str(self.owner)+"' ")

		return "test"

	@frappe.whitelist()
	def rectify(self):
		for i in self.attitude:
			frappe.db.sql("UPDATE `tabAttitude Table` set your_points=`tabAttitude Table`.`hod_points` where name='"+str(i.name)+"' ")
		for i in self.personal:
			frappe.db.sql("UPDATE `tabPersonal Table` set your_points=`tabPersonal Table`.`hod_points` where name='"+str(i.name)+"' ")
		for i in self.skill:
			frappe.db.sql("UPDATE `tabSkill Table` set your_points=`tabSkill Table`.`hod_points` where name='"+str(i.name)+"' ")
		for i in self.team:
			frappe.db.sql("UPDATE `tabTeam Table` set your_points=`tabTeam Table`.`hod_points` where name='"+str(i.name)+"' ")
		for i in self.work_performance:
			if(i.criteria not in ["Attendance","Punctuality"]):
				frappe.db.sql("UPDATE `tabWork performance` set your_points=`tabWork performance`.`hod_points` where name='"+str(i.name)+"' ")
		for i in self.work_knowledge:
			frappe.db.sql("UPDATE `tabWork knowledge` set your_points=`tabWork knowledge`.`hod_points` where name='"+str(i.name)+"' ")

	@frappe.whitelist()
	def attendance_percentage(self):
		month_array=['','January','February','March','April','May','June','July','August','September','October','November','December']
		mm=month_array.index(self.month)
		date1=date.today().replace(year=int(self.year),month=mm,day=1)
		date_cal=(date1+timedelta(days=32)).replace(day=1)
		date2=date_cal-timedelta(days=1)
		if(date.today()<date2):
			date2=date.today()
		working_days=date2-date1
		hol=[]
		holidays=frappe.db.sql("select distinct(holiday_date)as 'holiday_date' from `tabHoliday` where parent='Holiday 2023' and holiday_date>='"+str(date1)+"' and holiday_date<='"+str(date2)+"'",as_dict=1)
		if(holidays):
			for i in holidays:
				hol.append(i.holiday_date)
		year = 2023
		day_to_count = calendar.SUNDAY
		matrix = calendar.monthcalendar(year,mm)
		num_days = sum(1 for x in matrix if x[day_to_count] != 0)
		total_days=working_days.days-num_days+len(hol)+1#1 added for get full days in month
		if("31" in str(date2)):
			total_days=total_days-1

		query=frappe.db.sql("SELECT count(distinct(name))as count,status from `tabAttendance` where employee='"+str(self.employee)+"' and attendance_date>='"+str(date1)+"' and attendance_date<='"+str(date2)+"' and docstatus=1 GROUP BY status",as_dict=1)
		pre=hdy=abst=percentage=late_percentage=0
		for i in query:
			if(i.status=="Present"):
				pre+=i.count
			elif(i.status=="Half Day"):
				hdy+=(i.count)/2

		query=frappe.db.sql("SELECT count(distinct(name))as count,status from `tabAttendance` where late_entry=1 and status='Present' and employee='"+str(self.employee)+"' and attendance_date>='"+str(date1)+"' and attendance_date<='"+str(date2)+"' and docstatus=1 GROUP BY status",as_dict=1)
		late=0
		for i in query:
			if(i.status=="Present"):
				late+=i.count
		
		percentage=((pre+hdy+len(hol))/total_days)*100
		if(percentage>100):
			percentage=100
		late_percent=(late/total_days)*100

		for i in self.work_performance:
			if(i.criteria=="Punctuality"):
				i.your_points=100-round(late_percent,2)

			if(i.criteria=="Attendance" or i.criteria=="Attendence"):
				i.your_points=round(percentage,2)

	@frappe.whitelist()
	def attendance_percentage_on_submit(self):
		month_array=['','January','February','March','April','May','June','July','August','September','October','November','December']
		mm=month_array.index(self.month)
		date1=date.today().replace(month=mm,day=1)
		date_cal=(date1+timedelta(days=32)).replace(day=1)
		date2=date_cal-timedelta(days=1)
		working_days=date2-date1
		hol=[]
		holidays=frappe.db.sql("select distinct(holiday_date)as 'holiday_date' from `tabHoliday` where parent='Holiday 2023' and holiday_date>='"+str(date1)+"' and holiday_date<='"+str(date2)+"'",as_dict=1)
		if(holidays):
			for i in holidays:
				hol.append(i.holiday_date)
		year = 2023
		day_to_count = calendar.SUNDAY
		matrix = calendar.monthcalendar(year,mm)
		num_days = sum(1 for x in matrix if x[day_to_count] != 0)
		total_days=working_days.days-num_days+len(hol)+1#1 added for get full days in month
		if("31" in str(date2)):
			total_days=total_days-1
		query=frappe.db.sql("SELECT count(distinct(name))as count,status from `tabAttendance` where employee='"+str(self.employee)+"' and attendance_date>='"+str(date1)+"' and attendance_date<='"+str(date2)+"' and docstatus=1 GROUP BY status",as_dict=1)
		pre=hdy=abst=percentage=late_percentage=0
		for i in query:
			if(i.status=="Present"):
				pre+=i.count
			elif(i.status=="Half Day"):
				hdy+=(i.count)/2

		query=frappe.db.sql("SELECT count(distinct(name))as count,status from `tabAttendance` where late_entry=1 and status='Present' and employee='"+str(self.employee)+"' and attendance_date>='"+str(date1)+"' and attendance_date<='"+str(date2)+"' and docstatus=1 GROUP BY status",as_dict=1)
		late=0
		for i in query:
			if(i.status=="Present"):
				late+=i.count
		percentage=((pre+hdy+len(hol))/total_days)*100
		if(percentage>100):
			percentage=100
		late_percent=(late/total_days)*100

		for i in self.work_performance:
			if(i.criteria=="Punctuality"):
				i.your_points=100-round(late_percent,2)
				i.hod_points=100-round(late_percent,2)
				i.management_points=100-round(late_percent,2)

			if(i.criteria=="Attendance" or i.criteria=="Attendence"):
				i.your_points=round(percentage,2)
				i.hod_points=round(percentage,2)
				i.management_points=round(percentage,2)


