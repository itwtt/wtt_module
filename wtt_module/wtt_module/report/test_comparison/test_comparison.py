# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
import json
from frappe.model.mapper import get_mapped_doc
from datetime import date

def execute(filters=None):
    if not filters:
        return [], []
    data = []
    columns = get_columns(filters)
    data = get_data(data , filters)
    return columns, data

def get_columns(filters):
    columns=[
        {
            "label": _("Description"),
            "fieldtype": "HTML",
            "fieldname": "description",
            "width": 150
        },        
        {
            "label": _("Technical Description"),
            "fieldtype": "Data",
            "fieldname": "technical_description",
            "width": 200
        },
        {
            "label": _("MR Qty"),
            "fieldtype": "Data",
            "fieldname": "mr_qty",
            "width": 100
        }
    ]
    val=frappe.db.sql("SELECT supplier FROM `tabSupplier Quotation` WHERE request_for_quotation=%(request_for_quotation)s and revision='Final Revision'",filters,as_dict=1)
    for i in val:
        
        columns.append({
            "fieldname": i.supplier+"qty",
            "label": "Qty"+" - "+i.supplier,
            #"label": i.supplier+" - "+"Qty",
            "fieldtype": "HTML",
            "width": 100
        })
    # for i in val:
    #     columns.append({
    #         "fieldname": i.supplier+"gst",
    #         "label": "GST"+" - "+i.supplier,
    #         #"label": i.supplier+" - "+"Gst",
    #         "fieldtype": "Data",
    #         "width": 120
    #     })
    # for i in val:
        columns.append({
            "fieldname": i.supplier+"rate",
            "label": "Price"+" - "+i.supplier,
            #"label": i.supplier+" - "+"Price",
            "fieldtype": "Data",
            "width": 120
        })
    for i in val:
        columns.append({
            "fieldname": i.supplier+"amount",
            "label": "Amount"+" - "+i.supplier,
            #"label": i.supplier+" - "+"Amount",
            "fieldtype": "HTML",
            "width": 120
        })
    for i in val:
        columns.append({
            "fieldname": i.supplier+"description",
            "label": "Supplier Description"+" - "+i.supplier,
            #"label": i.supplier+" - "+"Supplier Description",
            "fieldtype": "Small Text",
            "width": 300
        })
    columns.append({
        "label": _("Item Code"),
        "fieldtype": "Data",
        "fieldname": "item_code",
        "width": 50
    })       
    return columns

