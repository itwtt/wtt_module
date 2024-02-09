// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Standard Process Items', {
	validate:function(frm)
	{
		var total_amount=0;
		$.each(frm.doc.mf_items, function (i,d) {
			total_amount+=d.total_price;
		});
		frm.set_value("mf_cost",total_amount);
		frm.refresh_fields("mf_cost");

		var total_amount=0;
		$.each(frm.doc.mbr_koch_items, function (i,d) {
			total_amount+=d.total_price;
		});
		frm.set_value("mbr_koch_cost",total_amount);
		frm.refresh_fields("mbr_koch_cost");

		var total_amount=0;
		$.each(frm.doc.mbr_ovivo_items, function (i,d) {
			total_amount+=d.total_price;
		});
		frm.set_value("mbr_ovivo_cost",total_amount);
		frm.refresh_fields("mbr_ovivo_cost");
	},
	onload:function(frm)
	{
		if(frm.doc.mf_items)
		{

		}
		else
		{
			var mf=["PRE-FILTER", "MODULES", "FEED PUMP", "BACKWASH PUMP", "FEED/BACKWASH PUMP", "CIP PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3", "SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "PH SENSOR", "CIP PRE-FILTER", "CIP TANK", "CIP DOSING TANK-1", "CIP DOSING TANK-2", "CIP DOSING TANK-3", "MF SKID FRAME", "CIP SKID FRAME", "CIP DOSING SKID FRAME", "PIPES,FITTINGS & VALVES", "FAB. & ERECTION"]
			for(var i=0;i<mf.length;i++)
			{
			var child = frm.add_child("mf_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", mf[i]);
			frm.refresh_field("mf_items");
			}
		}

		if(frm.doc.mbr_koch_items)
		{

		}
		else
		{
			var mbr=["MBR MODULES", "FEED PUMP", "PERMEATE PUMP", "BACKWASH PUMP", "CIP PUMP", "PERMEATE/BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3", "SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "CIP PRE-FILTER", "CIP TANK", "CIP DOSING TANK-1", "CIP DOSING TANK-2", "MBR SKID FRAME", "CIP SKID FRAME", "CIP DOSING SKID FRAME", "PIPES,FITTINGS & VALVES", "FAB. & ERECTION"]
			for(var i=0;i<mbr.length;i++)
			{
			var child = frm.add_child("mbr_koch_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", mbr[i]);
			frm.refresh_field("mbr_koch_items");
			}
		}

		if(frm.doc.mbr_ovivo_items)
		{

		}
		else
		{
			var mbr_ovivo=["MBR MODULES", "TOP PERMEATE MODULE", "BASE MODULE", "FEED PUMP", "PERMEATE PUMP", "BACKWASH PUMP", "CIP PUMP", "PERMEATE/BACKWASH/CIP PUMP", "BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SPRINKLER PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3", "SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "CIP PRE-FILTER", "CIP TANK", "CIP DOSING TANK-1", "CIP DOSING TANK-2", "MBR SKID FRAME", "CIP SKID FRAME", "CIP DOSING SKID FRAME", "PIPES,FITTINGS & VALVES", "FAB. & ERECTION"]
			for(var i=0;i<mbr_ovivo.length;i++)
			{
			var child = frm.add_child("mbr_ovivo_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", mbr_ovivo[i]);
			frm.refresh_field("mbr_ovivo_items");
			}
		}

		if(frm.doc.ro_items)
		{

		}
		else
		{
			var ro=["MEMBRANE", "PRESSURE VESSEL", "FEED PUMP", "CIP PUMP-1", "CIP PUMP-2", "HIGH PRESSURE PUMP", "BOOSTER PUMP-1", "BOOSTER PUMP-2", "BOOSTER PUMP-3", "DOSING PUMP-1", "DOSING PUMP-2", "DOSING PUMP-3", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "PH SENSOR", "RO PRE-FILTER", "CIP-1 PRE-FILTER", "CIP-2 PRE-FILTER", "CIP-1 TANK", "CIP-2 TANK", "CIP DOSING TANK-1", "CIP DOSING TANK-2", "RO SKID FRAME", "CIP SKID FRAME", "RO DOSING SKID FRAME", "CIP DOSING SKID FRAME", "PIPES,FITTINGS & VALVES", "FAB. & ERECTION"]
			for(var i=0;i<ro.length;i++)
			{
			var child = frm.add_child("ro_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", ro[i]);
			frm.refresh_field("ro_items");
			}
		}
	},
	project_startup_sheet:function(frm){
		frappe.call({
				method:"wtt_module.wtt_module.doctype.standard_process_items.standard_process_items.get_qty",
				args:{
					st:frm.doc.project_startup_sheet
				},
				callback(r){
					$.each(frm.doc.mf_items || [], function(i, v) {
					if(v.item_description=="FEED PUMP")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", r.message[0].mf_for_feed_flow)
						frappe.model.set_value(v.doctype, v.name, "w_qty", r.message[0].feed_qty)
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="BACKWASH PUMP")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", r.message[0].mf_for_bw_flow)
						frappe.model.set_value(v.doctype, v.name, "w_qty", r.message[0].bw_qty)
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="PRE-FILTER")
					{
						var flowv=((r.message[0].flow)/21)
						var preflow=0;
						var preqty=0;
						if(flowv>0 && flowv<=30)
						{
							preflow=30;
							preqty=1;
						}
						else if(flowv>30 && flowv<=45)
						{
							preflow=45;
							preqty=1;
						}
						else if(flowv>45 && flowv<=90)
						{
							preflow=82;
							preqty=1;
						}
						else if(flowv>90)
						{
							preflow=82;
							preqty=(flowv/82);
							preqty=Math.ceil(preqty / 1) * 1;
						}
						frappe.model.set_value(v.doctype, v.name, "flow", preflow)
						frappe.model.set_value(v.doctype, v.name, "w_qty", preqty);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="MODULES")
					{
						var roundmodule=Math.round(r.message[0].total_modules);
						frappe.model.set_value(v.doctype, v.name, "w_qty", roundmodule);
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="CIP PUMP")
					{
						var cip=r.message[0].cip_pump
						var cipqty=r.message[0].cip_qty
						frappe.model.set_value(v.doctype, v.name, "flow", cip);
						frappe.model.set_value(v.doctype, v.name, "w_qty", cipqty);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="LEVEL TRANSMITTER")
					{
						var range=r.message[0].range
						frappe.model.set_value(v.doctype, v.name, "range", range);
						frm.refresh_fields("range");
					}
					else if(v.item_description=="ELECTROMAGNETIC FLOWMETER")
					{
						var elflow=r.message[0].mf_for_bw_flow;
						var totalelqty=(r.message[0].no_of_loops + r.message[0].cip_qty + r.message[0].bw_qty);
						frappe.model.set_value(v.doctype, v.name, "flow", elflow);
						frappe.model.set_value(v.doctype, v.name, "w_qty", totalelqty);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="CIP PRE-FILTER")
					{
						var preflow=(r.message[0].cip_pump)*1.5;
						var preqty=(r.message[0].flow/5);
						frappe.model.set_value(v.doctype, v.name, "flow", preflow);
						frappe.model.set_value(v.doctype, v.name, "w_qty", preqty);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="CIP TANK")
					{
						var ciptankflow=(r.message[0].modules_per_loop)*80;
						frappe.model.set_value(v.doctype, v.name, "flow", ciptankflow);
						frm.refresh_fields("flow");
					}
				});

				$.each(frm.doc.mbr_koch_items || [], function(i, v) {
					if(v.item_description=="MBR MODULES")
					{
						var mbr_model=r.message[0].mbr_model;
						var design_total_no_of_modules=r.message[0].design_total_no_of_modules;
						frappe.model.set_value(v.doctype, v.name, "flow", mbr_model);
						frappe.model.set_value(v.doctype, v.name, "w_qty", design_total_no_of_modules);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="FEED PUMP")
					{
						if(r.message[0].is_feed_pump_required==1)
						{
							var mbrfeed=(r.message[0].mbr_feed_pump);
						}
						else
						{
							var mbrfeed=0;
						}
						frappe.model.set_value(v.doctype, v.name, "flow", mbrfeed);
						frappe.model.set_value(v.doctype, v.name, "w_qty", r.message[0].feed_pump_qty);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="PERMEATE/BACKWASH/CIP PUMP")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", r.message[0].mbr_backwash_pump);
						frappe.model.set_value(v.doctype, v.name, "w_qty", r.message[0].pump_qty);
						frappe.model.set_value(v.doctype, v.name, "ssb_qty", r.message[0].permeate_backwash_store_standby_qty);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
						frm.refresh_fields("ssb_qty");
					}
					else if(v.item_description=="SLUDGE EXTRACT PUMP")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", r.message[0].mbr_sludge_pump);
						frappe.model.set_value(v.doctype, v.name, "w_qty", r.message[0].blower_pump_qty);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="SLUDGE RECIRCULATION PUMP")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", r.message[0].mbr_circulation_pump);
						frappe.model.set_value(v.doctype, v.name, "w_qty", r.message[0].circulation_pump_qty);
						frappe.model.set_value(v.doctype, v.name, "ssb_qty", r.message[0].circulation_pump_store_standby_qty);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
						frm.refresh_fields("ssb_qty");
					}
					else if(v.item_description=="CIP DOSING PUMP-1")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", r.message[0].dosing_pump_mc);
						frm.refresh_fields("flow");
					}
					else if(v.item_description=="CIP DOSING PUMP-2")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", r.message[0].dosing_pump_rc);
						frm.refresh_fields("flow");
					}
					else if(v.item_description=="CIP DOSING PUMP-3")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", r.message[0].citric_dosing_pump_mc_and_rc);
						frm.refresh_fields("flow");
					}
					else if(v.item_description=="LEVEL TRANSMITTER")
					{
						var range=r.message[0].range
						frappe.model.set_value(v.doctype, v.name, "range", range);
						frm.refresh_fields("range");
					}
					else if(v.item_description=="ELECTROMAGNETIC FLOWMETER")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", r.message[0].mbr_backwash_pump);
						frappe.model.set_value(v.doctype, v.name, "w_qty", r.message[0].design_no_of_trains);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="PRESSURE TRANSMITTER" || v.item_description=="PRESSURE GAUGE")
					{
						frappe.model.set_value(v.doctype, v.name, "range", "0-2");
						frappe.model.set_value(v.doctype, v.name, "w_qty", r.message[0].design_no_of_trains);
						frm.refresh_fields("range");
						frm.refresh_fields("w_qty");
					}
				});	


				$.each(frm.doc.mbr_ovivo_items || [], function(i, v) {
					if(v.item_description=="MBR MODULES")
					{
						var mbr_model=r.message[0].mbr_model;
						var ovio_no_of_module_required=r.message[0].ovio_no_of_module_required;
						frappe.model.set_value(v.doctype, v.name, "flow", mbr_model);
						frappe.model.set_value(v.doctype, v.name, "w_qty", ovivo_no_module_required);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					});
				},
			});
	}
});
frappe.ui.form.on('MF Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	}
});

frappe.ui.form.on('MBR - KOCH Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	}
});

frappe.ui.form.on('MBR - OVIVO Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	}
});