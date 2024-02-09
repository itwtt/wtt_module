from __future__ import unicode_literals
import frappe
import json
from frappe.utils import cstr, flt, cint,getdate
from frappe import msgprint, _
from frappe.model.mapper import get_mapped_doc
import json
from datetime import date,datetime,timedelta
import time
import ast
import requests
import calendar
from pytz import timezone
from frappe.utils.background_jobs import enqueue
import subprocess
import pdfplumber
import traceback
import pyotp
import sys
import smtplib
import urllib.parse

@frappe.whitelist() 
def test(nn,rr):
	ar=[]
	for i in frappe.db.sql("SELECT aa.name,bb.item_code,bb.qty from `tabMaterial Request`as aa,`tabMaterial Request Item` as bb WHERE aa.name=bb.parent and aa.workflow_state!='Rejected' and aa.workflow_state!='Cancelled' GROUP BY aa.name ORDER BY bb.project ",as_dict=1):
		ar.append(i)
	# frappe.msgprint(len(ar))
	return nn

#md cancellation reason for material request -- material_request.js
@frappe.whitelist()
def mr_rejection(nn,rr):
	frappe.db.sql("UPDATE `tabMaterial Request` set reason_for_rejection='"+str(rr)+"' WHERE name='"+str(nn)+"' ")

	return nn


#md cancellation for purchase order -- purchase order.js
@frappe.whitelist()
def po_rejection(nn,rr):
	frappe.db.sql("UPDATE `tabPurchase Order` set rejected_reason_md='"+str(rr)+"' WHERE name='"+str(nn)+"' ")

	return nn

# receipt cancellation for purchase receipt -- purchase receipt.js
@frappe.whitelist()
def pr_rejection(nn,rr):
	frappe.db.sql("UPDATE `tabPurchase Receipt` set reason_for_rejection='"+str(rr)+"' WHERE name='"+str(nn)+"' ")

	return nn

#cancellation of leave by md sir --  leave_request.js
@frappe.whitelist()
def leave_rejection(nn,rr):
	frappe.db.sql("UPDATE `tabLeave Request` set md_remarks='"+str(rr)+"' WHERE name='"+str(nn)+"' ")
	return nn

# for work order get items from stock entry -- work_order.js
@frappe.whitelist()
def create_work_order(source_name, target_doc=None):
	doc = get_mapped_doc("Stock Entry", source_name, {
		"Stock Entry": {
			"doctype": "Work Order",
			"validation": {
				"docstatus": ["=", 1]
			},
			"field_map": {
				"Stores - WTT":"source_warehouse",
				"Stores - WTT":"fg_warehouse",
				"SHOP FLOOR - WTT":"wip_warehouse"
			}
		},
		"Stock Entry Detail": {
			"doctype": "Work Order Item",
			"field_map":{
				"qty":"required_qty",
				"parent":"stock_entry"
			}
		}
	}, target_doc)
	return doc


# for check the mail has already registered in registration form for hr interview process web form -- web form at erp -- job-form
@frappe.whitelist(allow_guest=True)
def validate_mail(mail):
	# frappe.msgprint("str(mail)")
	aa="for_callback"
	doc=frappe.db.sql("SELECT * from `tabRegistration Form` WHERE email='"+str(mail)+"' ",as_dict=1)
	if(doc):
		aa="remove"
		frappe.msgprint("Candidate with Email has been already registered")
	# 	return False
	# else:
	# 	return True
	return aa


#track Items in purchase receipt on material request and purchase order -- purchase_receipt.js
@frappe.whitelist()
def track_items(table):
	# for i in frappe.db.sql("SELECT ")
	tab=json.loads(table)
	ar=[]
	for i in tab:
		doc = frappe.db.sql("SELECT qty,uom,material_request,material_request_item,idx FROM `tabPurchase Order Item` WHERE name='"+str(i["purchase_order_item"])+"' ",as_dict=1)
		for j in doc:
			ar.append({
				"description":i["description"],
				"technical_description":i["technical_description"],
				"pr_qty":"PR Qty - "+str(i["qty"])+" "+str(i["uom"])+"\n (AQ-"+str(i["accepted_qty"])+"; RQ-"+str(i["rejected_qty"])+")",
				"po_qty":"PO QTY - "+str(j.qty)+" "+str(j.uom),
				"po_detail":str(i["purchase_order"])+"\n At row no: "+str(j.idx),
				"mr_qty":"MR Qty - "+str(frappe.db.get_value("Material Request Item",j.material_request_item,"qty"))+" "+str(frappe.db.get_value("Material Request Item",j.material_request_item,"uom")),
				"mr_detail":str(j.material_request)+"\n At row no: "+str(frappe.db.get_value("Material Request Item",j.material_request_item,"idx"))
				})
	return ar
 
# allow overbilling in account setting -- purchase_receipt.js
@frappe.whitelist()
def allow_overbilling(user):
	doc=frappe.new_doc("Accounts Settings")
	doc.over_billing_allowance=50
	doc.role_allowed_to_over_bill="Purchase Master Manager"
	doc.save()

	sub_doc=frappe.get_doc("Purchase Receipt",user)
	sub_doc.submit()

	doc=frappe.new_doc("Accounts Settings")
	doc.over_billing_allowance=0
	doc.save()

	return user


# allow overbilling in account setting -- purchase_receipt.js
@frappe.whitelist()
def allow_over_stock(user):
	doc=frappe.new_doc("Stock Settings")
	doc.over_delivery_receipt_allowance=50
	doc.save()

	sub_doc=frappe.get_doc("Purchase Order",user)
	sub_doc.submit()

	doc=frappe.new_doc("Stock Settings")
	doc.over_delivery_receipt_allowance=0
	doc.save()

	return user


# allow overbilling in account setting -- puchase_invoice.js
@frappe.whitelist()
def allow_overbilling_invoice(user):
	doc=frappe.new_doc("Accounts Settings")
	doc.over_billing_allowance=50
	doc.role_allowed_to_over_bill="Purchase Master Manager"
	doc.save()

	sub_doc=frappe.get_doc("Purchase Invoice",user)
	sub_doc.submit()

	doc=frappe.new_doc("Accounts Settings")
	doc.over_billing_allowance=0
	doc.save()

	return user

#Login android
@frappe.whitelist(allow_guest=True)
def login(username, password):
	try:
		login_manager = frappe.auth.LoginManager()
		login_manager.authenticate(user=username, pwd=password)
		login_manager.post_login(newip=10)
	except frappe.exceptions.AuthenticationError:
		frappe.clear_messages ()
		frappe.local.response['http_status_code'] = 400
		return
	cur_user = frappe.session.user
	frappe.set_user("Administrator")
	api_generate = generate_keys (cur_user)
	user = frappe.get_doc('User', cur_user)
	frappe.response ["message"] = {
		"success_key":1,
		"message":"Authentication success",
		"sid": frappe.session.sid,
		"api_key":user.api_key,
		"api_secret": api_generate,
		"username":user.username,
		"email":user.email,
		"full_name":user.full_name
	}
	token="Token "+str(frappe.response["message"]["api_key"])+":"+str(frappe.response["message"]["api_secret"])
	emp=frappe.db.get_value('Employee', {'user_id': frappe.response["message"]["email"]},'employee')
	dis= str({"emp":emp,"token":token})
	return dis

def generate_keys (user):
	user_details = frappe.get_doc('User', user)
	api_secret = frappe.generate_hash(length=15)

	if not user_details.api_key:
		api_key = frappe.generate_hash(length=15)
		user_details.api_key = api_key
	
	user_details.api_secret = api_secret
	user_details.save()
	
	return api_secret

# Leave requets data sharing from android application
@frappe.whitelist()
def create_leave(employee_id,from_date,to_date,leavetype,exp):
	employee_id=employee_id.upper()
	f_date=datetime.strptime(str(from_date),"%Y-%m-%d")
	t_date=datetime.strptime(str(to_date),"%Y-%m-%d")
	fd=f_date.date()
	td=t_date.date()
	nod=(td-fd).days
	month = fd.strftime("%B")
	if(leavetype=="Emergency leave" or leavetype=="Sick leave"):
		doc=frappe.new_doc("Emergency Leave")
		doc.employee=employee_id
		doc.month=month
		doc.append("leave_table",{
			"from_date":fd,
			"to_date":fd,
			"day":"Full day",
			"leave_type":leavetype,
			"no_of_days":1,
			"explanation":exp
		})
		while fd<td:
			fd+=timedelta(days=1)
			doc.append("leave_table",{
				"from_date":fd,
				"to_date":fd,
				"day":"Full day",
				"leave_type":leavetype,
				"no_of_days":1,
				"explanation":exp
				})
		doc.save()
	else:
		doc=frappe.new_doc("Leave Request")
		doc.employee=employee_id
		doc.month=month
		doc.append("leave_table",{
			"from_date":fd,
			"to_date":fd,
			"day":"Full day",
			"leave_type":leavetype,
			"no_of_days":1,
			"explanation":exp
		})
		while fd<td:
			fd+=timedelta(days=1)
			doc.append("leave_table",{
				"from_date":fd,
				"to_date":fd,
				"day":"Full day",
				"leave_type":leavetype,
				"no_of_days":1,
				"explanation":exp
				})
		doc.save()
	return
	
# raising On duty from android application
@frappe.whitelist()
def raise_od(employee_id1,frm_time1,totime,reason):
	employee_id1=employee_id1.upper()
	date1=frm_time1
	date2=totime
	dd=datetime.strptime(date1,"%Y-%m-%d %H:%M")
	from_time=dd.strftime("%Y-%m-%d %H:%M:%S")
	ft=datetime.strptime(from_time,"%Y-%m-%d %H:%M:%S")
	dd1=datetime.strptime(date2,"%Y-%m-%d %H:%M")
	to_time=dd1.strftime("%Y-%m-%d %H:%M:%S")
	tt=datetime.strptime(to_time,"%Y-%m-%d %H:%M:%S")
	diff=tt-ft
	doc=frappe.new_doc("On duty request")
	doc.employee=employee_id1
	doc.from_time=ft
	doc.to_time=tt
	doc.hours=diff.total_seconds()/3600
	doc.explanation=reason
	doc.save()
	return