def get_data(data, filters):
    data=[]
    to_be_compared_items = frappe.db.sql("SELECT soi.parent,sq.supplier_name,soi.item_code,soi.approval,soi.item_name,soi.description,soi.technical_description,soi.qty,soi.mr_qty,soi.item_tax_template,soi.rate2,soi.amount2,soi.name,soi.supplier_description,soi.rate_inr,soi.amount_inr FROM `tabSQ Combined Table` as soi,`tabSupplier Quotation` as sq WHERE sq.name = soi.parent and sq.request_for_quotation = %(request_for_quotation)s AND sq.workflow_state!='Cancelled' AND sq.workflow_state!='Rejected' AND sq.transaction_date between %(from_date)s and %(to_date)s",filters,as_dict = 1)
    query=frappe.db.sql("SELECT name,workflow_state,total_taxes_and_charges,supplier_name,others,make,freight_amount,p_and_f,gst,grand_total,total,price_basis,delivary_time,payment_terms,warranty FROM `tabSupplier Quotation` WHERE request_for_quotation=%(request_for_quotation)s",filters,as_dict=1)
    items_dict = {}
    temp_list = []
    for item in to_be_compared_items:
        temp_list.append(item.item_code)
    unique_item = set(temp_list)

    column1={}
    for item in query:
        column1['description'] = "Make"
        column1[item.supplier_name + 'amount'] = item.make
    data.append(column1)
    
    column10={}
    for item in query:
        column10['description'] = "SQ No"
        if(item.workflow_state=='Approved'):
            column10[item.supplier_name + 'amount'] = "<p style='background-color:lightgreen;color:black;'><b>"+str(item.name)+"</b></p>"
        if(item.workflow_state=='Rejected'):
            column10[item.supplier_name + 'amount'] = "<p style='background-color:#FF6666;color:black;'><b>"+str(item.name)+"</b></p>"
        if(item.workflow_state=='Created' or item.workflow_state=='Approved by HOD'):
            column10[item.supplier_name + 'amount'] = "<b>"+str(item.name)+"</b>"
    data.append(column10)
    
    for item in unique_item:
        column = {}
        for datum in to_be_compared_items:
            if item == datum.item_code:
                column['item_code'] = datum.item_code
                column['description'] = datum.description
                column['technical_description']=datum.technical_description
                column['mr_qty'] = str(datum.mr_qty)
                if(datum.approval=='Approved'):
                    column[datum.supplier_name + 'qty'] = "<p style='background-color:lightgreen;color:black;'><b>"+str(datum.qty)+"</b></p>"
                    #column[datum.supplier_name + 'qty'] = str(datum.qty)+" - "+"(A)"
                elif(datum.approval=='Rejected'):
                    column[datum.supplier_name + 'qty'] = "<p style='background-color:#FF6666;color:black;'><b>"+str(datum.qty)+"</b></p>"
                    #column[datum.supplier_name + 'qty'] = str(datum.qty)+" - "+"(R)"
                else:
                    column[datum.supplier_name + 'qty'] = datum.qty
                column[datum.supplier_name + 'gst'] = datum.item_tax_template
                if(datum.rate_inr<=0):
                    column[datum.supplier_name + 'rate'] = datum.rate2
                    column[datum.supplier_name + 'amount'] = datum.amount2
                else:
                    column[datum.supplier_name + 'rate'] = datum.rate_inr
                    column[datum.supplier_name + 'amount'] = datum.amount_inr
                column[datum.supplier_name + 'description'] = datum.supplier_description
        data.append(column)
    
    column2={}
    for item in query:
        column2['description'] = "Basic Total"
        column2[item.supplier_name + 'amount'] = item.total
    column3={}
    for item in query:
        column3['description'] = "Freight Amount"
        column3[item.supplier_name + 'amount'] = item.freight_amount
    column4={}
    for item in query:
        column4['description'] = "P & F"
        column4[item.supplier_name + 'amount'] = item.p_and_f
    column5={}
    gv=[]
    for item in query:
        gv.append(item.grand_total)
        #column5['description'] = "Grand Total"
        #column5[item.supplier_name + 'amount'] = item.grand_total
    
    maximum = max(gv)
    minimum = min(gv)
    for item in query:
        if(item.grand_total==maximum):
            column5['description'] = "<p><b>Grand Total</b></p>"
            column5[item.supplier_name + 'amount'] = "<p style='background-color:#FF6666;color:black'><b>"+str(item.grand_total)+"</b></p>"
        if(item.grand_total==minimum):
            column5['description'] = "<p><b>Grand Total</b></p>"
            column5[item.supplier_name + 'amount'] = "<p style='background-color:lightgreen;color:black'><b>"+str(item.grand_total)+"</b></p>"
        if(item.grand_total!=minimum and item.grand_total!=maximum):
            column5['description'] = "<p><b>Grand Total</b></p>"
            column5[item.supplier_name + 'amount'] = "<p style='background-color:orange;color:black'><b>"+str(item.grand_total)+"</b></p>"

    column6={}
    for item in query:
        column6['description'] = "Price Basis"
        column6[item.supplier_name + 'amount'] = item.price_basis
    column7={}
    for item in query:
        column7['description'] = "Payment Terms"
        column7[item.supplier_name + 'amount'] = item.payment_terms
    column8={}
    for item in query:
        column8['description'] = "Warranty"
        column8[item.supplier_name + 'amount'] = item.warranty
    column9={}
    for item in query:
        column9['description'] = "Delivary Time"
        column9[item.supplier_name + 'amount'] = item.delivary_time
    column12={}
    for item in query:
        column12['description'] = "Others"
        column12[item.supplier_name + 'amount'] = item.others
    column11={}
    for item in query:
        column11['description'] = "Workflow status"
        column11[item.supplier_name + 'amount'] = item.workflow_state

    column13={}
    for item in query:
        column13['description'] = "GST"
        if(item.freight_amount is not None):
            column13[item.supplier_name + 'amount'] = float(item.total_taxes_and_charges)-float(item.freight_amount)
    data.append(column2)
    data.append(column3)
    data.append(column13)
    data.append(column5)
    data.append(column4)
    data.append(column6)
    data.append(column7)
    data.append(column8)
    data.append(column9)
    data.append(column12)
    data.append(column11)
    return data

@frappe.whitelist()
def fun(rfq1,item_code):
    ar=[]
    a22=[]
    qq = frappe.db.sql("SELECT name,supplier FROM `tabSupplier Quotation` where request_for_quotation = '"+str(rfq1)+"' AND revision='Final Revision'",as_dict = 1)
    for i in qq:
        ar.append(i.supplier)
        a22.append(i.name)
    return ar,a22

