# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
from datetime import datetime

def execute(filters=None):
    if not filters:
        return [], []
    data = []
    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(conditions,data,filters)
    return columns, data

def get_columns(filters):
    columns = [
        {
            "label": _("PO NO"),
            "fieldname": "po_no",
            "fieldtype": "Link",
            "width": 150,
            "options":"Purchase Order"
        },
        {
            "label": _("Project"),
            "options": "Project",
            "fieldname": "project",
            "fieldtype": "Link",
            "width": 150
        },
        {
            "label": _("Item"),
            "options": "Item",
            "fieldname": "item",
            "fieldtype": "Link",
            "width": 150
        },
        {
            "label": _("Description"),
            "fieldname": "des",
            "fieldtype": "Data",
            "width": 150
        },
        {
        	"label":"Technical Description",
        	"fieldname":"tec",
        	"fieldtype":"Data",
        	"width":200
        },
        {
            "label": _("Amount"),
            "fieldname": "amt",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("MR No"),
            "options": "Material Request",
            "fieldname": "material_request_no",
            "fieldtype": "Link",
            "width": 180
        },
        {
            "label": _("Workflow"),
            "options": "Workflow State",
            "fieldname": "workflow_state",
            "fieldtype": "Link",
            "width": 180
        }
    ]
    return columns

def get_data(conditions,data, filters):
    data=[]
    po_details = frappe.db.sql("""SELECT po.name,poi.project,po.workflow_state,poi.amount,poi.material_request,poi.item_code,poi.description,poi.technical_description FROM `tabPurchase Order Item` as poi inner join `tabPurchase Order` as po on po.name = poi.parent where po.workflow_state=%(workflow)s {conditions}""".format(conditions=conditions),filters,as_dict = 1)
    for i in po_details:        
        data.append({
            "po_no":i.name,
            "project":i.project,
            "item":i.item_code,
            "des":i.description,
            "tec":i.technical_description,
            "amt":i.amount,
            "material_request_no":i.material_request,
            "workflow_state":i.workflow_state
        })
    return data
    
  


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND po.creation>='%s'" % filters.get('from_date')
    if filters.get("to_date"):
        conditions += " AND po.creation<='%s'" % filters.get('to_date')
    if filters.get("project"):
        conditions += " AND poi.project='%s'" % filters.get('project')
    return conditions
