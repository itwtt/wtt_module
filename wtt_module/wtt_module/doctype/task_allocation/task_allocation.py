# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime, date
from frappe.utils import date_diff
import datetime, math
import calendar
import datetime
import time
from datetime import datetime 
from datetime import  date,timedelta
from frappe.utils import cstr
from pytz import timezone 
from datetime import datetime
from datetime import date,datetime,timedelta
import json
from frappe.utils.background_jobs import enqueue

class TaskAllocation(Document):
	
	def validate(self):
		emp=frappe.db.get_value('Employee', {'user_id': self.user},'employee_name')
		self.assigned_by=emp
		if(frappe.session.user!='Administrator' or frappe.session.user!='venkat@wttindia.com' or frappe.session.user!='ps_cmd@wttindia.com'):
			doc=frappe.db.get_value("Employee",self.employee,"user_id")
			if(str(doc)==self.user):
				self.self_allocation=1

		

@frappe.whitelist()
def update_allocation(assign_date,expected,hours):
	arr=[]
	date_assign = datetime.strptime(assign_date,'%Y-%m-%d %H:%M:%S')
	date_expect = datetime.strptime(expected,'%Y-%m-%d %H:%M:%S')
	ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
	now = datetime.strptime(ind_time,'%Y-%m-%d %H:%M:%S')
	diff=date_diff(date_expect, date_assign)
	diff2=date_diff(now, date_assign)

	holidays=frappe.db.sql("SELECT holiday_date FROM `tabHoliday` WHERE holiday_date>='"+str(date_assign)+"' AND holiday_date<='"+str(date_expect)+"'",as_dict=1)
	so=0
	for hh in holidays:
		va=hh.holiday_date
		dafd = va.weekday()
		godfd=calendar.day_name[dafd]
		if(godfd!="Sunday"):
		 	so=so+1
	diff=diff-so

	holidays2=frappe.db.sql("SELECT holiday_date FROM `tabHoliday` WHERE holiday_date>='"+str(date_assign)+"' AND holiday_date<='"+str(now)+"'",as_dict=1)
	so2=0
	for hh2 in holidays:
		va2=hh2.holiday_date
		dafd2 = va2.weekday()
		godfd2=calendar.day_name[dafd2]
		if(godfd2!="Sunday"):
		 	so2=so2+1
	diff2=diff2-so2

	delta = timedelta(days=1)
	date1=date_assign
	date2=date_expect
	while date1 < date2:
		daf = date1.weekday()
		godf=calendar.day_name[daf]
		if(godf=="Sunday"):
			diff=diff-1
		date1 += delta

	delta2 = timedelta(days=1)
	date3=date_assign
	while date3 < now:
		daf1 = date3.weekday()
		godf1=calendar.day_name[daf1]
		if(godf1=="Sunday"):
			diff2=diff2-1
		date3 += delta2	

	daf1 = date_assign.weekday()
	godf1=calendar.day_name[daf1]
	if(godf1=="Sunday"):
		diff=diff+1
		diff2=diff2+1
	else:
		diff=diff
		diff2=diff2

	
	if(diff>=1):
		diff=diff-1
		totalhours=diff*8
		aa=date_assign.replace(hour=18,minute=0,second=0)
		bb=date_expect.replace(hour=9,minute=0,second=0)
		difference1 = aa - date_assign
		firsthrs = difference1.total_seconds() / 3600
		if(firsthrs>4.5):
			firsthrs=firsthrs-0.5
		else:
			firsthrs=firsthrs

		difference2 = date_expect - bb
		secondhrs = difference2.total_seconds() / 3600
		if(secondhrs>4.5):
			secondhrs=secondhrs-0.5
		else:
			secondhrs=secondhrs

		if(diff==0):
			overall=float(firsthrs)+float(secondhrs)	
		else:
			overall=float(totalhours)+float(firsthrs)+float(secondhrs)

		if(diff2>=1):
			diff2=diff2-1
			totalhh=diff2*8
			vv2=now.replace(hour=9,minute=0,second=0)
			difference3 = now - vv2
			thirdhrs = difference3.total_seconds() / 3600
			if(thirdhrs>4.5):
				thirdhrs=thirdhrs-0.5
			else:
				thirdhrs=thirdhrs
			if(diff2==0):
				completehrs=float(firsthrs)+float(thirdhrs)
			else:
				completehrs=float(totalhh)+float(firsthrs)+float(thirdhrs)

		else:
			difference3 = now - date_assign
			hrs3 = difference3.total_seconds() / 3600
			completehrs=float(hrs3)

		arr.append({
			'calculate_hrs':overall,
			'completehrs':completehrs
		})
		
	else:	
		difference1 = date_expect - date_assign
		hrs1 = difference1.total_seconds() / 3600
		difference2 = now - date_assign
		hrs2 = difference2.total_seconds() / 3600
		overall=float(hrs1)
		completehrs=float(hrs2)
		arr.append({
			'calculate_hrs':overall,
			'completehrs':completehrs
		})
	return arr


