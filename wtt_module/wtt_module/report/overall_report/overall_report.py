# from __future__ import unicode_literals
# import frappe
# from frappe import _
# import numpy as np
# from frappe.desk.reportview import build_match_conditions
# from datetime import datetime

# def execute(filters=None):
#     if not filters:
#         return [], []
#     data = []
#     columns = get_columns(filters)
#     conditions = get_conditions(filters)
#     data = get_data(conditions,data,filters)
#     return columns, data

# @frappe.whitelist()
# def get_columns(filters):
#     v=filters.get('dc')
#     if(v=='Material Request'):
#         columns = [
#             {
#                 "label": _("Creation Date"),
#                 "fieldname": "material_request_date",
#                 "fieldtype": "Date",
#                 "width": 160
#             },
#             {
#                 "label": _("MR No"),
#                 "options": "Material Request",
#                 "fieldname": "material_request_no",
#                 "fieldtype": "Link",
#                 "width": 180
#             },
#             {
#                 "label": _("Project"),
#                 "options": "Project",
#                 "fieldname": "project",
#                 "fieldtype": "Link",
#                 "width": 90
#             },
#             {
#                 "label": _("Request Purpose"),
#                 "fieldname": "rq_purpose",
#                 "fieldtype": "Data",
#                 "width": 220
#             },
#             {
#                 "label": _("Creator"),
#                 "fieldname": "requestor",
#                 "fieldtype": "Data",
#                 "width": 140
#             },
#             {
#                 "label": _("HOD approved Date"),
#                 "fieldname": "approval_date",
#                 "fieldtype": "Date",
#                 "width": 160
#             },
#             {
#                 "label": _("Modified by"),
#                 "fieldname": "modify_by",
#                 "fieldtype": "Data",
#                 "width": 180
#             },
#             {
#                 "label": _("Pending days"),
#                 "fieldname": "pending_days",
#                 "fieldtype": "Data",
#                 "width": 120
#             },
#             {
#                 "label": _("Pending days For MD"),
#                 "fieldname": "pending_md",
#                 "fieldtype": "Data",
#                 "width": 160
#             }
#         ]
#         return columns
#     elif(v=='Purchase Order'):
#         columns = [
#             {
#                 "label": _("Creation Date"),
#                 "fieldname": "material_request_date",
#                 "fieldtype": "Date",
#                 "width": 160
#             },
#             {
#                 "label": _("PO No"),
#                 "options": "Purchase Order",
#                 "fieldname": "material_request_no",
#                 "fieldtype": "Link",
#                 "width": 180
#             },
#             {
#                 "label": _("Project"),
#                 "options": "Project",
#                 "fieldname": "project",
#                 "fieldtype": "Link",
#                 "width": 90
#             },
#             {
#                 "label": _("Creator"),
#                 "fieldname": "requestor",
#                 "fieldtype": "Data",
#                 "width": 140
#             },
#             {
#                 "label": _("HOD approved Date"),
#                 "fieldname": "approval_date",
#                 "fieldtype": "Date",
#                 "width": 160
#             },
#             {
#                 "label": _("Modified by"),
#                 "fieldname": "modify_by",
#                 "fieldtype": "Data",
#                 "width": 180
#             },
#             {
#                 "label": _("Pending days"),
#                 "fieldname": "pending_days",
#                 "fieldtype": "Data",
#                 "width": 120
#             },
#             {
#                 "label": _("Pending days For MD"),
#                 "fieldname": "pending_md",
#                 "fieldtype": "Data",
#                 "width": 160
#             }
#         ]
#         return columns
#     elif(v=='Purchase Receipt'):
#         columns = [
#             {
#                 "label": _("Creation Date"),
#                 "fieldname": "material_request_date",
#                 "fieldtype": "Date",
#                 "width": 160
#             },
#             {
#                 "label": _("PR No"),
#                 "options": "Purchase Receipt",
#                 "fieldname": "material_request_no",
#                 "fieldtype": "Link",
#                 "width": 180
#             },
#             {
#                 "label": _("Project"),
#                 "options": "Project",
#                 "fieldname": "project",
#                 "fieldtype": "Link",
#                 "width": 90
#             },
#             {
#                 "label": _("Creator"),
#                 "fieldname": "requestor",
#                 "fieldtype": "Data",
#                 "width": 140
#             },
#             {
#                 "label": _("Modified by"),
#                 "fieldname": "modify_by",
#                 "fieldtype": "Data",
#                 "width": 180
#             },
#             {
#                 "label": _("Pending days"),
#                 "fieldname": "pending_days",
#                 "fieldtype": "Data",
#                 "width": 180
#             }
#         ]
#         return columns

