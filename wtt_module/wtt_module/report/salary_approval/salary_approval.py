# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, erpnext
from frappe.utils import flt
from frappe import _
from datetime import date

def execute(filters=None):
	if not filters: filters = {}
	currency = None
	if filters.get('currency'):
		currency = filters.get('currency')
	company_currency = erpnext.get_company_currency(filters.get("company"))
	salary_slips = get_salary_slips(filters, company_currency)
	if not salary_slips: return [], []

	columns, earning_types, ded_types = get_columns(salary_slips)
	ss_earning_map = get_ss_earning_map(salary_slips, currency, company_currency)
	ss_ded_map = get_ss_ded_map(salary_slips,currency, company_currency)
	doj_map = get_employee_doj_map()
	val=""
	data = []
	for ss in salary_slips:
		row = [ss.name,ss.verified_by,ss.workflow_state,ss.employee, ss.employee_name,ss.rounded_total,ss.total_working_days,ss.punched_days,ss.approval_leave,ss.sundays,ss.national_holidays,ss.late_deduction,ss.loss_of_pay,ss.payment_days]
		if currency == company_currency:
			row = [ss.name,ss.verified_by,ss.workflow_state,ss.employee, ss.employee_name,flt(ss.rounded_total) * flt(ss.exchange_rate),ss.total_working_days,ss.punched_days,ss.approval_leave,ss.sundays,ss.national_holidays,ss.late_deduction,ss.loss_of_pay,ss.payment_days]	
		if ss.branch is not None: columns[3] = columns[3].replace('-1','120')
		if ss.department is not None: columns[4] = columns[4].replace('-1','120')
		if ss.designation is not None: columns[5] = columns[5].replace('-1','120')
		if ss.leave_without_pay is not None: columns[9] = columns[9].replace('-1','130')


		for e in earning_types:
			row.append(ss_earning_map.get(ss.name, {}).get(e))

		if currency == company_currency:
			row += [flt(ss.gross_pay) * flt(ss.exchange_rate)]
		else:
			row += [ss.gross_pay]

		for d in ded_types:
			row.append(ss_ded_map.get(ss.name, {}).get(d))

		row.append(ss.total_loan_repayment)

		if currency == company_currency:
			row += [flt(ss.total_deduction) * flt(ss.exchange_rate), flt(ss.net_pay) * flt(ss.exchange_rate)]
		else:
			row += [ss.total_deduction, ss.net_pay]
		row.append(currency or company_currency)
		row.append(ss.name)
		#frappe.msgprint(row)
		data.append(row)

	return columns, data

