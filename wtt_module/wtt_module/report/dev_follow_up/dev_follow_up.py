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
		{
			"label": _("Convo Date"),
			"fieldtype": "HTML",
			"fieldname": "convo_date",
			"width": 80
		},
		{
			"label": _("Organization"),
			"fieldtype": "HTML",
			"fieldname": "organization",
			"width": 200
		},
		{
			"label": _("Lead Temp"),
			"fieldtype": "HTML",
			"fieldname": "lead_temp",
			"width": 100
		},
		{
			"label": _("Lead Scale"),
			"fieldtype": "HTML",
			"fieldname": "lead_scale",
			"width": 100
		},
		{
			"label": _("Location"),
			"fieldtype": "HTML",
			"fieldname": "location",
			"width": 100
		},
		{
			"label": _("Capacity m3/day"),
			"fieldtype": "HTML",
			"fieldname": "capacity",
			"width": 100
		},
		{
			"label": _("Contact Person"),
			"fieldtype": "HTML",
			"fieldname": "contact_person",
			"width": 120
		},
		{
			"label": _("Contact Details"),
			"fieldtype": "HTML",
			"fieldname": "contact_details",
			"width": 120
		},
		{
			"label": _("Follow Up Details"),
			"fieldtype": "HTML",
			"fieldname": "follow_up_details",
			"width": 350
		},
		{
			"label": _("Followed by"),
			"fieldtype": "HTML",
			"fieldname": "followed_by",
			"width": 100
		},
		{
			"label": _("Next Follow Up Date"),
			"fieldtype": "HTML",
			"fieldname": "next_follow_up_date",
			"width": 90
		},
		{
			"label": _("L"),
			"fieldtype": "HTML",
			"fieldname": "ll",
			"width": 1,
			"hidden":1
		},
		{
			"label": _("E"),
			"fieldtype": "HTML",
			"fieldname": "ee",
			"width": 1,
			"hidden":1
		},
		{
			"label": _("Q"),
			"fieldtype": "HTML",
			"fieldname": "qq",
			"width": 1,
			"hidden":1
		},
		{
			"label": _("C"),
			"fieldtype": "HTML",
			"fieldname": "cc",
			"width": 1,
			"hidden":1
		},
		{
			"label": _("P"),
			"fieldtype": "HTML",
			"fieldname": "pp",
			"width": 1,
			"hidden":1
		},
		{
			"label": _("T"),
			"fieldtype": "HTML",
			"fieldname": "tt",
			"width": 1,
			"hidden":1
		}
	]
	
	return columns