#     elif(v=='Purchase Invoice'):
#         columns = [
#             {
#                 "label": _("Creation Date"),
#                 "fieldname": "material_request_date",
#                 "fieldtype": "Date",
#                 "width": 160
#             },
#             {
#                 "label": _("Invoice No"),
#                 "options": "Purchase Invoice",
#                 "fieldname": "material_request_no",
#                 "fieldtype": "Link",
#                 "width": 180
#             },
#             {
#                 "label": _("Project"),
#                 "options": "Project",
#                 "fieldname": "project",
#                 "fieldtype": "Link",
#                 "width": 90
#             },
#             {
#                 "label": _("Creator"),
#                 "fieldname": "requestor",
#                 "fieldtype": "Data",
#                 "width": 140
#             },
#             {
#                 "label": _("Modified by"),
#                 "fieldname": "modify_by",
#                 "fieldtype": "Data",
#                 "width": 180
#             },
#             {
#                 "label": _("Pending days"),
#                 "fieldname": "pending_days",
#                 "fieldtype": "Data",
#                 "width": 180
#             }
#         ]
#         return columns

#     # elif(v=='Sales Invoice'):
#     #     columns = [
#     #         {
#     #             "label": _("Creation Date"),
#     #             "fieldname": "material_request_date",
#     #             "fieldtype": "Date",
#     #             "width": 160
#     #         },
#     #         {
#     #             "label": _("Invoice No"),
#     #             "options": "Sales Invoice",
#     #             "fieldname": "material_request_no",
#     #             "fieldtype": "Link",
#     #             "width": 180
#     #         },
#     #         {
#     #             "label": _("Creator"),
#     #             "fieldname": "requestor",
#     #             "fieldtype": "Data",
#     #             "width": 140
#     #         },
#     #         {
#     #             "label": _("Modified by"),
#     #             "fieldname": "modify_by",
#     #             "fieldtype": "Data",
#     #             "width": 180
#     #         },
#     #         {
#     #             "label": _("Pending days"),
#     #             "fieldname": "pending_days",
#     #             "fieldtype": "Data",
#     #             "width": 180
#     #         }
#     #     ]
#     #     return columns
#     else:
#         columns = [
#             {
#                 "label": _("Creation Date"),
#                 "fieldname": "material_request_date",
#                 "fieldtype": "Date",
#                 "width": 160
#             },
#             {
#                 "label": _("Serial No"),
#                 "options": "Material Request",
#                 "fieldname": "material_request_no",
#                 "fieldtype": "Link",
#                 "width": 180
#             },
#             {
#                 "label": _("Project"),
#                 "options": "Project",
#                 "fieldname": "project",
#                 "fieldtype": "Link",
#                 "width": 140
#             },
#             {
#                 "label": _("Creator"),
#                 "fieldname": "requestor",
#                 "fieldtype": "Data",
#                 "width": 140
#             },
#             {
#                 "label": _("Modified by"),
#                 "fieldname": "modify_by",
#                 "fieldtype": "Data",
#                 "width": 180
#             }
#         ]
#         return columns

    
# def get_data(conditions,data, filters):
#     v=filters.get('dc')
#     if(v=='Material Request'):
#         data=[]
#         mr_details = frappe.db.sql("""SELECT mr.name, mr.creation,mr.project,mr.request_purpose,mr.owner,mr.modified,mr.modified_by,mr.workflow_state
#             from `tabMaterial Request` as mr where mr.material_request_type='Purchase' and mr.workflow_state != 'Cancelled' and mr.workflow_state != 'Rejected' and mr.docstatus=0
#             {conditions}
#             """.format(conditions=conditions), as_dict=1)

