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
    "label": _("MR Row"),
    "fieldname": "mr_row",
    "fieldtype": "Data",
    "width": 80
    },
    {
    "label": _("Item"),
    "fieldname": "item_code",
    "fieldtype": "Link",
    "options":"Item",
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
    "label": _("Freezed Qty"),
    "fieldname": "freeze_qty",
    "fieldtype": "Float",
    "width": 120
    },
    {
    "label": _("Stock Qty"),
    "fieldname": "stock_qty",
    "fieldtype": "Float",
    "width": 120
    }
    ]
    return columns

def get_data(conditions,data, filters):
    data=[]
    for i in frappe.db.sql("SELECT mri.parent,mri.item_code,mri.description,mri.technical_description,mri.idx,mri.qty,mri.freeze_qty FROM `tabMaterial Request Item` as mri INNER JOIN `tabMaterial Request` as mr ON mr.name=mri.parent WHERE mr.docstatus=1{conditions}".format(conditions=conditions),as_dict=1):
        data.append({
            "mr_no":i.parent,
            "mr_row":i.idx,
            "item_code":i.item_code,
            "description":i.description,
            "technical_description":i.technical_description,
            "qty":i.qty,
            "freeze_qty":i.freeze_qty,
            "stock_qty":0
        })
    return data

def get_conditions(filters):
    conditions = ""
    if filters.get("project"):
        conditions += " AND mr.project='%s'" % filters.get('project')

    return conditions