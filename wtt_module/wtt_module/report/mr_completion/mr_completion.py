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
        },
        {
        "label": _("Status"),
        "fieldname": "status",
        "fieldtype": "Data",
        "width": 150
        },
        {
        "label": _("Order (%)"),
        "fieldname": "per_ordered",
        "fieldtype": "Float",
        "width": 150
        },
        {
        "label": _("Received (%)"),
        "fieldname": "per_received",
        "fieldtype": "Float",
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
        "label": _("MR Row"),
        "fieldname": "mr_row",
        "fieldtype": "Data",
        "width": 80
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
        for i in frappe.db.sql("SELECT name,request_purpose,project,approved_date,status,per_ordered,per_received FROM `tabMaterial Request` WHERE creation>'2023-01-01' and workflow_state='Approved'{conditions}".format(conditions=conditions),as_dict=1): 
            data.append({
                "mr_no":i.name,
                "request_purpose":i.request_purpose,
                "project":i.project,
                "date":i.approved_date,
                "status":i.status,
                "per_ordered":i.per_ordered,
                "per_received":i.per_received
            })
    else:
        data=[]
        batch_size = 1000
        offset = 0
        while True:
            batch_query = frappe.db.sql("""
                SELECT mr.name as mr_no, mri.name as ref_name, mr.request_purpose, mr.project,
                    mr.approved_date, mri.description, mri.technical_description, mri.qty,mri.idx
                FROM `tabMaterial Request` as mr
                INNER JOIN `tabMaterial Request Item` as mri ON mr.name = mri.parent
                WHERE mr.creation > '2023-01-01' and mr.workflow_state = 'Approved'{conditions}
                LIMIT {batch_size} OFFSET {offset}
            """.format(conditions=conditions, batch_size=batch_size, offset=offset), as_dict=1)

            if not batch_query:
                break

            for i in batch_query:
                po_no = frappe.db.get_value("Purchase Order Item", {'material_request_item': i.ref_name}, "parent")
                po_qty = frappe.db.get_value("Purchase Order Item", {'material_request_item': i.ref_name}, "qty")
                po_status = frappe.db.get_value("Purchase Order", po_no, "workflow_state")
                if(po_qty):
                    pass
                else:
                    po_qty=0
                if(po_status == 'Cancelled' or po_status == 'Rejected'):
                    po_no=''
                    po_qty=0
                    po_status=''
                if(filters.get("not_ordered") == 1):
                    diff = float(i.qty) - float(po_qty)
                    if(diff>0):
                        data.append({
                        "mr_no": i.mr_no,
                        "mr_row":i.idx,
                        "description": i.description,
                        "technical_description": i.technical_description,
                        "qty": i.qty,
                        "project": i.project,
                        "date": i.approved_date,
                        "po_no": po_no,
                        "po_status": po_status,
                        "po_qty": po_qty
                        })
                else:
                    data.append({
                        "mr_no": i.mr_no,
                        "mr_row":i.idx,
                        "description": i.description,
                        "technical_description": i.technical_description,
                        "qty": i.qty,
                        "project": i.project,
                        "date": i.approved_date,
                        "po_no": po_no,
                        "po_status": po_status,
                        "po_qty": po_qty
                    })
            offset += batch_size
    return data

def get_conditions(filters):
    if(filters.get("group_by") == 'MR Wise'):
        conditions = ""
        if filters.get("mr_no"):
            conditions += " AND name='%s'" % filters.get('mr_no')

        if filters.get("project"):
            conditions += " AND project='%s'" % filters.get('project')

        if filters.get("status"):
            conditions += " AND status='%s'" % filters.get('status')
    else:
        conditions = ""
        if filters.get("mr_no"):
            conditions += " AND mr.name='%s'" % filters.get('mr_no')

        if filters.get("project"):
            conditions += " AND mr.project='%s'" % filters.get('project')

    return conditions