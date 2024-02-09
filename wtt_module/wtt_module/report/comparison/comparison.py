# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import numpy as np
import json
from frappe.model.mapper import get_mapped_doc
from datetime import date,datetime,timedelta

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
            "width": 160
        },  
        {
            "label": _("Technical Description"),
            "fieldtype": "Data",
            "fieldname": "technical_description",
            "width": 100
        }
    ]
    val=frappe.db.sql("SELECT supplier FROM `tabSupplier Quotation` WHERE request_for_quotation=%(request_for_quotation)s and revision='Final Revision'",filters,as_dict=1)
    for i in val:
        columns.append({
            "fieldname": i.supplier+"qty",
            "label": "Qty"+" - "+i.supplier,
            "fieldtype": "HTML",
            "width": 120
        })
    for i in val:
        columns.append({
            "fieldname": i.supplier+"rate",
            "label": "Price"+" - "+i.supplier,
            "fieldtype": "HTML",
            "width": 120
        })
    for i in val:
        columns.append({
            "fieldname": i.supplier+"amount",
            "label": "Amount"+" - "+i.supplier,
            "fieldtype": "HTML",
            "width": 120
        })
    columns.append({
        "label": _("Difference"),
        "fieldtype": "Data",
        "fieldname": "diff",
        "width": 60
    })
    for i in val:
        columns.append({
            "fieldname": i.supplier+"description",
            "label": "Supplier Description"+" - "+i.supplier,
            "fieldtype": "Small Text",
            "width": 100
        })
    columns.append({
        "label": _("Item Code"),
        "fieldtype": "Data",
        "fieldname": "item_code",
        "width": 10
    })   
    return columns

