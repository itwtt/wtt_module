import frappe
from datetime import datetime,timedelta
from frappe.model.document import Document

class PermissionRequest(Document):
	def validate(self):
		
		gg=0
		if(self.employee is not None):
			gg=gg+self.hours
		if(gg>2):
			frappe.throw('Sorry You are eligible for two hours Permission Only')
		else:
			pass
		vv=self.hours
		gv=1
		dd=datetime.now().replace(day=1,hour=00,minute=00,second=00)
		ab=datetime.now()
		ddd=(ab.replace(day=1) + timedelta(days=32)).replace(day=1,hour=23,minute=59,second=59) - timedelta(days=1)
		query=frappe.db.sql("SELECT name,employee,employee_name,from_time,hours from `tabPermission Request` WHERE workflow_state!='Rejected' and workflow_state!='Cancelled' and from_time >='"+str(dd)+"' and from_time <='"+str(ddd)+"' and employee='"+str(self.employee)+"' ",as_dict=1)
		for i in query:
			if (self.name==i.name):
				pass
			else:
				vv=vv+i.hours
				gv=gv+1
		
		if(gv>2):
			frappe.throw("Only Two occasions of Permission is available")
		elif(vv>2):
			frappe.throw("Sorry You are eligible for two hours Permission Only")

			

	
	def on_submit(self):
		'''gug=self.from_time.date()
		vis=frappe.db.sql("SELECT in_time FROM `tabAttendance` WHERE employee='"+self.employee+"' and attendance_date='"+str(gug)+"'",as_dict=1)
		for k in vis:
			if k.in_time is not None:
				if(k.in_time<self.from_time):
					upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',permission='Issued permission for "+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
				else:
					upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',permission='Issued permission for "+str(self.hours)+"',in_time='"+str(self.from_time)+"',late_entry=0 WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
			else:
				val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',in_time='"+str(self.from_time)+"',permission='Issued permission for "+str(self.hours)+"',late_entry=0  WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")'''

		sri=self.from_time.replace(hour=9,minute=10,second=00)
		gug=self.from_time.date()
		early=self.from_time.replace(hour=17,minute=00,second=00)
		vis=frappe.db.sql("SELECT in_time,out_time,working_hours,status FROM `tabAttendance` WHERE employee='"+self.employee+"' and attendance_date='"+str(gug)+"'",as_dict=1)
		for k in vis:
			
			if(k.status=='Absent' and k.in_time is None and k.out_time is None):
				diff = self.to_time - self.from_time
				hrs = diff.total_seconds() / 3600
				if(self.from_time<sri and self.to_time>early):
					if(hrs>=8):					
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs<3):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs<8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
				elif(self.from_time>sri and self.to_time<early):
					if(hrs>=8):					
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',late_entry=1,early_exit=1,pr_late_entry='Late Entry Marked',pr_early_exit='Early Exit Marked',status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs<3):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',late_entry=1,early_exit=1,pr_late_entry='Late Entry Marked',pr_early_exit='Early Exit Marked',status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs<8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',late_entry=1,early_exit=1,pr_late_entry='Late Entry Marked',pr_early_exit='Early Exit Marked',status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
				elif(self.from_time>sri):
					if(hrs>=8):					
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',late_entry=1,pr_late_entry='Late Entry Marked',status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs<3):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',late_entry=1,pr_late_entry='Late Entry Marked',status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs<8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',late_entry=1,pr_late_entry='Late Entry Marked',status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
				elif(self.to_time<early):
					if(hrs>=8):					
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',early_exit=1,pr_early_exit='Early Exit Marked',status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs<3):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',early_exit=1,pr_early_exit='Early Exit Marked',status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs<8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET in_time='"+str(self.from_time)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs)+"',early_exit=1,pr_early_exit='Early Exit Marked',status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")



			if k.in_time is not None and k.out_time is not None:
			
				diff = k.out_time - self.from_time
				hrs1 = diff.total_seconds() / 3600

				if(k.in_time<self.from_time):
					if(k.working_hours>=8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(k.working_hours<3):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(k.working_hours<8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					
				
				elif(k.in_time>self.from_time and k.in_time>sri and self.from_time<sri):
					if(hrs1>=8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',in_time='"+str(self.from_time)+"',working_hours='"+str(hrs1)+"',late_entry=0,pr_late_entry='Late Entry Removed'  WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs1<3):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',in_time='"+str(self.from_time)+"',working_hours='"+str(hrs1)+"',late_entry=0,pr_late_entry='Late Entry Removed'  WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs1<8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',in_time='"+str(self.from_time)+"',working_hours='"+str(hrs1)+"',late_entry=0,pr_late_entry='Late Entry Removed'  WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					
				
				elif(k.in_time>self.from_time):
					if(hrs1>=8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',in_time='"+str(self.from_time)+"',working_hours='"+str(hrs1)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs1<3):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',in_time='"+str(self.from_time)+"',working_hours='"+str(hrs1)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs1<8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',in_time='"+str(self.from_time)+"',working_hours='"+str(hrs1)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					
			elif k.in_time is None and k.status!='Absent':
				diff = k.out_time - self.from_time
				hrs1 = diff.total_seconds() / 3600
				if(hrs1>=8):
					val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',in_time='"+str(self.from_time)+"',working_hours='"+str(hrs1)+"',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.from_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
				elif(hrs1<3):
					val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',in_time='"+str(self.from_time)+"',working_hours='"+str(hrs1)+"',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.from_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
				elif(hrs1<8):
					val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',in_time='"+str(self.from_time)+"',working_hours='"+str(hrs1)+"',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.from_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
				

			if k.out_time is None and k.status!='Absent':

				srig=self.from_time.replace(hour=19,minute=00,second=00)
				out_diff=self.to_time - k.in_time
				out_diff2=srig - k.in_time
				hrs2=out_diff.total_seconds() / 3600
				hrs3=out_diff2.total_seconds() / 3600

				if(str(self.to_time<str(srig))):
					if(hrs2>=8):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs2<3):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs2<8):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					
				else:
					if(hrs3>=8):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',out_time='"+str(srig)+"',working_hours='"+str(hrs3)+"',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs3<3):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',out_time='"+str(srig)+"',working_hours='"+str(hrs3)+"',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs3<8):
						val=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',out_time='"+str(srig)+"',working_hours='"+str(hrs3)+"',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					

			elif k.out_time is not None:
				early=self.from_time.replace(hour=17,minute=00,second=00)
				srig=self.from_time.replace(hour=19,minute=00,second=00)
				out_diff=self.to_time - k.in_time
				out_diff2=srig - k.in_time
				hrs2=out_diff.total_seconds() / 3600
				hrs3=out_diff2.total_seconds() / 3600

				if(k.out_time>self.to_time):
					if(k.working_hours>=8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(k.working_hours<3):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(k.working_hours<8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					
				
				elif(k.out_time<self.to_time and k.out_time>early):
					if(self.to_time>early):
						if(hrs2>=8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"',early_exit=0,pr_early_exit='Early Exit Removed' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
						elif(hrs2<3):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"',early_exit=0,pr_early_exit='Early Exit Removed' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
						elif(hrs2<8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"',early_exit=0,pr_early_exit='Early Exit Removed' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
						
					elif(self.to_time<early):
						if(hrs2>=8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
						elif(hrs2<3):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
						elif(hrs2<8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")

				elif(k.out_time<self.to_time):
					if(self.to_time>early):
						if(hrs2>=8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"',early_exit=0,pr_early_exit='Early Exit Removed' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
						elif(hrs2<3):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"',early_exit=0,pr_early_exit='Early Exit Removed' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
						elif(hrs2<8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"',early_exit=0,pr_early_exit='Early Exit Removed' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
						
					elif(self.to_time<early):
						if(hrs2>=8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
						elif(hrs2<3):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
						elif(hrs2<8):
							upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")

						

				elif(k.out_time<self.to_time and str(self.to_time)<str(srig)):
					if(hrs2>=8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs2<3):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs2<8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(self.to_time)+"',working_hours='"+str(hrs2)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					

				elif(k.out_time<self.to_time and str(self.to_time)>str(srig)):
					if(hrs3>=8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Present',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(srig)+"',working_hours='"+str(hrs3)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs3<3):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(srig)+"',working_hours='"+str(hrs3)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					elif(hrs3<8):
						upd=frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',pr_from_time='"+str(self.from_time)+"',pr_to_time='"+str(self.to_time)+"',pr_hours='"+str(self.hours)+"',out_time='"+str(srig)+"',working_hours='"+str(hrs3)+"' WHERE employee='"+self.employee+"' AND attendance_date='"+str(gug)+"'")
					
				