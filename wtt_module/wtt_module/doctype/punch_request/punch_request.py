import frappe
import calendar
import time
from datetime import datetime 
from datetime import  date,timedelta
from frappe.model.document import Document
from frappe.utils import getdate
from pytz import timezone
import calendar
class Punchrequest(Document):
	def validate(self):
		self.month = str(getdate(self.from_date).strftime("%B"))
	def on_submit(self):
		_from_date = datetime.strptime(self.from_date,"%Y-%m-%d %H:%M:%S")
		pdate=_from_date.date()	
		tdate=date.today()
		if(pdate==tdate):
			frappe.throw("Attendance is not marked Today")
		if(self.punch == "IN"):
			go=_from_date.date()
			query=frappe.db.sql("SELECT in_time,out_time FROM `tabAttendance` WHERE employee='"+self.employee+"' and attendance_date='"+str(go)+"'",as_dict=1)
			for k in query:
				if k.in_time is not None:
					sri=_from_date.replace(hour=9,minute=10,second=00)
					diff = k.out_time - _from_date
					hrs = diff.total_seconds() / 3600

					if(k.in_time<_from_date):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")

					elif(k.in_time>_from_date and _from_date<sri):
						if(hrs>=8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',punch_late_entry='Late Entry Was Removed ',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',in_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',late_entry=0 WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
						elif(hrs<3):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',punch_late_entry='Late Entry Was Removed ',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',in_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',late_entry=0 WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
						elif(hrs<8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',punch_late_entry='Late Entry Was Removed ',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',in_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',late_entry=0 WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")

					elif(k.in_time>_from_date):
						if(hrs>=8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',in_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
						elif(hrs<3):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',in_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
						elif(hrs<8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',in_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")

				elif k.out_time is not None:

					diff = k.out_time - _from_date
					hrs = diff.total_seconds() / 3600
					if(hrs>=8):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',in_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
					elif(hrs<3):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',in_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
					elif(hrs<8):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',in_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")

				elif k.in_time is None:
					val=frappe.db.sql("UPDATE `tabAttendance` SET status='"+self.att_status+"',in_time='"+str(_from_date)+"',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"' ")
				
		
		elif(self.punch == "OUT"):
			go=_from_date.date()
			query=frappe.db.sql("SELECT in_time,out_time FROM `tabAttendance` WHERE employee='"+self.employee+"' and attendance_date='"+str(go)+"'",as_dict=1)
			for k in query:
				if k.out_time is not None:
					sri=_from_date.replace(hour=17,minute=00,second=00)
					diff = _from_date - k.in_time 
					hrs = diff.total_seconds() / 3600

					if(k.out_time>_from_date):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")

					elif(k.out_time<_from_date and k.out_time<sri and _from_date>sri):
						if(hrs>=8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',punch_early_exit='Early Exit Was Removed ',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',out_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',early_exit=0 WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
						elif(hrs<3):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',punch_early_exit='Early Exit Was Removed ',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',out_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',early_exit=0 WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
						elif(hrs<8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',punch_early_exit='Early Exit Was Removed ',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',out_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',early_exit=0 WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")

					elif(k.out_time<_from_date):
						if(hrs>=8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',out_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
						elif(hrs<3):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',out_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
						elif(hrs<8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"',out_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")

				elif k.in_time is not None:

					diff = _from_date - k.in_time
					hrs = diff.total_seconds() / 3600
					if(hrs>=8):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',out_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
					elif(hrs<3):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',out_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")
					elif(hrs<8):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',out_time='"+str(_from_date)+"',working_hours='"+str(hrs)+"',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"'")

				elif k.out_time is None:
					val=frappe.db.sql("UPDATE `tabAttendance` SET status='"+self.att_status+"',out_time='"+str(_from_date)+"',punch_time='"+str(_from_date)+"',punch_type='"+str(self.punch)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(go)+"' ")