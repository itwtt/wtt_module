# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date,datetime,timedelta
import json
from frappe.utils import getdate,cstr, flt, get_link_to_form



class ClaimRequest(Document):
	def validate(self):
		pass
		# dd=date.today()
		# if(self.workflow_state=="Created" and self.employee!='WTT1408' and frappe.session.user!='praveen@wtt1301.com'):
		# 	ar=[]
		# 	for i in self.expenses:
		# 		ar.append(i.expense_date)
		# 	dif=(dd-getdate(min(ar))).days
		# 	if(dif>3):
		# 		# pass
		# 		frappe.throw("Claim Should be Raised within 2 working days for "+str(min(ar)))
		
	def on_cancel(self):
		if(frappe.db.exists("Expense Claim",{"claim_request":self.name})):
			doc=frappe.get_doc("Expense Claim",{"claim_request":self.name})
			doc.delete()
		query=frappe.db.sql("SELECT ss.name from `tabSalary Slip`as ss,`tabClaim Reference`as cr where cr.parent=ss.name and cr.claim_request='"+str(self.name)+"' ",as_dict=1)
		if(query):
			doc=frappe.get_doc("Salary Slip",str(query[0].name))
			if(doc.workflow_state=="Approved"):
				frappe.throw("Salary Slip "+str(query[0].name)+" Approved")
			else:
				thedetail=None
				for detail in doc.claim_reference:
					thedetail=None
					if(detail.claim_request==self.name):
						thedetail=detail
				if(thedetail!=None):doc.remove(thedetail)
				for detail in doc.earnings:
					thedetail=None
					if(detail.salary_component=="Expense Claim"):
						thedetail=detail
				if(thedetail!=None):doc.remove(thedetail)
				for detail in doc.deductions:
					thedetail=None
					if(detail.salary_component=="Advance"):
						thedetail=detail
				if(thedetail!=None):doc.remove(thedetail)
				doc.save()


	def on_trash(self):
		if(frappe.db.exists("Expense Claim",{"claim_request":self.name})):
			doc=frappe.get_doc("Expense Claim",{"claim_request":self.name})
			doc.delete()

	# def on_submit(self):
		#self.create_expense_claim()

	def create_expense_claim(self):
		data = frappe.new_doc("Expense Claim")
		data.posting_date = self.posting_date
		data.employee = self.employee
		data.expense_approver = self.expense_approver
		data.remark=self.remark
		data.payable_account='Travelling Exp (Fuel Claim) - WTT'
		data.approval_status="Approved"
		data.cost_center="Main - WTT"
		data.claim_request = self.name

		condition = 'docstatus=1 and employee={0} and paid_amount > 0 and paid_amount > claimed_amount + return_amount'.format(frappe.db.escape(self.employee))	
		query1 = frappe.db.sql("""
			select
				name, posting_date, paid_amount, claimed_amount, advance_account
			from
				`tabEmployee Advance`
			where {0}
		""".format(condition), as_dict=1)

		for cr in query1:
			condition = 'name={0}'.format(frappe.db.escape(cr.name))
		query = frappe.db.sql("""
			select
				name, posting_date, paid_amount, claimed_amount, advance_account
			from
				`tabEmployee Advance`
			where {0}
		""".format(condition), as_dict=1)

		for i in self.get("expenses"):
			if(i.status=="Approved"):
				if(i.expense_type=='Fuel (Bike)' or i.expense_type=='Fuel (Car)'):
					val='Fuel'
				else:
					val=i.expense_type
				if(i.expense_type=='Fuel (Bike)' or i.expense_type=='Fuel (Car)' or i.expense_type=='Food' or i.expense_type=='Travel' or i.expense_type=='Medical'):
					acc='Travelling Exp (Fuel Claim) - WTT'
				
				data.append("expenses",{
					"expense_date":i.expense_date,
					"expense_type":val,
					"description":i.description,
					"amount":i.amount,
					"sanctioned_amount":i.amount,
					"cost_center":"Main - WTT"
					})		
		data.save()
		adv_ar=[]
		for d in query:
			gt=data.total_claimed_amount
			if(data.total_claimed_amount>flt(d.paid_amount) - flt(d.claimed_amount)):
				gt=(flt(d.paid_amount) - flt(d.claimed_amount))
			adv_ar.append(flt(d.paid_amount) - flt(d.claimed_amount))
			data.append("advances",{
				"employee_advance":d.name,
				"posting_date":d.posting_date,
				"advance_account":d.advance_account,
				"advance_paid":d.paid_amount,
				"unclaimed_amount":flt(d.paid_amount) - flt(d.claimed_amount),
				"allocated_amount":gt
				})
		if(len(adv_ar)>0):
			data.total_advance_amount=sum(adv_ar)
		data.mode_of_payment='NEFT/RTGS/IMPS'
		data.clearance_date=date.today()
		data.cost_center="Main - WTT"
		# data.save()
		data.submit()
		
@frappe.whitelist()
def check_od(arr,emp):
	data=[]
	dt=[]
	odar=[]
	to_python = json.loads(arr)
	for i in to_python:
		if(i["date"] not in dt):
			dt.append(i["date"])
	
	doc=frappe.db.sql("SELECT * from `tabOn duty request` WHERE employee='"+str(emp)+"' ",as_dict=1)
	for od in doc:
		dd1 = datetime.strptime(str(od.from_time), '%Y-%m-%d %H:%M:%S')
		# for i in dt:
		if(str(dd1.date()) in dt):
			odar.append({
				"from_time":dd1.date().strftime("%d/%m/%y"),
				# "to_time":od.to_time,
				"hours":round(od.hours,2),
				"reason":od.explanation,
				"status":od.workflow_state,
				"od_name":od.name
				})
	return odar
