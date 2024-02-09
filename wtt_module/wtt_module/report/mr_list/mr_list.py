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
            "label": _("Employee"),
            "fieldname": "employee",
            "fieldtype": "Data",
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
            "label": _("Project"),
            "options": "Project",
            "fieldname": "project",
            "fieldtype": "Link",
            "width": 150
        },
        {
        	"label":"Status",
        	"fieldname":"workflow_state",
        	"fieldtype":"Data",
        	"width":200
        }
    ]
    return columns

    
def get_data(conditions,data, filters):
    data=[]
    mr_details = frappe.db.sql("""SELECT mr.name, mr.creation,mr.project,mr.request_purpose,mr.owner,mr.modified,mr.modified_by,mr.workflow_state
        from `tabMaterial Request` as mr where mr.material_request_type='Purchase' 
            {conditions}
            """.format(conditions=conditions), as_dict=1)
    for i in mr_details:
        created=frappe.db.get_value("User",i.owner,"first_name")
        
        data.append({
            "employee":created,
            "material_request_no":i.name,
            "project":i.project,
            "workflow_state":i.workflow_state
        })
    return data
    
  


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND mr.creation>='%s'" % filters.get('from_date')

    if filters.get("to_date"):
        conditions += " AND mr.creation<='%s'" % filters.get('to_date')

    if filters.get("emp"):
    	query=frappe.db.sql("SELECT user_id FROM `tabEmployee` WHERE employee='%s'"% filters.get('emp'),as_dict=1)
    	for i in query:
        	conditions += " AND mr.owner ='"+i.user_id+"'"

    if filters.get("project"):
        conditions += " AND mr.project='%s'" % filters.get('project')

    if filters.get("status"):
        conditions += " AND mr.workflow_state='%s'" % filters.get('status')
    return conditions

   