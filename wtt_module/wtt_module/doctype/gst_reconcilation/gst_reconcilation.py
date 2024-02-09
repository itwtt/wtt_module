# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import csv
import pandas as pd
from frappe.utils import getdate
class GSTreconcilation(Document):
	def validate(self):
		for i in self.gst_table:
			if("IGST" in str(i.account_name)):
				i.tax="IGST"
				if("18" in str(i.account_name)):
					i.tax_rate=18
				elif("12" in str(i.account_name)):
					i.tax_rate=12
				elif("28" in str(i.account_name)):
					i.tax_rate=28
				elif("5" in str(i.account_name)):
					i.tax_rate=5
			elif("CGST" in str(i.account_name)):
				i.tax="CGST"
				if("9" in str(i.account_name)):
					i.tax_rate=9
				elif("6" in str(i.account_name)):
					i.tax_rate=6
				elif("14" in str(i.account_name)):
					i.tax_rate=14
				elif("2.5" in str(i.account_name)):
					i.tax_rate=2.5
			elif("SGST" in str(i.account_name)):
				i.tax="SGST"
				if("9" in str(i.account_name)):
					i.tax_rate=9
				elif("6" in str(i.account_name)):
					i.tax_rate=6
				elif("14" in str(i.account_name)):
					i.tax_rate=14
				elif("2.5" in str(i.account_name)):
					i.tax_rate=2.5

	@frappe.whitelist()
	def get_journal(self):
		ar=[]
		for i in frappe.db.sql("SELECT pp.name,pp.payment_type,pp.pay_to_recd_from,pp.total_debit,pp.posting_date,pp.remark FROM `tabJournal Entry`as pp INNER JOIN `tabJournal Entry Account`as cc ON pp.name=cc.parent WHERE cc.party_type='Supplier' and pp.docstatus=1 and pp.posting_date>='"+str(self.fr_date)+"' and pp.posting_date<='"+str(self.to_date)+"' ",as_dict=1):
			ar.append(i)
		return ar
		
	@frappe.whitelist()
	def get_reconcile(self):
		ar=[]
		unique_line=[]
		query=frappe.db.sql("""SELECT 
			distinct(gt.`name`)as 'name',
			gt.`supplier_dc`,
			gt.`invoice_no`,
			gt.`invoice_date`,
			gt.`supplier`,
			gt.`tax_id`,
			gt.`account_name`,
			gt.`tax`,
			ut.`tax_name`,
			gt.`tax_id`,
			gt.`amount`as 'amount_in_erp',
			ut.`amount` as 'amount',
			gt.`taxable_value`,
			gt.`invoice_amount`
			FROM `tabGST Upload Table` as ut,`tabGST Table`as gt INNER JOIN `tabGST reconcilation` as gr ON gt.`parent`='"""+str(self.name)+"""' 
			WHERE  ut.`tax_name`=gt.`tax` and ut.`supplier_dc`=gt.`supplier_dc` and gt.`amount`!=ut.`amount`
			""",as_dict=1)

		for i in query:
			if(i.name not in unique_line):
				unique_line.append(i.name)
				ar.append(i)
			else:
				pass

		return ar


@frappe.whitelist()
def all_data(fr_date,to_date):
	ar=[]
	query = frappe.db.sql("SELECT name,supplier,posting_date,tax_id,base_rounded_total,bill_no,total FROM `tabPurchase Invoice` WHERE is_return!=1 and docstatus=1 and posting_date>='"+str(fr_date)+"' and posting_date<='"+str(to_date)+"' ",as_dict=1)
	for i in query:
		for j in frappe.db.sql("SELECT account_head,base_tax_amount FROM `tabPurchase Taxes and Charges` WHERE parent='"+str(i.name)+"'",as_dict=1):
			ar.append({
				"invoice_no":i.name,
				"supplier_dc":i.bill_no,
				"invoice_data":getdate(i.posting_date),
				"supplier":i.supplier,
				"tax_id":i.tax_id,
				"account_name":j.account_head,
				"amount":j.base_tax_amount,
				"taxable_value":i.total,
				"grand_total":i.base_rounded_total
			})
	return ar


@frappe.whitelist()
def get_excel(excel_link):
	val=[]
	df = pd.read_excel("https://erp.wttindia.com"+str(excel_link),skiprows = 5)
	df_new = pd.DataFrame(df)
	# mask=df["Integrated Tax(₹)"]!=0
	#df_new = pd.DataFrame(df[mask])
	rows = df_new.values.tolist() #convert dataframe to list
	for j in range(len(rows)):
		vals = {}
		for k in range(22):
			if(k==0 or k==1 or k==2 or k==4 or k==5 or k==8 or k==9 or k==10 or k==22 or k==11 or k==12):
				vals["col"+str(k)]=rows[j][k]
			vals["col22"]="IGST"
		val.append(vals)
	return str(val)
	# doc=frappe.get_doc("GST reconcilation",name_val)
	# for i in range(len(val)):
	# 		doc.append("upload",val[i])
	# doc.save()
	# return "Updated"
	# frappe.msgprint(str(val))
	# return str(val)
