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
    "label": _("PO Details 1"),
    "fieldname": "po_details1",
    "fieldtype": "Data",
    "width": 300
    },
    {
    "label": _("Price1"),
    "fieldname": "last_low",
    "fieldtype": "HTML",
    "width": 120
    },
    {
    "label": _("PO Details 2"),
    "fieldname": "po_details2",
    "fieldtype": "Data",
    "width": 300
    },
    {
    "label": _("Price2"),
    "fieldname": "price2",
    "fieldtype": "HTML",
    "width": 120
    },
    {
    "label": _("PO Details 3"),
    "fieldname": "po_details3",
    "fieldtype": "Data",
    "width": 300
    },
    {
    "label": _("Price3"),
    "fieldname": "price3",
    "fieldtype": "HTML",
    "width": 120
    },
    ]
    return columns

def get_data(conditions,data, filters):
    data=[]
    batch_size = 1000  # Adjust the batch size as needed
    offset = 0
    while True:
        batch_query = frappe.db.sql("""
            SELECT mr.name as mr_no, mri.name as ref_name,mri.idx, mr.request_purpose, mr.project,
                mr.approved_date,mri.item_code, mri.description, mri.technical_description, mri.qty
            FROM `tabMaterial Request` as mr
            INNER JOIN `tabMaterial Request Item` as mri ON mr.name = mri.parent
            WHERE mr.creation > '2023-01-01' and mr.workflow_state = 'Approved'{conditions} ORDER BY mr.creation DESC
            LIMIT {batch_size} OFFSET {offset}
        """.format(conditions=conditions, batch_size=batch_size, offset=offset), as_dict=1)

        if not batch_query:
            break

        for i in batch_query:
            po_details = []
            get_rates = frappe.db.sql("""
                SELECT poi.base_rate, po.supplier, poi.idx,po.name as po_n
                FROM `tabPurchase Order Item` as poi
                INNER JOIN `tabPurchase Order` as po ON po.name = poi.parent
                WHERE poi.item_code = %s AND po.workflow_state = 'Approved'
                ORDER BY poi.base_rate ASC LIMIT 3
            """, (i.item_code), as_dict=1)

            for k in range(3):
                if k < len(get_rates):
                    po_details.append({
                        "po_number": get_rates[k].po_n,
                        "supplier": get_rates[k].supplier,
                        "base_rate": get_rates[k].base_rate,
                        "po_idx": get_rates[k].idx
                    })
                else:
                    po_details.append({
                        "po_number": "",
                        "supplier": "",
                        "base_rate": 0,
                        "po_idx": 0
                    })

            prices = [get_rates[j].base_rate if j < len(get_rates) else 0 for j in range(3)]

            # Set HTML code for dynamic price comparison
            price1_html = get_price_html(prices[0], prices)
            price2_html = get_price_html(prices[1], prices)
            price3_html = get_price_html(prices[2], prices)

            data.append({
                "mr_no": i.mr_no,
                "mr_row": i.idx,
                "description": i.description,
                "technical_description": i.technical_description,
                "qty": i.qty,
                "project": i.project,
                "date": i.approved_date,
                "last_low": price1_html,
                "po_details1": f"Row {get_rates[0].idx} - {get_rates[0].po_n} - {get_rates[0].supplier}" if get_rates else "",
                "price2": price2_html,
                "po_details2": f"Row {get_rates[0].idx} - {get_rates[1].po_n} - {get_rates[1].supplier}" if get_rates and len(get_rates) > 1 else "",
                "price3": price3_html,
                "po_details3": f"Row {get_rates[0].idx} - {get_rates[2].po_n} - {get_rates[2].supplier}" if get_rates and len(get_rates) > 2 else "",
            })
        offset += batch_size
    return data

def get_price_html(price, all_prices):
    if price == 0:
        return '<span style="color: black;">0</span>'
    elif all_prices[0] == all_prices[1] == all_prices[2]:
        return '<span style="color: black;">{}</span>'.format(price)
    elif price == max(all_prices):
        return '<span style="color: red;">{}</span>'.format(price)
    elif price == min(all_prices):
        return '<span style="color: green;">{}</span>'.format(price)
    else:
        return '<span style="color: orange;">{}</span>'.format(price)

def get_conditions(filters):
    conditions = ""
    if filters.get("mr_no"):
        conditions += " AND mr.name='%s'" % filters.get('mr_no')

    if filters.get("project"):
        conditions += " AND mr.project='%s'" % filters.get('project')

    return conditions