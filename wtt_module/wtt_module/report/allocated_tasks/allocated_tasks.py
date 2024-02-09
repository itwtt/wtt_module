from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from datetime import datetime,timedelta
from frappe.desk.reportview import build_match_conditions
from frappe.utils import getdate

def execute(filters=None):
    if not filters:
        return [], []
    data = []
    columns = get_columns(filters)
    data = get_data(data,filters)
    return columns, data

def get_columns(filters):
    if(filters.report_type=='Task List'):
        columns=[
            {
                "label": _("Employee Name"),
                "fieldtype": "Data",
                "fieldname": "employee_name",
                "width": 150
            },
            {
                "label": _("Department"),
                "fieldtype": "Data",
                "fieldname": "department",
                "width": 150
            },
            # {
            #     "label": _("Assigned Date"),
            #     "fieldtype": "Data",
            #     "fieldname": "assigned_date",
            #     "width": 100
            # },
            # {
            #     "label": _("Expected Date"),
            #     "fieldtype": "Data",
            #     "fieldname": "expected_date",
            #     "width": 100
            # },
            {
                "label": _("Task"),
                "fieldtype": "Data",
                "fieldname": "task",
                "width": 200
            },
            {
                "label": _("Task Description"),
                "fieldtype": "Data",
                "fieldname": "task_description",
                "width": 250
            },
            {
                "label": _("Allocated Points"),
                "fieldtype": "Float",
                "fieldname": "points_allocated",
                "width": 100
            },
            {
                "label": _("Gained Points"),
                "fieldtype": "Float",
                "fieldname": "points_gained",
                "width": 100
            },
            {
                "label": _("Status"),
                "fieldtype": "Data",
                "fieldname": "status",
                "width": 100
            }

        ]
        
    elif(filters.report_type=='Employee Points'):
        columns=[
            {
                "label": _("Employee Name"),
                "fieldtype": "Data",
                "fieldname": "employee_name",
                "width": 150
            },
            {
                "label": _("Allocated Tasks"),
                "fieldtype": "Data",
                "fieldname": "allocated_tasks",
                "width": 150
            },
            {
                "label": _("Allocated Points"),
                "fieldtype": "Float",
                "fieldname": "points_allocated",
                "width": 150
            },
            {
                "label": _("Gained Points"),
                "fieldtype": "Float",
                "fieldname": "points_gained",
                "width": 150
            },
            {
                "label": _("Bonus Points"),
                "fieldtype": "Float",
                "fieldname": "bonus",
                "width": 150
            },
            {
                "label": _("Grade"),
                "fieldtype": "Float",
                "fieldname": "grade",
                "width": 80
            }

        ]
        
    elif(filters.report_type=='Department Points'):
        columns=[
            {
                "label": _("Department"),
                "fieldtype": "Data",
                "fieldname": "department",
                "width": 150
            },
            {
                "label": _("Allocated Tasks"),
                "fieldtype": "Data",
                "fieldname": "allocated_tasks",
                "width": 150
            },
            {
                "label": _("Allocated Points"),
                "fieldtype": "Float",
                "fieldname": "points_allocated",
                "width": 150
            },
            {
                "label": _("Gained Points"),
                "fieldtype": "Float",
                "fieldname": "points_gained",
                "width": 150
            },
            {
                "label": _("Bonus Points"),
                "fieldtype": "Float",
                "fieldname": "bonus",
                "width": 150
            },
            {
                "label": _("Grade"),
                "fieldtype": "Float",
                "fieldname": "grade",
                "width": 80
            }

        ]
    
    return columns
