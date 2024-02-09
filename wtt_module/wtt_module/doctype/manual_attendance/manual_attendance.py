# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
import calendar
import datetime
import time
from datetime import datetime 
from datetime import  date,timedelta
from frappe.model.document import Document
from frappe.utils import getdate
from pytz import timezone

class ManualAttendance(Document):
	pass


@frappe.whitelist()
def get_active(nn):
	ar=[]
	for i in frappe.db.sql("SELECT * FROM `tabEmployee` WHERE status='Active' and department not in ('MD - WTT','House keeping - WTT')",as_dict=1):
		ar.append({
			'emp':i.employee
		})
	return ar



@frappe.whitelist()
def update_att(mn_detail):
	to_python = json.loads(mn_detail)
	lst = []
	item = []
	mr=[]
	v=[]
	for mm in to_python:
		datetime1_start=datetime.strptime(str(mm['from_time']),"%Y-%m-%d %H:%M:%S")
		datetime2_end=datetime.strptime(str(mm['to_time']),"%Y-%m-%d %H:%M:%S")
		to_diff = datetime2_end - datetime1_start
		fl_hrs = to_diff.total_seconds() / 3600

		sri=datetime1_start.replace(hour=9,minute=1,second=00)
		start=datetime1_start.date()
		tdate=datetime.now()
		gug=start.weekday()
		dayname=calendar.day_name[gug]
		if(start==tdate.date()):
			frappe.throw("Attendance is not marked Today")
		query=frappe.db.sql("SELECT name,in_time,out_time,working_hours,status,shift FROM `tabAttendance` WHERE employee='"+mm['employee']+"' and attendance_date='"+str(start)+"'",as_dict=1)
		
		for k in query:
			if(k.shift=='workshop shift'):
				early=datetime1_start.replace(hour=19,minute=00,second=00)
				if(k.in_time is None and k.out_time is None):
					if(datetime2_end>early):
						diff = early - datetime1_start
						diff1 = datetime2_end - datetime1_start 
					else:
						diff = diff1 = datetime2_end - datetime1_start
					hrs = diff.total_seconds() / 3600
					act_hrs = diff1.total_seconds() / 3600

					if(datetime1_start<=sri and datetime2_end>=early):
						if(hrs>=9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Present',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"'")
						elif(hrs<4):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Absent',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")					
						elif(hrs<9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Half Day',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
							
					elif(datetime1_start>sri and datetime2_end>early):
						if(hrs>=9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Present',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"'")
						elif(hrs<4):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Absent',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")					
						elif(hrs<9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Half Day',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
							
					elif(datetime1_start>sri and datetime2_end<early):
						if(hrs>=9):					
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,early_exit=1,od_late_entry='Late Entry Marked',od_early_exit='Early Exit Marked',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<4):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,early_exit=1,od_late_entry='Late Entry Marked',od_early_exit='Early Exit Marked',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,early_exit=1,od_late_entry='Late Entry Marked',od_early_exit='Early Exit Marked',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")

					elif(datetime1_start<sri and datetime2_end<early):
						if(hrs>=9):					
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<4):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")

					elif(datetime1_start>sri):
						if(hrs>=9):					
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<4):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
					elif(datetime2_end<early):
						if(hrs>=9):					
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<4):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")

				elif k.in_time is not None and k.out_time is not None and k.out_time>datetime2_end:
					
					diff = k.out_time - datetime1_start
					hrs = diff.total_seconds() / 3600

					if(k.in_time<datetime1_start):						
						if(k.working_hours>=9):					
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(k.working_hours<4):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(k.working_hours<9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")

					elif(k.in_time>datetime1_start and k.in_time>sri and datetime1_start<sri):
						if(hrs>=9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_late_entry='Late Entry Removed ',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',late_entry=0 WHERE name='"+str(k.name)+"' ")
						elif(hrs<4):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_late_entry='Late Entry Removed ',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',late_entry=0 WHERE name='"+str(k.name)+"' ")
						elif(hrs<9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_late_entry='Late Entry Removed ',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',late_entry=0 WHERE name='"+str(k.name)+"' ")

					elif(k.in_time>datetime1_start):
						if(hrs>=9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<4):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"' WHERE name='"+str(k.name)+"' ")

				elif k.in_time is None:
					
					if(k.out_time>=early):
						diff = early - datetime1_start
						diff1 = k.out_time - datetime1_start 
					else:
						diff = diff1 = k.out_time - datetime1_start
					hrs = diff.total_seconds() / 3600
					act_hrs = diff1.total_seconds() / 3600
					if(datetime1_start>sri):
						if(hrs>=9):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',late_entry=1 WHERE name='"+str(k.name)+"' ")
						elif(hrs<4):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',late_entry=1 WHERE name='"+str(k.name)+"' ")
						elif(hrs<9):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',late_entry=1 WHERE name='"+str(k.name)+"' ")
					else:
						if(hrs>=9):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<4):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<9):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
					if(k.out_time>early):
						frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"' WHERE name='"+str(k.name)+"' ")
				elif k.out_time is None:
					if(k.in_time<datetime1_start):
						out_diff=datetime2_end - k.in_time
						out_diff2=early - k.in_time
						intym=k.in_time
					else:
						out_diff=datetime2_end - datetime1_start
						out_diff2=early - datetime1_start
						intym=datetime1_start
					hrs2=out_diff.total_seconds() / 3600
					hrs3=out_diff2.total_seconds() / 3600

					if(datetime2_end<early):
						if(hrs2>=9):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs2<4):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs2<9):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
					else:
						if(hrs3>=9):
							val=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Present',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs3<4):
							val=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Absent',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs3<9):
							val=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Half Day',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
				
				elif k.out_time is not None:
					
					out_diff=datetime2_end - k.in_time
					out_diff2=early - k.in_time
					hrs2=out_diff.total_seconds() / 3600
					hrs3=out_diff2.total_seconds() / 3600

					if(k.out_time>datetime2_end):
						if(k.working_hours>=9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(k.working_hours<4):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(k.working_hours<9):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")

					elif(k.out_time<datetime2_end and k.out_time<early):
						if(datetime2_end>=early):
							if(hrs3>=9):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")
							elif(hrs3<4):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")
							elif(hrs3<9):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")

							
						elif(datetime2_end<early):
							if(hrs2>=9):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")
							elif(hrs2<4):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")
							elif(hrs2<9):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")

					elif(k.out_time<datetime2_end):
						if(datetime2_end>=early):
							if(hrs3>=9):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")
							elif(hrs3<4):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")
							elif(hrs3<9):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")

							
						elif(datetime2_end<early):
							if(hrs2>=9):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")
							elif(hrs2<4):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")
							elif(hrs2<9):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")
						

				if(k.out_time!=None and k.out_time>early):
					if(k.in_time<datetime1_start):
						tt=k.in_time
						diff = early - tt
						diff1 = k.out_time - tt
						hrs = diff.total_seconds() / 3600
						act_hrs = diff1.total_seconds() / 3600
						upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',working_hours='"+str(hrs)+"' WHERE name='"+str(k.name)+"' ")
					elif(k.in_time>datetime1_start):
						tt=datetime1_start
						diff = early - tt
						diff1 = k.out_time - tt
						hrs = diff.total_seconds() / 3600
						act_hrs = diff1.total_seconds() / 3600
						upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',working_hours='"+str(hrs)+"' WHERE name='"+str(k.name)+"' ")

			elif(k.shift=='Day Shift'):
				if(dayname!='Saturday'):
					early=datetime1_start.replace(hour=18,minute=00,second=00)
					ff=7.5
				elif(dayname=='Saturday'):
					early=datetime1_start.replace(hour=17,minute=00,second=00)
					ff=7
				if(k.in_time is None and k.out_time is None):
					if(datetime2_end>early):
						diff = early - datetime1_start
						diff1 = datetime2_end - datetime1_start 
					else:
						diff = diff1 = datetime2_end - datetime1_start
					hrs = diff.total_seconds() / 3600
					act_hrs = diff1.total_seconds() / 3600
					if(datetime1_start<=sri and datetime2_end>=early):
						if(hrs>=ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Present',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"'")
						elif(hrs<3.5):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Absent',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")					
						elif(hrs<ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Half Day',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
							
					elif(datetime1_start>sri and datetime2_end>early):
						if(hrs>=ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Present',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"'")
						elif(hrs<3.5):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Absent',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")					
						elif(hrs<ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',status='Half Day',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
							
					elif(datetime1_start>sri and datetime2_end<early):
						if(hrs>=ff):					
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,early_exit=1,od_late_entry='Late Entry Marked',od_early_exit='Early Exit Marked',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<3.5):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,early_exit=1,od_late_entry='Late Entry Marked',od_early_exit='Early Exit Marked',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,early_exit=1,od_late_entry='Late Entry Marked',od_early_exit='Early Exit Marked',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")

					elif(datetime1_start<sri and datetime2_end<early):
						if(hrs>=ff):					
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<3.5):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")

					elif(datetime1_start>sri):
						if(hrs>=ff):					
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<3.5):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',late_entry=1,od_late_entry='Late Entry Marked',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
					elif(datetime2_end<early):
						if(hrs>=ff):					
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<3.5):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',in_time='"+str(datetime1_start)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs)+"',early_exit=1,od_early_exit='Early Exit Marked',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")

				elif k.in_time is not None and k.out_time is not None and k.out_time>datetime2_end:
					
					diff = k.out_time - datetime1_start
					hrs = diff.total_seconds() / 3600

					if(k.in_time<datetime1_start):						
						if(k.working_hours>=ff):					
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(k.working_hours<3.5):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(k.working_hours<ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")

					elif(k.in_time>datetime1_start and k.in_time>sri and datetime1_start<sri):
						if(hrs>=ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_late_entry='Late Entry Removed ',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',late_entry=0 WHERE name='"+str(k.name)+"' ")
						elif(hrs<3.5):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_late_entry='Late Entry Removed ',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',late_entry=0 WHERE name='"+str(k.name)+"' ")
						elif(hrs<ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_late_entry='Late Entry Removed ',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',late_entry=0 WHERE name='"+str(k.name)+"' ")

					elif(k.in_time>datetime1_start):
						if(hrs>=ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<3.5):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"' WHERE name='"+str(k.name)+"' ")

				elif k.in_time is None:
					
					if(k.out_time>=early):
						diff = early - datetime1_start
						diff1 = k.out_time - datetime1_start 
					else:
						diff = diff1 = k.out_time - datetime1_start
					hrs = diff.total_seconds() / 3600
					act_hrs = diff1.total_seconds() / 3600
					if(datetime1_start>sri):
						if(hrs>=ff):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',late_entry=1 WHERE name='"+str(k.name)+"' ")
						elif(hrs<3.5):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',late_entry=1 WHERE name='"+str(k.name)+"' ")
						elif(hrs<ff):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',late_entry=1 WHERE name='"+str(k.name)+"' ")
					else:
						if(hrs>=ff):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<3.5):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs<ff):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',in_time='"+str(datetime1_start)+"',working_hours='"+str(hrs)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
					if(k.out_time>early):
						frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"' WHERE name='"+str(k.name)+"' ")
				elif k.out_time is None:
					if(k.in_time<datetime1_start):
						out_diff=datetime2_end - k.in_time
						out_diff2=early - k.in_time
						intym=k.in_time
					else:
						out_diff=datetime2_end - datetime1_start
						out_diff2=early - datetime1_start
						intym=datetime1_start
					hrs2=out_diff.total_seconds() / 3600
					hrs3=out_diff2.total_seconds() / 3600

					if(datetime2_end<early):
						if(hrs2>=ff):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs2<3.5):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs2<ff):
							val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
					else:
						if(hrs3>=ff):
							val=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Present',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs3<3.5):
							val=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Absent',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(hrs3<ff):
							val=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Half Day',in_time='"+str(intym)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
				
				elif k.out_time is not None:
					
					out_diff=datetime2_end - k.in_time
					out_diff2=early - k.in_time
					hrs2=out_diff.total_seconds() / 3600
					hrs3=out_diff2.total_seconds() / 3600

					if(k.out_time>datetime2_end):
						if(k.working_hours>=ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(k.working_hours<3.5):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")
						elif(k.working_hours<ff):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"' WHERE name='"+str(k.name)+"' ")

					elif(k.out_time<datetime2_end and k.out_time<early):
						if(datetime2_end>=early):
							if(hrs3>=ff):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")
							elif(hrs3<3.5):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")
							elif(hrs3<ff):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")

							
						elif(datetime2_end<early):
							if(hrs2>=ff):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")
							elif(hrs2<3.5):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")
							elif(hrs2<ff):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")

					elif(k.out_time<datetime2_end):
						if(datetime2_end>=early):
							if(hrs3>=ff):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")
							elif(hrs3<3.5):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")
							elif(hrs3<ff):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(hrs2)+"',status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs3)+"',early_exit=0,od_early_exit='Early Exit Removed' WHERE name='"+str(k.name)+"' ")

							
						elif(datetime2_end<early):
							if(hrs2>=ff):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")
							elif(hrs2<3.5):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")
							elif(hrs2<ff):
								upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',od_from_time='"+str(datetime1_start)+"',od_to_time='"+str(datetime2_end)+"',od_hours='"+str(fl_hrs)+"',out_time='"+str(datetime2_end)+"',working_hours='"+str(hrs2)+"' WHERE name='"+str(k.name)+"' ")

				if(k.out_time!=None and k.out_time>early):
					if(k.in_time<datetime1_start):
						diff = early - k.in_time
						diff1 = k.out_time - k.in_time
						hrs = diff.total_seconds() / 3600
						act_hrs = diff1.total_seconds() / 3600
						upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',working_hours='"+str(hrs)+"' WHERE name='"+str(k.name)+"' ")
					elif(k.in_time>datetime1_start):
						
						diff = early - datetime1_start
						diff1 = k.out_time - datetime1_start
						hrs = diff.total_seconds() / 3600
						act_hrs = diff1.total_seconds() / 3600
						upd=frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(early)+"',actual_working_hours='"+str(act_hrs)+"',working_hours='"+str(hrs)+"' WHERE name='"+str(k.name)+"'")
	return "Success"