# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime,date
from frappe.utils import getdate

class TechnicalCriteria(Document):
	def validate(self):
		if(self.year is None or self.year==''):
			self.year=getdate(self.date).year
		# self.reduce_points()
		self.allocate_hod_points()
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
				# 	for i in self.position_specific:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.5),2)
				# 	for i in self.industry_specific:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.5),2)
				# 	for i in self.common_skills:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.5),2)
				# elif(date.today()>date4):
				# 	for i in self.position_specific:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.4),2)
				# 	for i in self.industry_specific:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.4),2)
				# 	for i in self.common_skills:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.4),2)
				# elif(date.today()>date3):
				# 	for i in self.position_specific:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.3),2)
				# 	for i in self.industry_specific:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.3),2)
				# 	for i in self.common_skills:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.3),2)
				# elif(date.today()>date2):
				# 	for i in self.position_specific:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.2),2)
				# 	for i in self.industry_specific:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.2),2)
				# 	for i in self.common_skills:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.2),2)
				# elif(date.today()>date1):
				# 	for i in self.position_specific:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.1),2)
				# 	for i in self.industry_specific:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.1),2)
				# 	for i in self.common_skills:
				# 		i.your_points = round(float(i.your_points)-(float(i.your_points)*0.1),2)
	def allocate_hod_points(self):
		if(self.workflow_state=='Approved by HOD'):
			for i in self.position_specific:
				if(i.hod_points==None):
					i.hod_points=i.your_points
			for i in self.industry_specific:
				if(i.hod_points==None):
					i.hod_points=i.your_points
			for i in self.common_skills:
				if(i.hod_points==None):
					i.hod_points=i.your_points

		if(self.workflow_state=='Approved by TD'):
			for i in self.position_specific:
				if(i.hod_points==None):
					i.hod_points=i.your_points
			for i in self.industry_specific:
				if(i.hod_points==None):
					i.hod_points=i.your_points
			for i in self.common_skills:
				if(i.hod_points==None):
					i.hod_points=i.your_points

		if(self.workflow_state=='Approved by ED'):
			for i in self.position_specific:
				if(i.hod_points==None):
					i.hod_points=i.your_points
			for i in self.industry_specific:
				if(i.hod_points==None):
					i.hod_points=i.your_points
			for i in self.common_skills:
				if(i.hod_points==None):
					i.hod_points=i.your_points

	def on_submit(self):
		for i in self.position_specific:
			if(i.hod_points==None):
				i.hod_points=i.your_points
		for i in self.industry_specific:
			if(i.hod_points==None):
				i.hod_points=i.your_points
		for i in self.common_skills:
			if(i.hod_points==None):
				i.hod_points=i.your_points
	
		for i in self.position_specific:
			if(i.management_points==None):
				i.management_points=i.hod_points
		for i in self.industry_specific:
			if(i.management_points==None):
				i.management_points=i.hod_points
		for i in self.common_skills:
			if(i.management_points==None):
				i.management_points=i.hod_points

		
	
@frappe.whitelist()
def update_technical(emp):
	arr=[]
	query=frappe.db.sql("SELECT performance_index,technical__criteria FROM `tabTechnical Data` WHERE employee='"+str(emp)+"'",as_dict=1)
	for i in query:
		arr.append({
			'perfor':i.performance_index,
			'techcri':i.technical__criteria
			})
	return arr
