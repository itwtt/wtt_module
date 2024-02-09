# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
import json
from frappe.model.mapper import get_mapped_doc
from datetime import date,datetime,timedelta

def execute(filters=None):
    if not filters:
        return [], []
    data = []
    columns = get_columns(filters)
    data = get_data(data , filters)
    return columns, data


def get_columns(filters):
    columns=[
        {
            "label": _("Request For Quotation"),
            "fieldtype": "Link",
            "fieldname": "rfq",
            "options": "Request for Quotation",
            "width": 180
        },
        {
            "label": _("Quotation Count"),
            "fieldtype": "Data",
            "fieldname": "qc",
            "width": 150
        },
        {
            "label": _("Supplier"),
            "fieldtype": "Data",
            "fieldname": "sup",
            "width": 300
        },
        {
            "label": _("Grand Total"),
            "fieldtype": "Currency",
            "fieldname": "total",
            "width": 180
        },
        {
            "label": _("Button"),
            "fieldtype": "HTML",
            "fieldname": "btn",
            "width": 180
        }
    ]

    return columns

def get_data(data, filters):
    data=[]
    aa=[]
    rfq=[]
    query=frappe.db.sql("SELECT sq.name FROM `tabRequest for Quotation` as sq WHERE sq.transaction_date between %(from_date)s and %(to_date)s and sq.docstatus='1'",filters,as_dict = 1)
    for i in query:
        val=frappe.db.sql("SELECT supplier,base_grand_total FROM `tabSupplier Quotation` as rd WHERE rd.request_for_quotation='"+str(i.name)+"' AND rd.revision='Final Revision' AND rd.workflow_state!='Cancelled'",as_dict = 1)
        for j in val:
            if(i.name not in rfq):
                rfq.append(i.name)
                vcount=frappe.db.count('Supplier Quotation', {'request_for_quotation': str(i.name),'revision':'Final Revision','workflow_state':['!=', 'Cancelled']})
                data.append({})
                data.append({
                    "rfq":i.name,
                    "qc":vcount,
                    "sup":j.supplier,
                    "total":j.base_grand_total,
                    "btn":'<button type="button" style="height:22px;background-color: #4CAF50;color: white;" data-message="'+str(i.name)+'" onclick="getURL(this)">Go to Comparison</button>'
                })
            else:
                data.append({
                    "sup":j.supplier,
                    "total":j.base_grand_total
                })
    return data