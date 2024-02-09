# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt

import frappe
import itertools

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
            "label":"PURCHASE ORDER",
            "fieldname":"purchase_order",
            "fieldtype":"Link",
            "options":"Purchase Order"
        },
        {
            "label":"SUPPLIER",
            "fieldname":"supplier",
            "fieldtype":"Link",
            "options":"Supplier"
        },
        {
            "label":"TOTAL",
            "fieldname":"total",
            "fieldtype":"Currency"
        },
        {
            "label":"Paid",
            "fieldname":"paid",
            "fieldtype":"Currency"
        }
    ]
    return columns

def get_data(data, filters):
    data=[]
    poi=[]
    query = frappe.db.sql("""SELECT distinct(purchase_order_item)as purchase_order_item FROM `tabPurchase Receipt Item` WHERE docstatus!=2  """,as_dict=1)
    for i in query:
        poi.append(i.purchase_order_item)
    query2 = frappe.db.sql(" SELECT distinct(parent)as purchase_order FROM `tabPurchase Order Item` WHERE docstatus=1  ",as_dict=1)
    for i in query2:
        data.append({
            "purchase_order":i.purchase_order,
            "supplier":frappe.db.get_value("Purchase Order",str(i.purchase_order),"supplier"),
            "total":frappe.db.get_value("Purchase Order",str(i.purchase_order),"rounded_total"),
            })
    
    return data
