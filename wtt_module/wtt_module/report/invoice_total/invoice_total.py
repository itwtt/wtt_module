# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
import json
from frappe.model.mapper import get_mapped_doc
from datetime import date,datetime,timedelta

def execute(filters=None):
    data = []
    columns = get_columns(filters)
    data = get_data(data , filters)
    return columns, data

def get_columns(filters):
    columns=[
        {
            "label": _("ACCOUNT"),
            "fieldtype": "Data",
            "fieldname": "account",
            "width": 180
        }
    ]
    val=frappe.db.sql("SELECT DISTINCT(project) FROM `tabPurchase Invoice Item` WHERE docstatus=1",filters,as_dict=1)
    for i in val:
        if(frappe.db.get_value("Project",i.project,'status')=='On going'):
        
            columns.append({
                "fieldname": i.project,
                "label": i.project,
                "fieldtype": "Data",
                "width": 150
            })
    return columns

def get_data(data, filters):
    data=[]
    temp_list=[]
    query=frappe.db.sql("SELECT DISTINCT(bb.expense_account),bb.project,sum(bb.base_net_amount)as amount FROM `tabPurchase Invoice`as aa,`tabPurchase Invoice Item` as bb WHERE aa.name=bb.parent and aa.docstatus=1 GROUP BY bb.project, bb.expense_account",as_dict=1)
    for i in query:
        temp_list.append(i.expense_account)
    unique_item = set(temp_list)
    for item in unique_item:
        column = {}
        for i in query:
            if item == i.expense_account:
                column['account'] = i.expense_account
                column[i.project]=round(i.amount,2)
        data.append(column)
    
    return data