#Attendance Request
@frappe.whitelist()
def att_request(emp_id,frm_tm,totm,exp):
	employee_id1=emp_id.upper()
	date1=frm_tm
	date2=totm
	dd=datetime.strptime(date1,"%Y-%m-%d %H:%M")
	from_time=dd.strftime("%Y-%m-%d %H:%M:%S")
	ft=datetime.strptime(from_time,"%Y-%m-%d %H:%M:%S")
	dd1=datetime.strptime(date2,"%Y-%m-%d %H:%M")
	to_time=dd1.strftime("%Y-%m-%d %H:%M:%S")
	tt=datetime.strptime(to_time,"%Y-%m-%d %H:%M:%S")
	diff=tt-ft
	doc=frappe.new_doc("Attendance Request")
	doc.employee=employee_id1
	doc.from_date=ft.date()
	doc.to_date=ft.date()
	doc.from_time=ft
	doc.to_time=tt
	doc.hours=diff.total_seconds()/3600
	doc.explanation=exp
	doc.reason="On Duty"
	doc.save()
	return "Success"

# Android Get Leave
@frappe.whitelist()
def create_new_leave(empp,month1,val):
	month=month1
	emp=empp
	array = []
	ll=[]
	dd=date.today()
	cc=datetime.strptime(str(month), "%B")
	mm=cc.month
	d1=dd.replace(day=1,month=mm)
	d0=(d1+timedelta(days=32)).replace(day=1)
	d2=d0-timedelta(days=1)
	doc=frappe.db.sql("SELECT lr.name,lr.employee_name,lt.from_date,lt.leave_type,lt.explanation,lr.workflow_state from `tabLeave Request`as lr,`tabLeave table`as lt WHERE lt.parent=lr.name and lr.employee='"+str(emp)+"' and lt.from_date>='"+str(d1)+"' and lt.to_date<='"+str(d2)+"' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' ",as_dict=1)
	for i in doc:			
		array.append({
			"employee_name":i.employee_name,
			"leave_date":i.from_date,
			"leave_type":i.leave_type,
			"explanation":i.explanation,
			"workflow_state":i.workflow_state
			})
	
	doc1=frappe.db.sql("SELECT lr.name,lr.employee_name,lt.from_date,lt.leave_type,lt.explanation,lr.workflow_state from `tabEmergency Leave`as lr,`tabEmergency Table`as lt WHERE lt.parent=lr.name and lr.employee='"+str(emp)+"' and lt.from_date>='"+str(d1)+"' and lt.to_date<='"+str(d2)+"' and lr.workflow_state!='Rejected' and lr.workflow_state!='Cancelled' ",as_dict=1)
	for k in doc1:			
		array.append({
			"employee_name":k.employee_name,
			"leave_date":k.from_date,
			"leave_type":k.leave_type,
			"explanation":k.explanation,
			"workflow_state":k.workflow_state
			})	

	frappe.response ["data"] = array
	return

# Android On duty
@frappe.whitelist()
def get_onduty(empp2,month2):
	month=month2
	emp=empp2
	array = []
	ll=[]
	dd=date.today()
	cc=datetime.strptime(str(month), "%B")
	mm=cc.month
	d1=dd.replace(day=1,month=mm)
	d0=(d1+timedelta(days=32)).replace(day=1)
	d2=d0-timedelta(days=1)
	doc=frappe.db.sql("SELECT employee_name,from_time,to_time,hours,explanation,workflow_state from `tabOn duty request` WHERE employee='"+str(emp)+"' and from_time>='"+str(d1)+"' and to_time<='"+str(d2)+"' and workflow_state!='Rejected' and workflow_state!='Cancelled' ",as_dict=1)
	for i in doc:			
		array.append({
			"employee_name":i.employee_name,
			"from_time":i.from_time,
			"to_time":i.to_time,
			"hours":round(i.hours,2),
			"explanation":i.explanation,
			"workflow_state":i.workflow_state
			})
	frappe.response ["data"] = array
	return


#Android Attendance Report
@frappe.whitelist()
def att_report(empp3,month3):
	month=month3
	emp=empp3
	array = []
	ll=[]
	dd=date.today()
	cc=datetime.strptime(str(month), "%B")
	mm=cc.month
	d1=dd.replace(day=1,month=mm)
	d0=(d1+timedelta(days=32)).replace(day=1)
	d2=d0-timedelta(days=1)
	doc=frappe.db.sql("SELECT employee_name,from_time,to_time,hours,explanation,workflow_state from `tabAttendance Request` WHERE employee='"+str(emp)+"' and from_time>='"+str(d1)+"' and to_time<='"+str(d2)+"' and workflow_state!='Rejected' and workflow_state!='Cancelled' ",as_dict=1)
	for i in doc:			
		array.append({
			"employee_name":i.employee_name,
			"from_time":i.from_time,
			"to_time":i.to_time,
			"hours":round(i.hours,2),
			"explanation":i.explanation,
			"workflow_state":i.workflow_state
			})
	frappe.response ["data"] = array
	return "Success"


@frappe.whitelist(allow_guest=True)
def get_plc_data(date):
	s = date.replace("\"", "")
	erp_data = []
	query = frappe.db.sql("SELECT * FROM `tabPlant Running Data`as pp,`tabReject RO Data`as cc WHERE pp.name=cc.parent and pp.date='"+str(s)+"' ",as_dict=1)
	if(query):
		# s="done"
		for i in query:
			erp_data.append({
				"col0":i.col0,
				"col1":i.col1,
				"col2":i.col2,
				"col3":i.col3,
				"col4":i.col4,
				"col5":i.col5,
				"col6":i.col6,
				"col7":i.col7,
				"col8":i.col8,
				"col9":i.col9,
				"col10":i.col10,
				"col11":i.col11,
				"col12":i.col12,
				"col13":i.col13,
				"col14":i.col14,
				"col15":i.col15,
				"col16":i.col16,
				"col17":i.col17,
				"col18":i.col18,
				"col19":i.col19,
				"col20":i.col20,
				"col21":i.col21,
				"col22":i.col22,
				"col23":i.col23,
				"col24":i.col24,
				"col25":i.col25,
				"col26":i.col26
				})
	return erp_data

@frappe.whitelist(allow_guest=True)
def update_plc_data(user):	
	child_table_data = []
	local = timezone("Asia/Kolkata")
	_time=datetime.now(local)
	today=_time.date()
	bb=user.replace("\"","")
	cc=bb.replace("\'[","[")
	dd=cc.replace("]\'","]")
	s = dd.replace("\'", "\"")
	vv= json.loads(s)
	gg=frappe.db.sql("SELECT * FROM `tabPlant Running Data` WHERE date='"+str(today)+"'",as_dict=1)
	if(gg):
		for j in gg:
			if(j.date==today):
				for i in (frappe.db.sql("SELECT * FROM `tabReject RO Data` WHERE parent='"+str(j.name)+"' ",as_dict=1)):
					child_table_data.append(i)

				doc=frappe.get_doc("Plant Running Data",j.name)
				doc.main_ro = []
				for i in range(len(vv)):
					if(vv[i] not in child_table_data):
						doc.append("main_ro",vv[i])
				doc.save(ignore_permissions=True)
	else:
		doc=frappe.new_doc("Plant Running Data")
		doc.plant_name="KANCHAN"
		for i in range(len(vv)):
			doc.append("main_ro",vv[i])
		doc.save(ignore_permissions=True)
	return "Updated"



@frappe.whitelist(allow_guest=True)
def set_itma_details(user):	
	bb=user.replace("\"","")
	cc=bb.replace("\'[","[")
	dd=cc.replace("]\'","]")
	s = dd.replace("\'", "\"")
	vv= json.loads(s)
	# for i in range(len(vv)):
	# 	gg=frappe.db.sql("SELECT * FROM `tabITMA Data` WHERE phone_no='"+str(vv[i]['col4'])+"'",as_dict=1)
	# 	if(gg):
	# 		pass
	# 	else:
	# 		doc=frappe.new_doc("ITMA Data")
	# 		doc.phone_no=vv[i]['col4']
	# 		doc.client_name=vv[i]['col0']
	# 		doc.email=vv[i]['col3']
	# 		doc.append("itma_details",vv[i])
	# 		doc.save(ignore_permissions=True)
	return str(vv)


	
@frappe.whitelist(allow_guest=True)
def update_rsl_plc_data(user):
	child_table_data = []
	local = timezone("Asia/Kolkata")
	_time=datetime.now(local)
	today=_time.date()
	bb=user.replace("\"","")
	cc=bb.replace("\'[","[")
	dd=cc.replace("]\'","]")
	s = dd.replace("\'", "\"")
	vv= json.loads(s)
	gg=frappe.db.sql("SELECT * FROM `tabPlant Running Data` WHERE date='"+str(today)+"'",as_dict=1)
	if(gg):
		for j in gg:
			if(j.date==today):
				for i in (frappe.db.sql("SELECT * FROM `tabRSL Table` WHERE parent='"+str(j.name)+"' ",as_dict=1)):
					child_table_data.append(i)

				doc=frappe.get_doc("Plant Running Data",j.name)
				doc.main_ro = []
				for i in range(len(vv)):
					if(vv[i] not in child_table_data):
						doc.append("rsl_table",vv[i])
				doc.save(ignore_permissions=True)
	else:
		doc=frappe.new_doc("Plant Running Data")
		doc.plant_name="RSL"
		for i in range(len(vv)):
			doc.append("rsl_table",vv[i])
		doc.save(ignore_permissions=True)
	return "Updated"

#Enquriy sheet
@frappe.whitelist(allow_guest=True)
def create_enquiry(company_name=None,mobile_no=None,contact_person=None,email_id=None,factory_address=None,
	existing_plant=None,current_required=None,if_others=None,ph=None,pva=None,cod=None,oilgreeze=None,bod=None,
	temp=None,tds=None,hardness=None,tss=None,alka=None,tkn=None,discharge=None,partial_recovery=None,zld=None,brine=None,salt=None,
	textile=None,cotton=None,denim=None,woven=None,dyeing=None,printing=None,knitting=None,desizing=None):
	
	doc=frappe.new_doc("Test Enquiry Sheet")
	doc.company_name=company_name
	doc.save()
	return doc 

#PLC Login
@frappe.whitelist(allow_guest=True)
def plc_login(username, password):
	try:
		login_manager = frappe.auth.LoginManager()
		login_manager.authenticate(user=username, pwd=password)
		login_manager.post_login()
	except frappe.exceptions.AuthenticationError:
		frappe.clear_messages ()
		frappe.local.response['http_status_code'] = 400
		return
	cur_user = frappe.session.user
	frappe.set_user("Administrator")
	api_generate = generate_keys1(cur_user)
	user = frappe.get_doc('User', cur_user)
	frappe.response ["message"] = {
		"success_key":1,
		"message":"Authentication success",
		"sid": frappe.session.sid,
		"api_key":user.api_key,
		"api_secret": api_generate,
		"username":user.username,
		"email":user.email,
		"full_name":user.full_name
	}
	token="Token "+str(frappe.response["message"]["api_key"])+":"+str(frappe.response["message"]["api_secret"])
	emp=frappe.db.get_value('Employee', {'user_id': frappe.response["message"]["email"]},'employee')
	dis= str({"emp":emp,"token":token})
	return dis

