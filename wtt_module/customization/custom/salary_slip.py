# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe, erpnext
import datetime, math
import calendar
import datetime
import time
from datetime import datetime 
from datetime import  date,timedelta
from frappe.utils import add_days, cint, cstr, flt, getdate, rounded, date_diff, money_in_words, formatdate, get_first_day
from frappe.model.naming import make_autoname
from frappe.utils import time_diff_in_hours
from frappe import msgprint, _
from erpnext.payroll.doctype.payroll_entry.payroll_entry import get_start_end_dates
from erpnext.hr.doctype.employee.employee import get_holiday_list_for_employee
from erpnext.utilities.transaction_base import TransactionBase
from frappe.utils.background_jobs import enqueue
from erpnext.payroll.doctype.additional_salary.additional_salary import get_additional_salaries
from erpnext.payroll.doctype.payroll_period.payroll_period import get_period_factor, get_payroll_period
from erpnext.payroll.doctype.employee_benefit_application.employee_benefit_application import get_benefit_component_amount
from erpnext.payroll.doctype.employee_benefit_claim.employee_benefit_claim import get_benefit_claim_amount, get_last_payroll_period_benefits
from erpnext.loan_management.doctype.loan_repayment.loan_repayment import calculate_amounts, create_repayment_entry
from erpnext.accounts.utils import get_fiscal_year
from six import iteritems
import itertools
import functools
from frappe.utils import getdate