@frappe.whitelist()
def update_allocation2(assign_date,expected,hours,actual):
	arr=[]
	date_assign = datetime.strptime(assign_date,'%Y-%m-%d %H:%M:%S')
	date_expect = datetime.strptime(expected,'%Y-%m-%d %H:%M:%S')
	actual = datetime.strptime(actual,'%Y-%m-%d %H:%M:%S')

	ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
	now = datetime.strptime(ind_time,'%Y-%m-%d %H:%M:%S')
	diff=date_diff(date_expect, date_assign)
	diff2=date_diff(actual, date_assign)

	holidays=frappe.db.sql("SELECT holiday_date FROM `tabHoliday` WHERE holiday_date>='"+str(date_assign)+"' AND holiday_date<='"+str(date_expect)+"'",as_dict=1)
	so=0
	for hh in holidays:
		va=hh.holiday_date
		dafd = va.weekday()
		godfd=calendar.day_name[dafd]
		if(godfd!="Sunday"):
		 	so=so+1
	diff=diff-so

	holidays2=frappe.db.sql("SELECT holiday_date FROM `tabHoliday` WHERE holiday_date>='"+str(date_assign)+"' AND holiday_date<='"+str(now)+"'",as_dict=1)
	so2=0
	for hh2 in holidays:
		va2=hh2.holiday_date
		dafd2 = va2.weekday()
		godfd2=calendar.day_name[dafd2]
		if(godfd2!="Sunday"):
		 	so2=so2+1
	diff2=diff2-so2

	delta = timedelta(days=1)
	date1=date_assign
	date2=date_expect
	while date1 < date2:
		daf = date1.weekday()
		godf=calendar.day_name[daf]
		if(godf=="Sunday"):
			diff=diff-1
		date1 += delta

	delta2 = timedelta(days=1)
	date3=date_assign
	while date3 < actual:
		daf1 = date3.weekday()
		godf1=calendar.day_name[daf1]
		if(godf1=="Sunday"):
			diff2=diff2-1
		date3 += delta2	

	daf1 = date_assign.weekday()
	godf1=calendar.day_name[daf1]
	if(godf1=="Sunday"):
		diff=diff+1
		diff2=diff2+1
	else:
		diff=diff
		diff2=diff2

	
	if(diff>=1):
		diff=diff-1
		totalhours=diff*8
		aa=date_assign.replace(hour=18,minute=0,second=0)
		bb=date_expect.replace(hour=9,minute=0,second=0)
		difference1 = aa - date_assign
		firsthrs = difference1.total_seconds() / 3600
		if(firsthrs>4.5):
			firsthrs=firsthrs-0.5
		else:
			firsthrs=firsthrs

		difference2 = date_expect - bb
		secondhrs = difference2.total_seconds() / 3600
		if(secondhrs>4.5):
			secondhrs=secondhrs-0.5
		else:
			secondhrs=secondhrs

		if(diff==0):
			overall=float(firsthrs)+float(secondhrs)	
		else:
			overall=float(totalhours)+float(firsthrs)+float(secondhrs)

		if(diff2>=1):
			diff2=diff2-1
			totalhh=diff2*8
			vv2=actual.replace(hour=9,minute=0,second=0)
			difference3 = actual - vv2
			thirdhrs = difference3.total_seconds() / 3600
			if(thirdhrs>4.5):
				thirdhrs=thirdhrs-0.5
			else:
				thirdhrs=thirdhrs
			if(diff2==0):
				completehrs=float(firsthrs)+float(thirdhrs)
			else:
				completehrs=float(totalhh)+float(firsthrs)+float(thirdhrs)

		else:
			difference3 = actual - date_assign
			hrs3 = difference3.total_seconds() / 3600
			completehrs=float(hrs3)

		arr.append({
			# 'calculate_hrs':overall,
			'actualcompleted':completehrs
		})

	else:	
		difference1 = date_expect - date_assign
		hrs1 = difference1.total_seconds() / 3600
		difference2 = actual - date_assign
		hrs2 = difference2.total_seconds() / 3600
		overall=float(hrs1)
		completehrs=float(hrs2)
		arr.append({
			# 'calculate_hrs':overall,
			'actualcompleted':completehrs
		})
	return arr

