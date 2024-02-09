# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date,datetime,timedelta
from num2words import num2words
class FarmSalarySlip(Document):
	# pass
	def validate(self):
		if self.advance!=None and self.additional!=None:
			self.net_total=self.total+self.additional-self.advance
			self.in_words=num2words(self.net_total)
		elif self.advance!=None:
			self.net_total=self.total-self.advance
			self.in_words=num2words(self.net_total)
		elif self.additional!=None:
			self.net_total=self.total+self.additional
			self.in_words=num2words(self.net_total)

		# pass
		# aa=bb=cc=0
		# start="2022-02-01"
		# b4=str(self.posting_date)
		# aaa=datetime.strptime(start, '%Y-%m-%d')
		# bbb=datetime.strptime(b4, '%Y-%m-%d')
		# dayst=(bbb+timedelta(days=1))-aaa
		# doc=frappe.db.sql("SELECT * from `tabFarm Attendance` WHERE attendance_date>='"+str(start)+"' and attendance_date<='"+str(self.posting_date)+"' and employee='"+str(self.employee)+"' ",as_dict=1)
		# for i in doc:
		# 	if(i.status=='Present'):
		# 		aa=aa+1	
		# 	elif(i.status=='Absent'):
		# 		bb=bb+1	
		# 	elif(i.status=='Half Day'):
		# 		cc=cc+1
		# dd=dayst.days
		# wd=dd-2
		# pd=aa+(cc/2)
		# self.present_days=pd
		# self.absent_days=bb
		# self.working_days=dd
		# if(pd>=wd):
		# 	pass
		# 	# self.approval_leave=bb
		# 	# self.payment_days=pd+bb
		# 	# self.loss_of_pay=0
		# # else:
		# self.approval_leave=0
		# self.payment_days=pd
		# self.loss_of_pay=bb # end of else
		# salary=frappe.db.get_value('Farm Employee',self.employee,'salary')
		# self.total=(salary/dd)*self.payment_days
		# self.net_total=round(self.total)
		# self.in_words=num2words(self.net_total)