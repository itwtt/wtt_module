from __future__ import unicode_literals
import frappe
import json
import calendar
from frappe.utils import cstr, flt, getdate, new_line_sep, nowdate, add_days, get_link_to_form
from frappe import msgprint, _
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.stock_balance import update_bin_qty, get_indented_qty
from erpnext.controllers.buying_controller import BuyingController
from erpnext.manufacturing.doctype.work_order.work_order import get_item_details
from erpnext.buying.utils import check_on_hold_or_closed_status, validate_for_items
from erpnext.stock.doctype.item.item import get_item_defaults
from datetime import date,datetime,timedelta
from frappe.utils.xlsxutils import make_xlsx
from six import string_types
from pytz import timezone

from erpnext.stock.doctype.material_request.material_request import MaterialRequest

class customMR(MaterialRequest):
	
			
	def validate(self):
		super().validate()
		if(self.workflow_state=='Approved by HOD'):
			if(self.hod_approved_date==None):
				self.hod_approved_date=str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'))
		
		
		aa=str(self.name)
		self.mr=aa[6:]

		av=[]
		av.append(self.project)

		for i in self.items:
			if i.project in av:
				pass
			else:
				frappe.throw("Can't able to raise the MR for multiple project, choose the single project in item table.")

	def on_submit(self):
		super().on_submit()
		count=0
		ead=date.today()-timedelta(days=2)
		if(frappe.session.user=='giri@wttindia.com' or frappe.session.user=='purchase@wttindia.com'):
			ddoc1 = frappe.db.sql("SELECT count(name)as mr from `tabMaterial Request` WHERE workflow_state='Emergency Approval' and approver='"+str(frappe.session.user)+"' ",as_dict=1)
			# if (ddoc1):
			# 	for i in ddoc1:
			# 		count+=i.mr
			# # frappe.msgprint(str(count))
			# ddoc = frappe.db.sql("SELECT name from `tabMaterial Request` WHERE workflow_state='Emergency Approval' and approved_date<='"+str(ead)+"' and approver='"+str(frappe.session.user)+"' ",as_dict=1)
			# if(ddoc or count>1):
			# 	frappe.throw("Please get the approval from MD for Previous Record")


		df=datetime.strptime(str(datetime.now().replace(microsecond=00)),'%Y-%m-%d %H:%M:%S')
		dt=datetime.strptime(str(df),'%Y-%m-%d %H:%M:%S')+timedelta(days=4)
		bb = dt.weekday()
		godfd=calendar.day_name[bb]
		if(godfd=="Sunday"):
			dt=datetime.strptime(str(df),'%Y-%m-%d %H:%M:%S')+timedelta(days=7)
		difference = dt - df
		hrs = difference.total_seconds() / 3600
		task_to=frappe.db.get_value("Project Cast",self.project,"employee")
		if(self.task):
			if(task_to==None):
				frappe.throw("Details missing from Purchase Team who handling this Project, Create a Cast by using button")
			else:			
				if (frappe.db.sql("SELECT * FROM `tabTask Allocation` WHERE mr_inward='"+str(self.name)+"' ",as_dict=1)):
					# pass
					task=frappe.new_doc("Task Allocation")
					task.user=frappe.session.user
					task.employee=task_to
					task.mr_inward='WTT1396'
					task.append("works_table",{
						"type_of_work":str(self.name)+" ("+str(self.project)+")",
						"description":"MR has been approved, Raise PO for "+self.title,
						"from_time":datetime.strptime(str(datetime.now().replace(microsecond=00)),'%Y-%m-%d %H:%M:%S'),
						"to_time":dt,
						"hours":hrs
						})
					task.save()
					frappe.db.commit()
					frappe.msgprint("Task Allocated for "+str(task.employee_name))

				else:
					task=frappe.new_doc("Task Allocation")
					task.user=frappe.session.user
					task.employee=task_to
					task.mr_inward=self.name
					task.append("works_table",{
						"type_of_work":str(self.name)+" ("+str(self.project)+")",
						"description":"MR has been approved, Raise PO for "+self.title,
						"from_time":datetime.strptime(str(datetime.now().replace(microsecond=00)),'%Y-%m-%d %H:%M:%S'),
						"to_time":dt,
						"hours":hrs
						})
					task.save()
					frappe.db.commit()
					frappe.msgprint("Task Allocated for "+str(task.employee_name))
		aa=str(self.name)
		self.mr=aa[6:]
		today = str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d'))
		now=str(datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S'))	
		doc=frappe.get_doc("Material Request",self.name)
		doc.db_set("approved_date",today)
		doc.db_set("approval_date",frappe.get_value("User",frappe.session.user,"full_name"))
		doc.db_set("approved_time",now)
		doc.db_set("approver",frappe.session.user)
		doc.db_set("final_status",self.status)

		if(self.downgrade_value):
			vala = frappe.db.set_value("Material Request",self.name,'downgrade_value','reapproved')

	def on_cancel(self):
		try:
			super().on_cancel()
			if ((frappe.db.exists("Task Allocation", {"mr_inward": self.name}))):
				frappe.db.sql("DELETE FROM `tabTask Allocation` WHERE mr_inward='"+str(self.name)+"' ",as_dict=1)
				
			dop=frappe.get_doc("Material Request",self.name)
			dop.db_set("final_status",self.status)
			doc=frappe.db.sql("SELECT pot.material_request,po.name FROM `tabPurchase Order Item`as pot,`tabPurchase Order`as po WHERE pot.parent=po.name and pot.material_request='"+str(self.name)+"' and po.docstatus!=2 and po.workflow_state!='Rejected' and po.workflow_state!='Cancelled' ",as_dict=1)
			if doc:
				frappe.throw("This MR is linked with PO")
		except Exception as e:
			frappe.throw(str(e))

	def on_trash(self):
		super().on_trash()
		doc=frappe.db.sql("SELECT pot.material_request,po.name FROM `tabPurchase Order Item`as pot,`tabPurchase Order`as po WHERE pot.parent=po.name and pot.material_request='"+str(self.name)+"' ",as_dict=1)
		if doc:
			frappe.throw("This MR is linked with PO")

	def set_title(self):
		'''Set title as comma separated list of items'''
		if not self.title:
			items = ', '.join([d.item_name for d in self.items][:3])
			self.title = _('{1}').format(self.material_request_type, items)[:100]

	@frappe.whitelist()
	def download_table(self):
		ur=[]
		xl=[["S.No","Item Code","Description","Technical Description","Item Group","Qty","UOM","Remarks"]]
		for i in self.items:
			xl.append([i.idx,i.item_code,i.description,i.technical_description,i.item_group,i.qty,i.uom,i.remarks])
		xlsx_file = make_xlsx(xl,"ChildTable")
		file_data = xlsx_file.getvalue()
		_file = frappe.get_doc({
		"doctype": "File",
		"file_name":"ChildTable.xlsx",
		"folder": "Home/Attachments",
		"content": file_data})
		_file.save()
		ur.append({"url":_file.file_url})
		return ur

@frappe.whitelist()
def check_repeating_items(parent):
	for i in frappe.db.sql("SELECT count(name)as name,GROUP_CONCAT(distinct(idx))as row from `tabMaterial Request Item` WHERE parent='"+str(self.name)+"' and creation>'2022-12-03 08:22:17.489923' GROUP BY item_code ",as_dict=1):
		if(i.name>1):
			frappe.throw("Same Items are Repeating "+str(i.row)+".Club them or Kindly use Pre MR")