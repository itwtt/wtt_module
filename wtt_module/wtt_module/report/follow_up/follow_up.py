# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

# from __future__ import unicode_literals
# import frappe
# from frappe import _
# import numpy as np
# from datetime import datetime,timedelta
# from frappe.desk.reportview import build_match_conditions


# def execute(filters=None):
# 	data = []
# 	columns = get_columns(filters)
# 	data = get_data(data,filters)
# 	return columns, data

# def get_columns(filters):
# 	columns=[
# 		{
# 			"label": _("Lead"),
# 			"fieldtype": "Link",
# 			"fieldname": "lead",
# 			"options":"Lead",
# 			"width": 25
# 		},
# 		{
# 			"label": _("Conversation Date"),
# 			"fieldtype": "HTML",
# 			"fieldname": "convo_date",
# 			"width": 80
# 		},
# 		{
# 			"label": _("organization"),
# 			"fieldtype": "HTML",
# 			"fieldname": "organization",
# 			"width": 150
# 		},
# 		{
# 			"label": _("Contact Person"),
# 			"fieldtype": "HTML",
# 			"fieldname": "contact_person",
# 			"width": 100
# 		},
# 		{
# 			"label": _("Location"),
# 			"fieldtype": "HTML",
# 			"fieldname": "location",
# 			"width": 80
# 		},
# 		{
# 			"label": _("Designation"),
# 			"fieldtype": "HTML",
# 			"fieldname": "designation",
# 			"width": 80
# 		},
# 		{
# 			"label": _("Conversation"),
# 			"fieldtype": "HTML",
# 			"fieldname": "conversation",
# 			"width": 150
# 		},
# 		{
# 			"label": _("Enquiry For"),
# 			"fieldtype": "HTML",
# 			"fieldname": "enquiry_for",
# 			"width": 80
# 		},
# 		{
# 			"label": _("Capacity"),
# 			"fieldtype": "HTML",
# 			"fieldname": "capacity",
# 			"width": 50
# 		},
# 		{
# 			"label": _("Followed by"),
# 			"fieldtype": "HTML",
# 			"fieldname": "follow_by",
# 			"width": 80
# 		},
# 		{
# 			"label": _("Next Contact Date"),
# 			"fieldtype": "HTML",
# 			"fieldname": "next_contact",
# 			"width": 80
# 		},
# 		{
# 			"label": _("L"),
# 			"fieldtype": "HTML",
# 			"fieldname": "ll",
# 			"width": 1,
# 			"hidden":1
# 		},
# 		{
# 			"label": _("E"),
# 			"fieldtype": "HTML",
# 			"fieldname": "ee",
# 			"width": 1,
# 			"hidden":1
# 		},
# 		{
# 			"label": _("Q"),
# 			"fieldtype": "HTML",
# 			"fieldname": "qq",
# 			"width": 1,
# 			"hidden":1
# 		},
# 		{
# 			"label": _("C"),
# 			"fieldtype": "HTML",
# 			"fieldname": "cc",
# 			"width": 1,
# 			"hidden":1
# 		},
# 		{
# 			"label": _("P"),
# 			"fieldtype": "HTML",
# 			"fieldname": "pp",
# 			"width": 1,
# 			"hidden":1
# 		},
# 		{
# 			"label": _("T"),
# 			"fieldtype": "HTML",
# 			"fieldname": "tt",
# 			"width": 1,
# 			"hidden":1
# 		}
# 	]
	
# 	return columns
# def get_data(data,filters):
# 	data=[]
# 	for i in frappe.db.sql("SELECT `tabLead`.name,`tabFollow up`.date,`tabFollow up`.color,`tabFollow up`.employee_name,`tabLead`.company_name,`tabLead`.contact_date,`tabLead`.state,`tabLead`.country,`tabLead`.job_title,`tabLead`.mobile_no,`tabLead`.capacity,`tabLead`.plant_type,`tabLead`.system_name,`tabLead`.future_expansion,`tabLead`.enquiry_for,`tabFollow up`.conversation,`tabFollow up`.employee_name,`tabFollow up`.client_side_representative,`tabFollow up`.result,`tabLead`.lead_s,`tabLead`.enquiry_s,`tabLead`.clarification_s,`tabLead`.questionnaire_s,`tabLead`.pp_meeting,`tabLead`.tcp FROM `tabFollow up` INNER JOIN `tabLead` ON `tabLead`.name=`tabFollow up`.parent WHERE `tabFollow up`.date>='"+str(filters.get("from_date"))+"' and `tabFollow up`.date<='"+str(filters.get("to_date"))+"'",as_dict=1):
# 		vv=''
# 		if(i.lead_s):
# 			ll='<p>&#10004;</p>'
# 		else:
# 			ll='<p>&#9633;</p>'
		
