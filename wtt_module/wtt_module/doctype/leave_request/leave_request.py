import frappe
from frappe.model.document import Document
from datetime import date,datetime,timedelta
import calendar
from frappe.utils import getdate
import pytz
from pytz import timezone
from datetime import datetime
import calendar

class LeaveRequest(Document):
	def validate(self):
		if(self.workflow_state == 'Created'):
			if(self.proceed_to_take_leave or frappe.session.user == 'Administrator'):
				pass
			else:
				for i in self.leave_table:
					if(i.leave_type == 'Casual Leave' or i.leave_type == 'Earned Leave' or i.leave_type == 'Balance Leave'):
						indian_timezone = pytz.timezone('Asia/Kolkata')
						now_indian = datetime.now(indian_timezone)
						fr_time=str(i.from_date)+" 09:05:00"
						date = indian_timezone.localize(datetime.strptime(fr_time, '%Y-%m-%d %H:%M:%S'))
						if date <= now_indian:
							frappe.throw("Can't raise the taken leave now.")
						else:
							pass
		for i in self.leave_table:
			dt = datetime.strptime(str(i.from_date), '%Y-%m-%d')
			if(self.year == str(dt.year)):
				pass
			else:
				frappe.throw("Row "+str(i.idx)+" is not allowed, Please choose the date within the year")
		self.set_date_month()
		# self.leaves_applied_and_restrict_to_apply()
		v=0
		for i in self.leave_table:
			if(i.leave_type == 'Leave Without Pay' or i.leave_type == 'Emergency leave'):
				pass
			else:
				v=1
		if(v==1):
			self.leaves_applied_and_restrict_to_apply()
		self.create_calendar()

		seen_value=set()
		for i in self.leave_table:
			if i.from_date in seen_value:
				frappe.throw(("Date ({0}) is repeated in the table.").format(i.from_date))
			seen_value.add(i.from_date)

	def restrict_cas(self):
		pass
	def leaves_applied_and_restrict_to_apply(self):
		year=int(self.year)
		first_day = f"{year}-01-01"
		last_day = f"{year}-12-31"

		same_sl=0
		same_el=0
		same_cl=0
		for i in self.leave_table:
			if(i.leave_type=="Sick Leave"):
				same_sl=same_sl+i.no_of_days
			if(i.leave_type=="Earned Leave"):
				same_el=same_el+i.no_of_days
			if(i.leave_type=="Casual Leave"):
				same_cl=same_cl+i.no_of_days
			if(i.leave_type == 'Balance Leave'):
				frappe.throw("Balance leave is valid only in 2023.")

		for i in self.leave_table:
			if(i.leave_type=="Sick Leave"):
				qq = frappe.db.sql("SELECT * FROM `tabLeave Allocation` WHERE employee='"+str(self.employee)+"' and from_date<='"+str(i.from_date)+"' and leave_type='Sick Leave' and docstatus=1",as_dict=1)
				if(qq):
					pass
				else:
					frappe.throw("Not Enough Sick Leave")

		for i in self.leave_table:
			if(i.leave_type=="Earned Leave"):
				qq = frappe.db.sql("SELECT * FROM `tabLeave Allocation` WHERE employee='"+str(self.employee)+"' and from_date<='"+str(i.from_date)+"' and leave_type='Sick Leave' and docstatus=1",as_dict=1)
				if(qq):
					pass
				else:
					frappe.throw("Not Enough Earned Leave")

		sl_leave = 0
		el_leave = 0
		sl_leave = frappe.db.get_value("Leave Allocation", { "employee": self.employee, "leave_type": "Sick Leave", "from_date": (">=", first_day), "to_date": ("<=", last_day), "docstatus": 1 }, "total_leaves_allocated")
		el_leave = frappe.db.get_value("Leave Allocation", { "employee": self.employee, "leave_type": "Earned Leave", "from_date": (">=", first_day), "to_date": ("<=", last_day), "docstatus": 1 }, "total_leaves_allocated")

		act_sl_count=0
		act_sl = frappe.db.sql("SELECT sum(lt.no_of_days) as nos_days FROM `tabLeave Request` as lr INNER JOIN `tabLeave table` as lt ON lr.name=lt.parent WHERE lt.leave_type='Sick Leave' and lt.from_date>='"+str(first_day)+"' AND lt.from_date<='"+str(last_day)+"' AND lr.employee='"+str(self.employee)+"' and lt.status!='Not Taken' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' and lr.name!='"+str(self.name)+"'",as_dict=1)
		for i in act_sl:
			act_sl_count = i.nos_days

		act_el_count=0
		act_el = frappe.db.sql("SELECT sum(lt.no_of_days) as nos_days FROM `tabLeave Request` as lr INNER JOIN `tabLeave table` as lt ON lr.name=lt.parent WHERE lt.leave_type='Earned Leave' and lt.from_date>='"+str(first_day)+"' AND lt.from_date<='"+str(last_day)+"' AND lr.employee='"+str(self.employee)+"'  and lt.status!='Not Taken' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' and lr.name!='"+str(self.name)+"'",as_dict=1)
		for i in act_el:
			act_el_count = i.nos_days

		act_cl_count=0
		act_cl = frappe.db.sql("SELECT sum(lt.no_of_days) as nos_days FROM `tabLeave Request` as lr INNER JOIN `tabLeave table` as lt ON lr.name=lt.parent WHERE lt.leave_type='Casual Leave' and lt.from_date>='"+str(first_day)+"' AND lt.from_date<='"+str(last_day)+"' AND lr.employee='"+str(self.employee)+"' and lt.status!='Not Taken' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' and lr.name!='"+str(self.name)+"'",as_dict=1)
		for i in act_cl:
			act_cl_count = i.nos_days

		if(act_sl_count):
			pass
		else:
			act_sl_count=0

		if(act_el_count):
			pass
		else:
			act_el_count=0

		if(act_cl_count):
			pass
		else:
			act_cl_count=0

		if(sl_leave):
			pass
		else:
			sl_leave=0

		if(el_leave):
			pass
		else:
			el_leave=0

		if(same_sl):
			pass
		else:
			same_sl=0

		if(same_el):
			pass
		else:
			same_el=0

		if(same_cl):
			pass
		else:
			same_cl=0
		
		for i in self.leave_table:
			if(i.leave_type=="Sick Leave"):
				if((act_sl_count + same_sl) >sl_leave):
					frappe.throw("Not Enough Sick Leave")

			if(i.leave_type=="Earned Leave"):
				if((act_el_count + same_el) >el_leave):
					frappe.throw("Not Enough Earned Leave")
		#Casual Leave
			if(i.leave_type=="Casual Leave"):
				ful_sun=[]
				half_sun=[]
				for k in frappe.db.sql("SELECT attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(first_day)+"' and attendance_date<='"+str(last_day)+"' AND DAYOFWEEK(attendance_date) = 1 and status='Present' and employee='"+str(self.employee)+"'",as_dict=1):
					ful_sun.append(k.attendance_date)

				for l in frappe.db.sql("SELECT attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(first_day)+"' and attendance_date<='"+str(last_day)+"' AND DAYOFWEEK(attendance_date) = 1 and status='Half Day' and employee='"+str(self.employee)+"'",as_dict=1):
					half_sun.append(l.attendance_date)

				ful_sun_count = len(ful_sun)
				half_sun_count = len(half_sun)

				total_ded = ful_sun_count + (half_sun_count/2)
				query1=frappe.db.sql("SELECT count(name) as count FROM `tabAttendance` where status='Present' and docstatus=1 and employee='"+str(self.employee)+"' and attendance_date>='"+str(first_day)+"' and attendance_date<='"+str(last_day)+"'",as_dict=1)
				query2=frappe.db.sql("SELECT count(name) as count FROM `tabAttendance` where status='Half Day' and docstatus=1 and employee='"+str(self.employee)+"' and attendance_date>='"+str(first_day)+"' and attendance_date<='"+str(last_day)+"'",as_dict=1)
				pr=query1[0]["count"]
				ab=query2[0]["count"]/2
				present_days=((pr+ab)-total_ded)/23.3
				available_cl=(round(present_days/2,2))
				ovv_cl = act_cl_count + same_cl
				if(ovv_cl>available_cl):
					frappe.throw("Not Enough Casual Leave")

		# date1=date.today().replace(day=1)
		# date2=(date1+timedelta(days=32)).replace(day=1)-timedelta(days=1)
		# oo=0
		# cl=0
		# sl=0
		# bl=0
		# for i in self.leave_table:
		# 	if(i.leave_type=="Earned Leave"):
		# 		if(getdate(i.from_date)>getdate("2023-01-01")):
		# 			frappe.throw("Sick and Casual Leave are only Eligible")
		# 		if(i.alt_date==None):
		# 			oo=oo+i.no_of_days

		# 	if(i.leave_type=="Sick Leave"):
		# 		sl+=i.no_of_days

		# 	if(i.leave_type=="Casual Leave"):
		# 		cl+=i.no_of_days

		# 	if(i.leave_type=="Balance Leave"):
		# 		bl+=i.no_of_days

		# cc=datetime.strptime(str(self.month),"%B")
		# mm=cc.month
		# d1=date1.replace(day=1,month=mm)
		# d0=(d1+timedelta(days=32)).replace(day=1)
		# d2=d0-timedelta(days=1)
		# el=frappe.db.get_value("Employee",self.employee,"eligible_leave")
		# bal_lev=frappe.db.get_value("Balance Leave",{"employee":self.employee},"total")
		# if(bal_lev==None):
		# 	bal_lev=0
		# sick_leave = frappe.db.get_value("Leave Allocation",{"employee":self.employee,"leave_type":"Sick Leave"},"balance_leave")
		# if(sick_leave==None):
		# 	sick_leave=0
		# # casual_leave = frappe.db.get_value("Leave Allocation",{"employee":self.employee,"leave_type":"Casual Leave"},"balance_leave")
		# casual_leave = 0
		# this_year_date=date.today().replace(day=1,month=12,year=2022)
		# if (frappe.db.exists("Leave Request",{"employee":self.employee})):
		# 	dop=frappe.db.sql("SELECT sum(lt.no_of_days)as no_of_days,lt.leave_type from `tabLeave Request`as lr,`tabLeave table`as lt WHERE lt.parent=lr.name and lt.alt_date is NULL and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' and lr.employee='" +str(self.employee)+ "' and lt.from_date>='" +str(d1)+ "' and lt.from_date<='" +str(d2)+ "' and lt.from_date!='" +str(i.from_date)+ "' and lt.from_date!='" +str(i.alt_date)+ "' and lr.name!='"+str(self.name)+"' and lt.from_date>='"+str(this_year_date)+"' GROUP BY lt.leave_type ",as_dict=1)
		# 	for i in dop:
		# 		if(i.leave_type=="Earned Leave"):
		# 			oo=oo+i.no_of_days
		# 		if(i.leave_type=="Casual Leave"):
		# 			cl=cl+i.no_of_days
		# 		if(i.leave_type=="Sick Leave"):
		# 			sl=sl+i.no_of_days
		# 		if(i.leave_type=="Balance Leave"):
		# 			bl=bl+i.no_of_days
		# # frappe.msgprint(str(sl))
		# if(sl>sick_leave):
		# 	frappe.throw("Not Enough Sick Leaves are Available")
		# elif(sl>2):
		# 	lt=[]
		# 	for i in self.leave_table:
		# 		lt.append(i.leave_type)

		# 	if(self.attachment==None and "Sick Leave" in lt):
		# 		frappe.throw("Attachment is Mandatory for more than 2 Sick Leaves")

		# if(bl>bal_lev):
		# 	if(self.year == 2023):
		# 		frappe.throw("Not Enough balance Leave")

		# for i in self.leave_table:
		# 	if(i.leave_type=="Leave Without Pay"):
		# 		pass
		# 	else:
		# 		if(i.leave_type=="Casual Leave"):
		# 			self.check_casual_leave(cl)

	def check_casual_leave(self,cl):
		casual_leave_doctype=frappe.db.sql("SELECT * from `tabCasual Leave` where employee='"+str(self.employee)+"' ",as_dict=1)
		leave_allocated=frappe.db.sql("SELECT from_date,to_date from `tabLeave Allocation` where leave_type='Sick Leave' and docstatus=1 and employee='"+str(self.employee)+"' ORDER BY creation DESC LIMIT 1",as_dict=1)
		if(leave_allocated):
			year_start=leave_allocated[0].from_date
			year_end=leave_allocated[0].to_date

			ful_sun=[]
			half_sun=[]
			for k in frappe.db.sql("SELECT attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(year_start)+"' and attendance_date<='"+str(year_end)+"' AND DAYOFWEEK(attendance_date) = 1 and status='Present' and employee='"+str(self.employee)+"'",as_dict=1):
				ful_sun.append(k.attendance_date)

			for l in frappe.db.sql("SELECT attendance_date FROM `tabAttendance` WHERE attendance_date>='"+str(year_start)+"' and attendance_date<='"+str(year_end)+"' AND DAYOFWEEK(attendance_date) = 1 and status='Half Day' and employee='"+str(self.employee)+"'",as_dict=1):
				half_sun.append(l.attendance_date)

			ful_sun_count = len(ful_sun)
			half_sun_count = len(half_sun)

			total_ded = ful_sun_count + (half_sun_count/2)
			query1=frappe.db.sql("SELECT count(name) as count FROM `tabAttendance` where status='Present' and docstatus=1 and employee='"+str(self.employee)+"' and attendance_date>='"+str(year_start)+"' and attendance_date<='"+str(year_end)+"'",as_dict=1)
			query2=frappe.db.sql("SELECT count(name) as count FROM `tabAttendance` where status='Half Day' and docstatus=1 and employee='"+str(self.employee)+"' and attendance_date>='"+str(year_start)+"' and attendance_date<='"+str(year_end)+"'",as_dict=1)
			pr=query1[0]["count"]
			ab=query2[0]["count"]/2
			present_days=((pr+ab)-total_ded)/23.3
			availed_casual_leave=0
			if(casual_leave_doctype):
				availed_casual_leave = casual_leave_doctype[0]["total"]
			available_cl=(round(present_days/2,2))-availed_casual_leave
			if(cl<=available_cl):
				pass
			else:
				frappe.throw("Not Enough Casual Leaves Earned.")
		else:
			frappe.throw("Not Enough Casual Leaves Earned.")

	def set_date_month(self):
		mr=[]
		pr=[]
		temp_list=[]
		temp_list1=[]
		val=0
		for i in self.leave_table:
			if(i.status!='Rejected'):
				val=val+i.no_of_days
		for i in self.leave_table:
			if(i.status!='Rejected'):
				d = datetime.strptime(str(i.from_date), '%Y-%m-%d')
				e = datetime.strptime(str(i.to_date), '%Y-%m-%d')
				v=date.strftime(d,"%d")
				u=date.strftime(e,"%d")
				temp_list.append(str(v))
				temp_list1.append(val)
		unique_item = set(temp_list)
		unique_item1 = set(temp_list1)

		for j in unique_item:
			mr.append(j)

		for k in unique_item1:
			pr.append(k)

		str1 = ','.join(str(e) for e in mr)
		str2 = ','.join(str(f) for f in pr)

		self.leave_date=str1
		self.no_of_days=str2
		# self.year=2023

	def create_calendar(self):
		for i in self.leave_table:
			if not (frappe.db.exists("Leave Calendar",{"request_number":i.name,"request_name":i.parent})):				
				doc=frappe.new_doc("Leave Calendar")
				doc.employee=self.employee
				doc.employee_name=self.employee_name
				doc.from_date=i.from_date
				doc.to_date=i.to_date
				doc.reason=i.explanation
				doc.leave_type=i.leave_type
				doc.request_number=str(i.name)
				doc.request_name=self.name
				doc.color="#29CD42"
				doc.status=i.status
				doc.save()
			else:
				# doc=frappe.db.sql("UPDATE  `tabLeave Calendar` set from_date='" +str(i.from_date)+ "',to_date='" +str(i.to_date)+ "',reason='" +str(i.explanation)+ "',leave_type='" +str(i.leave_type)+ "',request_number='" +str(i.name)+ "',status='" +str(i.status)+ "' where request_number='" +str(i.name)+ "' ")
				frappe.db.sql("DELETE from `tabLeave Calendar`  where request_name='"+str(self.name)+"' ")
				doc=frappe.new_doc("Leave Calendar")
				doc.employee=self.employee
				doc.employee_name=self.employee_name
				doc.from_date=i.from_date
				doc.to_date=i.to_date
				doc.reason=i.explanation
				doc.leave_type=i.leave_type
				doc.request_number=str(i.name)
				doc.request_name=self.name
				doc.color="#29CD42"
				doc.status=i.status
				doc.save()

	def on_cancel(self):
		frappe.db.sql("UPDATE `tabLeave Request` set approved_by='"+str(frappe.session.user_fullname)+"' WHERE name='"+str(self.name)+"' ")
	def on_trash(self):		
		for i in self.leave_table:
			if frappe.db.exists("Leave Calendar",{"request_number":i.name}):				
				doc=frappe.db.sql("DELETE from `tabLeave Calendar` where request_number='" +str(i.name)+ "'")

	def on_submit(self):
		# for i in self.leave_table:
		# 	same_day_leave = frappe.db.sql("SELECT * FROM `tabLeave table` as lt INNER JOIN `tabLeave Request` as lr ON lr.name=lt.parent WHERE lr.workflow_state not in ('Cancelled','Rejected') and lr.name!='"+str(self.name)+"' and lr.department='"+str(self.department)+"' and lt.from_date='"+str(i.from_date)+"'",as_dict=1)
		# 	if(same_day_leave):
		# 		if(self.proceed_to_take_leave):
		# 			pass
		# 		else:
		# 			frappe.throw("Same department person can't be raised same day")
		# 	else:
		# 		pass
		self.del_task()
		for i in self.get("leave_table"):
			dd=date.today().replace(day=1)
			ab=date.today()
			ddd=(ab.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
			if(i.leave_type=="Earned Leave"):
				if(i.alt_date==True):
					if frappe.db.exists("Leave Request",{"employee":self.employee}):
						dop=frappe.db.sql("UPDATE `tabLeave Request`as lr,`tabLeave table`as lt SET lt.status='Rejected' WHERE lt.parent=lr.name and lt.leave_type='Earned Leave' and lr.employee='" +str(self.employee)+ "' and lt.from_date='" +str(i.alt_date)+ "' and lt.from_date='" +str(i.alt_date)+ "' and lt.from_date!='" +str(i.from_date)+ "' and lt.remarks!='Taken' ")
		arr=[]
		for j in self.get("leave_table"):
			if(j.alt_date!=None):
				dd=date.today()
				cc=datetime.strptime(str(self.month), "%B")
				mm=cc.month
				doc=frappe.db.sql("SELECT lr.name,lt.from_date,lt.to_date,lt.leave_type,lt.day,lt.no_of_days,lt.explanation,lt.remarks,lt.status,lr.workflow_state from `tabLeave Request`as lr,`tabLeave table`as lt WHERE lt.parent=lr.name and lr.employee='"+str(self.employee)+"' and lt.from_date='"+str(j.alt_date)+"' and lt.to_date='"+str(j.alt_date)+"' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' and lr.name!='"+str(self.name)+"' ",as_dict=1)
				if doc:
					for i in doc:
						frappe.db.set_value('Leave Request', i.name, {
							'docstatus': 0,
							'workflow_state':'Rejected'
						})
					dok1=frappe.get_doc("Leave Request",i.name)
					for je in dok1.get("leave_table"):
						if(je.from_date!=j.alt_date):
							arr.append({
								"from_date":je.from_date,
								"to_date":je.to_date,
								"leave_type":je.leave_type,
								"day":je.day,
								"no_of_days":je.no_of_days,
								"explanation":je.explanation,
								"status":je.status,
								"remarks":je.remarks
								})

		for i in arr:
			self.append("leave_table",{
				"from_date":i["from_date"],
				"to_date":i["to_date"],
				"leave_type":i["leave_type"],
				"day":i["day"],
				"no_of_days":i["no_of_days"],
				"explanation":i["explanation"],
				"status":i["status"],
				"remarks":i["remarks"]
				})
		self.submit()

		# self.update_casual_leave()
	def update_casual_leave(self):
		cls_approved=0
		for i in self.leave_table:
			if(i.leave_type=="Casual Leave"):
				if(frappe.db.sql("SELECT * from `tabCasual Leave` where employee='"+str(self.employee)+"' ",as_dict=1)):
					cl_doc=frappe.get_doc("Casual Leave",str(self.employee))
					cl_doc.append('casual_leave_table',{
						"date":i.from_date,
						"leave_approved":i.no_of_days
						})
					cl_doc.save()
				else:
					cl_doc=frappe.new_doc("Casual Leave")
					cl_doc.employee=self.employee
					cl_doc.append('casual_leave_table',{
						"date":i.from_date,
						"leave_approved":i.no_of_days
						})
					cl_doc.save()

	def del_task(self):
		for i in self.leave_table:
			frappe.db.sql("DELETE from `tabTask Allocation` where date='"+str(getdate(i.from_date))+"' and employee='"+str(self.employee)+"' ")

	@frappe.whitelist()
	def casual_leave_availability(self):
		solution=""
		dates=[]
		leave_allocated=frappe.db.sql("SELECT from_date from `tabLeave Allocation` where leave_type='Sick Leave' and docstatus=1 and employee='"+str(self.employee)+"' ",as_dict=1)
		if(leave_allocated):
			year_start=leave_allocated[0].from_date
			# year_start=getdate("2023-01-01")
			casual_leave_availed = frappe.db.get_list('Salary Slip',
				fields=['sum(casual_leave) as casual_leave','employee'],
				group_by='employee'
			)

			cl_availed=0
			for j in casual_leave_availed:
				if(j["employee"]==self.employee):
					cl_availed+=float(j["casual_leave"])

			present=0
			for i in self.leave_table:
				if(i.leave_type=="Casual Leave"):
					present = frappe.db.count('Attendance', filters=[
						['attendance_date', 'between', [str(year_start), str(i.from_date)]],
						['status','=','Present'],
						['employee','=',self.employee],
						['docstatus','=',1]
						])
					val = round((present/46.6),1)-cl_availed
					if(val<i.no_of_days):
						solution="error"
		else:
			solution="error"				

		return solution


@frappe.whitelist()
def check_leave(emp,year):
	year=int(year)
	date1=date.today().replace(day=1,month=1,year=year)
	date2=(date1+timedelta(days=32)).replace(day=1,month=1,year=year+1)-timedelta(days=1)
	ar=[]
	leave_allocated=frappe.db.sql("SELECT from_date,to_date from `tabLeave Allocation` where leave_type='Sick Leave' and docstatus=1 and employee='"+str(emp)+"' and from_date>='"+str(date1)+"' and to_date<='"+str(date2)+"'",as_dict=1)
	if(leave_allocated):
		year_start=leave_allocated[0].from_date
		year_end=leave_allocated[0].to_date
		query1 = frappe.db.sql("SELECT total_leaves_allocated from `tabLeave Allocation` where docstatus=1 and employee='"+str(emp)+"' and from_date>='"+str(date1)+"' and to_date<='"+str(date2)+"' and leave_type='Sick Leave' LIMIT 1",as_dict=1) 
		el_avail = frappe.db.sql("SELECT total_leaves_allocated from `tabLeave Allocation` where docstatus=1 and employee='"+str(emp)+"' and from_date>='"+str(date1)+"' and to_date<='"+str(date2)+"' and leave_type='Earned Leave' LIMIT 1",as_dict=1) 
		total_el=0
		total_sl = 0

		for i in el_avail:
			total_el=total_el+i.total_leaves_allocated
		for i in query1:
			total_sl=total_sl+i.total_leaves_allocated

		query2 = frappe.db.sql("SELECT sum(`tabSalary Slip`.`sick_leave`) as 'sl_taken' FROM `tabSalary Slip` WHERE `tabSalary Slip`.`docstatus`!=2 and `tabSalary Slip`.`workflow_state`!='Rejected' and `tabSalary Slip`.`posting_date`>='"+str(year_start)+"' and `tabSalary Slip`.`posting_date`<='"+str(year_end)+"' and `tabSalary Slip`.`employee`='"+str(emp)+"' GROUP BY `tabSalary Slip`.`employee`",as_dict=1)
		taken_sl = 0
		for i in query2:
			taken_sl = taken_sl + i.sl_taken

		query2 = frappe.db.sql("SELECT sum(`tabSalary Slip`.`earned_leave`) as 'el_taken' FROM `tabSalary Slip` WHERE `tabSalary Slip`.`docstatus`!=2 and `tabSalary Slip`.`workflow_state`!='Rejected' and `tabSalary Slip`.`posting_date`>='"+str(year_start)+"' and `tabSalary Slip`.`posting_date`<='"+str(year_end)+"' and `tabSalary Slip`.`employee`='"+str(emp)+"' GROUP BY `tabSalary Slip`.`employee`",as_dict=1)
		taken_el = 0
		for i in query2:
			taken_el = taken_el + i.el_taken

		asv={
			"total_sl":total_sl,
			"total_el":total_el,
			"sl_taken":taken_sl,
			"el_taken":taken_el
			}
		query4=frappe.db.sql("""SELECT 
			IF((SELECT total from `tabBalance Leave` where employee=`tabSalary Slip`.`employee`)>0, (SELECT total from `tabBalance Leave` where employee=`tabSalary Slip`.`employee`), 0) as "balance_leave",
			IF(((SELECT total_leaves_allocated from `tabLeave Allocation` where docstatus=1 and employee=`tabSalary Slip`.`employee` and from_date>='"""+str(year_start)+"""' and to_date<='"""+str(year_end)+"""' and leave_type="Sick Leave"))>0, ROUND(((SELECT count(distinct(name)) from `tabAttendance` where docstatus=1 and status='Present' and employee=`tabSalary Slip`.`employee` and DAYOFWEEK(attendance_date) != 1 and attendance_date>='"""+str(year_start)+"""' and attendance_date<='"""+str(year_end)+"""')+((SELECT count(distinct(name)) from `tabAttendance` where docstatus=1 and status='Half Day' and employee=`tabSalary Slip`.`employee` and DAYOFWEEK(attendance_date) != 1 and attendance_date>='"""+str(year_start)+"""' and attendance_date<='"""+str(year_end)+"""')/2))/46.6,2), 0) as "total_cl",
			sum(`tabSalary Slip`.`casual_leave`)as "cl_taken"
			FROM `tabSalary Slip`
			where `tabSalary Slip`.`docstatus`!=2 and `tabSalary Slip`.`workflow_state`!='Rejected' and `tabSalary Slip`.`posting_date`>='"""+str(year_start)+"""' and `tabSalary Slip`.`posting_date`<='"""+str(year_end)+"""' and `tabSalary Slip`.`employee`='"""+str(emp)+"""'
			group by `tabSalary Slip`.`employee`
			""",as_dict=1)
		for i in query4:
			ar.append(i.update(asv))

		if(ar):
			pass
		else:
			vvs={
				"total_sl":total_sl,
				"total_el":total_el,
				"sl_taken":taken_sl,
				"el_taken":taken_el,
				"balance_leave":0,
				"total_cl":0,
				"cl_taken":0
			}
			ar.append(vvs)
	else:
		vvs={
			"total_sl":0,
			"total_el":0,
			"sl_taken":0,
			"el_taken":0,
			"balance_leave":0,
			"total_cl":0,
			"cl_taken":0
		}
		ar.append(vvs)
	return ar
	# ar=[]
	# leave_allocated=frappe.db.sql("SELECT from_date,to_date from `tabLeave Allocation` where leave_type='Sick Leave' and docstatus=1 and employee='"+str(emp)+"' ORDER BY creation DESC LIMIT 1",as_dict=1)
	# if(leave_allocated):
	# 	year_start=leave_allocated[0].from_date
	# 	year_end=leave_allocated[0].to_date
	# 	query1 = frappe.db.sql("SELECT total_leaves_allocated from `tabLeave Allocation` where docstatus=1 and employee='"+str(emp)+"' and leave_type='Sick Leave' LIMIT 1",as_dict=1) 
	# 	total_sl = 0
	# 	for i in query1:
	# 		total_sl=total_sl+i.total_leaves_allocated

	# 	query2 = frappe.db.sql("SELECT sum(`tabSalary Slip`.`sick_leave`) as 'sl_taken' FROM `tabSalary Slip` WHERE `tabSalary Slip`.`docstatus`!=2 and `tabSalary Slip`.`workflow_state`!='Rejected' and `tabSalary Slip`.`posting_date`>='"+str(year_start)+"' and `tabSalary Slip`.`posting_date`<='"+str(year_end)+"' and `tabSalary Slip`.`employee`='"+str(emp)+"' GROUP BY `tabSalary Slip`.`employee`",as_dict=1)
	# 	taken_sl = 0
	# 	for i in query2:
	# 		taken_sl = taken_sl + i.sl_taken

	# 	doc=frappe.db.sql("SELECT lt.from_date,lr.employee from `tabLeave Request`as lr,`tabLeave table`as lt WHERE lt.parent=lr.name and lr.employee='"+str(emp)+"' and lt.leave_type='Sick Leave' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' ",as_dict=1)
	# 	sl_taken=0
	# 	for i in doc:
	# 		doc=frappe.db.sql("SELECT status FROM `tabAttendance` WHERE attendance_date='"+str(i.from_date)+"' AND employee='"+str(i.employee)+"'",as_dict=1)
	# 		if doc:
	# 			for j in doc:
	# 				if(j.status=='Present'):
	# 					sl_taken=sl_taken+0
	# 				elif(j.status=='Absent'):
	# 					sl_taken=sl_taken+1
	# 				elif(j.status=='Half Day'):
	# 					sl_taken=sl_taken+0.5

	# 	doc=frappe.db.sql("SELECT lt.from_date,lr.employee,lt.no_of_days from `tabLeave Request`as lr,`tabLeave table`as lt WHERE lt.parent=lr.name and lr.employee='"+str(emp)+"' and lt.leave_type='Sick Leave' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' ",as_dict=1)
	# 	vs=0
	# 	for i in doc:
	# 		v_att=frappe.db.sql("SELECT status FROM `tabAttendance` WHERE attendance_date='"+str(i.from_date)+"' AND employee='"+str(i.employee)+"'",as_dict=1)
	# 		if v_att:
	# 			pass
	# 		else:
	# 			vs = vs + i.no_of_days
		
	# 	total_taken = vs + sl_taken
	# 	sl_applied = total_taken - taken_sl


	# 	doc=frappe.db.sql("SELECT lt.from_date,lr.employee from `tabLeave Request`as lr,`tabLeave table`as lt WHERE lt.parent=lr.name and lr.employee='"+str(emp)+"' and lt.leave_type='Casual Leave' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' ",as_dict=1)
	# 	taken_cl=0
	# 	for i in doc:
	# 		doc=frappe.db.sql("SELECT status FROM `tabAttendance` WHERE attendance_date='"+str(i.from_date)+"' AND employee='"+str(i.employee)+"'",as_dict=1)
	# 		if doc:
	# 			for j in doc:
	# 				if(j.status=='Present'):
	# 					taken_cl=taken_cl+0
	# 				elif(j.status=='Absent'):
	# 					taken_cl=taken_cl+1
	# 				elif(j.status=='Half Day'):
	# 					taken_cl=taken_cl+0.5

	# 	doc=frappe.db.sql("SELECT lt.from_date,lr.employee,lt.no_of_days from `tabLeave Request`as lr,`tabLeave table`as lt WHERE lt.parent=lr.name and lr.employee='"+str(emp)+"' and lt.leave_type='Casual Leave' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' ",as_dict=1)
	# 	vs=0
	# 	for i in doc:
	# 		v_att=frappe.db.sql("SELECT status FROM `tabAttendance` WHERE attendance_date='"+str(i.from_date)+"' AND employee='"+str(i.employee)+"'",as_dict=1)
	# 		if v_att:
	# 			pass
	# 		else:
	# 			vs = vs + i.no_of_days
		
	# 	total_taken_cl = vs + taken_cl
	# 	cl_applied = total_taken_cl - taken_cl

	# 	asv={
	# 		"total_sl":total_sl,
	# 		"sl_taken":taken_sl,
	# 		"sl_applied":sl_applied,
	# 		"cl_applied":cl_applied
	# 		}

	# 	query4=frappe.db.sql("""SELECT 
	# 		IF((SELECT total from `tabBalance Leave` where employee=`tabSalary Slip`.`employee`)>0, (SELECT total from `tabBalance Leave` where employee=`tabSalary Slip`.`employee`), 0) as "balance_leave",
	# 		IF(((SELECT total_leaves_allocated from `tabLeave Allocation` where docstatus=1 and employee=`tabSalary Slip`.`employee` and leave_type="Sick Leave"))>0, ROUND(((SELECT count(distinct(name)) from `tabAttendance` where docstatus=1 and status='Present' and employee=`tabSalary Slip`.`employee` and DAYOFWEEK(attendance_date) != 1 and attendance_date>='"""+str(year_start)+"""' and attendance_date<='"""+str(year_end)+"""')+((SELECT count(distinct(name)) from `tabAttendance` where docstatus=1 and status='Half Day' and employee=`tabSalary Slip`.`employee` and DAYOFWEEK(attendance_date) != 1 and attendance_date>='"""+str(year_start)+"""' and attendance_date<='"""+str(year_end)+"""')/2))/46.6,2), 0) as "total_cl",
	# 		sum(`tabSalary Slip`.`casual_leave`)as "cl_taken"
	# 		FROM `tabSalary Slip`
	# 		where `tabSalary Slip`.`docstatus`!=2 and `tabSalary Slip`.`workflow_state`!='Rejected' and `tabSalary Slip`.`posting_date`>='"""+str(year_start)+"""' and `tabSalary Slip`.`posting_date`<='"""+str(year_end)+"""' and `tabSalary Slip`.`employee`='"""+str(emp)+"""'
	# 		group by `tabSalary Slip`.`employee`
	# 		""",as_dict=1)
	# 	for i in query4:
	# 		ar.append(i.update(asv))

	# 	return ar


# @frappe.whitelist()
# def check_leave(emp):
# 	ar=[]
# 	leave_allocated=frappe.db.sql("SELECT from_date from `tabLeave Allocation` where leave_type='Sick Leave' and docstatus=1 and employee='"+str(emp)+"' ",as_dict=1)
# 	if(leave_allocated):
# 		year_start=leave_allocated[0].from_date
# 		query=frappe.db.sql("""SELECT 
# 			`tabSalary Slip`.`employee_name` as "employee_name",
# 			(SELECT total_leaves_allocated from `tabLeave Allocation` where docstatus=1 and employee=`tabSalary Slip`.`employee` and leave_type="Sick Leave")as "total_sl",
# 			sum(`tabSalary Slip`.`sick_leave`)as "sl_taken",
# 			IF((SELECT total from `tabBalance Leave` where employee=`tabSalary Slip`.`employee`)>0, (SELECT total from `tabBalance Leave` where employee=`tabSalary Slip`.`employee`), 0) as "balance_leave",
# 			IF(((SELECT total_leaves_allocated from `tabLeave Allocation` where docstatus=1 and employee=`tabSalary Slip`.`employee` and leave_type="Sick Leave"))>0, ROUND(((SELECT count(distinct(name)) from `tabAttendance` where docstatus=1 and status='Present' and employee=`tabSalary Slip`.`employee` and attendance_date>'"""+str(year_start)+"""')+((SELECT count(distinct(name)) from `tabAttendance` where docstatus=1 and status='Half Day' and employee=`tabSalary Slip`.`employee` and attendance_date>'"""+str(year_start)+"""')/2))/46.6,2), 0) as "total_cl",
# 			sum(`tabSalary Slip`.`casual_leave`)as "cl_taken"
# 			FROM `tabSalary Slip`
# 			where `tabSalary Slip`.`workflow_state`='Approved' and `tabSalary Slip`.`posting_date`>'2023-01-01' and `tabSalary Slip`.`employee`='"""+str(emp)+"""'
# 			group by `tabSalary Slip`.`employee_name`""",as_dict=1)
# 		for i in query:
# 			ar.append(i)
# 	return ar

#TAKEN NON TAKEN
@frappe.whitelist()
def checkatt():
	gug=date.today() - timedelta(days=1)
	doc = frappe.db.sql("SELECT employee,employee_name,attendance_date,status from `tabAttendance` where attendance_date='" +str(gug)+ "' ",as_dict=1)
	for i in doc:
		if(i.status=='Absent'):
			
			dop = frappe.db.sql("SELECT lr.employee,lr.employee_name,lt.from_date,lt.to_date,lt.leave_type,lt.status,lt.name from `tabLeave Request`as lr,`tabLeave table`as lt where lt.parent=lr.name and lt.from_date='" +str(gug)+ "' and lt.to_date='" +str(gug)+ "' and lt.status='Approved' and lr.workflow_state!='Cancelled' and lt.leave_type='Earned Leave' and lr.employee='"+str(i.employee)+"' ",as_dict=1)
			for j in dop:				
				dom = frappe.db.sql("UPDATE `tabLeave table` set remarks='Taken' where name='"+str(j.name)+"' ")
				
		elif(i.status=='Present'):
			
			dop = frappe.db.sql("SELECT lr.employee,lr.employee_name,lr.name,lt.from_date,lt.to_date,lt.leave_type,lt.status,lr.workflow_state from `tabLeave Request`as lr,`tabLeave table`as lt where lt.parent=lr.name and lt.from_date='" +str(gug)+ "' and lt.to_date='" +str(gug)+ "' and lt.status='Approved' and lr.workflow_state!='Cancelled' and lt.leave_type='Earned Leave' and lr.employee='"+str(i.employee)+"' ",as_dict=1)
			for j in dop:				
				dom = frappe.db.sql("UPDATE `tabLeave table` set remarks='Non Taken',status='Rejected' where parent='" +str(j.name)+ "'")
#SHOW LEAVES FOR THE MENTIONED MONTH
@frappe.whitelist()
def get_leave(month,emp):
	ll=[]
	year=int(year)
	month_datetime = datetime.strptime(month, "%B")
	month = month_datetime.month
	first_day = f"{year}-{month:02d}-01"
	last_day = f"{year}-{month:02d}-{calendar.monthrange(year, month)[1]}"
	vvs=frappe.db.sql("SELECT lr.name,lr.employee,lt.from_date,lt.to_date,lt.leave_type,lt.day,lt.no_of_days,lt.explanation,lr.workflow_state from `tabLeave Request`as lr,`tabLeave table`as lt WHERE lt.parent=lr.name and lr.employee='"+str(emp)+"' and lt.from_date>='"+str(first_day)+"' and lt.from_date<='"+str(last_day)+"' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' ",as_dict=1)
	for i in vvs:
		doc=frappe.db.sql("SELECT status FROM `tabAttendance` WHERE attendance_date='"+str(i.from_date)+"' AND employee='"+str(i.employee)+"'",as_dict=1)
		dat=i.from_date
		if doc:
			for j in doc:
				if(j.status=='Present'):
					st='Non Taken'
				elif(j.status=='Absent'):
					st='Taken'
				elif(j.status=='Half Day'):
					st='Half Taken'
				else:
					st=''
				ll.append({
					"from_date":dat.strftime("%d/%m/%y"),
					"to_date":i.to_date,
					"day":i.day,
					"no_of_days":i.no_of_days,
					"leave_type":i.leave_type,
					"explanation":i.explanation,
					"status":i.status,
					"remarks":st,
					"request":"Leave Request"
					})
		else:
			ll.append({
			"from_date":dat.strftime("%d/%m/%y"),
			"to_date":i.to_date,
			"day":i.day,
			"no_of_days":i.no_of_days,
			"leave_type":i.leave_type,
			"explanation":i.explanation,
			"status":i.status,
			"remarks":"Unmarked",
			"request":"Leave Request"
			})
	return ll
	# ll=[]
	# dd=date.today()
	# if(month=="December"):
	# 	dd=dd.today().replace(year=2022)
	# cc=datetime.strptime(str(month), "%B")

	# mm=cc.month
	# d1=dd.replace(day=1,month=mm)
	# d0=(d1+timedelta(days=32)).replace(day=1)
	# d2=d0-timedelta(days=1)
	# doc=frappe.db.sql("SELECT lr.name,lr.employee,lt.from_date,lt.to_date,lt.leave_type,lt.day,lt.no_of_days,lt.explanation,lr.workflow_state from `tabLeave Request`as lr,`tabLeave table`as lt WHERE lt.parent=lr.name and lr.employee='"+str(emp)+"' and lt.from_date>='"+str(d1)+"' and lt.to_date<='"+str(d2)+"' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' ",as_dict=1)
	# for i in doc:
	# 	doc=frappe.db.sql("SELECT status FROM `tabAttendance` WHERE attendance_date='"+str(i.from_date)+"' AND employee='"+str(i.employee)+"'",as_dict=1)
	# 	dat=i.from_date
	# 	if doc:
	# 		for j in doc:
	# 			if(j.status=='Present'):
	# 				st='Non Taken'
	# 			elif(j.status=='Absent'):
	# 				st='Taken'
	# 			elif(j.status=='Half Day'):
	# 				st='Half Taken'
	# 			else:
	# 				st=''
	# 			ll.append({
	# 				"from_date":dat.strftime("%d/%m/%y"),
	# 				"to_date":i.to_date,
	# 				"day":i.day,
	# 				"no_of_days":i.no_of_days,
	# 				"leave_type":i.leave_type,
	# 				"explanation":i.explanation,
	# 				"status":i.status,
	# 				"remarks":st,
	# 				"request":"Leave Request"
	# 				})
	# 	else:
	# 		ll.append({
	# 		"from_date":dat.strftime("%d/%m/%y"),
	# 		"to_date":i.to_date,
	# 		"day":i.day,
	# 		"no_of_days":i.no_of_days,
	# 		"leave_type":i.leave_type,
	# 		"explanation":i.explanation,
	# 		"status":i.status,
	# 		"remarks":"Unmarked",
	# 		"request":"Leave Request"
	# 		})
	# doc=frappe.db.sql("SELECT lr.name,lr.employee,lt.from_date,lt.to_date,lt.leave_type,lt.day,lt.no_of_days,lt.explanation,lr.workflow_state from `tabEmergency Leave`as lr,`tabEmergency Table`as lt WHERE lt.parent=lr.name and lr.employee='"+str(emp)+"' and lt.from_date>='"+str(d1)+"' and lt.to_date<='"+str(d2)+"' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' ",as_dict=1)
	# for i in doc:
	# 	doc=frappe.db.sql("SELECT status FROM `tabAttendance` WHERE attendance_date='"+str(i.from_date)+"' AND employee='"+str(i.employee)+"'",as_dict=1)
	# 	dat=i.from_date
	# 	if doc:
	# 		for j in doc:
	# 			if(j.status=='Present'):
	# 				st='Non Taken'
	# 			elif(j.status=='Absent'):
	# 				st='Taken'
	# 			elif(j.status=='Half Day'):
	# 				st='Half Taken'
	# 			else:
	# 				st=''
	# 			ll.append({
	# 				"from_date":dat.strftime("%d/%m/%y"),
	# 				"to_date":i.to_date,
	# 				"day":i.day,
	# 				"no_of_days":i.no_of_days,
	# 				"leave_type":i.leave_type,
	# 				"explanation":i.explanation,
	# 				"status":i.status,
	# 				"remarks":st,
	# 				"request":"Emergency Leave"
	# 				})
	# 	else:
	# 		ll.append({
	# 		"from_date":dat.strftime("%d/%m/%y"),
	# 		"to_date":i.to_date,
	# 		"day":i.day,
	# 		"no_of_days":i.no_of_days,
	# 		"leave_type":i.leave_type,
	# 		"explanation":i.explanation,
	# 		"status":i.status,
	# 		"remarks":"Unmarked",
	# 		"request":"Emergency Leave"
	# 		})
	# return ll


#for attendance update
@frappe.whitelist()
def checktym():
	vis=date.today()-timedelta(days=1)
	gug=vis.weekday()
	dayname=calendar.day_name[gug]
	doc = frappe.db.sql("SELECT * from `tabAttendance` WHERE attendance_date='"+str(vis)+"' and docstatus!=2 ",as_dict=1)
	for i in doc:
		if(i.shift=='workshop shift' and i.in_time!=None and i.status!="Absent"):
			vish=datetime.now().replace(hour=10,minute=31,second=00,microsecond=00)-timedelta(days=1)
			d1=datetime.now().replace(hour=19,minute=00,second=00,microsecond=00)-timedelta(days=1)

			#late entry for Half Day update
			if(i.in_time>=vish):
				frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',late_entry=0,too_late='In Time>10:31:00' WHERE name='" +str(i.name)+ "' ")
			#shift end time update
			if(i.in_time!=None and i.out_time!=None):
				if(i.out_time>=d1):
					wh=d1-i.in_time
					awh=i.out_time-i.in_time
					hrs=wh.total_seconds() / 3600
					act_hrs=awh.total_seconds() / 3600
					if(act_hrs>=9):
						frappe.db.sql("UPDATE `tabAttendance` SET status='Present',actual_working_hours='"+str(act_hrs)+"',working_hours='"+str(hrs)+"',shift_end_time='"+str(d1)+"' WHERE name='" +str(i.name)+ "' ")
					elif(act_hrs<4):
						frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',actual_working_hours='"+str(act_hrs)+"',working_hours='"+str(hrs)+"',shift_end_time='"+str(d1)+"' WHERE name='" +str(i.name)+ "' ")
					elif(act_hrs>=4):
						frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',actual_working_hours='"+str(act_hrs)+"',working_hours='"+str(hrs)+"',shift_end_time='"+str(d1)+"' WHERE name='" +str(i.name)+ "' ")
	
		elif(i.shift=='Day Shift' and i.in_time!=None and i.status!="Absent"):
			if(dayname!="Saturday"):
				vish=datetime.now().replace(hour=10,minute=31,second=00,microsecond=00)-timedelta(days=1)
				d1=datetime.now().replace(hour=18,minute=00,second=00,microsecond=00)-timedelta(days=1)
			

				#late entry for Half Day update
				if(i.in_time>=vish):
					frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',late_entry=0,too_late='In Time>10:31:00' WHERE name='" +str(i.name)+ "' ")
				
				#shift end time update
				if(i.in_time!=None and i.out_time!=None):
					if(i.out_time>=d1):
						wh=d1-i.in_time
						awh=i.out_time-i.in_time
						hrs=wh.total_seconds() / 3600
						act_hrs=awh.total_seconds() / 3600
						if(act_hrs>=7.5):
							frappe.db.sql("UPDATE `tabAttendance` SET status='Present',actual_working_hours='"+str(act_hrs)+"',working_hours='"+str(hrs)+"',shift_end_time='"+str(d1)+"' WHERE name='" +str(i.name)+ "' ")
						elif(act_hrs<3.5):
							frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',actual_working_hours='"+str(act_hrs)+"',working_hours='"+str(hrs)+"',shift_end_time='"+str(d1)+"' WHERE name='" +str(i.name)+ "' ")
						elif(act_hrs>=3.5):
							frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',actual_working_hours='"+str(act_hrs)+"',working_hours='"+str(hrs)+"',shift_end_time='"+str(d1)+"' WHERE name='" +str(i.name)+ "' ")			
				
		
		elif(dayname=="Saturday" and i.in_time!=None and i.status!="Absent"):
			vish=datetime.now().replace(hour=10,minute=1,second=00,microsecond=00)-timedelta(days=1)
			d2=vish.replace(hour=17,minute=00)
			doc = frappe.db.sql("SELECT * from `tabAttendance` WHERE attendance_date='"+str(vis)+"' ",as_dict=1)
			for i in doc:
				#late entry for Half Day update
				if(i.in_time>=vish):
					frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',late_entry=0,too_late='In Time>10:00:00' WHERE name='" +str(i.name)+ "' ")
				
				#shift end time update
				if(i.in_time!=None and i.out_time!=None):
					if(i.out_time>=d2):
						wh=d2-i.in_time
						out=i.out_time
						hrs=wh.total_seconds() / 3600
						if(hrs>=7):
							frappe.db.sql("UPDATE `tabAttendance` SET status='Present',actual_working_hours='"+str(i.working_hours)+"',working_hours='"+str(hrs)+"',shift_end_time='"+str(d2)+"' WHERE name='" +str(i.name)+ "' ")
						elif(hrs<3.5):
							frappe.db.sql("UPDATE `tabAttendance` SET status='Absent',actual_working_hours='"+str(i.working_hours)+"',working_hours='"+str(hrs)+"',shift_end_time='"+str(d2)+"' WHERE name='" +str(i.name)+ "' ")
						elif(hrs>3.5):
							frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',actual_working_hours='"+str(i.working_hours)+"',working_hours='"+str(hrs)+"',shift_end_time='"+str(d2)+"' WHERE name='" +str(i.name)+ "' ")

@frappe.whitelist()
def clientscript(lr):
	ar=[]
	doc=frappe.get_doc("Leave Request",str(lr))
	for i in doc.leave_table:
		ar.append({
			"from_date":(i.from_date).strftime("%a  %d/%m"),
			"leave_type":i.leave_type,
			"explanation":i.explanation,
			"status":i.status
			})
	return ar


# @frappe.whitelist()
# def checktym():
# 	emp=[]
# 	vis=date.today()-timedelta(days=1)
# 	guga=vis.weekday()
# 	dayname=calendar.day_name[gug]
# 	doc = frappe.db.sql("SELECT employee,employee_name,in_time,out_time,status,attendance_date,name,shift from `tabAttendance` WHERE attendance_date='"+str(vis)+"' ",as_dict=1)
# 	for i in doc:
# 		if(i.shift=='Day Shift' and dayname!='Saturday'):
# 			vish=datetime.now().replace(hour=10,minute=31,second=00,microsecond=00)-timedelta(days=1)
# 			if(i.in_time>=vish):
# 				frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',late_entry=0,too_late='In time>=10:31' WHERE name='" +str(i.name)+ "' and employee='"+str(i.employee)+"' ")
# 		elif(i.shift=='Day Shift' and dayname=='Saturday'):
# 			vish=datetime.now().replace(hour=10,minute=00,second=00,microsecond=00)-timedelta(days=1)
# 			if(i.in_time>=vish):
# 				frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',late_entry=0,too_late='In time>=10:00' WHERE name='" +str(i.name)+ "' and employee='"+str(i.employee)+"' ")
# 		elif(i.shift=='workshop shift'):
# 			vish=datetime.now().replace(hour=10,minute=31,second=00,microsecond=00)-timedelta(days=1)
# 			if(i.in_time>=vish):
# 				frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',late_entry=0,too_late='In time>=10:31' WHERE name='" +str(i.name)+ "' and employee='"+str(i.employee)+"' ")
# 		if(i.shift=='Day Shift' and dayname=='Saturday'):
# 			gug=datetime.now().replace(hour=17,minute=00,second=00,microsecond=00)-timedelta(days=1)
# 			if(i.out_time>=guga):
# 				frappe.db.sql("UPDATE `tabAttendance` SET early_exit=0 WHERE name='" +str(i.name)+ "' and employee='"+str(i.employee)+"' ")
		

# @frappe.whitelist()
# def checktym():
# 	vis=date.today()-timedelta(days=1)
# 	gug=vis.weekday()
# 	dayname=calendar.day_name[gug]
# 	if(dayname!="Saturday"):
# 		vish=datetime.now().replace(hour=10,minute=31,second=00,microsecond=00)-timedelta(days=1)
# 		d1=datetime.now().replace(hour=18,minute=00,second=00,microsecond=00)-timedelta(days=1)
# 		d2=d1.replace(hour=17)
# 		d3=d1.replace(hour=19)
# 		doc = frappe.db.sql("SELECT employee,employee_name,in_time,status,attendance_date,name,shift from `tabAttendance` WHERE attendance_date='"+str(vis)+"' ",as_dict=1)
# 		for i in doc:
# 			if(i.in_time>=vish):
# 				frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',late_entry=0 WHERE name='" +str(i.name)+ "' and employee='"+str(i.employee)+"' ")
# 		dot = frappe.db.sql("SELECT * FROM `tabAttendance` WHERE attendance_date='"+str(vis)+"'",as_dict=1)
# 		for i in dot:
# 			if(i.shift=='Day Shift'):
# 				wh=d1-i.in_time
# 				hrs=wh.total_seconds() / 3600
# 				frappe.db.sql("UPDATE `tabAttendance` SET working_hours='"+str(hrs)+"',shift_end_time='"+str(d1)+"' WHERE name='" +str(i.name)+ "' and employee='"+str(i.employee)+"' ")
# 			elif(i.shift=='workshop shift'):
# 				wh=d3-i.in_time
# 				hrs=wh.total_seconds() / 3600
# 				frappe.db.sql("UPDATE `tabAttendance` SET working_hours='"+str(hrs)+"',shift_end_time='"+str(d3)+"' WHERE name='" +str(i.name)+ "' and employee='"+str(i.employee)+"' ")
		
# 	elif(dayname=="Saturday"):
# 		vish=datetime.now().replace(hour=10,minute=1,second=00,microsecond=00)-timedelta(days=1)
# 		d2=vish.replace(hour=17,minute=00)
# 		d3=d2.replace(hour=19)
# 		doc = frappe.db.sql("SELECT employee,employee_name,in_time,status,attendance_date,name,shift from `tabAttendance` WHERE attendance_date='"+str(vis)+"' ",as_dict=1)
# 		for i in doc:
# 			if(i.in_time>=vish):
# 				frappe.db.sql("UPDATE `tabAttendance` SET status='Half Day',late_entry=0 WHERE name='" +str(i.name)+ "' and employee='"+str(i.employee)+"' ")
# 		for i in dot:
# 			if(i.shift=='Day Shift'):
# 				wh=d2-i.in_time
# 				hrs=wh.total_seconds() / 3600
# 				frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(d1)+"',working_hours='"+str(hrs)+"' WHERE name='" +str(i.name)+ "' and employee='"+str(i.employee)+"' ")
# 			elif(i.shift=='workshop shift'):
# 				wh=d3-i.in_time
# 				hrs=wh.total_seconds() / 3600
# 				frappe.db.sql("UPDATE `tabAttendance` SET shift_end_time='"+str(d3)+"',working_hours='"+str(hrs)+"' WHERE name='" +str(i.name)+ "' and employee='"+str(i.employee)+"' ")