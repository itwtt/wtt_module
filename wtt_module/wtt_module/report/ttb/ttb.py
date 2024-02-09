# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
import json
import itertools
from datetime import date,datetime,timedelta
from frappe.utils import getdate
def execute(filters=None):

	data = []
	columns = get_columns(filters)
	data = get_data(data , filters)
	return columns, data

def get_columns(filters):
	columns=[]

	if(filters.pending_emp):
		columns=[
		{
		"label": _("Technical"),
		"fieldtype": "Data",
		"fieldname": "technical",
		"width": 200
		},
		{
		"label": _("Behavioral"),
		"fieldtype": "Data",
		"fieldname": "behavioral",
		"width": 200
		}
		]

	elif(filters.employee==None):
		if(filters.avg==1):
			columns=[
				{
				"label":"Employee Name",
				"fieldtype":"Data",
				"fieldname":"employee_name"
				}
				]
			val=frappe.db.sql("SELECT DISTINCT(month) FROM `tabTechnical Criteria` ",filters,as_dict=1)
			for i in val:				
				columns.append({
					"label":"Target",
					"fieldtype":"Data",
					"fieldname":i.month+"target"
					})
				columns.append({
					"label":"Technical",
					"fieldtype":"Data",
					"fieldname":i.month+"technical"
					})
				columns.append({
					"label":"Behavioural",
					"fieldtype":"Data",
					"fieldname":i.month+"behavioral"
					})
				columns.append({
					"fieldname": i.month,
					"label": i.month,
					"fieldtype": "Data",
					"width": 100
					})
		else:
			columns=[
			
			{
			"label": _("Employee"),
			"fieldtype": "HTML",
			"fieldname": "employee_name",
			"width": 160
			},
			{
			"label": _("<p style='color:green'>Task</p>"),
			"fieldtype": "HTML",
			"fieldname": "a1",
			"width": 100
			},
			{
			"label": _("<p style='color:indigo'>Position</p>"),
			"fieldtype": "HTML",
			"fieldname": "b1",
			"width": 80
			},
			{
			"label": _("<p style='color:indigo'>Industry</p>"),
			"fieldtype": "HTML",
			"fieldname": "b2",
			"width": 80
			},
			{
			"label": _("<p style='color:indigo'>Common</p>"),
			"fieldtype": "HTML",
			"fieldname": "b3",
			"width": 80
			},
			{
			"label": _("<p style='color:orange'>Attitude</p>"),
			"fieldtype": "HTML",
			"fieldname": "c1",
			"width":80
			},
			{
			"label": _("<p style='color:orange'>Personal</p>"),
			"fieldtype": "HTML",
			"fieldname": "c2",
			"width": 80
			},
			{
			"label": _("<p style='color:orange'>Skill</p>"),
			"fieldtype": "HTML",
			"fieldname": "c3",
			"width": 80
			},
			{
			"label": _("<p style='color:orange'>Team</p>"),
			"fieldtype": "HTML",
			"fieldname": "c4",
			"width": 80
			},
			{
			"label": _("<p style='color:orange'>Knowledge</p>"),
			"fieldtype": "HTML",
			"fieldname": "c5",
			"width": 80
			},
			{
			"label": _("<p style='color:orange'>Performance</p>"),
			"fieldtype": "HTML",
			"fieldname": "c6",
			"width": 80
			},
			{
			"label": _('Total'),
			"fieldtype": "HTML",
			"fieldname": "total",
			"width": 80
			},

		]
			  
	return columns

