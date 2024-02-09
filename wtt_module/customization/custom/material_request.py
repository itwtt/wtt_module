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

class MaterialRequest(BuyingController):
	def before_save(self):
		for i in frappe.db.sql("SELECT count(name)as name,GROUP_CONCAT(distinct(idx))as row from `tabMaterial Request Item` WHERE parent='"+str(self.name)+"' and creation>'2022-12-03 08:22:17.489923' GROUP BY item_code ",as_dict=1):
			if(i.name>1):
				pass
				# frappe.throw("Same Items are Repeating "+str(i.row)+".Club them or Kindly use Pre MR.")
	def validate(self):
		
		if(self.workflow_state=='Approved by HOD'):
			if(self.hod_approved_date==None):
				self.hod_approved_date=date.today()
		aa=str(self.name)
		self.mr=aa[6:]
		super(MaterialRequest, self).validate()
		self.set_title()
		self.validate_schedule_date()
		self.check_for_on_hold_or_closed_status('Sales Order', 'sales_order')
		self.validate_uom_is_integer("uom", "qty")

		if not self.status:
			self.status = "Draft"
			self.final_status=self.status
		else:
			self.final_status=self.status

		from erpnext.controllers.status_updater import validate_status
		validate_status(self.status,
			["Draft", "Submitted", "Stopped", "Cancelled", "Pending",
			"Partially Ordered", "Ordered", "Issued", "Transferred", "Received"])

		validate_for_items(self)

		self.set_title()
		# self.validate_qty_against_so()
		# NOTE: Since Item BOM and FG quantities are combined, using current data, it cannot be validated
		# Though the creation of Material Request from a Production Plan can be rethought to fix this

	def on_submit(self):
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
		if(self.task):
			if (frappe.db.sql("SELECT * FROM `tabTask Allocation` WHERE mr_inward='"+str(self.name)+"' ",as_dict=1)):
				pass
			else:
				task=frappe.new_doc("Task Allocation")
				task.user=frappe.session.user
				task.employee='WTT1396'
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
		aa=str(self.name)
		self.mr=aa[6:]
		today = date.today()
		now=datetime.now()		
		doc=frappe.get_doc("Material Request",self.name)
		doc.db_set("approved_date",today)
		doc.db_set("approval_date",frappe.get_value("User",frappe.session.user,"full_name"))
		doc.db_set("approved_time",now)
		doc.db_set("approver",frappe.session.user)
		doc.db_set("final_status",self.status)

		if(self.downgrade_value):
			vala = frappe.db.set_value("Material Request",self.name,'downgrade_value','reapproved')
		
	def set_title(self):
		'''Set title as comma separated list of items'''
		if not self.title:
			items = ', '.join([d.item_name for d in self.items][:3])
			self.title = _('{1}').format(self.material_request_type, items)[:100]

	def on_cancel(self):
		if ((frappe.db.exists("Task Allocation", {"mr_inward": self.name}))):
			frappe.db.sql("DELETE FROM `tabTask Allocation` WHERE mr_inward='"+str(self.name)+"' ",as_dict=1)
			
		dop=frappe.get_doc("Material Request",self.name)
		dop.db_set("final_status",self.status)
		doc=frappe.db.sql("SELECT pot.material_request,po.name FROM `tabPurchase Order Item`as pot,`tabPurchase Order`as po WHERE pot.parent=po.name and pot.material_request='"+str(self.name)+"' and po.workflow_state!='Rejected' and po.workflow_state!='Cancelled' ",as_dict=1)
		if doc:
			# for i in doc:
			# 	frappe.msgprint(str(i.material_request))
			frappe.throw("This MR is linked with PO")

	def on_trash(self):
		doc=frappe.db.sql("SELECT pot.material_request,po.name FROM `tabPurchase Order Item`as pot,`tabPurchase Order`as po WHERE pot.parent=po.name and pot.material_request='"+str(self.name)+"' ",as_dict=1)
		if doc:
			# for i in doc:
			# 	frappe.msgprint(str(i.name))
			frappe.throw("This MR is linked with PO")