def get_columns(salary_slips):
	"""
	columns = [
		_("Salary Slip ID") + ":Link/Salary Slip:150",
		_("Employee") + ":Link/Employee:120",
		_("Employee Name") + "::140",
		_("Date of Joining") + "::80",
		_("Branch") + ":Link/Branch:120",
		_("Department") + ":Link/Department:120",
		_("Designation") + ":Link/Designation:120",
		_("Company") + ":Link/Company:120",
		_("Start Date") + "::80",
		_("End Date") + "::80",
		_("Leave Without Pay") + ":Float:130",
		_("Payment Days") + ":Float:120", 
		_("Currency") + ":Link/Currency:80"
	]
	"""
	columns = [
		_("Salary Slip") + ":Link/Salary Slip:120",_("Verified By") + "::140",_("Status") + "::120",
		_("Employee") + ":Link/Employee:120", _("Employee Name") + "::140",_("Rounded Total") + ":Currency:120",
		_("Total Days") + ":Float:100",_("Worked Days") + ":Float:100",_("Benefit Leave") + ":Float:100",_("Week Off") + ":Float:100",_("NH /FH") + ":Float:100",_("Late Deduction") + ":Float:120",_("Loss of Pay") + ":Float:100", _("Total") + ":Float:120"
	]

	salary_components = {_("Earning"): [], _("Deduction"): []}

	for component in frappe.db.sql("""select distinct sd.salary_component, sc.type
		from `tabSalary Detail` sd, `tabSalary Component` sc
		where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s)""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1):
		salary_components[_(component.type)].append(component.salary_component)

	columns = columns + [(e + ":Currency:120") for e in salary_components[_("Earning")]] + \
		[_("Gross Pay") + ":Currency:120"] + [(d + ":Currency:120") for d in salary_components[_("Deduction")]] + \
		[_("Loan Repayment") + ":Currency:120", _("Total Deduction") + ":Currency:120", _("Net Pay") + ":Currency:120"]

	return columns, salary_components[_("Earning")], salary_components[_("Deduction")]

def get_salary_slips(filters, company_currency):
	filters.update({"from_date": filters.get("from_date"), "to_date":filters.get("to_date"),"branch":filters.get("branch")})
	conditions, filters = get_conditions(filters, company_currency)
	salary_slips = frappe.db.sql("""select * from `tabSalary Slip` where %s order by name""" %(conditions), filters, as_dict=1)

	return salary_slips or []

def get_conditions(filters, company_currency):
	conditions = ""
	doc_status = {"Draft": 0, "Submitted": 1, "Cancelled": 2}

	if filters.get("docstatus"):
		conditions += "docstatus = {0}".format(doc_status[filters.get("docstatus")])

	if filters.get("from_date"): conditions += " and start_date >= %(from_date)s"
	if filters.get("to_date"): conditions += " and end_date <= %(to_date)s"
	if filters.get("company"): conditions += " and company = %(company)s"
	if filters.get("branch"): conditions += " and branch = %(branch)s"
	if filters.get("workflow_state"): conditions += " and workflow_state = %(workflow_state)s"
	if filters.get("employee"): conditions += " and employee = %(employee)s"
	if filters.get("currency") and filters.get("currency") != company_currency:
		conditions += " and currency = %(currency)s"

	return conditions, filters

def get_employee_doj_map():
	return	frappe._dict(frappe.db.sql("""
				SELECT
					employee,
					date_of_joining
				FROM `tabEmployee`
				"""))

def get_ss_earning_map(salary_slips, currency, company_currency):
	ss_earnings = frappe.db.sql("""select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
		from `tabSalary Detail` sd, `tabSalary Slip` ss where sd.parent=ss.name and sd.parent in (%s)""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_earning_map = {}
	for d in ss_earnings:
		ss_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		if currency == company_currency:
			ss_earning_map[d.parent][d.salary_component] = flt(d.amount) * flt(d.exchange_rate if d.exchange_rate else 1)
		else:
			ss_earning_map[d.parent][d.salary_component] = flt(d.amount)

	return ss_earning_map

def get_ss_ded_map(salary_slips, currency, company_currency):
	ss_deductions = frappe.db.sql("""select sd.parent, sd.salary_component, sd.amount, ss.exchange_rate, ss.name
		from `tabSalary Detail` sd, `tabSalary Slip` ss where sd.parent=ss.name and sd.parent in (%s)""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_ded_map = {}
	for d in ss_deductions:
		ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		if currency == company_currency:
			ss_ded_map[d.parent][d.salary_component] = flt(d.amount) * flt(d.exchange_rate if d.exchange_rate else 1)
		else:
			ss_ded_map[d.parent][d.salary_component] = flt(d.amount)

	return ss_ded_map

# @frappe.whitelist()
# def function(name):
# 	user=frappe.session.user
# 	if(user=='venkat@wttindia.com' or user=='Administrator'):
# 		frappe.db.sql("UPDATE `tabSalary Details` set verified_by='MD',docstatus=1,workflow_state='Approved' where employee='" +name+ "' ")
# 		frappe.msgprint("Approved")
# 	elif(user=='gm_admin@wttindia.com' or user=='erp@wttindia.com'):
# 		frappe.db.sql("UPDATE `tabSalary Details` set verified_by='SIVAKUMAR P',docstatus=0,workflow_state='Approved by GM' where employee='" +name+ "' ")
# 		frappe.msgprint("Approved")
# 	elif(user=='saravanakumar@wttindia.com' or user=='erp@wttindia.com'):
# 		frappe.db.sql("UPDATE `tabSalary Details` set verified_by='SARAVANAKUMAR K',docstatus=0,workflow_state='Verified by HR' where employee='" +name+ "' ")
# 		frappe.msgprint("Approved")	
# 	else:
# 		frappe.throw("Not Permitted to Approve")

# @frappe.whitelist()
# def func(name):
# 	user=frappe.session.user
# 	if(user=='venkat@wttindia.com' or user=='Administrator'):
# 		frappe.db.sql("UPDATE `tabSalary Details` set verified_by='MD',docstatus=2,workflow_state='Cancelled' where employee='" +name+ "' ")
# 		frappe.msgprint("Cancelled")
# 	elif(user=='saravanakumar@wttindia.com' or user=='erp@wttindia.com'):
# 		frappe.db.sql("UPDATE `tabSalary Details` set verified_by='SARAVANAKUMAR K',docstatus=0,workflow_state='Rejected' where employee='" +name+ "' ")
# 		frappe.msgprint("Rejected")	
# 	elif(user=='gm_admin@wttindia.com' or user=='erp@wttindia.com'):
# 		frappe.db.sql("UPDATE `tabSalary Details` set verified_by='SIVAKUMAR P',docstatus=0,workflow_state='Rejected' where employee='" +name+ "' ")
# 		frappe.msgprint("Rejected")
# 	else:
# 		frappe.throw("Not Permitted to Reject")


@frappe.whitelist()
def function(name):
	user=frappe.session.user
	if(user=='venkat@wttindia.com' or user=='Administrator' or user=='priya@wttindia.com'):
		doc=frappe.get_doc("Salary Slip",str(name))   
		doc.verified_by='MD'
		doc.docstatus=1
		doc.workflow_state='Approved'
		doc.submit()
	
	elif(user=='sarnita@wttindia.com'):
		doc=frappe.get_doc("Salary Slip",str(name))   
		doc.verified_by='ED'
		doc.docstatus=1
		doc.workflow_state='Approved'
		doc.submit()   
	
	elif(user=='gm_admin@wttindia.com' or user=='erp@wttindia.com'):
		doc=frappe.get_doc("Salary Slip",str(name))   
		doc.verified_by='SIVAKUMAR P'
		doc.docstatus=0
		doc.workflow_state='Approved by GM'
		doc.save()
	
	elif(user=='praveen@wtt1301.com' or user=='erp@wttindia.com' or user=='siju.v@wtt1376.com'):
		doc=frappe.get_doc("Salary Slip",str(name))   
		doc.verified_by='PRAVEEN S'
		doc.docstatus=0
		doc.workflow_state='Verified by HR'
		doc.save()
	
	else:
		frappe.throw("Not Permitted to Approve")

	# frappe.msgprint("Approved")
	return user

@frappe.whitelist()
def func(name):
	user=frappe.session.user
	if(user=='venkat@wttindia.com' or user=='Administrator' or user=='priya@wttindia.com'):
		frappe.db.sql("UPDATE `tabSalary Slip` set verified_by='MD',docstatus=2,workflow_state='Cancelled' where name='" +name+ "' ")
		frappe.msgprint("Cancelled")
	elif(user=='sarnita@wttindia.com'):
		frappe.db.sql("UPDATE `tabSalary Slip` set verified_by='ED',docstatus=2,workflow_state='Cancelled' where name='" +name+ "' ")
		frappe.msgprint("Cancelled")
	elif(user=='praveen@wtt1301.com' or user=='erp@wttindia.com'):
		frappe.db.sql("UPDATE `tabSalary Slip` set verified_by='PRAVEEN S',docstatus=0,workflow_state='Rejected' where name='" +name+ "' ")
		frappe.msgprint("Rejected")	
	elif(user=='gm_admin@wttindia.com' or user=='erp@wttindia.com'):
		frappe.db.sql("UPDATE `tabSalary Slip` set verified_by='SIVAKUMAR P',docstatus=0,workflow_state='Rejected' where name='" +name+ "' ")
		frappe.msgprint("Rejected")
	else:
		frappe.throw("Not Permitted to Reject")

	return user
	
@frappe.whitelist()
def additionals(name):
	user=frappe.session.user
	doc=frappe.get_doc("Salary Slip",str(name))  
	doc.workflow_state='Created'
	doc.save()
	frappe.msgprint("Success")
	

@frappe.whitelist()
def create_statement(name):
	salary_doc=frappe.get_doc("Salary Slip",str(name))
	start_date = str(salary_doc.start_date)
	end_date = str(salary_doc.end_date)
	a1=a2=[]
	charge=0


	doc=frappe.new_doc("Final Salary Statement")
	doc.posting_date = date.today()
	doc.from_date = str(start_date)
	doc.end_date = str(end_date)
	doc.bank_name = "Indian Bank - INDIAN BANK"
	query1=frappe.db.sql("SELECT distinct(employee)as employee,employee_name,rounded_total FROM `tabSalary Slip` WHERE workflow_state='Approved' and posting_date>='"+str(start_date)+"' and posting_date<='"+str(end_date)+"' order by employee_name",as_dict=1)
	for i in query1:
		if(float(i.rounded_total)<float(10000)):
			crg=2
		elif(float(i.rounded_total)>float(10000) and float(i.rounded_total)<float(100000)):
			crg=5
		elif(float(i.rounded_total)>float(100000) and float(i.rounded_total)<float(200000)):
			crg=13
		elif(float(i.rounded_total)>float(200000) and float(i.rounded_total)<float(500000)):
			crg=28
		elif(float(i.rounded_total)>float(500000)):
			crg=56

		if(frappe.db.get_value('Employee',i.employee,'bank_name')=="INDIAN BANK"):
			a2.append(float(i.rounded_total))
			doc.append("salary2",{
				"employee_name":i.employee_name,
				"account_no":frappe.db.get_value('Employee',i.employee,'bank_ac_no'),
				"ifsc_code":frappe.db.get_value('Employee',i.employee,'ifsc_code'),
				"bank_name":frappe.db.get_value('Employee',i.employee,'bank_name'),
				"charges":0,
				"amount":i.rounded_total
				})
		else:
			a1.append(i.rounded_total)
			charge+=crg
			doc.append("salary",{
				"employee_name":i.employee_name,
				"account_no":frappe.db.get_value('Employee',i.employee,'bank_ac_no'),
				"ifsc_code":frappe.db.get_value('Employee',i.employee,'ifsc_code'),
				"bank_name":frappe.db.get_value('Employee',i.employee,'bank_name'),
				"charges":crg,
				"amount":i.rounded_total
				})
	doc.charge1=charge
	doc.total1=sum(a1)
	doc.total2=sum(a2)
	doc.total3=sum(a1)+charge
	doc.total4=sum(a2)
	doc.save()
	frappe.msgprint("Salary Statement Created Successfully")


@frappe.whitelist()
def email(nn):
	if(nn==None):
		pass
	else:
		doc=frappe.get_doc("Salary Slip",str(nn))
		receiver = frappe.db.get_value("Employee", doc.employee, "personal_email")
		payroll_settings = frappe.get_single("Payroll Settings")
		message=f"<html>Dear <b>"+str(doc.employee_name)+"</b>,<br><br>Please find the Salary Slip for the month of <b>"+str(doc.month)+" - 2023</b> attached with this mail.<br><br><u><i>Let’s work with more cheerfulness towards achieving our goal !!</i></u><br><br>Thanks & Regards,<br>HR - WTT"
		password = None
		if payroll_settings.encrypt_salary_slips_in_emails:
			password = generate_password_for_pdf(payroll_settings.password_policy, doc.employee)
			message += """<br>Note: Your salary slip is password protected,
				the password to unlock the PDF is of the format {0}. """.format(payroll_settings.password_policy)

		if receiver:
			email_args = {
				"recipients": [receiver],
				"message": _(message),
				"subject": 'Salary Slip - from {0} to {1}'.format(doc.start_date, doc.end_date),
				"attachments": [frappe.attach_print(doc.doctype, doc.name, file_name=doc.name, password=password)],
				"reference_doctype": doc.doctype,
				"reference_name": doc.name
				}
			if not frappe.flags.in_test:
				enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
			else:
				frappe.sendmail(**email_args)
		else:
			msgprint(_("{0}: Employee email not found, hence email not sent").format(doc.employee_name))

frappe.whitelist()
def draft(nn):
	frappe.db.sql("UPDATE `tabSalary Slip` SET docstatus=0,workflow_state='Created' WHERE name='"+str(nn)+"' ")

	# salary_doc=frappe.get_doc("Salary Slip",str(name))
	# query = frappe.db.sql("SELECT * from `tabFinal Salary Statement` WHERE from_date='"+str(salary_doc.start_date)+"' and to_date='"+str(salary_doc.end_date)+"' ORDER BY posting_date DESC LIMIT 1",as_dict=1)
	# if(query):
	# 	for i in query:
	# 		doc=frappe.get_doc("Final Salary Statement",str(i.name))
	# 		if(frappe.db.get_value("Employee",salary_doc.employee,"bank_name")=="INDIAN BANK"):
	# 			doc.append("salary2",{
	# 				"employee_name":salary_doc.employee_name,
	# 				"bank_name":frappe.db.get_value("Employee",salary_doc.employee,"bank_name"),
	# 				"account_no":frappe.db.get_value("Employee",salary_doc.employee,"bank_ac_no"),
	# 				"ifsc_code":frappe.db.get_value("Employee",salary_doc.employee,"ifsc_code"),
	# 				"amount":str(salary_doc.rounded_total)
	# 			})
	# 		else:
	# 			doc.append("salary",{
	# 				"employee_name":salary_doc.employee_name,
	# 				"bank_name":frappe.db.get_value("Employee",salary_doc.employee,"bank_name"),
	# 				"account_no":frappe.db.get_value("Employee",salary_doc.employee,"bank_ac_no"),
	# 				"ifsc_code":frappe.db.get_value("Employee",salary_doc.employee,"ifsc_code"),
	# 				"amount":str(salary_doc.rounded_total)
	# 			})
	# 		doc.save()
	# else:
	# 	doc=frappe.new_doc("Final Salary Statement")
	# 	doc.posting_date=date.today()
	# 	doc.from_date=salary_doc.start_date
	# 	doc.to_date=salary_doc.end_date
	# 	if(frappe.db.get_value("Employee",salary_doc.employee,"bank_name")=="INDIAN BANK"):
	# 		doc.append("salary2",{
	# 			"employee_name":salary_doc.employee_name,
	# 			"bank_name":frappe.db.get_value("Employee",salary_doc.employee,"bank_name"),
	# 			"account_no":frappe.db.get_value("Employee",salary_doc.employee,"bank_ac_no"),
	# 			"ifsc_code":frappe.db.get_value("Employee",salary_doc.employee,"ifsc_code"),
	# 			"amount":str(salary_doc.rounded_total)
	# 		})
	# 	else:
	# 		doc.append("salary",{
	# 			"employee_name":salary_doc.employee_name,
	# 			"bank_name":frappe.db.get_value("Employee",salary_doc.employee,"bank_name"),
	# 			"account_no":frappe.db.get_value("Employee",salary_doc.employee,"bank_ac_no"),
	# 			"ifsc_code":frappe.db.get_value("Employee",salary_doc.employee,"ifsc_code"),
	# 			"amount":str(salary_doc.rounded_total)
	# 		})
	# 	doc.save()
	# frappe.msgprint("done")
