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
            "label": ("Material Request"),
            "fieldtype": "Link",
            "fieldname": "mr",
            "options":"Material Request",
            "width": 150
        },
        {
            "label": ("Item Code"),
            "fieldtype": "Data",
            "fieldname": "item_code",
            "width": 150
        },
        {
            "label": ("Description"),
            "fieldtype": "Data",
            "fieldname": "description",
            "width": 150
        },
        {
            "label": ("Technical Description"),
            "fieldtype": "Data",
            "fieldname": "technical_description",
            "width": 250
        },
        {
            "label": ("MR Qty"),
            "fieldtype": "Data",
            "fieldname": "qty",
            "width": 100
        },
        {
            "label": ("PO Qty"),
            "fieldtype": "Data",
            "fieldname": "po_qty",
            "width": 100
        },
        {
            "label":"Row",
            "fieldname":"row",
            "fieldtype":"Data",
            "width":100
        },
        {
            "label": ("Purchase Order"),
            "fieldtype": "Link",
            "fieldname": "po",
            "options":"Purchase Order",
            "width": 150
        }
    ]
    return columns

def get_data(data, filters):

    data=[]
    ic=[]
    act=[]
    check = frappe.db.sql("""select mrt.idx,mrt.item_code,mrt.description,mrt.technical_description,mrt.qty,mrt.uom,mr.name from `tabMaterial Request Item`as mrt,`tabMaterial Request`as mr Where mrt.parent=mr.name and mr.name=%(mr_no)s""",filters, as_dict=1) 
    if(filters.item_group!=None):
        check = frappe.db.sql("""select mrt.idx,mrt.item_code,mrt.description,mrt.technical_description,mrt.qty,mrt.uom,mr.name from `tabMaterial Request Item`as mrt,`tabMaterial Request`as mr Where mrt.parent=mr.name and mr.name=%(mr_no)s and mrt.item_group=%(item_group)s""",filters, as_dict=1) 

    mate = frappe.db.sql("""select prt.idx,prt.material_request,prt.item_code,prt.description,prt.technical_description,prt.qty,prt.uom,pr.name from `tabPurchase Order Item`as prt,`tabPurchase Order`as pr where prt.parent=pr.name and pr.docstatus!=2 and pr.workflow_state!="Rejected" and prt.material_request=%(mr_no)s """,filters, as_dict=1)
    if(filters.item_group!=None):
        check = frappe.db.sql("""select mrt.idx,mrt.item_code,mrt.description,mrt.technical_description,mrt.qty,mrt.uom,mr.name from `tabMaterial Request Item`as mrt,`tabMaterial Request`as mr Where mrt.parent=mr.name and mr.name=%(mr_no)s and mrt.item_group=%(item_group)s ORDER BY mrt.idx""",filters, as_dict=1)
        mate = frappe.db.sql("""select prt.idx,prt.material_request,prt.material_request_item,prt.item_code,prt.description,prt.technical_description,prt.qty,prt.uom,pr.name from `tabPurchase Order Item`as prt,`tabPurchase Order`as pr where prt.parent=pr.name and pr.docstatus!=2 and pr.workflow_state!="Rejected" and prt.material_request=%(mr_no)s  and prt.item_group=%(item_group)s""",filters, as_dict=1)

    for j in mate:
        ic.append(j.item_code)

    for i in check:
        if(i.item_code not in ic):
            data.append({
                "mr":i.name,
                "item_code":i.item_code,
                "description":i.description,
                "technical_description":i.technical_description,
                "qty":str(i.qty)+" "+i.uom,
                "po_qty":"-",
                "row":"MR-"+str(i.idx),
                "po":"Not Linked"
                })
    #     else:
    for k in mate:
        data.append({
            "mr":k.material_request,
            "item_code":k.item_code,
            "description":k.description,
            "technical_description":k.technical_description,
            "qty":"-",
            "po_qty":str(k.qty)+" "+k.uom,
            "row":"MR-"+str(frappe.db.sql("SELECT idx from `tabMaterial Request Item` where name='"+str(k.material_request_item)+"' ",as_dict=1)),
            "po":k.name
            })
    return data