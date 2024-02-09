// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('MBR ovivo Standard Items', {
	refresh:function(frm){
		const element = document.querySelector('.btn.btn-xs.btn-default');
		    element.style.background = 'green';
		    element.style.color = 'white';
	},
	validate:function(frm){
		var arr=[]
		$.each(frm.doc.mbr_ovivo_items || [], function(i, v) {
			arr.push({"renamed":v.renamed,"flow":v.flow,"range":v.range,"item_description":v.item_description})	
		});
		frappe.call({
			method:"wtt_module.wtt_module.doctype.mbr_ovivo_standard_items.mbr_ovivo_standard_items.get_mf",
			args:{
				arr:arr
			},
			callback(r){
				
				$.each(frm.doc.mbr_ovivo_items || [], function(i, v) {
					for(var k=0;k<r.message.length;k++)
					{
						if(v.item_description==r.message[k].item_d)
						{
							frappe.model.set_value(v.doctype, v.name, "unit_price", r.message[k].rate)
							frm.refresh_fields("unit_price");
						}
					}
				});
			}
		});
	},
	startup_sheet: function(frm) {
	    var openlink = window.open("https://erp.wttindia.com/app/startup-sheet/"+frm.doc.project_startup_sheet+"","_self");
	},
	not_linked_items:function(frm){
		frm.clear_table("mbr_ovivo_not_linked_items")
		frm.refresh_field("mbr_ovivo_not_linked_items");
		$.each(frm.doc.mbr_ovivo_items || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("mbr_ovivo_not_linked_items");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "req_flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frm.refresh_field("mbr_ovivo_not_linked_items");
			}
		});
	},
	onload:function(frm){
		
		if(frm.doc.mbr_ovivo_items){

		}
		else{
			var mbr_ovivo=["MBR MODULES", "TOP PERMEATE MODULE", "BASE MODULE", "FEED PUMP", "PERMEATE PUMP", "BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SPRINKLER PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3", "SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER","TURBIDITY SENSOR", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "CIP DOSING TANK-1", "CIP DOSING TANK-2", "CIP DOSING TANK-3", "CIP DOSING SKID FRAME", "FAB. & ERECTION"]
			var renamed_ovivo_items=["CERAMIC MBR", "TOP PERMEATE MODULE", "BASE MODULE", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "DOSING PUMP", "DOSING PUMP", "DOSING PUMP", "DOSING PUMP", "TUBE SETTLER MEDIA", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOW METER","TURBIDITY SENSOR", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "TANK", "TANK", "TANK", "CIP DOSING SKID FRAME", "FAB. & ERECTION"]
			console.log(mbr_ovivo.length);
			console.log(renamed_ovivo_items.length);
			for(var i=0;i<mbr_ovivo.length;i++)
			{
				var child = frm.add_child("mbr_ovivo_items");
				frappe.model.set_value(child.doctype, child.name, "item_description", mbr_ovivo[i]);
				frm.refresh_field("mbr_ovivo_items");
				frappe.model.set_value(child.doctype, child.name, "renamed", renamed_ovivo_items[i]);
				frm.refresh_fields("renamed");
			}
		}
		if(frm.doc.mbr_ovivo_electrical_items)
		{

		}
		else
		{
			var mbr_ele=["FEED PUMP", "PERMEATE PUMP", "BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SPRINKLER PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3", "SULPHUR BLACK DOSING PUMP", "PANEL", "PLC"]
			
			var items018=["CIP DOSING PUMP-1","CIP DOSING PUMP-2","SULPHUR BLACK DOSING PUMP"];
			var items037=["PRE-FILTER"];
			for(var i=0;i<mbr_ele.length;i++)
			{
			var child = frm.add_child("mbr_ovivo_electrical_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", mbr_ele[i]);
			frm.refresh_field("mbr_ovivo_electrical_items");
			}
		}		

	},
	project_startup_sheet:function(frm){
		frappe.call({
				method:"wtt_module.wtt_module.doctype.mbr_standard_items.mbr_standard_items.get_qty",
				args:{
					st:frm.doc.project_startup_sheet
				},
				callback(r){
					console.log(r.message[0])			
					$.each(frm.doc.mbr_ovivo_items || [], function(i, v) {
						if(v.item_description=="MBR MODULES")
						{
							frappe.model.set_value(v.doctype,v.name,"flow",1);
							frm.refresh_fields("flow");
							var ovivo_no_module_required=r.message[0].ovivo_no_module_required;
							frappe.model.set_value(v.doctype, v.name, "w_qty", ovivo_no_module_required);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="TOP PERMEATE MODULE"){
							frappe.model.set_value(v.doctype,v.name,"flow",1);
							frm.refresh_fields("flow");
							var ovivo_no_of_stacks_required=r.message[0].ovivo_no_of_stacks_required;
							frappe.model.set_value(v.doctype,v.name,"w_qty",ovivo_no_of_stacks_required);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="BASE MODULE"){
							frappe.model.set_value(v.doctype,v.name,"flow",1);
							frm.refresh_fields("flow");
							var ovivo_no_of_stacks_required=r.message[0].ovivo_no_of_stacks_required;
							frappe.model.set_value(v.doctype,v.name,"w_qty",ovivo_no_of_stacks_required);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="FEED PUMP"){
							if(r.message[0].feed_pump_required_for_ovivo==1){
								var ovivo_permeate_pump=r.message[0].ovivo_permeate_pump;
								frappe.model.set_value(v.doctype,v.name,"flow",ovivo_permeate_pump);
								frm.refresh_fields("flow");
								var ovivo_permeate_qty=r.message[0].ovivo_permeate_qty;
								frappe.model.set_value(v.doctype,v.name,"w_qty",ovivo_permeate_qty);
								frm.refresh_fields("w_qty");
								var ovivo_permeate_sqty=r.message[0].ovivo_permeate_sqty;
								frappe.model.set_value(v.doctype,v.name,"sb_qty",ovivo_permeate_sqty);
								frm.refresh_fields("sb_qty");
							}								
						}
						else if(v.item_description=="PERMEATE PUMP"){
							var ovivo_permeate_pump=r.message[0].ovivo_permeate_pump;
							frappe.model.set_value(v.doctype,v.name,"flow",ovivo_permeate_pump);
							frm.refresh_fields("flow");
							var ovivo_permeate_qty=r.message[0].ovivo_permeate_qty;
							frappe.model.set_value(v.doctype,v.name,"w_qty",ovivo_permeate_qty);
							frm.refresh_fields("w_qty");
							var ovivo_permeate_sqty=r.message[0].ovivo_permeate_sqty;
							frappe.model.set_value(v.doctype,v.name,"sb_qty",ovivo_permeate_sqty);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="BACKWASH PUMP"){
							var ovivo_bc=r.message[0].ovivo_bc;
							frappe.model.set_value(v.doctype,v.name,"flow",ovivo_bc);
							frm.refresh_fields("flow");
							var ovivo_backwash_qty=r.message[0].ovivo_backwash_qty;
							frappe.model.set_value(v.doctype,v.name,"w_qty",ovivo_backwash_qty);
							frm.refresh_fields("w_qty");
							var ovivo_backwash_sqty=r.message[0].ovivo_backwash_sqty;
							frappe.model.set_value(v.doctype,v.name,"sb_qty",ovivo_backwash_sqty);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="CIP PUMP"){
							var ovivo_cip_pump=r.message[0].ovivo_cip_pump;
							frappe.model.set_value(v.doctype,v.name,"flow",ovivo_cip_pump);
							frm.refresh_fields("flow");
							var ovivo_cip_qty=r.message[0].ovivo_cip_qty;
							frappe.model.set_value(v.doctype,v.name,"w_qty",ovivo_cip_qty);
							frm.refresh_fields("w_qty");
							var ovivo_cip_sqty=r.message[0].ovivo_cip_sqty;
							frappe.model.set_value(v.doctype,v.name,"sb_qty",ovivo_cip_sqty);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="SLUDGE EXTRACT PUMP"){
							var ovivo_sludge_pump=r.message[0].ovivo_sludge_pump;
							frappe.model.set_value(v.doctype,v.name,"flow",ovivo_sludge_pump);
							frm.refresh_fields("flow");
							var ovivo_sludge_qty=r.message[0].ovivo_sludge_qty;
							frappe.model.set_value(v.doctype,v.name,"w_qty",ovivo_sludge_qty);
							frm.refresh_fields("w_qty");
							var ovivo_sludge_sqty=r.message[0].ovivo_sludge_sqty;
							frappe.model.set_value(v.doctype,v.name,"sb_qty",ovivo_sludge_sqty);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="SPRINKLER PUMP"){
							var ovivo_sprinkler_pump=r.message[0].ovivo_sprinkler_pump;
							frappe.model.set_value(v.doctype,v.name,"flow",ovivo_sprinkler_pump);
							frm.refresh_fields("flow");
							var ovivo_sprinkler_qty=r.message[0].ovivo_sprinkler_qty;
							frappe.model.set_value(v.doctype,v.name,"w_qty",ovivo_sprinkler_qty);
							frm.refresh_fields("w_qty");
							var ovivo_sprinkler_sqty=r.message[0].ovivo_sprinkler_sqty;
							frappe.model.set_value(v.doctype,v.name,"sb_qty",ovivo_sprinkler_sqty);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="CIP DOSING PUMP-1"){
							var naocl_dosing_pump_rc=r.message[0].naocl_dosing_pump_rc;
							frappe.model.set_value(v.doctype,v.name,"flow",naocl_dosing_pump_rc);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype,v.name,"w_qty",1);
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype,v.name,"sb_qty",1);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="CIP DOSING PUMP-2"){
							var citric_dosing_pump_mc_rc=r.message[0].citric_dosing_pump_mc_rc;
							frappe.model.set_value(v.doctype,v.name,"flow",citric_dosing_pump_mc_rc);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype,v.name,"w_qty",1);
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype,v.name,"sb_qty",1);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="CIP DOSING PUMP-3"){
							var hcl_dosing_pump_mc_rc=r.message[0].hcl_dosing_pump_mc_rc;
							frappe.model.set_value(v.doctype,v.name,"flow",hcl_dosing_pump_mc_rc);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype,v.name,"w_qty",1);
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype,v.name,"sb_qty",1);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="CIP DOSING PUMP-4"){
							var alum_dosing_pump_mc_rc=r.message[0].alum_dosing_pump_mc_rc;
							frappe.model.set_value(v.doctype,v.name,"flow",alum_dosing_pump_mc_rc);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype,v.name,"w_qty",1);
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype,v.name,"sb_qty",1);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="LEVEL TRANSMITTER"){
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frm.refresh_fields("flow");
							var tank_height=r.message[0].tank_height;
							frappe.model.set_value(v.doctype,v.name,"range",tank_height);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype,v.name,"w_qty",r.message[0].ovivo_no_of_trains);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="LEVEL FLOAT"){
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frappe.model.set_value(v.doctype,v.name,"w_qty",2);
							frm.refresh_fields("flow");
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="ELECTROMAGNETIC FLOWMETER"){
							var ovivo_bc=r.message[0].ovivo_bc;
							var rr=r.message[0].ovivo_no_of_trains+r.message[0].ovivo_sprinkler_qty+r.message[0].ovivo_backwash_qty+r.message[0].ovivo_sludge_qty
							frappe.model.set_value(v.doctype,v.name,"flow",ovivo_bc);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype,v.name,"w_qty",rr);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="PRESSURE TRANSMITTER"){
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frm.refresh_fields("flow");
							var rr=r.message[0].ovivo_no_of_trains+r.message[0].ovivo_sprinkler_qty+r.message[0].ovivo_backwash_qty+r.message[0].ovivo_sludge_qty
							frappe.model.set_value(v.doctype,v.name,"range",2);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype,v.name,"w_qty",rr);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="PRESSURE GAUGE"){
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frm.refresh_fields("flow");
							var rr=r.message[0].ovivo_no_of_trains+r.message[0].ovivo_sprinkler_qty+r.message[0].ovivo_backwash_qty+r.message[0].ovivo_sludge_qty
							frappe.model.set_value(v.doctype,v.name,"range",2);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype,v.name,"w_qty",rr);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="CIP DOSING TANK-1"){
							var naocl_dosing_pump_rc=r.message[0].naocl_dosing_pump_rc;
							frappe.model.set_value(v.doctype,v.name,"flow",naocl_dosing_pump_rc*2);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype,v.name,"w_qty",1);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="CIP DOSING TANK-2"){
							var citric_dosing_pump_mc_rc=r.message[0].citric_dosing_pump_mc_rc;
							frappe.model.set_value(v.doctype,v.name,"flow",citric_dosing_pump_mc_rc*2);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype,v.name,"w_qty",1);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="CIP DOSING TANK-3"){
							var hcl_dosing_pump_mc_rc=r.message[0].hcl_dosing_pump_mc_rc;
							frappe.model.set_value(v.doctype,v.name,"flow",hcl_dosing_pump_mc_rc*2);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype,v.name,"w_qty",1);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="CIP DOSING TANK-4"){
							var alum_dosing_pump_mc_rc=r.message[0].alum_dosing_pump_mc_rc;
							frappe.model.set_value(v.doctype,v.name,"flow",alum_dosing_pump_mc_rc*2);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype,v.name,"w_qty",1);
							frm.refresh_fields("w_qty");
						}
						});
					},
			});
	},
	panel:function(frm,cdt,cdn){
		from_panel_calculate_other_plc_qty(frm,cdt,cdn);
		calculate_missed(frm,cdt,cdn);
	}
});
frappe.ui.form.on('MBR - OVIVO Items', {
	flow:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		var ele=["FEED PUMP", "PERMEATE PUMP", "BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SPRINKLER PUMP", "SULPHUR BLACK SLUDGE PUMP"]
		if(child.range!=undefined && ele.includes(child.item_description)){
			update_kw_in_electrical_table(frm,cdt,cdn)
		}
	},
	range:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		var ele=["FEED PUMP", "PERMEATE PUMP", "BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SPRINKLER PUMP", "SULPHUR BLACK SLUDGE PUMP"]
		if(child.range!=undefined && ele.includes(child.item_description)){
			update_kw_in_electrical_table(frm,cdt,cdn)
		}
	},
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		update_wqty_in_child_table2(frm,cdt,cdn);
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		update_sbqty_in_child_table2(frm,cdt,cdn);
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		update_ssbqty_in_child_table2(frm,cdt,cdn);
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
	}
});
frappe.ui.form.on('MBR Ovivo Not Linked Items', {
	w_qty:function(frm,cdt,cdn){
		var child=locals[cdt][cdn];
		child.total_price = (child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price;
		frm.refresh_fields("mbr_ovivo_not_linked_items");
	},
	unit_price:function(frm,cdt,cdn){
		var child=locals[cdt][cdn];
		child.total_price = (child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price;
		frm.refresh_fields("mbr_ovivo_not_linked_items");
	}
});
frappe.ui.form.on('MBR Ovivo Electrical Items', {
	item_description:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		// update_kw(frm,cdt,cdn);
		frappe.model.set_value(cdt, cdn, "type",'');
		frm.refresh_fields("type");
	},
	kw: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		if(child.kw>=0 && child.kw<=5.5)
		{
			frappe.model.set_value(cdt, cdn, "type","DOL FEEDER");
		}
		else
		{
			frappe.model.set_value(cdt, cdn, "type","S/D FEEDER");
		}
		var type_of_item = child.type;
		if(child.vfd_type=="VFD FEEDER")
		{
			type_of_item = "VFD FEEDER"
		}
		frappe.call({
			method:"wtt_module.wtt_module.doctype.mf_standard_items.mf_standard_items.get_elrate",
			args:{
				ic:child.item_description,
				kw:child.kw,
				tty:type_of_item,
				di:frm.doc.digital_input,
				do:frm.doc.digital_output,
				ai:frm.doc.analog_input,
				ao:frm.doc.analog_output,
				ai2:frm.doc.analog_input2
			},
			callback(r){
				frappe.model.set_value(cdt, cdn, "unit_price",r.message);
				frm.refresh_fields("unit_price");
			}
		});
		
	},
	vfd_type:function(frm,cdt, cdn){
		calculate_total_price(frm,cdt,cdn);
		
	},
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		calculate_total_price(frm,cdt,cdn);
	},
	sb_qty: function(frm,cdt, cdn){
		calculate_total_price(frm,cdt,cdn);
	},
	ssb_qty: function(frm,cdt, cdn){
		calculate_total_price(frm,cdt,cdn);
	},
	unit_price: function(frm,cdt, cdn){
		calculate_total_price(frm,cdt,cdn);
	}

});
var update_kw_in_electrical_table = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.mbr_ovivo_electrical_items || [],function(i,v){
		if(v.item_description==child.item_description){
			var theoritical_power = (child.flow/3600)*(child.range*10*10*10*10*10)/1000
			var pump_shaft_power = (theoritical_power/70)*100
			var absorbed_motor_power = (pump_shaft_power/90)*100
			var kw = 0;
			if(absorbed_motor_power<=0.045){kw=0.045}
			else if(absorbed_motor_power<=0.18){kw=0.18}
			else if(absorbed_motor_power<=0.37){kw=0.37}
			else if(absorbed_motor_power<=0.55){kw=0.55}
			else if(absorbed_motor_power<=0.75){kw=0.75}
			else if(absorbed_motor_power<=1.1){kw=1.1}
			else if(absorbed_motor_power<=1.5){kw=1.5}
			else if(absorbed_motor_power<=2.2){kw=2.2}
			else if(absorbed_motor_power<=3.7){kw=3.7}
			else if(absorbed_motor_power<=4){kw=4}
			else if(absorbed_motor_power<=5.5){kw=5.5}
			else if(absorbed_motor_power<=7.5){kw=7.5}
			else if(absorbed_motor_power<=11){kw=11}
			else if(absorbed_motor_power<=15){kw=15}
			else if(absorbed_motor_power<=18.5){kw=18.5}
			else if(absorbed_motor_power<=22){kw=22}
			else if(absorbed_motor_power<=30){kw=30}
			else if(absorbed_motor_power<=37){kw=37}
			else if(absorbed_motor_power<=45){kw=45}
			else if(absorbed_motor_power<=55){kw=55}
			else if(absorbed_motor_power<=75){kw=75}
			else if(absorbed_motor_power<=90){kw=90}
			frappe.model.set_value(v.doctype,v.name,"kw",kw);
			frm.refresh_fields("kw");
		}
	})
}
var calculate_missed = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	var non_vfd_tot = 0;
	var	vfd_tot = 0;
	var	wire2_tot = 0;
	var	wire4_tot = 0;
	var	level_float_tot = 0;
	var non_vfd=["FEED PUMP","PERMEATE PUMP", "BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SPRINKLER PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1","CIP DOSING PUMP-2","CIP DOSING PUMP-3","SULPHUR BLACK DOSING PUMP"];
	var vfd=["BACKWASH/CIP PUMP","SPRINKLER PUMP"];
	var wire2=["LEVEL TRANSMITTER", "PRESSURE TRANSMITTER"];
	var wire4=["ELECTROMAGNETIC FLOWMETER", "TURBIDITY SENSOR"];
	var level_float=["LEVEL FLOAT"];
	$.each(frm.doc.mbr_ovivo_items || [],function(i,v){
		if(non_vfd.includes(v.item_description)){
			if(vfd.includes(v.item_description)){
				non_vfd_tot = non_vfd_tot+v.sb_qty+v.ssb_qty	
			}
			else{
				non_vfd_tot = non_vfd_tot+v.w_qty+v.sb_qty+v.ssb_qty
			}
		}
		if(vfd.includes(v.item_description)){
			vfd_tot = vfd_tot+v.w_qty;
			
		}
		if(wire2.includes(v.item_description)){
			wire2_tot = wire2_tot+v.w_qty+v.sb_qty+v.ssb_qty;	
		}
		if(wire4.includes(v.w_qty)){
			wire4_tot = wire4_tot+v.w_qty+v.sb_qty+v.ssb_qty;	
		}
		if(level_float.includes(v.item_description)){
			level_float_tot = level_float_tot+v.w_qty+v.sb_qty+v.ssb_qty;	
		}
	})
	frm.set_value("digital_input",(non_vfd_tot+vfd_tot)*3+level_float_tot+10);
	frm.refresh_fields("digital_input");
	frm.set_value("digital_output",non_vfd_tot+vfd_tot+5);
	frm.refresh_fields("digital_output");
	frm.set_value("analog_input2",(vfd_tot*2)+wire2_tot);
	frm.refresh_fields("analog_input2");
	frm.set_value("analog_input",wire4_tot);
	frm.refresh_fields("analog_input");
	frm.set_value("analog_output",vfd_tot);
	frm.refresh_fields("analog_output");
}
var calculate_total_price = function(frm,cdt,cdn){
	var panel=["PANEL","PLC"];
	var child = locals[cdt][cdn];
	var wq = child.w_qty;
	var sbq = child.sb_qty;
	var ssbq = child.ssb_qty;
	if(child.w_qty==undefined){wq=0}
	if(child.sb_qty==undefined){sbq=0}
	if(child.ssb_qty==undefined){ssbq=0}
	var type_of_item = child.type
	if(child.vfd_type=="VFD FEEDER"){
		type_of_item = "VFD FEEDER"
	}

	if(panel.includes(child.item_description)){
		var tot2 = ((wq+sbq+ssbq)*child.unit_price)
		frappe.model.set_value(cdt, cdn, "type",'');
		frm.refresh_fields("type");
		frappe.model.set_value(cdt, cdn, "total_price",tot2);
		frm.refresh_fields("total_price");
	}
	else{
		frappe.call({
			method:"wtt_module.wtt_module.doctype.mf_standard_items.mf_standard_items.get_elrate",
			args:{
				ic:child.item_description,
				kw:child.kw,
				tty:type_of_item,
				di:frm.doc.digital_input,
				do:frm.doc.digital_output,
				ai:frm.doc.analog_input,
				ao:frm.doc.analog_output,
				ai2:frm.doc.analog_input2
			},
			callback(r){
				frappe.model.set_value(cdt, cdn, "unit_price",r.message);
				frm.refresh_fields("unit_price");
				var tot1 = wq*r.message
				frappe.call({
					method:"wtt_module.wtt_module.doctype.mf_standard_items.mf_standard_items.get_elrate",
					args:{
						ic:child.item_description,
						kw:child.kw,
						tty:child.type,
						di:frm.doc.digital_input,
						do:frm.doc.digital_output,
						ai:frm.doc.analog_input,
						ao:frm.doc.analog_output,
						ai2:frm.doc.analog_input2
					},
					callback(r){
						var tot2 = tot1+((sbq+ssbq)*r.message)
						frappe.model.set_value(cdt, cdn, "total_price",tot2);
						frm.refresh_fields("total_price");
					}
				});
			}
		});
	}
}
var update_wqty_in_child_table2 = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.mbr_ovivo_electrical_items || [], function(i, v) {
		if(v.item_description==child.item_description)
		{
			frappe.model.set_value(v.doctype, v.name, "w_qty", child.w_qty)
			frm.refresh_fields("w_qty");
		}
	})
}
var update_sbqty_in_child_table2 = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.mbr_ovivo_electrical_items || [],function(i,v){
		if(v.item_description==child.item_description){
			frappe.model.set_value(v.doctype,v.name,"sb_qty",child.sb_qty);
			frm.refresh_fields("sb_qty");
		}
	})
}
var update_ssbqty_in_child_table2 = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.mbr_ovivo_electrical_items || [],function(i,v){
		if(v.item_description==child.item_description){
			frappe.model.set_value(v.doctype,v.name,"ssb_qty",child.ssb_qty);
			frm.refresh_fields("ssb_qty");
		}
	})
}
var from_panel_calculate_other_plc_qty = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.mbr_ovivo_electrical_items || [],function(i,v){
		if(v.item_description=="PANEL"){
			frappe.model.set_value(v.doctype,v.name,"w_qty",frm.doc.panel);
			frm.refresh_fields("w_qty");
		}
		if(v.item_description=="PLC"){
			frappe.model.set_value(v.doctype,v.name, "w_qty",1);
			frm.refresh_fields("w_qty");
		}
	})
}
var update_kw = function (frm,cdt,cdn) {
	var child = locals[cdt][cdn];
	var items018=["CIP DOSING PUMP-1","CIP DOSING PUMP-2","SULPHUR BLACK DOSING PUMP"];
	var items037=["PRE-FILTER"];
	var panel_items=["PLC","PANEL"];
	if(items018.includes(child.item_description)){
		frappe.model.set_value(cdt, cdn, "kw",0.18);
		frm.refresh_fields("kw");
	}
	else if(items037.includes(child.item_description)){
		frappe.model.set_value(cdt, cdn, "kw",0.37);
		frm.refresh_fields("kw");
	}
	else if(panel_items.includes(child.item_description)){
		frappe.model.set_value(cdt, cdn, "kw",0);
		frm.refresh_fields("kw");
		frappe.model.set_value(cdt, cdn, "type",'');
		frm.refresh_fields("type");
	}
	else{
		frappe.model.set_value(cdt, cdn, "kw",0);
		frm.refresh_fields("kw");
	}
}
