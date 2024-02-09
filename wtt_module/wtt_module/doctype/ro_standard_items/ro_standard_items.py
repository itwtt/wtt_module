import frappe
import json
from frappe.model.document import Document

class ROStandardItems(Document):
	pass
	# def validate(self):
	# 	frappe.msgprint("gss");

# @frappe.whitelist()
# def get_ro(arr):
# 	data=[]
# 	to_python = json.loads(arr)
# 	for i in to_python:
# 		if(str(i['renamed']) == 'RO MEMBRANE'):
# 			for k in frappe.db.sql("SELECT item_code,item_description,name from `tabChild Fetch Items` where item_description='"+str(i['renamed'])+"' and model='"+str(i['model_no'])+"'",as_dict=1):
# 				for g in frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1):
# 					ar.append({
# 						"model_no":i['model_no'],
# 						"item_description":k.item_description,
# 						"rate":g.base_rate
# 						})
# 	return ar