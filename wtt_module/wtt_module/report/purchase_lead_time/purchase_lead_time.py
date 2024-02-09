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
    data=[]
    batch_size = 1000  # Adjust the batch size as needed
    offset = 0
    while True:
        batch_query = frappe.db.sql("""
            SELECT mr.name as mr_no, mri.name as ref_name, mr.request_purpose, mr.project,
                mr.approved_date, mri.description, mri.technical_description, mri.qty
            FROM `tabMaterial Request` as mr
            INNER JOIN `tabMaterial Request Item` as mri ON mr.name = mri.parent
            WHERE mr.creation > '2023-01-01' and mr.workflow_state = 'Approved'{conditions}
            LIMIT {batch_size} OFFSET {offset}
        """.format(conditions=conditions, batch_size=batch_size, offset=offset), as_dict=1)

        if not batch_query:
            break  # No more records

        for i in batch_query:
            po_no = frappe.db.get_value("Purchase Order Item", {'material_request_item': i.ref_name}, "parent")
            po_qty = frappe.db.get_value("Purchase Order Item", {'material_request_item': i.ref_name}, "qty")
            po_status = frappe.db.get_value("Purchase Order", po_no, "workflow_state")
            if(po_status == 'Cancelled' or po_status == 'Rejected'):
                po_no=''
                po_qty=0
                po_status=''
            data.append({
                "mr_no": i.mr_no,
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
    conditions = ""
    if filters.get("mr_no"):
        conditions += " AND mr.name='%s'" % filters.get('mr_no')

    if filters.get("project"):
        conditions += " AND mr.project='%s'" % filters.get('project')

    return conditions