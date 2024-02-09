# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import functools
class ProjectInfo(Document):
	pass

@frappe.whitelist()
def get_system_table(project):
	ar=[]
	detail_datasheet=frappe.db.sql("SELECT ch.system_name FROM `tabDetail datasheet`as pp,`tabSystem Table`as ch WHERE pp.name=ch.parent and pp.project='"+str(project)+"' ",as_dict=1)
	if(detail_datasheet):
		for i in detail_datasheet:
			ar.append(i.system_name)

	return ar


@frappe.whitelist()
def get_tracking(project):
	cre=0
	ahod=0
	app=0
	epp=0
	ar=[]
	sq=frappe.db.sql("SELECT workflow_state,count(name) as ct FROM `tabMaterial Request` WHERE workflow_state!='Rejected' and workflow_state!='Cancelled' and project='"+str(project)+"' GROUP BY workflow_state",as_dict=1)
	for i in sq:
		if(i.workflow_state=="Created"):
			cre=i.ct
		elif(i.workflow_state=="Approved"):
			app=i.ct
		elif(i.workflow_state=="Emergency Approval"):
			epp=i.ct
		elif(i.workflow_state=="Approved by HOD"):
			ahod=i.ct

	tt=int(cre)+int(ahod)+int(app)+int(epp)
	ar.append({
		"document_name":"MR",
		"created":cre,
		"approved_by_hod":ahod,
		"emergency_app":epp,
		"approved":app,
		"total":tt
		})
	
	po_c = 0
	po_hod = 0
	po_a = 0
	po_ea = 0
	po = frappe.db.sql("SELECT workflow_state,count(name) as cnt FROM `tabPurchase Order` WHERE project LIKE '"+str(project)+"' GROUP BY workflow_state",as_dict=1)
	for i in po:
		if(i.workflow_state=="Created"):
			po_c = i.cnt
		if(i.workflow_state=="Approved by HOD"):
			po_hod = i.cnt
		if(i.workflow_state=="Approved"):
			po_a = i.cnt
		if(i.workflow_state=="Emergency Approval"):
			po_ea = i.cnt
	ar.append({
		"document_name":"PO",
		"created":po_c,
		"approved_by_hod":po_hod,
		"emergency_app":po_ea,
		"approved":po_a,
		"total":int(po_c)+int(po_hod)+int(po_a)+int(po_ea)
		})
	return ar

@frappe.whitelist()
def pr_details(project):
	ag=[]
	pr_d = 0
	pr_b = 0
	pr_c = 0
	pi_d = 0
	pi_over = 0
	pi_paid = 0
	pr = frappe.db.sql("SELECT status,count(name) as prcnt FROM `tabPurchase Receipt` WHERE project LIKE '"+str(project)+"' GROUP BY status",as_dict=1)
	for i in pr:
		if(i.status=="Draft"):
			pr_d = i.prcnt
		if(i.status=="To Bill"):
			pr_b = i.prcnt
		if(i.status=="Completed"):
			pr_c = i.prcnt
	
	pi = frappe.db.sql("SELECT status,count(name) as picnt FROM `tabPurchase Invoice` WHERE project LIKE '"+str(project)+"' GROUP BY status",as_dict=1)
	for i in pi:
		if(i.status=="Draft"):
			pi_d = i.picnt
		if(i.status=="Overdue"):
			pi_over = i.picnt
		if(i.status=="Paid"):
			pi_paid = i.picnt

	ag.append({
		"prdraft":pr_d,
		"prbill":pr_b,
		"prcom":pr_c,
		"prtotal":int(pr_d)+int(pr_b)+int(pr_c),
		"pidraft":pi_d,
		"piover":pi_over,
		"pipaid":pi_paid,
		"pitotal":int(pi_d)+int(pi_over)+int(pi_paid)
		})
	return ag