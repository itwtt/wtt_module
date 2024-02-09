# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class MRColorCorrection(Document):
	# pass
	def validate(self):
		for i in frappe.db.sql("SELECT name,qty,mi_qty from `tabMaterial Request Item` ",as_dict=1):
			frappe.db.sql("UPDATE `tabMaterial Request Item` set bal_qty='"+str(i.qty-i.mi_qty)+"' WHERE name='"+str(i.name)+"' ")
		frappe.msgprint("done")


@frappe.whitelist()
def mr_color(mr):
	ar=[]
	# pass

	################################################CHECKING RECEIVED QUANITY IN PURCHASE ORDER
	# query = frappe.db.sql("SELECT c.parent,c.name,c.item_code,c.qty,c.received_qty,c.idx FROM `tabPurchase Order`as p,`tabPurchase Order Item`as c WHERE p.name=c.parent and p.docstatus!=2 and p.workflow_state!='Cancelled' ",as_dict=1)
	# for i in query:
	# 	qt=0
	# 	qr=frappe.db.sql("SELECT sum(c.received_qty)as qty FROM `tabPurchase Receipt`as p,`tabPurchase Receipt Item`as c WHERE c.parent=p.name and p.docstatus=1 and c.purchase_order_item='"+str(i.name)+"' and p.status!='Return'  GROUP BY c.purchase_order_item ",as_dict=1)
	# 	if qr:
	# 		for j in qr:
	# 			qt+=j.qty
	# 		if(qt!=i.received_qty):
	# 			ar.append({
	# 				"po":i.parent,
	# 				"item_code":i.item_code,
	# 				"mr_qty":i.qty,
	# 				"po_qty":qt,
	# 				"completed_qty":i.received_qty,
	# 				"po_name":i.name,
	# 				"description":i.idx
	# 				})





	################################################
	#            UPDATE COMPLETED QUANTITY IN MATERIAL REQUEST
	
	query=frappe.db.sql("SELECT c.parent,c.name,c.item_code,c.qty,c.ordered_qty,c.idx FROM `tabMaterial Request`as p,`tabMaterial Request Item`as c WHERE p.name=c.parent and p.docstatus!=2 and p.workflow_state!='Rejected' ",as_dict=1)
	for i in query:
		qt=0
		qr=frappe.db.sql("SELECT sum(c.qty)as qty FROM `tabPurchase Order`as p,`tabPurchase Order Item`as c WHERE c.parent=p.name and p.docstatus=1 and p.workflow_state!='Rejected' and c.material_request_item='"+str(i.name)+"'  GROUP BY c.material_request_item ",as_dict=1)
		if qr:
			for j in qr:
				qt+=j.qty
			if(qt!=i.ordered_qty):
				ar.append({
					"mr":i.parent,
					"item_code":i.item_code,
					"mr_qty":i.qty,
					"po_qty":qt,
					"completed_qty":i.ordered_qty,
					"mr_name":i.name,
					"description":i.idx
					})
					


	return ar


@frappe.whitelist()
def update_completed_qty_mr(ar):

	"""   ##########  ##   UPDATE TAC TEMPLATE PURCHASE ORDER   ##   ###################     """
	# ar=[]
	# arg=[]
	# percentage=[]
	# for i in frappe.db.sql("SELECT item_tax_template,base_amount as amount,name,parent from `tabPurchase Order Item` ",as_dict=1):
	# 	if(i.item_tax_template!=None and i.item_tax_template!=''):
	# 		arg.append({
	# 			"name":i.name,
	# 			"item_tax_template":i.item_tax_template,
	# 			"amount":i.amount,
	# 			"parent":str(i.parent)
	# 			})
	# 	elif(frappe.db.get_value("Purchase Order",str(i.parent),"taxes_and_charges")!=None and frappe.db.get_value("Purchase Order",str(i.parent),"taxes_and_charges")!=''):
	# 		percentage.append({
	# 			"name":i.name,
	# 			"item_tax_template":frappe.db.get_value("Purchase Order",str(i.parent),"taxes_and_charges"),
	# 			"amount":i.amount,
	# 			"parent":str(i.parent)
	# 			})

	# # frappe.msgprint(str(arg))
	# for j in percentage:
	# 	if(j["item_tax_template"] not in ["GST - 0 - WTT","GST - 0% - WTT"]):
	# 		if(frappe.db.exists("Purchase Taxes and Charges Template",str(j["item_tax_template"]))):
	# 			for k in frappe.db.sql("SELECT sum(rate)as rate FROM `tabPurchase Taxes and Charges` WHERE parent='"+str(j["item_tax_template"])+"' ",as_dict=1):
	# 				ar.append({
	# 					"parent":str(j["parent"]),
	# 					"name":j["name"],
	# 					"tax":(float(j["amount"])*(float(k.rate)/100))
	# 					})
	# 				# frappe.db.sql("UPDATE `tabPurchase Order Item` SET tax='"+str(float(j["amount"])/(float(k.rate)/100))+"' WHERE name='"+str(j["name"])+"' ")
	# 				frappe.db.sql("UPDATE `tabPurchase Order Item` SET tax='"+str(float(j["amount"])*(float(k.rate)/100))+"' WHERE name='"+str(j["name"])+"' ")
	# frappe.msgprint("done")












			# for j in frappe.db.sql("SELECT sum(rate)as rate FROM `tabPurchase Taxes and Charges` WHERE parent='"+str(i.item_tax_template)+"' ",as_dict=1):
			# 	percentage.append(j.rate)
		
	# frappe.msgprint(str(percentage))
			# ar.append({
			# 	"name":i.name,
			# 	"tax":(float(i.amount)/(float(sum(percentage))/100))
			# 	})
		# frappe.db.sql("UPDATE `tabPurchase Order Item` SET tax='"+str(float(i.amount)/(float(sum(percentage)/100)))+"' WHERE name='"+str(i.name)+"' ")

	# frappe.msgprint(str(ar))


	# frappe.msgprint("done")
	to_python = json.loads(ar)
