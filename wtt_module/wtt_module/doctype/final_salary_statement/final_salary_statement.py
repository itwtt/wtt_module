# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from num2words import num2words
import json
from frappe.utils.xlsxutils import make_xlsx

class FinalSalaryStatement(Document):
	def validate(self):
		# pass
		valword=num2words(self.total3, lang='en_IN')
		self.in_words1=valword.capitalize()

		valword2=num2words(self.total4, lang='en_IN')
		self.in_words2=valword2.capitalize()


@frappe.whitelist()
def update_salary(fr_date,to_date,company):
	arr=[]
	arr2=[]
	if(company=="WTT INTERNATIONAL PVT LTD"):
		query1=frappe.db.sql("SELECT employee,employee_name,rounded_total FROM `tabSalary Slip` WHERE workflow_state='Approved' and posting_date>='"+str(fr_date)+"' and posting_date<='"+str(to_date)+"' order by employee_name",as_dict=1)
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

			
			arr.append({
				"employee_name":i.employee_name,
				"account_no":frappe.db.get_value('Employee',i.employee,'bank_ac_no'),
				"ifsc_code":frappe.db.get_value('Employee',i.employee,'ifsc_code'),
				"bank_name":frappe.db.get_value('Employee',i.employee,'bank_name'),
				"charges":crg,
				"amount":i.rounded_total
				})
	else:
		query1=frappe.db.sql("SELECT employee,employee_name,net_total FROM `tabFarm Salary Slip` WHERE workflow_state='Approved' and posting_date>='"+str(fr_date)+"' and posting_date<='"+str(to_date)+"' order by employee_name",as_dict=1)
		for i in query1:
			if(float(i.net_total)<float(10000)):
				crg=2
			elif(float(i.net_total)>float(10000) and float(i.net_total)<float(100000)):
				crg=5
			elif(float(i.net_total)>float(100000) and float(i.net_total)<float(200000)):
				crg=13
			elif(float(i.net_total)>float(200000) and float(i.net_total)<float(500000)):
				crg=28
			elif(float(i.net_total)>float(500000)):
				crg=56

			
			arr.append({
				"employee_name":i.employee_name,
				"account_no":frappe.db.get_value('Farm Employee',i.employee,'account_no'),
				"ifsc_code":frappe.db.get_value('Farm Employee',i.employee,'ifsc_code'),
				"bank_name":frappe.db.get_value('Farm Employee',i.employee,'bank'),
				"charges":crg,
				"amount":i.net_total
				})
		
	return arr
@frappe.whitelist()
def get_arrear(fr_date,to_date,company):
	query1=frappe.db.sql("SELECT employee,employee_name,arrear_amount FROM `tabArrear Table` WHERE docstatus=1 and parent='ARR-CAL-00002' order by employee_name",as_dict=1)
	arr=[]
	for i in query1:
		if(float(i.arrear_amount)<float(10000)):
			crg=2
		elif(float(i.arrear_amount)>float(10000) and float(i.arrear_amount)<float(100000)):
			crg=5
		elif(float(i.arrear_amount)>float(100000) and float(i.arrear_amount)<float(200000)):
			crg=13
		elif(float(i.arrear_amount)>float(200000) and float(i.arrear_amount)<float(500000)):
			crg=28
		elif(float(i.arrear_amount)>float(500000)):
			crg=56
		arr.append({
			"employee_name":i.employee_name,
			"account_no":frappe.db.get_value('Employee',i.employee,'bank_ac_no'),
			"ifsc_code":frappe.db.get_value('Employee',i.employee,'ifsc_code'),
			"bank_name":frappe.db.get_value('Employee',i.employee,'bank_name'),
			"charges":crg,
			"amount":i.arrear_amount
			})
	return arr



@frappe.whitelist()
def create_excel(doc):
	to_python = json.loads(doc)
	ur=[]
	xl=[["BENIFICIARY NAME","ACCOUNT NO","IFSC CODE","BANK","CHARGES","AMOUNT"]]
	for i in to_python:
		xl.append([i["employee_name"],i["account_no"],i["ifsc_code"],i["bank_name"],i["charges"],i["amount"]])
	
	xlsx_file = make_xlsx(xl, "Salary_Table")
	file_data = xlsx_file.getvalue()

	_file = frappe.get_doc({
	"doctype": "File",
	"file_name": "Salary_Table.xlsx",
	"folder": "Home/Attachments",
	"content": file_data})
	_file.save()
	ur.append({"url":_file.file_url})
	return ur


@frappe.whitelist()
def create_excel_ib(doc):
	to_python = json.loads(doc)
	ur=[]
	xl=[["BENIFICIARY NAME","ACCOUNT NO","IFSC CODE","BANK","CHARGES","AMOUNT"]]
	for i in to_python:
		xl.append([i["employee_name"],i["account_no"],i["ifsc_code"],i["bank_name"],i["charges"],i["amount"]])
	
	xlsx_file = make_xlsx(xl, "Salary_Table_IB")
	file_data = xlsx_file.getvalue()

	_file = frappe.get_doc({
	"doctype": "File",
	"file_name": "Salary_Table_IB.xlsx",
	"folder": "Home/Attachments",
	"content": file_data})
	_file.save()
	ur.append({"url":_file.file_url})
	return ur