@frappe.whitelist()
def make_request(source_name, target_doc=None):
	def postprocess(source, target):
		target.material_request_type="Material Issue"
		target.schedule_date=target.transaction_date
		for i in target.get("items"):
			i.schedule_date=target.transaction_date
	doc = get_mapped_doc("Material Request", source_name, {
		"Material Request": {
			"doctype": "Material Request",
			"validation": {
				"docstatus": ["=", 1]
			}
		},
		"Material Request Item": {
			"doctype": "Material Request Item",
			"field_map": {
				"stock_accepted": "qty",
				"parent":"dc_against_mr",
				"name":"dc_against_mr_item"
			}
		}
	}, target_doc,postprocess)
	return doc


@frappe.whitelist()
def make_tag(source_name, target_doc=None):
	def postprocess(source, target):
		lst = []
		item = []
		mr=[]
		for i in target.get("items"):
			if i.item_code not in lst:
				item.append(i)
				lst.append(i.item_code)
			else:
				item[lst.index(i.item_code)].qty += i.qty
		target.items = item
	doc = get_mapped_doc("Tag Listing", source_name, {
		"Tag Listing": {
			"doctype": "Material Request",
			"validation": {
				"docstatus": ["=", 0]
			}
		},
		"Table list": {
			"doctype": "Material Request Item"
		}
	}, target_doc,postprocess)
	return doc

# @frappe.whitelist()
# def make_request_for_quotation(source_name, target_doc=None):
# 	doclist = get_mapped_doc("Material Request", source_name, 	{
# 		"Material Request": {
# 			"doctype": "Request for Quotation",
# 			"validation": {
# 				"docstatus": ["=", 1],
# 				"material_request_type": ["=", "Purchase"]
# 			},
# 			"field_map": {
# 				"name": "material_series"
# 			}
# 		},
# 		"Material Request Item": {
# 			"doctype": "Request for Quotation Item",
# 			"field_map": [
# 				["name", "material_request_item"],
# 				["parent", "material_request"],
# 				["project","project_name"],
# 				["uom", "uom"]
# 			]
# 		}
# 	}, target_doc)

# 	return doclist

@frappe.whitelist()
def get_pre_mr(source_name, target_doc=None,args=None):
	doclist = get_mapped_doc("Pre MR", source_name, 	{
		"Pre MR": {
			"doctype": "Material Request",
			"validation": {
				"docstatus": ["=", 0]
			}
		},
		"Pre MR Table": {
			"doctype": "Material Request Item",
			"field_map": [
				["description","description"],
				["technical_description","technical_description"],
				["qty","pre_mr_qty"],
				["uom", "pre_mr_uom"],
				["req_qty","qty"],
				["req_uom", "uom"]
			]
		}
	}, target_doc)
	return doclist






@frappe.whitelist()
def make_request_for_quotation(source_name, target_doc=None,args=None):
	if args is None:
		args = {}
	if isinstance(args, string_types):
		args = json.loads(args)

	def select_item(d):
		filtered_items = args.get('filtered_children', [])
		child_filter = d.name in filtered_items if filtered_items else True

		return d.ordered_qty < d.stock_qty and child_filter 
	
	doclist = get_mapped_doc("Material Request", source_name, 	{
		"Material Request": {
			"doctype": "Request for Quotation",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["=", "Purchase"]
			},
			"field_map": {
				"name": "material_series"
			}
		},
		"Material Request Item": {
			"doctype": "Request for Quotation Item",
			"field_map": [
				["name", "material_request_item"],
				["parent", "material_request"],
				["project","project_name"],
				["uom", "uom"]
			],
			"condition": select_item
		}
	}, target_doc)
	return doclist

@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None):
	def postprocess(source, target_doc):
		if frappe.flags.args and frappe.flags.args.default_supplier:
			# items only for given default supplier
			supplier_items = []
			for d in target_doc.items:
				default_supplier = get_item_defaults(d.item_code, target_doc.company).get('default_supplier')
				if frappe.flags.args.default_supplier == default_supplier:
					supplier_items.append(d)
			target_doc.items = supplier_items
		set_missing_values(source, target_doc)

	def select_item(d):
		return d.ordered_qty < d.stock_qty

	doclist = get_mapped_doc("Material Request", source_name, 	{
		"Material Request": {
			"doctype": "Purchase Order",
			"validation": {
				"docstatus": ["=", 1],
				"material_request_type": ["=", "Purchase"]
			}
		},
		"Material Request Item": {
			"doctype": "Purchase Order Item",
			"field_map": [
				["name", "material_request_item"],
				["parent", "material_request"],
				["qty", "required_qty"],
				["uom", "stock_uom"],
				["uom", "uom"],
				["sales_order", "sales_order"],
				["sales_order_item", "sales_order_item"]
			],
			"postprocess": update_item,
			"condition": select_item
		}
	}, target_doc, postprocess)

	return doclist



