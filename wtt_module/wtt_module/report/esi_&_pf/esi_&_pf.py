# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from datetime import datetime,timedelta,date
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
    data = []
    columns = get_columns(filters)
    data = get_data(data,filters)
    return columns, data

def get_columns(filters):
    
    columns=[
        {
        "label":"Employee Name",
        "fieldtype":"Data",
        "fieldname":"employee_name",
        "width":150
        },
        {
        "label":"ESI Number",
        "fieldtype":"Data",
        "fieldname":"esi_no",
        "width":70
        },
        {
        "label":"UAN Number",
        "fieldtype":"Data",
        "fieldname":"uan_no",
        "width":70
        },
        {
        "label":"Gross Fixed",
        "fieldtype":"Currency",
        "fieldname":"gross_fixed",
        "width":100
        },
        {
        "label":"PF Wages fixed",
        "fieldtype":"Currency",
        "fieldname":"pf_wages_fixed",
        "width":100
        },
        {
        "label":"Payment Days",
        "fieldtype":"Float",
        "fieldname":"payment_days",
        "width":70
        },
        {
        "label":"Actual Gross",
        "fieldtype":"Currency",
        "fieldname":"actual_gross",
        "width":100
        },
        {
        "label":"Actual PF Wages",
        "fieldtype":"Currency",
        "fieldname":"actual_pf_wages",
        "width":100
        },
        {
        "label":"Employee ESI",
        "fieldtype":"Currency",
        "fieldname":"employee_esi",
        "width":120
        },
        {
        "label":"Employer ESI",
        "fieldtype":"Currency",
        "fieldname":"employer_esi",
        "width":120
        },
        {
        "label":"Employee EPF",
        "fieldtype":"Currency",
        "fieldname":"employee_epf",
        "width":120
        },
        {
        "label":"Employer EPF",
        "fieldtype":"Currency",
        "fieldname":"employer_epf",
        "width":120
        },
        {
        "label":"Total ESI",
        "fieldname":"total_esi",
        "fieldtype":"Currency",
        "width":100
        },
        {
        "label":"Total EPF",
        "fieldname":"total_epf",
        "fieldtype":"Currency",
        "width":100
        },
        {
        "label":"Total",
        "fieldname":"total",
        "fieldtype":"Currency",
        "width":100
        }
    ]
    
    return columns
def get_data(data,filters):
    data=[]
    yy=filters.year
    aa=filters.month
    mm=datetime.strptime(aa, '%B').month
    date1=date.today().replace(day=1,month=mm,year=yy)
    date3=(date1+timedelta(days=32)).replace(day=1)
    date2=date3-timedelta(days=1)
    total_days=(date3-date1).days
    # frappe.msgprint(str(date2))

    query=frappe.db.sql("SELECT name,employee_name,uan_no,esi_no,gross_amount,esi,pf FROM `tabEmployee` WHERE status='Active' and name not in ('WTT001','WTT002','WTT003') ",as_dict=1)
    if(filters.branch!=None):
        query=frappe.db.sql("SELECT name,employee_name,uan_no,esi_no,gross_amount,esi,pf FROM `tabEmployee` WHERE status='Active' and name not in ('WTT001','WTT002','WTT003') and branch='"+str(filters.branch)+"' ",as_dict=1)
    column={}
    for i in query:
        if(i.esi=='Yes' or i.pf=='Yes'):
            esi=frappe.db.sql("SELECT sum(sldt.amount)as amt,sldt.salary_component from `tabSalary Slip` as sl,`tabSalary Detail` as sldt WHERE sl.name=sldt.parent and sl.docstatus!=2 and sl.workflow_state!='Rejected' and sl.employee='"+str(i.name)+"' and sl.posting_date='"+str(date2)+"' and sldt.salary_component='ESI' ",as_dict=1)
            pf=frappe.db.sql("SELECT sum(sldt.amount)as amt,sldt.salary_component from `tabSalary Slip` as sl,`tabSalary Detail` as sldt WHERE sl.name=sldt.parent and sl.docstatus!=2 and sl.workflow_state!='Rejected' and sl.employee='"+str(i.name)+"' and sl.posting_date='"+str(date2)+"' and sldt.salary_component='Provident Fund' ",as_dict=1)
            salary_structure_assignment=frappe.db.get_value("Salary Structure Assignment",{"employee":i.name,"docstatus":1},"salary_structure")
            gross=0
            pf_wages=0
            for sal in frappe.db.sql("SELECT sldt.amount,sldt.salary_component from `tabSalary Detail`as sldt,`tabSalary Structure`as ss WHERE ss.name=sldt.parent and ss.name='"+str(salary_structure_assignment)+"' and sldt.salary_component in ('Basic Salary','House Rent Allowance','Other Allowance') ",as_dict=1):
                gross+=sal.amount
                if(sal.salary_component!='House Rent Allowance'):
                    if(i.name=="WTT1373"):
                        if(sal.salary_component!='Other Allowance'):
                            pf_wages+=sal.amount
                    else:
                        pf_wages+=sal.amount

            payment_days=frappe.db.get_value("Salary Slip",{"employee":i.name},"payment_days")
            salary_slip=frappe.db.get_value("Salary Slip",{"employee":i.name},"name")

            gross_paid=0
            pf_wages_paid=0
            for sal in frappe.db.sql("SELECT sldt.amount,sldt.salary_component from `tabSalary Detail`as sldt,`tabSalary Slip`as ss WHERE ss.name=sldt.parent and ss.name='"+str(salary_slip)+"' and sldt.salary_component in ('Basic Salary','House Rent Allowance','Other Allowance') and ss.posting_date='"+str(date2)+"' ",as_dict=1):
                gross_paid+=sal.amount
                if(sal.salary_component!='House Rent Allowance'):
                    if(i.name=="WTT1373"):
                        if(sal.salary_component!='Other Allowance'):
                            pf_wages_paid+=sal.amount
                    else:
                        pf_wages_paid+=sal.amount
            
            emp_esi=gross_paid*0.0325
            emp_epf=pf_wages_paid*0.13
            if(pf_wages_paid>15000):
                emp_epf=15000*0.13
            if(i.esi=="No"):
                emp_esi=0
            if(i.pf=="No"):
                emp_epf=0
            if(esi[0]["amt"]==None):
                esi[0]["amt"]=0
            if(pf[0]["amt"]==None):
                pf[0]["amt"]=0
            if(salary_slip!=None):
                data.append({
                    "employee_name":i.employee_name,
                    "esi_no":i.esi_no,
                    "uan_no":i.uan_no,
                    "gross_fixed":round(gross),
                    "pf_wages_fixed":round(pf_wages),
                    "actual_gross":round(gross_paid),
                    "actual_pf_wages":round(pf_wages_paid),
                    "payment_days":payment_days,
                    "employee_esi":round(esi[0]["amt"]),
                    "employee_epf":round(pf[0]["amt"]),
                    "employer_esi":round(emp_esi),
                    "employer_epf":round(emp_epf),
                    "total_esi":round(esi[0]["amt"]+emp_esi),
                    "total_epf":round(pf[0]["amt"]+emp_epf),
                    "total":round(esi[0]["amt"]+pf[0]["amt"]+emp_epf+emp_esi)
                    })

    return data