def generate_keys1(user):
	user_details = frappe.get_doc('User', user)
	api_secret = frappe.generate_hash(length=15)

	if not user_details.api_key:
		api_key = frappe.generate_hash(length=15)
		user_details.api_key = api_key
	
	user_details.api_secret = api_secret
	user_details.save()
	
	return api_secret

@frappe.whitelist()
def get_plc_report(date,from_time=None,to_time=None):
	pass


@frappe.whitelist(allow_guest=True)
def feedback(organization=None,q1=None,q3=None,q4=None,q9=None,q10=None,s1=None,s2=None,s5=None,s6=None):
	doc="test"
	if(organization==None):
		frappe.msgprint("Please fill Organization Name")
	else:
		doc=frappe.new_doc("Feedback Form")
		doc.organization=organization
		doc.question1=q1
		doc.question3=q3
		doc.question4=q4
		# doc.question7=q7
		doc.question9=q9
		doc.question10=q10
		doc.select1=s1
		doc.select2=s2
		doc.select5=s5
		doc.select6=s6
		doc.save()
	return doc


@frappe.whitelist(allow_guest=True)
def flutter_login(username,password):
	try:
		login_manager = frappe.auth.LoginManager()
		login_manager.authenticate(user=username, pwd=password)
		login_manager.post_login()
	except frappe.exceptions.AuthenticationError:
		frappe.clear_messages ()
		frappe.local.response['http_status_code'] = 400
		return
	cur_user = frappe.session.user
	frappe.set_user("Administrator")
	api_generate = generate_keys1(cur_user)
	user = frappe.get_doc('User', cur_user)
	frappe.response ["message"] = {
		"success_key":1,
		"message":"Authentication success",
		"sid": frappe.session.sid,
		"api_key":user.api_key,
		"api_secret": api_generate,
		"username":user.username,
		"email":user.name,
		"full_name":user.full_name
	}
	token="Token "+str(frappe.response["message"]["api_key"])+":"+str(frappe.response["message"]["api_secret"])
	emp=frappe.db.get_value('Employee', {'user_id': frappe.response["message"]["email"]},'employee')
	if(frappe.db.sql("SELECT * from `tabMobile Users` where user='"+str(user.name)+"' ",as_dict=1)):
		dis= str({"emp":emp,"token":token})
	else:
		dis= str({"emp":"Permission Error","token":"You are restricted to Mobile Application"})
	# tok = str(frappe.response["message"]["api_key"])+":"+str(frappe.response["message"]["api_secret"])
	return dis


@frappe.whitelist(allow_guest=True)
def plant_report_flutter():
	ar = []
	query = frappe.db.sql("SELECT cc.col27 as name,cc.col1 as plant_name from `tabPlant Running Data`as pp,`tabReject RO Data`as cc WHERE pp.name=cc.parent and pp.plant_name='KANCHAN' ",as_dict=1)

	# for i in query:
	# 	ar.append({
	# 		'name':i.name,
	# 		'plant_name':round(i.plant_name,2)
	# 		})

	# frappe.response ["data"] = query
	return query

@frappe.whitelist(allow_guest=True)
def kanchan_data():
	ar=[]
	query = frappe.db.sql("""SELECT AVG(ch.col1)as col1,AVG(ch.col2)as col2,AVG(ch.col3)as col3,AVG(ch.col4)as col4,AVG(ch.col5)as col5,AVG(ch.col6)as col6,AVG(ch.col7)as col7,AVG(ch.col8)as col8,AVG(ch.col9)as col9,AVG(ch.col10)as col10,
		AVG(ch.col11)as col11,AVG(ch.col12)as col12,AVG(ch.col13)as col13,AVG(ch.col14)as col14,AVG(ch.col15)as col15,AVG(ch.col16)as col16,AVG(ch.col17)as col17,AVG(ch.col18)as col18,AVG(ch.col19)as col19,AVG(ch.col20)as col20
	 	FROM `tabPlant Running Data`as pp,`tabRSL Table`as ch 
	 	WHERE  
	 	pp.name=ch.parent and pp.plant_name="RSL" ORDER BY ch.col27 DESC LIMIT 1 """,as_dict=1)
	for i in query:
		ar.append({
			"col1":str(round(float(i.col1),2)),
			"col2":str(round(float(i.col2),2)),
			"col3":str(round(float(i.col3),2)),
			"col4":str(round(float(i.col4),2)),
			"col5":str(round(float(i.col5),2)),
			"col6":str(round(float(i.col6),2)),
			"col7":str(round(float(i.col7),2)),
			"col8":str(round(float(i.col8),2)),
			"col9":str(round(float(i.col9),2)),
			"col10":str(round(float(i.col10),2)),
			"col11":str(round(float(i.col11),2)),
			"col12":str(round(float(i.col12),2)),
			"col13":str(round(float(i.col13),2)),
			"col14":str(round(float(i.col14),2)),
			"col15":str(round(float(i.col15),2)),
			"col16":str(round(float(i.col16),2)),
			"col17":str(round(float(i.col17),2)),
			"col18":str(round(float(i.col18),2)),
			"col19":str(round(float(i.col19),2)),
			"col20":str(round(float(i.col20),2)),
			"main_recovery":str(round((float(i.col2)+float(i.col3)+float(i.col4)+float(i.col5))*100/float(i.col1),2) if float(i.col1)>0.0 else 0),
			"main_dp1":str((float(i.col8)-float(i.col9))),
			"main_dp2":str((float(i.col10)-float(i.col11))),
			"main_dp3":str((float(i.col12)-float(i.col13)))
			})

	return ar


