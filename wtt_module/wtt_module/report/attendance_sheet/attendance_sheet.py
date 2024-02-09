# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.utils import getdate
from frappe.desk.reportview import build_match_conditions
from datetime import date,datetime,timedelta

def execute(filters):
    data = []
    columns = get_colomns(filters)
    data = get_data(data,filters)
    return columns, data


def get_colomns(filters):
    columns=[
        {"label":"Employee ID","fieldname":"employee","fieldtype":"Link","options":"Employee","width":150},
        {"label":"Employee Name","fieldname":"employee_name","fieldtype":"Data","width":150},
        {"label":"Sunday","fieldname":"sunday","fieldtype":"Data","width":100},
        {"label":"Present","fieldname":"present","fieldtype":"Data","width":100},
        {"label":"Absent","fieldname":"absent","fieldtype":"Data","width":100},
        {"label":"Sunday Worked","fieldname":"sunday_worked","fieldtype":"Data","width":100},
        {"label":"Sick Leave","fieldname":"sick_leave","fieldtype":"Data","width":100},
        {"label":"Casual Leave","fieldname":"casual_leave","fieldtype":"Data","width":100},
        {"label":"Balance Leave","fieldname":"balance_leave","fieldtype":"Data","width":100},
        {"label":"Earned Leave","fieldname":"earned_leave","fieldtype":"Data","width":100},
        {"label":"Loss of Pay","fieldname":"lop","fieldtype":"Data","width":100},
        {"label":"9 - 9:20","fieldname":"late1","fieldtype":"Data","width":100},
        {"label":">9:20","fieldname":"late2","fieldtype":"Data","width":100}
    ]
    return columns

