# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class MBRStandardItems(Document):
	pass
@frappe.whitelist()
def get_qty(st):
	ar=[]
	for i in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(st)+"'",as_dict=1):
		ar.append(i)
	return ar

@frappe.whitelist()
def get_mbr(arr):
	ar=[]
	data=[]
	to_python = json.loads(arr)
	for i in to_python:
		if(str(i['flow'])=='0' and str(i['renamed'])!="MBR MODULES"):		
			pass
		else:
			if(str(i['renamed']) == 'ELECTROMAGNETIC FLOWMETER'):
				addflow=float(i['flow'])+20
			elif(str(i['renamed']) == 'TANK'):
				addflow=float(i['flow'])+2000
			else:
				addflow=float(i['flow'])+10
			
			query=frappe.db.sql("SELECT item_code,item_description,name,'Flow and Range are equal'as 'remarks' from `tabChild Fetch Items` where item_description='"+str(i['renamed'])+"' and flow>='"+str(i['flow'])+"' and flow<='"+str(addflow)+"'",as_dict=1)
			if(i['renamed']=="MBR MODULES"):
				query=frappe.db.sql("SELECT item_code,item_description,name,'Based on Model'as 'remarks' from `tabChild Fetch Items` where item_description='"+str(i['renamed'])+"' and model='"+str(i['range'])+"'",as_dict=1)
			for k in query:
				po_rate = frappe.db.sql("SELECT `tabPurchase Order Item`.`base_rate` from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
				if(po_rate):
					for g in po_rate:
						ar.append({
							"item_d":i['item_description'],
							"item_description":k.item_description,
							"rate":g.base_rate
							})
				else:
					if(k.item_code=="MBRSMBRKOPSH1840FRPAHED"):
						ar.append({
							"item_d":i['item_description'],
							"item_description":k.item_description,
							"rate":5102445
							})
					elif(k.item_code=="MBRSMBRKOPSH1844FRPAHED"):
						ar.append({
							"item_d":i['item_description'],
							"item_description":k.item_description,
							"rate":5349337
							})
	return ar

@frappe.whitelist()
def get_elrate(ic,kw,tty,di,do,ai,ao,ai2):
	arr=[]
	ml_el=[]	
	if(ic in ["PANEL","PLC"]):# condition to club the rate for electrical panel and plc items
		panel_items=("PANEL ENCLOSURE","INCOMER MCCB","BUS BAR")
		plc_items=("PLC CPU", "REMOTE CPU", "BUS END COVER", "POWER SUPPLY CARD", "16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)", "MONITOR", "MODEM", "ETHERNET SWITCH", "SMPS", "DP DVI CABLE", "POWER ADAPTER", "TOUCH SCREEN CABLE")
		if(ic=="PANEL"):
			query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(panel_items)+" ",as_dict=1)
			for k in query:
				if(k.item_description=="BUS BAR"):
					k.qty = 3
				query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
				for g in query2:
					ml_el.append(g.base_rate)
		elif(ic=="PLC"):
			ml_el=[50000]
			cards = ["16 DI (DIGITAL INPUT)", "16 DO (DIGITAL OUTPUT)", "8AI ANALOG INPUT - SINGLE END", "4AI ANALOG INPUT - DIFFERENTIAL END", "4AQ (ANALOG OUTPUT)"]
			query = frappe.db.sql("SELECT distinct(item_code) as 'item_code','1' as 'qty',item_description FROM `tabElectrical Child Items` WHERE item_description IN "+str(plc_items)+" ",as_dict=1)
			for k in query:
				if(k.item_description in cards):
					di_cal = float(di)/16
					do_cal = float(do)/16
					ai_cal = float(ai)/4
					ao_cal = float(ao)/8
					ai2_cal = float(ai2)/8
					# quantity calulation for cards based on input output calculatuion
					ar=[di_cal,do_cal,ai2_cal,ai_cal,ao_cal]
					for i in range(len(ar)):
						if(k.item_description==cards[i]):
							k.qty = round(ar[i])
							if(round(ar[i])<ar[i]):
								k.qty = round(ar[i])+1						

				query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
				for g in query2:
					ml_el.append(g.base_rate)
	else:
		query=frappe.db.sql("SELECT item_code,qty FROM `tabElectrical Child Items` WHERE kw='"+str(kw)+"' and type='"+str(tty)+"' GROUP BY item_code",as_dict=1)
		for k in query:
			query2=frappe.db.sql("SELECT `tabPurchase Order Item`.`item_code`,`tabPurchase Order Item`.`qty`,(`tabPurchase Order Item`.`base_rate`*'"+str(k.qty)+"') as 'base_rate' from `tabPurchase Order` INNER JOIN `tabPurchase Order Item` ON `tabPurchase Order Item`.`parent`=`tabPurchase Order`.`name` WHERE `tabPurchase Order`.`docstatus`!=2 and `tabPurchase Order`.`workflow_state`!='Rejected' and `tabPurchase Order Item`.`item_code`='"+str(k.item_code)+"' ORDER BY `tabPurchase Order`.`creation` DESC LIMIT 1",as_dict=1)
			for g in query2:
				ml_el.append(g.base_rate)
	v=sum(ml_el)
	return v
