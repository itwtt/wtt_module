# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime,timedelta

def execute(filters=None):
    if not filters:
        return [],[]
    data = []
    columns = get_columns(filters)
    data = get_data(data,filters)
    return columns, data

def get_columns(filters):
    columns=[
        {
            "label": ("PR Date"),
            "fieldtype": "Data",
            "fieldname": "pr_date",
            "width": 200
        },
        {
            "label": ("PR NO"),
            "fieldtype": "Link",
            "fieldname": "pr_no",
            "options":"Purchase Receipt",
            "width": 200
        },
        {
            "label": ("Inspection Date"),
            "fieldtype": "Date",
            "fieldname": "ins_date",
            "width": 150
        },
        {
            "label": ("Inspection No"),
            "fieldtype": "Link",
            "fieldname": "ins_no",
            "options":"Item Inspection",
            "width": 200
        }
    ]
    return columns

def get_data(data, filters):    
    data=[]
    if(filters.get("pr")):
        for j in frappe.db.sql("SELECT pr.name,pr.creation FROM `tabPurchase Receipt` as pr WHERE pr.posting_date>=%(from_date)s AND pr.posting_date<=%(to_date)s AND pr.name=%(pr)s ",filters,as_dict=1):
            for k in frappe.db.sql("SELECT insp.name,insp.report_date FROM `tabItem Inspection` as insp WHERE insp.receipt_series='"+str(j.name)+"' and insp.docstatus=1 ",as_dict=1):
                val=datetime.strptime(str(j.creation),'%Y-%m-%d %H:%M:%S.%f')	            
                go=val
                data.append({
                    "pr_date":val.strftime("%d-%m-%Y %H:%M:%S"),
                    "pr_no":j.name,
                    "ins_date":k.report_date,
                    "ins_no":k.name
                    })
    else:
        for j in frappe.db.sql("SELECT pr.name,pr.creation FROM `tabPurchase Receipt` as pr WHERE pr.posting_date>=%(from_date)s AND pr.posting_date<=%(to_date)s",filters,as_dict=1):
            for k in frappe.db.sql("SELECT insp.name,insp.report_date FROM `tabItem Inspection` as insp WHERE insp.receipt_series='"+str(j.name)+"' and insp.docstatus=1 ",as_dict=1):
               	val=datetime.strptime(str(j.creation),'%Y-%m-%d %H:%M:%S.%f')
                go=val.date()
                data.append({
                    "pr_date":val.strftime("%d-%m-%Y %H:%M:%S"),
                    "pr_no":j.name,
                    "ins_date":k.report_date,
                    "ins_no":k.name
                    })
    return data