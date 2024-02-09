# Copyright (c) 2021, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime,timedelta
import calendar
from pytz import timezone

class MaterialMovement(Document):
	
	def on_submit(self):
		if(self.inward_outward!="Inward"):
			pass
		else:
			df=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
			dt=(datetime.now(timezone("Asia/Kolkata"))+timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
			datetime_format1 = datetime.strptime(df,"%Y-%m-%d %H:%M:%S")
			datetime_format2 = datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
			items=0
			for i in frappe.db.sql("SELECT count(name)as cnt FROM `tabPurchase Order Item` WHERE parent='"+str(self.purchase_order)+"' GROUP BY parent ",as_dict=1):
				items=i.cnt
			if(int(items)>50):
				datetime_format2+=timedelta(days=1)
			if(calendar.day_name[datetime_format2.weekday()]=="Sunday"):
				datetime_format2+=timedelta(days=1)

			difference = datetime_format2-datetime_format1
			hrs = difference.total_seconds() / 3600
			doc=frappe.new_doc("Task Allocation")
			doc.user=frappe.session.user
			doc.employee="WTT1402"
			doc.mr_inward=self.name
			doc.append("works_table",{
				"type_of_work":str(self.purchase_order),
				"description":"Receipt should be raised for PO",
				"from_time":datetime_format1,
				"to_time":datetime_format2,
				"hours":hrs
				})
			doc.save()
			frappe.db.commit()
			frappe.msgprint("Task Allocated for "+str(doc.employee_name)+" Succesfully")
			# aa=datetime.now().replace(microsecond=00)
			# bb=aa.replace(hour=18,minute=00,second=00)
			# t1=aa
			# t2=aa+timedelta(hours=8)
			# if(aa>bb):
			# 	t1=(datetime.now()+timedelta(days=1)).replace(hour=9,minute=00,second=00)
			# 	if(calendar.day_name[((datetime.now()).date()).weekday()]=='Saturday'):
			# 		t1=(datetime.now()+timedelta(days=2)).replace(hour=9,minute=00,second=00)

			# 	t2=t1+timedelta(hours=8)
			# difference = t2 - t1
			# hrs1 = difference.total_seconds() / 3600

			# if(self.sample==0):
			# 	doc=frappe.new_doc("Task Allocation")
			# 	doc.user=frappe.session.user
			# 	doc.employee='WTT1382'
			# 	doc.mr_inward=self.name
			# 	doc.append("works_table",{
			# 		"type_of_work":str(self.purchase_order),
			# 		"description":"Receipt Should be raised for PO",
			# 		"from_time":t1,
			# 		"to_time":t2,
			# 		"hours":hrs1
			# 		})
			# 	doc.save()
	def on_cancel(self):
		if frappe.db.exists("Task Allocation",{"mr_inward":self.name}):
			frappe.db.sql("DELETE FROM `tabTask Allocation` WHERE mr_inward='"+str(self.name)+"' ",as_dict=1)
