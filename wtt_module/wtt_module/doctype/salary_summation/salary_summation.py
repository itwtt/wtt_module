# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from datetime import date,datetime,timedelta
from frappe.model.document import Document
from frappe.utils import getdate

class SalarySummation(Document):
	def validate(self):
		# dd=getdate(self.posting_date)
		# self.month=dd.strftime("%B")
		if(self.head_office is None):
			self.head_office=0
		if(self.project is None):
			self.project=0
		if(self.esi is None):
			self.esi=0
		if(self.epf is None):
			self.epf=0
		if(self.labour_welfare_fund is None):
			self.labour_welfare_fund=0
		if(self.site_worker_salary is None):
			self.site_worker_salary=0
		if(self.house_keeping is None):
			self.house_keeping=0
		if(self.last_month_arrear is None):
			self.last_month_arrear=0
		if(self.security_service is None):
			self.security_service=0
		self.total_salary=self.head_office+self.project+self.esi+self.epf+self.labour_welfare_fund+self.site_worker_salary+self.house_keeping+self.last_month_arrear+self.security_service

	@frappe.whitelist()
	def get_from_salary_slip(self):
		ar=[]
		column={}
		for i in frappe.db.sql("SELECT branch,sum(rounded_total)as tot FROM `tabSalary Slip` WHERE posting_date='"+str(self.posting_date)+"' and docstatus=0 and workflow_state!='Rejected' and workflow_state!='Cancelled' and workflow_state!='Created' GROUP BY branch",as_dict=1):
			column[i.branch]=i.tot
			for j in frappe.db.sql("SELECT sum(sldt.amount)as amt,sldt.salary_component FROM `tabSalary Slip`as sl,`tabSalary Detail` as sldt WHERE sl.name=sldt.parent and sl.docstatus=0 and sl.workflow_state='Verified by HR' and sl.posting_date='"+str(self.posting_date)+"' GROUP BY sldt.salary_component ",as_dict=1):
				if(j.salary_component=="ESI"):
					column["esi"]=j.amt
				if(j.salary_component=="Provident Fund"):
					column["pf"]=j.amt
				if(j.salary_component=="LWF"):
					column["ewf"]=j.amt
		ar.append(column)

		return ar
	@frappe.whitelist()
	def set_last_date(self):
		month=self.month
		mm=datetime.strptime(month, '%B').month
		first_date=date.today().replace(day=1,month=mm)
		next_month=(first_date+timedelta(days=32)).replace(day=1)
		last_date=next_month-timedelta(days=1)
		return last_date