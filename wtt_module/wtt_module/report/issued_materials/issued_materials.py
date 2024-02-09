# from __future__ import unicode_literals
# import frappe
# from frappe import _
# from frappe.desk.reportview import build_match_conditions

# def execute(filters=None):
#     if not filters:
#         return [], []

#     columns = get_columns(filters)
#     conditions = get_conditions(filters)
#     data = get_data(conditions, filters)
    
#     return columns, data

# @frappe.whitelist()
# def get_columns(filters):
#     columns = [
#         {"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150, "hidden": 1},
#         {"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 150},
#         {"label": _("Technical Description"), "fieldname": "technical_description", "fieldtype": "Data", "width": 150},
#         {"label": _("MR Row"), "fieldname": "mr_row", "fieldtype": "Data", "width": 80},
#         {"label": _("MR Qty"), "fieldname": "mr_qty", "fieldtype": "Float", "width": 80},
#         {"label": _("MR No"), "fieldname": "mr_no", "fieldtype": "Link", "options": "Material Request", "width": 120},
#         {"label": _("Issue No"), "fieldname": "issue_no", "fieldtype": "Link", "options": "Material Issue", "width": 150},
#         {"label": _("Issue Row"), "fieldname": "issue_row", "fieldtype": "Data", "width": 100},
#         {"label": _("Issue Qty"), "fieldname": "issue_qty", "fieldtype": "Float", "width": 100},
#         {"label": _("Status"), "fieldname": "status", "fieldtype": "HTML", "width": 120}
#     ]

#     return columns

# def get_data(conditions, filters):
#     data = []
#     material_request_items = frappe.db.sql(
#         """
#         SELECT * FROM `tabMaterial Request Item`
#         WHERE docstatus = 1 {conditions}
#         """.format(conditions=conditions), as_dict=1
#     )

#     for i in material_request_items:
#         issue_row, issue_no, issue_qty = frappe.db.get_value(
#             "Material Issue Item",
#             {'material_request_item': i.name},
#             ['idx', 'parent', 'qty']
#         ) or (0, '-', 0)

#         status_html = "<b style='color:green'>Issued</b>" if issue_no != '-' else "<b style='color:red'>Not Issued</b>"
        
#         if(filters.get('status') == 'Issued'):
#             if(issue_qty>0):
#                 data.append({
#                 "item_code": i.item_code,
#                 "description": i.description,
#                 "technical_description": i.technical_description,
#                 "mr_row": i.idx,
#                 "mr_qty": i.qty,
#                 "mr_no": i.parent,
#                 "issue_no": issue_no,
#                 "issue_row": issue_row,
#                 "issue_qty": issue_qty,
#                 "status": status_html
#                 })
#         elif(filters.get('status') == 'Not Issued'):
#             if(issue_no == '-'):
#                 data.append({
#                 "item_code": i.item_code,
#                 "description": i.description,
#                 "technical_description": i.technical_description,
#                 "mr_row": i.idx,
#                 "mr_qty": i.qty,
#                 "mr_no": i.parent,
#                 "issue_no": issue_no,
#                 "issue_row": issue_row,
#                 "issue_qty": issue_qty,
#                 "status": status_html
#                 })
#         else:
#             data.append({
#                 "item_code": i.item_code,
#                 "description": i.description,
#                 "technical_description": i.technical_description,
#                 "mr_row": i.idx,
#                 "mr_qty": i.qty,
#                 "mr_no": i.parent,
#                 "issue_no": issue_no,
#                 "issue_row": issue_row,
#                 "issue_qty": issue_qty,
#                 "status": status_html
#             })
#     return data

# def get_conditions(filters):
#     conditions = ""
#     if filters.get("project"):
#         conditions += " AND project='%s'" % filters.get('project')

#     return conditions


from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions
import asyncio

def execute(filters=None):
    if not filters:
        return [], []

    columns = get_columns(filters)
    conditions = get_conditions(filters)
    data = asyncio.run(get_data_async(conditions, filters))

    return columns, data

@frappe.whitelist()
def get_columns(filters):
    columns = [
        {"label": _("Item Code"), "fieldname": "item_code", "fieldtype": "Link", "options": "Item", "width": 150, "hidden": 1},
        {"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 150},
        {"label": _("Technical Description"), "fieldname": "technical_description", "fieldtype": "Data", "width": 150},
        {"label": _("MR Row"), "fieldname": "mr_row", "fieldtype": "Data", "width": 80},
        {"label": _("MR Qty"), "fieldname": "mr_qty", "fieldtype": "Float", "width": 80},
        {"label": _("MR No"), "fieldname": "mr_no", "fieldtype": "Link", "options": "Material Request", "width": 120},
        {"label": _("Issue No"), "fieldname": "issue_no", "fieldtype": "Link", "options": "Material Issue", "width": 120},
        {"label": _("Issue Row"), "fieldname": "issue_row", "fieldtype": "Data", "width": 80},
        {"label": _("Issue Qty"), "fieldname": "issue_qty", "fieldtype": "Float", "width": 80},
        {"label": _("Status"), "fieldname": "status", "fieldtype": "HTML", "width": 120}
    ]

    return columns

async def get_data_async(conditions, filters):
    data = []
    material_request_items = await frappe.db.sql(
        """
        SELECT * FROM `tabMaterial Request Item`
        WHERE docstatus = 1 {conditions}
        """.format(conditions=conditions), as_dict=1
    )

    tasks = []
    for i in material_request_items:
        tasks.append(get_issue_data_async(i))

    issue_data = await asyncio.gather(*tasks)

    for i, (issue_row, issue_no, issue_qty) in enumerate(issue_data):
        item = material_request_items[i]

        status_html = "<b style='color:green'>Issued</b>" if issue_no else "<b style='color:red'>Not Issued</b>"

        data.append({
            "item_code": item.item_code,
            "description": item.description,
            "technical_description": item.technical_description,
            "mr_row": item.idx,
            "mr_qty": item.qty,
            "mr_no": item.parent,
            "issue_no": issue_no,
            "issue_row": issue_row,
            "issue_qty": issue_qty,
            "status": status_html
        })

    return data

async def get_issue_data_async(material_request_item):
    issue_row, issue_no, issue_qty = frappe.db.get_value(
        "Material Issue Item",
        {'material_request_item': material_request_item.name},
        ['idx', 'parent', 'qty']
    ) or (0, '-', 0)

    return issue_row, issue_no, issue_qty

def get_conditions(filters):
    conditions = ""
    if filters.get("project"):
        conditions += " AND project='%s'" % filters.get('project')
    return conditions