#         for i in mr_details:
#             created=frappe.db.get_value("User",i.owner,"first_name")
#             if(i.workflow_state=='Approved by HOD' or i.workflow_state=='Approved by TD' or i.workflow_state=='Approved by ED' or i.workflow_state=='Approved by GM'):
#                 modify=frappe.db.get_value("User",i.modified_by,"first_name")
#             else:
#                 modify="Pending for HOD approval"

#             if(i.workflow_state=='Approved by HOD' or i.workflow_state=='Approved by TD' or i.workflow_state=='Approved by ED' or i.workflow_state=='Approved by GM'):
#                 approval_date=i.modified
#             else:
#                 approval_date="Pending for HOD approval"

#             if(modify=="Pending for HOD approval"):
#                 diff=datetime.now()-i.creation
#                 days=diff.days
#                 seconds = diff.total_seconds()
#                 hours = (seconds // 3600)%24
#                 minutes = ((seconds % 3600) // 60)%1440
#                 finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
#             else:
#                 diff=i.modified-i.creation
#                 days=diff.days
#                 seconds = diff.total_seconds()
#                 hours = (seconds // 3600)%24
#                 minutes = ((seconds % 3600) // 60)%1440
#                 finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
            
#             if(modify=="Pending for HOD approval"):
#                 finaldiff=""
#             else:
#                 diff2=datetime.now()-i.modified
#                 days=diff2.days
#                 seconds = diff2.total_seconds()
#                 hours = (seconds // 3600)%24
#                 minutes = ((seconds % 3600) // 60)%1440
#                 finaldiff=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
                
#             data.append({
#                 "material_request_date":i.creation,
#                 "material_request_no":i.name,
#                 "project":i.project,
#                 "rq_purpose":i.request_purpose,
#                 "requestor":created,
#                 "approval_date":approval_date,
#                 "modify_by":modify,
#                 "pending_days":finaldiff1,
#                 "pending_md":finaldiff
#             })
#         return data
    
#     elif(v=='Purchase Order'):
#         data=[]
#         mr_details = frappe.db.sql("""SELECT mr.name, mr.creation,mr.owner,mr.modified,mr.modified_by,mr.workflow_state,mr.project
#             from `tabPurchase Order` as mr where mr.workflow_state != 'Cancelled' and mr.workflow_state != 'Rejected' and mr.docstatus=0
#             {conditions}
#             """.format(conditions=conditions), as_dict=1)

#         for i in mr_details:
#             created=frappe.db.get_value("User",i.owner,"first_name")
#             if(i.workflow_state=='Approved by HOD' or i.workflow_state=='Approved by ED'):
#                 modify=frappe.db.get_value("User",i.modified_by,"first_name")
#             else:
#                 modify="Pending for HOD approval"

#             if(i.workflow_state=='Approved by HOD' or i.workflow_state=='Approved by ED'):
#                 approval_date=i.modified
#             else:
#                 approval_date="Pending for HOD approval"

#             if(approval_date=="Pending for HOD approval"):
#                 diff=datetime.now()-i.creation
#                 days=diff.days
#                 seconds = diff.total_seconds()
#                 hours = (seconds // 3600)%24
#                 minutes = ((seconds % 3600) // 60)%1440
#                 finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
#             else:
#                 diff=i.modified-i.creation
#                 days=diff.days
#                 seconds = diff.total_seconds()
#                 hours = (seconds // 3600)%24
#                 minutes = ((seconds % 3600) // 60)%1440
#                 finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "

#             if(modify=="Pending for HOD approval"):
#                 finaldiff=""
#             else:
#                 diff2=datetime.now()-i.modified
#                 days=diff2.days
#                 seconds = diff2.total_seconds()
#                 hours = (seconds // 3600)%24
#                 minutes = ((seconds % 3600) // 60)%1440
#                 finaldiff=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "

#             data.append({
#                 "material_request_date":i.creation,
#                 "material_request_no":i.name,
#                 "project":i.project,
#                 "requestor":created,
#                 "approval_date":approval_date,
#                 "modify_by":modify,
#                 "pending_days":finaldiff1,
#                 "pending_md":finaldiff
#             })
#         return data
    
#     elif(v=='Purchase Receipt'):
#         data=[]
#         mr_details = frappe.db.sql("""SELECT mr.name, mr.creation,mr.owner,mr.modified,mr.modified_by,mr.status,mr.project
#             from `tabPurchase Receipt` as mr where mr.status != 'Cancelled' and mr.docstatus=0
#             {conditions}
#             """.format(conditions=conditions), as_dict=1)

#         for i in mr_details:
#             diff=datetime.now()-i.creation
#             days=diff.days
#             seconds = diff.total_seconds()
#             hours = (seconds // 3600)%24
#             minutes = ((seconds % 3600) // 60)%1440
#             finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
#             created=frappe.db.get_value("User",i.owner,"first_name")
#             data.append({
#                 "material_request_date":i.creation,
#                 "material_request_no":i.name,
#                 "project":i.project,
#                 "requestor":created,
#                 "modify_by":"Pending for Approval",
#                 "pending_days":finaldiff1
#             })
#         return data

#     elif(v=='Purchase Invoice'):
#         data=[]
#         mr_details = frappe.db.sql("""SELECT mr.name, mr.creation,mr.owner,mr.modified,mr.modified_by,mr.status,mr.project
#             from `tabPurchase Invoice` as mr where mr.status != 'Cancelled' and mr.docstatus=0
#             {conditions}
#             """.format(conditions=conditions), as_dict=1)

#         for i in mr_details:
#             diff=datetime.now()-i.creation
#             days=diff.days
#             seconds = diff.total_seconds()
#             hours = (seconds // 3600)%24
#             minutes = ((seconds % 3600) // 60)%1440
#             finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
#             created=frappe.db.get_value("User",i.owner,"first_name")
#             data.append({
#                 "material_request_date":i.creation,
#                 "material_request_no":i.name,
#                 "project":i.project,
#                 "requestor":created,
#                 "modify_by":"Pending for Approval",
#                 "pending_days":finaldiff1
#             })
#         return data

#     # elif(v=='Sales Invoice'):
#     #     data=[]
#     #     mr_details = frappe.db.sql("""SELECT mr.name, mr.creation,mr.owner,mr.modified,mr.modified_by,mr.status
#     #         from `tabSales Invoice` as mr where mr.status != 'Cancelled' and mr.docstatus=0
#     #         {conditions}
#     #         """.format(conditions=conditions), as_dict=1)

#     #     for i in mr_details:
#     #         diff=datetime.now()-i.creation
#     #         days=diff.days
#     #         seconds = diff.total_seconds()
#     #         hours = (seconds // 3600)%24
#     #         minutes = ((seconds % 3600) // 60)%1440
#     #         finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
#     #         created=frappe.db.get_value("User",i.owner,"first_name")
#     #         data.append({
#     #             "material_request_date":i.creation,
#     #             "material_request_no":i.name,
#     #             "requestor":created,
#     #             "modify_by":"Pending for Approval",
#     #             "pending_days":finaldiff1
#     #         })
#     #     return data


# def get_conditions(filters):
#     conditions = ""
#     if filters.get("from_date"):
#         conditions += " AND mr.creation>='%s'" % filters.get('from_date')

#     if filters.get("to_date"):
#         conditions += " AND mr.creation<='%s'" % filters.get('to_date')

#     if filters.get("project"):
#         conditions += " AND mr.project='%s'" % filters.get('project')
#     return conditions


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