@frappe.whitelist()
def create_task():
	local_time=timezone("Asia/Kolkata")
	current_date=datetime.now(local_time).date()
	daf1 = current_date.weekday()
	godf1=calendar.day_name[daf1]
	if(godf1!="Sunday"):
		df=datetime.strptime(str(datetime.now().replace(hour=9,minute=00,second=00,microsecond=00)),'%Y-%m-%d %H:%M:%S')
		dt=datetime.strptime(str(df),'%Y-%m-%d %H:%M:%S')+timedelta(hours=9)
		difference = dt - df
		hrs = difference.total_seconds() / 3600
		doc=frappe.new_doc("Task Allocation")
		doc.user='venkat@wttindia.com'
		doc.employee="WTT1149"
		doc.append("works_table",{
			"type_of_work":"Update Accounts Details",
			"description":"Update "+str(current_date)+" Accounts Details",
			"from_time":df,
			"to_time":dt,
			"hours":hrs
			})
		doc.save()




@frappe.whitelist()
def clientscript(lr):
	ar=[]
	doc=frappe.get_doc("Task Allocation",str(lr))
	for i in doc.works_table:
		ar.append({
			"task_name":i.type_of_work,
			"description":i.description,
			"from_time":(i.from_time).strftime("%d/%m/%y %X"),
			"to_time":(i.to_time).strftime("%d/%m/%y %X"),
			"status":i.status,
			"points":i.gained_points
			})
	return ar


@frappe.whitelist()
def split_task(arr):
	to_python=json.loads(arr)
	for i in to_python:
		doc=frappe.new_doc("Task Allocation")
		doc.user=frappe.session.user
		doc.employee=i["employee"]
		doc.append("works_table",i)
		doc.save()
			
		frappe.db.sql("UPDATE `tabTask Split Table` Set allocated=1 WHERE name='"+str(i["split_no"])+"' ",as_dict=1)
	frappe.msgprint("Allocated")
	return arr


@frappe.whitelist()
def prabhu_task():
	local_time=timezone("Asia/Kolkata")
	ar=[]
	for i in frappe.db.sql("SELECT holiday_date FROM `tabHoliday` WHERE parent='Holiday 2023' ",as_dict=1):
		ar.append(i.holiday_date)

	for j in frappe.db.sql("SELECT lt.from_date FROM `tabLeave table`as lt,`tabLeave Request`as lr WHERE lt.parent=lr.name and lr.workflow_state!='Rejected' and lr.employee='WTT1387' ",as_dict=1):
		ar.append(j.from_date)
	aa=datetime.now(local_time)
	cc=aa.strftime("%Y-%m-%d %H:%M:%S")
	va=datetime.strptime(cc,"%Y-%m-%d %H:%M:%S")
	current_date=aa.date()
	dafd = current_date.weekday()
	godfd=calendar.day_name[dafd]
	if(godfd!="Sunday" and godfd!="Saturday"):
		if(current_date not in ar):
			dc=frappe.db.sql("SELECT * FROM `tabTask Allocation` as ta INNER JOIN `tabWork Update` as tat ON ta.name=tat.parent WHERE tat.type_of_work='2 Trade Enquiry' AND ta.date='"+str(current_date)+"'")
			if(dc):
				pass
			else:

				df=datetime.strptime(str(va.replace(hour=9,minute=00,second=00,microsecond=00)),'%Y-%m-%d %H:%M:%S')
				dt=datetime.strptime(str(df),'%Y-%m-%d %H:%M:%S')+timedelta(hours=9)
				difference = dt - df
				hrs = difference.total_seconds() / 3600
				doc=frappe.new_doc("Task Allocation")
				doc.user='venkat@wttindia.com'
				doc.employee='WTT1387'
				doc.append("works_table",{
					"type_of_work":"2 Trade Enquiry",
					"from_time":df,
					"to_time":dt,
					"hours":hrs
					})
				doc.save()	

