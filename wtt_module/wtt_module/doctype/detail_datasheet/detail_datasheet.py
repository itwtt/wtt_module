# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class Detaildatasheet(Document):
	pass




@frappe.whitelist()
def get_beltpress(val):
	arr=[]
	vals=json.loads(val)
	# frappe.msgprint(str(val))
	ar=[{"name1":'Reverse Osmosis'},{"name1":'Reject RO'},{"name1":'Permeate RO'},{"name1":'Bag Filter'},{"name1":'Cartridge Filter'}]
	for j in vals:
		if(str(j)=='Reverse Osmosis' or str(j)=='Reject RO' or str(j)=='Permeate RO'):
			query=frappe.db.sql("SELECT dp.name,dsp.name1,dsp.parameter FROM `tabDatasheet Parameters` as dp INNER JOIN `tabDatasheet Parameter Table` as dsp ON dsp.parent=dp.name WHERE dp.parameter_type='"+str(j)+"' or dp.parameter_type='Bag Filter' or dp.parameter_type='Cartridge Filter' ORDER BY dsp.idx",as_dict=1)
		else:
			query=frappe.db.sql("SELECT dp.name,dsp.name1,dsp.parameter FROM `tabDatasheet Parameters` as dp INNER JOIN `tabDatasheet Parameter Table` as dsp ON dsp.parent=dp.name WHERE dp.parameter_type='"+str(j)+"' ORDER BY dsp.idx",as_dict=1)
		for i in query:
			arr.append(i)
	
	return arr
