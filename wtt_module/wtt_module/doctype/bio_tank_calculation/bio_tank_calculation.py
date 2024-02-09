# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class BioTankCalculation(Document):
	pass
@frappe.whitelist()
def check_system(pes,system):
	aa="Not Found"
	if(frappe.db.sql("SELECT * from `tabSelected Process System` where selected_system_name='"+str(system)+"' and parent='"+str(pes)+"' ",as_dict=1)):
		aa="Found"
	return aa

@frappe.whitelist()
def get_mf(arr):
	ar=[]
	data=[]
	to_python = json.loads(arr)
	for i in to_python:
		if(str(i['flow'])=='0' and str(i['renamed']) not in ['MBR MODULES','DIFFUSER']):
			if(i['renamed'] in ['OTT LATERAL','PIPE']):
				query=frappe.db.sql("SELECT item_code,item_description,name,'Based on Model'as 'remarks' from `tabChild Fetch Items` where item_description='"+str(i['renamed'])+"' and model='"+str(i['range'])+"'",as_dict=1)
				for k in query:
					for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
						ar.append({
							"item_d":i['item_description'],
							"item_description":k.item_description,
							"rate":g.base_rate
							})
		else:
			if(str(i['renamed']) == 'ELECTROMAGNETIC FLOWMETER'):
				addflow=float(i['flow'])+20
			elif(str(i['renamed']) == 'TANK'):
				addflow=float(i['flow'])+2000
			elif(str(i['renamed']) == 'DOSING PUMP'):
				addflow=float(i['flow'])+100
			else:
				addflow=float(i['flow'])+10
			query=frappe.db.sql("SELECT item_code,item_description,name,'Flow and Range are equal'as 'remarks' from `tabChild Fetch Items` where item_description='"+str(i['renamed'])+"' and flow>='"+str(i['flow'])+"' and flow<='"+str(addflow)+"'",as_dict=1)
			if not query:
				query=frappe.db.sql("SELECT item_code,item_description,name,'Based on Model'as 'remarks' from `tabChild Fetch Items` where item_description='"+str(i['renamed'])+"' and model='"+str(i['range'])+"'",as_dict=1)
			for k in query:
				for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
					ar.append({
						"item_d":i['item_description'],
						"item_description":k.item_description,
						"rate":g.base_rate
						})
	return ar