################################################
	#            UPDATE COMPLETED QUANTITY IN MATERIAL REQUEST

	for i in to_python:
		frappe.db.sql("UPDATE `tabMaterial Request Item` SET ordered_qty='"+str(i["po_qty"])+"' WHERE name='"+str(i["mr_name"])+"' ")
	frappe.msgprint("Done")


################################################CHECKING RECEIVED QUANITY IN PURCHASE ORDER

	# for i in to_python:
	# 	if(i["completed_qty"]<i["po_qty"]):
	# 		frappe.db.sql("UPDATE `tabPurchase Order Item` SET received_qty='"+str(i["po_qty"])+"' WHERE name='"+str(i["po_name"])+"' ")
	# frappe.msgprint("Done")














	##############code for get avg for default task hours calculation
	'''avg_raghul=[]
	query=frappe.db.sql("SELECT child.completed_hours from `tabTask Allocation` as parent,`tabWork Update` as child WHERE parent.name=child.parent and parent.employee='WTT1278' and child.status='Completed' and child.type_of_work='5 Cutomer Followup' ",as_dict=1)
	for i in query:
		avg_raghul.append(i.completed_hours)
	frappe.msgprint("Raghul Raj "+str(sum(avg_raghul)/len(avg_raghul)))

	

	avg_prabhu=[]
	query=frappe.db.sql("SELECT child.completed_hours from `tabTask Allocation` as parent,`tabWork Update` as child WHERE parent.name=child.parent and parent.employee='WTT1090' and child.status='Completed' and child.type_of_work='2 Trade Enquiry' ",as_dict=1)
	for i in query:
		avg_prabhu.append(i.completed_hours)
	frappe.msgprint("Prabhu - "+str(sum(avg_prabhu)/len(avg_prabhu)))


	avg_sivakumar=[]
	query=frappe.db.sql("SELECT child.completed_hours from `tabTask Allocation` as parent,`tabWork Update` as child WHERE parent.name=child.parent and parent.employee='WTT1211' and child.status='Completed' and child.type_of_work='Department Meeting Update' ",as_dict=1)
	for i in query:
		avg_sivakumar.append(i.completed_hours)
	frappe.msgprint("Sivakumar - "+str(sum(avg_sivakumar)/len(avg_sivakumar)))
	'''


	








	#item inspection project update
	# for i in frappe.db.sql("SELECT pri.project,pri.name,pri.parent FROm `tabPurchase Receipt` as pr,`tabPurchase Receipt Item`as pri WHERE pr.name=pri.parent ",as_dict=1):
	# 	frappe.db.sql("UPDATE `tabItem Inspection item` SET project='"+str(i.project)+"' WHERE purchase_receipt='"+str(i.parent)+"' and pr_item='"+str(i.name)+"' ",as_dict=1)
	# frappe.msgprint("done")
	