class SalarySlip(TransactionBase):
	def __init__(self, *args, **kwargs):
		super(SalarySlip, self).__init__(*args, **kwargs)
		self.series = 'Sal Slip/{0}/.#####'.format(self.employee)
		self.whitelisted_globals = {
			"int": int,
			"float": float,
			"long": int,
			"round": round,
			"date": datetime.date,
			"getdate": getdate
		}

	def autoname(self):
		self.name = make_autoname(self.series)

	def validate(self):
		# self.check_pms_record()
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
				if(frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": date1,"status":"Present","docstatus": 1 })):
					suncountsave=suncountsave+1
				elif(frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": date1,"status":"Half Day","docstatus": 1 }) or frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": date1,"working_hours":[">",0],"docstatus": 1 })):
					for dd in frappe.db.sql("SELECT working_hours FROM `tabAttendance` WHERE attendance_date='"+str(date1)+"' and employee='"+self.employee+"'",as_dict=1):
						total_amt=((salary/self.total_working_days)/8)*dd.working_hours
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

		holicnt=0
		gug=0
		holidays = self.get_holidays_for_employee(self.start_date, self.end_date)
		for holiday in holidays:
			date1 = datetime.strptime(holiday, '%Y-%m-%d')
			date2=date1.replace(hour=23,minute=00,second=0,microsecond=0)
			for j in frappe.db.sql("SELECT hours,from_time,to_time FROM `tabOn duty request` WHERE from_time>='"+str(date1)+"' AND to_time<='"+str(date2)+"' AND employee='"+self.employee+"' AND workflow_state='Approved'",as_dict=1):
				f_date=j.from_time.replace(hour=13,minute=00,second=0,microsecond=0)
				f_date2=j.to_time.replace(hour=13,minute=30,second=0,microsecond=0)	
				if(j.hours<8.00):
					if(j.from_time>f_date):
						holicnt=((salary/self.total_working_days)/8)*j.hours
					else:
						gug=j.hours-0.5
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
			for k in frappe.db.sql("SELECT hours,from_time,to_time FROM `tabOT request`  WHERE from_time>='"+str(otdate1)+"' AND from_time<='"+str(otdate3)+"' AND employee='"+self.employee+"' AND workflow_state='Approved'",as_dict=1):	
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
		self.status = self.get_status()
		self.validate_dates()
		self.check_existing()
		if not self.salary_slip_based_on_timesheet:
			self.get_date_details()

		if not (len(self.get("earnings")) or len(self.get("deductions"))):
			# get details from salary structure
			self.get_emp_and_working_day_details()
		else:
			self.get_working_days_details(lwp = self.leave_without_pay)

		self.calculate_net_pay()
		self.compute_year_to_date()
		self.compute_month_to_date()
		self.compute_component_wise_year_to_date()
		self.add_leave_balances()

		if frappe.db.get_single_value("Payroll Settings", "max_working_hours_against_timesheet"):
			max_working_hours = frappe.db.get_single_value("Payroll Settings", "max_working_hours_against_timesheet")
			if self.salary_slip_based_on_timesheet and (self.total_working_hours > int(max_working_hours)):
				frappe.msgprint(_("Total working hours should not be greater than max working hours {0}").
								format(max_working_hours), alert=True)

	def set_net_total_in_words(self):
		doc_currency = self.currency
		company_currency = erpnext.get_company_currency(self.company)
		total = self.net_pay if self.is_rounding_total_disabled() else self.rounded_total
		base_total = self.base_net_pay if self.is_rounding_total_disabled() else self.base_rounded_total
		self.total_in_words = money_in_words(total, doc_currency)
		self.base_total_in_words = money_in_words(base_total, company_currency)

	def check_pms_record(self):
		aa=getdate(self.posting_date)
		month_name = aa.strftime("%B")
		if not frappe.db.exists("Technical Criteria", {"employee": self.employee, "month": month_name,"docstatus": 1 }):
			frappe.throw("PMS Record is not found (Technical)")
		if not frappe.db.exists("Behavioural Criteria", {"employee": self.employee, "month": month_name,"docstatus": 1 }):
			frappe.throw("PMS Record is not found (Behavioural)")
	

	def on_submit(self):
		# self.check_pms_record()
		if self.net_pay < 0:
			frappe.throw(_("Net Pay cannot be less than 0"))
		else:
			self.set_status()
			self.update_status(self.name)
			self.make_loan_repayment_entry()
			if (frappe.db.get_single_value("Payroll Settings", "email_salary_slip_to_employee")) and not frappe.flags.via_payroll_entry:
				if(self.employee!='WTT917'):
					self.email_salary_slip()

		self.update_payment_status_for_gratuity()
		self.update_balance_leave()

	def update_balance_leave(self):
		el=frappe.db.get_value("Employee",self.employee,"eligible_leave")
		if(self.approval_leave>el):
			el_lev=el
			bal_lev=self.approval_leave-el
		else:
			el_lev=self.approval_leave
			bal_lev=0
		if(frappe.db.sql("SELECT * FROM `tabBalance Leave` WHERE employee='"+str(self.employee)+"' ",as_dict=1)):
			doc=frappe.get_doc("Balance Leave",{"employee":self.employee})
			doc.append("balance_leave_table",{
				"posting_date":self.posting_date,
				"balance_leave":self.balance_leave,
				"taken_el":el_lev,
				"taken_bl":bal_lev
				})
			doc.save()
		else:
			doc=frappe.new_doc("Balance Leave")
			doc.employee=self.employee
			doc.append("balance_leave_table",{
				"posting_date":self.posting_date,
				"balance_leave":self.balance_leave,
				"taken_el":el_lev,
				"taken_bl":bal_lev
				})
			doc.save()

	def update_payment_status_for_gratuity(self):
		add_salary = frappe.db.get_all("Additional Salary",
			filters = {
				"payroll_date": ("BETWEEN", [self.start_date, self.end_date]),
				"employee": self.employee,
				"ref_doctype": "Gratuity",
				"docstatus": 1,
			}, fields = ["ref_docname", "name"], limit=1)

		if len(add_salary):
			status = "Paid" if self.docstatus == 1 else "Unpaid"
			if add_salary[0].name in [data.additional_salary for data in self.earnings]:
				frappe.db.set_value("Gratuity", add_salary.ref_docname, "status", status)

	def on_cancel(self):
		self.set_status()
		self.update_status()
		self.update_payment_status_for_gratuity()
		self.cancel_loan_repayment_entry()

	def on_trash(self):
		from frappe.model.naming import revert_series_if_last
		revert_series_if_last(self.series, self.name)

	def get_status(self):
		if self.docstatus == 0:
			status = "Draft"
		elif self.docstatus == 1:
			status = "Submitted"
		elif self.docstatus == 2:
			status = "Cancelled"
		return status

	def validate_dates(self, joining_date=None, relieving_date=None):
		if date_diff(self.end_date, self.start_date) < 0:
			frappe.throw(_("To date cannot be before From date"))

		if not joining_date:
			joining_date, relieving_date = frappe.get_cached_value(
				"Employee",
				self.employee,
				("date_of_joining", "relieving_date")
			)

		if date_diff(self.end_date, joining_date) < 0:
			frappe.throw(_("Cannot create Salary Slip for Employee joining after Payroll Period"))

		if relieving_date and date_diff(relieving_date, self.start_date) < 0:
			frappe.throw(_("Cannot create Salary Slip for Employee who has left before Payroll Period"))

	def is_rounding_total_disabled(self):
		return cint(frappe.db.get_single_value("Payroll Settings", "disable_rounded_total"))

	def check_existing(self):
		if not self.salary_slip_based_on_timesheet:
			cond = ""
			if self.payroll_entry:
				cond += "and payroll_entry = '{0}'".format(self.payroll_entry)
			ret_exist = frappe.db.sql("""select name from `tabSalary Slip`
						where start_date = %s and end_date = %s and docstatus != 2
						and employee = %s and name != %s {0}""".format(cond),
						(self.start_date, self.end_date, self.employee, self.name))
			if ret_exist:
				self.employee = ''
				frappe.throw(_("Salary Slip of employee {0} already created for this period").format(self.employee))
		else:
			for data in self.timesheets:
				if frappe.db.get_value('Timesheet', data.time_sheet, 'status') == 'Payrolled':
					frappe.throw(_("Salary Slip of employee {0} already created for time sheet {1}").format(self.employee, data.time_sheet))

	def get_date_details(self):
		if not self.end_date:
			date_details = get_start_end_dates(self.payroll_frequency, self.start_date or self.posting_date)
			dd=datetime.strptime(str(self.posting_date), '%Y-%m-%d').date()
			self.month=dd.strftime("%B")
			self.start_date = date_details.start_date
			self.end_date = date_details.end_date

	@frappe.whitelist()
	def get_emp_and_working_day_details(self):
		'''First time, load all the components from salary structure'''
		if self.employee:
			self.set("earnings", [])
			self.set("deductions", [])

			if not self.salary_slip_based_on_timesheet:
				self.get_date_details()

			joining_date, relieving_date = frappe.get_cached_value(
				"Employee",
				self.employee,
				("date_of_joining", "relieving_date")
			)

			self.validate_dates(joining_date, relieving_date)

			#getin leave details
			self.get_working_days_details(joining_date, relieving_date)
			struct = self.check_sal_struct(joining_date, relieving_date)

			if struct:
				self._salary_structure_doc = frappe.get_doc('Salary Structure', struct)
				self.salary_slip_based_on_timesheet = self._salary_structure_doc.salary_slip_based_on_timesheet or 0
				self.set_time_sheet()
				self.pull_sal_struct()
				ps = frappe.db.get_value("Payroll Settings", None, ["payroll_based_on","consider_unmarked_attendance_as"], as_dict=1)
				return [ps.payroll_based_on, ps.consider_unmarked_attendance_as]

	def set_time_sheet(self):
		if self.salary_slip_based_on_timesheet:
			self.set("timesheets", [])
			timesheets = frappe.db.sql(""" select * from `tabTimesheet` where employee = %(employee)s and start_date BETWEEN %(start_date)s AND %(end_date)s and (status = 'Submitted' or
				status = 'Billed')""", {'employee': self.employee, 'start_date': self.start_date, 'end_date': self.end_date}, as_dict=1)

			for data in timesheets:
				self.append('timesheets', {
					'time_sheet': data.name,
					'working_hours': data.total_hours
				})

	def check_sal_struct(self, joining_date, relieving_date):
		cond = """and sa.employee=%(employee)s and (sa.from_date <= %(start_date)s or
				sa.from_date <= %(end_date)s or sa.from_date <= %(joining_date)s)"""
		if self.payroll_frequency:
			cond += """and ss.payroll_frequency = '%(payroll_frequency)s'""" % {"payroll_frequency": self.payroll_frequency}

		st_name = frappe.db.sql("""
			select sa.salary_structure
			from `tabSalary Structure Assignment` sa join `tabSalary Structure` ss
			where sa.salary_structure=ss.name
				and sa.docstatus = 1 and ss.docstatus = 1 and ss.is_active ='Yes' %s
			order by sa.from_date desc
			limit 1
		""" %cond, {'employee': self.employee, 'start_date': self.start_date,
			'end_date': self.end_date, 'joining_date': joining_date})

		if st_name:
			self.salary_structure = st_name[0][0]
			return self.salary_structure

		else:
			self.salary_structure = None
			frappe.msgprint(_("No active or default Salary Structure found for employee {0} for the given dates")
				.format(self.employee), title=_('Salary Structure Missing'))

	def pull_sal_struct(self):
		from erpnext.payroll.doctype.salary_structure.salary_structure import make_salary_slip

		if self.salary_slip_based_on_timesheet:
			self.salary_structure = self._salary_structure_doc.name
			self.hour_rate = self._salary_structure_doc.hour_rate
			self.base_hour_rate = flt(self.hour_rate) * flt(self.exchange_rate)
			self.total_working_hours = sum([d.working_hours or 0.0 for d in self.timesheets]) or 0.0
			wages_amount = self.hour_rate * self.total_working_hours

			self.add_earning_for_hourly_wages(self, self._salary_structure_doc.salary_component, wages_amount)

		make_salary_slip(self._salary_structure_doc.name, self)

	def get_working_days_details(self, joining_date=None, relieving_date=None, lwp=None, for_preview=0):
		# self.get_allowance()

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
			actual_lwp, absent = self.calculate_lwp_ppl_and_absent_days_based_on_attendance(holidays)
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
					holidays.sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")))
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
							vv.append(ae[j].date())
						if ((frappe.db.exists("Attendance", {"employee": self.employee, "attendance_date": ae1[j].date()}))):
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
							hhcount=hhcount+deduct[ku]
					ccount=hhcount

			if payroll_based_on == "Attendance":
				uninformed_leave=0
				elsum=0
				el=frappe.get_value('Employee',self.employee,'eligible_leave')
				bl=el
				eeee=0
				elcr=0
				start=str(self.start_date)
				end=str(self.end_date)
				if(el!=0):
					query1=frappe.db.sql("SELECT attendance_date,in_time,out_time FROM `tabAttendance` WHERE employee='"+str(self.employee)+"' and status='Absent' and attendance_date>='"+str(start)+"' and attendance_date<='"+str(end)+"'",as_dict=1)
					query3=frappe.db.sql("SELECT attendance_date,in_time,out_time FROM `tabAttendance` WHERE employee='"+str(self.employee)+"' and status='Half Day' and attendance_date>='"+str(start)+"' and attendance_date<='"+str(end)+"'",as_dict=1)
					
					if(query1):
						bl=0
						for j in query1:
							if(j.in_time is None and j.out_time is None):
								atd = getdate(j.attendance_date).weekday()
								atk=calendar.day_name[atd]
								if(atk!="Sunday"):
									query4=frappe.db.sql("SELECT * FROM `tabLeave Request` as lr INNER JOIN `tabLeave table` as lt on lr.name=lt.parent WHERE lr.employee='"+str(self.employee)+"' and lt.from_date='"+str(j.attendance_date)+"' and lr.workflow_state!='Created' and lr.workflow_state!='Rejected' and lr.workflow_state!='Approved by HOD' and lr.workflow_state!='Cancelled'")
									query5=frappe.db.sql("SELECT * FROM `tabEmergency Leave` as el INNER JOIN `tabEmergency Table` as et on el.name=et.parent WHERE el.employee='"+str(self.employee)+"' and et.from_date>='"+str(j.attendance_date)+"' and et.from_date='"+str(j.attendance_date)+"' and el.workflow_state!='Created' and el.workflow_state!='Rejected' and el.workflow_state!='Approved by HOD' and el.workflow_state!='Cancelled'")
									if not query4 and not query5:
										uninformed_leave+=1
										elcr=elcr+1
									else:
										elcr=elcr
							else:
								elcr=1
						
									
						for j in query1:
							if(elcr==0):
								atd = getdate(j.attendance_date).weekday()
								atk=calendar.day_name[atd]
								if(atk!="Sunday"):
									query2=frappe.db.sql("SELECT lt.no_of_days FROM `tabLeave Request` as lr INNER JOIN `tabLeave table` as lt on lr.name=lt.parent WHERE lr.employee='"+str(self.employee)+"' and lt.leave_type='Eligible Leave' and lt.from_date='"+str(j.attendance_date)+"' and lr.workflow_state!='Created' and lr.workflow_state!='Rejected' and lr.workflow_state!='Approved by HOD' and lr.workflow_state!='Cancelled'",as_dict=1)
									if(query2):
										for i in query2:
											elsum=elsum+i.no_of_days
									else:
										if(elsum==0):
											bl=el
							else:
								elsum=0
						# frappe.msgprint(str(elcr))
						# frappe.msgprint(str(elsum))

						if(elsum<=el):
							if(elsum!=0):
								bl=el-elsum

					
					if(query3):
						bl=0
						chalf=0
						ar=[]
						for j in query3:
							atd = getdate(j.attendance_date).weekday()
							atk=calendar.day_name[atd]
							if(atk!="Sunday"):
								chalf=frappe.db.sql("SELECT count(name) as nna FROM `tabEmployee Checkin` WHERE time>='"+str(j.attendance_date)+" 00:00:00' and time<='"+str(j.attendance_date)+" 23:00:00' and employee='"+str(self.employee)+"'",as_dict=1)
								for i in chalf:
									if(i.nna<3):		
										query6=frappe.db.sql("SELECT * FROM `tabLeave Request` as lr INNER JOIN `tabLeave table` as lt on lr.name=lt.parent WHERE lr.employee='"+str(self.employee)+"' and lt.from_date='"+str(j.attendance_date)+"' and lr.workflow_state!='Created' and lr.workflow_state!='Rejected' and lr.workflow_state!='Approved by HOD' and lr.workflow_state!='Cancelled'",as_dict=1)
										query7=frappe.db.sql("SELECT * FROM `tabEmergency Leave` as el INNER JOIN `tabEmergency Table` as et on el.name=et.parent WHERE el.employee='"+str(self.employee)+"' and et.from_date>='"+str(j.attendance_date)+"' and et.from_date='"+str(j.attendance_date)+"' and el.workflow_state!='Created' and el.workflow_state!='Rejected' and el.workflow_state!='Approved by HOD' and el.workflow_state!='Cancelled'")
										if not query6 and not query7:
											uninformed_leave+=0.5
											eeee=eeee+0.5
										else:
											eeee=eeee

						for j in query3:
							if(eeee==0):
								atd = getdate(j.attendance_date).weekday()
								atk=calendar.day_name[atd]
								if(atk!="Sunday"):
									query2=frappe.db.sql("SELECT lt.no_of_days FROM `tabLeave Request` as lr INNER JOIN `tabLeave table` as lt on lr.name=lt.parent WHERE lr.employee='"+str(self.employee)+"' and lt.leave_type='Eligible Leave' and lt.from_date='"+str(j.attendance_date)+"' and lr.workflow_state!='Created' and lr.workflow_state!='Rejected' and lr.workflow_state!='Approved by HOD' and lr.workflow_state!='Cancelled'",as_dict=1)
									if(query2):
										for i in query2:
											elsum=elsum+0.5
									else:
										if(elsum==0):
											bl=el
							else:
								elsum=0
						
						if(elsum<el):
							if(elsum!=0):
								bl=el-elsum		
					elif not query1 and not query3:
						bl=0
						bl=el

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

				unmarked_days = self.get_unmarked_days()
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
							x = datetime.now().time().replace(hour=9,minute=30,second=0,microsecond=0)
							z = datetime.now().time().replace(hour=9,minute=1,second=0,microsecond=0)
							el = datetime.now().time().replace(hour=11,minute=00,second=0,microsecond=0)
							z1 = datetime.now().time().replace(hour=9,minute=00,second=0,microsecond=0)
							z2 = datetime.now().time().replace(hour=9,minute=10,second=0,microsecond=0)
							if(j.in_time.time()>x and j.in_time.time()<=el):
								mrgcnt=mrgcnt+1
							elif(j.in_time.time()>z and j.in_time.time()<=el):
								mrgcnt2=mrgcnt2+1
							else:
								mrgcnt=mrgcnt
								mrgcnt2=mrgcnt2
							if(j.in_time.time()>z1 and j.in_time.time()<=z2):
								gracecnt=gracecnt+1
							else:
								gracecnt=gracecnt



					
					for j in frappe.db.sql("SELECT in_time,attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(self.start_date)+"' AND attendance_date<='"+str(self.end_date)+"' AND employee='"+self.employee+"' AND late_entry!=0 AND status='Half Day'",as_dict=1):
						date1 = j.attendance_date
						daf = date1.weekday()
						godf=calendar.day_name[daf]
						if(godf!="Sunday"):
							x = datetime.now().time().replace(hour=9,minute=30,second=0,microsecond=0)
							y = datetime.now().time().replace(hour=14,minute=30,second=0,microsecond=0)
							z = datetime.now().time().replace(hour=9,minute=1,second=0,microsecond=0)
							w = datetime.now().time().replace(hour=13,minute=31,second=0,microsecond=0)
							el = datetime.now().time().replace(hour=11,minute=00,second=0,microsecond=0)
							z1 = datetime.now().time().replace(hour=9,minute=00,second=0,microsecond=0)
							z2 = datetime.now().time().replace(hour=9,minute=10,second=0,microsecond=0)
					
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
							if(j.in_time.time()>z1 and j.in_time.time()<=z2):
								gracecnt=gracecnt+1
							else:
								gracecnt=gracecnt
					

					if(gracecnt<=2):
						mrgtotal=mrgcnt+((mrgcnt2-gracecnt)/3)
						over=mrgtotal
						go=int(over)	
					else:
						mrgtotal=mrgcnt+((mrgcnt2-2)/3)
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
							x = datetime.now().time().replace(hour=9,minute=30,second=0,microsecond=0)
							z = datetime.now().time().replace(hour=9,minute=1,second=0,microsecond=0)
							el = datetime.now().time().replace(hour=11,minute=00,second=0,microsecond=0)
							z1 = datetime.now().time().replace(hour=9,minute=00,second=0,microsecond=0)
							z2 = datetime.now().time().replace(hour=9,minute=10,second=0,microsecond=0)
							if(j.in_time.time()>x and j.in_time.time()<=el):
								mrgcnt=mrgcnt+1
							elif(j.in_time.time()>z and j.in_time.time()<=el):
								mrgcnt2=mrgcnt2+1
							else:
								mrgcnt=mrgcnt
								mrgcnt2=mrgcnt2
							if(j.in_time.time()>z1 and j.in_time.time()<=z2):
								gracecnt=gracecnt+1
							else:
								gracecnt=gracecnt



					
					for j in frappe.db.sql("SELECT in_time,attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(self.start_date)+"' AND attendance_date<='"+str(self.end_date)+"' AND employee='"+self.employee+"' AND late_entry!=0 AND status='Half Day'",as_dict=1):
						date1 = j.attendance_date
						daf = date1.weekday()
						godf=calendar.day_name[daf]
						if(godf!="Sunday"):
							x = datetime.now().time().replace(hour=9,minute=30,second=0,microsecond=0)
							y = datetime.now().time().replace(hour=15,minute=00,second=0,microsecond=0)
							z = datetime.now().time().replace(hour=9,minute=1,second=0,microsecond=0)
							w = datetime.now().time().replace(hour=14,minute=31,second=0,microsecond=0)
							el = datetime.now().time().replace(hour=11,minute=00,second=0,microsecond=0)
							z1 = datetime.now().time().replace(hour=9,minute=00,second=0,microsecond=0)
							z2 = datetime.now().time().replace(hour=9,minute=10,second=0,microsecond=0)
					
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
							if(j.in_time.time()>z1 and j.in_time.time()<=z2):
								gracecnt=gracecnt+1
							else:
								gracecnt=gracecnt

					if(gracecnt<=2):
						mrgtotal=mrgcnt+((mrgcnt2-gracecnt)/3)
						over=mrgtotal
						go=int(over)	
					else:
						mrgtotal=mrgcnt+((mrgcnt2-2)/3)
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

				
				bal_lev=frappe.db.get_value('Employee',self.employee,'eligible_leave')
				if(elsum<=bal_lev and elcr==0 and eeee==0):
					this_month_bal_leave=bal_lev-elsum
				else:
					this_month_bal_leave=0
				if(self.employee=="WTT1385"):
					ccount=0

				# frappe.msgprint(str(elsum)+" and "+str(this_month_bal_leave))
				val=self.total_working_days-(flt(absent)+unmarked_days+lwp)
				self.punched_days=val
				self.uninformed_leave=uninformed_leave
				if((val+ccount)>=20):
					sun_cal=(val+ccount-worked_sundays)/6
					if(sun_cal>=3.6):
						total_pay=val+v+elsum+ccount    #removed sunday because the sunday status were changed
						self.actual_payment_days=total_pay
						self.payment_days=total_pay-overall_total-suncount-(halfsuncount/2)
						self.actual_absent_days=total_pay-self.actual_payment_days
						self.absent_days=(self.total_working_days)-self.payment_days+elsum
						self.loss_of_pay=self.absent_days-elsum
						self.sundays=v
						self.approval_leave=elsum
						self.balance_leave=this_month_bal_leave
						self.late_deduction=overall_total
						self.national_holidays=cnt
						self.nh_given=ccount
					else:
						sun_cal=0.5*math.floor((((val+ccount)/3)*0.5)/0.5)
						total_pay=val+sun_cal+ccount+elsum
						# frappe.msgprint(str(val)+"-------"+str(sun_cal)+"__----____"+str(ccount))
						self.actual_payment_days=total_pay
						self.payment_days=total_pay-overall_total-suncount-(halfsuncount/2)
						self.actual_absent_days=total_pay-self.actual_payment_days
						self.absent_days=(self.total_working_days)-self.payment_days+elsum
						self.loss_of_pay=self.absent_days-elsum
						self.sundays=sun_cal
						self.approval_leave=elsum
						self.balance_leave=this_month_bal_leave
						self.late_deduction=overall_total
						self.national_holidays=cnt
						self.nh_given=ccount

				else:
					sun_cal=0.5*math.floor((((val+ccount-worked_sundays)/3)*0.5)/0.5)
					total_pay=val+sun_cal+ccount
					self.actual_payment_days=total_pay
					self.payment_days=total_pay-overall_total-suncount-(halfsuncount/2)
					self.actual_absent_days=total_pay-self.actual_payment_days
					self.absent_days=(self.total_working_days)-self.payment_days+elsum
					self.loss_of_pay=self.absent_days-elsum
					self.sundays=sun_cal
					self.approval_leave=0
					self.balance_leave=0
					self.late_deduction=overall_total
					self.national_holidays=cnt
					self.nh_given=ccount
				if(self.absent_days-elsum<0):
					self.loss_of_pay=0
			# frappe.msgprint("absent : "+str(absent)+"; lwp : "+str(lwp)+" ; unmarked_days : "+str(unmarked_days)+" ; Sundays : "+str(v)+" ; LATE : "+str(overall_total)+" ; NH : "+str(ccount)+" ; EL : "+str(elsum)+" ; BL : "+str(bl)+" ; working_days : "+str(self.total_working_days))
			
			consider_unmarked_attendance_as = frappe.db.get_value("Payroll Settings", None, "consider_unmarked_attendance_as") or "Present"

			if payroll_based_on == "Attendance" and consider_unmarked_attendance_as =="Absent":
				#self.absent_days += unmarked_days #will be treated as absent
				#self.payment_days -= unmarked_days
				if include_holidays_in_total_working_days:
					if not holidays:
						pass
					else:
						holidays.sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")))
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
						# else:
						# 	self.actual_payment_days=self.actual_payment_days-hhcount
						# 	self.nh_given=self.nh_given-hhcount
						# 	self.payment_days=self.payment_days-hhcount
						# frappe.msgprint(str(hhcount))
			else:
				self.payment_days = 0

	
	def get_allowance(self):
		ar=[]
		pass
		# doc=frappe.get_doc("Shoes and TShirt",{"employee":self.employee,"employee_allowance":"Shoes","docstatus":1})
		# for i in doc.shoes_table:
		# 	if(getdate(self.start_date)<=getdate(i.issue_date)<=getdate(self.end_date)):
		# 		self.append("earnings",{
		# 			"salary_component":"Shoe Allowance",
		# 			"amount":i.amount
		# 			})
		# 		frappe.db.commit()
		
	def get_unmarked_days(self):
		marked_days = frappe.get_all("Attendance", filters = {
					"attendance_date": ["between", [self.start_date, self.end_date]],
					"employee": self.employee,
					"docstatus": 1
				}, fields = ["COUNT(*) as marked_days"])[0].marked_days
		return self.total_working_days - marked_days


	def get_payment_days(self, joining_date, relieving_date, include_holidays_in_total_working_days):
		if not joining_date:
			joining_date, relieving_date = frappe.get_cached_value("Employee", self.employee,
				["date_of_joining", "relieving_date"])

		start_date = getdate(self.start_date)
		if joining_date:
			if getdate(self.start_date) <= joining_date <= getdate(self.end_date):
				start_date = joining_date
			elif joining_date > getdate(self.end_date):
				return

		end_date = getdate(self.end_date)
		if relieving_date:
			if getdate(self.start_date) <= relieving_date <= getdate(self.end_date):
				end_date = relieving_date
			elif relieving_date < getdate(self.start_date):
				frappe.throw(_("Employee relieved on {0} must be set as 'Left'")
					.format(relieving_date))

		payment_days = date_diff(end_date, start_date) + 1

		if not cint(include_holidays_in_total_working_days):
			holidays = self.get_holidays_for_employee(start_date, end_date)
			payment_days -= len(holidays)

		return payment_days

	def get_holidays_for_employee(self, start_date, end_date):
		holiday_list = get_holiday_list_for_employee(self.employee)
		holidays = frappe.db.sql_list('''select holiday_date from `tabHoliday`
			where
				parent=%(holiday_list)s
				and holiday_date >= %(start_date)s
				and holiday_date <= %(end_date)s''', {
					"holiday_list": holiday_list,
					"start_date": start_date,
					"end_date": end_date
				})

		holidays = [cstr(i) for i in holidays]

		return holidays

	def calculate_lwp_or_ppl_based_on_leave_application(self, holidays, working_days):
		lwp = 0
		holidays = "','".join(holidays)
		daily_wages_fraction_for_half_day = \
			flt(frappe.db.get_value("Payroll Settings", None, "daily_wages_fraction_for_half_day")) or 0.5

		for d in range(working_days):
			dt = add_days(cstr(getdate(self.start_date)), d)
			leave = frappe.db.sql("""
				SELECT t1.name,
					CASE WHEN (t1.half_day_date = %(dt)s or t1.to_date = t1.from_date)
					THEN t1.half_day else 0 END,
					t2.is_ppl,
					t2.fraction_of_daily_salary_per_leave
				FROM `tabLeave Application` t1, `tabLeave Type` t2
				WHERE t2.name = t1.leave_type
				AND (t2.is_lwp = 1 or t2.is_ppl = 1)
				AND t1.docstatus = 1
				AND t1.employee = %(employee)s
				AND ifnull(t1.salary_slip, '') = ''
				AND CASE
					WHEN t2.include_holiday != 1
						THEN %(dt)s not in ('{0}') and %(dt)s between from_date and to_date
					WHEN t2.include_holiday
						THEN %(dt)s between from_date and to_date
					END
				""".format(holidays), {"employee": self.employee, "dt": dt})

			if leave:
				equivalent_lwp_count = 0
				is_half_day_leave = cint(leave[0][1])
				is_partially_paid_leave = cint(leave[0][2])
				fraction_of_daily_salary_per_leave = flt(leave[0][3])

				equivalent_lwp_count =  (1 - daily_wages_fraction_for_half_day) if is_half_day_leave else 1

				if is_partially_paid_leave:
					equivalent_lwp_count *= fraction_of_daily_salary_per_leave if fraction_of_daily_salary_per_leave else 1

				lwp += equivalent_lwp_count

		return lwp

	def calculate_lwp_ppl_and_absent_days_based_on_attendance(self, holidays):
		lwp = 0
		absent = 0

		daily_wages_fraction_for_half_day = \
			flt(frappe.db.get_value("Payroll Settings", None, "daily_wages_fraction_for_half_day")) or 0.5

		leave_types = frappe.get_all("Leave Type",
			or_filters=[["is_ppl", "=", 1], ["is_lwp", "=", 1]],
			fields =["name", "is_lwp", "is_ppl", "fraction_of_daily_salary_per_leave", "include_holiday"])

		leave_type_map = {}
		for leave_type in leave_types:
			leave_type_map[leave_type.name] = leave_type

		attendances = frappe.db.sql('''
			SELECT attendance_date, status, leave_type
			FROM `tabAttendance`
			WHERE
				status in ("Absent", "Half Day", "On leave")
				AND employee = %s
				AND docstatus = 1
				AND attendance_date between %s and %s
		''', values=(self.employee, self.start_date, self.end_date), as_dict=1)

		for d in attendances:
			if d.status in ('Half Day', 'On Leave') and d.leave_type and d.leave_type not in leave_type_map.keys():
				continue

			if formatdate(d.attendance_date, "yyyy-mm-dd") in holidays:
				if d.status == "Absent" or \
					(d.leave_type and d.leave_type in leave_type_map.keys() and not leave_type_map[d.leave_type]['include_holiday']):
						continue

			if d.leave_type:
				fraction_of_daily_salary_per_leave = leave_type_map[d.leave_type]["fraction_of_daily_salary_per_leave"]

			if d.status == "Half Day":
				equivalent_lwp =  (1 - daily_wages_fraction_for_half_day)

				if d.leave_type in leave_type_map.keys() and leave_type_map[d.leave_type]["is_ppl"]:
					equivalent_lwp *= fraction_of_daily_salary_per_leave if fraction_of_daily_salary_per_leave else 1
				lwp += equivalent_lwp
			elif d.status == "On Leave" and d.leave_type and d.leave_type in leave_type_map.keys():
				equivalent_lwp = 1
				if leave_type_map[d.leave_type]["is_ppl"]:
					equivalent_lwp *= fraction_of_daily_salary_per_leave if fraction_of_daily_salary_per_leave else 1
				lwp += equivalent_lwp
			elif d.status == "Absent":
				absent += 1
		return lwp, absent

	def add_earning_for_hourly_wages(self, doc, salary_component, amount):
		row_exists = False
		for row in doc.earnings:
			if row.salary_component == salary_component:
				row.amount = amount
				row_exists = True
				break

		if not row_exists:
			wages_row = {
				"salary_component": salary_component,
				"abbr": frappe.db.get_value("Salary Component", salary_component, "salary_component_abbr"),
				"amount": self.hour_rate * self.total_working_hours,
				"default_amount": 0.0,
				"additional_amount": 0.0
			}
			doc.append('earnings', wages_row)

	def calculate_net_pay(self):
		if self.salary_structure:
			self.calculate_component_amounts("earnings")
		self.gross_pay = self.get_component_totals("earnings", depends_on_payment_days=1)
		self.base_gross_pay = flt(flt(self.gross_pay) * flt(self.exchange_rate), self.precision('base_gross_pay'))

		if self.salary_structure:
			self.calculate_component_amounts("deductions")

		self.set_loan_repayment()
		self.set_component_amounts_based_on_payment_days()
		self.set_net_pay()

	def set_net_pay(self):
		self.total_deduction = self.get_component_totals("deductions")
		self.base_total_deduction = flt(flt(self.total_deduction) * flt(self.exchange_rate), self.precision('base_total_deduction'))
		self.net_pay = flt(self.gross_pay) - (flt(self.total_deduction) + flt(self.total_loan_repayment))
		self.rounded_total = rounded(self.net_pay)
		self.base_net_pay = flt(flt(self.net_pay) * flt(self.exchange_rate), self.precision('base_net_pay'))
		self.base_rounded_total = flt(rounded(self.base_net_pay), self.precision('base_net_pay'))
		if self.hour_rate:
			self.base_hour_rate = flt(flt(self.hour_rate) * flt(self.exchange_rate), self.precision('base_hour_rate'))
		self.set_net_total_in_words()

	def calculate_component_amounts(self, component_type):
		if not getattr(self, '_salary_structure_doc', None):
			self._salary_structure_doc = frappe.get_doc('Salary Structure', self.salary_structure)

		payroll_period = get_payroll_period(self.start_date, self.end_date, self.company)

		self.add_structure_components(component_type)
		self.add_additional_salary_components(component_type)
		if component_type == "earnings":
			self.add_employee_benefits(payroll_period)
		else:
			self.add_tax_components(payroll_period)

	def add_structure_components(self, component_type):
		data = self.get_data_for_eval()
		for struct_row in self._salary_structure_doc.get(component_type):
			amount = self.eval_condition_and_formula(struct_row, data)
			if amount and struct_row.statistical_component == 0:
				self.update_component_row(struct_row, amount, component_type)

	def get_data_for_eval(self):
		'''Returns data for evaluating formula'''
		data = frappe._dict()
		employee = frappe.get_doc("Employee", self.employee).as_dict()

		start_date = getdate(self.start_date)
		date_to_validate = (
			employee.date_of_joining
			if employee.date_of_joining > start_date
			else start_date
		)

		salary_structure_assignment = frappe.get_value(
			"Salary Structure Assignment",
			{
				"employee": self.employee,
				"salary_structure": self.salary_structure,
				"from_date": ("<=", date_to_validate),
				"docstatus": 1,
			},
			"*",
			order_by="from_date desc",
			as_dict=True,
		)

		if not salary_structure_assignment:
			frappe.throw(
				_("Please assign a Salary Structure for Employee {0} "
				"applicable from or before {1} first").format(
					frappe.bold(self.employee_name),
					frappe.bold(formatdate(date_to_validate)),
				)
			)

		data.update(salary_structure_assignment)
		data.update(employee)
		data.update(self.as_dict())

		# set values for components
		salary_components = frappe.get_all("Salary Component", fields=["salary_component_abbr"])
		for sc in salary_components:
			data.setdefault(sc.salary_component_abbr, 0)

		for key in ('earnings', 'deductions'):
			for d in self.get(key):
				data[d.abbr] = d.amount

		return data

	def eval_condition_and_formula(self, d, data):
		try:
			condition = d.condition.strip().replace("\n", " ") if d.condition else None
			if condition:
				if not frappe.safe_eval(condition, self.whitelisted_globals, data):
					return None
			amount = d.amount
			if d.amount_based_on_formula:
				formula = d.formula.strip().replace("\n", " ") if d.formula else None
				if formula:
					amount = flt(frappe.safe_eval(formula, self.whitelisted_globals, data), d.precision("amount"))
			if amount:
				data[d.abbr] = amount

			return amount

		except NameError as err:
			frappe.throw(_("{0} <br> This error can be due to missing or deleted field.").format(err),
				title=_("Name error"))
		except SyntaxError as err:
			frappe.throw(_("Syntax error in formula or condition: {0}").format(err))
		except Exception as e:
			frappe.throw(_("Error in formula or condition: {0}").format(e))
			raise

	def add_employee_benefits(self, payroll_period):
		for struct_row in self._salary_structure_doc.get("earnings"):
			if struct_row.is_flexible_benefit == 1:
				if frappe.db.get_value("Salary Component", struct_row.salary_component, "pay_against_benefit_claim") != 1:
					benefit_component_amount = get_benefit_component_amount(self.employee, self.start_date, self.end_date,
						struct_row.salary_component, self._salary_structure_doc, self.payroll_frequency, payroll_period)
					if benefit_component_amount:
						self.update_component_row(struct_row, benefit_component_amount, "earnings")
				else:
					benefit_claim_amount = get_benefit_claim_amount(self.employee, self.start_date, self.end_date, struct_row.salary_component)
					if benefit_claim_amount:
						self.update_component_row(struct_row, benefit_claim_amount, "earnings")

		self.adjust_benefits_in_last_payroll_period(payroll_period)

	def adjust_benefits_in_last_payroll_period(self, payroll_period):
		if payroll_period:
			if (getdate(payroll_period.end_date) <= getdate(self.end_date)):
				last_benefits = get_last_payroll_period_benefits(self.employee, self.start_date, self.end_date,
					payroll_period, self._salary_structure_doc)
				if last_benefits:
					for last_benefit in last_benefits:
						last_benefit = frappe._dict(last_benefit)
						amount = last_benefit.amount
						self.update_component_row(frappe._dict(last_benefit.struct_row), amount, "earnings")

	def add_additional_salary_components(self, component_type):
		additional_salaries = get_additional_salaries(self.employee,
			self.start_date, self.end_date, component_type)

		for additional_salary in additional_salaries:
			self.update_component_row(
				get_salary_component_data(additional_salary.component),
				additional_salary.amount,
				component_type,
				additional_salary
			)

	def add_tax_components(self, payroll_period):
		# Calculate variable_based_on_taxable_salary after all components updated in salary slip
		tax_components, other_deduction_components = [], []
		for d in self._salary_structure_doc.get("deductions"):
			if d.variable_based_on_taxable_salary == 1 and not d.formula and not flt(d.amount):
				tax_components.append(d.salary_component)
			else:
				other_deduction_components.append(d.salary_component)

		if not tax_components:
			tax_components = [d.name for d in frappe.get_all("Salary Component", filters={"variable_based_on_taxable_salary": 1})
				if d.name not in other_deduction_components]

		for d in tax_components:
			tax_amount = self.calculate_variable_based_on_taxable_salary(d, payroll_period)
			tax_row = get_salary_component_data(d)
			self.update_component_row(tax_row, tax_amount, "deductions")

	def update_component_row(self, component_data, amount, component_type, additional_salary=None):
		component_row = None
		for d in self.get(component_type):
			if d.salary_component != component_data.salary_component:
				continue

			if (
				(not d.additional_salary
				and (not additional_salary or additional_salary.overwrite))
				or (additional_salary
				and additional_salary.name == d.additional_salary)
			):
				component_row = d
				break

		if additional_salary and additional_salary.overwrite:
			# Additional Salary with overwrite checked, remove default rows of same component
			self.set(component_type, [
				d for d in self.get(component_type)
				if d.salary_component != component_data.salary_component
				or (d.additional_salary and additional_salary.name != d.additional_salary)
				or d == component_row
			])

		if not component_row:
			if not amount:
				return

			component_row = self.append(component_type)
			for attr in (
				'depends_on_payment_days', 'salary_component',
				'do_not_include_in_total', 'is_tax_applicable',
				'is_flexible_benefit', 'variable_based_on_taxable_salary',
				'exempted_from_income_tax'
			):
				component_row.set(attr, component_data.get(attr))

			abbr = component_data.get('abbr') or component_data.get('salary_component_abbr')
			component_row.set('abbr', abbr)

		if additional_salary:
			component_row.default_amount = 0
			component_row.additional_amount = amount
			component_row.additional_salary = additional_salary.name
			component_row.deduct_full_tax_on_selected_payroll_date = \
				additional_salary.deduct_full_tax_on_selected_payroll_date
		else:
			component_row.default_amount = amount
			component_row.additional_amount = 0
			component_row.deduct_full_tax_on_selected_payroll_date = \
				component_data.deduct_full_tax_on_selected_payroll_date

		component_row.amount = amount

	def calculate_variable_based_on_taxable_salary(self, tax_component, payroll_period):
		if not payroll_period:
			frappe.msgprint(_("Start and end dates not in a valid Payroll Period, cannot calculate {0}.")
				.format(tax_component))
			return

		# Deduct taxes forcefully for unsubmitted tax exemption proof and unclaimed benefits in the last period
		if payroll_period.end_date <= getdate(self.end_date):
			self.deduct_tax_for_unsubmitted_tax_exemption_proof = 1
			self.deduct_tax_for_unclaimed_employee_benefits = 1

		return self.calculate_variable_tax(payroll_period, tax_component)

	def calculate_variable_tax(self, payroll_period, tax_component):
		# get Tax slab from salary structure assignment for the employee and payroll period
		tax_slab = self.get_income_tax_slabs(payroll_period)

		# get remaining numbers of sub-period (period for which one salary is processed)
		remaining_sub_periods = get_period_factor(self.employee,
			self.start_date, self.end_date, self.payroll_frequency, payroll_period)[1]
		# get taxable_earnings, paid_taxes for previous period
		previous_taxable_earnings = self.get_taxable_earnings_for_prev_period(payroll_period.start_date,
			self.start_date, tax_slab.allow_tax_exemption)
		previous_total_paid_taxes = self.get_tax_paid_in_period(payroll_period.start_date, self.start_date, tax_component)

		# get taxable_earnings for current period (all days)
		current_taxable_earnings = self.get_taxable_earnings(tax_slab.allow_tax_exemption)
		future_structured_taxable_earnings = current_taxable_earnings.taxable_earnings * (math.ceil(remaining_sub_periods) - 1)

		# get taxable_earnings, addition_earnings for current actual payment days
		current_taxable_earnings_for_payment_days = self.get_taxable_earnings(tax_slab.allow_tax_exemption, based_on_payment_days=1)
		current_structured_taxable_earnings = current_taxable_earnings_for_payment_days.taxable_earnings
		current_additional_earnings = current_taxable_earnings_for_payment_days.additional_income
		current_additional_earnings_with_full_tax = current_taxable_earnings_for_payment_days.additional_income_with_full_tax

		# Get taxable unclaimed benefits
		unclaimed_taxable_benefits = 0
		if self.deduct_tax_for_unclaimed_employee_benefits:
			unclaimed_taxable_benefits = self.calculate_unclaimed_taxable_benefits(payroll_period)
			unclaimed_taxable_benefits += current_taxable_earnings_for_payment_days.flexi_benefits

		# Total exemption amount based on tax exemption declaration
		total_exemption_amount = self.get_total_exemption_amount(payroll_period, tax_slab)

		#Employee Other Incomes
		other_incomes = self.get_income_form_other_sources(payroll_period) or 0.0

		# Total taxable earnings including additional and other incomes
		total_taxable_earnings = previous_taxable_earnings + current_structured_taxable_earnings + future_structured_taxable_earnings \
			+ current_additional_earnings + other_incomes + unclaimed_taxable_benefits - total_exemption_amount

		# Total taxable earnings without additional earnings with full tax
		total_taxable_earnings_without_full_tax_addl_components = total_taxable_earnings - current_additional_earnings_with_full_tax

		# Structured tax amount
		total_structured_tax_amount = self.calculate_tax_by_tax_slab(
			total_taxable_earnings_without_full_tax_addl_components, tax_slab)
		current_structured_tax_amount = (total_structured_tax_amount - previous_total_paid_taxes) / remaining_sub_periods

		# Total taxable earnings with additional earnings with full tax
		full_tax_on_additional_earnings = 0.0
		if current_additional_earnings_with_full_tax:
			total_tax_amount = self.calculate_tax_by_tax_slab(total_taxable_earnings, tax_slab)
			full_tax_on_additional_earnings = total_tax_amount - total_structured_tax_amount

		current_tax_amount = current_structured_tax_amount + full_tax_on_additional_earnings
		if flt(current_tax_amount) < 0:
			current_tax_amount = 0

		return current_tax_amount

	def get_income_tax_slabs(self, payroll_period):
		income_tax_slab, ss_assignment_name = frappe.db.get_value("Salary Structure Assignment",
			{"employee": self.employee, "salary_structure": self.salary_structure, "docstatus": 1}, ["income_tax_slab", 'name'])

		if not income_tax_slab:
			frappe.throw(_("Income Tax Slab not set in Salary Structure Assignment: {0}").format(ss_assignment_name))

		income_tax_slab_doc = frappe.get_doc("Income Tax Slab", income_tax_slab)
		if income_tax_slab_doc.disabled:
			frappe.throw(_("Income Tax Slab: {0} is disabled").format(income_tax_slab))

		if getdate(income_tax_slab_doc.effective_from) > getdate(payroll_period.start_date):
			frappe.throw(_("Income Tax Slab must be effective on or before Payroll Period Start Date: {0}")
				.format(payroll_period.start_date))

		return income_tax_slab_doc


	def get_taxable_earnings_for_prev_period(self, start_date, end_date, allow_tax_exemption=False):
		taxable_earnings = frappe.db.sql("""
			select sum(sd.amount)
			from
				`tabSalary Detail` sd join `tabSalary Slip` ss on sd.parent=ss.name
			where
				sd.parentfield='earnings'
				and sd.is_tax_applicable=1
				and is_flexible_benefit=0
				and ss.docstatus=1
				and ss.employee=%(employee)s
				and ss.start_date between %(from_date)s and %(to_date)s
				and ss.end_date between %(from_date)s and %(to_date)s
			""", {
				"employee": self.employee,
				"from_date": start_date,
				"to_date": end_date
			})
		taxable_earnings = flt(taxable_earnings[0][0]) if taxable_earnings else 0

		exempted_amount = 0
		if allow_tax_exemption:
			exempted_amount = frappe.db.sql("""
				select sum(sd.amount)
				from
					`tabSalary Detail` sd join `tabSalary Slip` ss on sd.parent=ss.name
				where
					sd.parentfield='deductions'
					and sd.exempted_from_income_tax=1
					and is_flexible_benefit=0
					and ss.docstatus=1
					and ss.employee=%(employee)s
					and ss.start_date between %(from_date)s and %(to_date)s
					and ss.end_date between %(from_date)s and %(to_date)s
				""", {
					"employee": self.employee,
					"from_date": start_date,
					"to_date": end_date
				})
			exempted_amount = flt(exempted_amount[0][0]) if exempted_amount else 0

		return taxable_earnings - exempted_amount

	def get_tax_paid_in_period(self, start_date, end_date, tax_component):
		# find total_tax_paid, tax paid for benefit, additional_salary
		total_tax_paid = flt(frappe.db.sql("""
			select
				sum(sd.amount)
			from
				`tabSalary Detail` sd join `tabSalary Slip` ss on sd.parent=ss.name
			where
				sd.parentfield='deductions'
				and sd.salary_component=%(salary_component)s
				and sd.variable_based_on_taxable_salary=1
				and ss.docstatus=1
				and ss.employee=%(employee)s
				and ss.start_date between %(from_date)s and %(to_date)s
				and ss.end_date between %(from_date)s and %(to_date)s
		""", {
			"salary_component": tax_component,
			"employee": self.employee,
			"from_date": start_date,
			"to_date": end_date
		})[0][0])

		return total_tax_paid

	def get_taxable_earnings(self, allow_tax_exemption=False, based_on_payment_days=0):
		joining_date, relieving_date = frappe.get_cached_value("Employee", self.employee,
			["date_of_joining", "relieving_date"])

		if not relieving_date:
			relieving_date = getdate(self.end_date)

		if not joining_date:
			frappe.throw(_("Please set the Date Of Joining for employee {0}").format(frappe.bold(self.employee_name)))

		taxable_earnings = 0
		additional_income = 0
		additional_income_with_full_tax = 0
		flexi_benefits = 0

		for earning in self.earnings:
			if based_on_payment_days:
				amount, additional_amount = self.get_amount_based_on_payment_days(earning, joining_date, relieving_date)
			else:
				amount, additional_amount = earning.amount, earning.additional_amount

			if earning.is_tax_applicable:
				if additional_amount:
					taxable_earnings += (amount - additional_amount)
					additional_income += additional_amount
					if earning.deduct_full_tax_on_selected_payroll_date:
						additional_income_with_full_tax += additional_amount
					continue

				if earning.is_flexible_benefit:
					flexi_benefits += amount
				else:
					taxable_earnings += amount

		if allow_tax_exemption:
			for ded in self.deductions:
				if ded.exempted_from_income_tax:
					amount = ded.amount
					if based_on_payment_days:
						amount = self.get_amount_based_on_payment_days(ded, joining_date, relieving_date)[0]
					taxable_earnings -= flt(amount)

		return frappe._dict({
			"taxable_earnings": taxable_earnings,
			"additional_income": additional_income,
			"additional_income_with_full_tax": additional_income_with_full_tax,
			"flexi_benefits": flexi_benefits
		})

	def get_amount_based_on_payment_days(self, row, joining_date, relieving_date):
		amount, additional_amount = row.amount, row.additional_amount
		if (self.salary_structure and
			cint(row.depends_on_payment_days) and cint(self.total_working_days) and
			(not self.salary_slip_based_on_timesheet or
				getdate(self.start_date) < joining_date or
				(relieving_date and getdate(self.end_date) > relieving_date)
			)):
			additional_amount = flt((flt(row.additional_amount) * flt(self.payment_days)
				/ cint(self.total_working_days)), row.precision("additional_amount"))
			amount = flt((flt(row.default_amount) * flt(self.payment_days)
				/ cint(self.total_working_days)), row.precision("amount")) + additional_amount

		elif not self.payment_days and not self.salary_slip_based_on_timesheet and cint(row.depends_on_payment_days):
			amount, additional_amount = 0, 0
		elif not row.amount:
			amount = flt(row.default_amount) + flt(row.additional_amount)

		# apply rounding
		if frappe.get_cached_value("Salary Component", row.salary_component, "round_to_the_nearest_integer"):
			amount, additional_amount = rounded(amount), rounded(additional_amount)

		return amount, additional_amount

	def calculate_unclaimed_taxable_benefits(self, payroll_period):
		# get total sum of benefits paid
		total_benefits_paid = flt(frappe.db.sql("""
			select sum(sd.amount)
			from `tabSalary Detail` sd join `tabSalary Slip` ss on sd.parent=ss.name
			where
				sd.parentfield='earnings'
				and sd.is_tax_applicable=1
				and is_flexible_benefit=1
				and ss.docstatus=1
				and ss.employee=%(employee)s
				and ss.start_date between %(start_date)s and %(end_date)s
				and ss.end_date between %(start_date)s and %(end_date)s
		""", {
			"employee": self.employee,
			"start_date": payroll_period.start_date,
			"end_date": self.start_date
		})[0][0])

		# get total benefits claimed
		total_benefits_claimed = flt(frappe.db.sql("""
			select sum(claimed_amount)
			from `tabEmployee Benefit Claim`
			where
				docstatus=1
				and employee=%s
				and claim_date between %s and %s
		""", (self.employee, payroll_period.start_date, self.end_date))[0][0])

		return total_benefits_paid - total_benefits_claimed

	def get_total_exemption_amount(self, payroll_period, tax_slab):
		total_exemption_amount = 0
		if tax_slab.allow_tax_exemption:
			if self.deduct_tax_for_unsubmitted_tax_exemption_proof:
				exemption_proof = frappe.db.get_value("Employee Tax Exemption Proof Submission",
					{"employee": self.employee, "payroll_period": payroll_period.name, "docstatus": 1},
					["exemption_amount"])
				if exemption_proof:
					total_exemption_amount = exemption_proof
			else:
				declaration = frappe.db.get_value("Employee Tax Exemption Declaration",
					{"employee": self.employee, "payroll_period": payroll_period.name, "docstatus": 1},
					["total_exemption_amount"])
				if declaration:
					total_exemption_amount = declaration

			total_exemption_amount += flt(tax_slab.standard_tax_exemption_amount)

		return total_exemption_amount

	def get_income_form_other_sources(self, payroll_period):
		return frappe.get_all("Employee Other Income",
			filters={
				"employee": self.employee,
				"payroll_period": payroll_period.name,
				"company": self.company,
				"docstatus": 1
			},
			fields="SUM(amount) as total_amount"
		)[0].total_amount

	def calculate_tax_by_tax_slab(self, annual_taxable_earning, tax_slab):
		data = self.get_data_for_eval()
		data.update({"annual_taxable_earning": annual_taxable_earning})
		tax_amount = 0
		for slab in tax_slab.slabs:
			if slab.condition and not self.eval_tax_slab_condition(slab.condition, data):
				continue
			if not slab.to_amount and annual_taxable_earning >= slab.from_amount:
				tax_amount += (annual_taxable_earning - slab.from_amount + 1) * slab.percent_deduction *.01
				continue
			if annual_taxable_earning >= slab.from_amount and annual_taxable_earning < slab.to_amount:
				tax_amount += (annual_taxable_earning - slab.from_amount + 1) * slab.percent_deduction *.01
			elif annual_taxable_earning >= slab.from_amount and annual_taxable_earning >= slab.to_amount:
				tax_amount += (slab.to_amount - slab.from_amount + 1) * slab.percent_deduction * .01

		# other taxes and charges on income tax
		for d in tax_slab.other_taxes_and_charges:
			if flt(d.min_taxable_income) and flt(d.min_taxable_income) > annual_taxable_earning:
				continue

			if flt(d.max_taxable_income) and flt(d.max_taxable_income) < annual_taxable_earning:
				continue

			tax_amount += tax_amount * flt(d.percent) / 100

		return tax_amount

	def eval_tax_slab_condition(self, condition, data):
		try:
			condition = condition.strip()
			if condition:
				return frappe.safe_eval(condition, self.whitelisted_globals, data)
		except NameError as err:
			frappe.throw(_("{0} <br> This error can be due to missing or deleted field.").format(err),
				title=_("Name error"))
		except SyntaxError as err:
			frappe.throw(_("Syntax error in condition: {0}").format(err))
		except Exception as e:
			frappe.throw(_("Error in formula or condition: {0}").format(e))
			raise

	def get_component_totals(self, component_type, depends_on_payment_days=0):
		joining_date, relieving_date = frappe.get_cached_value("Employee", self.employee,
			["date_of_joining", "relieving_date"])

		total = 0.0
		for d in self.get(component_type):
			if not d.do_not_include_in_total:
				if depends_on_payment_days:
					amount = self.get_amount_based_on_payment_days(d, joining_date, relieving_date)[0]
				else:
					amount = flt(d.amount, d.precision("amount"))
				total += amount
		return total

	def set_component_amounts_based_on_payment_days(self):
		joining_date, relieving_date = frappe.get_cached_value("Employee", self.employee,
			["date_of_joining", "relieving_date"])

		if not relieving_date:
			relieving_date = getdate(self.end_date)

		if not joining_date:
			frappe.throw(_("Please set the Date Of Joining for employee {0}").format(frappe.bold(self.employee_name)))

		for component_type in ("earnings", "deductions"):
			for d in self.get(component_type):
				d.amount = flt(self.get_amount_based_on_payment_days(d, joining_date, relieving_date)[0], d.precision("amount"))

	def set_loan_repayment(self):
		self.total_loan_repayment = 0
		self.total_interest_amount = 0
		self.total_principal_amount = 0

		if not self.get('loans'):
			for loan in self.get_loan_details():

				amounts = calculate_amounts(loan.name, self.posting_date, "Regular Payment")

				if amounts['interest_amount'] or amounts['payable_principal_amount']:
					self.append('loans', {
						'loan': loan.name,
						'total_payment': amounts['interest_amount'] + amounts['payable_principal_amount'],
						'interest_amount': amounts['interest_amount'],
						'principal_amount': amounts['payable_principal_amount'],
						'loan_account': loan.loan_account,
						'interest_income_account': loan.interest_income_account
					})

		for payment in self.get('loans'):
			amounts = calculate_amounts(payment.loan, self.posting_date, "Regular Payment")
			total_amount = amounts['interest_amount'] + amounts['payable_principal_amount']
			if payment.total_payment > total_amount:
				frappe.throw(_("""Row {0}: Paid amount {1} is greater than pending accrued amount {2} against loan {3}""")
					.format(payment.idx, frappe.bold(payment.total_payment),
						frappe.bold(total_amount), frappe.bold(payment.loan)))

			self.total_interest_amount += payment.interest_amount
			self.total_principal_amount += payment.principal_amount

			self.total_loan_repayment += payment.total_payment

	def get_loan_details(self):
		return frappe.get_all("Loan",
			fields=["name", "interest_income_account", "loan_account", "loan_type"],
			filters = {
				"applicant": self.employee,
				"docstatus": 1,
				"repay_from_salary": 1,
			})

	def make_loan_repayment_entry(self):
		for loan in self.loans:
			repayment_entry = create_repayment_entry(loan.loan, self.employee,
				self.company, self.posting_date, loan.loan_type, "Regular Payment", loan.interest_amount,
				loan.principal_amount, loan.total_payment)

			repayment_entry.save()
			repayment_entry.submit()

			frappe.db.set_value("Salary Slip Loan", loan.name, "loan_repayment_entry", repayment_entry.name)

	def cancel_loan_repayment_entry(self):
		for loan in self.loans:
			if loan.loan_repayment_entry:
				repayment_entry = frappe.get_doc("Loan Repayment", loan.loan_repayment_entry)
				repayment_entry.cancel()
				
	def email_salary_slip(self):
		receiver = frappe.db.get_value("Employee", self.employee, "personal_email")
		payroll_settings = frappe.get_single("Payroll Settings")
		message=f"<html>Dear <b>"+str(self.employee_name)+"</b>,<br><br>Please find the Salary Slip for the month of <b>"+str(self.month)+" - 2022</b> attached with this mail.<br><br><u><i>Let’s work with more cheerfulness towards achieving our goal !!</i></u><br><br>Thanks & Regards,<br>HR - WTT"
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

	def update_status(self, salary_slip=None):
		for data in self.timesheets:
			if data.time_sheet:
				timesheet = frappe.get_doc('Timesheet', data.time_sheet)
				timesheet.salary_slip = salary_slip
				timesheet.flags.ignore_validate_update_after_submit = True
				timesheet.set_status()
				timesheet.save()

	def set_status(self, status=None):
		'''Get and update status'''
		if not status:
			status = self.get_status()
		self.db_set("status", status)


	def process_salary_structure(self, for_preview=0):
		'''Calculate salary after salary structure details have been updated'''
		if not self.salary_slip_based_on_timesheet:
			self.get_date_details()
		self.pull_emp_details()
		self.get_working_days_details(for_preview=for_preview)
		self.calculate_net_pay()

	def pull_emp_details(self):
		emp = frappe.db.get_value("Employee", self.employee, ["bank_name", "bank_ac_no", "salary_mode"], as_dict=1)
		if emp:
			self.mode_of_payment = emp.salary_mode
			self.bank_name = emp.bank_name
			self.bank_account_no = emp.bank_ac_no

	@frappe.whitelist()
	def process_salary_based_on_working_days(self):
		self.get_working_days_details(lwp=self.leave_without_pay)
		self.calculate_net_pay()

	@frappe.whitelist()
	def set_totals(self):
		self.gross_pay = 0.0
		if self.salary_slip_based_on_timesheet == 1:
			self.calculate_total_for_salary_slip_based_on_timesheet()
		else:
			self.total_deduction = 0.0
			if hasattr(self, "earnings"):
				for earning in self.earnings:
					self.gross_pay += flt(earning.amount, earning.precision("amount"))
			if hasattr(self, "deductions"):
				for deduction in self.deductions:
					self.total_deduction += flt(deduction.amount, deduction.precision("amount"))
			self.net_pay = flt(self.gross_pay) - flt(self.total_deduction) - flt(self.total_loan_repayment)
		self.set_base_totals()

	def set_base_totals(self):
		self.base_gross_pay = flt(self.gross_pay) * flt(self.exchange_rate)
		self.base_total_deduction = flt(self.total_deduction) * flt(self.exchange_rate)
		self.rounded_total = rounded(self.net_pay)
		self.base_net_pay = flt(self.net_pay) * flt(self.exchange_rate)
		self.base_rounded_total = rounded(self.base_net_pay)
		self.set_net_total_in_words()

	#calculate total working hours, earnings based on hourly wages and totals
	def calculate_total_for_salary_slip_based_on_timesheet(self):
		if self.timesheets:
			self.total_working_hours = 0
			for timesheet in self.timesheets:
				if timesheet.working_hours:
					self.total_working_hours += timesheet.working_hours

		wages_amount = self.total_working_hours * self.hour_rate
		self.base_hour_rate = flt(self.hour_rate) * flt(self.exchange_rate)
		salary_component = frappe.db.get_value('Salary Structure', {'name': self.salary_structure}, 'salary_component')
		if self.earnings:
			for i, earning in enumerate(self.earnings):
				if earning.salary_component == salary_component:
					self.earnings[i].amount = wages_amount
				self.gross_pay += self.earnings[i].amount
		self.net_pay = flt(self.gross_pay) - flt(self.total_deduction)

	def compute_year_to_date(self):
		year_to_date = 0
		period_start_date, period_end_date = self.get_year_to_date_period()

		salary_slip_sum = frappe.get_list('Salary Slip',
			fields = ['sum(net_pay) as sum'],
			filters = {'employee_name' : self.employee_name,
				'start_date' : ['>=', period_start_date],
				'end_date' : ['<', period_end_date],
				'name': ['!=', self.name],
				'docstatus': 1
			})

		year_to_date = flt(salary_slip_sum[0].sum) if salary_slip_sum else 0.0

		year_to_date += self.net_pay
		self.year_to_date = year_to_date

	def compute_month_to_date(self):
		month_to_date = 0
		first_day_of_the_month = get_first_day(self.start_date)
		salary_slip_sum = frappe.get_list('Salary Slip',
			fields = ['sum(net_pay) as sum'],
			filters = {'employee_name' : self.employee_name,
				'start_date' : ['>=', first_day_of_the_month],
				'end_date' : ['<', self.start_date],
				'name': ['!=', self.name],
				'docstatus': 1
			})

		month_to_date = flt(salary_slip_sum[0].sum) if salary_slip_sum else 0.0

		month_to_date += self.net_pay
		self.month_to_date = month_to_date

	def compute_component_wise_year_to_date(self):
		period_start_date, period_end_date = self.get_year_to_date_period()

		for key in ('earnings', 'deductions'):
			for component in self.get(key):
				year_to_date = 0
				component_sum = frappe.db.sql("""
					SELECT sum(detail.amount) as sum
					FROM `tabSalary Detail` as detail
					INNER JOIN `tabSalary Slip` as salary_slip
					ON detail.parent = salary_slip.name
					WHERE
						salary_slip.employee_name = %(employee_name)s
						AND detail.salary_component = %(component)s
						AND salary_slip.start_date >= %(period_start_date)s
						AND salary_slip.end_date < %(period_end_date)s
						AND salary_slip.name != %(docname)s
						AND salary_slip.docstatus = 1""",
						{'employee_name': self.employee_name, 'component': component.salary_component, 'period_start_date': period_start_date,
							'period_end_date': period_end_date, 'docname': self.name}
				)

				year_to_date = flt(component_sum[0][0]) if component_sum else 0.0
				year_to_date += component.amount
				component.year_to_date = year_to_date

	def get_year_to_date_period(self):
		payroll_period = get_payroll_period(self.start_date, self.end_date, self.company)

		if payroll_period:
			period_start_date = payroll_period.start_date
			period_end_date = payroll_period.end_date
		else:
			# get dates based on fiscal year if no payroll period exists
			fiscal_year = get_fiscal_year(date=self.start_date, company=self.company, as_dict=1)
			period_start_date = fiscal_year.year_start_date
			period_end_date = fiscal_year.year_end_date

		return period_start_date, period_end_date

	def add_leave_balances(self):
		self.set('leave_details', [])

		if frappe.db.get_single_value('Payroll Settings', 'show_leave_balances_in_salary_slip'):
			from erpnext.hr.doctype.leave_application.leave_application import get_leave_details
			leave_details = get_leave_details(self.employee, self.end_date)

			for leave_type, leave_values in iteritems(leave_details['leave_allocation']):
				self.append('leave_details', {
					'leave_type': leave_type,
					'total_allocated_leaves': flt(leave_values.get('total_leaves')),
					'expired_leaves': flt(leave_values.get('expired_leaves')),
					'used_leaves': flt(leave_values.get('leaves_taken')),
					'pending_leaves': flt(leave_values.get('pending_leaves')),
					'available_leaves': flt(leave_values.get('remaining_leaves'))
				})

def unlink_ref_doc_from_salary_slip(ref_no):
	linked_ss = frappe.db.sql_list("""select name from `tabSalary Slip`
	where journal_entry=%s and docstatus < 2""", (ref_no))
	if linked_ss:
		for ss in linked_ss:
			ss_doc = frappe.get_doc("Salary Slip", ss)
			frappe.db.set_value("Salary Slip", ss_doc.name, "journal_entry", "")

def generate_password_for_pdf(policy_template, employee):
	employee = frappe.get_doc("Employee", employee)
	return policy_template.format(**employee.as_dict())

def get_salary_component_data(component):
	return frappe.get_value(
		"Salary Component",
		component,
		[
			"name as salary_component",
			"depends_on_payment_days",
			"salary_component_abbr as abbr",
			"do_not_include_in_total",
			"is_tax_applicable",
			"is_flexible_benefit",
			"variable_based_on_taxable_salary",
		],
		as_dict=1,
	)
