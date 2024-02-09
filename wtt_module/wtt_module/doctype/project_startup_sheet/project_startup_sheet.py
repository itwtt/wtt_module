# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class ProjectStartupSheet(Document):
	pass

@frappe.whitelist()
def get_all_value(enq):
	ar=[]
	cod=0;
	bod=0;
	tss=0;
	tkn=0;
	for i in frappe.db.sql("SELECT * FROM `tabSystem Parameter Details` WHERE parent='"+str(enq)+"'",as_dict=1):
		if(i.parameter=="COD(mg/l)"):	
			ar.append({
				"cod":i.value
			})
		if(i.parameter=="BOD(mg/l)"):
			ar.append({
				"bod":i.value
			})
		if(i.parameter=="TSS(mg/l)"):
			ar.append({
				"tss":i.value
				})
	return ar


@frappe.whitelist()
def get_system(enq,st):
	arr=[]
	for j in frappe.db.sql("SELECT selected_system_name FROM `tabSelected Process System` WHERE parent='"+str(enq)+"'",as_dict=1):
		arr.append({
			"select_system":j.selected_system_name
		})
	return arr

# @frappe.whitelist()
# def get_matching_bom(process_system,params):
# 	ps=json.loads(params)
# 	aa=[]
# 	data=[]
# 	for param in ps:
# 		v = frappe.db.sql("SELECT * FROM `tabMapping BOM` WHERE process_system='"+str(param["system_name"])+"'")
# 		if(v):
# 			bom_doc = frappe.get_doc("Mapping BOM",{"process_system":param["system_name"]})
# 			for condition in bom_doc.conditions:
# 				if(str(param["parameter_name"])==condition.parameter_name and str(param["value"])==condition.value):
# 					if(bom_doc.name not in aa):
# 						aa.append(bom_doc.name)
# 	if(len(aa)==0):
# 		frappe.msgprint("There is no BOM found for these parameter")
# 	for bom_list in aa:
# 		doc = frappe.get_doc("BOM", bom_list)
# 		data.append({
# 			"bom":doc.name,
# 			"cost":str(doc.total_cost),
# 			"items":doc.get("exploded_items")
# 		})
# 	return data



@frappe.whitelist()
def get_stand(st):
	arr=[]
	for j in frappe.db.sql("SELECT mf_cost FROM `tabMF Standard Items` WHERE project_startup_sheet='"+str(st)+"'",as_dict=1):
		arr.append({
			"cost":j.mf_cost
		})
	for j in frappe.db.sql("SELECT mbr_overall_cost FROM `tabMBR Standard Items` WHERE project_startup_sheet='"+str(st)+"'",as_dict=1):
		arr.append({
			"cost":j.mbr_overall_cost
		})
	for j in frappe.db.sql("SELECT total_cost FROM `tabMBR ovivo Standard Items` WHERE project_startup_sheet='"+str(st)+"'",as_dict=1):
		arr.append({
			"cost":j.total_cost
		})
	return arr