def get_data(data, filters):
    data=[]
    to_be_compared_items = frappe.db.sql("SELECT soi.parent,sq.supplier_name,soi.item_code,soi.approval,soi.item_name,soi.description,sq.currency,soi.technical_description,sum(soi.qty)as qty,sum(soi.mr_qty)as mr_qty,soi.item_tax_template,soi.rate,sum(soi.amount)as amount,soi.name,soi.supplier_description,soi.base_rate,sum(soi.base_amount)as base_amount FROM `tabSupplier Quotation Item` as soi,`tabSupplier Quotation` as sq WHERE sq.name = soi.parent and sq.request_for_quotation = %(request_for_quotation)s AND sq.workflow_state!='Cancelled' AND sq.workflow_state!='Rejected' AND sq.revision='Final Revision' AND sq.transaction_date between %(from_date)s and %(to_date)s GROUP BY sq.name,soi.item_code",filters,as_dict = 1)
    query=frappe.db.sql("SELECT name,workflow_state,conversion_rate,total_taxes_and_charges,currency,base_grand_total,base_total,supplier_name,others,make,freight_amount,freight_terms,p_and_f,gst,grand_total,total,price_basis,delivary_time,payment_terms,warranty,import_duty_percentage,import_duty_amount,custom_duty_percentage,custom_duty_amount FROM `tabSupplier Quotation` WHERE request_for_quotation=%(request_for_quotation)s AND revision='Final Revision'",filters,as_dict=1)
    items_dict = {}
    temp_list = []
    dummy_rate=[]
    low_amt=[]
    for item in to_be_compared_items:
        temp_list.append(item.item_code)
    unique_item = set(temp_list)

    column1={}
    for item in query:
        column1['description'] = "Make"
        column1[item.supplier_name + 'amount'] = item.supplier_name
    data.append(column1)
    
    column10={}
    for item in query:
        column10['description'] = "SQ No"
        # column10[item.supplier_name + 'amount'] = item.name
        if(item.workflow_state=='Approved'):
            column10[item.supplier_name + 'amount'] = "<p style='background-color:lightgreen;color:black;'><b>"+str(item.name)+"</b></p>"
        if(item.workflow_state=='Rejected'):
            column10[item.supplier_name + 'amount'] = "<p style='background-color:#FF6666;color:black;'><b>"+str(item.name)+"</b></p>"
        if(item.workflow_state=='Created' ):
            column10[item.supplier_name + 'amount'] = "<b>"+str(item.name)+"</b>"
        if(item.workflow_state=='Verified' or item.workflow_state=='Approved by HOD'):
            column10[item.supplier_name + 'amount'] = "<p style='background-color:cyan;color:black;'><b>"+str(item.name)+"</b></p>"
    data.append(column10)

    for item in unique_item:
        column = {}
        amt_for_color=[]
        for datum in to_be_compared_items:
            if (item == datum.item_code):
                if(datum.currency=="INR" and datum.amount>0):
                    amt_for_color.append(round(datum.amount,2))
                else:
                    amt_for_color.append(round(datum.base_amount,2))
        amt_for_color.sort()
        for datum in to_be_compared_items:
            if item == datum.item_code:
                column['item_code'] = datum.item_code
                column['description'] = datum.description
                column['technical_description']=datum.technical_description
                if(datum.approval=='Approved'):
                    column[datum.supplier_name + 'qty'] = "<p style='background-color:lightgreen;color:black;'><b>"+str(datum.qty)+"</b></p>"
                elif(datum.approval=='Rejected'):
                    column[datum.supplier_name + 'qty'] = "<p style='background-color:#FF6666;color:black;'><b>"+str(datum.qty)+"</b></p>"
                elif(datum.approval=='Verified'):
                    column[datum.supplier_name + 'qty'] = "<p style='background-color:orange;color:black;'><b>"+str(datum.qty)+"</b></p>"
                elif(datum.approval=='Approved by HOD'):
                    column[datum.supplier_name + 'qty'] = "<p style='background-color:cyan;color:black;'><b>"+str(datum.qty)+"</b></p>"
                else:
                    column[datum.supplier_name + 'qty'] = datum.qty
                column[datum.supplier_name + 'gst'] = datum.item_tax_template         
                column[datum.supplier_name + 'description'] = datum.supplier_description
                if(datum.currency=="INR"):
                    column[datum.supplier_name + 'rate'] = str(datum.rate)
                else:
                    column[datum.supplier_name + 'rate'] = str(round(datum.base_rate,2))
                percentage=0
                if(max(amt_for_color)>0):
                    percentage=((max(amt_for_color)-min(amt_for_color))/max(amt_for_color))*100
                if(datum.currency=="INR"):
                    amount_="<p>"+str(round(datum.amount,2))+"</p>"
                    if(round(datum.amount,2)==max(amt_for_color)):
                        amount_="<p style='background-color:tomato;'>"+str(round(datum.amount,2))+"</p>"
                        if(amt_for_color[len(amt_for_color)-2]==0):
                            amount_="<p style='background-color:lightgreen;'>"+str(round(datum.amount,2))+"</p>"
                    elif(round(datum.amount,2)==0):
                        amount_="<p style='background-color:lightblue;'>"+str(max(amt_for_color))+"</p>"
                        percentage=0
                        dummy_rate.append({"supplier":datum.supplier_name,"amt":max(amt_for_color)})
                    elif(round(datum.amount,2)==min(amt_for_color)):
                        amount_="<p style='background-color:lightgreen;'>"+str(round(datum.amount,2))+"</p>"
                        low_amt.append({"supplier":datum.supplier_name,"amt":datum.amount})
                    elif(round(datum.amount,2)>0 and min(amt_for_color)==0):
                        if(round(datum.amount,2)==amt_for_color[1] and round(datum.amount,2)<max(amt_for_color)):
                            amount_="<p style='background-color:lightgreen;'>"+str(round(datum.amount,2))+"</p>"
                            low_amt.append({"supplier":datum.supplier_name,"amt":datum.amount})

                    column[datum.supplier_name + 'amount'] = amount_


                else:
                    amount_="<p>"+str(round(datum.base_amount,2))+"</p>"
                    if(round(datum.base_amount,2)==max(amt_for_color)):
                        amount_="<p style='background-color:tomato;'>"+str(round(datum.base_amount,2))+"</p>"
                        if(amt_for_color[len(amt_for_color)-2]==0):
                            amount_="<p style='background-color:lightgreen;'>"+str(round(datum.base_amount,2))+"</p>"
                    elif(datum.base_amount==0):
                        amount_="<p style='background-color:lightblue;'>"+str(max(amt_for_color))+"</p>"
                        percentage=0
                        dummy_rate.append({"supplier":datum.supplier_name,"amt":max(amt_for_color)})
                    elif(round(datum.base_amount,2)==min(amt_for_color)):
                        amount_="<p style='background-color:lightgreen;'>"+str(round(datum.base_amount,2))+"</p>"
                        low_amt.append({"supplier":datum.supplier_name,"amt":datum.base_amount})
                    elif(round(datum.base_amount,2)>0 and min(amt_for_color)==0):
                        if(round(datum.base_amount,2)==amt_for_color[1] and round(datum.base_amount,2)<max(amt_for_color)):
                            amount_="<p style='background-color:lightgreen;'>"+str(round(datum.base_amount,2))+"</p>"
                            low_amt.append({"supplier":datum.supplier_name,"amt":datum.base_amount})
                    column[datum.supplier_name + 'amount'] = amount_


                column["diff"]=str(round(percentage))+ "%"
        data.append(column)
    

    column2={}
    for item in query:
        column2['description'] = "Basic total"
        column2[item.supplier_name + 'amount'] = item.base_total
    
    column3={}
    for item in query:
        column3['description'] = "Freight Amount"
        column3[item.supplier_name + 'amount'] = item.freight_amount
    column14={}
    for item in query:
        column14['description'] = "Freight Terms"
        column14[item.supplier_name + 'amount'] = item.freight_terms
    column4={}
    for item in query:
        column4['description'] = "P & F"
        column4[item.supplier_name + 'amount'] = item.p_and_f
    column5={}
    for item in query:
        column5['description'] = "<p><b>Grand Total</b></p>"
        if(item.conversion_rate==None):
            column5[item.supplier_name + 'amount'] = item.grand_total
        else:
            column5[item.supplier_name + 'amount'] = item.base_grand_total

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
        if(item.freight_amount is not None and item.total_taxes_and_charges>0):
            column13[item.supplier_name + 'amount'] = float(item.total_taxes_and_charges)-float(item.freight_amount)
        elif(item.total_taxes_and_charges>0):
            column13[item.supplier_name + 'amount'] = float(item.freight_amount)
    column15={}
    for item in query:
        column15['description'] = "Import Duty"
        column15[item.supplier_name + 'amount'] = str(round(item.import_duty_amount,2))+" ("+str(item.import_duty_percentage)+"%)"
    column16={}
    for item in query:
        column16['description'] = "Custom Duty"
        column16[item.supplier_name + 'amount'] = str(round(item.custom_duty_amount,2))+" ("+str(item.custom_duty_percentage)+"%)"
    column17={}
    gv=[]
    for item in query:
        tot=item.total
        if(item.currency!="INR"):
            tot=item.base_total
        gv.append(tot+item.import_duty_amount+item.custom_duty_amount)
    maximum = max(gv)
    minimum = min(gv)
    for item in query:
        tot=item.total
        if(item.currency!="INR"):
            tot=item.base_total
        column17['description'] = "Overall Basic"
        if(tot+item.import_duty_amount+item.custom_duty_amount==maximum):
            column17[item.supplier_name + 'amount'] = "<p style='background-color:#FF6666;color:black'><b>"+str(round(tot+item.import_duty_amount+item.custom_duty_amount,2))+"</b></p>"
        if(tot+item.import_duty_amount+item.custom_duty_amount==minimum):
            column17[item.supplier_name + 'amount'] = "<p style='background-color:lightgreen;color:black'><b>"+str(round(tot+item.import_duty_amount+item.custom_duty_amount,2))+"</b></p>"
        if(tot+item.import_duty_amount+item.custom_duty_amount!=minimum and tot+item.import_duty_amount+item.custom_duty_amount!=maximum):
            column17[item.supplier_name + 'amount'] = "<p style='background-color:orange;color:black'><b>"+str(round(tot+item.import_duty_amount+item.custom_duty_amount,2))+"</b></p>"

    column18={}
    ss=[]
    for item in query:
        ass_amt=[]
        tot=item.base_total
        if(item.currency=='INR'):
            tot=item.total
        if(len(dummy_rate)>0):
            for i in dummy_rate:
                if(item.supplier_name==i["supplier"]):
                    ass_amt.append(i['amt'])
            ss.append(round(sum(ass_amt)+tot,2))
            aamm=round(sum(ass_amt)+tot,2)
            ht="<p><b>"+str(aamm)+"</b></p>"
            ht="<p style='background-color:lightblue;'><b>"+str(aamm)+"</b></p>"
            column18["description"]="Assumed Rate"
            column18[item.supplier_name+'amount']=ht
    # frappe.msgprint(str(ss))
    column19={}
    for item in query:
        l_amt=0
        for i in low_amt:
            if(item.supplier_name==i["supplier"]):
                l_amt+=i["amt"]
        column19["description"]="Low Rate"
        column19[item.supplier_name+'amount']="<p style='background-color:orange'>"+str(round(l_amt,2))+'</p>'

    if(len(dummy_rate)>0):
        data.append(column18)
        # data.append(column19)
    data.append(column2)
    data.append(column15)
    data.append(column16)
    data.append(column17)
    data.append(column3)
    data.append(column14)
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
    qq = frappe.db.sql("SELECT name FROM `tabSupplier Quotation` where request_for_quotation = '"+str(rfq1)+"' AND revision='Final Revision'",as_dict = 1)
    for i in qq:
        ar.append(i.name)
    return ar