# 		if(i.enquiry_s):
# 			ee='<p>&#10004;</p>'
# 		else:
# 			ee='<p>&#9633;</p>'
		
# 		if(i.questionnaire_s):
# 			qq='<p>&#10004;</p>'
# 		else:
# 			qq='<p>&#9633;</p>'
		
# 		if(i.clarification_s):
# 			cc='<p>&#10004;</p>'
# 		else:
# 			cc='<p>&#9633;</p>'

		
# 		if(i.pp_meeting):
# 			pp='<p>&#10004;</p>'
# 		else:
# 			pp='<p>&#9633;</p>'
		
# 		if(i.tcp):
# 			tt='<p>&#10004;</p>'
# 		else:
# 			tt='<p>&#9633;</p>'

# 		cab='-'
# 		if(i.capacity is not None):
# 			cab=i.capacity	

# 		enqf='-'
# 		if(i.enquiry_for is not None):
# 			enqf=i.enquiry_for

# 		desg='-'
# 		if(i.job_title is not None):
# 			desg=i.job_title


# 		if(i.color == "Green"):
# 			if(i.contact_date is not None):
# 				vv=i.contact_date.strftime("%d/%m/%y")
# 			data.append({
# 				'lead':i.name,
# 				'convo_date':"<p style='background:lightgreen;color:black;font-weight:bold;'>"+i.date.strftime("%d/%m/%y")+"</p>",
# 				'organization':"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
# 				'location':"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.country)+"</p>",
# 				'contact_person':"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.client_side_representative)+"</p>",
# 				'designation':"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(desg)+"</p>",
# 				'conversation':"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.conversation)+"</p>",
# 				'enquiry_for':"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(enqf)+"</p>",
# 				'capacity':"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(cab)+"</p>",
# 				'follow_by':"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
# 				'next_contact':"<p style='background:lightgreen;color:black;font-weight:bold;'>"+vv+"</p>",
# 				'll':ll,
# 				'ee':ee,
# 				'qq':qq,
# 				'cc':cc,
# 				'pp':pp,
# 				'tt':tt
# 				})
# 		elif(i.color == "Red"):
# 			if(i.contact_date is not None):
# 				vv=i.contact_date.strftime("%d/%m/%y")
# 			data.append({
# 				'lead':i.name,
# 				'convo_date':"<p style='background:#F67280;color:black;font-weight:bold;;color:black;font-weight:bold;'>"+i.date.strftime("%d/%m/%y")+"</p>",
# 				'organization':"<p style='background:#F67280;color:black;font-weight:bold;;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
# 				'location':"<p style='background:#F67280;color:black;font-weight:bold;;color:black;font-weight:bold;'>"+str(i.country)+"</p>",
# 				'contact_person':"<p style='background:#F67280;color:black;font-weight:bold;;color:black;font-weight:bold;'>"+str(i.client_side_representative)+"</p>",
# 				'designation':"<p style='background:#F67280;color:black;font-weight:bold;;color:black;font-weight:bold;'>"+str(desg)+"</p>",
# 				'conversation':"<p style='background:#F67280;color:black;font-weight:bold;;color:black;font-weight:bold;'>"+str(i.conversation)+"</p>",
# 				'enquiry_for':"<p style='background:#F67280;color:black;font-weight:bold;;color:black;font-weight:bold;'>"+str(enqf)+"</p>",
# 				'follow_by':"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
# 				'capacity':"<p style='background:#F67280;color:black;font-weight:bold;;color:black;font-weight:bold;'>"+str(cab)+"</p>",
# 				'next_contact':"<p style='background:#F67280;color:black;font-weight:bold;'>"+vv+"</p>",
# 				'll':ll,
# 				'ee':ee,
# 				'qq':qq,
# 				'cc':cc,
# 				'pp':pp,
# 				'tt':tt
# 				})
# 		elif(i.color == "Yellow"):
# 			if(i.contact_date is not None):
# 				vv=i.contact_date.strftime("%d/%m/%y")
# 			data.append({
# 				'lead':i.name,
# 				'convo_date':"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+i.date.strftime("%d/%m/%y")+"</p>",
# 				'organization':"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
# 				'location':"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.country)+"</p>",
# 				'contact_person':"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.client_side_representative)+"</p>",
# 				'designation':"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(desg)+"</p>",
# 				'conversation':"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.conversation)+"</p>",
# 				'enquiry_for':"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(enqf)+"</p>",
# 				'follow_by':"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
# 				'capacity':"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(cab)+"</p>",
# 				'next_contact':"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+vv+"</p>",
# 				'll':ll,
# 				'ee':ee,
# 				'qq':qq,
# 				'cc':cc,
# 				'pp':pp,
# 				'tt':tt
# 				})
# 		else:
# 			if(i.contact_date is not None):
# 				vv=i.contact_date.strftime("%d/%m/%y")
# 			data.append({
# 				'lead':i.name,
# 				'convo_date':i.date.strftime("%d/%m/%y"),
# 				'organization':i.company_name,
# 				'location':i.country,
# 				'contact_person':i.client_side_representative,
# 				'designation':desg,
# 				'conversation':i.conversation,
# 				'enquiry_for':enqf,
# 				'follow_by':i.employee_name,
# 				'capacity':cab,
# 				'next_contact':vv,
# 				'll':ll,
# 				'ee':ee,
# 				'qq':qq,
# 				'cc':cc,
# 				'pp':pp,
# 				'tt':tt
# 				})
# 	return data


# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from datetime import datetime,timedelta
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
	data = []
	columns = get_columns(filters)
	conditions = get_conditions(filters)
	data = get_data(conditions,data,filters)
	return columns, data

def get_columns(filters):
	columns=[
		{
			"label": _("Lead"),
			"fieldtype": "Link",
			"fieldname": "lead",
			"options":"Lead",
			"width": 25
		},
		# {
		# 	"label": _("Idx"),
		# 	"fieldtype": "Data",
		# 	"fieldname": "row",
		# 	"width": 80
		# },
		# {
		# 	"label": _("Taken Date"),
		# 	"fieldtype": "Data",
		# 	"fieldname": "date",
		# 	"width": 80
		# },
		{
			"label": _("Convo Date"),
			"fieldtype": "Data",
			"fieldname": "convo_date",
			"width": 80
		},
		# {
		# 	"label": _("Next Follow BY"),
		# 	"fieldtype": "Data",
		# 	"fieldname": "follow_by",
		# 	"width": 120
		# },
		{
			"label": _("Organization"),
			"fieldtype": "Data",
			"fieldname": "organization",
			"width": 200
		},
		# {
		# 	"label": _("Project"),
		# 	"fieldtype": "Data",
		# 	"fieldname": "project",
		# 	"width": 100
		# },
		{
			"label": _("Location"),
			"fieldtype": "Data",
			"fieldname": "location",
			"width": 100
		},
		{
			"label": _("Contact Person"),
			"fieldtype": "Data",
			"fieldname": "contact_person",
			"width": 120
		},
		{
			"label": _("Contact Details"),
			"fieldtype": "Data",
			"fieldname": "contact_details",
			"width": 120
		},
		{
			"label": _("Follow Up Details"),
			"fieldtype": "Data",
			"fieldname": "follow_up_details",
			"width": 300
		},
		{
			"label": _("Followed by"),
			"fieldtype": "Data",
			"fieldname": "followed_by",
			"width": 100
		},
		{
			"label": _("Next Follow Up Date"),
			"fieldtype": "HTML",
			"fieldname": "next_follow_up_date",
			"width": 90
		}

	]
	
	return columns