@frappe.whitelist()
def po_func(arr):
	data=[]
	to_python = json.loads(arr)
	
	for i in to_python:
		doc=frappe.db.sql("SELECT poi.name,poi.idx,poi.parent,poi.creation,poi.qty,poi.supplier_description FROM `tabPurchase Order Item`as poi INNER JOIN `tabPurchase Order`as po ON po.name=poi.parent WHERE po.workflow_state!='Rejected' and po.docstatus!=2 and poi.material_request='"+str(i["parent"])+"' and poi.material_request_item='"+str(i["nn"])+"'",as_dict=1)
		if doc:
			for j in doc:
				if(j.supplier_description==None):
					j.supplier_description="-"
				dot=frappe.db.sql("SELECT idx,parent,creation,qty FROM `tabPurchase Receipt Item` WHERE purchase_order='"+str(j.parent)+"' and material_request='"+str(i["parent"])+"' and purchase_order_item='"+str(j.name)+"' and material_request_item='"+str(i["nn"])+"' and docstatus!=2 ",as_dict=1)
				if dot:
					for k in dot:
						data.append({
							"idx":i["idx"],
							"description":i["description"],
							"technical_description":i["technical_description"],
							"supplier_description":j.supplier_description,
							"mr_qty":i["qty"],
							"qty":j.qty,
							"pr_row":k.idx,
							"pr_qty":k.qty,
							"rate":j.idx,
							"parent":j.parent,
							"pr":k.parent,
							"status":frappe.db.get_value("Purchase Order",j.parent,"workflow_state"),
							"pr_status":frappe.db.get_value("Purchase Receipt",k.parent,"status")
							})
				else:
					data.append({
						"idx":i["idx"],
						"description":i["description"],
						"technical_description":i["technical_description"],
						"supplier_description":j.supplier_description,
						"mr_qty":i["qty"],
						"qty":j.qty,
						"rate":j.idx,
						"pr_row":"-",
						"pr_qty":"-",
						"parent":j.parent,
						"pr":"-",
						"status":frappe.db.get_value("Purchase Order",j.parent,"workflow_state"),
						"pr_status":"-"
						})
		else:
			data.append({
				"idx":i["idx"],
				"description":i["description"],
				"technical_description":i["technical_description"],
				"supplier_description":"-",
				"mr_qty":i["qty"],
				"qty":"-",
				"rate":"-",
				"pr_row":"-",
				"pr_qty":"-",
				"parent":"Not Linked",
				"pr":"-",
				"status":"-",
				"pr_status":"-"
				})
	return data

