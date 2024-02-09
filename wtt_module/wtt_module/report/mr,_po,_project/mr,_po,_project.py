# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt

import frappe
import itertools
from frappe.desk.reportview import build_match_conditions


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
            "label": ("MATERIAL REQUEST"),
            "fieldtype": "Link",
            "fieldname": "mr",
            "options":"Material Request",
            "width": 200
        },
        {
            "label":"WORKFLOW STATE",
            "fieldtype":"Data",
            "fieldname":"status",
            "width":100
        },
        {
            "label": ("DESCRIPTION"),
            "fieldtype": "Data",
            "fieldname": "description",
            "width": 150
        },
        {
            "label": ("TECHNICAL DESCRIPTION"),
            "fieldtype": "Data",
            "fieldname": "technical_description",
            "width": 300
        },
        {
            "label": ("PROJECT"),
            "fieldtype": "Data",
            "fieldname": "project",
            "width": 150
        },
        {
            "label": ("RATE"),
            "fieldtype": "Data",
            "fieldname": "rate",
            "width": 70
        },
        {
            "label": ("QUANTITY"),
            "fieldtype": "Data",
            "fieldname": "qty",
            "width": 70
        },
        {
            "label": ("AMOUNT"),
            "fieldtype": "Data",
            "fieldname": "amount",
            "width": 80
        },
        {
            "label": ("PURCHASE ORDER"),
            "fieldtype": "Link",
            "fieldname": "po",
            "options":"Purchase Order",
            "width": 150
        }
    ]
    return columns

def get_data(data, filters):
    
    data=[]
    if(filters.get("mr")):
        doc=frappe.db.sql("SELECT a.name,a.workflow_state,b.material_request,b.project,b.description,b.technical_description,b.qty,b.price_list_rate,b.last_purchase_rate from `tabPurchase Order`as a,`tabPurchase Order Item`as b Where a.name=b.parent and a.project=%(project)s and b.project=%(project)s and b.material_request=%(mr)s",filters,as_dict=1)
        for i in doc:
            data.append({
                "mr":i.material_request,
                "status":i.workflow_state,
                "technical_description":i.technical_description,
                "description":i.description,
                "project":i.project,
                "rate":i.price_list_rate,
                "qty":i.qty,
                "amount":i.last_purchase_rate,
                "po":i.name
                })
    else:
        doc=frappe.db.sql("SELECT a.name,a.workflow_state,b.material_request,b.project,b.description,b.technical_description,b.qty,b.rate,b.amount from `tabPurchase Order`as a,`tabPurchase Order Item`as b Where a.name=b.parent and a.project=%(project)s and b.project=%(project)s ",filters,as_dict=1)
        for i in doc:
            data.append({
                "mr":i.material_request,
                "status":i.workflow_state,
                "technical_description":i.technical_description,
                "description":i.description,
                "project":i.project,
                "rate":i.rate,
                "qty":i.qty,
                "amount":i.amount,
                "po":i.name
                })

    # if filters.get("mr"):
    #     frappe.msgprint(filters.get("project"))
    #     mate = frappe.db.sql("""select prt.material_request,prt.item_code,prt.description,prt.project,pr.name 
    #         from `tabPurchase Order Item`as prt,`tabPurchase Order`as pr 
    #         where pr.name=prt.parent and prt.project=%(project)s and pr.project=%(project)s""",filters, as_dict=1)
    
    #     for k in mate:            
    #         data.append({
    #             "mr":k.material_request,
    #             "item_code":k.item_code,
    #             "description":k.description,
    #             "project":k.project,
    #             "po":k.name
    #             })

    return data