def get_data(conditions,data,filters):
	if(filters.get("reports_type") == 'Followup Table wise'):
		data=[]
		lead=[]
		row=[]
		ref=[]
		ar=[]
		ar2=[]
		td=datetime.now().replace(hour=00,minute=00,second=00,microsecond=00)
		td2=td.replace(hour=23,minute=59,second=59)
		
		query2=frappe.db.sql("SELECT lr.lead_status,lr.lead_scale,lr.lead_s,lr.enquiry_s,lr.clarification_s,lr.questionnaire_s,lr.pp_meeting,lr.tcp,lt.color,lt.idx,lt.employee_name,lr.taken_date,lr.contact_by,lr.name,lr.contact_date,lr.city,lr.company_name,lr.status,lt.date,lr.city as location,lr.capacity,lt.mode_of_communication,lr.mobile_no,lr.lead_name,lt.conversation as result from `tabLead` as lr, `tabFollow up` as lt where lt.parent = lr.name and lr.contact_date>='"+str(td)+"' and lr.contact_date<='"+str(td2)+"' and lr.follow_up=1 ", filters, as_dict=1)
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
				
				vdes='-'
				if(i.capacity!=None):
					vdes = i.capacity

				vloc='-'
				if(i.location!=None):
					vloc = i.location

				if(i.lead_s):
					ll='<p>&#10004;</p>'
				else:
					ll='<p>&#9633;</p>'
				
				if(i.enquiry_s):
					ee='<p>&#10004;</p>'
				else:
					ee='<p>&#9633;</p>'
				
				if(i.questionnaire_s):
					qq='<p>&#10004;</p>'
				else:
					qq='<p>&#9633;</p>'
				
				if(i.clarification_s):
					cc='<p>&#10004;</p>'
				else:
					cc='<p>&#9633;</p>'

				
				if(i.pp_meeting):
					pp='<p>&#10004;</p>'
				else:
					pp='<p>&#9633;</p>'
				
				if(i.tcp):
					tt='<p>&#10004;</p>'
				else:
					tt='<p>&#9633;</p>'	

				if(i.color == "Green"):
					data.append({
						"row":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.idx)+"</p>",
						"lead_temp":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.lead_status)+"</p>",
						"lead_scale":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.lead_scale)+"</p>",
						"lead":i.name,
						"date":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(td_format)+"</p>",
						"convo_date":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.date)+"</p>",
						"follow_by":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.contact_by)+"</p>",
						"organization":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
						"location":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(vloc)+"</p>",
						"capacity":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(vdes)+"</p>",
						"follow_up_details":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.result)+"</p>",
						"next_follow_up_date":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(ht)+"</p>",
						"contact_details":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.mobile_no)+"</p>",
						"followed_by":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
						"contact_person":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.lead_name)+"</p>",
						'll':ll,
						'ee':ee,
						'qq':qq,
						'cc':cc,
						'pp':pp,
						'tt':tt
						})
				elif(i.color == "Red"):
					data.append({
						"row":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.idx)+"</p>",
						"lead_temp":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.lead_status)+"</p>",
						"lead_scale":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.lead_scale)+"</p>",
						"lead":i.name,
						"date":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(td_format)+"</p>",
						"convo_date":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.date)+"</p>",
						"follow_by":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.contact_by)+"</p>",
						"organization":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
						"location":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(vloc)+"</p>",
						"capacity":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(vdes)+"</p>",
						"follow_up_details":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.result)+"</p>",
						"next_follow_up_date":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(ht)+"</p>",
						"contact_details":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.mobile_no)+"</p>",
						"followed_by":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
						"contact_person":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.lead_name)+"</p>",
						'll':ll,
						'ee':ee,
						'qq':qq,
						'cc':cc,
						'pp':pp,
						'tt':tt
						})
				elif(i.color == "Yellow"):
					data.append({
						"row":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.idx)+"</p>",
						"lead_temp":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.lead_status)+"</p>",
						"lead_scale":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.lead_scale)+"</p>",
						"lead":i.name,
						"date":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(td_format)+"</p>",
						"convo_date":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.date)+"</p>",
						"follow_by":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.contact_by)+"</p>",
						"organization":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
						"location":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(vloc)+"</p>",
						"capacity":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(vdes)+"</p>",
						"follow_up_details":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.result)+"</p>",
						"next_follow_up_date":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(ht)+"</p>",
						"contact_details":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.mobile_no)+"</p>",
						"followed_by":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
						"contact_person":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.lead_name)+"</p>",
						'll':ll,
						'ee':ee,
						'qq':qq,
						'cc':cc,
						'pp':pp,
						'tt':tt
						})
				else:
					data.append({
						"row":i.idx,
						"lead_temp":i.lead_status,
						"lead_scale":i.lead_scale,
						"lead":i.name,
						"date":td_format,
						"convo_date":i.date,
						"follow_by":i.contact_by,
						"organization":i.company_name,
						"location":i.location,
						"capacity":i.capacity,
						"follow_up_details":i.result,
						"next_follow_up_date":ht,
						"contact_details":i.mobile_no,
						"followed_by":i.employee_name,
						"contact_person":i.lead_name,
						'll':ll,
						'ee':ee,
						'qq':qq,
						'cc':cc,
						'pp':pp,
						'tt':tt
						})
			ref.append(i.name)
		
		query=frappe.db.sql(""" SELECT lr.lead_status,lr.lead_scale,lr.lead_s,lr.enquiry_s,lr.clarification_s,lr.questionnaire_s,lr.pp_meeting,lr.tcp,lt.color,lt.idx,lt.employee_name,lr.taken_date,lr.name,lr.contact_date,lr.city,lr.company_name,lr.status,lt.date,lr.city as location,lr.capacity,lt.mode_of_communication,lr.mobile_no,lr.lead_name,lt.conversation as result from `tabLead` as lr, `tabFollow up` as lt WHERE lt.parent = lr.name and lr.follow_up=1 """,filters, as_dict=1)
		for i in query:
			ar.clear()
			for j in frappe.db.sql("SELECT bb.idx from `tabLead` as aa,`tabFollow up` as bb WHERE aa.name=bb.parent and aa.name='"+str(i.name)+"' ",as_dict=1):
				ar.append(j)
			if(i.contact_date!=None):
				if(i.contact_date.replace(hour=00,minute=00,second=00,microsecond=00)==datetime.now().replace(hour=00,minute=00,second=00,microsecond=00)):
					ht='<p style="font-color:solidblack"><b>'+(i.contact_date).strftime("%d/%m/%y")+'</b></p>'
				else:
					ht='<p>'+(i.contact_date).strftime("%d/%m/%y")+'</p>'
			else:
				ht="-"

			if(len(ar)==i.idx):
				if(i.name not in ref):
					td_format="-"
					convo_date="-"
					if(i.taken_date!=None):
						td_format=(i.taken_date).strftime("%d/%m/%y")
					if(i.date!=None):
						convo_format=(i.date).strftime("%d/%m/%y")
					

					vdes='-'
					if(i.capacity!=None):
						vdes = i.capacity

					vloc='-'
					if(i.location!=None):
						vloc = i.location

					if(i.lead_s):
						ll='<p>&#10004;</p>'
					else:
						ll='<p>&#9633;</p>'
					
					if(i.enquiry_s):
						ee='<p>&#10004;</p>'
					else:
						ee='<p>&#9633;</p>'
					
					if(i.questionnaire_s):
						qq='<p>&#10004;</p>'
					else:
						qq='<p>&#9633;</p>'
					
					if(i.clarification_s):
						cc='<p>&#10004;</p>'
					else:
						cc='<p>&#9633;</p>'

					
					if(i.pp_meeting):
						pp='<p>&#10004;</p>'
					else:
						pp='<p>&#9633;</p>'
					
					if(i.tcp):
						tt='<p>&#10004;</p>'
					else:
						tt='<p>&#9633;</p>'

					if(i.color == "Green"):
						data.append({
							"row":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.idx)+"</p>",
							"lead_temp":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.lead_status)+"</p>",
							"lead_scale":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.lead_scale)+"</p>",
							"lead":i.name,
							"convo_date":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(convo_format)+"</p>",
							"date":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(td_format)+"</p>",
							"follow_by":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.contact_by)+"</p>",
							"organization":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
							"location":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(vloc)+"</p>",
							"capacity":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(vdes)+"</p>",
							"follow_up_details":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.result)+"</p>",
							"next_follow_up_date":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(ht)+"</p>",
							"contact_details":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.mobile_no)+"</p>",
							"followed_by":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
							"contact_person":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.lead_name)+"</p>",
							'll':ll,
							'ee':ee,
							'qq':qq,
							'cc':cc,
							'pp':pp,
							'tt':tt
							})
					elif(i.color == "Red"):
						data.append({
							"row":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.idx)+"</p>",
							"lead_temp":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.lead_status)+"</p>",
							"lead_scale":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.lead_scale)+"</p>",
							"lead":i.name,
							"date":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(td_format)+"</p>",
							"convo_date":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.date)+"</p>",
							"follow_by":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.contact_by)+"</p>",
							"organization":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
							"location":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(vloc)+"</p>",
							"capacity":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(vdes)+"</p>",
							"follow_up_details":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.result)+"</p>",
							"next_follow_up_date":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(ht)+"</p>",
							"contact_details":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.mobile_no)+"</p>",
							"followed_by":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
							"contact_person":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.lead_name)+"</p>",
							'll':ll,
							'ee':ee,
							'qq':qq,
							'cc':cc,
							'pp':pp,
							'tt':tt
							})
					elif(i.color == "Yellow"):
						data.append({
							"row":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.idx)+"</p>",
							"lead_temp":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.lead_status)+"</p>",
							"lead_scale":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.lead_scale)+"</p>",
							"lead":i.name,
							"date":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(td_format)+"</p>",
							"convo_date":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.date)+"</p>",
							"follow_by":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.contact_by)+"</p>",
							"organization":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
							"location":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(vloc)+"</p>",
							"capacity":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(vdes)+"</p>",
							"follow_up_details":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.result)+"</p>",
							"next_follow_up_date":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(ht)+"</p>",
							"contact_details":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.mobile_no)+"</p>",
							"followed_by":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
							"contact_person":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.lead_name)+"</p>",
							'll':ll,
							'ee':ee,
							'qq':qq,
							'cc':cc,
							'pp':pp,
							'tt':tt
							})
					else:
						data.append({
							"row":i.idx,
							"lead_temp":i.lead_status,
							"lead_scale":i.lead_scale,
							"lead":i.name,
							"convo_date":convo_format,
							"date":td_format,
							"follow_by":i.contact_by,
							"organization":i.company_name,
							"location":i.location,
							"capacity":i.capacity,
							"follow_up_details":i.result,
							"next_follow_up_date":ht,
							"contact_details":i.mobile_no,
							"followed_by":i.employee_name,
							"contact_person":i.lead_name,
							'll':ll,
							'ee':ee,
							'qq':qq,
							'cc':cc,
							'pp':pp,
							'tt':tt
							})
		return data
	elif(filters.get("reports_type") == 'Status wise'):
		data=[]
		lead=[]
		row=[]
		ref=[]
		ar=[]
		ar2=[]
		query=frappe.db.sql(""" SELECT lr.lead_status,lr.lead_scale,lr.lead_scale,lr.lead_s,lr.enquiry_s,lr.clarification_s,lr.questionnaire_s,lr.pp_meeting,lr.tcp,lt.color,lt.idx,lt.employee_name,lr.taken_date,lr.name,lr.contact_date,lr.city,lr.company_name,lr.status,lt.date,lr.city as location,lr.capacity,lt.mode_of_communication,lr.mobile_no,lr.lead_name,lt.conversation as result from `tabLead` as lr, `tabFollow up` as lt WHERE lt.parent = lr.name and lr.follow_up=1 and %s ORDER BY CAST(lr.lead_scale AS int) DESC"""%(conditions),filters, as_dict=1)
		for i in query:
			if(i.contact_date!=None):
				if(i.contact_date.replace(hour=00,minute=00,second=00,microsecond=00)==datetime.now().replace(hour=00,minute=00,second=00,microsecond=00)):
					ht='<p style="font-color:solidblack"><b>'+(i.contact_date).strftime("%d/%m/%y")+'</b></p>'
				else:
					ht='<p>'+(i.contact_date).strftime("%d/%m/%y")+'</p>'
			else:
				ht="-"
			td_format="-"
			convo_date="-"
			if(i.taken_date!=None):
				td_format=(i.taken_date).strftime("%d/%m/%y")
			if(i.date!=None):
				convo_format=(i.date).strftime("%d/%m/%y")
			

			vdes='-'
			if(i.capacity!=None):
				vdes = i.capacity

			vloc='-'
			if(i.location!=None):
				vloc = i.location

			if(i.lead_s):
				ll='<p>&#10004;</p>'
			else:
				ll='<p>&#9633;</p>'
			
			if(i.enquiry_s):
				ee='<p>&#10004;</p>'
			else:
				ee='<p>&#9633;</p>'
			
			if(i.questionnaire_s):
				qq='<p>&#10004;</p>'
			else:
				qq='<p>&#9633;</p>'
			
			if(i.clarification_s):
				cc='<p>&#10004;</p>'
			else:
				cc='<p>&#9633;</p>'

			
			if(i.pp_meeting):
				pp='<p>&#10004;</p>'
			else:
				pp='<p>&#9633;</p>'
			
			if(i.tcp):
				tt='<p>&#10004;</p>'
			else:
				tt='<p>&#9633;</p>'

			if(i.color == "Green"):
				data.append({
					"row":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.idx)+"</p>",
					"lead_temp":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.lead_status)+"</p>",
					"lead_scale":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.lead_scale)+"</p>",
					"lead":i.name,
					"convo_date":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(convo_format)+"</p>",
					"date":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(td_format)+"</p>",
					"follow_by":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.contact_by)+"</p>",
					"organization":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
					"location":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(vloc)+"</p>",
					"capacity":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(vdes)+"</p>",
					"follow_up_details":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.result)+"</p>",
					"next_follow_up_date":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(ht)+"</p>",
					"contact_details":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.mobile_no)+"</p>",
					"followed_by":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
					"contact_person":"<p style='background:lightgreen;color:black;font-weight:bold;'>"+str(i.lead_name)+"</p>",
					'll':ll,
					'ee':ee,
					'qq':qq,
					'cc':cc,
					'pp':pp,
					'tt':tt
					})
			elif(i.color == "Red"):
				data.append({
					"row":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.idx)+"</p>",
					"lead_temp":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.lead_status)+"</p>",
					"lead_scale":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.lead_scale)+"</p>",
					"lead":i.name,
					"date":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(td_format)+"</p>",
					"convo_date":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.date)+"</p>",
					"follow_by":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.contact_by)+"</p>",
					"organization":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
					"location":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(vloc)+"</p>",
					"capacity":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(vdes)+"</p>",
					"follow_up_details":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.result)+"</p>",
					"next_follow_up_date":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(ht)+"</p>",
					"contact_details":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.mobile_no)+"</p>",
					"followed_by":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
					"contact_person":"<p style='background:#F67280;color:black;font-weight:bold;'>"+str(i.lead_name)+"</p>",
					'll':ll,
					'ee':ee,
					'qq':qq,
					'cc':cc,
					'pp':pp,
					'tt':tt
					})
			elif(i.color == "Yellow"):
				data.append({
					"row":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.idx)+"</p>",
					"lead_temp":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.lead_status)+"</p>",
					"lead_scale":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.lead_scale)+"</p>",
					"lead":i.name,
					"date":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(td_format)+"</p>",
					"convo_date":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.date)+"</p>",
					"follow_by":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.contact_by)+"</p>",
					"organization":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.company_name)+"</p>",
					"location":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(vloc)+"</p>",
					"capacity":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(vdes)+"</p>",
					"follow_up_details":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.result)+"</p>",
					"next_follow_up_date":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(ht)+"</p>",
					"contact_details":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.mobile_no)+"</p>",
					"followed_by":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.employee_name)+"</p>",
					"contact_person":"<p style='background:#D4AF37;color:black;font-weight:bold;'>"+str(i.lead_name)+"</p>",
					'll':ll,
					'ee':ee,
					'qq':qq,
					'cc':cc,
					'pp':pp,
					'tt':tt
					})
			else:
				data.append({
					"row":i.idx,
					"lead_temp":i.lead_status,
					"lead_scale":i.lead_scale,
					"lead":i.name,
					"convo_date":convo_format,
					"date":td_format,
					"follow_by":i.contact_by,
					"organization":i.company_name,
					"location":i.location,
					"capacity":i.capacity,
					"follow_up_details":i.result,
					"next_follow_up_date":ht,
					"contact_details":i.mobile_no,
					"followed_by":i.employee_name,
					"contact_person":i.lead_name,
					'll':ll,
					'ee':ee,
					'qq':qq,
					'cc':cc,
					'pp':pp,
					'tt':tt
					})
		return data
def get_conditions(filters):
	conditions = "lr.docstatus = 0"
	if filters.get("lead_ss"):
		conditions += " and lr.lead_status = %(lead_ss)s"

	match_conditions = build_match_conditions("Lead")
	if match_conditions:
		conditions += " and %s" % match_conditions
	return conditions