@frappe.whitelist()
def fun_make2(sq,itc):
    arq=[]
    qq = frappe.db.sql("SELECT soi.qty, soi.rate, soi.amount,soi.name,soi.item_code,sq.currency,sq.conversion_rate FROM `tabSupplier Quotation Item` as soi inner join `tabSupplier Quotation` as sq on sq.name = soi.parent where sq.name = '"+str(sq)+"' AND soi.item_code='"+str(itc)+"' AND revision='Final Revision'",as_dict = 1)
    qqq = frappe.db.sql("SELECT sq.supplier,soi.qty, soi.rate, soi.amount,soi.name,soi.item_code,sq.currency,sq.conversion_rate,sq.price_basis,sq.delivary_time,sq.warranty,sq.payment_terms FROM `tabSupplier Quotation Item` as soi inner join `tabSupplier Quotation` as sq on sq.name = soi.parent where sq.name = '"+str(sq)+"' AND soi.item_code='"+str(itc)+"' AND revision='Final Revision'",as_dict = 1)
    for j in qqq:
        for i in qq:
            if(i.item_code==j.item_code):
                arq.append({
                "supplier":j.supplier,
                "material_request":j.material_request,
                "qty":j.qty,
                "rate":j.rate,
                "amount":j.amount,
                "mr_name":j.name,
                "sup_qty":i.qty,
                "sup_rate":i.rate,
                "sup_amount":i.amount,
                "sup_mr_name":i.name,
                "currency":i.currency,
                "cr":i.conversion_rate,
                "price_basis":j.price_basis,
                "warranty":j.warranty,
                "payment_terms":j.payment_terms,
                "delivery_time":j.delivary_time
                })
    return arq

