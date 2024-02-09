# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DowngradeMR(Document):
	def on_submit(self):
		arr=[]
		doc = frappe.get_doc("Material Request",self.mr)
		frappe.get_meta("Material Request").get_field("request_purpose").allow_on_submit = 1
		frappe.get_meta("Material Request").get_field("items").allow_on_submit = 1
		frappe.get_meta("Material Request Item").get_field("item_code").allow_on_submit = 1
		frappe.get_meta("Material Request Item").get_field("description").allow_on_submit = 1
		frappe.get_meta("Material Request Item").get_field("technical_description").allow_on_submit = 1
		frappe.get_meta("Material Request Item").get_field("qty").allow_on_submit = 1
		frappe.get_meta("Material Request Item").get_field("uom").allow_on_submit = 1
		frappe.get_meta("Material Request Item").get_field("stock_uom").allow_on_submit = 1
		frappe.get_meta("Material Request Item").get_field("project").allow_on_submit = 1
		frappe.get_meta("Material Request Item").get_field("conversion_factor").allow_on_submit = 1
		frappe.get_meta("Material Request Item").get_field("ordered_qty").allow_on_submit = 1
		frappe.get_meta("Material Request Item").get_field("actual_qty").allow_on_submit = 1
		for i in self.items:
			if(i.mr_ref):
				for dd in doc.items:
					if(i.mr_ref == dd.name):
						if(dd.qty == i.qty):
							pass
						else:
							dd.qty = i.qty
			else:
				doc.append('items',{
					"item_code":i.item_code,
					"description":i.description,
					"technical_description":i.technical_description,
					"qty":i.qty,
					"stock_qty":i.qty,
					"uom":i.uom,
					"stock_uom":i.uom,
					"project":i.project,
					"conversion_factor":1,
					"actual_qty":i.qty,
					"ordered_qty":0
				})

		for deleted_item in self.deleted_items:
			for item in doc.items:
				if item.name == deleted_item.mr_ref:
					doc.remove(item)
					
		for index, item in enumerate(doc.items):
			item.idx = index + 1
		doc.save()

@frappe.whitelist()
def get_mr(mr):
	arr=[]
	for i in frappe.db.sql("SELECT * FROM `tabMaterial Request Item` WHERE parent='"+str(mr)+"' ORDER BY idx ASC",as_dict=1):
		qq = frappe.db.sql("SELECT * FROM `tabPurchase Order Item` as poi INNER JOIN `tabPurchase Order` as po ON po.name=poi.parent WHERE po.workflow_state!='Rejected' AND po.workflow_state!='Cancelled' AND poi.material_request_item='"+str(i.name)+"'",as_dict=1)
		if(qq):
			pass
		else:
			arr.append({
				"item_code":i.item_code,
				"description":i.description,
				"technical_description":i.technical_description,
				"qty":i.qty,
				"uom":i.uom,
				"project":i.project,
				"mr_ref":i.name,
				"drawing_no":i.drawing_no,
				"remarks":i.remarks,
				"mr_row":i.idx
			})
	return arr