# 	update ordered qty in material request after po is submitted but the ordered qty is notr updated


	# array=[]
	# po=[]
	# mr=[]
	# mr_list=[]
	# query=frappe.db.sql("SELECT poi.material_request,poi.material_request_item,poi.qty FROM `tabPurchase Order Item`as poi,`tabPurchase Order`as po WHERE poi.parent=po.name and po.workflow_state!='Rejected' and po.workflow_state!='Cancelled' and po.naming_series!='JOB-.YY.-' ",as_dict=1)
	# for i in query:
	# 	for j in frappe.db.sql("SELECT mri.name,mri.parent,mri.idx FROM `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mri.parent=mr.name and mri.name='"+str(i.material_request_item)+"' and mri.parent='"+str(i.material_request)+"' and mri.ordered_qty=0 ",as_dict=1):
	# 		frappe.db.sql("UPDATE `tabMaterial Request Item` SET ordered_qty='"+str(i.qty)+"' WHERE name='"+str(j.name)+"' ",as_dict=1)
	# 		mr.append({
	# 			"idx":j.idx,
	# 			"mr":j.parent,
	# 			"child":j.name
	# 			})
	# frappe.msgprint(str(mr))

	# #material issue qty update in material request mi_qty and bal_qty
	# array=[]
	# po=['PO-22-00472']
	# mr=[]
	# mr_list=[]
	# for p in po:
	# 	for i in frappe.db.sql("SELECT poi.item_code,poi.material_request_item,poi.item_name,poi.description,poi.qty,poi.technical_description,poi.uom,poi.material_request,poi.name FROM `tabPurchase Order`as po,`tabPurchase Order Item`as poi WHERE poi.parent=po.name AND po.name='"+str(p)+"' ",as_dict=1):
	# 		if(i.material_request_item==None):
	# 			mr.append({
	# 					"item_code":i.item_code,
	# 					"description":i.description,
	# 					"qty":i.qty
	# 					})
	# for i in mr:
	# 	for j in frappe.db.sql("SELECT name FROM `tabMaterial Request Item` WHERE item_code='"+str(i.item_code)+"' and qty='"+str(i.qty)+"' ",as_dict=1):
	# 		array.append({
	# 			"item_code":i.item_code,
	# 			"description":i.description,
	# 			"qty":i.qty,
	# 			"name":j.name
	# 			})
	# 				# frappe.db.sql("UPDATE `tabPurchase Order Item` SET material_request_item='"+str(j.name)+"' WHERE name='"+str(i.name)+"' and parent='"+str(p)+"' ",as_dict=1)
	# frappe.msgprint(str(array))
	# frappe.msgprint("four")













	# for i in frappe.db.sql("SELECT cc.qty,cc.name,cc.mi_qty FROM `tabMaterial Request`as aa,`tabMaterial Request Item`as cc WHERE aa.name=cc.parent AND aa.docstatus!=2 AND aa.workflow_state!='Rejected' ",as_dict=1):
	# 	qt=i.qty-i.mi_qty
	# 	frappe.db.sql("UPDATE `tabMaterial Request Item` set bal_qty='"+str(qt)+"' WHERE name='"+str(i.name)+"' ",as_dict=1)
	# query=frappe.db.sql("SELECT poi.material_request,poi.material_request_item,poi.qty FROM `tabMaterial Issue Item`as poi,`tabMaterial Issue`as po WHERE poi.parent=po.name and po.status!='Cancelled' ",as_dict=1)
	# # for i in query:
	# # 	for j in frappe.db.sql("SELECT mri.name,mri.qty FROM `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mr.name=mri.parent AND mri.parent='"+str(i.material_request)+"' AND mri.name='"+str(i.material_request_item)+"' ",as_dict=1):
	# # 		qt=j.qty-i.qty
	# # 		if(qt<0):
	# # 			qtt=0
	# # 		else:
	# # 			qtt=qt
	# # 		frappe.db.sql("UPDATE `tabMaterial Request Item` set mi_qty='"+str(i.qty)+"',bal_qty='"+str(qt)+"' WHERE name='"+str(j.name)+"' ",as_dict=1)
	# frappe.msgprint("rightuh")





	
		# if(i.material_request==None):
		# 	if(i.name not in po):
		# 		po.append({
		# 			"po":i.name
		# 			})
	# 	po.append(i.material_request)
	# 	mr.append(i.material_request_item)

	# query2=frappe.db.sql("SELECT DISTINCT(po.name) FROM `tabMaterial Request Item`as poi,`tabMaterial Request`as po WHERE poi.parent=po.name and po.workflow_state='Approved' ",as_dict=1)
	# for i in query2:
	# 	if(i.name not in po):
	# 		if(i.name not in mr_list):
	# 			mr_list.append({
	# 				"po":i.name
	# 				})

	# return mr_list