@frappe.whitelist()
def raghul_task():
	local_time=timezone("Asia/Kolkata")
	ar=[]
	for i in frappe.db.sql("SELECT holiday_date FROM `tabHoliday` WHERE parent='Holiday 2023' ",as_dict=1):
		ar.append(i.holiday_date)
	for j in frappe.db.sql("SELECT lt.from_date FROM `tabLeave table`as lt,`tabLeave Request`as lr WHERE lt.parent=lr.name and lr.workflow_state!='Rejected' and lr.employee='WTT1278' ",as_dict=1):
		ar.append(j.from_date)
	aa=datetime.now(local_time)
	cc=aa.strftime("%Y-%m-%d %H:%M:%S")
	va=datetime.strptime(cc,"%Y-%m-%d %H:%M:%S")
	current_date=aa.date()
	dafd = current_date.weekday()
	godfd=calendar.day_name[dafd]
	if(godfd!="Sunday" and godfd!="Saturday"):
		if(current_date not in ar):
			dc=frappe.db.sql("SELECT * FROM `tabTask Allocation` as ta INNER JOIN `tabWork Update` as tat ON ta.name=tat.parent WHERE tat.type_of_work='5 Cutomer Followup' AND ta.date='"+str(current_date)+"'")
			if(dc):
				pass
			else:
				df=datetime.strptime(str(va.replace(hour=9,minute=00,second=00,microsecond=00)),'%Y-%m-%d %H:%M:%S')
				dt=datetime.strptime(str(df),'%Y-%m-%d %H:%M:%S')+timedelta(hours=9)
				difference = dt - df
				hrs = difference.total_seconds() / 3600
				doc=frappe.new_doc("Task Allocation")
				doc.user='venkat@wttindia.com'
				doc.employee='WTT1278'
				doc.append("works_table",{
					"type_of_work":"5 Cutomer Followup",
					"from_time":df,
					"to_time":dt,
					"hours":hrs
					})
				doc.save()

@frappe.whitelist()
def sivakumar_task():
	local_time=timezone("Asia/Kolkata")
	ar=[]
	for i in frappe.db.sql("SELECT holiday_date FROM `tabHoliday` WHERE parent='Holiday 2023' ",as_dict=1):
		ar.append(i.holiday_date)
	for j in frappe.db.sql("SELECT lt.from_date FROM `tabLeave table`as lt,`tabLeave Request`as lr WHERE lt.parent=lr.name and lr.workflow_state!='Rejected' and lr.employee='WTT1211' ",as_dict=1):
		ar.append(j.from_date)
	aa=datetime.now(local_time)
	cc=aa.strftime("%Y-%m-%d %H:%M:%S")
	va=datetime.strptime(cc,"%Y-%m-%d %H:%M:%S")
	current_date=aa.date()
	dafd = current_date.weekday()
	godfd=calendar.day_name[dafd]
	if(godfd!="Sunday" and godfd!="Saturday"):
		if(current_date not in ar):
			dc=frappe.db.sql("SELECT * FROM `tabTask Allocation` as ta INNER JOIN `tabWork Update` as tat ON ta.name=tat.parent WHERE tat.type_of_work='Department Meeting Update' AND ta.date='"+str(current_date)+"'")
			if(dc):
				pass
			else:
				df=datetime.strptime(str(va.replace(hour=9,minute=00,second=00,microsecond=00)),'%Y-%m-%d %H:%M:%S')
				dt=datetime.strptime(str(df),'%Y-%m-%d %H:%M:%S')+timedelta(hours=9)
				difference = dt - df
				hrs = difference.total_seconds() / 3600
				doc=frappe.new_doc("Task Allocation")
				doc.user='venkat@wttindia.com'
				doc.employee='WTT1211'
				doc.append("works_table",{
					"type_of_work":"Department Meeting Update",
					"description":"Update "+str(current_date)+" Department Meeting",
					"from_time":df,
					"to_time":dt,
					"hours":hrs
					})
				doc.save()

