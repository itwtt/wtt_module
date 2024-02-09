from __future__ import unicode_literals
import frappe
from datetime import datetime
from frappe import _
import numpy as np
from frappe.desk.reportview import build_match_conditions
import json

def execute(filters=None):        
    if not filters:
        return [], []
    data = []
    columns = get_columns(filters)
    data = get_data(data,filters)
    return columns, data

def get_columns(filters):
    if(filters.payment_type=='Pay'):
        columns=[
            {
                "label": _("Company"),
                "fieldtype": "Data",
                "fieldname": "company",
                "width": 150
            },
            {
                "label": _("Paid Date"),
                "fieldtype": "Data",
                "fieldname": "paid_date",
                "width": 100
            },
            {
                "label": _("Sites"),
                "fieldtype": "Data",
                "fieldname": "sites",
                "width": 100
            },
            {
                "label": _("Remarks"),
                "fieldtype": "Data",
                "fieldname": "remarks",
                "width": 550
            },
            {
                "label": _("Amount"),
                "fieldtype": "Float",
                "fieldname": "amount",
                "width": 120
            },
            {
                "label": _("Journal Entry"),
                "fieldtype": "Link",
                "fieldname": "journal_entry",
                "options":"Journal Entry",
                "width": 50
            },
            {
                "label": _("Payment Type"),
                "fieldtype": "Data",
                "fieldname": "payment_type",
                "width": 50
            }
        ]
    elif(filters.payment_type=='Receive'):
        columns=[
            {
                "label": _("Company"),
                "fieldtype": "Data",
                "fieldname": "company",
                "width": 150
            },
            {
                "label": _("Received Date"),
                "fieldtype": "Data",
                "fieldname": "paid_date",
                "width": 100
            },
            {
                "label": _("Sites"),
                "fieldtype": "Data",
                "fieldname": "sites",
                "width": 100
            },
            {
                "label": _("Remarks"),
                "fieldtype": "Data",
                "fieldname": "remarks",
                "width": 550
            },
            {
                "label": _("Amount"),
                "fieldtype": "Float",
                "fieldname": "amount",
                "width": 120
            },
            {
	            "label": _("Journal Entry"),
                "fieldtype": "Link",
                "fieldname": "journal_entry",
                "options":"Journal Entry",
                "width": 50
            },
            {
                "label": _("Payment Type"),
                "fieldtype": "Data",
                "fieldname": "payment_type",
                "width": 50
            }
        ]
    elif(filters.payment_type=='--Select--'):
        columns=[
            {
                "label": _("Company"),
                "fieldtype": "Data",
                "fieldname": "company",
                "width": 150
            },
            {
                "label": _("Payment Type"),
                "fieldtype": "Data",
                "fieldname": "payment_type",
                "width": 100
            },
            {
                "label": _("Sites"),
                "fieldtype": "Data",
                "fieldname": "sites",
                "width": 100
            },
            {
                "label": _("Date"),
                "fieldtype": "Data",
                "fieldname": "paid_date",
                "width": 100
            },
            {
                "label": _("Remarks"),
                "fieldtype": "Data",
                "fieldname": "remarks",
                "width": 450
            },
            {
                "label": _("Amount"),
                "fieldtype": "Float",
                "fieldname": "amount",
                "width": 110
            },
            {
	            "label": _("Journal Entry"),
                "fieldtype": "Link",
                "fieldname": "journal_entry",
                "options":"Journal Entry",
                "width": 160
            }
        ]
    return columns

def get_data(data, filters):
    data=[]
    if(filters.payment_type=='--Select--'):
        cash_entry = frappe.db.sql(""" SELECT name,journal_name,payment_type,sites,posting_date,paid_date,company,received_date,user_remark,total_credit FROM `tabPre Journal Entry` WHERE docstatus=0 and workflow_state='Created' and company=%(company)s order by journal_name asc""", filters, as_dict=1) 	
        for i in cash_entry:
            val=i.posting_date
            if(i.payment_type=='Pay'):
                val=i.paid_date
            elif(i.payment_type=='Receive'):
                val=i.received_date
            vis=val.strftime("%d/%m/%y")
            data.append({
                "company":i.company,
                "journal_entry":str(i.journal_name),
                "payment_type":i.payment_type,
                "sites":i.sites,
                "paid_date":vis,
                "remarks":str(i.user_remark),
                "amount":i.total_credit            
            })


    else:
        cash_entry = frappe.db.sql(""" SELECT name,journal_name,payment_type,sites,posting_date,paid_date,company,received_date,user_remark,total_credit FROM `tabPre Journal Entry` WHERE docstatus=0 and workflow_state='Created' and payment_type=%(payment_type)s and company=%(company)s order by journal_name asc""",filters , as_dict=1) 
        for i in cash_entry:
            if(i.payment_type=='Pay'):
                val=i.paid_date
                data.append({
                    "company":i.company,
                    "journal_entry":str(i.journal_name),
                    "payment_type":i.payment_type,
                    "sites":i.sites,
                    "paid_date":val.strftime("%d/%m/%y"),
                    "remarks":str(i.user_remark),
                    "amount":i.total_credit            
                })
            elif(i.payment_type=='Receive'):
                gug=i.received_date
                data.append({
                    "company":i.company,
                    "journal_entry":str(i.journal_name),
                    "payment_type":str(i.payment_type),
                    "sites":i.sites,
                    "paid_date":gug.strftime("%d/%m/%y"),
                    "remarks":str(i.user_remark),
                    "amount":i.total_credit           
                })    
            
    return data


@frappe.whitelist()
def function(lr_name):
    user=frappe.session.user
    if(user=='venkat@wttindia.com' or user=='sarnita@wttindia.com' or user=='Administrator'):
        doc=frappe.get_last_doc('Pre Journal Entry', filters={"journal_name": lr_name})
        doc.submit()
        frappe.msgprint("Approved")
    else:
        frappe.throw("Not Permitted to Approve")

@frappe.whitelist()
def func(lt_name):
    user=frappe.session.user
    if(user=='venkat@wttindia.com' or user=='sarnita@wttindia.com' or user=='Administrator'):
        dop = frappe.get_last_doc('Pre Journal Entry', filters={"journal_name": lt_name})
        dop.docstatus=0
        dop.workflow_state='Rejected'
        dop.save()
        doc=frappe.get_doc("Journal Entry",lt_name)
        doc.cancel()
        frappe.msgprint("Cancelled")
    else:
        frappe.throw("Not Permitted to Cancel")