@frappe.whitelist()
def download_po_func(arr):
	data=[]
	to_python = json.loads(arr)
	for i in to_python:
		doc=frappe.db.sql("SELECT poi.name,poi.idx,poi.parent,poi.creation,poi.qty,poi.base_rate FROM `tabPurchase Order Item`as poi INNER JOIN `tabPurchase Order`as po ON po.name=poi.parent WHERE po.workflow_state NOT IN ('Cancelled','Rejected') and poi.material_request='"+str(i["parent"])+"' and poi.material_request_item='"+str(i["nn"])+"'",as_dict=1)
		if doc:
			for j in doc:
				dot=frappe.db.sql("SELECT idx,parent,creation,qty FROM `tabPurchase Receipt Item` WHERE purchase_order='"+str(j.parent)+"' and material_request='"+str(i["parent"])+"' and purchase_order_item='"+str(j.name)+"' and material_request_item='"+str(i["nn"])+"' and docstatus!=2 ",as_dict=1)
				if dot:
					for k in dot:
						data.append({
							"idx":i["idx"],
							"item_code":i["item"],
							"description":i["description"],
							"technical_description":i["technical_description"],
							"mr_qty":i["qty"],
							"qty":j.qty,
							"uom":j.uom,
							"porate":j.base_rate,
							"poamnt":j.amount,
							"sup":frappe.db.get_value("Purchase Order",j.parent,"supplier"),
							"pr_row":k.idx,
							"pr_qty":k.qty,
							"rate":j.idx,
							"parent":j.parent,
							"pr":k.parent,
							"status":frappe.db.get_value("Purchase Order",j.parent,"workflow_state"),
							"pr_status":frappe.db.get_value("Purchase Receipt",k.parent,"status")
							})
				else:
					data.append({
						"idx":i["idx"],
						"item_code":i["item"],
						"description":i["description"],
						"technical_description":i["technical_description"],
						"mr_qty":i["qty"],
						"qty":j.qty,
						"uom":j.uom,
						"porate":j.base_rate,
						"poamnt":j.amount,
						"sup":frappe.db.get_value("Purchase Order",j.parent,"supplier"),
						"rate":j.idx,
						"pr_row":"-",
						"pr_qty":"-",
						"parent":j.parent,
						"pr":"-",
						"status":frappe.db.get_value("Purchase Order",j.parent,"workflow_state"),
						"pr_status":"-"
						})
		else:
			data.append({
				"idx":i["idx"],
				"item_code":i["item"],
				"description":i["description"],
				"technical_description":i["technical_description"],
				"mr_qty":i["qty"],
				"qty":"-",
				"uom":"-",
				"porate":"-",
				"poamnt":"-",
				"sup":"-",
				"rate":"-",
				"pr_row":"-",
				"pr_qty":"-",
				"parent":"Not Linked",
				"pr":"-",
				"status":"-",
				"pr_status":"-"
				})
	ur=[]
	xl=[["ITEM CODE","DESCRIPTION","TECHNICAL DECRIPTION","MR QTY","PO QTY","UOM","PO RATE","PO AMOUNT","SUPPLIER","PO ROW","PURCHASE ORDER","PO STATUS","PR QTY","PR ROW","PURCHASE RECEIPT","PR STATUS"]]
	for i in data:
		xl.append([i["item_code"],i["description"],i["technical_description"],i["mr_qty"],i["qty"],i["uom"],i["porate"],i["poamnt"],i["sup"],i["rate"],i["parent"],i["status"],i["pr_qty"],i["pr_row"],i["pr"],i["pr_status"]])
	
	xlsx_file = make_xlsx(xl, "PR Link")
	file_data = xlsx_file.getvalue()

	_file = frappe.get_doc({
	"doctype": "File",
	"file_name": "PR Link.xlsx",
	"folder": "Home/Attachments",
	"content": file_data})
	_file.save()
	ur.append({"url":_file.file_url})
	return ur


@frappe.whitelist()
def download_rate(arr):
	data=[]
	to_python = json.loads(arr)
	for i in to_python:	
		doc=frappe.db.sql("SELECT base_rate,parent,qty FROM `tabPurchase Order Item` WHERE item_code='"+str(i["item"])+"' ORDER BY creation DESC LIMIT 1",as_dict=1)
		if doc:
			for j in doc:
				data.append({
					"item_code":i["item"],
					"description":i["description"],
					"technical_description":i["technical_description"],
					"qty":i["qty"],
					"rate":round(j.base_rate,2),
					"amount":float(i["qty"])*round(j.base_rate,2),
					"parent":j.parent,
					"status":frappe.db.get_value("Purchase Order",j.parent,"workflow_state")
					})
		else:
			data.append({
				"item_code":i["item"],
				"description":i["description"],
				"technical_description":i["technical_description"],
				"qty":i["qty"],
				"rate":0,
				"amount":0,
				"parent":"Not Linked",
				"status":"-"
				})
	ur=[]
	xl=[["ITEM CODE","DESCRIPTION","TECHNICAL DECRIPTION","QTY","RATE","AMOUNT","PO NO","PO STATUS"]]
	for i in data:
		xl.append([i["item_code"],i["description"],i["technical_description"],i["qty"],i["rate"],i["amount"],i["parent"],i["status"]])
	
	xlsx_file = make_xlsx(xl, "PO_RATE Link")
	file_data = xlsx_file.getvalue()

	_file = frappe.get_doc({
	"doctype": "File",
	"file_name": "PO_RATE Link.xlsx",
	"folder": "Home/Attachments",
	"content": file_data})
	_file.save()
	ur.append({"url":_file.file_url})
	return ur



@frappe.whitelist()
def get_rate(arr):
	d=[]
	summ=0
	to_python = json.loads(arr)
	for i in to_python:
		for j in frappe.db.sql("SELECT base_rate FROM `tabPurchase Order Item` WHERE item_code='"+str(i["item"])+"' ORDER BY creation DESC LIMIT 1",as_dict=1):
			d.append({
				"amt":flt(i["qty"])*flt(j.base_rate)
			})
	for q in d:
		summ=summ+flt(q["amt"])				
	return summ