def get_data(data, filters):
	data=[]
	temp_list=[]
	column={}

	if(filters.pending_emp==1):
		list1=[]
		list2=[]
		list3=[]
		ar1=[]
		ar2=[]
		for i in frappe.db.sql("SELECT name FROM `tabEmployee` WHERE status='Active' and employee!='WTT917' AND employee!='WTT915' AND department!='MD - WTT' AND department!='House keeping - WTT'",as_dict=1):
			list1.append(i.name)
		for i in frappe.db.sql("SELECT DISTINCT(employee) FROM `tabTechnical Criteria` WHERE month=%(month)s and year=%(year)s",filters,as_dict=1):
			list2.append(i.employee)
		for i in frappe.db.sql("SELECT DISTINCT(employee) FROM `tabBehavioural Criteria` WHERE month=%(month)s and year=%(year)s",filters,as_dict=1):
			list3.append(i.employee)
		column1={}
		column2={}
		for j in list1:
			if(j not in list2):
				ar1.append(frappe.db.get_value("Employee",j,"employee_name"))

			if(j not in list3):
				ar2.append(frappe.db.get_value("Employee",j,"employee_name"))

		for (a1,a2) in itertools.zip_longest(ar1,ar2):
			data.append({
				"technical":a1,
				"behavioral":a2
				})

	elif(filters.employee==None):
		query1 = frappe.db.sql("SELECT distinct(employee_name),employee FROM `tabEmployee` where status='Active' and department!='MD - WTT' and name LIKE 'WTT%' and employee_name not in ('SAMUNDESWARI  R','KRISHNAMOORTHY  C') ORDER BY date_of_joining",as_dict=1)
		
		#TASK POINTS FOR INDIVIDUAL EMPLOYEE
		for i in query1:
			array=["","January","February","March","April","May","June","July","August","September","October","November","December"]
			month_name=filters.month
			year=filters.year
			month_start_time=(datetime.now()).replace(day=1,month=array.index(month_name),year=year,hour=00,minute=00,second=00,microsecond=00)
			cc=month_start_time+timedelta(days=32)
			dd=cc.replace(day=1)
			month_end_time=dd-timedelta(seconds=1)

			task=[]
			task_doc=[]
			for task_p in frappe.db.sql("SELECT DISTINCT(name) FROM `tabTask Allocation` WHERE employee='"+str(i.employee)+"' and workflow_state NOT IN ('Cancelled','Rejected') ",as_dict=1):
				task_doc.append(task_p.name)
			for parent in task_doc:
				for gp in frappe.db.sql("SELECT gained_points FROM `tabWork Update` WHERE parent='"+str(parent)+"' and from_time>='"+str(month_start_time)+"' and to_time<='"+str(month_end_time)+"' ",as_dict=1):
					task.append(gp.gained_points)
			completed =[i.count for i in frappe.db.sql("SELECT count(DISTINCT(wu.name))as count FROM `tabTask Allocation`as ta,`tabWork Update` as wu WHERE ta.name=wu.parent and wu.status='Completed' and ta.workflow_state NOT IN ('Cancelled','Rejected') and ta.employee='"+str(i.employee)+"' and wu.from_time>='"+str(month_start_time)+"' and wu.to_time<='"+str(month_end_time)+"'",as_dict=1)]
			pending = [i.count for i in frappe.db.sql("SELECT count(DISTINCT(wu.name))as count FROM `tabTask Allocation`as ta,`tabWork Update` as wu WHERE ta.name=wu.parent and wu.status!='Completed' and ta.workflow_state NOT IN ('Cancelled','Rejected') and ta.employee='"+str(i.employee)+"' and wu.from_time>='"+str(month_start_time)+"' and wu.to_time<='"+str(month_end_time)+"'",as_dict=1)]

			total_task=len(task)
			if(len(task)>0):
				grade= (sum(task)/(len(task)*100))*5
			else:
				grade=0


			# AVERAGE POINTS FOR TASK ALLOCATED
			gg=0
			if(grade<0):
				gg=0
			elif(grade>5):
				gg=5
			else:
				gg=str(round(grade,2))
			
			column={}
			hod_row={}
			manag_row={}
			query = frappe.db.sql("""SELECT 
				tc.employee_name as "employee",
				tc.month as "month",
				tc.date as "year",
				ROUND(avg(tc1.your_points/20),2) as "position",
				ROUND(avg(tc2.your_points/20),2) as "industry",
				ROUND(avg(tc3.your_points/20),2) as "common",
				ROUND(avg(tc1.hod_points/20),2) as "position1",
				ROUND(avg(tc2.hod_points/20),2) as "industry1",
				ROUND(avg(tc3.hod_points/20),2) as "common1",
				ROUND(avg(tc1.management_points/20),2) as "position3",
				ROUND(avg(tc2.management_points/20),2) as "industry3",
				ROUND(avg(tc3.management_points/20),2) as "common3"
				from `tabTechnical Criteria` as tc
				left join `tabPosition Specific` as tc1 ON tc.name=tc1.parent 
				left join `tabIndustry Specific` as tc2 ON tc.name=tc2.parent 
				left join `tabCommon Skills` as tc3 ON tc.name=tc3.parent
				where tc.docstatus=1 and tc.employee_name='"""+str(i.employee_name)+"""' and YEAR(tc.date)='"""+str(filters.year)+"""' and tc.month='"""+str(filters.month)+"""'
				group by tc.month order by tc.creation""",as_dict=1)
			query2 = frappe.db.sql("""SELECT
				bc.employee_name as "employee",
				bc.month as "month",
				bc.date as "year",
				ROUND(avg(bc1.your_points/20),2) as "attitude",
				ROUND(avg(bc2.your_points/20),2) as "personal",
				ROUND(avg(bc3.your_points/20),2) as "team",
				ROUND(avg(bc4.your_points/20),2) as "skill",
				ROUND(avg(bc5.your_points/20),2) as "performance",
				ROUND(avg(bc6.your_points/20),2) as "knowledge",
				ROUND(avg(bc1.hod_points/20),2) as "attitude1",
				ROUND(avg(bc2.hod_points/20),2) as "personal1",
				ROUND(avg(bc3.hod_points/20),2) as "team1",
				ROUND(avg(bc4.hod_points/20),2) as "skill1",
				ROUND(avg(bc5.hod_points/20),2) as "performance1",
				ROUND(avg(bc6.hod_points/20),2) as "knowledge1",
				ROUND(avg(bc1.management_points/20),2) as "attitude2",
				ROUND(avg(bc2.management_points/20),2) as "personal2",
				ROUND(avg(bc3.management_points/20),2) as "team2",
				ROUND(avg(bc4.management_points/20),2) as "skill2",
				ROUND(avg(bc5.management_points/20),2) as "performance2",
				ROUND(avg(bc6.management_points/20),2) as "knowledge2"
				from `tabBehavioural Criteria` as bc
				left join `tabAttitude Table` as bc1 ON bc.name=bc1.parent 
				left join `tabPersonal Table` as bc2 ON bc.name=bc2.parent 
				left join `tabTeam Table` as bc3 ON bc.name=bc3.parent
				left join `tabSkill Table` as bc4 ON bc.name=bc4.parent
				left join `tabWork performance` as bc5 ON bc.name=bc5.parent
				left join `tabWork knowledge` as bc6 ON bc.name=bc6.parent
				where bc.docstatus=1 and bc.employee_name='"""+str(i.employee_name)+"""' and YEAR(bc.date)='"""+str(filters.year)+"""' and bc.month='"""+str(filters.month)+"""'
				group by bc.month order by bc.creation""",as_dict=1)
			if(query or query2):
				column["employee_name"]=i.employee_name
				column["a1"]=gg
				column["total"]=0
				hod_row["employee_name"]="HOD"
				hod_row["a1"]="Total - "+str(total_task)
				hod_row["total"]=0
				manag_row["employee_name"]="Management"
				manag_row["a1"]="Comp - "+str(completed)
				manag_row["total"]=0
				for tech in query:
					if(i.employee_name==tech.employee):
						column["b1"]=tech.position
						column["b2"]=tech.industry
						column["b3"]=tech.common
						column["total"]=round(((tech.position+tech.industry+tech.common)/3),2)
						hod_row["b1"]=tech.position1
						hod_row["b2"]=tech.industry1
						hod_row["b3"]=tech.common1
						hod_row["total"]=round(((tech.position1+tech.industry1+tech.common1)/3),2)
						manag_row["b1"]=tech.position3
						manag_row["b2"]=tech.industry3
						manag_row["b3"]=tech.common3
						manag_row["total"]=round(((tech.position3+tech.industry3+tech.common3)/3),2)
				for beh in query2:
					if(i.employee_name==beh.employee):
						column["c1"]=beh.attitude
						column["c2"]=beh.personal
						column["c3"]=beh.team
						column["c4"]=beh.skill
						column["c5"]=beh.knowledge
						column["c6"]=beh.performance
						column["total"]=round(((float(column["total"])+((beh.attitude+beh.personal+beh.team+beh.skill+beh.knowledge+beh.performance)/6))/2),2)
						hod_row["c1"]=beh.attitude1
						hod_row["c2"]=beh.personal1
						hod_row["c3"]=beh.team1
						hod_row["c4"]=beh.skill1
						hod_row["c5"]=beh.knowledge1
						hod_row["c6"]=beh.performance1
						hod_row["total"]=round(((float(hod_row["total"])+((beh.attitude1+beh.personal1+beh.team1+beh.skill1+beh.knowledge1+beh.performance1)/6))/2),2)
						manag_row["c1"]=beh.attitude2
						manag_row["c2"]=beh.personal2
						manag_row["c3"]=beh.team2
						manag_row["c4"]=beh.skill2
						manag_row["c5"]=beh.knowledge2
						manag_row["c6"]=beh.performance2
						manag_row["total"]=round(((float(manag_row["total"])+((beh.attitude2+beh.personal2+beh.team2+beh.skill2+beh.knowledge2+beh.performance2)/6))/2),2)
				data.append(column)
				data.append(hod_row)
				data.append(manag_row)
				data.append({})
	return data




