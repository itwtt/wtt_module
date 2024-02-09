

import math
from datetime import date, timedelta

import frappe
from frappe import _, msgprint
from frappe.model.naming import make_autoname
from frappe.query_builder import Order
from frappe.query_builder.functions import Sum
from frappe.utils import (
	add_days,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_first_day,
	get_link_to_form,
	getdate,
	money_in_words,
	rounded,
)
from frappe.utils.background_jobs import enqueue

import erpnext
from erpnext.accounts.utils import get_fiscal_year
from erpnext.loan_management.doctype.loan_repayment.loan_repayment import (
	calculate_amounts,
	create_repayment_entry,
)
from erpnext.loan_management.doctype.process_loan_interest_accrual.process_loan_interest_accrual import (
	process_loan_interest_accrual_for_term_loans,
)
from erpnext.utilities.transaction_base import TransactionBase

from hrms.hr.utils import get_holiday_dates_for_employee, validate_active_employee
from hrms.payroll.doctype.additional_salary.additional_salary import get_additional_salaries
from hrms.payroll.doctype.employee_benefit_application.employee_benefit_application import (
	get_benefit_component_amount,
)
from hrms.payroll.doctype.employee_benefit_claim.employee_benefit_claim import (
	get_benefit_claim_amount,
	get_last_payroll_period_benefits,
)
from hrms.payroll.doctype.payroll_entry.payroll_entry import get_start_end_dates
from hrms.payroll.doctype.payroll_period.payroll_period import (
	get_payroll_period,
	get_period_factor,
)

