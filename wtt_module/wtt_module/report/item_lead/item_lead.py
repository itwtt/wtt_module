# Copyright (c) 2013, wtt_module and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
import json
from datetime import datetime,date,timedelta
from dateutil import relativedelta

def execute(filters=None):
    if not filters:
        return [], []
    data = []
    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = get_data(conditions,data,filters)
    return columns, data


def get_columns(filters):
    v=filters.get('dc')
    if(v=='Material Request'):
        columns = [
            # {
            #     "label": _("Row"),
            #     "fieldname": "row",
            #     "fieldtype": "Data",
            #     "width": 120
            # },
            {
                "label": _("Item Code"),
                "fieldname": "item_code",
                "fieldtype": "Link",
                "options":"Item",
                "width": 120
            },
            {
                "label": _("Description"),
                "fieldname": "description",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("Technical Description"),
                "fieldname": "technical_description",
                "fieldtype": "Small Text",
                "width": 300
            },
            # {
            #     "label": _("Request Purpose"),
            #     "fieldname": "rq_purpose",
            #     "fieldtype": "Data",
            #     "width": 120
            # },
            # {
            #     "label": _("MR No"),
            #     "options": "Material Request",
            #     "fieldname": "material_request_no",
            #     "fieldtype": "Link",
            #     "width": 180
            # },
            # {
            #     "label": _("Project"),
            #     "options": "Project",
            #     "fieldname": "project",
            #     "fieldtype": "Link",
            #     "width": 90
            # },
            {
                "label": _("Creation Date"),
                "fieldname": "material_request_date",
                "fieldtype": "Date",
                "width": 160
            },
            {
                "label": _("Delivery Date"),
                "fieldname": "delivery_date",
                "fieldtype": "Data",
                "width": 160
            }
        ]
        return columns
    elif(v=='Item'):
        columns = [
            {
                "label": _("Item"),
                "fieldname": "item",
                "fieldtype": "Link",
                "options":"Item",
                "width": 160
            },
            {
                "label": _("Lead Time"),
                "fieldname": "lead_time",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Selection"),
                "fieldname": "selection",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Ordering"),
                "fieldname": "ordering",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Lead Days"),
                "fieldname": "lead_days",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Delivery Time"),
                "fieldname": "delivery_time",
                "fieldtype": "Data",
                "width": 80
            },
            {
                "label": _("Total Days"),
                "fieldname": "total_days",
                "fieldtype": "Data",
                "width": 80
            }
        ]
        if(filters.item!=None):
            columns = [
                {
                    "label": _("Item"),
                    "fieldname": "item",
                    "fieldtype": "Link",
                    "options":"Item",
                    "width": 160
                },
                {
                    "label": _("Description"),
                    "fieldname": "description",
                    "fieldtype": "Data",
                    "width": 160
                },
                {
                    "label": _("Technical Description"),
                    "fieldname": "technical_description",
                    "fieldtype": "Small Text",
                    "width": 160
                },
                {
                    "label": _("Lead Time"),
                    "fieldname": "lead_time",
                    "fieldtype": "Data",
                    "width": 80
                },
                {
                    "label": _("Selection"),
                    "fieldname": "selection",
                    "fieldtype": "Data",
                    "width": 80
                },
                {
                    "label": _("Ordering"),
                    "fieldname": "ordering",
                    "fieldtype": "Data",
                    "width": 80
                },
                {
                    "label": _("Lead Days"),
                    "fieldname": "lead_days",
                    "fieldtype": "Data",
                    "width": 80
                },
                {
                    "label": _("Delivery Time"),
                    "fieldname": "delivery_time",
                    "fieldtype": "Data",
                    "width": 80
                },
                {
                    "label": _("Total Days"),
                    "fieldname": "total_days",
                    "fieldtype": "Data",
                    "width": 80
                }
            ]
        return columns




