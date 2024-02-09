from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from datetime import datetime,timedelta
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
    if not filters:
        return [], []
    data = []
    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(conditions,data,filters)
    return columns, data

def get_columns(filters):
    columns=[
        
        {
            "label": _("Employee Name"),
            "fieldtype": "Data",
            "fieldname": "employee_name",
            "width": 150
        }
    ]
    d4=str(filters.from_date)
    d5=str(filters.to_date)
    d1=datetime.strptime(d4,"%Y-%m-%d")
    d2=datetime.strptime(d5,"%Y-%m-%d")
    delta=timedelta(days=1)
    while d1<=d2:
        val=d1.strftime("%Y-%m-%d")
        vaal=d1.strftime("%d")
        go=str(val)
        gog=str(vaal)
        columns.append({
            "fieldname":go+"date",
            "label": go,
            "fieldtype":"Data",
            "width": 180
        })
        d1=d1+delta
    return columns
def get_data(conditions,data,filters):
    data=[]
    date=[]
    ref_date=[]
    emp=[]
    query=frappe.db.sql(""" select employee,employee_name,department,attendance_date,
        in_time,out_time,working_hours,status from `tabAttendance` where status!='Absent' and %s order by employee"""%(conditions), filters, as_dict=1)
    
    items_dict = {}
    temp_list = []
    for item in query:
        temp_list.append(item.employee)
    unique_item = set(temp_list)

    for item in unique_item:
        column = {}
        for datum in query:
            if item == datum.employee:
                column["employee_name"]=datum.employee_name
                if(str(datum.in_time)!="None"):
                    vis=str(datum.in_time)
                    gug=datetime.strptime(vis,"%Y-%m-%d %H:%M:%S")
                    sri=gug.strftime("%H:%M:%S")
                else:
                    sri="-"
                if(str(datum.out_time)!="None"):
                    vug=str(datum.out_time)
                    guv=datetime.strptime(vug,"%Y-%m-%d %H:%M:%S")
                    nu=guv.strftime("%H:%M:%S")
                else:
                    nu="-"
                
                column[str(datum.attendance_date)+'date']=str(sri)+" "+str(nu)+" "+" "+" Hours "+str(datum.working_hours)
                
        data.append(column)
    return data

def get_conditions(filters):
    conditions = "docstatus = 1"
    if filters.get("from_date"):
        conditions += " and attendance_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and attendance_date <= %(to_date)s"
    if filters.get("emp"):
        conditions += " and employee = %(emp)s"

    match_conditions = build_match_conditions("Attendance")
    if match_conditions:
        conditions += " and %s" % match_conditions
    return conditions