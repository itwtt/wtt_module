# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date,datetime,timedelta
from frappe.utils import getdate

class MeetingSlotBooking(Document):
	def validate(self):
		doc=frappe.db.sql("SELECT from_time,to_time,department from `tabMeeting Slot Booking` WHERE workflow_state='Approved' and venue='"+str(self.venue)+"' and name!='"+str(self.name)+"' ",as_dict=1)
		if(doc):
			for i in doc:
				if(getdate(i.from_time)<=getdate(self.from_time)<=getdate(i.to_time)):
					frappe.throw("Slot already booked by "+i.department +" at "+str(self.venue))
				elif(getdate(i.from_time)<=getdate(self.to_time)<=getdate(i.to_time)):
					frappe.throw("Slot already booked by "+i.department +" at "+str(self.venue))
	def on_submit(self):
		doc=frappe.db.sql("SELECT from_time,to_time,department from `tabMeeting Slot Booking` WHERE workflow_state='Approved' and venue='"+str(self.venue)+"' and name!='"+str(self.name)+"' ",as_dict=1)
		if(doc):
			for i in doc:
				if(getdate(i.from_time)<=getdate(self.from_time)<=getdate(i.to_time)):
					frappe.throw("Slot already Approved by "+i.department +" at "+str(self.venue))
				elif(getdate(i.from_time)<=getdate(self.to_time)<=getdate(i.to_time)):
					frappe.throw("Slot already Approved by "+i.department +" at "+str(self.venue))

		df=datetime.strptime(str(datetime.now().replace(microsecond=00)),'%Y-%m-%d %H:%M:%S'),
		dt=datetime.strptime(str(df.replace(hour=18,minute=00,second=00)),'%Y-%m-%d %H:%M:%S')
		difference = dt - df
		hrs = difference.total_seconds() / 3600
		doc=frappe.new_doc("Task Allocation")
		doc.user=frappe.session.user
		doc.employee='WTT1211'
		doc.mr_inward=self.name
		doc.append("works_table",{
			"type_of_work":'Meeting Slot for '+str(self.department),
			"description":"Update the meeting details to MD sir",
			"from_time":df,
			"to_time":dt,
			"hours":hrs
			})
		doc.save()
		frappe.db.commit()
	def on_cancel(self):
		frappe.db.sql("DELETE FROM `tabTask Allocation` WHERE mr_inward='"+str(self.name)+"' ",as_dict=1)
	