def get_data(conditions,data, filters):
    data=[]
    v=filters.get('dc')
    if(v=='Item'):
        if(filters.get('item')==None):
            mr_details = frappe.db.sql("""SELECT item_template as item,lead_time,selection,ordering,lead_days,delivery_time,total_days FROM `tabItem Lead Time` """,filters,as_dict=1)
            for i in mr_details:
                data.append(i)
        else:
            mr_details = frappe.db.sql("""SELECT distinct(name)as item_code,variant_of,description,technical_description FROM `tabItem` WHERE variant_of=%(item)s """.format(conditions=conditions),filters,as_dict=1)

            for i in mr_details:
                data.append({
                    "item":i.item_code,
                    "description":i.description,
                    "technical_description":i.technical_description,
                    "lead_time":str(frappe.db.get_value("Item Lead Time",{"item_template":filters.get('item')},"lead_time")),
                    "selection":str(frappe.db.get_value("Item Lead Time",{"item_template":filters.get('item')},"selection")),
                    "ordering":str(frappe.db.get_value("Item Lead Time",{"item_template":filters.get('item')},"ordering")),
                    "lead_days":str(frappe.db.get_value("Item Lead Time",{"item_template":filters.get('item')},"lead_days")),
                    "delivery_time":str(frappe.db.get_value("Item Lead Time",{"item_template":filters.get('item')},"delivery_time")),
                    "total_days":str(frappe.db.get_value("Item Lead Time",{"item_template":filters.get('item')},"total_days"))
                    })

    elif(v=='Material Request'):
        if(filters.get('material_request')==None):
            pass
        else:
            mr=[]
            if(filters.get('item')==None):
                mr_details = frappe.db.sql(""" SELECT mr.name,mr.request_purpose,mr.project,mri.idx,mri.item_code,mri.description,mri.technical_description,mr.creation FROM `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent and mr.name=%(material_request)s ORDER BY mr.name,mri.idx""".format(conditions=conditions),filters,as_dict=1)
            else:
                mr_details = frappe.db.sql(""" SELECT mr.name,mr.request_purpose,mr.project,mri.idx,mri.item_code,mri.description,mri.technical_description,mr.creation FROM `tabMaterial Request`as mr,`tabMaterial Request Item`as mri INNER JOIN `tabItem`as item on mri.item_code=item.name WHERE mr.name=mri.parent and item.variant_of=%(item)s and mr.name=%(material_request)s ORDER BY mr.name,mri.idx""".format(conditions=conditions),filters,as_dict=1)
            for i in mr_details:
                date1=(i.creation).date()
                variant_of=frappe.db.get_value("Item",i.item_code,"variant_of")
                delivery_days=frappe.db.get_value("Item Lead Time",{"item_template":variant_of},"total_days")
                if(delivery_days!=None):
                    date__=date1+timedelta(days=int(delivery_days))
                    delivery_date_datetime=datetime.strptime(str(date__),"%Y-%m-%d")
                    delivery_date=delivery_date_datetime.strftime("%d-%m-%Y")+" ("+str(delivery_days)+" days)"
                else:
                    delivery_date="-"
                if(i.name not in mr):
                    mr.append(i.name)
                    data.append({
                        "material_request_date":(i.creation).date(),
                        "material_request_no":i.name,
                        "row":i.idx,
                        "item_code":i.item_code,
                        "description":i.description,
                        "technical_description":i.technical_description,
                        "project":i.project,
                        "delivery_date":delivery_date,
                        "rq_purpose":i.request_purpose
                        })
                else:
                    data.append({
                        "row":i.idx,
                        "item_code":i.item_code,
                        "description":i.description,
                        "delivery_date":delivery_date,
                        "technical_description":i.technical_description,
                        "material_request_date":(i.creation).date()
                        })



    else:
        pass

    return data

def get_conditions(filters):
    conditions = "mr.docstatus = 1"
    if filters.get("material_request"):
        conditions += " and mr.name = %(material_request)s"
    if filters.get("item"):
        conditions += " and variant_of = %(item)s"

    match_conditions = build_match_conditions("Material Request")
    if match_conditions:
        conditions += " and %s" % match_conditions
    return conditions