from frappe.utils import getdate
import calendar
from pytz import timezone
from datetime import date,datetime,timedelta
import functools
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip
class customSalarySlip(SalarySlip):

	
	def get_working_days_details(self, joining_date=None, relieving_date=None, lwp=None, for_preview=0):
		super().get_working_days_details()
		payroll_based_on = frappe.db.get_value("Payroll Settings", None, "payroll_based_on")
		include_holidays_in_total_working_days = frappe.db.get_single_value("Payroll Settings", "include_holidays_in_total_working_days")

		working_days = date_diff(self.end_date, self.start_date) + 1
		holidays = self.get_holidays_for_employee(self.start_date, self.end_date)
		if not cint(include_holidays_in_total_working_days):
			working_days -= len(holidays)
			if working_days < 0:
				frappe.throw(_("There are more holidays than working days this month."))

		if not payroll_based_on:
			frappe.throw(_("Please set Payroll based on in Payroll settings"))

		if payroll_based_on == "Attendance":
			actual_lwp, absent = self.calculate_lwp_ppl_and_absent_days_based_on_attendance(holidays, relieving_date)
			#self.absent_days = absent
		else:
			actual_lwp = self.calculate_lwp_or_ppl_based_on_leave_application(holidays, working_days)

		if not lwp:
			lwp = actual_lwp
		elif lwp != actual_lwp:
			frappe.msgprint(_("Leave Without Pay does not match with approved {} records")
				.format(payroll_based_on))

		self.leave_without_pay = lwp
		self.total_working_days = working_days

		payment_days = self.get_payment_days(joining_date,
			relieving_date, include_holidays_in_total_working_days)

		if flt(payment_days) > flt(lwp):
			self.payment_days = flt(payment_days) - flt(lwp)
			ccount=0
			if include_holidays_in_total_working_days:
				if not holidays:
					pass
				else:
					# holidays.sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")))
					ae=[]
					ae1=[]
					count=0
					
					for i in range(len(holidays)):
						d1 = datetime.strptime(holidays[i], '%Y-%m-%d')
						dti = d1.strftime('%Y-%m-%d %H:%M:%S')
						days_before = (d1-timedelta(days=1))
						days_after = (d1+timedelta(days=1))
						dbf = days_before.weekday()
						godb=calendar.day_name[dbf]
						daf = days_after.weekday()
						godf=calendar.day_name[daf]
						if(godb=="Sunday"):
							days_before = (days_before-timedelta(days=1))
						if(godf=="Sunday"):
							days_after = (days_after+timedelta(days=1))

						ae.append(days_before)
						ae1.append(days_after)
	
					
					vv=[]
					vv1=[]
					for j in range(len(holidays)):
						if ((frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": ae[j].date()}))):
							if(ae[j].date() not in vv):
								vv.append(ae[j].date())
						if ((frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": ae1[j].date()}))):
							if(ae1[j].date() not in vv1):
								vv1.append(ae1[j].date())
					deduct=[]
					for s in range(len(vv)):
						for k in frappe.db.sql("SELECT count(distinct(holiday_date))as days FROM `tabHoliday` WHERE holiday_date>='"+str(vv[s])+"' AND holiday_date<='"+str(vv1[s])+"'",as_dict=1):
							# res = functools.reduce(lambda sub, ele: sub * 10 + ele, k)
							deduct.append(k.days)
					hhcount=0
					for ku in range(len(vv)):
						if((frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": vv[ku],"status":"Absent"})) and (frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": vv1[ku],"status":"Absent"}))):
							hhcount=hhcount
						else:
							hhcount=hhcount+int(deduct[ku])
					ccount=hhcount

			if payroll_based_on == "Attendance":
				uninformed_leave=0
				el=frappe.get_value('Employee',self.employee,'eligible_leave')
				bl=el
				eeee=0
				elcr=0
				sl_cnt=0
				cl_cnt=0
				bl_cnt=0
				enl_cnt=0
				start=str(self.start_date)
				end=str(self.end_date)
				
				query1=frappe.db.sql("SELECT attendance_date,in_time,out_time FROM `tabAttendance` WHERE employee='"+str(self.employee)+"' and status='Absent' and attendance_date>='"+str(start)+"' and attendance_date<='"+str(end)+"'",as_dict=1)
				query3=frappe.db.sql("SELECT attendance_date,in_time,out_time FROM `tabAttendance` WHERE employee='"+str(self.employee)+"' and status='Half Day' and attendance_date>='"+str(start)+"' and attendance_date<='"+str(end)+"'",as_dict=1)
				
				if(query1):
					for j in query1:
						atd = getdate(j.attendance_date).weekday()
						atk=calendar.day_name[atd]
						if(atk!="Sunday"):
							query4=frappe.db.sql("SELECT * FROM `tabLeave Request` as lr INNER JOIN `tabLeave table` as lt on lr.name=lt.parent WHERE lr.employee='"+str(self.employee)+"' and lt.from_date='"+str(j.attendance_date)+"' and lr.workflow_state!='Created' and lr.workflow_state!='Rejected' and lr.workflow_state!='Approved by HOD' and lr.workflow_state!='Cancelled'",as_dict=1)
							if not query4:
								uninformed_leave+=1
								elcr=elcr+1
							else:
								for i in query4:
									if(i.leave_type=="Balance Leave"):
										bl_cnt+=float(i.no_of_days)
									elif(i.leave_type=="Sick Leave"):
										sl_cnt+=float(i.no_of_days)
									elif(i.leave_type=="Casual Leave"):
										cl_cnt+=float(i.no_of_days)
									elif(i.leave_type=="Earned Leave"):
										enl_cnt+=float(i.no_of_days)
				if(query3):
					chalf=0
					ar=[]
					for j in query3:
						atd = getdate(j.attendance_date).weekday()
						atk=calendar.day_name[atd]
						if(atk!="Sunday"):
							chalf=frappe.db.sql("SELECT count(name) as nna FROM `tabEmployee Checkin` WHERE time>='"+str(j.attendance_date)+" 00:00:00' and time<='"+str(j.attendance_date)+" 23:00:00' and employee='"+str(self.employee)+"'",as_dict=1)
							for i in chalf:
							
								# if(i.nna<3):		
								query6=frappe.db.sql("SELECT * FROM `tabLeave Request` as lr INNER JOIN `tabLeave table` as lt on lr.name=lt.parent WHERE lr.employee='"+str(self.employee)+"' and lt.from_date='"+str(j.attendance_date)+"' and lr.workflow_state!='Created' and lr.workflow_state!='Rejected' and lr.workflow_state!='Approved by HOD' and lr.workflow_state!='Cancelled'",as_dict=1)
								if not query6:
									uninformed_leave+=0.5
								else:
									for i in query6:
										if(i.leave_type=="Balance Leave"):
											bl_cnt+=0.5
										elif(i.leave_type=="Sick Leave"):
											sl_cnt+=0.5
										elif(i.leave_type=="Casual Leave"):
											cl_cnt+=0.5
										elif(i.leave_type=="Earned Leave"):
											enl_cnt+=0.5	

					
							
						


				start=str(self.start_date)
				end=str(self.end_date)
				d1 = datetime.strptime(start, '%Y-%m-%d')
				d2 = datetime.strptime(end, '%Y-%m-%d')
				week_day=6
				v=0
				num_weeks, remainder = divmod((d2-d1).days, 7)
				if ( week_day - d1.weekday() ) % 7 <= remainder:
					v=num_weeks + 1
				else:
					v=num_weeks
				cnt=0
				for holiday in holidays:
					cnt=cnt+1	

				unmarked_days = self.get_unmarked_days(include_holidays_in_total_working_days)
				jd = frappe.db.get_value("Employee",str(self.employee),"date_of_joining")
				if(getdate(jd)>getdate(self.start_date)):
					unmarked_days += date_diff(jd,self.start_date)

				
				val=0
				mrgcnt=0
				mrgcnt2=0

				suncount=0
				halfsuncount=0
				st_date = str(self.start_date)
				ed_date = str(self.end_date)
				date1 = datetime.strptime(st_date, '%Y-%m-%d')
				date2 = datetime.strptime(ed_date, '%Y-%m-%d')
				delta = timedelta(days=1)
				while date1 <= date2:
					daf = date1.weekday()
					godf=calendar.day_name[daf]
					if(godf=="Sunday"):
						if(frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": date1,"status":"Present","docstatus": 1 })):
							suncount=suncount+1
						elif(frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": date1,"status":"Half Day","docstatus": 1 })):
							halfsuncount=halfsuncount+1
					date1 += delta
				# frappe.msgprint(str(suncount+halfsuncount))
				
				
				attsuncount=0
				qu=frappe.db.sql("SELECT attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(self.start_date)+"' AND attendance_date<='"+str(self.end_date)+"' AND status='Absent' AND employee='"+self.employee+"'",as_dict=1)
				for i in qu:
					date1 = i.attendance_date
					daf = date1.weekday()
					godf=calendar.day_name[daf]
					if(godf=="Sunday"):
						attsuncount=attsuncount+1

				mrgcnt=0
				mrgcnt2=0
				gracecnt=0
				if(self.branch=="HEAD OFFICE"):
					for j in frappe.db.sql("SELECT in_time,attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(self.start_date)+"' AND attendance_date<='"+str(self.end_date)+"' AND employee='"+self.employee+"' AND late_entry!=0 AND status='Present'",as_dict=1):	
						date1 = j.attendance_date
						daf = date1.weekday()
						godf=calendar.day_name[daf]
						if(godf!="Sunday"):
							x = datetime.now().time().replace(hour=9,minute=20,second=0,microsecond=0)
							z = datetime.now().time().replace(hour=9,minute=1,second=0,microsecond=0)
							el = datetime.now().time().replace(hour=11,minute=00,second=0,microsecond=0)

							if(j.in_time.time()>x and j.in_time.time()<=el):
								mrgcnt=mrgcnt+1
							elif(j.in_time.time()>z and j.in_time.time()<=el):
								mrgcnt2=mrgcnt2+1
							else:
								mrgcnt=mrgcnt
								mrgcnt2=mrgcnt2



					
					for j in frappe.db.sql("SELECT in_time,attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(self.start_date)+"' AND attendance_date<='"+str(self.end_date)+"' AND employee='"+self.employee+"' AND late_entry!=0 AND status='Half Day'",as_dict=1):
						date1 = j.attendance_date
						daf = date1.weekday()
						godf=calendar.day_name[daf]
						if(godf!="Sunday"):
							x = datetime.now().time().replace(hour=9,minute=20,second=0,microsecond=0)
							y = datetime.now().time().replace(hour=14,minute=30,second=0,microsecond=0)
							z = datetime.now().time().replace(hour=9,minute=1,second=0,microsecond=0)
							w = datetime.now().time().replace(hour=13,minute=31,second=0,microsecond=0)
							el = datetime.now().time().replace(hour=11,minute=00,second=0,microsecond=0)
					
							if((j.in_time.time()>x and j.in_time.time()<=el)):
								mrgcnt=mrgcnt+1
							elif(j.in_time.time()>y):
								mrgcnt=mrgcnt+1
							elif(j.in_time.time()>w):
								mrgcnt2=mrgcnt2+1
							elif((j.in_time.time()>z and j.in_time.time()<=el)):
								mrgcnt2=mrgcnt2+1
							else:
								mrgcnt=mrgcnt
								mrgcnt2=mrgcnt2				

					
					mrgtotal=mrgcnt+((mrgcnt2-gracecnt)/3)
					over=mrgtotal
					go=int(over)					

					vv=0
					overall_total=0
					if(go>0):
						vv=(go/2)
						overall_total=vv
				else:				
					for j in frappe.db.sql("SELECT in_time,attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(self.start_date)+"' AND attendance_date<='"+str(self.end_date)+"' AND employee='"+self.employee+"' AND late_entry!=0 AND status='Present'",as_dict=1):	
						date1 = j.attendance_date
						daf = date1.weekday()
						godf=calendar.day_name[daf]
						if(godf!="Sunday"):
							x = datetime.now().time().replace(hour=9,minute=20,second=0,microsecond=0)
							z = datetime.now().time().replace(hour=9,minute=1,second=0,microsecond=0)
							el = datetime.now().time().replace(hour=11,minute=00,second=0,microsecond=0)
							if(j.in_time.time()>x and j.in_time.time()<=el):
								mrgcnt=mrgcnt+1
							elif(j.in_time.time()>z and j.in_time.time()<=el):
								mrgcnt2=mrgcnt2+1
							else:
								mrgcnt=mrgcnt
								mrgcnt2=mrgcnt2

					
					for j in frappe.db.sql("SELECT in_time,attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(self.start_date)+"' AND attendance_date<='"+str(self.end_date)+"' AND employee='"+self.employee+"' AND late_entry!=0 AND status='Half Day'",as_dict=1):
						date1 = j.attendance_date
						daf = date1.weekday()
						godf=calendar.day_name[daf]
						if(godf!="Sunday"):
							x = datetime.now().time().replace(hour=9,minute=20,second=0,microsecond=0)
							y = datetime.now().time().replace(hour=15,minute=00,second=0,microsecond=0)
							z = datetime.now().time().replace(hour=9,minute=1,second=0,microsecond=0)
							w = datetime.now().time().replace(hour=14,minute=31,second=0,microsecond=0)
							el = datetime.now().time().replace(hour=11,minute=00,second=0,microsecond=0)
					
							if((j.in_time.time()>x and j.in_time.time()<=el)):
								mrgcnt=mrgcnt+1
							elif(j.in_time.time()>y):
								mrgcnt=mrgcnt+1
							elif(j.in_time.time()>w):
								mrgcnt2=mrgcnt2+1
							elif((j.in_time.time()>z and j.in_time.time()<=el)):
								mrgcnt2=mrgcnt2+1
							else:
								mrgcnt=mrgcnt
								mrgcnt2=mrgcnt2

					mrgtotal=mrgcnt+((mrgcnt2-gracecnt)/3)
					over=mrgtotal
					go=int(over)

					vv=0
					overall_total=0
					if(go>0):
						vv=(go/2)
						overall_total=vv
				sd = getdate(self.start_date)
				ed = getdate(self.end_date)
				worked_sundays = 0
				while sd<=ed:
					daf = sd.weekday()
					godf=calendar.day_name[daf]
					if(godf=="Sunday"):
						if(frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": sd,"status":"Present","docstatus": 1 })):
							worked_sundays += 1
						elif(frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": sd,"status":"Half Day","docstatus": 1 })):
							worked_sundays +=0.5
					sd+=timedelta(days=1)
				res=[]
				for i in frappe.db.sql("SELECT employee from `tabResignation` ",as_dict=1):
					res.append(i.employee)
				if(self.employee in res):
					cl_cnt=0
					enl_cnt=0
					sl_cnt=0
					bl_cnt=0
				elsum=cl_cnt+enl_cnt+sl_cnt+bl_cnt
				holidays_in_sundays=self.holidays_in_sundays_function()
				# frappe.msgprint(str(holidays_in_sundays))
				if(self.employee=="WTT1385"):
					ccount=0
				val=self.total_working_days-(flt(absent)+unmarked_days+lwp)
				self.punched_days=val
				self.uninformed_leave=uninformed_leave
				if((val+ccount)>=20):
					sun_cal=(val-worked_sundays+ccount-holidays_in_sundays)/6
					if(sun_cal>=3.6):
						total_pay=val+v+elsum+ccount    #removed sunday because the sunday status were changed
						self.actual_payment_days=total_pay
						self.payment_days=total_pay-overall_total-suncount-(halfsuncount/2)
						self.actual_absent_days=total_pay-self.actual_payment_days
						if((self.total_working_days)-self.payment_days+elsum<0):
							self.absent_days=(self.total_working_days)-self.payment_days+elsum+1
						else:
							self.absent_days=(self.total_working_days)-self.payment_days+elsum
						self.loss_of_pay=self.absent_days-elsum
						self.sundays=v
						self.approval_leave=elsum
						self.redeemed_bl=bl_cnt
						self.casual_leave=cl_cnt
						self.sick_leave=sl_cnt
						self.earned_leave=enl_cnt
						self.late_deduction=overall_total
						self.national_holidays=cnt
						self.nh_given=ccount
					else:
						sun_cal=0.5*math.floor((((val-worked_sundays+ccount-holidays_in_sundays)/3)*0.5)/0.5)
						total_pay=val+sun_cal+ccount+elsum
						self.actual_payment_days=total_pay
						self.payment_days=total_pay-overall_total-suncount-(halfsuncount/2)
						self.actual_absent_days=total_pay-self.actual_payment_days
						if((self.total_working_days)-self.payment_days+elsum<0):
							self.absent_days=(self.total_working_days)-self.payment_days+elsum+1
						else:
							self.absent_days=(self.total_working_days)-self.payment_days+elsum
						self.loss_of_pay=self.absent_days-elsum
						self.sundays=sun_cal
						self.approval_leave=elsum
						self.redeemed_bl=bl_cnt
						self.casual_leave=cl_cnt
						self.sick_leave=sl_cnt
						self.earned_leave=enl_cnt
						self.late_deduction=overall_total
						self.national_holidays=cnt
						self.nh_given=ccount

				else:
					sun_cal=0.5*math.floor((((val+ccount-worked_sundays-holidays_in_sundays)/3)*0.5)/0.5)
					total_pay=val+sun_cal+ccount+elsum
					self.actual_payment_days=total_pay
					self.payment_days=total_pay-overall_total-suncount-(halfsuncount/2)
					self.actual_absent_days=total_pay-self.actual_payment_days
					if((self.total_working_days)-self.payment_days+elsum<0):
						self.absent_days=(self.total_working_days)-self.payment_days+elsum+1
					else:
						self.absent_days=(self.total_working_days)-self.payment_days+elsum
					self.loss_of_pay=self.absent_days-elsum
					self.sundays=sun_cal
					self.approval_leave=elsum
					self.redeemed_bl=bl_cnt
					self.casual_leave=cl_cnt
					self.sick_leave=sl_cnt
					self.earned_leave=enl_cnt
					self.late_deduction=overall_total
					self.national_holidays=cnt
					self.nh_given=ccount
				if(self.absent_days-elsum<0):
					self.loss_of_pay=0


			# frappe.msgprint("absent : "+str(absent)+"; lwp : "+str(lwp)+" ; unmarked_days : "+str(unmarked_days)+" ; Sundays : "+str(v)+" ; LATE : "+str(overall_total)+" ; NH : "+str(ccount)+" ; PL : "+str(elsum)+" ; BL : "+str(bl_cnt)+" ;CL : "+str(cl_cnt)+" ; SL : "+str(sl_cnt)+" ; working_days : "+str(self.total_working_days)+ " ; Payment: "+str(payment_days))
			
			consider_unmarked_attendance_as = frappe.db.get_value("Payroll Settings", None, "consider_unmarked_attendance_as") or "Present"

			if payroll_based_on == "Attendance" and consider_unmarked_attendance_as =="Absent":
				#self.absent_days += unmarked_days #will be treated as absent
				#self.payment_days -= unmarked_days
				if include_holidays_in_total_working_days:
					if not holidays:
						pass
					else:
						# holidays.sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")))
						ae=[]
						ae1=[]
						count=0
						hhcount=0
						hocount=0
						for i in range(len(holidays)):
							hocount=hocount+1
						for i in range(len(holidays)):
							d1 = datetime.strptime(holidays[i], '%Y-%m-%d')
							dti = d1.strftime('%Y-%m-%d %H:%M:%S')
							days_before = (d1-timedelta(days=1))
							days_after = (d1+timedelta(days=1))
							dbf = days_before.weekday()
							godb=calendar.day_name[dbf]
							daf = days_after.weekday()
							godf=calendar.day_name[daf]
							if(godb=="Sunday"):
								days_before = (days_before+timedelta(days=1))
							if(godf=="Sunday"):
								days_after = (days_after+timedelta(days=1))
							ae.append(days_before)
							ae1.append(days_after)

						vv=[]
						vv1=[]
						for j in range(len(holidays)):
							if ((frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": ae[j].date()}))):
								vv.append(ae[j].date())
							if ((frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": ae1[j].date()}))):
								vv1.append(ae1[j].date())

						deduct=[]
						for s in range(len(vv)):
							for k in frappe.db.sql("SELECT count(holiday_date) FROM `tabHoliday` WHERE holiday_date>='"+str(vv[s])+"' AND holiday_date<='"+str(vv1[s])+"'"):
								res = functools.reduce(lambda sub, ele: sub * 10 + ele, k)
								deduct.append(res)
						
						hhcount=0
						for ku in range(len(vv)):
							if((frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": vv[ku],"status":"Absent"})) and (frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": vv1[ku],"status":"Absent"}))):
								hhcount=hhcount+deduct[ku]
							else:
								hhcount=hhcount
			else:
				self.payment_days = 0

	def validate(self):
		super().validate()
		self.ot_calculation()
		self.sunday_working()
		self.new_policy()
		self.month = getdate(self.posting_date).strftime("%B")
		if(self.punched_days>=23.3):
			self.earned_leave_for_next_year=1
		else:
			self.earned_leave_for_next_year=0
		super().validate()
		if(self.workflow_state=="Verified by HR" and self.verified_by==None):
			self.update_leave_by_hr()
			self.verified_by=frappe.session.user_fullname
			if(self.employee not in ["WTT1410","WTT1430","WTT915","WTT917","INT5015","WTT1442","WTT1090","WTT1449","WTT1454","WTT1459"]):
				self.check_pms_record()



	
	def ot_calculation(self):
		salary=0
		query=frappe.db.sql("SELECT amount FROM `tabSalary Detail` WHERE parenttype='Salary Structure' AND parentfield='earnings' AND parent='"+str(self.salary_structure)+"'",as_dict=1)
		for i in query:
			salary+=float(i.amount)
		holicnt=0
		gug=0
		holidays = self.get_holidays_for_employee(self.start_date, self.end_date)
		for holiday in holidays:
			date1 = datetime.strptime(holiday, '%Y-%m-%d')
			date2=date1.replace(hour=23,minute=00,second=0,microsecond=0)
			for j in frappe.db.sql("SELECT employee,hours,from_time,to_time FROM `tabOn duty request` WHERE from_time>='"+str(date1)+"' AND to_time<='"+str(date2)+"' AND employee='"+self.employee+"' AND workflow_state='Approved'",as_dict=1):
				f_date=j.from_time.replace(hour=13,minute=00,second=0,microsecond=0)
				f_date2=j.to_time.replace(hour=13,minute=30,second=0,microsecond=0)
				if(frappe.db.sql("SELECT * FROM `tabOT Prior Information`as otp,`tabOvertime table`as otpt where otp.name=otpt.parent and otpt.employee='"+str(self.employee)+"' and otp.docstatus=1 and otp.date='"+str(date1)+"' ",as_dict=1)):
					if(j.hours<8.00):
						if(j.from_time>f_date):
							holicnt=((salary/self.total_working_days)/8)*j.hours
						else:
							# gug=j.hours-0.5
							gug=j.hours
							holicnt=((salary/self.total_working_days)/8)*gug				
					else:
						holicnt=int(salary)/self.total_working_days

		if(self.branch=="HEAD OFFICE"):
			ot=0
			gug1=0
			otdate1 = datetime.strptime(str(self.start_date), '%Y-%m-%d')
			otdate2 = datetime.strptime(str(self.end_date), '%Y-%m-%d')
			otdate3 = otdate2.replace(hour=23,minute=00,second=0,microsecond=0)
			for k in frappe.db.sql("SELECT hours,from_time,to_time FROM `tabOT request`  WHERE from_time>='"+str(otdate1)+"' AND to_time<='"+str(otdate3)+"' AND employee='"+self.employee+"' AND workflow_state='Approved'",as_dict=1):
				# if(frappe.db.sql("SELECT * FROM `tabOT Prior Information`as otp,`tabOvertime table`as otpt where otp.name=otpt.parent and otpt.employee='"+str(self.employee)+"' and otp.docstatus=1 and otp.date='"+str(otdate1)+"' ",as_dict=1)):
				if(k.hours<8.00):
					ot=ot+(((salary/self.total_working_days)/8)*k.hours)			
				else:
					ot=ot+(int(salary)/self.total_working_days)
			gug3=0	
			for i in self.get('earnings'):
				if (i.salary_component=='OT calculation'):
					gug3=gug3+1	
			if (gug3==0):
				if(ot>0):
					row=self.append('earnings',{})
					row.salary_component='OT calculation'
					row.amount=ot
		else:
			ot=0
			gug1=0
			otdate1 = datetime.strptime(str(self.start_date), '%Y-%m-%d')
			otdate2 = datetime.strptime(str(self.end_date), '%Y-%m-%d')
			otdate3 = otdate2.replace(hour=23,minute=00,second=0,microsecond=0)
			for k in frappe.db.sql("SELECT employee,hours,from_time,to_time FROM `tabOT request`  WHERE from_time>='"+str(otdate1)+"' AND from_time<='"+str(otdate3)+"' AND employee='"+self.employee+"' AND workflow_state='Approved'",as_dict=1):	
				# if(frappe.db.sql("SELECT * FROM `tabOT Prior Information`as otp,`tabOvertime table`as otpt where otp.name=otpt.parent and otpt.employee='"+str(self.employee)+"' and otp.docstatus=1 and otp.date='"+str(otdate1)+"' ",as_dict=1)):
				ot=ot+(((salary/self.total_working_days)/8)*k.hours)			
			gug3=0	
			for i in self.get('earnings'):
				if (i.salary_component=='OT calculation'):
					gug3=gug3+1	
			if (gug3==0):		
				if(ot>0):
					row=self.append('earnings',{})
					row.salary_component='OT calculation'
					row.amount=ot

		gug4=0	
		for i in self.get('earnings'):
			if (i.salary_component=='Holiday working'):
				gug4=gug4+1	
		if (gug4==0):
			if(holicnt>0):
				row=self.append('earnings',{})
				row.salary_component='Holiday working'
				row.amount=holicnt

	def sunday_working(self):
		salary=0
		query=frappe.db.sql("SELECT amount FROM `tabSalary Detail` WHERE parenttype='Salary Structure' AND parentfield='earnings' AND parent='"+str(self.salary_structure)+"'",as_dict=1)
		for i in query:
			salary+=float(i.amount)
		suncountsave=0
		halfsuncountsave=0
		total_amt=0
		date1 = datetime.strptime(str(self.start_date), '%Y-%m-%d')
		date2 = datetime.strptime(str(self.end_date), '%Y-%m-%d')
		delta = timedelta(days=1)
		while date1 <= date2:
			daf = date1.weekday()
			godf=calendar.day_name[daf]
			if(godf=="Sunday"):
				if(frappe.db.sql("SELECT * FROM `tabOT Prior Information`as otp,`tabOvertime table`as otpt where otp.name=otpt.parent and otpt.employee='"+str(self.employee)+"' and otp.docstatus=1 and otp.date='"+str(date1)+"' ",as_dict=1)):
					if(frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": date1,"status":"Present","docstatus": 1 })):
						suncountsave=suncountsave+1
					elif(frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": date1,"status":"Half Day","docstatus": 1 }) or frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": date1,"working_hours":[">",0],"docstatus": 1 })):
						for dd in frappe.db.sql("SELECT working_hours FROM `tabAttendance` WHERE attendance_date='"+str(date1)+"' and employee='"+self.employee+"'",as_dict=1):
							total_amt=total_amt+((salary/self.total_working_days)/8)*dd.working_hours
			date1 += delta
		gug5=0
		for i in self.get('earnings'):
			if (i.salary_component=='Additional working'):
				gug5=gug5+1	
		if (gug5==0):
			if(total_amt!=0):
				row=self.append('earnings',{})
				row.salary_component='Additional working'
				row.amount=total_amt


			if(suncountsave>0):
				total=int(salary)/self.total_working_days
				if(total!=0):
					row=self.append('earnings',{})
					row.salary_component='Additional working'
					row.amount=total*suncountsave

	def on_submit(self):
		super().on_submit()
		self.email_salary_slip()
	
	def email_salary_slip(self):
		receiver = frappe.db.get_value("Employee", self.employee, "personal_email")
		payroll_settings = frappe.get_single("Payroll Settings")
		message=f"<html>Dear <b>"+str(self.employee_name)+"</b>,<br><br>Please find the Salary Slip for the month of <b>"+str(self.month)+" - 2023</b> attached with this mail.<br><br><u><i>Let’s work with more cheerfulness towards achieving our goal !!</i></u><br><br>Thanks & Regards,<br>HR - WTT"
		password = None
		if payroll_settings.encrypt_salary_slips_in_emails:
			password = generate_password_for_pdf(payroll_settings.password_policy, self.employee)
			message += """<br>Note: Your salary slip is password protected,
				the password to unlock the PDF is of the format {0}. """.format(payroll_settings.password_policy)

		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": _(message),
				"subject": 'Salary Slip - from {0} to {1}'.format(self.start_date, self.end_date),
				"attachments": [frappe.attach_print(self.doctype, self.name, file_name=self.name, password=password)],
				"reference_doctype": self.doctype,
				"reference_name": self.name
				}
			if not frappe.flags.in_test:
				enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
		else:
			msgprint(_("{0}: Employee email not found, hence email not sent").format(self.employee_name))

	def update_sick_leave(self):
		if(frappe.db.sql("SELECT name from `tabLeave Allocation` WHERE docstatus=1 and employee='"+str(self.employee)+"' and leave_type='Sick Leave' ",as_dict=1)):
			doc=frappe.get_doc("Leave Allocation",{"employee":self.employee,"leave_type":"Sick Leave"})
			doc.balance_leave=doc.balance_leave-self.sick_leave
			doc.save()

	def update_casual_leave(self):
		if(self.casual_leave>0):
			if(frappe.db.sql("SELECT * from `tabCasual Leave` where employee='"+str(self.employee)+"' ",as_dict=1)):
				cl_doc=frappe.get_doc("Casual Leave",str(self.employee))
				cl_doc.append('casual_leave_table',{
					"date":self.posting_date,
					"leave_approved":self.casual_leave
					})
				cl_doc.save()
			else:
				cl_doc=frappe.new_doc("Casual Leave")
				cl_doc.employee=self.employee
				cl_doc.append('casual_leave_table',{
					"date":self.posting_date,
					"leave_approved":self.casual_leave
					})
				cl_doc.save()

	def new_policy(self):
		ar=[]
		br=[]
		for j in self.deductions:
			ar.append(j.salary_component)
		if("Punch Missed" not in ar):
			self.punch_miss_deduction()
		if("Cancelled Weekoff" not in ar):
			# self.saturday_sunday()
			pass
		if("Uninformed Leave" not in ar):
			self.uninformed_leave_()
			# pass
		for i in self.earnings:
			br.append(i.salary_component)
		self.incident()
		if("Expense Claim" not in br and "Advance" not in ar):
			self.expense_claim()
		# self.attendance_bonus()

	def punch_miss_deduction(self):
		punch_raised = frappe.db.count('Checkin Request', {'month': str(getdate(self.posting_date).strftime("%B")),'employee':self.employee,'workflow_state':'Approved'})
		punch_raised = punch_raised-2
		salary=0
		query=frappe.db.sql("""SELECT amount 
			FROM `tabSalary Detail` 
			WHERE parenttype='Salary Structure' 
			AND parentfield='earnings' 
			AND parent='"""+str(self.salary_structure)+"""' 
			""",as_dict=1)
		for i in query:
			salary+=float(i.amount)

		self.punch_raised = punch_raised

		if(punch_raised>5):
			self.append("deductions",{
				"salary_component":"Punch Missed",
				"amount":str(float(salary)/float(self.total_working_days))
				})
		elif(punch_raised>2):
			self.append("deductions",{
				"salary_component":"Punch Missed",
				"amount":str((float(salary)/float(self.total_working_days))*((punch_raised)*0.1))
				})

	def add_el_cl(self):
		if(self.earned_leave_for_next_year>0):
			self.add_earned_leave()

	def add_earned_leave(self):
		if(frappe.db.sql("SELECT name from `tabLeave Allocation` WHERE docstatus!=2 and employee='"+str(self.employee)+"' and leave_type='Earned Leave' ",as_dict=1)):
			doc=frappe.get_doc("Leave Allocation",{"employee":self.employee,"leave_type":"Earned Leave"})
			doc.new_leaves_allocated=doc.new_leaves_allocated+self.earned_leave_for_next_year
			doc.balance_leave=doc.balance_leave+self.earned_leave_for_next_year
			doc.save()
		else:
			doc=frappe.new_doc("Leave Allocation")
			doc.employee=self.employee
			doc.start_date="2023-01-01"
			doc.end_date="2023-12-31"
			doc.leave_type="Earned Leave"
			doc.new_leaves_allocated=self.earned_leave_for_next_year
			doc.balance_leave=self.earned_leave_for_next_year
			doc.save()
	def add_casual_leave(self):
		if(frappe.db.sql("SELECT name from `tabLeave Allocation` WHERE docstatus!=2 and employee='"+str(self.employee)+"' and leave_type='Casual Leave' ",as_dict=1)):
			doc=frappe.get_doc("Leave Allocation",{"employee":self.employee,"leave_type":"Casual Leave"})
			doc.new_leave_allocated=doc.new_leave_allocated+self.earned_leave_for_next_year
			doc.balance=doc.balance+self.earned_leave_for_next_year
			doc.save()
		else:
			doc=frappe.new_doc("Leave Allocation")
			doc.employee=self.employee
			doc.start_date="2023-01-01"
			doc.end_date="2023-12-31"
			doc.leave_type="Casual Leave"
			doc.new_leave_allocated=doc.new_leave_allocated+self.earned_leave_for_next_year
			doc.balance=doc.balance+self.earned_leave_for_next_year
			doc.save()

	def expense_claim(self):
		self.claim_reference=[]
		self.advance_reference=[]
		claim_query = frappe.db.sql(""" SELECT sum(grand_total) as total
			FROM `tabClaim Request`
			WHERE employee='"""+str(self.employee)+"""' and workflow_state='Approved' and 
			is_paid=0 and posting_date>='2023-03-01' """,as_dict=1)

		advance_query = frappe.db.sql(""" SELECT sum(advance_amount) as total
			FROM `tabEmployee Advance`
			WHERE employee='"""+str(self.employee)+"""' and docstatus=1 and 
			posting_date>='"""+str(self.start_date)+"""' and posting_date<='"""+str(self.end_date)+"""' """,as_dict=1)

		if(claim_query):
			amt=0
			if(advance_query[0].total!=None and claim_query[0].total!=None):
				amt=claim_query[0].total-advance_query[0].total
			elif(claim_query[0].total!=None):
				amt=claim_query[0].total
			elif(advance_query[0].total!=None):
				amt=advance_query[0].total*(-1)

			if(amt>0):
				self.append("earnings",{
					"salary_component":"Expense Claim",
					"amount":amt
					})
			elif(amt<0):
				self.append("deductions",{
					"salary_component":"Advance",
					"amount":amt*(-1)
					})

			claim_reference = frappe.db.sql(""" SELECT grand_total,name as claim_request,posting_date
				FROM `tabClaim Request`
				WHERE employee='"""+str(self.employee)+"""' and workflow_state='Approved' and 
				is_paid=0 and posting_date>='2023-03-01' """,as_dict=1)
			if(claim_reference):
				for i in claim_reference:
					self.append("claim_reference",i)

			advance_reference = frappe.db.sql(""" SELECT name as "employee_advance",advance_amount as "grand_total",posting_date
				FROM `tabEmployee Advance`
				WHERE employee='"""+str(self.employee)+"""' and docstatus=1 and 
				posting_date>='"""+str(self.start_date)+"""' and posting_date<='"""+str(self.end_date)+"""' """,as_dict=1)
			if(advance_reference):
				for i in advance_reference:
					self.append("advance_reference",i)
		
	def incident(self):
		ded = 0
		query = frappe.db.sql("""SELECT count(distinct(name))as count,incident
			FROM `tabIncident Record` 
			WHERE against_employee='"""+str(self.employee)+"""'
			and report_date>='"""+str(self.start_date)+"""' and report_date<='"""+str(self.end_date)+"""' group by incident """,as_dict=1)
		for i in query:
			if(i.incident=="ID Card"):
				ded+=(i.count*200)

			if(i.incident=="Mobile Usage"):
				ded+=(i.count*200)

			if(i.incident=="Damaged Document"):
				salary=0
				query=frappe.db.sql("""SELECT amount 
					FROM `tabSalary Detail` 
					WHERE parenttype='Salary Structure' 
					AND parentfield='earnings' 
					AND parent='"""+str(self.salary_structure)+"""' 
					""",as_dict=1)
				for j in query:
					salary+=float(j.amount)
				if(self.department=="Accounts - WTT"):
					ded+=(float(salary)/float(self.total_working_days))*15
				else:
					ded+=(float(salary)/float(self.total_working_days))*7
		if(ded>0):
			self.append("deductions",{
				"salary_component":"Incident Record",
				"amount":ded
				})
				
	def saturday_sunday(self):
		remove_sunday=0
		salary=0
		query=frappe.db.sql("""SELECT amount 
			FROM `tabSalary Detail` 
			WHERE parenttype='Salary Structure' 
			AND parentfield='earnings' 
			AND parent='"""+str(self.salary_structure)+"""' 
			""",as_dict=1)
		for i in query:
			salary+=float(i.amount)

		aa=getdate(self.start_date)
		bb=getdate(self.end_date)
		holiday=[]
		sat_dates=[]
		mon_dates=[]
		for i in frappe.db.sql("""SELECT distinct(child.holiday_date)as holiday_date
			FROM `tabHoliday`as child,`tabHoliday List`as parent 
			WHERE parent.name=child.parent and parent.from_date<='"""+str(self.posting_date)+"""' and parent.to_date>='"""+str(self.posting_date)+"""'
			""",as_dict=1):
			holiday.append(i.holiday_date)
		while aa<bb:
			if(calendar.day_name[aa.weekday()]=="Saturday"):
				if(aa not in holiday):
					sat_dates.append(aa)
				else:
					sat_sates.append(aa-timedelta(days=1))
			if(calendar.day_name[aa.weekday()]=="Monday"):
				if(aa not in holiday):
					mon_dates.append(aa)
				else:
					mon_dates.append(aa+timedelta(days=1))

			aa+=timedelta(days=1)
		ll_dd=sat_dates
		if(len(mon_dates)>len(sat_dates)):
			ll_dd=mon_dates
		
				
		for d1 in range(len(mon_dates)):
			data1=frappe.db.get_value("Attendance",{'employee':self.employee,'attendance_date':str(sat_dates[d1])},'status')
			data2=frappe.db.get_value("Attendance",{'employee':self.employee,'attendance_date':str(mon_dates[d1])},'status')
			if(data1=="Absent"):
				if not (frappe.db.sql("SELECT * from `tabLeave Request`as lr,`tabLeave table` as lt WHERE lt.parent=lr.name and lt.from_date!='"+str(sat_dates[d1])+"' and lr.docstatus!=2 and lr.workflow_state!='Created' and lr.workflow_state!='Rejected' ",as_dict=1)):
					remove_sunday=remove_sunday+1
			elif(data2=="Absent"):
				if not (frappe.db.sql("SELECT * from `tabLeave Request`as lr,`tabLeave table` as lt WHERE lt.parent=lr.name and lt.from_date!='"+str(mon_dates[d1])+"' and lr.docstatus!=2 and lr.workflow_state!='Created' and lr.workflow_state!='Rejected' ",as_dict=1)):
					remove_sunday=remove_sunday+1
		if(remove_sunday>0 and (float(salary)/float(self.total_working_days))*remove_sunday>0):
			self.append("deductions",{
				"salary_component":"Cancelled Weekoff",
				"amount":(float(salary)/float(self.total_working_days))*remove_sunday
				})

	def uninformed_leave_(self):
		salary=0
		query=frappe.db.sql("SELECT amount FROM `tabSalary Detail` WHERE parenttype='Salary Structure' AND parentfield='earnings' AND parent='"+str(self.salary_structure)+"'",as_dict=1)
		for i in query:
			salary+=float(i.amount)
		ul=self.uninformed_leave

		for i in frappe.db.sql("SELECT uninformed_leave as ul,deducted as leave_deducted,name FROM `tabSalary Slip` WHERE posting_date>'2023-01-01' and posting_date<'"+str(self.posting_date)+"' and docstatus=1 and employee='"+self.employee+"' GROUP BY employee ORDER BY posting_date DESC LIMIT 1",as_dict=1):
			if(i.leave_deducted==0):
				ul+=i.ul
			for j in frappe.db.sql("SELECT uninformed_leave as ul,deducted as leave_deducted FROM `tabSalary Slip` WHERE posting_date>'2023-01-01' and posting_date<'"+str(self.posting_date)+"' and name!='"+str(i.name)+"' and docstatus=1 and employee='"+self.employee+"' GROUP BY employee ORDER BY posting_date DESC LIMIT 1",as_dict=1):
				if(j.leave_deducted==0):
					ul+=j.ul
		# frappe.msgprint(str(ul))
		ar=[]
		for j in self.deductions:
			ar.append(j.salary_component)
		if(ul>2 and "Uninformed Leave" not in ar):
			self.deducted = 1
			self.append("deductions",{
				"salary_component":"Uninformed Leave",
				"amount":(float(salary)/float(self.total_working_days))*5
				})
		super().validate()

	def check_pms_record(self):
		aa=getdate(self.posting_date)
		current_year=aa.year
		month_name = aa.strftime("%B")
		if not frappe.db.exists("Technical Criteria", {"employee": self.employee, "month": month_name,"docstatus": 1,"year":current_year }):
			frappe.throw("PMS Record is not found "+str(self.employee_name)+" (Technical)")
			 
		if not frappe.db.exists("Behavioural Criteria", {"employee": self.employee, "month": month_name,"docstatus": 1,"year":current_year }):
			frappe.throw("PMS Record is not found "+str(self.employee_name)+" (Behavioural)")

	def attendance_bonus(self):
		ab = 0
		aa=0
		if(self.loss_of_pay==0):
			for i in frappe.db.sql("SELECT count(loss_of_pay)as lop,count(attendance_bonus_check)as abc FROM `tabSalary Slip` WHERE docstatus=1 and employee='"+str(self.employee)+"' GROUP BY employee ORDER BY posting_date DESC LIMIT 11 ",as_dict=1):
				if(i.abc<1):
					if(i.lop==0):
						aa+=1
						ab=12
			if(aa==0):
				for i in frappe.db.sql("SELECT count(loss_of_pay)as lop,count(attendance_bonus_check)as abc FROM `tabSalary Slip` WHERE docstatus=1 and employee='"+str(self.employee)+"' GROUP BY employee ORDER BY posting_date DESC LIMIT 5 ",as_dict=1):
					if(i.abc<1):
						if(i.lop==0):
							aa+=1
							ab=5
			if(aa==0):
				for i in frappe.db.sql("SELECT count(loss_of_pay)as lop,count(attendance_bonus_check)as abc FROM `tabSalary Slip` WHERE docstatus=1 and employee='"+str(self.employee)+"' GROUP BY employee ORDER BY posting_date DESC LIMIT 2 ",as_dict=1):
					if(i.abc<1):
						if(i.lop==0):
							aa+=1
							ab=2

		self.earned_leave_for_next_year = self.earned_leave_for_next_year+ab
	
	def update_balance_leave(self):
		el_lev=self.approval_leave
		bl_cnt=self.redeemed_bl
		
		if(frappe.db.sql("SELECT * FROM `tabBalance Leave` WHERE employee='"+str(self.employee)+"' ",as_dict=1)):
			doc=frappe.get_doc("Balance Leave",{"employee":self.employee})
			doc.append("balance_leave_table",{
				"posting_date":self.posting_date,
				"balance_leave":0,
				"taken_el":el_lev,
				"taken_bl":bl_cnt
				})
			doc.save()
		else:
			doc=frappe.new_doc("Balance Leave")
			doc.employee=self.employee
			doc.append("balance_leave_table",{
				"posting_date":self.posting_date,
				"balance_leave":0,
				"taken_el":el_lev,
				"taken_bl":bl_cnt
				})
			doc.save()

	def holidays_in_sundays_function(self):
		aa=getdate(self.start_date)
		bb=getdate(self.end_date)
		holiday_dates=[]
		for i in frappe.db.sql("""SELECT distinct(child.holiday_date)as holiday_date
			FROM `tabHoliday`as child,`tabHoliday List`as parent 
			WHERE parent.name=child.parent and parent.from_date<='"""+str(self.posting_date)+"""' and parent.to_date>='"""+str(self.posting_date)+"""'
			and child.holiday_date>='"""+str(aa)+"""' and child.holiday_date<='"""+str(bb)+"""'
			""",as_dict=1):
			if (calendar.day_name[getdate(i.holiday_date).weekday()]=="Sunday"):
				if(frappe.db.get_value("Attendance",{'employee':self.employee,'attendance_date':getdate(i.holiday_date)-timedelta(days=1)},'status')!='Absent' and frappe.db.get_value("Attendance",{'employee':self.employee,'attendance_date':getdate(i.holiday_date)+timedelta(days=1)},'status')!='Absent'):
					holiday_dates.append(i.holiday_date)
		
		return len(holiday_dates)
	def update_leave_by_hr(self):
		self.update_balance_leave()
		self.update_sick_leave()
		self.update_casual_leave()
		for i in self.claim_reference:
			frappe.db.sql("UPDATE `tabClaim Request` SET is_paid=1 WHERE name='"+str(i.claim_request)+"' ")
	@frappe.whitelist()
	def update_leave(self):
		self.update_balance_leave()
		self.update_sick_leave()
		self.update_casual_leave()
		for i in self.claim_reference:
			frappe.db.sql("UPDATE `tabClaim Request` SET is_paid=1 WHERE name='"+str(i.claim_request)+"' ")

	@frappe.whitelist()## created for javascript frappe call on verified by hr workflow state before_workflow_action(frm){}
	def update_salary_slip(self):
		if(self.employee not in ["WTT1410","WTT1430","WTT915","WTT917","INT5015","WTT1442","WTT1090","WTT1449","WTT1454","WTT1459","WTT1464","WTT1466"]):
			self.check_pms_record()

	@frappe.whitelist()
	def email_sal_slip(self):
		receiver = frappe.db.get_value("Employee", self.employee, "personal_email")
		payroll_settings = frappe.get_single("Payroll Settings")
		message=f"<html>Dear <b>"+str(self.employee_name)+"</b>,<br><br>Please find the Salary Slip for the month of <b>"+str(self.month)+" - 2023</b> attached with this mail.<br><br><u><i>Let’s work with more cheerfulness towards achieving our goal !!</i></u><br><br>Thanks & Regards,<br>HR - WTT"
		password = None
		if payroll_settings.encrypt_salary_slips_in_emails:
			password = generate_password_for_pdf(payroll_settings.password_policy, self.employee)
			message += """<br>Note: Your salary slip is password protected,
				the password to unlock the PDF is of the format {0}. """.format(payroll_settings.password_policy)

		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": _(message),
				"subject": 'Salary Slip - from {0} to {1}'.format(self.start_date, self.end_date),
				"attachments": [frappe.attach_print(self.doctype, self.name, file_name=self.name, password=password)],
				"reference_doctype": self.doctype,
				"reference_name": self.name
				}
			if not frappe.flags.in_test:
				enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
		else:
			msgprint(_("{0}: Employee email not found, hence email not sent").format(self.employee_name))

	@frappe.whitelist()
	def update_balance_leave(self):
		el_lev=self.approval_leave
		bl_cnt=self.redeemed_bl
		
		if(frappe.db.sql("SELECT * FROM `tabBalance Leave` WHERE employee='"+str(self.employee)+"' ",as_dict=1)):
			doc=frappe.get_doc("Balance Leave",{"employee":self.employee})
			doc.append("balance_leave_table",{
				"posting_date":self.posting_date,
				"balance_leave":0,
				"taken_el":el_lev,
				"taken_bl":bl_cnt
				})
			doc.save()
		else:
			doc=frappe.new_doc("Balance Leave")
			doc.employee=self.employee
			doc.append("balance_leave_table",{
				"posting_date":self.posting_date,
				"balance_leave":0,
				"taken_el":el_lev,
				"taken_bl":bl_cnt
				})
			doc.save()

	@frappe.whitelist()
	def update_sick_leave(self):
		if(frappe.db.sql("SELECT name from `tabLeave Allocation` WHERE docstatus=1 and employee='"+str(self.employee)+"' and leave_type='Sick Leave' ",as_dict=1)):
			doc=frappe.get_doc("Leave Allocation",{"employee":self.employee,"leave_type":"Sick Leave"})
			doc.balance_leave=doc.balance_leave-self.sick_leave
			doc.save()

	@frappe.whitelist()
	def update_casual_leave(self):
		if(self.casual_leave>0):
			if(frappe.db.sql("SELECT * from `tabCasual Leave` where employee='"+str(self.employee)+"' ",as_dict=1)):
				cl_doc=frappe.get_doc("Casual Leave",str(self.employee))
				cl_doc.append('casual_leave_table',{
					"date":self.posting_date,
					"leave_approved":self.casual_leave
					})
				cl_doc.save()
			else:
				cl_doc=frappe.new_doc("Casual Leave")
				cl_doc.employee=self.employee
				cl_doc.append('casual_leave_table',{
					"date":self.posting_date,
					"leave_approved":self.casual_leave
					})
				cl_doc.save()
