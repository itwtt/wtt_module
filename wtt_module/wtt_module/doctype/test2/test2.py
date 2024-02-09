 # Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date,datetime,timedelta
from frappe.utils import getdate
from frappe.utils.background_jobs import enqueue
import calendar
import re
class test2(Document):
	# def validate(self):
	# 	frappe.msgprint(self.test_field)
	pass
	# def validate(self):
	# 	if(self.validate_gst()==True):
	# 		pass
	# 	else:
	# 		frappe.throw("Invalid Tax ID")
	# def validate_gst(self):
	# 	regex = "^[0-9]{2}[A-Z]{5}[0-9]{4}" +"[A-Z]{1}[1-9A-Z]{1}" +"Z[0-9A-Z]{1}$"
	# 	p = re.compile(regex)
	# 	if (self.tax_id == None):
	# 		return False
	# 	if(re.search(p, self.tax_id)):
	# 		return True
	# 	else:
	# 		return False
	