@frappe.whitelist()
def get_columns(filters):
    v=filters.get('dc')
    if(v=='Material Request'):
        columns = [
            {
                "label": _("Creation Date"),
                "fieldname": "material_request_date",
                "fieldtype": "Date",
                "width": 160
            },
            {
                "label": _("MR No"),
                "options": "Material Request",
                "fieldname": "material_request_no",
                "fieldtype": "Link",
                "width": 180
            },
            {
                "label": _("Project"),
                "options": "Project",
                "fieldname": "project",
                "fieldtype": "Link",
                "width": 90
            },
            {
                "label": _("Request Purpose"),
                "fieldname": "rq_purpose",
                "fieldtype": "Data",
                "width": 220
            },
            {
                "label": _("Creator"),
                "fieldname": "requestor",
                "fieldtype": "Data",
                "width": 140
            },
            {
                "label": _("HOD approved Date"),
                "fieldname": "approval_date",
                "fieldtype": "Date",
                "width": 160
            },
            {
                "label": _("Modified by"),
                "fieldname": "modify_by",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": _("Pending days"),
                "fieldname": "pending_days",
                "fieldtype": "Float",
                "width": 120
            },
            {
                "label": _("Pending days For MD"),
                "fieldname": "pending_md",
                "fieldtype": "Float",
                "width": 160
            }
        ]
        return columns
    elif(v=='Purchase Order'):
        columns = [
            {
                "label": _("Creation Date"),
                "fieldname": "material_request_date",
                "fieldtype": "Date",
                "width": 160
            },
            {
                "label": _("PO No"),
                "options": "Purchase Order",
                "fieldname": "material_request_no",
                "fieldtype": "Link",
                "width": 180
            },
            {
                "label": _("Project"),
                "options": "Project",
                "fieldname": "project",
                "fieldtype": "Link",
                "width": 90
            },
            {
                "label": _("Creator"),
                "fieldname": "requestor",
                "fieldtype": "Data",
                "width": 140
            },
            {
                "label": _("HOD approved Date"),
                "fieldname": "approval_date",
                "fieldtype": "Date",
                "width": 160
            },
            {
                "label": _("Modified by"),
                "fieldname": "modify_by",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": _("Pending days"),
                "fieldname": "pending_days",
                "fieldtype": "Float",
                "width": 120
            },
            {
                "label": _("Pending days For MD"),
                "fieldname": "pending_md",
                "fieldtype": "Float",
                "width": 160
            }
        ]
        return columns
    elif(v=='Purchase Receipt'):
        columns = [
            {
                "label": _("Creation Date"),
                "fieldname": "material_request_date",
                "fieldtype": "Date",
                "width": 160
            },
            {
                "label": _("PR No"),
                "options": "Purchase Receipt",
                "fieldname": "material_request_no",
                "fieldtype": "Link",
                "width": 180
            },
            {
                "label": _("Project"),
                "options": "Project",
                "fieldname": "project",
                "fieldtype": "Link",
                "width": 90
            },
            {
                "label": _("Creator"),
                "fieldname": "requestor",
                "fieldtype": "Data",
                "width": 140
            },
            {
                "label": _("Modified by"),
                "fieldname": "modify_by",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": _("Pending days"),
                "fieldname": "pending_days",
                "fieldtype": "Float",
                "width": 180
            }
        ]
        return columns

    elif(v=='Purchase Invoice'):
        columns = [
            {
                "label": _("Creation Date"),
                "fieldname": "material_request_date",
                "fieldtype": "Date",
                "width": 160
            },
            {
                "label": _("Invoice No"),
                "options": "Purchase Invoice",
                "fieldname": "material_request_no",
                "fieldtype": "Link",
                "width": 180
            },
            {
                "label": _("Project"),
                "options": "Project",
                "fieldname": "project",
                "fieldtype": "Link",
                "width": 90
            },
            {
                "label": _("Creator"),
                "fieldname": "requestor",
                "fieldtype": "Data",
                "width": 140
            },
            {
                "label": _("Modified by"),
                "fieldname": "modify_by",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": _("Pending days"),
                "fieldname": "pending_days",
                "fieldtype": "Float",
                "width": 180
            }
        ]
        return columns

    else:
        columns = [
            {
                "label": _("Creation Date"),
                "fieldname": "material_request_date",
                "fieldtype": "Date",
                "width": 160
            },
            {
                "label": _("Serial No"),
                "options": "Material Request",
                "fieldname": "material_request_no",
                "fieldtype": "Link",
                "width": 180
            },
            {
                "label": _("Project"),
                "options": "Project",
                "fieldname": "project",
                "fieldtype": "Link",
                "width": 140
            },
            {
                "label": _("Creator"),
                "fieldname": "requestor",
                "fieldtype": "Data",
                "width": 140
            },
            {
                "label": _("Modified by"),
                "fieldname": "modify_by",
                "fieldtype": "Data",
                "width": 180
            }
        ]
        return columns

    