@frappe.whitelist()
def fun_make2(sq,itc):
    arq=[]
    qq = frappe.db.sql("SELECT soi.qty, soi.rate, soi.amount,soi.name,soi.item_code,sq.currency,sq.conversion_rate FROM `tabSupplier Data Table` as soi inner join `tabSupplier Quotation` as sq on sq.name = soi.parent where sq.name = '"+str(sq)+"' AND soi.item_code='"+str(itc)+"' AND revision='Final Revision'",as_dict = 1)
    qqq = frappe.db.sql("SELECT sq.supplier,soi.qty, soi.rate2, soi.amount2,soi.name,soi.item_code,sq.currency,sq.conversion_rate FROM `tabSQ Combined Table` as soi inner join `tabSupplier Quotation` as sq on sq.name = soi.parent where sq.name = '"+str(sq)+"' AND soi.item_code='"+str(itc)+"' AND revision='Final Revision'",as_dict = 1)
    for j in qqq:
        for i in qq:
            if(i.item_code==j.item_code):
                arq.append({
                "supplier":j.supplier,
                "material_request":j.material_request,
                "qty":j.qty,
                "rate":j.rate2,
                "amount":j.amount2,
                "mr_name":j.name,
                "sup_qty":i.qty,
                "sup_rate":i.rate,
                "sup_amount":i.amount,
                "sup_mr_name":i.name,
                "currency":i.currency,
                "cr":i.conversion_rate
                })
    return arq

@frappe.whitelist()
def fun_make(sq,itc):
    arq=[]
    
    qqq = frappe.db.sql("SELECT sq.supplier,soi.qty, soi.rate2, soi.amount2,soi.name FROM `tabSQ Combined Table` as soi inner join `tabSupplier Quotation` as sq on sq.name = soi.parent where sq.name = '"+str(sq)+"' AND soi.item_code='"+str(itc)+"' AND revision='Final Revision'",as_dict = 1)
    for j in qqq:
        arq.append({
        "supplier":j.supplier,
        "material_request":j.material_request,
        "qty":j.qty,
        "rate":j.rate2,
        "amount":j.amount2,
        "mr_name":j.name
        })
    return arq


@frappe.whitelist()
def update_supplier_quotation(item_code,sq,mr,supplier,qty,rate,amt,mr_name,rate_inr,amount_inr):
    ar=[]
    br=[]
    mmar=[]
    v=frappe.db.sql("UPDATE `tabSQ Combined Table` SET qty='"+str(qty)+"',rate2='"+str(rate)+"',amount2='"+str(amt)+"',rate_inr='"+str(rate_inr)+"',amount_inr='"+str(amount_inr)+"',approval='Approved' WHERE parent='"+str(sq)+"' and name='"+str(mr_name)+"' ",as_dict=1)
    
    doc=frappe.get_doc("Supplier Quotation",sq)
    for i in doc.get("items"):
        ar.append(i.approval)
        if(i.item_code==item_code):
            i.quoted_qty=str(qty)
            i.rate=str(rate)
            i.approval='Approved'
    doc.save()


    # for i in frappe.db.sql("SELECT qty,item_code,rate,name FROM `tabSupplier Quotation Item` WHERE parent='"+str(sq)+"' and item_code='"+str(item_code)+"' ",as_dict=1):
    #     if(i.item_code==item_code):
    #         ar.append(i.qty)
    #         br.append(str(i.name))
    # ss=sum(float(aa) for aa in ar)
    # if(ss==int(qty)):
    #     vv=0
    # elif(ss<int(qty)):
    #     frappe.throw("Oops! But the Quoted Quantity is "+str(ss))
    # else:
    #     if(ss>int(qty)):
    #         vv=ss-int(qty)
    #     else:
    #         vv=int(qty)-ss
    # doc=frappe.get_doc("Supplier Quotation",sq)
    # for i in doc.get("items"):
    #     if(i.item_code==item_code and i.name==br[0] and i.qty>(i.qty-vv)):
    #         i.qty=i.qty-vv
    #         i.rate=rate
    #         i.amount=(i.qty-vv)*int(rate)
    # doc.save()
    # frappe.msgprint("Perfectly Updated On individual Item")
    return v


