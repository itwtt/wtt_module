# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime,timedelta

def execute(filters=None):
    data = []
    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(conditions,data,filters)
    return columns, data

@frappe.whitelist()
def get_columns(filters):
    if(filters.get("group_by") == 'MR Wise'):
        columns = [
        {
        "label": _("MR No"),
        "fieldname": "mr_no",
        "fieldtype": "Link",
        "options":"Material Request",
        "width": 120
        },
        {
        "label": _("Request Purpose"),
        "fieldname": "request_purpose",
        "fieldtype": "Data",
        "width": 250
        },
        {
        "label": _("Project"),
        "fieldname": "project",
        "fieldtype": "Link",
        "options":"Project",
        "width": 150
        },
        {
        "label": _("Approved Date"),
        "fieldname": "date",
        "fieldtype": "Date",
        "width": 150
        }
        ]
    else:
        columns = [
        {
        "label": _("MR No"),
        "fieldname": "mr_no",
        "fieldtype": "Link",
        "options":"Material Request",
        "width": 120
        },
        {
        "label": _("Description"),
        "fieldname": "description",
        "fieldtype": "Data",
        "width": 150
        },
        {
        "label": _("Technical Description"),
        "fieldname": "technical_description",
        "fieldtype": "Data",
        "width": 250
        },
        {
        "label": _("Qty"),
        "fieldname": "qty",
        "fieldtype": "Float",
        "width": 80
        },
        {
        "label": _("Project"),
        "fieldname": "project",
        "fieldtype": "Link",
        "options":"Project",
        "width": 100
        },
        {
        "label": _("Approved Date"),
        "fieldname": "date",
        "fieldtype": "Date",
        "width": 120
        },
        {
        "label": _("Purchase Order"),
        "fieldname": "po_no",
        "fieldtype": "Link",
        "options":"Purchase Order",
        "width": 150
        },
        {
        "label": _("PO Status"),
        "fieldname": "po_status",
        "fieldtype": "Data",
        "width": 150
        },
        {
        "label": _("PO Qty"),
        "fieldname": "po_qty",
        "fieldtype": "Float",
        "width": 80
        }
        ]

    return columns

def get_data(conditions,data, filters):
    if(filters.get("group_by") == 'MR Wise'):
        data=[]
        today_date = datetime.now().date()
        yesterday_date = today_date - timedelta(days=1)
        if yesterday_date.weekday() == 6:
            yesterday_date = today_date - timedelta(days=2)
        for i in frappe.db.sql("SELECT name,request_purpose,project,approved_date FROM `tabMaterial Request` WHERE approved_date='"+str(today_date)+"'{conditions}".format(conditions=conditions),as_dict=1): 
            data.append({
                "mr_no":i.name,
                "request_purpose":i.request_purpose,
                "project":i.project,
                "date":i.approved_date,
            })
        for k in frappe.db.sql("SELECT name,request_purpose,project,approved_date FROM `tabMaterial Request` WHERE approved_date='"+str(yesterday_date)+"'{conditions}".format(conditions=conditions),as_dict=1): 
            data.append({
                "mr_no":k.name,
                "request_purpose":k.request_purpose,
                "project":k.project,
                "date":k.approved_date,
            })
    else:
        data=[]
        today_date = datetime.now().date()
        yesterday_date = today_date - timedelta(days=1)
        if yesterday_date.weekday() == 6:
            yesterday_date = today_date - timedelta(days=2)
        for i in frappe.db.sql("SELECT mr.name as mr_no,mri.name as ref_name,mr.request_purpose,mr.project,mr.approved_date,mri.description,mri.technical_description,mri.qty FROM `tabMaterial Request` as mr INNER JOIN `tabMaterial Request Item` as mri ON mr.name=mri.parent WHERE mr.approved_date='"+str(today_date)+"'{conditions}".format(conditions=conditions),as_dict=1): 
            po_no=frappe.db.get_value("Purchase Order Item",{'material_request_item':i.ref_name},"parent")
            po_qty=frappe.db.get_value("Purchase Order Item",{'material_request_item':i.ref_name},"qty")
            po_status=frappe.db.get_value("Purchase Order",po_no,"workflow_state")
            data.append({
                "mr_no":i.mr_no,
                "description":i.description,
                "technical_description":i.technical_description,
                "qty":i.qty,
                "project":i.project,
                "date":i.approved_date,
                "po_no":po_no,
                "po_status":po_status,
                "po_qty":po_qty
            })
        for k in frappe.db.sql("SELECT mr.name as mr_no,mri.name as ref_name,mr.request_purpose,mr.project,mr.approved_date,mri.description,mri.technical_description,mri.qty FROM `tabMaterial Request` as mr INNER JOIN `tabMaterial Request Item` as mri ON mr.name=mri.parent WHERE mr.approved_date='"+str(yesterday_date)+"'{conditions}".format(conditions=conditions),as_dict=1): 
            po_no=frappe.db.get_value("Purchase Order Item",{'material_request_item':k.ref_name},"parent")
            po_qty=frappe.db.get_value("Purchase Order Item",{'material_request_item':k.ref_name},"qty")
            po_status=frappe.db.get_value("Purchase Order",po_no,"workflow_state")
            data.append({
                "mr_no":k.mr_no,
                "description":k.description,
                "technical_description":k.technical_description,
                "qty":k.qty,
                "project":k.project,
                "date":k.approved_date,
                "po_no":po_no,
                "po_status":po_status,
                "po_qty":po_qty
            })
    return data

def get_conditions(filters):
    if(filters.get("group_by") == 'MR Wise'):
        conditions = ""
        if filters.get("mr_no"):
            conditions += " AND name='%s'" % filters.get('mr_no')

        if filters.get("project"):
            conditions += " AND project='%s'" % filters.get('project')
    else:
        conditions = ""
        if filters.get("mr_no"):
            conditions += " AND mr.mr_no='%s'" % filters.get('mr_no')

        if filters.get("project"):
            conditions += " AND mr.project='%s'" % filters.get('project')

    return conditions