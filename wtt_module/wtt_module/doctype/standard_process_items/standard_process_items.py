# Copyright (c) 2023, wtt_module and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StandardProcessItems(Document):
	pass


@frappe.whitelist()
def get_qty(st):
	ar=[]
	for i in frappe.db.sql("SELECT * FROM `tabStartup Sheet` WHERE name='"+str(st)+"'",as_dict=1):
		ar.append({
			"mf_for_feed_flow":i.feed_pump,
			"feed_qty":i.feed_qty,
			"mf_for_bw_flow":i.bw_pump,
			"bw_qty":i.bw_qty,
			"flow":i.flow,
			"total_modules":i.total_modules,
			"cip_pump":i.cip_pump,
			"cip_qty":i.cip_qty,
			"range":i.tank_height,
			"no_of_loops":i.no_of_loops,
			"modules_per_loop":i.modules_per_loop,
			"mbr_model":i.mbr_model,
			"design_total_no_of_modules":i.design_total_no_of_modules,
			"is_feed_pump_is_required":i.is_feed_pump_is_required,
			"mbr_feed_pump":i.mbr_feed_pump,
			"feed_pump_qty":i.feed_pump_qty,
			"mbr_backwash_pump":i.mbr_backwash_pump,
			"pump_qty":i.pump_qty,
			"permeate_backwash_store_standby_qty":i.permeate_backwash_store_standby_qty,
			"mbr_sludge_pump":i.mbr_sludge_pump,
			"blower_pump_qty":i.blower_pump_qty,
			"mbr_circulation_pump":i.mbr_circulation_pump,
			"circulation_pump_qty":i.circulation_pump_qty,
			"circulation_pump_store_standby_qty":i.circulation_pump_store_standby_qty,
			"dosing_pump_mc":i.dosing_pump_mc,
			"dosing_pump_rc":i.dosing_pump_rc,
			"citric_dosing_pump_mc_and_rc":i.citric_dosing_pump_mc_and_rc,
			"design_no_of_trains":i.design_no_of_trains,
			"ovivo_no_module_required":i.ovivo_no_module_required,
			"ovivo_no_of_stacks_required":i.ovivo_no_of_stacks_required,
			"ovivo_permeate_pump":i.ovivo_permeate_pump,
			"feed_pump_required_for_ovivo":i.feed_pump_required_for_ovivo
		})
	return ar