# @frappe.whitelist()
# def approvesq(parent,item_code,user,quoted_qty):
#     ar=[]
#     # frappe.db.sql("UPDATE `tabSupplier Quotation Item` SET approval='Approved' WHERE parent='"+str(parent)+"' and item_code='"+str(item_code)+"' ",as_dict=1)
#     frappe.db.sql("UPDATE `tabSQ Combined Item` SET approval='Approved' WHERE parent='"+str(parent)+"' and item_code='"+str(item_code)+"' ",as_dict=1)
#     doc=frappe.get_doc("Supplier Quotation",parent)
#     for i in doc.get('items'):
#         ar.append(i.approval)
#     if('Rejected' not in ar):
#         doc.docstatus=0
#         doc.workflow_state='Approved by HOD'
#     doc.save()
@frappe.whitelist()
def approvesq(sq,supplier):
    ar=[]
    for j in frappe.db.sql("SELECT sqi.qty,sqi.item_code FROM `tabSupplier Quotation`as sq,`tabSQ Combined Table`as sqi WHERE sq.name=sqi.parent and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqi.approval!='Rejected' ",as_dict=1):
        frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSupplier Quotation Item`as sqt SET sqt.approval='Approved',sqt.quoted_qty='"+str(j.qty)+"' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(j.item_code)+"' ",as_dict=1)
    doc=frappe.get_doc("Supplier Quotation",sq)
    for i in doc.get('items'):
        ar.append(i.approval)
    if('Rejected' not in ar):
        doc.docstatus=1
        doc.workflow_state='Approved'
    else:
        frappe.msgprint("Some items were Rejected")
    doc.submit()
@frappe.whitelist()
def rejectsq(sq,supplier):
    ar=[]
    doc=frappe.get_doc("Supplier Quotation",sq)
    for i in doc.get('items'):
        ar.append(i.approval)
    if('Approved' not in ar):
        frappe.db.sql("UPDATE `tabSupplier Quotation` SET docstatus=0,workflow_state='Rejected' WHERE name='"+str(sq)+"' and supplier='"+str(supplier)+"' ")
    else:
        frappe.msgprint("Some items were Approved")

@frappe.whitelist()
def rejectitc(sq,item_code,item,supplier):
    array = json.loads(item)
    for i in array:    
        frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSQ Combined Table`as sqt SET sqt.approval='Rejected' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)

        frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSupplier Quotation Item`as sqt SET sqt.approval='Rejected' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)
@frappe.whitelist()
def approveitc(sq,item_code,item,supplier):
    array = json.loads(item)
    for i in array:
        frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSQ Combined Table`as sqt SET sqt.approval='Approved' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)
        for j in frappe.db.sql("SELECT sqi.qty FROM `tabSupplier Quotation`as sq,`tabSQ Combined Table`as sqi WHERE sq.name=sqi.parent and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqi.item_code='"+str(i["it"])+"' ",as_dict=1):
            frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSupplier Quotation Item`as sqt SET sqt.approval='Approved',sqt.quoted_qty='"+str(j.qty)+"' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)

@frappe.whitelist()
def fun12(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.ignore_pricing_rule = 1
        target.run_method("set_missing_values")
        target.run_method("get_schedule_dates")
        target.run_method("calculate_taxes_and_totals")

    def update_item(obj, target, source_parent):
        target.schedule_date=date.today()
        target.stock_qty = float(obj.qty) * float(obj.conversion_factor)

    doclist = get_mapped_doc("Supplier Quotation", source_name,     {
        "Supplier Quotation": {
            "doctype": "Purchase Order",
            "validation": {
                "docstatus": ["=", 1],
            }
        },
        "Supplier Quotation Item": {
            "doctype": "Purchase Order Item",
            "field_map": [
                ["name", "supplier_quotation_item"],
                ["parent", "supplier_quotation"],
                ["material_request", "material_request"],
                ["material_request_item", "material_request_item"],
                ["sales_order", "sales_order"]
            ],
            "postprocess": update_item,
            "condition": lambda doc: doc.approval=="Approved" and doc.qty>0
        },
        "SQ Combined Table": {
            "doctype": "PO Combined Table",
            "field_map": [
                ["price_list_rate2","price_list_rate"],
                ["discount_percentage2","discount_percentage"],
                ["discount_amount2","discount_amount"],
                ["rate2","rate"],
                ["amount2","amount"],
                ["name", "sq_combined_item"],
                ["parent", "supplier_quotation"],
                ["material_request", "material_request"],
                ["material_request_item", "material_request_item"],
                ["sales_order", "sales_order"]
            ],
            "postprocess": update_item,
            "condition": lambda doc: doc.approval=="Approved" and doc.qty>0
        },
        "Purchase Taxes and Charges": {
            "doctype": "Purchase Taxes and Charges",
        }
    }, target_doc, set_missing_values)

    doclist.save()
    return doclist

@frappe.whitelist()
def suppliername(sqi,new_ar):
    aa=""
    to_python=json.loads(new_ar)
    for k in to_python:
        for i in frappe.db.sql("SELECT name,supplier from `tabSupplier Quotation` WHERE supplier='"+str(sqi)+"' and name='"+str(k)+"' ",as_dict=1):
            aa+=i.name
    # frappe.msgprint(aa)

    return aa
