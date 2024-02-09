# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import traceback
import datetime
from datetime import datetime, date

class CashRequest(Document):
	def on_submit(self):
		dd = str(self.transaction_date)
		ds=date.today()
		fdate=ds.replace(day=5)
		date_from_string = datetime.strptime(dd, "%Y-%m-%d")
		if(date_from_string.date()>fdate):
			if(self.grand_total<=2000):
				if(frappe.session.user=="karthi@wtt1401.com" or frappe.session.user == 'gm_admin@wttindia.com' or frappe.session.user == 'sarnita@wttindia.com' or frappe.session.user == 'venkat@wttindia.com' or frappe.session.user == 'priya@wttindia.com'):
					pass
				else:
					frappe.throw("Need Accounts Manager approval for this request.")
			elif(self.grand_total<=4000):
				if(frappe.session.user == 'gm_admin@wttindia.com' or frappe.session.user == 'sarnita@wttindia.com' or frappe.session.user == 'venkat@wttindia.com' or frappe.session.user == 'priya@wttindia.com'):
					pass
				else:
					frappe.throw("Need GM sir approval for this request.")
			elif(self.grand_total<=6000):
				if(frappe.session.user == 'sarnita@wttindia.com' or frappe.session.user == 'venkat@wttindia.com' or frappe.session.user == 'priya@wttindia.com'):
					pass
				else:
					frappe.throw("Need ED Mam approval for this request.")
			elif(self.grand_total>6000):
				if(frappe.session.user == 'sarnita@wttindia.com' or frappe.session.user == 'venkat@wttindia.com' or frappe.session.user == 'priya@wttindia.com'):
					pass
				else:
					frappe.throw("Need Md sir approval for this request.")
		else:
			if(self.grand_total<=2000):
				if(frappe.session.user=="karthi@wtt1401.com" or frappe.session.user == 'gm_admin@wttindia.com' or frappe.session.user == 'sarnita@wttindia.com' or frappe.session.user == 'venkat@wttindia.com' or frappe.session.user == 'priya@wttindia.com'):
					pass
				else:
					frappe.throw("Need Accounts Manager approval for this request.")
			elif(self.grand_total<=4000):
				if(frappe.session.user == 'gm_admin@wttindia.com' or frappe.session.user == 'sarnita@wttindia.com' or frappe.session.user == 'venkat@wttindia.com' or frappe.session.user == 'priya@wttindia.com'):
					pass
				else:
					frappe.throw("Need GM sir approval for this request.")
			elif(self.grand_total>4000):
				if(frappe.session.user == 'sarnita@wttindia.com' or frappe.session.user == 'venkat@wttindia.com' or frappe.session.user == 'priya@wttindia.com'):
					pass
				else:
					frappe.throw("Need Directors approval for this request.")


@frappe.whitelist()
def update_given(ref_name):
	ar=[]
	frappe.db.sql("UPDATE `tabCash Request` SET cash_status='Given' WHERE name='"+str(ref_name)+"'")
	return ar

@frappe.whitelist()
def update_par_given(ref_name):
	ar=[]
	frappe.db.sql("UPDATE `tabCash Request` SET cash_status='Partially Given' WHERE name='"+str(ref_name)+"'")
	return ar