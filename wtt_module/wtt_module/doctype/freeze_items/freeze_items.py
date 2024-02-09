# Copyright (c) 2022, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FreezeItems(Document):
	def on_submit(self):
		for i in self.items:
			o_qt=frappe.db.get_value("Material Request Item",str(i.mr_ref),"ordered_qty")
			r_qt=frappe.db.get_value("Material Request Item",str(i.mr_ref),"received_qty")
			f_qt=frappe.db.get_value("Material Request Item",str(i.mr_ref),"freeze_qty")
			frappe.db.sql("UPDATE `tabMaterial Request Item` SET freeze=1,freeze_qty='"+str(float(f_qt)+float(i.qty))+"',ordered_qty='"+str(float(o_qt)+float(i.qty))+"',received_qty='"+str(float(r_qt)+float(i.qty))+"' WHERE name='"+str(i.mr_ref)+"' and parent='"+str(self.mr)+"' ",as_dict=1)
	def on_cancel(self):
		for i in self.items:
			o_qt=frappe.db.get_value("Material Request Item",str(i.mr_ref),"ordered_qty")
			r_qt=frappe.db.get_value("Material Request Item",str(i.mr_ref),"received_qty")
			f_qt=frappe.db.get_value("Material Request Item",str(i.mr_ref),"freeze_qty")
			frappe.db.sql("UPDATE `tabMaterial Request Item` SET freeze=0,freeze_qty='"+str(float(f_qt)-float(i.qty))+"',ordered_qty='"+str(float(o_qt)-float(i.qty))+"',received_qty='"+str(float(r_qt)-float(i.qty))+"' WHERE name='"+str(i.mr_ref)+"' and parent='"+str(self.mr)+"' ",as_dict=1)

@frappe.whitelist()
def freeze(mr,project):
	ar=[]
	mr_child_po=[]
	for i in frappe.db.sql("SELECT poi.material_request_item FROM `tabPurchase Order`as po,`tabPurchase Order Item`as poi WHERE poi.parent=po.name and poi.material_request='"+str(mr)+"' and po.workflow_state!='Rejected' and po.workflow_state!='Cancelled' ",as_dict=1):
		mr_child_po.append(i.material_request_item)
	for i in frappe.db.sql("SELECT mri.name,mri.item_code,mri.item_name,mri.description,mri.technical_description,mri.qty,mri.uom FROM `tabMaterial Request`as mr,`tabMaterial Request Item`as mri WHERE mri.parent=mr.name and mri.ordered_qty=0 and mri.parent='"+str(mr)+"' and mr.name='"+str(mr)+"' and mri.project='"+str(project)+"' ",as_dict=1):
		if(i.name not in mr_child_po):
			if(i.ordered_qty!=None):
				qq=i.qty-i.ordered_qty
			else:
				qq=i.qty
			ar.append({
				"item_code":i.item_code,
				"item_name":i.item_name,
				"description":i.description,
				"technical_description":i.technical_description,
				"qty":qq,
				"uom":i.uom,
				"mr_ref":i.name
				})
		else:
			query=frappe.db.sql("SELECT sum(poi.qty)as 'qty' FROM `tabPurchase Order`as po,`tabPurchase Order Item`as poi WHERE poi.parent=po.name and po.workflow_state!='Rejected' and po.workflow_state!='Cancelled' and poi.material_request_item='"+str(i.name)+"' GROUP BY poi.material_request_item",as_dict=1)
			qq=float(i.qty)-float(query[0].qty)
			if(qq>0):
				ar.append({
					"item_code":i.item_code,
					"item_name":i.item_name,
					"description":i.description,
					"technical_description":i.technical_description,
					"qty":qq,
					"uom":i.uom,
					"mr_ref":i.name
					})
	return ar