def get_data(conditions,data, filters):
    v=filters.get('dc')
    if(v=='Material Request'):
        data=[]
        mr_details = frappe.db.sql("""SELECT mr.name, mr.creation,mr.project,mr.request_purpose,mr.owner,mr.modified,mr.modified_by,mr.workflow_state
            from `tabMaterial Request` as mr where mr.material_request_type='Purchase' and mr.workflow_state != 'Cancelled' and mr.workflow_state != 'Rejected' and mr.docstatus=0
            {conditions}
            """.format(conditions=conditions), as_dict=1)

        for i in mr_details:
            created=frappe.db.get_value("User",i.owner,"first_name")
            if(i.workflow_state=='Approved by HOD' or i.workflow_state=='Approved by TD' or i.workflow_state=='Approved by ED' or i.workflow_state=='Approved by GM'):
                modify=frappe.db.get_value("User",i.modified_by,"first_name")
            else:
                modify="Pending for HOD approval"

            if(i.workflow_state=='Approved by HOD' or i.workflow_state=='Approved by TD' or i.workflow_state=='Approved by ED' or i.workflow_state=='Approved by GM'):
                approval_date=i.modified
            else:
                approval_date="Pending for HOD approval"

            if(modify=="Pending for HOD approval"):
                diff=datetime.now()-i.creation
                days=diff.days
                seconds = diff.total_seconds()
                hours = (seconds // 3600)%24
                minutes = ((seconds % 3600) // 60)%1440
                # finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
                finaldiff1 = float(days)
            else:
                diff=i.modified-i.creation
                days=diff.days
                seconds = diff.total_seconds()
                hours = (seconds // 3600)%24
                minutes = ((seconds % 3600) // 60)%1440
                # finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
                finaldiff1 = float(days)
            
            if(modify=="Pending for HOD approval"):
                finaldiff=""
            else:
                diff2=datetime.now()-i.modified
                days=diff2.days
                seconds = diff2.total_seconds()
                hours = (seconds // 3600)%24
                minutes = ((seconds % 3600) // 60)%1440
                # finaldiff=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
                finaldiff=float(days)
                
            data.append({
                "material_request_date":i.creation,
                "material_request_no":i.name,
                "project":i.project,
                "rq_purpose":i.request_purpose,
                "requestor":created,
                "approval_date":approval_date,
                "modify_by":modify,
                "pending_days":finaldiff1,
                "pending_md":finaldiff
            })
            data = sorted(data, key=lambda x: x["pending_days"] if x.get("modify_by") == "Pending for HOD approval" else 0, reverse=True)
        return data
    
    elif(v=='Purchase Order'):
        data=[]
        mr_details = frappe.db.sql("""SELECT mr.name, mr.creation,mr.owner,mr.modified,mr.modified_by,mr.workflow_state,mr.project
            from `tabPurchase Order` as mr where mr.workflow_state != 'Cancelled' and mr.workflow_state != 'Rejected' and mr.docstatus=0
            {conditions}
            """.format(conditions=conditions), as_dict=1)

        for i in mr_details:
            created=frappe.db.get_value("User",i.owner,"first_name")
            if(i.workflow_state=='Approved by HOD' or i.workflow_state=='Approved by ED'):
                modify=frappe.db.get_value("User",i.modified_by,"first_name")
            else:
                modify="Pending for HOD approval"

            if(i.workflow_state=='Approved by HOD' or i.workflow_state=='Approved by ED'):
                approval_date=i.modified
            else:
                approval_date="Pending for HOD approval"

            if(approval_date=="Pending for HOD approval"):
                diff=datetime.now()-i.creation
                days=diff.days
                seconds = diff.total_seconds()
                hours = (seconds // 3600)%24
                minutes = ((seconds % 3600) // 60)%1440
                # finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
                finaldiff1 = float(days)
            else:
                diff=i.modified-i.creation
                days=diff.days
                seconds = diff.total_seconds()
                hours = (seconds // 3600)%24
                minutes = ((seconds % 3600) // 60)%1440
                # finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
                finaldiff1 = float(days)

            if(modify=="Pending for HOD approval"):
                finaldiff=0
            else:
                diff2=datetime.now()-i.modified
                days=diff2.days
                seconds = diff2.total_seconds()
                hours = (seconds // 3600)%24
                minutes = ((seconds % 3600) // 60)%1440
                # finaldiff=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
                finaldiff=float(days)

            data.append({
                "material_request_date":i.creation,
                "material_request_no":i.name,
                "project":i.project,
                "requestor":created,
                "approval_date":approval_date,
                "modify_by":modify,
                "pending_days":finaldiff1,
                "pending_md":finaldiff
            })
            data = sorted(data, key=lambda x: x["pending_days"] if x.get("modify_by") == "Pending for HOD approval" else 0, reverse=True)
        return data
    
    elif(v=='Purchase Receipt'):
        data=[]
        mr_details = frappe.db.sql("""SELECT mr.name, mr.creation,mr.owner,mr.modified,mr.modified_by,mr.status,mr.project
            from `tabPurchase Receipt` as mr where mr.status != 'Cancelled' and mr.docstatus=0
            {conditions}
            """.format(conditions=conditions), as_dict=1)

        for i in mr_details:
            diff=datetime.now()-i.creation
            days=diff.days
            seconds = diff.total_seconds()
            hours = (seconds // 3600)%24
            minutes = ((seconds % 3600) // 60)%1440
            # finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
            finaldiff1=float(days)
            created=frappe.db.get_value("User",i.owner,"first_name")
            data.append({
                "material_request_date":i.creation,
                "material_request_no":i.name,
                "project":i.project,
                "requestor":created,
                "modify_by":"Pending for Approval",
                "pending_days":finaldiff1
            })
            data = sorted(data, key=lambda x: x["pending_days"], reverse=True)
        return data

    elif(v=='Purchase Invoice'):
        data=[]
        mr_details = frappe.db.sql("""SELECT mr.name, mr.creation,mr.owner,mr.modified,mr.modified_by,mr.status,mr.project
            from `tabPurchase Invoice` as mr where mr.status != 'Cancelled' and mr.docstatus=0
            {conditions}
            """.format(conditions=conditions), as_dict=1)

        for i in mr_details:
            diff=datetime.now()-i.creation
            days=diff.days
            seconds = diff.total_seconds()
            hours = (seconds // 3600)%24
            minutes = ((seconds % 3600) // 60)%1440
            # finaldiff1=str(days)+"d "+str(int(hours))+"h "+str(int(minutes))+"m "
            finaldiff1=float(days)
            created=frappe.db.get_value("User",i.owner,"first_name")
            data.append({
                "material_request_date":i.creation,
                "material_request_no":i.name,
                "project":i.project,
                "requestor":created,
                "modify_by":"Pending for Approval",
                "pending_days":finaldiff1
            })
            data = sorted(data, key=lambda x: x["pending_days"], reverse=True)
        return data

def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND mr.creation>='%s'" % filters.get('from_date')

    if filters.get("to_date"):
        conditions += " AND mr.creation<='%s'" % filters.get('to_date')

    if filters.get("project"):
        conditions += " AND mr.project='%s'" % filters.get('project')
    return conditions