@frappe.whitelist()
def po_rate_func(arr):
	data=[]
	to_python = json.loads(arr)
	
	for i in to_python:	
		#doc=frappe.db.sql("SELECT rate,parent,qty FROM `tabPurchase Order Item` WHERE item_code='"+str(i["item"])+"' ",as_dict=1)
		doc=frappe.db.sql("SELECT base_rate,parent,qty FROM `tabPurchase Order Item` WHERE item_code='"+str(i["item"])+"' and docstatus=1 ORDER BY creation DESC LIMIT 1",as_dict=1)
		if doc:
			for j in doc:
				data.append({
					"description":i["description"],
					"technical_description":i["technical_description"],
					"qty":i["qty"],
					"rate":round(j.base_rate,2),
					"parent":j.parent,
					"date":getdate(frappe.db.get_value("Purchase Order",j.parent,"approved_date")).strftime("%d-%m-%Y"),
					"supplier":frappe.db.get_value("Purchase Order",j.parent,"supplier"),
					"status":frappe.db.get_value("Purchase Order",j.parent,"workflow_state")
					})
		else:
			data.append({
				"description":i["description"],
				"technical_description":i["technical_description"],
				"qty":i["qty"],
				"rate":"-",
				"parent":"Not Linked",
				"date":"",
				"supplier":"",
				"status":"-"
				})

	
	return data



@frappe.whitelist()
def downgrade(name):
	val = frappe.db.set_value("Material Request",name,'workflow_state','Created')
	val1 = frappe.db.set_value("Material Request",name,'docstatus',0)
	val1 = frappe.db.set_value("Material Request",name,'edit_items',1)
	val2 = frappe.db.set_value("Material Request",name,'status','Pending')
	val3 = frappe.db.set_value("Material Request",name,'downgrade_value','downgraded')
	doc = frappe.get_doc("Material Request",name)
	doc.edit_table=[]
	for i in doc.items:
		query=frappe.db.sql("SELECT poi.material_request_item FROM `tabPurchase Order` as po INNER JOIN `tabPurchase Order Item` as poi on po.name=poi.parent WHERE poi.material_request_item='"+str(i.name)+"' and po.workflow_state!='Cancelled' and po.workflow_state!='Rejected' and poi.material_request='"+str(name)+"' ",as_dict=1)
		if query:
			pass
		else:
			# frappe.db.set_value("Material Request Item",i.name,"docstatus",0)
			if(i.remarks==None and i.drawing_no==None):
				doc.append("edit_table",{
					"item_code":i.item_code,
					"qty":i.qty,
					"uom":i.uom,
					"row_name":i.name,
					"remarks":"-",
					"drawing_no":"-"
					# "corrected_from":i.name
					})
			elif(i.remarks==None):
				doc.append("edit_table",{
					"item_code":i.item_code,
					"qty":i.qty,
					"uom":i.uom,
					"drawing_no":i.drawing_no,
					"row_name":i.name,
					"remarks":"-"
					# "corrected_from":i.name
					})
			elif(i.drawing_no==None):
				doc.append("edit_table",{
					"item_code":i.item_code,
					"qty":i.qty,
					"uom":i.uom,
					"remarks":i.remarks,
					"row_name":i.name,
					"drawing_no":"-"
					# "corrected_from":i.name
					})
			else:
				doc.append("edit_table",{
					"item_code":i.item_code,
					"qty":i.qty,
					"uom":i.uom,
					"remarks":i.remarks,
					"row_name":i.name,
					"drawing_no":i.drawing_no
					# "corrected_from":i.name
					})	
	doc.save()

@frappe.whitelist()
def remove_items(ar,nn):
	doc=frappe.get_doc("Material Request",nn)


@frappe.whitelist()
def clientscript(lr):
	ar=[]
	doc=frappe.get_doc("Material Request",str(lr))
	if(doc.approved_date==None):
		dd=doc.modified
		d=dd.date()
	else:
		d=doc.approved_date
	
	diff=(date.today()-d).days
	if(diff>0):
		ar.append({"days":doc.workflow_state+" by "+str(diff)+" Days"})
	else:
		ar.append({"days":doc.workflow_state+" by Today"})
	# +frappe.get_value("User",doc.modified_by,"full_name")+" "
	for i in doc.items:
		ar.append(i)

	return ar

