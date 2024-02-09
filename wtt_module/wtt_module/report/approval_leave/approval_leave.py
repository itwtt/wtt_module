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
            "width": 150,
            "frozen":True
        }
    ]
    d4=str(filters.from_date)
    d5=str(filters.to_date)
    d1=datetime.strptime(d4,"%Y-%m-%d")
    d2=datetime.strptime(d5,"%Y-%m-%d")
    delta=timedelta(days=1)
    while d1<=d2:
        val=d1.strftime("%Y-%m-%d")
        go=str(val)
        gg=d1.strftime("%d")
        gk=str(gg)
        columns.append({
            "fieldname":go+"date",
            "label": gk,
            "fieldtype":"Data",
            "width": 80
        })
        d1=d1+delta
    return columns
def get_data(conditions,data,filters):
    data=[]
    date=[]
    ref_date=[]
    emp=[]
    query=frappe.db.sql(""" select lr.employee, lr.employee_name,lr.department,lr.workflow_state,
        lt.from_date,lt.to_date,
        lt.day,lt.no_of_days,lt.leave_type,lt.explanation
        from `tabLeave table` as lt, `tabLeave Request` as lr 
        where
        lt.parent = lr.name and lt.status='Approved' and  
        %s order by lt.employee"""%(conditions), filters, as_dict=1)
    
    items_dict = {}
    temp_list = []
    for item in query:
        temp_list.append(item.employee)
    unique_item = set(temp_list)

    for item in unique_item:
        column = {}
        for datum in query:
            if item == datum.employee:
                if(datum.leave_type=="Eligible Leave"):
                    el="EL"
                elif(datum.leave_type=="Leave Without Pay"):
                    el="LOP"
                elif(datum.leave_type=="Sick Leave"):
                    el="SL"
                elif(datum.leave_type=="Emergency Leave"):
                    el="EML"
                elif(datum.leave_type=="Balance Leave"):
                    el="BL"
                elif(datum.leave_type=="Casual Leave"):
                    el="CL"
                column["employee_name"]=datum.employee_name
                column[str(datum.from_date)+'date']=el
                column[str(datum.to_date)+'date']=el
        data.append(column)
    return data

def get_conditions(filters):
    conditions = "lr.docstatus = 0"
    if filters.get("from_date"):
        conditions += " and lt.from_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and lt.to_date <= %(to_date)s"
    if filters.get("emp"):
        conditions += " and lr.employee = %(emp)s"

    match_conditions = build_match_conditions("Leave Request")
    if match_conditions:
        conditions += " and %s" % match_conditions
    return conditions