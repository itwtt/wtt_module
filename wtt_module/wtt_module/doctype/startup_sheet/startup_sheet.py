# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from docx import Document as doc
from htmldocx import HtmlToDocx

class StartupSheet(Document):
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
def get_system(st):
	arr=[]
	for j in frappe.db.sql("SELECT selected_system_name,selected_type FROM `tabSelected Process System` WHERE parent='"+str(st)+"' ORDER BY idx ASC",as_dict=1):
		arr.append({
			"select_system":j.selected_system_name,
			"selected_type":j.selected_type
		})
	return arr

@frappe.whitelist()
def get_matching_bom(process_system,params):
	ps=json.loads(params)
	aa=[]
	data=[]
	for param in ps:
		v = frappe.db.sql("SELECT * FROM `tabMapping BOM` WHERE process_system='"+str(param["system_name"])+"'")
		if(v):
			bom_doc = frappe.get_doc("Mapping BOM",{"process_system":param["system_name"]})
			for condition in bom_doc.conditions:
				if(str(param["parameter_name"])==condition.parameter_name and str(param["value"])==condition.value):
					if(bom_doc.name not in aa):
						aa.append(bom_doc.name)
	if(len(aa)==0):
		frappe.msgprint("There is no BOM found for these parameter")
	for bom_list in aa:
		doc = frappe.get_doc("BOM", bom_list)
		data.append({
			"bom":doc.name,
			"cost":str(doc.total_cost),
			"items":doc.get("exploded_items")
		})
	return data


@frappe.whitelist()
def get_formula(f2):
	ar=[]
	for i in frappe.db.sql("SELECT pipe_size,pipe_id FROM `tabRQ pipes`",as_dict=1):
		ar.append(i)
	return ar

@frappe.whitelist()
def get_stand(st):
	arr=[]
	for j in frappe.db.sql("SELECT overall_cost FROM `tabMF Standard Items` WHERE project_startup_sheet='"+str(st)+"'",as_dict=1):
		arr.append({
			"cost":j.overall_cost
		})
	for j in frappe.db.sql("SELECT mbr_overall_cost FROM `tabMBR Standard Items` WHERE project_startup_sheet='"+str(st)+"'",as_dict=1):
		arr.append({
			"cost":j.mbr_overall_cost
		})
	for j in frappe.db.sql("SELECT total_cost FROM `tabMBR ovivo Standard Items` WHERE project_startup_sheet='"+str(st)+"'",as_dict=1):
		arr.append({
			"cost":j.total_cost
		})
	for j in frappe.db.sql("SELECT overall_cost FROM `tabBio Tank Calculation` WHERE project_startup_sheet='"+str(st)+"'",as_dict=1):
		arr.append({
			"cost":j.overall_cost
		})
	return arr

@frappe.whitelist()
def get_ro(st):
	arr=[]
	for j in frappe.db.sql("SELECT overall_cost FROM `tabRO Standard Items` WHERE name='"+str(st)+"'",as_dict=1):
		arr.append({
			"cost":j.overall_cost
		})
	return arr