@frappe.whitelist()
def approve_after_emergency_approval(nn):
	v=frappe.db.sql("UPDATE `tabMaterial Request` SET docstatus=1,workflow_state='Approved' WHERE name='"+str(nn)+"' ")
	return v

# @frappe.whitelist()
# def check_reating_items(name):
# 	for i in frappe.db.sql("SELECT count(name)as name,GROUP_CONCAT(distinct(idx))as row from `tabMaterial Request Item` WHERE parent='"+str(name)+"' and creation>'2022-12-03 08:22:17.489923' GROUP BY item_code ",as_dict=1):
# 		if(i.name>1):
# 			frappe.throw("Same Items are Repeating "+str(i.row)+".Club them or Kindly use Pre MR")
@frappe.whitelist()
def filter_and_update(ar,parent):
	to_python = json.loads(ar)
	create_row=[]

	for i in to_python:
		rr=i["remarks"]
		dn=i["drawing_no"]
		if(i["row_name"]!="Added New"):
			frappe.db.sql("UPDATE `tabMaterial Request Item` SET item_code='"+str(i["item_code"])+"',qty='"+str(i["qty"])+"',uom='"+str(i["uom"])+"',remarks='"+str(rr)+"',drawing_no='"+str(dn)+"',edited=1,corrected_from='"+str(i["name"])+"' WHERE name='"+str(i["row_name"])+"' and parent='"+str(parent)+"' ",as_dict=1)
			frappe.db.sql("UPDATE `tabFilter Items` SET item_code='"+str(i["item_code"])+"',qty='"+str(i["qty"])+"',uom='"+str(i["uom"])+"',remarks='"+str(rr)+"',drawing_no='"+str(dn)+"' WHERE name='"+str(i["name"])+"' and parent='"+str(parent)+"' ",as_dict=1)
		elif(frappe.db.sql("SELECT name from `tabMaterial Request Item` where corrected_from='"+str(i["name"])+"' ",as_dict=1)):
			frappe.db.sql("UPDATE `tabMaterial Request Item` SET item_code='"+str(i["item_code"])+"',qty='"+str(i["qty"])+"',uom='"+str(i["uom"])+"',remarks='"+str(rr)+"',drawing_no='"+str(dn)+"',edited=1,corrected_from='"+str(i["name"])+"' WHERE corrected_from='"+str(i["name"])+"' and parent='"+str(parent)+"' ",as_dict=1)

		else:

			create_row.append({
				"edit_row":i["name"],
				"item_code":i["item_code"],
				"qty":i["qty"],
				"uom":i["uom"],				
				"remarks":rr,
				"drawing_no":dn
				})




	doc=frappe.get_doc("Material Request",parent)
	for j in create_row:
		# frappe.msgprint(str(rem))
		if(frappe.db.sql("SELECT name from `tabMaterial Request Item` where corrected_from='"+str(j["edit_row"])+"' ",as_dict=1)):
			frappe.db.sql("UPDATE `tabMaterial Request Item` SET qty='"+str(j["qty"])+"',uom='"+str(j["uom"])+"',remarks='"+str(j["remarks"])+"',drawing_no='"+str(j["drawing_no"])+"' WHERE corrected_from='"+str(j["edit_row"])+"' and parent='"+str(parent)+"' ")
		else:
			doc.append("items",{
				"item_code":j["item_code"],
				"qty":j["qty"],
				"uom":j["uom"],
				"remarks":j["remarks"],
				"drawing_no":j["drawing_no"],
				"edited":1,
				"warehouse":doc.set_warehouse,
				"project":doc.project,
				"corrected_from":j["edit_row"]
				})
	doc.save()
	doc.reload()
	frappe.msgprint("Updated, Refresh and Verify")
	return to_python

@frappe.whitelist()
def check_multiple_items(name):
	res=[]
	for i in frappe.db.sql("SELECT count(item_code)as item_code,item_code as item,GROUP_CONCAT(distinct(idx))as row from `tabMaterial Request Item` WHERE parent='"+str(name)+"' and creation>'2022-12-03 08:22:17.489923' GROUP BY item_code ",as_dict=1):
		if(i.item_code>1):
			res.append(i.item+" i repeating in "+i.row)
	
	if(len(res)>=1):
		frappe.throw(str(res))

	return res