def get_data(data,filters):
    data=[]
    try:
        employee_list = frappe.db.sql("SELECT name as employee,employee_name,branch from `tabEmployee` where status='Active' and department!='MD - WTT' ORDER BY date_of_joining ASC",as_dict=1)
        for i in employee_list:
            columns = {}
            columns["employee"]=i.employee
            columns["employee_name"]=i.employee_name
            # columns["working_days"]=(getdate(filters.to_date)-getdate(filters.from_date)).days+1
            query=frappe.db.sql("SELECT count(name) as present FROM `tabAttendance` WHERE status='Present' and docstatus=1 and employee='"+str(i.employee)+"' and attendance_date between '"+str(filters.from_date)+"' and '"+str(filters.to_date)+"' GROUP BY employee ",as_dict=1)
            present=query[0].present if query else 0

            query=frappe.db.sql("SELECT count(name) as hd FROM `tabAttendance` WHERE status='Half Day' and docstatus=1 and employee='"+str(i.employee)+"' and attendance_date between '"+str(filters.from_date)+"' and '"+str(filters.to_date)+"' GROUP BY employee ",as_dict=1)
            hd=query[0].hd/2 if query else 0
            columns["present"]=present+hd 

            query=frappe.db.sql("SELECT count(name) as sundays FROM `tabAttendance` WHERE docstatus=1 and employee='"+str(i.employee)+"' and DAYNAME(attendance_date)='Sunday' and attendance_date between '"+str(filters.from_date)+"' and '"+str(filters.to_date)+"' GROUP BY employee ",as_dict=1)
            sundays=query[0].sundays if query else 0
            columns["sunday"]=sundays

            query=frappe.db.sql("SELECT count(name) as sundays FROM `tabAttendance` WHERE docstatus=1 and status='Present'and employee='"+str(i.employee)+"' and DAYNAME(attendance_date)='Sunday' and attendance_date between '"+str(filters.from_date)+"' and '"+str(filters.to_date)+"' GROUP BY employee ",as_dict=1)
            sundays_work=query[0].sundays if query else 0
            query=frappe.db.sql("SELECT count(name) as sundays FROM `tabAttendance` WHERE docstatus=1 and status='Half Day'and employee='"+str(i.employee)+"' and DAYNAME(attendance_date)='Sunday' and attendance_date between '"+str(filters.from_date)+"' and '"+str(filters.to_date)+"' GROUP BY employee ",as_dict=1)
            sundays_work+=(query[0].sundays/2) if query else 0
            columns["sunday_worked"]=sundays_work

            query=frappe.db.sql("SELECT count(name) as absent FROM `tabAttendance` WHERE status='Absent' and docstatus=1 and employee='"+str(i.employee)+"' and attendance_date between '"+str(filters.from_date)+"' and '"+str(filters.to_date)+"' GROUP BY employee ",as_dict=1)
            absent=query[0].absent if query else 0
            columns["absent"]=absent+hd-sundays+sundays_work

            sick_leave=0
            casual_leave=0
            earned_leave=0
            balance_leave=0
            leave_query = frappe.db.sql("SELECT distinct(attendance_date) as att_date from `tabAttendance` where  status!='Present' and docstatus=1 and employee='"+str(i.employee)+"' and attendance_date between '"+str(filters.from_date)+"' and '"+str(filters.to_date)+"' ",as_dict=1)
            if(leave_query):
                for jj in leave_query:
                    leave_type_query = frappe.db.sql("SELECT sum(lt.no_of_days) as days_cnt,lt.leave_type from `tabLeave Request`as lr,`tabLeave table` as lt where lt.parent=lr.name and lr.employee='"+str(i.employee)+"' and lt.from_date='"+str(jj.att_date)+"' and lr.docstatus=1 GROUP BY lt.leave_type ",as_dict=1)
                    if(leave_type_query):
                        for ii in leave_type_query:
                            if(ii.leave_type=="Sick Leave"):
                                sick_leave+=ii.days_cnt
                            elif(ii.leave_type=="Casual Leave"):
                                casual_leave+=ii.days_cnt
                            elif(ii.leave_type=="Balance Leave"):
                                balance_leave+=ii.days_cnt
                            elif(ii.leave_type=="Earned Leave"):
                                earned_leave+=ii.days_cnt

            columns["sick_leave"]=sick_leave
            columns["casual_leave"]=casual_leave
            columns["earned_leave"]=earned_leave
            columns["balance_leave"]=balance_leave
            columns["lop"]=(absent+hd-sundays+sundays_work)-(sick_leave+casual_leave+earned_leave+balance_leave) if ((sick_leave+casual_leave+earned_leave+balance_leave)<=(absent+hd-sundays+sundays_work)) else (sick_leave+casual_leave+earned_leave+balance_leave)-(absent+hd-sundays+sundays_work)
            late1=0
            late2=0
            tt_tt=getdate(filters.from_date)
            to_to=getdate(filters.to_date)
            while (tt_tt <= to_to):
                tt_tt += timedelta(days=1)
                tt=str(getdate(filters.from_date))+" 09:20:00"
                late1_query = frappe.db.sql("SELECT * from `tabAttendance` where employee='"+str(i.employee)+"' and attendance_date='"+str(tt_tt)+"' and in_time>'"+str(tt)+"' and status='Present' and late_entry=1 ",as_dict=1)
                late2_query = frappe.db.sql("SELECT * from `tabAttendance` where employee='"+str(i.employee)+"' and attendance_date='"+str(tt_tt)+"' and in_time<='"+str(tt)+"' and status='Present' and late_entry=1 ",as_dict=1)
                late1=late1+1 if late1_query else late1
                late2=late2+1 if late2_query else late2
            columns["late1"]=late1
            columns["late2"]=late2





            data.append(columns)
    except Exception as e:
        frappe.msgprint(str(e))
    return data

# def get_conditions(filters):
#     conditions = ""
#     if filters.get("from_date"):
#         conditions += " AND attendance_date>='%s'" % filters.get('from_date')
#     if filters.get("to_date"):
#         conditions += " AND attendance_date>='%s'" % filters.get('to_date')
#     return conditions

