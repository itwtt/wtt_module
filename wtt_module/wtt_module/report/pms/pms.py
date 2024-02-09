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
import traceback
def execute(filters=None):

	data = []
	columns = get_columns(filters)
	data = get_data(data , filters)
	return columns, data

def get_columns(filters):
	columns=[
		{
		"label":"Employee Name",
		"fieldtype":"Data",
		"fieldname":"employee_name"
		}
		]
	val=frappe.db.sql("SELECT DISTINCT(month) FROM `tabTechnical Criteria` WHERE YEAR(date)='"+str(filters.year)+"' ",filters,as_dict=1)
	if(filters.category=="Bahavioural"):
		val=frappe.db.sql("SELECT DISTINCT(month) FROM `tabBehavioral Criteria` WHERE YEAR(date)='"+str(filters.year)+"' ",filters,as_dict=1)
	for i in val:
		columns.append({
			"label":i.month,
			"fieldtype":"Data",
			"fieldname":i.month
			})
			  
	return columns

def get_data(data, filters):
	data=[]
	try:
		temp_list=[]
		emp_query = frappe.db.sql("SELECT distinct(employee_name) FROM `tabEmployee` where status='Active' and department!='MD - WTT' and name LIKE 'WTT%' and employee_name not in ('SAMUNDESWARI  R','KRISHNAMOORTHY  C') ORDER BY date_of_joining",as_dict=1)
		
		if(filters.category=="Technical"):
			for emp in emp_query:
				query = frappe.db.sql("""SELECT 
					tc.employee_name as "employee",
					tc.month as "month",
					tc.date as "year",
					ROUND(avg(tc1.your_points/20),2) as "position",
					ROUND(avg(tc2.your_points/20),2) as "industry",
					ROUND(avg(tc3.your_points/20),2) as "common"
					from `tabTechnical Criteria` as tc
					left join `tabPosition Specific` as tc1 ON tc.name=tc1.parent 
					left join `tabIndustry Specific` as tc2 ON tc.name=tc2.parent 
					left join `tabCommon Skills` as tc3 ON tc.name=tc3.parent
					where tc.docstatus=1 and tc.employee_name='"""+str(emp.employee_name)+"""' and YEAR(tc.date)='"""+str(filters.year)+"""'
					group by tc.month order by tc.creation""",as_dict=1)
				if(query):
					column={}
					column["employee_name"]=emp.employee_name
					for i in query:
						if(i.employee==emp.employee_name):
							column[i.month]=round(((i.position+i.industry+i.common)/3),2)
					data.append(column)
		elif(filters.category=="Target"):
			query1 = frappe.db.sql("SELECT distinct(employee_name),employee FROM `tabEmployee` where status='Active' and department!='MD - WTT' and name LIKE 'WTT%' and employee_name not in ('SAMUNDESWARI  R','KRISHNAMOORTHY  C') ORDER BY date_of_joining",as_dict=1)
		
			#TASK POINTS FOR INDIVIDUAL EMPLOYEE
			for i in query1:
				column={}
				column["employee_name"]=i.employee_name
				array=["January","February","March","April","May","June","July","August","September","October","November","December"]
				for mon in array:
					month_name=mon
					year=filters.year
					month_start_time=(datetime.now()).replace(day=1,month=array.index(month_name)+1,year=year,hour=00,minute=00,second=00,microsecond=00)
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
					column[mon]=gg
				data.append(column)
		elif(filters.category=='Behavioural'):
			for emp in emp_query:
				query2 = frappe.db.sql("""SELECT
					bc.employee_name as "employee",
					bc.month as "month",
					bc.date as "year",
					ROUND(avg(bc1.your_points/20),2) as "attitude",
					ROUND(avg(bc2.your_points/20),2) as "personal",
					ROUND(avg(bc3.your_points/20),2) as "team",
					ROUND(avg(bc4.your_points/20),2) as "skill",
					ROUND(avg(bc5.your_points/20),2) as "performance",
					ROUND(avg(bc6.your_points/20),2) as "knowledge"
					from `tabBehavioural Criteria` as bc
					left join `tabAttitude Table` as bc1 ON bc.name=bc1.parent 
					left join `tabPersonal Table` as bc2 ON bc.name=bc2.parent 
					left join `tabTeam Table` as bc3 ON bc.name=bc3.parent
					left join `tabSkill Table` as bc4 ON bc.name=bc4.parent
					left join `tabWork performance` as bc5 ON bc.name=bc5.parent
					left join `tabWork knowledge` as bc6 ON bc.name=bc6.parent
					where bc.docstatus=1 and bc.employee_name='"""+str(emp.employee_name)+"""' and YEAR(bc.date)='"""+str(filters.year)+"""'
					group by bc.month order by bc.creation""",as_dict=1)
				if query2:
					column={}
					column["employee_name"]=emp.employee_name
					for j in query2:
						if(j.employee==emp.employee_name):
							try:j.attitude = float(j.attitude)
							except:j.attitude = 0
							try:j.personal = float(j.personal)
							except:j.personal = 0
							try:j.team = float(j.team)
							except:j.team = 0
							try:j.skill = float(j.skill)
							except:j.skill = 0
							try:j.performance = float(j.performance)
							except:j.performance = 0
							try:j.knowledge = float(j.knowledge)
							except:j.knowledge = 0
							column[j.month]=round(((j.attitude+j.personal+j.team+j.skill+j.performance+j.knowledge)/6),2)

					data.append(column)
	except Exception as e:
		error_message = f"An error occurred: {str(e)} (Line {traceback.extract_tb(e.__traceback__)[0].lineno})"
		frappe.throw(str(error_message))
	
	return data