def get_data(conditions,data,filters):
	data=[]
	lead=[]
	row=[]
	ref=[]
	ar=[]
	ar2=[]
	td=datetime.now().replace(hour=00,minute=00,second=00,microsecond=00)
	td2=td.replace(hour=23,minute=59,second=59)
	
	query2=frappe.db.sql(" SELECT lt.idx,lt.employee_name,lr.taken_date,lr.contact_by,lr.name,lr.contact_date,lr.city,lr.company_name,lr.status,lt.date,lr.city as location,lt.mode_of_communication,lr.mobile_no,lr.lead_name,lt.conversation as result from `tabLead` as lr, `tabFollow up` as lt where lt.parent = lr.name and lr.contact_date>='"+str(td)+"' and lr.contact_date<='"+str(td2)+"' and lr.follow_up=1 ", filters, as_dict=1)
	if(filters.reports_for=="trading@wttindia.com"):
		query2=frappe.db.sql(" SELECT lt.idx,lt.employee_name,lr.taken_date,lr.contact_by,lr.name,lr.contact_date,lr.city,lr.company_name,lr.status,lt.date,lr.city as location,lt.mode_of_communication,lr.mobile_no,lr.lead_name,lt.conversation as result from `tabLead` as lr, `tabFollow up` as lt where lt.parent = lr.name and lr.contact_date>='"+str(td)+"' and lr.contact_date<='"+str(td2)+"' and lr.follow_up=1 ", filters, as_dict=1)

	for i in query2:
		ar.clear()
		for j in frappe.db.sql("SELECT bb.idx from `tabLead` as aa,`tabFollow up` as bb WHERE aa.name=bb.parent and aa.name='"+str(i.name)+"' ",as_dict=1):
			ar.append(j)
		if(i.contact_date!=None):
			if(i.contact_date.replace(hour=00,minute=00,second=00,microsecond=00)==datetime.now().replace(hour=00,minute=00,second=00,microsecond=00)):
				ht='<p style="color:green"><b>'+(i.contact_date).strftime("%d/%m/%y")+'</b></p>'
			else:
				ht='<p>'+(i.contact_date).strftime("%d/%m/%y")+'</p>'
		else:
			ht="-"
		
		if(len(ar)==i.idx):
			td_format="-"
			convo_format='-'
			if(i.taken_date!=None):
				td_format=(i.taken_date).strftime("%d/%m/%y")
			if(i.date!=None):
				convo_format=(i.date).strftime("%d/%m/%y")
			
			data.append({
				"row":i.idx,
				"lead":i.name,
				"date":td_format,
				"convo_date":i.date,
				"follow_by":i.contact_by,
				"organization":i.company_name,
				"location":i.location,
				"follow_up_details":i.result,
				"next_follow_up_date":ht,
				"contact_details":i.mobile_no,
				"followed_by":i.employee_name,
				"contact_person":i.lead_name
				})
		ref.append(i.name)
	#query=frappe.db.sql(""" select lt.idx,lr.taken_date,lr.name,lr.contact_date,lr.city,lr.company_name,lr.status,lt.date,lr.city as location,lt.conversation as result,lt.mode_of_communication,lr.mobile_no,lr.lead_name,lt.conversation as result from `tabLead` as lr, `tabFollow up` as lt where lt.parent = lr.name and lr.category = 'Follow Up' %s group by lr.name"""%(conditions), filters, as_dict=1)
	query=frappe.db.sql(""" SELECT lt.idx,lt.employee_name,lr.taken_date,lr.name,lr.contact_date,lr.city,lr.company_name,lr.status,lt.date,lr.city as location,lt.mode_of_communication,lr.mobile_no,lr.lead_name,lt.conversation as result from `tabLead` as lr, `tabFollow up` as lt WHERE lt.parent = lr.name and lr.follow_up=1 """,filters, as_dict=1)
	if(filters.reports_for=="trading@wttindia.com"):
		query=frappe.db.sql(""" SELECT lt.idx,lt.employee_name,lr.taken_date,lr.name,lr.contact_date,lr.city,lr.company_name,lr.status,lt.date,lr.city as location,lt.mode_of_communication,lr.mobile_no,lr.lead_name,lt.conversation as result from `tabLead` as lr, `tabFollow up` as lt WHERE lt.parent = lr.name and lr.follow_up=1 """,filters, as_dict=1)

	for i in query:
		# frappe.msgprint(str(i.company_name))
		ar.clear()
		for j in frappe.db.sql("SELECT bb.idx from `tabLead` as aa,`tabFollow up` as bb WHERE aa.name=bb.parent and aa.name='"+str(i.name)+"' ",as_dict=1):
			ar.append(j)
		if(i.contact_date!=None):
			if(i.contact_date.replace(hour=00,minute=00,second=00,microsecond=00)==datetime.now().replace(hour=00,minute=00,second=00,microsecond=00)):
				ht='<p style="background-color:purple;font-color:solidblack"><b>'+(i.contact_date).strftime("%d/%m/%y")+'</b></p>'
			else:
				ht='<p>'+(i.contact_date).strftime("%d/%m/%y")+'</p>'
		else:
			ht="-"
		
		# if(i.name=='CRM-LEAD-2021-00604'):
		# 	frappe.msgprint(str())
		convo_format='-'
		if(len(ar)==i.idx):
			if(i.name not in ref):
				td_format="-"
				convo_date="-"
				if(i.taken_date!=None):
					td_format=(i.taken_date).strftime("%d/%m/%y")
				if(i.date!=None):
					convo_format=(i.date).strftime("%d/%m/%y")
				
				data.append({
					"row":i.idx,
					"lead":i.name,
					"convo_date":convo_format,
					"date":td_format,
					"follow_by":i.contact_by,
					"organization":i.company_name,
					"location":i.location,
					"follow_up_details":i.result,
					"next_follow_up_date":ht,
					"contact_details":i.mobile_no,
					"followed_by":i.employee_name,
					"contact_person":i.lead_name
					})
	return data

def get_conditions(filters):
	conditions=''
	if filters.get("date"):
		conditions += " and lr.taken_date = %(date)s"
	if filters.get("organization"):
		conditions += " and lr.company_name = %(organization)s"

	match_conditions = build_match_conditions("Lead")
	if match_conditions:
		conditions += " and %s" % match_conditions
	return conditions