@frappe.whitelist(allow_guest=True)
def filtered_kanchan_data(dropdown,plant_name):
	# server = '122.165.198.254'
	# port = '631'
	# # server = '10.15.5.51'
	# username = 'sa'
	# password = 'Hmi##5454$'
	# database = "KANCHAN" if plant_name=="KANCHAN" else "RSL" if plant_name=="RSL" else "SIDDHI"
	# connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};PORT={port};UID={username};PWD={password};'
	# connection = pyodbc.connect(connection_string)
	# cursor = connection.cursor()
	ar=[]
	column={}
	local = timezone("Asia/Kolkata")
	_time=datetime.now(local)
	dd=_time.date()
	date1 = date2 = _time.date()
	if(dropdown=="Yesterday"):
		date1 = dd-timedelta(days=1)
		date2 = dd-timedelta(days=1)
	elif(dropdown=="Last Week"):
		date1=dd-timedelta(days=dd.weekday())
		date2=date1+timedelta(days=5)
	elif(dropdown=="Last Month"):
		mm = dd.month-1
		date1=dd.replace(day=1,month=mm)
		date2=((date1+timedelta(days=32)).replace(day=1))-timedelta(days=1)
	if(plant_name=="KANCHAN" and dropdown=="Last Week"):
		ar = [{"col1": "61.13", "col2": "33.94", "col3": "14.36", "col4": "5.27", "col5": "1.97", "col6": "6.78", "col7": "7.08", "col8": "12.26", "col9": "9.9", "col10": "27.5", "col11": "26.45", "col12": "43.42", "col13": "42.99", "col14": "57.97", "col15": "57.22", "main_dp1": "2.36", "main_dp2": "1.05", "main_dp3": "0.45", "main_dp4": "0.75", "main_recovery": "91.12", "col18": "48.54", "col19": "7.31", "col20": "5.76", "col21": "7.14", "col22": "46.47", "col23": "45.89", "col24": "64.65", "col25": "64.34", "reject_dp1": "0.59", "reject_dp2": "0.31", "reject_recovery": "26.92", "col16": "2", "col17": "2", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="SIDDHI" and dropdown=="Last Week"):
		ar = [{"homo_lt": "2.04", "bio_lift": "1.03", "srs_fm": "51.2", "cooling_fm": "9.7", "an_feed": "5.57", "an_nt": "6.15", "bio_nt": "6.62", "cts_flu": "0.0", "do_out": "5.47", "blw_line": "0.6", "cooling_line": "0.04", "mf_tank_lt": "2.95", "mf_backwash": "8.08", "mf_per": "61.45", "mf_rej": "28.55", "mf_cip": "0.02", "nt_ph": "12.38", "rack1": "150.17", "rack2": "149.71", "dgt_ph": "8.45", "ro_hpp_vfd": "43.29", "ro_bp1_vfd": "42.02", "ro_bp2_vfd": "41.71", "ro_bp3_vfd": "0.0", "ro_bp4_vfd": "40.63", "cat_filt_out": "0.72", "ro_stg1_in": "10.29", "ro_stg1_out": "9.6", "ro_stg2_in": "16.88", "ro_stg2_out": "15.98", "ro_stg3_in": "23.79", "ro_stg3_out": "23.35", "ro_stg4_in": "33.04", "ro_stg4_out": "32.53", "ro_stg5_in": "38.03", "ro_stg5_out": "35.62", "raw_ro_cat": "0.26", "raw_ro_stg1_in": "0.2", "raw_ro_stg1_out": "0.23", "raw_ro_stg2_in": "0.28", "ro_feed": "3.24", "ro_per_tank": "4.6", "ro_rej_tank": "2.06", "m_ro_feed": "75.26", "m_ro_1st": "33.33", "m_ro_2nd": "21.52", "m_ro_3rd": "10.27", "m_ro_4th": "3.72", "m_ro_5th": "0.32", "m_ro_cip_i_ii": "0.06", "m_ro_cip_iii_iv": "0.06", "m_ro_rej": "4.25", "m_ro_rec": "0.0", "raw_ro_f": "0.03", "raw_ro_1": "0.03", "raw_ro_2": "0.03", "raw_ro_r": "0.0", "m_ro_ph": "7.25", "raw_ro_ph": "7.9", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="RSL" and dropdown=="Last Week"):
		ar = [{"col1": "18.71", "col2": "10.08", "col3": "3.68", "col4": "3.16", "col5": "0", "col6": "5.78", "col7": "0", "col8": "0", "col9": "0", "col10": "15.97", "col11": "0", "col12": "21.96", "col13": "0", "col14": "32.53", "col15": "0", "col16": "0", "col17": "0", "col18": "0", "col19": "3.74", "col20": "8.21", "main_recovery": "90.36", "main_dp1": "0.67", "main_dp2": "0.61", "main_dp3": "0.08", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="KANCHAN" and dropdown=="Last Month"):
		ar = [{"col1": "60.27", "col2": "33.55", "col3": "14.78", "col4": "5.29", "col5": "2.02", "col6": "6.82", "col7": "5.1", "col8": "11.44", "col9": "9.98", "col10": "26.77", "col11": "25.46", "col12": "42.81", "col13": "42.3", "col14": "58.37", "col15": "57.6", "main_dp1": "1.47", "main_dp2": "1.31", "main_dp3": "0.51", "main_dp4": "0.77", "main_recovery": "92.4", "col18": "49.34", "col19": "8.25", "col20": "5.18", "col21": "6.54", "col22": "45.62", "col23": "41.97", "col24": "64.11", "col25": "63.81", "reject_dp1": "3.66", "reject_dp2": "0.3", "reject_recovery": "27.16", "col16": "2", "col17": "2", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="SIDDHI" and dropdown=="Last Month"):
		ar = [{"homo_lt": "3.37", "bio_lift": "1.04", "srs_fm": "58.11", "cooling_fm": "32.93", "an_feed": "6.26", "an_nt": "6.51", "bio_nt": "6.45", "cts_flu": "14.0", "do_out": "3.42", "blw_line": "0.6", "cooling_line": "0.16", "mf_tank_lt": "3.47", "mf_backwash": "10.15", "mf_per": "65.14", "mf_rej": "29.36", "mf_cip": "0.23", "nt_ph": "10.3", "rack1": "118.14", "rack2": "115.56", "dgt_ph": "6.05", "ro_hpp_vfd": "43.55", "ro_bp1_vfd": "42.91", "ro_bp2_vfd": "42.86", "ro_bp3_vfd": "23.66", "ro_bp4_vfd": "42.22", "cat_filt_out": "1.33", "ro_stg1_in": "10.97", "ro_stg1_out": "10.32", "ro_stg2_in": "17.98", "ro_stg2_out": "17.19", "ro_stg3_in": "25.2", "ro_stg3_out": "24.71", "ro_stg4_in": "34.7", "ro_stg4_out": "34.07", "ro_stg5_in": "39.59", "ro_stg5_out": "38.4", "raw_ro_cat": "0.48", "raw_ro_stg1_in": "1.65", "raw_ro_stg1_out": "1.64", "raw_ro_stg2_in": "1.82", "ro_feed": "3.6", "ro_per_tank": "4.77", "ro_rej_tank": "4.48", "m_ro_feed": "73.99", "m_ro_1st": "33.7", "m_ro_2nd": "20.07", "m_ro_3rd": "8.71", "m_ro_4th": "3.63", "m_ro_5th": "0.26", "m_ro_cip_i_ii": "0.03", "m_ro_cip_iii_iv": "0.37", "m_ro_rej": "4.01", "m_ro_rec": "1.92", "raw_ro_f": "2.61", "raw_ro_1": "1.9", "raw_ro_2": "0.44", "raw_ro_r": "0.31", "m_ro_ph": "6.41", "raw_ro_ph": "7.82", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="RSL" and dropdown=="Last Month") :
		ar = [{"col1": "20.31", "col2": "10.77", "col3": "4.0", "col4": "3.76", "col5": "0", "col6": "6.21", "col7": "0", "col8": "0", "col9": "0", "col10": "15.07", "col11": "0", "col12": "20.05", "col13": "0", "col14": "29.55", "col15": "0", "col16": "0", "col17": "0", "col18": "0", "col19": "3.73", "col20": "3.61", "main_recovery": "113.0", "main_dp1": "0.85", "main_dp2": "0.75", "main_dp3": "0.1", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="KANCHAN" and dropdown=="Yesterday"):
		ar = [{"col1": "0", "col2": "0", "col3": "0", "col4": "0", "col5": "0", "col6": "0", "col7": "0", "col8": "0", "col9": "0", "col10": "0", "col11": "0", "col12": "0", "col13": "0", "col14": "0", "col15": "0", "main_dp1": "0", "main_dp2": "0", "main_dp3": "0", "main_dp4": "0", "main_recovery": "0", "col18": "0", "col19": "0", "col20": "0", "col21": "0", "col22": "0", "col23": "0", "col24": "0", "col25": "0", "reject_dp1": "0", "reject_dp2": "0", "reject_recovery": "0", "col16": "2", "col17": "2", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="SIDDHI" and dropdown=="Yesterday"):
		ar = [{"homo_lt": "0", "bio_lift": "0", "srs_fm": "0", "cooling_fm": "0", "an_feed": "0", "an_nt": "0", "bio_nt": "0", "cts_flu": "0", "do_out": "0", "blw_line": "0", "cooling_line": "0", "mf_tank_lt": "0", "mf_backwash": "0", "mf_per": "0", "mf_rej": "0", "mf_cip": "0", "nt_ph": "0", "rack1": "0", "rack2": "0", "dgt_ph": "0", "ro_hpp_vfd": "0", "ro_bp1_vfd": "0", "ro_bp2_vfd": "0", "ro_bp3_vfd": "0", "ro_bp4_vfd": "0", "cat_filt_out": "0", "ro_stg1_in": "0", "ro_stg1_out": "0", "ro_stg2_in": "0", "ro_stg2_out": "0", "ro_stg3_in": "0", "ro_stg3_out": "0", "ro_stg4_in": "0", "ro_stg4_out": "0", "ro_stg5_in": "0", "ro_stg5_out": "0", "raw_ro_cat": "0", "raw_ro_stg1_in": "0", "raw_ro_stg1_out": "0", "raw_ro_stg2_in": "0", "ro_feed": "0", "ro_per_tank": "0", "ro_rej_tank": "0", "m_ro_feed": "0", "m_ro_1st": "0", "m_ro_2nd": "0", "m_ro_3rd": "0", "m_ro_4th": "0", "m_ro_5th": "0", "m_ro_cip_i_ii": "0", "m_ro_cip_iii_iv": "0", "m_ro_rej": "0", "m_ro_rec": "0", "raw_ro_f": "0", "raw_ro_1": "0", "raw_ro_2": "0", "raw_ro_r": "0", "m_ro_ph": "0", "raw_ro_ph": "0", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="RSL" and dropdown=="Yesterday"):
		ar = [{"col1": "0", "col2": "0", "col3": "0", "col4": "0", "col5": "0", "col6": "0", "col7": "0", "col8": "0", "col9": "0", "col10": "0", "col11": "0", "col12": "0", "col13": "0", "col14": "0", "col15": "0", "col16": "0", "col17": "0", "col18": "0", "col19": "0", "col20": "0", "main_recovery": "0", "main_dp1": "0", "main_dp2": "0", "main_dp3": "0", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="KANCHAN" and dropdown=="Today"):
		ar = [{"col1": "0", "col2": "0", "col3": "0", "col4": "0", "col5": "0", "col6": "0", "col7": "0", "col8": "0", "col9": "0", "col10": "0", "col11": "0", "col12": "0", "col13": "0", "col14": "0", "col15": "0", "main_dp1": "0", "main_dp2": "0", "main_dp3": "0", "main_dp4": "0", "main_recovery": "0", "col18": "0", "col19": "0", "col20": "0", "col21": "0", "col22": "0", "col23": "0", "col24": "0", "col25": "0", "reject_dp1": "0", "reject_dp2": "0", "reject_recovery": "0", "col16": "2", "col17": "2", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="SIDDHI" and dropdown=="Today"):
		ar = [{"homo_lt": "0", "bio_lift": "0", "srs_fm": "0", "cooling_fm": "0", "an_feed": "0", "an_nt": "0", "bio_nt": "0", "cts_flu": "0", "do_out": "0", "blw_line": "0", "cooling_line": "0", "mf_tank_lt": "0", "mf_backwash": "0", "mf_per": "0", "mf_rej": "0", "mf_cip": "0", "nt_ph": "0", "rack1": "0", "rack2": "0", "dgt_ph": "0", "ro_hpp_vfd": "0", "ro_bp1_vfd": "0", "ro_bp2_vfd": "0", "ro_bp3_vfd": "0", "ro_bp4_vfd": "0", "cat_filt_out": "0", "ro_stg1_in": "0", "ro_stg1_out": "0", "ro_stg2_in": "0", "ro_stg2_out": "0", "ro_stg3_in": "0", "ro_stg3_out": "0", "ro_stg4_in": "0", "ro_stg4_out": "0", "ro_stg5_in": "0", "ro_stg5_out": "0", "raw_ro_cat": "0", "raw_ro_stg1_in": "0", "raw_ro_stg1_out": "0", "raw_ro_stg2_in": "0", "ro_feed": "0", "ro_per_tank": "0", "ro_rej_tank": "0", "m_ro_feed": "0", "m_ro_1st": "0", "m_ro_2nd": "0", "m_ro_3rd": "0", "m_ro_4th": "0", "m_ro_5th": "0", "m_ro_cip_i_ii": "0", "m_ro_cip_iii_iv": "0", "m_ro_rej": "0", "m_ro_rec": "0", "raw_ro_f": "0", "raw_ro_1": "0", "raw_ro_2": "0", "raw_ro_r": "0", "m_ro_ph": "0", "raw_ro_ph": "0", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]
	elif(plant_name=="RSL" and dropdown=="Today"):
		ar = [{"col1": "0", "col2": "0", "col3": "0", "col4": "0", "col5": "0", "col6": "0", "col7": "0", "col8": "0", "col9": "0", "col10": "0", "col11": "0", "col12": "0", "col13": "0", "col14": "0", "col15": "0", "col16": "0", "col17": "0", "col18": "0", "col19": "0", "col20": "0", "main_recovery": "0", "main_dp1": "0", "main_dp2": "0", "main_dp3": "0", "date1":str(date1.strftime("%d-%m-%y")) ,"date2":str(date2.strftime("%d-%m-%y"))}]

	# if(plant_name=="KANCHAN"):
	# 	cursor.execute("SELECT AVG(ro_reco),AVG(ro_1st_stg_dp),AVG(ro_1st_stg_fm),AVG(ro_1st_stg_in),AVG(ro_1st_stg_out),AVG(ro_2nd_stg_dp),AVG(ro_2nd_stg_fm),AVG(ro_2nd_stg_in),AVG(ro_2nd_stg_out),AVG(ro_3rd_stg_dp),AVG(ro_3rd_stg_fm),AVG(ro_3rd_stg_in),AVG(ro_3rd_stg_out),AVG(ro_4th_stg_dp),AVG(ro_4th_stg_fm),AVG(ro_4th_stg_in),AVG(ro_4th_stg_out),AVG(ro_feed),AVG(ro_feed_lt),AVG(ro_feed_ph),AVG(ro_1st_reco),AVG(ro_2nd_reco),AVG(ro_3rd_reco),AVG(ro_4th_reco) FROM kanchan_main WHERE date_time>'"+str(date1)+"' and date_time<'"+str(date2)+"' ")
	# 	rows_main = cursor.fetchall()
	# 	for row in rows_main:
	# 		column["col1"]=str(round(row[17],2))#ro_feed
	# 		column["col2"]=str(round(row[2],2))#ro_1st_stg_fm
	# 		column["col3"]=str(round(row[6],2))#ro_2nd_stg_fm
	# 		column["col4"]=str(round(row[10],2))#ro_3rd_stg_fm
	# 		column["col5"]=str(round(row[14],2))#ro_4th_stg_fm
	# 		column["col6"]=str(round(row[19],2))#ro_feed_ph
	# 		column["col7"]=str(round(row[18],2))#ro_feed_lt
	# 		column["col8"]=str(round(row[3],2))#ro_1st_stg_in
	# 		column["col9"]=str(round(row[4],2))#ro_1st_stg_out
	# 		column["col10"]=str(round(row[7],2))#ro_2nd_stg_in
	# 		column["col11"]=str(round(row[8],2))#ro_2nd_stg_out
	# 		column["col12"]=str(round(row[11],2))#ro_3rd_stg_in
	# 		column["col13"]=str(round(row[12],2))#ro_3rd_stg_out
	# 		column["col14"]=str(round(row[15],2))#ro_4th_stg_in
	# 		column["col15"]=str(round(row[16],2))#ro_4th_stg_out
	# 		column["main_dp1"]=str(round(row[1],2))#ro_1st_stg_dp
	# 		column["main_dp2"]=str(round(row[5],2))#ro_2nd_stg_dp
	# 		column["main_dp3"]=str(round(row[9],2))#ro_3rd_stg_dp
	# 		column["main_dp4"]=str(round(row[13],2))#ro_4th_stg_dp
	# 		column["main_recovery"]=str(round(row[0],2))#ro_reco
	# 		# column["ro_1st_reco"]=str(round(row[20],2))#ro_1st_reco
	# 		# column["ro_2nd_reco"]=str(round(row[21],2))#ro_2nd_reco
	# 		# column["ro_3rd_reco"]=str(round(row[22],2))#ro_3rd_reco
	# 		# column["ro_4th_reco"]=str(round(row[23],2))#ro_4th_reco

	# 	cursor.execute("SELECT AVG(rej_recovery),AVG(rej_feed),AVG(rej_1st_db),AVG(rej_1st_stg_fm),AVG(rej_1st_stg_in),AVG(rej_1st_stg_out),AVG(rej_2nd_stg_fm),AVG(rej_2nd_stg_in),AVG(rej_2nd_stg_out),AVG(rej_feed_lt),AVG(rej_ph_out),AVG(rej_1st_reco),AVG(rej_2nd_reco),AVG(rej_2nd_db) FROM kanchan_rej WHERE date_time>'"+str(date1)+"' and date_time<'"+str(date2)+"' ")
	# 	rows_rej = cursor.fetchall()
	# 	for row in rows_rej:
	# 		column["col18"]=str(round(row[0],2))#rej_recovery
	# 		column["col19"]=str(round(row[3],2))#rej_1st_stg_fm
	# 		column["col20"]=str(round(row[6],2))#rej_2nd_stg_fm
	# 		column["col21"]=str(round(row[9],2))#rej_feed_lt
	# 		column["col22"]=str(round(row[4],2))#rej_1st_stg_im
	# 		column["col23"]=str(round(row[5],2))#rej_1st_stg_out
	# 		column["col24"]=str(round(row[7],2))#rej_2nd_stg_in
	# 		column["col25"]=str(round(row[8],2))#rej_2nd_stg_out
	# 		column["reject_dp1"]=str(round(row[2],2))#rej_1st_db
	# 		column["reject_dp2"]=str(round(row[13],2))#rej_2nd_db
	# 		column["reject_recovery"]=str(round(row[1],2))#rej_feed
	# 		column["col16"]="1"
	# 		column["col17"]="1"
	# 		# column["rej_ph_out"]=str(round(row[10],2))#rej_ph_out
	# 		# column["rej_1st_reco"]=str(round(row[11],2))#rej_1st_reco
	# 		# column["rej_2nd_reco"]=str(round(row[12],2))#rej_2nd_reco

	# elif(plant_name=="SIDDHI"):
	# 	cursor.execute("SELECT AVG(homo_lt),AVG(bio_lift),AVG(srs_fm),AVG(cooling_fm),AVG(an_feed),AVG(an_nt),AVG(bio_nt),AVG(cts_flu),AVG(do_out),AVG(blw_line),AVG(cooling_line) FROM bio WHERE date_time>'"+str(date1)+"' and date_time<'"+str(date2)+"' ")
	# 	rows = cursor.fetchall()
	# 	for row in rows:
	# 		column["homo_lt"]=str(round(row[0],2))#Homo Tank Level
	# 		column["bio_lift"]=str(round(row[1],2))#Bio Lifting
	# 		column["srs_fm"]=str(round(row[2],2))#SRM Feed
	# 		column["cooling_fm"]=str(round(row[3],2))#Cooling tower feed
	# 		column["an_feed"]=str(round(row[4],2))#Anaerobic Feed
	# 		column["an_nt"]=str(round(row[5],2))#Anaerobic NT
	# 		column["bio_nt"]=str(round(row[6],2))#Bio Nt
	# 		column["cts_flu"]=str(round(row[7],2))#
	# 		column["do_out"]=str(round(row[8],2))#DO Sensor pH
	# 		column["blw_line"]=str(round(row[9],2))#
	# 		column["cooling_line"]=str(round(row[10],2))

	# 	cursor.execute("SELECT AVG(mf_tank_lt),AVG(mf_backwash),AVG(mf_per),AVG(mf_rej),AVG(mf_cip),AVG(nt_ph),AVG(rack1),AVG(rack2),AVG(dgt_ph) FROM mf WHERE date_time>'"+str(date1)+"' and date_time<'"+str(date2)+"' ")
	# 	rows = cursor.fetchall()
	# 	for row in rows:
	# 		column["mf_tank_lt"]=str(round(row[0],2))
	# 		column["mf_backwash"]=str(round(row[1],2))
	# 		column["mf_per"]=str(round(row[2],2))
	# 		column["mf_rej"]=str(round(row[3],2))
	# 		column["mf_cip"]=str(round(row[4],2))
	# 		column["nt_ph"]=str(round(row[5],2))
	# 		column["rack1"]=str(round(row[6],2))
	# 		column["rack2"]=str(round(row[7],2))
	# 		column["dgt_ph"]=str(round(row[8],2))

	# 	cursor.execute("SELECT AVG(ro_hpp_vfd),AVG(ro_bp1_vfd),AVG(ro_bp2_vfd),AVG(ro_bp3_vfd),AVG(ro_bp4_vfd),AVG(cat_filt_out),AVG(ro_stg1_in),AVG(ro_stg1_out),AVG(ro_stg2_in),AVG(ro_stg2_out),AVG(ro_stg3_in),AVG(ro_stg3_out),AVG(ro_stg4_in),AVG(ro_stg4_out),AVG(ro_stg5_in),AVG(ro_stg5_out),AVG(raw_ro_cat),AVG(raw_ro_stg1_in),AVG(raw_ro_stg1_out),AVG(raw_ro_stg2_in),AVG(ro_feed),AVG(ro_per_tank),AVG(ro_rej_tank),AVG(m_ro_feed),AVG(m_ro_1st),AVG(m_ro_2nd),AVG(m_ro_3rd),AVG(m_ro_4th),AVG(m_ro_5th),AVG(m_ro_cip_i_ii),AVG(m_ro_cip_iii_iv),AVG(m_ro_rej),AVG(m_ro_rec),AVG(raw_ro_f),AVG(raw_ro_1),AVG(raw_ro_2),AVG(raw_ro_r),AVG(m_ro_ph),AVG(raw_ro_ph) FROM ro WHERE date_time>'"+str(date1)+"' and date_time<'"+str(date2)+"' ")
	# 	rows = cursor.fetchall()
	# 	for row in rows:
	# 		column["ro_hpp_vfd"]=str(round(row[0],2))
	# 		column["ro_bp1_vfd"]=str(round(row[1],2))
	# 		column["ro_bp2_vfd"]=str(round(row[2],2))
	# 		column["ro_bp3_vfd"]=str(round(row[3],2))
	# 		column["ro_bp4_vfd"]=str(round(row[4],2))
	# 		column["cat_filt_out"]=str(round(row[5],2))
	# 		column["ro_stg1_in"]=str(round(row[6],2))
	# 		column["ro_stg1_out"]=str(round(row[7],2))
	# 		column["ro_stg2_in"]=str(round(row[8],2))
	# 		column["ro_stg2_out"]=str(round(row[9],2))
	# 		column["ro_stg3_in"]=str(round(row[10],2))
	# 		column["ro_stg3_out"]=str(round(row[11],2))
	# 		column["ro_stg4_in"]=str(round(row[12],2))
	# 		column["ro_stg4_out"]=str(round(row[13],2))
	# 		column["ro_stg5_in"]=str(round(row[14],2))
	# 		column["ro_stg5_out"]=str(round(row[15],2))
	# 		column["raw_ro_cat"]=str(round(row[16],2))
	# 		column["raw_ro_stg1_in"]=str(round(row[17],2))
	# 		column["raw_ro_stg1_out"]=str(round(row[18],2))
	# 		column["raw_ro_stg2_in"]=str(round(row[19],2))
	# 		column["ro_feed"]=str(round(row[20],2))
	# 		column["ro_per_tank"]=str(round(row[21],2))
	# 		column["ro_rej_tank"]=str(round(row[22],2))
	# 		column["m_ro_feed"]=str(round(row[23],2))
	# 		column["m_ro_1st"]=str(round(row[24],2))
	# 		column["m_ro_2nd"]=str(round(row[25],2))
	# 		column["m_ro_3rd"]=str(round(row[26],2))
	# 		column["m_ro_4th"]=str(round(row[27],2))
	# 		column["m_ro_5th"]=str(round(row[28],2))
	# 		column["m_ro_cip_i_ii"]=str(round(row[29],2))
	# 		column["m_ro_cip_iii_iv"]=str(round(row[30],2))
	# 		column["m_ro_rej"]=str(round(row[31],2))
	# 		column["m_ro_rec"]=str(round(row[32],2))
	# 		column["raw_ro_f"]=str(round(row[33],2))
	# 		column["raw_ro_1"]=str(round(row[34],2))
	# 		column["raw_ro_2"]=str(round(row[35],2))
	# 		column["raw_ro_r"]=str(round(row[36],2))
	# 		column["m_ro_ph"]=str(round(row[37],2))
	# 		column["raw_ro_ph"]=str(round(row[38],2))

	# elif(plant_name=="RSL"):
	# 	cursor.execute("SELECT AVG(ro_3rd_stg_in),AVG(mbr_lt),AVG(cooling_fm),AVG(cooling_ph),AVG(mbr_per_fm),AVG(ro_1st_stg_fm),AVG(ro_2nd_stg_fm),AVG(ro_3rd_stg_fm),AVG(ro_feed),AVG(ro_feed_ph),AVG(ro_feed_tank),AVG(ro_reject_fm),AVG(ro_1st_stg_dp),AVG(ro_1st_stg_reco),AVG(ro_2nd_stg_dp),AVG(ro_2nd_stg_reco),AVG(ro_3rd_stg_dp),AVG(ro_3rd_stg_reco),AVG(ro_1st_stg_in),AVG(ro_2nd_stg_in),AVG(ro_reco) FROM rsl_db WHERE date_time>'"+str(date1)+"' and date_time<'"+str(date2)+"' ")
	# 	rows = cursor.fetchall()
	# 	for row in rows:
	# 		column["col1"]=str(round(row[8],2)) #ro_feed
	# 		column["col2"]=str(round(row[5],2)) #ro_1st_stg_fm
	# 		column["col3"]=str(round(row[6],2)) #ro_2nd_stg_fm
	# 		column["col4"]=str(round(row[7],2)) #ro_3rd_stg_fm
	# 		column["col5"]=str(0)
	# 		column["col6"]=str(round(row[9],2)) #ro_feed_ph
	# 		column["col7"]=str(0)
	# 		column["col8"]=str(0)
	# 		column["col9"]=str(0)
	# 		column["col10"]=str(round(row[18],2)) #ro_1st_stg_in
	# 		column["col11"]=str(0)
	# 		column["col12"]=str(round(row[19],2)) #ro_2nd_stg_in
	# 		column["col13"]=str(0)
	# 		column["col14"]=str(round(row[0],2)) #ro_3rd_stg_in
	# 		column["col15"]=str(0)
	# 		column["col16"]=str(0)
	# 		column["col17"]=str(0)
	# 		column["col18"]=str(0)
	# 		column["col19"]=str(round(row[1],2)) #mbr_lt
	# 		column["col20"]=str(round(row[4],2)) #mbr_per_fm
	# 		column["main_recovery"]=str(round(row[20],2)) #ro_reco
	# 		column["main_dp1"]=str(round(row[12],2)) #ro_1st_stg_dp
	# 		column["main_dp2"]=str(round(row[14],2)) #ro_2nd_stg_dp
	# 		column["main_dp3"]=str(round(row[16],2)) #ro_3rd_stg_dp

	# 		# column["ro_1st_stg_reco"]=str(round(row[13],2)) #ro_1st_stg_reco
	# 		# column["ro_2nd_stg_reco"]=str(round(row[15],2)) #ro_2nd_stg_reco
	# 		# column["ro_3rd_stg_reco"]=str(round(row[17],2)) #ro_3rd_stg_reco
	# 		# column["cooling_fm"]=str(round(row[2],2)) #cooling_fm
	# 		# column["cooling_ph"]=str(round(row[3],2)) #cooling_ph
	# 		# column["ro_feed_tank"]=str(round(row[10],2)) #ro_feed_tank
	# 		# column[" "]=str(round(row[11],2)) #ro_reject_fm
	# column["date1"]=date1
	# column["date2"]=date2
	# ar.append(column)
	return ar

@frappe.whitelist(allow_guest=True)
def get_plant_access_data(full_name):
	user = frappe.db.get_value("User",{"full_name":full_name},"name")
	ar=[]
	for i in frappe.db.sql("SELECT distinct(plant_name) from `tabPlant Data Access` WHERE user='"+str(user)+"' ",as_dict=1):
		ar.append(i.plant_name)
	if(full_name=="Administrator" or full_name=="MANAGING DIRECTOR"):
		for i in frappe.db.sql("SELECT distinct(name) from `tabPlant` ",as_dict=1):
			ar.append(i.name)

	return ar



@frappe.whitelist(allow_guest=True)
def inquires_mail_stopped(): #this function has removed from hooks because of unwanted mail
	pass
	# frappe.msgprint(str(today))
	# ar=[]
	# today = date.today()
	# d1 = datetime.strptime(str(today), '%Y-%m-%d')
	# f_date=d1.replace(hour=0,minute=0,second=0,microsecond=0)
	# t_date=d1.replace(hour=23,minute=0,second=0,microsecond=0)
	# val=frappe.db.sql("SELECT name,lead_name,category,contact_by FROM `tabInquiries` WHERE contact_date>='"+str(f_date)+"' and contact_date<='"+str(t_date)+"'",as_dict=1)
	# for i in val:
	# 	ar.append(str(i.lead_name)+" - "+str(i.category)+" ("+str(i.name)+")")

	# st = today.strftime("%d-%m-%Y")
	# message="Today Follow-ups: "+str(st)+"<br><br>"
	# for j in ar:
	# 	message+=j+"<br>"
	
	# email_args = {
	# 	"reply_to":"trading@wttindia.com",
	# 	"recipients": "trading@wttindia.com",
	# 	"cc":"purchase@wttindia.com",
	# 	"message":message,
	# 	"subject": "Inquiries"
	# 	}
	# if not frappe.flags.in_test:
	# 	enqueue(method=frappe.sendmail, queue='short', timeout=300, is_async=True, **email_args)
	# else:
	# 	frappe.sendmail(**email_args)



######  WTTINT CODING EMPLOYEE APPLICATION CODE
@frappe.whitelist()
def create_feedback(emp,state,feedback):
	doc=frappe.new_doc("Employee Feedback")
	doc.date=date.today()
	doc.employee=emp
	doc.feedback=state
	doc.description=feedback
	doc.save()
@frappe.whitelist()
def create_say_it_do_it(emp,text,say_type,comp_time=None):
	err="Done"
	try:
		local = timezone("Asia/Kolkata")
		_time=datetime.now(local)
		today=_time.date()
		doc=frappe.new_doc("Say It Do It")
		doc.date = today
		doc.employee=emp
		doc.type=say_type
		doc.completion_time = comp_time
		doc.say_it_do_it=text
		doc.status="Pending"
		doc.save()
	except Exception as e:
		err = str(e)
	return err
@frappe.whitelist()
def complete_say_it_do_it(emp):
	local = timezone("Asia/Kolkata")
	_time=datetime.now(local)
	today=_time.date()
	ar=[]
	query = frappe.db.sql("SELECT name,say_it_do_it from `tabSay It Do It` where status='Pending' and date='"+str(today)+"' and employee='"+str(emp)+"' ",as_dict=1)
	if query:
		for i in query:
			ar.append(i)
	return ar
@frappe.whitelist()
def complete_say_it_do_it_entry(name):
	err="Done"
	try:
		doc=frappe.get_doc("Say It Do It",str(name))
		doc.status="Completed"
		doc.save()
	except Exception as e:
		err=str(e)
	return err

@frappe.whitelist()
def get_notification(emp):
	
	local = timezone("Asia/Kolkata")
	_time=datetime.now(local)
	today=_time.date()
	dd_time1 = str(date.today())+" 00:00:00"
	dd_time2 = str(date.today())+" 23:59:00"

	time1 = datetime.strptime(dd_time1,"%Y-%m-%d %H:%M:%S")
	time2 = datetime.strptime(dd_time2,"%Y-%m-%d %H:%M:%S")
	ar=[]
	query=frappe.db.sql("""SELECT cc.type_of_work,cc.status,cc.to_time,cc.name
		FROM `tabTask Allocation` as aa,`tabWork Update` as cc WHERE aa.name=cc.parent
		and aa.docstatus!=2 and aa.workflow_state!='Rejected'
		and aa.employee='"""+str(emp)+"""' and cc.status!='Completed'
		and cc.to_time>='"""+str(time1)+"""' and cc.to_time<='"""+str(time2)+"""' 
		""",as_dict=1)
	for i in query:
		time_=i.to_time
		# time__=datetime.strptime(time_,"%H:%M")
		time__=time_.strftime("%H:%M")
		ar.append({
			"name":i.name,
			"Task":i.type_of_work,
			"Status":i.status,
			"Expected":time__
			})

	return ar

@frappe.whitelist()
def complete_task(token,name):
	parent=frappe.db.sql("SELECT parent from `tabWork Update` where name='"+str(name)+"' ",as_dict=1)
	task=frappe.get_doc("Task Allocation",str(parent[0].parent))
	for i in task.works_table:
		task.status="Completed"
	task.save()
	return task_list

@frappe.whitelist(allow_guest=True)
def get_attendance_data(month,token):
	aaa=token.replace("\"","")
	bb=aaa.split(",")
	cc=str(bb[0])
	dd=cc.split(":")
	emp=dd[1]

	month_array=['','January','February','March','April','May','June','July','August','September','October','November','December']
	mm=month_array.index(month)
	date1=date.today().replace(month=mm,day=1)
	date_cal=(date1+timedelta(days=32)).replace(day=1)
	date2=date_cal-timedelta(days=1)

	total_data=[]
	query=frappe.db.sql("""SELECT count(distinct(name))as count,status FROM `tabAttendance`
		WHERE employee="""+str(emp)+""" and docstatus='1'
		and attendance_date>='"""+str(date1)+"""' and attendance_date<='"""+str(date2)+"""' and DAYNAME(attendance_date)!='SUNDAY'
		GROUP BY status ORDER BY status desc
		""",as_dict=1)
	for i in query:
		if(calendar.day_name[getdate(i.attendance_date).weekday()]!="Sunday"):
			total_data.append({
				"status":i.status,
				"count":str(i.count)
				})
	return total_data


@frappe.whitelist(allow_guest=True)
def get_attendance_data_individual(month,token):
	aaa=token.replace("\"","")
	bb=aaa.split(",")
	cc=str(bb[0])
	dd=cc.split(":")
	emp=dd[1]
	
	month_array=['','January','February','March','April','May','June','July','August','September','October','November','December']
	mm=month_array.index(month)
	date1=date.today().replace(month=mm,day=1)
	date_cal=(date1+timedelta(days=32)).replace(day=1)
	date2=date_cal-timedelta(days=1)

	total_data=[]
	query=frappe.db.sql("""SELECT attendance_date,status,late_entry FROM `tabAttendance`
		WHERE employee="""+str(emp)+""" and docstatus='1'
		and attendance_date>='"""+str(date1)+"""' and attendance_date<='"""+str(date2)+"""'
		ORDER BY attendance_date
		""",as_dict=1)
	for i in query:
		val="No"
		if(i.late_entry==1):
			val="Yes"
		if(calendar.day_name[getdate(i.attendance_date).weekday()]!="Sunday"):
			total_data.append({
				"attendance_date":i.attendance_date,
				"status":i.status,
				"late_entry":val
				})
	return total_data


@frappe.whitelist()
def create_leave_request(emp,from_date,to_date,day,leave_type,reason):
	err='Done'
	try:
		d1=getdate(from_date)
		d2=getdate(to_date)
		ar=[]
		while d1<=d2:
			ar.append(d1.strftime("%Y-%m-%d"))
			d1+=timedelta(days=1)
		nn=0.5
		if(day=="Full day"):
			nn=1
		
		leave=frappe.new_doc("Leave Request")
		leave.employee=emp
		leave.employee_name=frappe.db.get_value("Employee",str(emp),"employee_name")
		leave.department=frappe.db.get_value("Employee",str(emp),"department")
		leave.month=d2.strftime("%B")
		for i in ar:
			leave.append("leave_table",{
				"from_date":str(i),
				"to_date":str(i),
				"day":day,
				"no_of_days":nn,
				"leave_type":str(leave_type),
				"explanation":str(reason)
				})
		leave.save()
	except Exception as e:
		err=str(e)
	return err

@frappe.whitelist()
def create_ot_request(emp,token,from_date,to_date,reason):
	err='Done'
	try:
		d1=datetime.strptime(from_date,("%Y-%m-%d %H:%M:%S"))
		d2=datetime.strptime(to_date,("%Y-%m-%d %H:%M:%S"))
		diff=(d2-d1).total_seconds() / 3600
		ot=frappe.new_doc("OT request")
		ot.employee=emp
		ot.from_time=d1
		ot.to_time=d2
		ot.hours=diff
		ot.explanation=reason
		ot.status='Present'
		ot.save()
	except Exception as e:
		err=str(e)

	return err

@frappe.whitelist()
def create_claim_request(emp,token,expense_date,claim_type,description,amount,km_travel=None):
	err='Done'
	local = timezone("Asia/Kolkata")
	_time=datetime.now(local)
	today=_time.date()
	diff=(today-getdate(expense_date)).days
	try:
		if(diff<=3):
			amt=3.10
			if(claim_type=="Fuel (Car)"):
				amt=6.70
			claim=frappe.new_doc("Claim Request")
			claim.posting_date=today
			claim.employee=emp
			if(claim_type in ["Fuel (Bike)","Fuel (Car)"]):
				claim.grand_total=float(km_travel)*float(amt)
				claim.append("expenses",{
					"expense_date":getdate(expense_date),
					"expense_type":claim_type,
					"km_if_travel":km_travel,
					"amount":float(km_travel)*float(amt),
					"description":description
					})
			else:
				claim.append("expenses",{
					"expense_date":getdate(expense_date),
					"expense_type":claim_type,
					"amount":amount,
					"description":description
					})
				claim.grand_total=amount
			claim.save()
		else:
			err="Claim should be raised within 2 working days"
	except Exception as e:
		err=str(e)
	return err
@frappe.whitelist()
def get_claim_report(emp,token):
	query=frappe.db.sql("""SELECT cr.posting_date,cr.grand_total,cr.workflow_state
		FROM `tabClaim Request`as cr
		WHERE cr.posting_date>"2023-01-01" and cr.employee='"""+str(emp)+"""'
		ORDER BY cr.posting_date DESC""",as_dict=1)
	ar=[]
	for i in query:
		ar.append({
			"date":str(getdate(i.posting_date).strftime("%d-%m-%Y")),
			"grand_total":str(i.grand_total),
			"workflow_state":i.workflow_state
			})
	return ar
	
@frappe.whitelist()
def get_applied_leaves(emp,token):
	query=frappe.db.sql("""SELECT lt.from_date,lt.leave_type,lr.workflow_state,lt.day,lt.explanation 
		FROM `tabLeave Request`as lr INNER JOIN `tabLeave table`as lt 
		ON lt.parent=lr.name 
		WHERE lt.from_date>"2023-01-01" and lr.employee='"""+str(emp)+"""'
		ORDER BY lt.from_date DESC""",as_dict=1)
	ar=[]
	for i in query:
		ar.append({
			"from_date":getdate(i.from_date).strftime("%d/%m/%y"),
			"leave_type":i.leave_type,
			"workflow_state":i.workflow_state,
			"day":i.day,
			"explanation":i.explanation
			})
	return ar

@frappe.whitelist()
def get_ot_request(emp,token):
	query=frappe.db.sql("""SELECT employee_name,from_time,hours,workflow_state
		FROM `tabOT request`
		WHERE from_time>"2023-01-01 00:00:00" and employee='"""+str(emp)+"""'
		ORDER BY to_time DESC""",as_dict=1)
	ar=[]
	for i in query:
		ar.append({
			"employee_name":i.employee_name,
			"from_time":str(getdate(i.from_time)),
			"hours":str(i.hours),
			"workflow_state":str(i.workflow_state)
			})
	return ar

@frappe.whitelist()
def get_od_request(emp,token):
	query=frappe.db.sql("""SELECT employee_name,from_time,to_time,hours,explanation,workflow_state
		FROM `tabOn duty request`
		WHERE from_time>"2023-01-01 00:00:00" and employee='"""+str(emp)+"""'
		ORDER BY to_time DESC""",as_dict=1)
	ar=[]
	for i in query:
		ar.append(i)
	return ar

@frappe.whitelist()
def days_in_wtt(emp):
	query=frappe.db.sql("SELECT datediff(date_format(current_date,'%Y-%m-%d'),date_format(date_of_joining,'%Y-%m-%d')) as days FROM `tabEmployee` WHERE name='"+str(emp)+"' ",as_dict=1)
	ar=''
	for i in query:
		ar=str(i.days)
	return ar
@frappe.whitelist()
def last_late(emp):
	dd=''
	query=frappe.db.sql("SELECT datediff(date_format(current_date,'%Y-%m-%d'),date_format(attendance_date,'%Y-%m-%d'))as late FROM `tabAttendance` WHERE employee='"+str(emp)+"' AND late_entry=1 AND status!='Half Day' and docstatus=1 ORDER BY attendance_date DESC LIMIT 1",as_dict=1)
	for i in query:
		dd=str(i.late)
	return dd


@frappe.whitelist()
def last_leave(emp):
	dd=''
	query=frappe.db.sql("SELECT datediff(date_format(current_date,'%Y-%m-%d'),date_format(attendance_date,'%Y-%m-%d'))as days FROM `tabAttendance` WHERE status='Absent' AND employee='"+str(emp)+"' AND DAYOFWEEK(date_format(attendance_date,'%Y-%m-%d'))!=1 and docstatus=1 ORDER BY attendance_date DESC LIMIT 1",as_dict=1)
	for i in query:
		dd=str(i.days)
	return dd
@frappe.whitelist()
def grade(emp):
	dd=''
	query=frappe.db.sql("""SELECT
		CASE WHEN ((sum(`tabWork Update`.`gained_points`)/sum(`tabWork Update`.`total_points`)*5)<0) THEN 0 WHEN ((sum(`tabWork Update`.`gained_points`)/sum(`tabWork Update`.`total_points`)*5)>5) THEN 5 ELSE sum(`tabWork Update`.`gained_points`)/sum(`tabWork Update`.`total_points`)*5 END AS 'grade'
		FROM `tabTask Allocation`
		INNER JOIN 
		`tabWork Update` 
		ON `tabTask Allocation`.`name` = `tabWork Update`.`parent`
		WHERE 
		`tabTask Allocation`.`docstatus`!=2 and `tabTask Allocation`.`employee`='"""+str(emp)+"""' and `tabTask Allocation`.`workflow_state`!='Rejected'
		GROUP BY `tabTask Allocation`.`employee_name`
		""",as_dict=1)
	for i in query:
		dd=str(round(i.grade,2))

	return dd

@frappe.whitelist()
def task_list(emp):
	ar=[]
	query = frappe.db.sql("""SELECT 
		act.type_of_work as "type_of_work",
		act.description as "description",
		date_format(act.from_time,'%d-%m-%Y %H:%i:%S') as "assing_date",
		date_format(act.to_time,'%d-%m-%Y %H:%i:%S') as "expected_date",
		act.status as "status",
		CASE WHEN (DATEDIFF(now(),act.to_time))<0 THEN 0 ELSE DATEDIFF(now(),act.to_time) END AS "pending_days"
		from `tabWork Update` as act, `tabTask Allocation` as ac 
		where act.parent = ac.name and ac.employee='"""+str(emp)+"""' and act.status!='Completed' and ac.docstatus!=2 and ac.workflow_state!='Rejected' """,as_dict=1)
	for i in query:
		ar.append({
			"type_of_work":str(i.type_of_work),
			"description":str(i.description),
			"assing_date":str(i.assing_date),
			"expected_date":str(i.expected_date),
			"status":str(i.status),
			"pending_days":str(i.pending_days)
			})

	return ar

@frappe.whitelist()
def dept_design(emp):
	department=frappe.db.get_value("Employee",str(emp),"department")
	designation=frappe.db.get_value("Employee",str(emp),"designation")
	return department,designation


@frappe.whitelist()
def in_punch(emp,lat,log,add):
	local = timezone("Asia/Kolkata")
	_time=datetime.now(local)
	ttime=_time.strftime("%Y-%m-%d %H:%M:%S")

	# geolocator = Nominatim(user_agent="geoapiExercises")
	# Latitude = lat
	# Longitude = log
	# location = geolocator.geocode(Latitude+","+Longitude)

	punch=frappe.new_doc("Day In Day Out")
	punch.employee=emp
	punch.time=ttime
	punch.latitude=lat
	punch.longitude=log
	punch.address=add
	punch.log="IN"
	punch.save()

	ec=frappe.new_doc("Employee Checkin")
	ec.employee=emp
	ec.time=ttime
	ec.latitude=lat
	ec.longitude=log
	ec.address=add
	ec.log_type="IN"
	ec.save(ignore_permissions=True)

	return ec.name
@frappe.whitelist()
def out_punch(emp,lat,log,add):
	local = timezone("Asia/Kolkata")
	_time=datetime.now(local)
	ttime=_time.strftime("%Y-%m-%d %H:%M:%S")

	# geolocator = Nominatim(user_agent="geoapiExercises")
	# Latitude = lat
	# Longitude = log
	# location = geolocator.geocode(Latitude+","+Longitude)

	punch=frappe.new_doc("Day In Day Out")
	punch.employee=emp
	punch.time=ttime
	punch.latitude=lat
	punch.longitude=log
	punch.address=add
	punch.log="OUT"
	punch.save()

	ec=frappe.new_doc("Employee Checkin")
	ec.employee=emp
	ec.time=ttime
	ec.latitude=lat
	ec.longitude=log
	ec.address=add
	ec.log_type="OUT"
	ec.save(ignore_permissions=True)
	return ec.name

@frappe.whitelist()
def get_checkin(emp):
	local = timezone("Asia/Kolkata")
	_time=datetime.now(local)
	ttime=_time.replace(hour=0,minute=0,second=0)
	ar=[]
	query=frappe.db.sql("SELECT * from `tabDay In Day Out` where employee='"+str(emp)+"' and time>='"+str(ttime)+"' order by time desc",as_dict=1)
	if query:
		for i in query:
			ar.append(i)
	return ar

@frappe.whitelist()
def agent_communication(emp,customer,conversation,client_side,mode_of_communication,result):
	local = timezone("Asia/Kolkata")
	_time=datetime.now(local)
	today=_time.date()
	if(frappe.db.sql("SELECT * from `tabAgent Communication` WHERE customer='"+str(customer)+"' ")):
		ac=frappe.get_doc("Agent Communication",str(customer))
		ac.append("communication",{
			"date":today,
			"conversation":conversation,
			"agent":frappe.db.get_value("User",{"full_name":str(emp)}),
			"client_side_representative":client_side,
			"mode_of_communication":mode_of_communication,
			"result":result
			})
		ac.save()
	else:
		ac=frappe.new_doc("Agent Communication")
		ac.customer=customer
		ac.append("communication",{
			"date":today,
			"conversation":conversation,
			"agent":frappe.db.get_value("User",{"full_name":str(emp)}),
			"client_side_representative":client_side,
			"mode_of_communication":mode_of_communication,
			"result":result
			})
		ac.save()

@frappe.whitelist()
def create_customer(emp,customer_name,cg,ter,em=None,mob=None,a1=None,a2=None,ct=None,zc=None,st=None,cnty=None):
	ac=frappe.new_doc("Customer")
	ac.customer_name=customer_name
	ac.customer_group=cg
	ac.territory=ter
	if(em!=None):
		ac.email_id=em
	if(mob!=None):
		ac.moobile_no=mob
	if(a1!=None):
		ac.address_line1=a1
	if(a2!=None):
		ac.address_line2=a2
	if(ct!=None):
		ac.city=ct
	if(st!=None):
		ac.state=st
	if(cnty!=None):
		ac.country=cnty
	if(zc!=None):
		ac.pincode=zc
	ac.save()
@frappe.whitelist()
def get_customer_list():
	customer=[]
	for i in frappe.db.sql("SELECT distinct(name)as name from `tabCustomer` WHERE disabled=0",as_dict=1):
		customer.append(i.name)
	return customer
@frappe.whitelist()
def get_customer_group_list():
	customer=[]
	for i in frappe.db.sql("SELECT distinct(name)as name FROM `tabCustomer Group`",as_dict=1):
		customer.append(i.name)
	return customer
@frappe.whitelist()
def get_territory():
	customer=[]
	for i in frappe.db.sql("SELECT distinct(name)as name FROM `tabTerritory`",as_dict=1):
		customer.append(i.name)
	return customer




@frappe.whitelist()
def get_employee(token):
	query=frappe.db.sql("SELECT distinct(employee) as employee,employee_name FROM `tabDay In Day Out`",as_dict=1)
	
	return query


@frappe.whitelist()
def get_employee_logtime(token,emp):
	query=frappe.db.sql("SELECT time as 'log_time',latitude,longitude,address,log FROM `tabDay In Day Out` where employee='"+str(emp)+"' order by log_time DESC",as_dict=1)
	return query


@frappe.whitelist()
def get_employee_logtime_on_date(token,emp,ondate):
	aa=datetime.strptime(str(ondate), '%Y-%m-%d %H:%M:%S.%f')
	bb=aa+timedelta(hours=24)

	query=frappe.db.sql("SELECT time as 'log_time',latitude,longitude,address,log FROM `tabDay In Day Out` where employee='"+str(emp)+"' and time>='"+str(aa)+"' and time<='"+str(bb)+"' order by log_time DESC",as_dict=1)
	return query

@frappe.whitelist()
def check_leave(emp,from_date,to_date,value,day):
	frappe.msgprint(emp)
	frappe.msgprint(str(from_date))
	frappe.msgprint(str(to_date))
	frappe.msgprint(value)
	frappe.msgprint(day)

##ENDING OF EMPLOYEE APPLICATION CODING
@frappe.whitelist()
def create_lead_series(zone,nn):
	try:
		leads=frappe.db.sql("SELECT count(name)as lead_count FROM `tabLead` WHERE zone='"+str(zone)+"' and name!='"+str(nn)+"' GROUP BY zone",as_dict=1)
		cnt=1
		if leads:
			for i in leads:
				cnt=1+i.lead_count
		sers_no=zone+"-"+"L"+(str(cnt))

		return [{"sers_no":sers_no}]
	except Exception as e:
		frappe.msgprint(str(e))
		return [{"sers_no":''}]

@frappe.whitelist(allow_guest=True)
def create_enquiry_from_website(f1=None,f2=None,f3=None,f4=None,f5=None,f6=None,f7=None):
	doc=frappe.new_doc("Enquiry")
	doc.first_name=f1
	doc.email=f2
	doc.company=f3
	doc.city=f4
	doc.country_code=f5
	doc.mobile=f6
	doc.description=f7
	doc.save()
	return 'done'

@frappe.whitelist(allow_guest=True)
def create_card_details(user):	
	frappe.msgprint(str(user))
	# child_table_data = []
	# local = timezone("Asia/Kolkata")
	# _time=datetime.now(local)
	# today=_time.date()
	# bb=user.replace("\"","")
	# cc=bb.replace("\'[","[")
	# dd=cc.replace("]\'","]")
	# s = dd.replace("\'", "\"")
	# vv= json.loads(s)
	# return str(vv)

@frappe.whitelist()
def send_whatsapp(client_name,phone):
	url = "https://api.ultramsg.com/instance53998/messages/chat"
	payload = "token=sufdskptbgekq839&to="+str(phone)+"&body=Dear "+str(client_name)+",\n\nHappy Greetings from *WTT INTERNATIONAL PVT LTD!*\n\nWe are delighted to meet you.\n\nThank you for listening us."
	payload = payload.encode('utf8').decode('iso-8859-1')
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response

@frappe.whitelist()
def get_items_from_itemgroup(item_group):
	ar=[]
	for i in frappe.db.sql("SELECT name FROM `tabItem` where item_group='"+str(item_group)+"' ",as_dict=1):
		ar.append(i.name)
	return ar


@frappe.whitelist()
def mail_send(ref_name):
	recipients_=["poa@wttindia.com","purchase@wttindia.com"]
	message= f"Dear Purchase Team,<br><br>Here I listed out the rejected items for <b>"+str(ref_name)+"</b>.<br><br><table cellpadding='5' cellspacing='5' style='border: 1px solid;border-collapse:collapse;'><tr><th style='border: 1px solid;border-collapse:collapse;'>Description</th><th style='border: 1px solid;border-collapse:collapse;'>Technical Description</th><th style='border: 1px solid;border-collapse:collapse;'>Qty</th><th style='border: 1px solid;border-collapse:collapse;'>PR Row</th><th style='border: 1px solid;border-collapse:collapse;'>Purchase Order</th><th style='border: 1px solid;border-collapse:collapse;'>PO Row</th><th style='border: 1px solid;border-collapse:collapse;'>Status</th><th style='border: 1px solid;border-collapse:collapse;'>Reason</th></tr>"
	dc = frappe.get_doc("Purchase Receipt",ref_name)
	for i in dc.items:
		po_row = frappe.db.get_value("Purchase Order Item",i.purchase_order_item,"idx")
		po_name = i.purchase_order
		if(po_row == None):
			po_row = "-"
		if(po_name == None):
			po_name = "-"
		rej=i.reject_reason
		if(i.reject_reason == None):
			rej=''
		if(i.inspection_status == 'Debit'):
			message+="<tr>"
			message+="<td style='border: 1px solid;border-collapse:collapse;'>"+str(i.description)+"</td>"
			message+="<td style='border: 1px solid;border-collapse:collapse;'>"+str(i.technical_description)+"</td>"
			message+="<td style='border: 1px solid;border-collapse:collapse;'>"+str(i.qty)+"</td>"
			message+="<td style='border: 1px solid;border-collapse:collapse;'>"+str(i.idx)+"</td>"
			message+="<td style='border: 1px solid;border-collapse:collapse;'>"+str(po_name)+"</td>"
			message+="<td style='border: 1px solid;border-collapse:collapse;'>"+str(po_row)+"</td>"
			message+="<td style='border: 1px solid;border-collapse:collapse;><b style='color:red'>Rejected</b></td>"
			message+="<td style='border: 1px solid;border-collapse:collapse;'>"+str(rej)+"</td>"
			message+="</tr>"
	message+="</table><br><br>Thank you,<br>Stores Department"
	password = None
	email_args = {
		"subject": "Rejected Items",
		"recipients": recipients_,
		"message": message
		}
	frappe.sendmail(**email_args)
	return "Success"


@frappe.whitelist()
def order_confirmation_mail(ref_name,supplier):
	recipients_=["it@wttindia.com","erp@wttindia.com"]
	url = f"https://erp.wttindia.com/order-confirmation/new?purchase_order={ref_name}&supplier={supplier}"
	encoded_url = urllib.parse.quote(url, safe=':/?=&')
	message= f"Dear Supplier,<br><br>I hope this email finds you well. We are writing to request your confirmation on the following details related to our recent purchase order, {ref_name}<br><br><b>Acceptance:</b> Kindly confirm your acceptance of the purchase order.<br><b>Dispatch Date:</b> Please provide the expected dispatch date for the ordered goods/services.<br><b>Receive Date:</b> Confirm the anticipated date of receiving the consignment.<br><b>Payment Terms:</b> Verify the agreed-upon payment terms or inform us of any adjustments.<br><b>Other Terms:</b> Confirm understanding of any additional terms mentioned in the purchase order.<br><br>Update the details using this link below<br>{encoded_url}<br><br>Your swift response is appreciated, as it will help us ensure a smooth procurement process. If there are any concerns or queries, feel free to reach out.<br><br>Thank you for your cooperation.<br><br>Best regards,<br>WTT"
	password = None
	email_args = {
		"subject": f"Order Confimation for {ref_name}",
		"recipients": recipients_,
		"message": message
		}
	frappe.sendmail(**email_args)
	frappe.db.sql("UPDATE `tabPurchase Order` SET order_confirmation_mail='Order Confirmation Mail Sent' WHERE name='"+str(ref_name)+"'")
	return "Success"