@frappe.whitelist()
def generate_cost(nam,ro_tem,project,rewolutte_ro=None,startup_sheet=None,cip=None):
	ar=[]
	cwt_ref='no_ref'
	doc = frappe.new_doc('Cost Working Tool')
	doc.project_startup_sheet = nam
	doc.choose_ro_template = ro_tem
	doc.project = project
	doc.rewolutte_ro = rewolutte_ro
	doc.choose_cip = cip
	# if(startup_sheet!=None):
	# 	doc.rewolutte_comparison_tool=[]
	# 	query=frappe.db.sql("SELECT name from `tabCost Working Tool` where project_startup_sheet='"+str(startup_sheet)+"' and name!='"+str(nam)+"' order by creation ",as_dict=1)
	# 	if(query):
	# 		cwt_ref = query[0].name
	# 		doc.pre_cost_working_reference = cwt_ref
	########################rewolute comparison
	# if(cwt_ref!="no_ref"):
	# 	pre_cwt=frappe.get_doc("Cost Working Tool",cwt_ref)
	# 	for iii in pre_cwt.standard_cost:
	# 		doc.append("rewolutte_comparison_table",{
	# 			"system_name":iii.system_name,
	# 			"price":iii.total_cost
	# 		})
	doc.save()
	ar.append(doc.name)
	# ar2=[]
	# doc2 = frappe.get_doc('Cost Working Tool',str(doc.name))
	# rew_sys=[]
	# for kk in doc2.rewolutte_comparison_table:
	# 	rew_sys.append(kk.system_name)
	# for i in doc2.standard_cost:
	# 	loop_sys=[]
	# 	for jj in doc2.rewolutte_comparison_table:
	# 		if(jj.system_name==i.system_name):
	# 			jj.rewolutte_price=i.total_cost
	# 			jj.difference_price=i.total_cost-jj.price
	# 		else:
	# 			if(i.system_name not in rew_sys and i.system_name not in loop_sys):
	# 				loop_sys.append(i.system_name)
	# 				ar2.append({"system_name":i.system_name,"rewolutte_price":i.total_cost})
	# for ii in ar2:
	# 	doc2.append("rewolutte_comparison_table",{
	# 		"system_name":ii["system_name"],
	# 		"rewolutte_price":ii["rewolutte_price"]
	# 	})
	# doc2.save()
	# rew_cost=[0]
	# no_rew_cost=[0]
	# diff_cost=[0]
	# for i in doc2.rewolutte_comparison_table:
	# 	rew_cost.append(i.rewolutte_price) if i.rewolutte_price is not None else 0
	# 	no_rew_cost.append(i.price) if i.price is not None else 0
	# 	diff_cost.append(i.difference_price) if i.difference_price is not None else 0
	# doc2.with_rewolutte_price=sum(rew_cost)
	# doc2.without_rewolutte_price=sum(no_rew_cost)
	# doc2.total_difference=sum(diff_cost)
	# doc2.save()
	frappe.db.commit()
	#############################rewolute comparison

	if(cwt_ref!="no_ref"):
		cwt = frappe.get_doc("Cost Working Tool",cwt_ref)
		cwt.rewolutte_reference=doc.name
		cwt.save()
	return ar


@frappe.whitelist()
def get_total_bom_cost(st_list,range_list):
	ar=[]
	arr=[]

	mapping_bom=frappe.db.sql("SELECT distinct(`tabMapping BOM`.`name`)as 'name',parent,process_system,`tabProcess System Parameter Threshold`.`value` as val FROM `tabMapping BOM` INNER JOIN `tabProcess System Parameter Threshold` ON `tabMapping BOM`.`name`=`tabProcess System Parameter Threshold`.`parent` WHERE `tabMapping BOM`.`process_system`='"+str(st_list)+"'",as_dict=1)
	if(mapping_bom):
		for j in mapping_bom:
			if(j.val == str(range_list)):
				rate_from_bom=[]
				for bb in frappe.db.sql("SELECT distinct(name),item_code,parent,stock_qty,stock_uom,total_weight,weight_per_unit,qty from `tabBOM Item` where parent='"+str(j.name)+"' ",as_dict=1):
					if(str(bb.item_code)[slice(3)]!="S60"):
						for rate in frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,`tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(bb.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
							# rate_from_bom.append(rate.base_rate*bb.stock_qty)
							ar.append({
							"item_code":bb.item_code,
							"qty":bb.stock_qty,
							"unit_price":rate.base_rate,
							"total_price":rate.base_rate*bb.stock_qty,
							"bom":str(j.name)
							})
					else:
						query_s6=frappe.db.sql("SELECT rate from `tabBOM Template for S6 Materials` where parent='BOM Template' and item_code='"+str(bb.item_code)+"' ",as_dict=1)
						if(query_s6):
							ww=bb.total_weight
							if(bb.total_weight==0):ww=bb.weight_per_unit*bb.qty
							# rate_from_bom.append(query_s6[0].rate*bb.total_weight)
							ar.append({
							"item_code":bb.item_code,
							"qty":bb.total_weight,
							"unit_price":query_s6[0].rate,
							"total_price":query_s6[0].rate*ww,
							"bom":str(j.name)
							})
						else:
							ar.append({
							"item_code":bb.item_code,
							"qty":bb.total_weight,
							"unit_price":480,
							"total_price":480*bb.total_weight,
							"bom":str(j.name)
							})
	return ar


@frappe.whitelist()
def get_wd(ht_word):
	pass
	# ar=[]
	# document = Document()
	# new_parser = HtmlToDocx()
	# html = '<h1>Hello world</h1>'
	# new_parser.parse_html_string(html, document)
	# document.save('Proposal')
	# return ar