@frappe.whitelist()
def ajith_task():
	local_time=timezone("Asia/Kolkata")
	ar=[]
	for i in frappe.db.sql("SELECT holiday_date FROM `tabHoliday` WHERE parent='Holiday 2023' ",as_dict=1):
		ar.append(i.holiday_date)
	for j in frappe.db.sql("SELECT lt.from_date FROM `tabLeave table`as lt,`tabLeave Request`as lr WHERE lt.parent=lr.name and lr.workflow_state!='Rejected' and lr.employee='WTT1348' ",as_dict=1):
		ar.append(j.from_date)
	aa=datetime.now(local_time)
	cc=aa.strftime("%Y-%m-%d %H:%M:%S")
	va=datetime.strptime(cc,"%Y-%m-%d %H:%M:%S")
	current_date=aa.date()
	dafd = current_date.weekday()
	godfd=calendar.day_name[dafd]
	if(godfd!="Sunday" and godfd!="Saturday"):
		if(current_date not in ar):
			dc=frappe.db.sql("SELECT * FROM `tabTask Allocation` as ta INNER JOIN `tabWork Update` as tat ON ta.name=tat.parent WHERE tat.type_of_work='Daily Update' AND ta.date='"+str(current_date)+"'")
			if(dc):
				pass
			else:
				df=datetime.strptime(str(va.replace(hour=9,minute=00,second=00,microsecond=00)),'%Y-%m-%d %H:%M:%S')
				dt=datetime.strptime(str(df),'%Y-%m-%d %H:%M:%S')+timedelta(hours=10)
				difference = dt - df
				hrs = difference.total_seconds() / 3600
				doc=frappe.new_doc("Task Allocation")
				doc.user='venkat@wttindia.com'
				doc.employee='WTT1348'
				doc.append("works_table",{
					"type_of_work":"Daily Update",
					"description":"Update Team Performance",
					"from_time":df,
					"to_time":dt,
					"hours":hrs
					})
				doc.save()

	# ar=[]
	# local_time=timezone("Asia/Kolkata")
	# aa=datetime.now(local_time)
	# cc=aa.strftime("%Y-%m-%d %H:%M:%S")
	# va=datetime.strptime(cc,"%Y-%m-%d %H:%M:%S")
	# today=aa.date()
	# d1 = datetime.strptime(str(today), '%Y-%m-%d')
	# f_date=d1.replace(hour=0,minute=0,second=0,microsecond=0)
	# t_date=d1.replace(hour=23,minute=0,second=0,microsecond=0)
	# val=frappe.db.sql("SELECT name,lead_name,category,contact_by FROM `tabInquiries` WHERE contact_date>='"+str(f_date)+"' and contact_date<='"+str(t_date)+"'",as_dict=1)
	# for i in val:
	# 	ar.append(str(i.lead_name)+" - "+str(i.category)+" ("+str(i.name)+")")

	# st = today.strftime("%d-%m-%Y")
	# message="Today Follow-ups: "+str(st)+"<br><br>"
	# for j in ar:
	# 	message+=j+"<br>"
	
	# email_args = {
	# 	"reply_to":"trading@wttindia.com",
	# 	"recipients": "trading@wttindia.com",
	# 	"cc":"purchase@wttindia.com",
	# 	"message":message,
	# 	"subject": "Inquiries"
	# 	}
	# if not frappe.flags.in_test:
	# 	enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
	# else:
	# 	frappe.sendmail(**email_args)