@frappe.whitelist()
def fun_make(sq,itc):
    arq=[]
    
    qqq = frappe.db.sql("SELECT sq.supplier,soi.qty, soi.rate, soi.amount,soi.name,sq.price_basis,sq.delivary_time,sq.warranty,sq.payment_terms FROM `tabSupplier Quotation Item` as soi inner join `tabSupplier Quotation` as sq on sq.name = soi.parent where sq.name = '"+str(sq)+"' AND soi.item_code='"+str(itc)+"' AND revision='Final Revision'",as_dict = 1)
    for j in qqq:
        arq.append({
        "supplier":j.supplier,
        "material_request":j.material_request,
        "qty":j.qty,
        "rate":j.rate,
        "amount":j.amount,
        "mr_name":j.name,
        "price_basis":j.price_basis,
        "warranty":j.warranty,
        "payment_terms":j.payment_terms,
        "delivery_time":j.delivary_time
        })
    return arq


@frappe.whitelist()
def update_supplier_quotation(item_code,sq,mr,supplier,qty,rate,amt,mr_name,base_rate,base_amount,price_basis,payment_terms,warranty,delivery_time):
    ar=[]
    br=[]
    mmar=[]
    # v=frappe.db.sql("UPDATE `tabSupplier Quotation Item` SET approval='Approved',qty='"+str(qty)+"',amount='"+str(amt)+"',rate='"+str(rate)+"' WHERE parent='"+str(sq)+"' and item_code='"+str(item_code)+"' and material_request='"+str(mr)+"' and material_request_item='"+str(mr_name)+"' ",as_dict=1)
    v=frappe.db.sql("UPDATE `tabSupplier Quotation Item` SET qty='"+str(qty)+"',rate='"+str(rate)+"',amount='"+str(amt)+"',base_rate='"+str(base_rate)+"',base_amount='"+str(base_amount)+"',approval='Approved' WHERE parent='"+str(sq)+"' and name='"+str(mr_name)+"' ",as_dict=1)
    
    doc=frappe.get_doc("Supplier Quotation",sq)
    doc.price_basis=price_basis
    doc.delivary_time=delivery_time
    doc.warranty=warranty
    doc.payment_terms=payment_terms
    for i in doc.get("items"):
        ar.append(i.approval)
        if(i.item_code==item_code):
            i.quoted_qty=str(qty)
            i.rate=str(rate)
            if(frappe.session.user=='venkat@wttindia.com' or frappe.session.user=='Administrator'):
                i.approval='Approved'
            elif(frappe.session.user=='malayalaraj@wtt.com' or frappe.session.user=='vishnu@wtt.com'):
                i.approval='Approved by HOD'
            elif(frappe.session.user=='purchase@wttindia.com' or frappe.session.user=='erp@wttindia.com'):
                i.approval='Verified'
    doc.save()
    return v