def get_data(data,filters):
    data=[]
    emp=[]
    lst=[]
    if(filters.report_type=='Task List'):
        if(filters.employee==None):
            if(filters.status!=None):
                if(filters.department==None):
                    query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assigned_date,bb.status,bb.to_time,bb.type_of_work,bb.description,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and bb.status!=%(status)s ORDER BY aa.employee_name",filters,as_dict=1)
                else:
                    query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assigned_date,bb.status,bb.to_time,bb.type_of_work,bb.description,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and bb.status!=%(status)s and aa.department=%(department)s ORDER BY aa.employee_name",filters,as_dict=1)
            else:
                if(filters.department==None):
                    query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assigned_date,bb.status,bb.to_time,bb.type_of_work,bb.description,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s ORDER BY aa.employee_name",filters,as_dict=1)
                else:
                    query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assigned_date,bb.status,bb.to_time,bb.type_of_work,bb.description,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.department=%(department)s ORDER BY aa.employee_name",filters,as_dict=1)
        else:
            if(filters.status!=None):
                if(filters.department==None):
                    query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assigned_date,bb.status,bb.to_time,bb.type_of_work,bb.description,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.employee=%(employee)s and bb.status!=%(status)s ORDER BY aa.employee_name",filters,as_dict=1)
                else:
                    query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assigned_date,bb.status,bb.to_time,bb.type_of_work,bb.description,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.employee=%(employee)s and bb.status!=%(status)s and aa.department=%(department)s ORDER BY aa.employee_name",filters,as_dict=1)
            else:
                if(filters.department==None):
                    query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assigned_date,bb.status,bb.to_time,bb.type_of_work,bb.description,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.employee=%(employee)s ORDER BY aa.employee_name",filters,as_dict=1)
                else:
                    query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.assigned_date,bb.status,bb.to_time,bb.type_of_work,bb.description,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.employee=%(employee)s and aa.department=%(department)s ORDER BY aa.employee_name",filters,as_dict=1)
        for i in query:
            if(i.description==None):
                var="-"
            else:
                var=i.description
            if(i.employee_name not in emp):
                emp.append(i.employee_name)
                data.append({
                    "employee_name":i.employee_name,
                    "assigned_date":getdate(i.assigned_date).strftime("%d-%m-%Y"),
                    "department":i.department,
                    "expected_date": getdate(i.to_time).strftime("%d-%m-%Y"),
                    "task":i.type_of_work,
                    "task_description":var,
                    "points_allocated":i.total_points,
                    "points_gained":i.gained_points,
                    "status":i.status
                    })
            else:
                data.append({
                    "assigned_date":getdate(i.assigned_date).strftime("%d-%m-%Y"),
                    "expected_date": getdate(i.to_time).strftime("%d-%m-%Y"),
                    "task":i.type_of_work,
                    "task_description":var,
                    "points_allocated":i.total_points,
                    "points_gained":i.gained_points,
                    "status":i.status
                    })
            
    elif(filters.report_type=='Employee Points'):
        
        t_d=[]
        if(filters.employee==None):            
            if(filters.department==None):
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s ORDER BY bb.gained_points DESC",filters,as_dict=1)
            else:
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.department=%(department)s ORDER BY bb.gained_points DESC",filters,as_dict=1)
                    
        else:            
            if(filters.department==None):
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.employee=%(employee)s ORDER BY bb.gained_points DESC",filters,as_dict=1)
            else:
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.employee=%(employee)s and aa.department=%(department)s ORDER BY bb.gained_points DESC",filters,as_dict=1)
            
        for i in query:
            
            emp.append({
                "employee_name":i.employee_name,
                "points_allocated":i.total_points,
                "points_gained":i.gained_points
                })
        
        for i in emp:
            if(i["employee_name"] not in lst):
                lst.append(i["employee_name"])
                t_d.append(i)
            else:
                t_d[lst.index(i["employee_name"])]["points_allocated"]+=i["points_allocated"]
                t_d[lst.index(i["employee_name"])]["points_gained"]+=i["points_gained"]
        for i in t_d:
            if(i["points_gained"]>i["points_allocated"]):
                data.append({
                    "employee_name":i["employee_name"],
                    "allocated_tasks":i["points_allocated"]/100,
                    "points_allocated":i["points_allocated"],
                    "points_gained":i["points_gained"],
                    "bonus":i["points_gained"]-i["points_allocated"],
                    "grade":(i["points_gained"]/(i["points_allocated"]/100))/20 if ((i["points_gained"]/(i["points_allocated"]/100))/20<5) else 5
                    })
            else:
                data.append({
                    "employee_name":i["employee_name"],
                    "allocated_tasks":i["points_allocated"]/100,
                    "points_allocated":i["points_allocated"],
                    "points_gained":i["points_gained"],
                    "bonus":0,
                    "grade":(i["points_gained"]/(i["points_allocated"]/100))/20 if ((i["points_gained"]/(i["points_allocated"]/100))/20<5) else 5
                    })
        def get_points(data):
            return data.get('points_gained')
        data.sort(key=get_points,reverse=True)

    elif(filters.report_type=='Department Points'):
        t_d=[]
        if(filters.employee==None):            
            if(filters.department==None):
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s ORDER BY bb.gained_points DESC",filters,as_dict=1)
            else:
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.department=%(department)s ORDER BY bb.gained_points DESC",filters,as_dict=1)
            
        else:            
            if(filters.department==None):
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.employee=%(employee)s ORDER BY bb.gained_points DESC",filters,as_dict=1)
            else:
                query=frappe.db.sql("SELECT aa.employee,aa.employee_name,aa.department,bb.total_points,bb.gained_points from `tabTask Allocation`as aa,`tabWork Update`as bb WHERE aa.name=bb.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' AND bb.to_time>=%(from_date)s and bb.to_time<=%(to_date)s and aa.employee=%(employee)s and aa.department=%(department)s ORDER BY bb.gained_points DESC",filters,as_dict=1)
            
        for i in query:
            emp.append({
                "department":i.department,
                "points_allocated":i.total_points,
                "points_gained":i.gained_points
                })
        for i in emp:
            if(i["department"] not in lst):
                lst.append(i["department"])
                t_d.append(i)
            else:
                t_d[lst.index(i["department"])]["points_allocated"]+=i["points_allocated"]
                t_d[lst.index(i["department"])]["points_gained"]+=i["points_gained"]
        for i in t_d:
            if(i["points_gained"]>i["points_allocated"]):
                data.append({
                    "department":i["department"],
                    "allocated_tasks":i["points_allocated"]/100,
                    "points_allocated":i["points_allocated"],
                    "points_gained":i["points_gained"],
                    "bonus":i["points_gained"]-i["points_allocated"],
                    "grade":(i["points_gained"]/(i["points_allocated"]/100))/20 if ((i["points_gained"]/(i["points_allocated"]/100))/20<5) else 5
                    })
            else:
                data.append({
                    "department":i["department"],
                    "allocated_tasks":i["points_allocated"]/100,
                    "points_allocated":i["points_allocated"],
                    "points_gained":i["points_gained"],
                    "bonus":0,
                    "grade":(i["points_gained"]/(i["points_allocated"]/100))/20 if ((i["points_gained"]/(i["points_allocated"]/100))/20<5) else 5
                    })
        def get_points(data):
            return data.get('points_gained')
        data.sort(key=get_points,reverse=True)

    return data

