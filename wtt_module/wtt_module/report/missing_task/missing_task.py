# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime,date,timedelta


def execute(filters=None):
	columns, data = getcolumns(filters), getdata(filters)
	return columns, data

def getcolumns(filters):
	columns=[
		{
		"label":"Employee Name",
		"fieldname":"employee_name",
		"fieldtype":"Data",
		"width":150
		},
		{
		"label":"Date",
		"fieldtype":"HTML",
		"fieldname":"date",
		"width":100
		},
		{
		"label":"Attendance",
		"fieldtype":"HTML",
		"fieldname":"attendance",
		"width":100
		},
		{
		"label":"Task",
		"fieldname":"task",
		"fieldtype":"HTML",
		"width":100
		}
	]
	return columns

def getdata(filters):
	data=[]
	if(filters.from_date==None):
		filters.from_date=date.today().replace(day=1,month=2)
	if(filters.to_date==None):
		filters.to_date=date.today()


	query=frappe.db.sql("""SELECT 
		`tabAttendance`.`employee_name`,`tabAttendance`.`status`,`tabAttendance`.`employee` ,`tabAttendance`.`attendance_date`
		FROM `tabAttendance` INNER JOIN `tabEmployee` ON `tabAttendance`.`employee`=`tabEmployee`.`name`
		WHERE 
		`tabEmployee`.`status`='Active' and
		`tabAttendance`.`attendance_date`>='"""+str(filters.from_date)+"""' and 
		`tabAttendance`.`attendance_date`<='"""+str(filters.to_date)+"""' and 
		`tabAttendance`.`docstatus`=1 and `tabAttendance`.`status`!='Absent'
		""",as_dict=1)
	for i in query:
		query_1=frappe.db.sql("SELECT * FROM `tabWork Update`as wu,`tabTask Allocation`as ta WHERE wu.parent=ta.name and ta.employee='"+str(i.employee)+"' and ta.docstatus!=2 and ta.workflow_state!='Rejected' and wu.from_time<='"+str(filters.from_date)+" 00:00:00' and wu.to_time>='"+str(filters.to_time)+" 00:00:00' ",as_dict=1)
		if not query_1:
			data.append({
				"employee_name":i.employee_name,
				"date":i.attendance_date,
				"attendance":i.status,
				"task":"No"
				})

	return data