@frappe.whitelist()
def approvesq(sq,supplier,user,item):
    ar=[]
    array = json.loads(item)
    for i in array:
    # for j in frappe.db.sql("SELECT sqi.qty,sqi.item_code FROM `tabSupplier Quotation`as sq,`tabSupplier Quotation Item`as sqi WHERE sq.name=sqi.parent and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqi.approval!='Rejected' ",as_dict=1):
        frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSupplier Quotation Item`as sqt SET sqt.approval='Approved',sqt.quoted_qty=sqt.qty WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)
    doc=frappe.get_doc("Supplier Quotation",sq)

    if(user=='venkat@wttindia.com' or user=='Administrator' or user=='sarnita@wttindia.com'):
        doc.docstatus=1
        doc.workflow_state='Approved'
    elif(user=='malayalaraj@wtt.com' or user=='vishnu@wtt.com'):
        doc.docstatus=0
        doc.workflow_state='Approved by HOD'
    elif(user=='purchase@wttindia.com' or user=='erp@wttindia.com'):
        doc.docstatus=0
        doc.workflow_state='Approved by HOD' 
    doc.save()
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
def approveitc(sq,item_code,item,supplier,user):
    array = json.loads(item)
    for i in array:
        if(user=='venkat@wttindia.com' or user=='Administrator' or user=='sarnita@wttindia.com'):
            frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSupplier Quotation Item`as sqt SET sqt.approval='Approved' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)
            frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSQ Combined Table`as sqt SET sqt.approval='Approved' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)
            
        elif(user=='malayalaraj@wtt.com' or user=='vishnu@wtt.com'):
            frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSupplier Quotation Item`as sqt SET sqt.approval='Approved by HOD' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)
            frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSQ Combined Table`as sqt SET sqt.approval='Approved by HOD' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)

        elif(user=='purchase@wttindia.com' or user=='erp@wttindia.com'):
            frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSupplier Quotation Item`as sqt SET sqt.approval='Verified' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)
            frappe.db.sql("UPDATE `tabSupplier Quotation`as sq,`tabSQ Combined Table`as sqt SET sqt.approval='Verified' WHERE sqt.parent=sq.name and sq.name='"+str(sq)+"' and sq.supplier='"+str(supplier)+"' and sqt.item_code='"+str(i["it"])+"' ",as_dict=1)
            

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

    doclist = get_mapped_doc("Supplier Quotation", source_name,  {
        "Supplier Quotation": {
            "doctype": "Purchase Order",
            "validation": {
                "docstatus": ["=", 1],
            },
            "field_map":[
                [date.today(),"schedule_date"],
                ["taxes_and_charges","taxes_and_charges"]
            ]
        },
        "Supplier Quotation Item": {
            "doctype": "Purchase Order Item",
            "field_map": [
                ["name", "supplier_quotation_item"],
                ["parent", "supplier_quotation"],
                ["material_request", "material_request"],
                ["material_request_item", "material_request_item"],
                ["sales_order", "sales_order"],
                ["qty","qty"],
                [date.today(),"schedule_date"]
            ],
            "postprocess": update_item,
            "condition": lambda doc: doc.approval=="Approved" and doc.qty>0
        }
    }, target_doc, set_missing_values)

    doclist.save()
    return doclist