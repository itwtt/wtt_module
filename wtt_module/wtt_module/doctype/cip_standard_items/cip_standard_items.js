// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('CIP Standard Items', {
	onload:function(frm)
	{
		if(frm.doc.cip_items)
		{

		}
		else
		{
			var cip = ["CIP PUMP-1", "CIP PUMP-2", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "ELECTROMAGNETIC FLOW METER - CIP-1", "ELECTROMAGNETIC FLOWMETER - CIP-2", "PRESSURE TRANSMITTER - CIP-1 - IN & OUT", "PRESSURE TRANSMITTER - CIP-2 - IN & OUT", "PRESSURE GAUGE - CIP-1", "PRESSURE GAUGE - CIP-2", "pH SENSOR - CIP-1", "pH SENSOR - CIP-2", "CIP-1 PRE-FILTER", "CIP-2 PRE-FILTER", "CIP DOSING TANK-1", "CIP DOSING TANK-2", "CIP-1 TANK", "CIP-2 TANK", "CIP DOSING PUMP-1 FRAME", "CIP DOSING PUMP-2 FRAME", "CIP DOSING TANK-1 FRAME", "CIP DOSING TANK-2 FRAME", "CIP-1 TANK FRAME", "CIP-2 TANK FRAME"]
			var cip_renamed = ["SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "DOSING PUMP", "DOSING PUMP", "ELECTROMAGNETIC FLOWMETER", "ELECTROMAGNETIC FLOWMETER", "PRESSURE TRANSMITTER", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "PRESSURE GAUGE", "PH SENSOR", "PH SENSOR", "BAG FILTER", "BAG FILTER", "TANK", "TANK", "TANK", "TANK", "FRAME", "FRAME", "FRAME", "FRAME", "FRAME", "FRAME"]
			
			for(var i=0;i<cip.length;i++)
			{
			var child = frm.add_child("cip_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", cip[i]);
			frappe.model.set_value(child.doctype, child.name, "renamed", cip_renamed[i]);
			frm.refresh_field("cip_items");
			}
		}
		if(frm.doc.cip_electrical_items)
		{

		}
		else
		{
			var cip_electrical=["CIP PUMP-1", "CIP PUMP-2", "HCL DOSING", "CAUSTIC DOSING", "PANEL", "PLC" ]
			
			for(var i=0;i<cip_electrical.length;i++)
			{
				var child = frm.add_child("cip_electrical_items");
				frappe.model.set_value(child.doctype, child.name, "item_description", cip_electrical[i]);
				frm.refresh_field("cip_electrical_items");
			}
		}
	},
	get_data:function(frm)
	{
		$.each(frm.doc.cip_items || [], function(i, v) {
			if(v.item_description=='FEED PUMP')
			{
				frappe.model.set_value(v.doctype, v.name, "w_qty",1)
				frm.refresh_fields("w_qty");
				frappe.model.set_value(v.doctype, v.name, "sb_qty",1)
				frm.refresh_fields("sb_qty");
				frappe.model.set_value(v.doctype, v.name, "range",5)
				frm.refresh_fields("range");
			}
			else if(v.item_description == "ELECTROMAGNETIC FLOWMETER - CIP-2" || v.item_description=='HIGH PRESSURE PUMP'|| v.item_description=='RO DOSING PUMP -1' || v.item_description=='RO DOSING PUMP -2' || v.item_description=='RO DOSING PUMP -3'|| v.item_description=='BOOSTER PUMP-1' || v.item_description=='BOOSTER PUMP-2' || v.item_description=='BOOSTER PUMP-3' || v.item_description=='pH SENSOR' || v.item_description=='pH SENSOR - CIP-2')
			{
				frappe.model.set_value(v.doctype, v.name, "w_qty",1)
				frm.refresh_fields("w_qty");
			}
			else if(v.item_description=='ELECTROMAGNETIC FLOWMETER - FEED' || v.item_description=='ELECTROMAGNETIC FLOW METER - PERMEATE - STAGE 1' || v.item_description=='ELECTROMAGNETIC FLOW METER - PERMEATE - STAGE 2' || v.item_description=='ELECTROMAGNETIC FLOW METER - PERMEATE - STAGE 3' || v.item_description=='ELECTROMAGNETIC FLOW METER - PERMEATE - STAGE 4' || v.item_description=='ELECTROMAGNETIC FLOW METER - CIP-1' || v.item_description=='ELECTROMAGNETIC FLOW METER - CIP-2' || v.item_description=='PRESSURE TRANSMITTER - CIP-1 - IN & OUT' || v.item_description=='PRESSURE TRANSMITTER - CIP-2 - IN & OUT' || v.item_description=='RO PRE-FILTER' || v.item_description=='CIP-1 PRE-FILTER' || v.item_description=='CIP-2 PRE-FILTER' || v.item_description=='RO DOSING TANK-1' || v.item_description=='RO DOSING TANK-2' || v.item_description=='RO DOSING TANK-3'|| v.item_description=='CIP DOSING TANK-1' || v.item_description=='CIP DOSING TANK-2' || v.item_description=='CIP-1 TANK' || v.item_description=='CIP-2 TANK')
			{
				frappe.model.set_value(v.doctype, v.name, "w_qty",1)
				frm.refresh_fields("w_qty");
			}
			else if(v.item_description=='LEVEL TRANSMITTER'|| v.item_description=='LEVEL FLOAT' || v.item_description=='CIP DOSING PUMP-1' || v.item_description=='CIP DOSING PUMP-2'||v.item_description=='PRESSURE TRANSMITTER - PRE-FILTER IN & OUT' || v.item_description=='PRESSURE TRANSMITTER - STAGE 1 - IN & OUT' || v.item_description=='PRESSURE TRANSMITTER - STAGE 2 - IN & OUT' || v.item_description=='PRESSURE TRANSMITTER - STAGE 3 - IN & OUT' || v.item_description=='PRESSURE TRANSMITTER - STAGE 4 - IN & OUT' || v.item_description=='PRESSURE GAUGE - PRE-FILTER - IN & OUT' || v.item_description=='PRESSURE GAUGE - STAGE 1 - IN & OUT' || v.item_description=='PRESSURE GAUGE - STAGE 2 - IN & OUT' || v.item_description=='PRESSURE GAUGE - STAGE 3 - IN & OUT' || v.item_description=='PRESSURE GAUGE - STAGE 4 - IN & OUT' || v.item_description=='PRESSURE GAUGE - CIP-1' || v.item_description=='PRESSURE GAUGE - CIP-2')
			{
				frappe.model.set_value(v.doctype, v.name, "w_qty",2)
				frm.refresh_fields("w_qty");
			}
			else if(v.item_description=='RO DOSING PUMP -1')
			{
				frappe.model.set_value(v.doctype, v.name, "ssb_qty",1)
				frm.refresh_fields("ssb_qty");
			}
			else if(v.item_description=='CIP PUMP-1' || v.item_description=='CIP PUMP-2')
			{
				frappe.model.set_value(v.doctype, v.name, "range",4)
				frm.refresh_fields("range");
			}
		});
	},
	qty_update:function(frm,cdt,cdn) {
		var child = locals[cdt][cdn];
		var ele = ["CIP PUMP-1", "CIP PUMP-2", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "PANEL", "PLC" ]
		$.each(frm.doc.cip_items || [], function(i, v) {
			if(ele.includes(v.item_description)){
				$.each(frm.doc.cip_electrical_items || [], function(i, vv) {
					if(v.item_description==vv.item_description)
					{
						frappe.model.set_value(vv.doctype, vv.name, "w_qty", v.w_qty)
						frm.refresh_fields("w_qty");
						frappe.model.set_value(vv.doctype, vv.name, "sb_qty", v.sb_qty)
						frm.refresh_fields("sb_qty");
						frappe.model.set_value(vv.doctype, vv.name, "ssb_qty", v.ssb_qty)
						frm.refresh_fields("ssb_qty");
					}
				})
			}
				
		})	
	},
	get_not_linked:function(frm)
	{
		frm.clear_table("not_linked_items")
		frm.refresh_field("not_linked_items");
		$.each(frm.doc.cip_items || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("not_linked_items");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "model_no", v.model_no);
				frappe.model.set_value(child.doctype, child.name, "fluid_passed", v.fluid_passed);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frm.refresh_field("not_linked_items");
			}
		});
	},
	panel:function(frm,cdt,cdn){
		from_panel_calculate_other_plc_qty(frm,cdt,cdn);
		calculate_missed(frm,cdt,cdn);
	},
});
frappe.ui.form.on('RO Items', {
	flow:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		var ele=["FEED PUMP", "CIP PUMP-1", "CIP PUMP-2", "HIGH PRESSURE PUMP", "BOOSTER PUMP-1", "BOOSTER PUMP-2", "BOOSTER PUMP-3", "SMBS", "ANTISCALANT"]
		if(child.range!=undefined && ele.includes(child.item_description)){
			update_kw_in_electrical_table(frm,cdt,cdn)
		}
	},
	range:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		var ele=["FEED PUMP", "CIP PUMP-1", "CIP PUMP-2", "HIGH PRESSURE PUMP", "BOOSTER PUMP-1", "BOOSTER PUMP-2", "BOOSTER PUMP-3", "SMBS", "ANTISCALANT"]
		if(child.range!=undefined && ele.includes(child.item_description)){
			update_kw_in_electrical_table(frm,cdt,cdn)
		}
		if(child.item_description == 'PRESSURE VESSEL')
		{
			var vvs = Math.ceil((child.range * 14.5038) / 10) * 10
			frappe.model.set_value(cdt, cdn, "model_no", vvs);
			refresh_field("model_no");
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
frappe.ui.form.on('RO Not Linked Items', {
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
frappe.ui.form.on('RO Electrical Items', {
	item_description:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		// update_kw(frm,cdt,cdn);
		frappe.model.set_value(cdt, cdn, "type",'');
		frm.refresh_fields("type");
	},
	kw: function(frm,cdt, cdn){
		if(frm.doc.digital_input==undefined){
			msgprint("kindly choose the panel quantity needed")
		}
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
		if(frm.doc.digital_input==undefined || frm.doc.digital_output==undefined || frm.doc.analog_input2==undefined || frm.doc.analog_input==undefined || frm.doc.analog_output==undefined){
			msgprint("Choose panel qty")
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
	$.each(frm.doc.cip_electrical_items || [],function(i,v){
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
	$.each(frm.doc.cip_electrical_items || [], function(i, v) {
		if(v.item_description==child.item_description)
		{
			frappe.model.set_value(v.doctype, v.name, "w_qty", child.w_qty)
			frm.refresh_fields("w_qty");
		}
	})
}
var update_sbqty_in_child_table2 = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.cip_electrical_items || [],function(i,v){
		if(v.item_description==child.item_description){
			frappe.model.set_value(v.doctype,v.name,"sb_qty",child.sb_qty);
			frm.refresh_fields("sb_qty");
		}
	})
}
var update_ssbqty_in_child_table2 = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.cip_electrical_items || [],function(i,v){
		if(v.item_description==child.item_description){
			frappe.model.set_value(v.doctype,v.name,"ssb_qty",child.ssb_qty);
			frm.refresh_fields("ssb_qty");
		}
	})
}
var from_panel_calculate_other_plc_qty = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.cip_electrical_items || [],function(i,v){
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
var calculate_missed = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	var non_vfd_tot = 0;
	var	vfd_tot = 0;
	var	wire2_tot = 0;
	var	wire4_tot = 0;
	var	level_float_tot = 0;
	var non_vfd=["LIFTING SUMP PUMP", "EQT BLOWER", "EQUALIZATION FLOW MAKER", "DAF BUBBLE GENERATION PUMP","DAF SLUDGE PUMP","NEUTRALIZATION PUMP","NT DOSING PUMP","DENITRIFICATION FLOW MIXER","DENITRIFICATION PUMP","BIO BLOWER","BIOLOGICAL FLOW MAKER"];
	var vfd=["BIO BLOWER"];
	var wire2=["LEVEL TRANSMITTER"];
	var wire4=["ELECTROMAGNETIC FLOWMETER", "pH SENSOR","DO SENSOR"];
	var level_float=["LEVEL FLOAT"];
	$.each(frm.doc.cip_items || [],function(i,v){
		if(non_vfd.includes(v.item_description)){
			if(v.item_description=="BIO BLOWER"){
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
	frm.set_value("digital_input",(non_vfd_tot+vfd_tot)*3+level_float_tot+10+28);// 28 for pneumatic valve, 10 for EMG, CON ON,ACK,RST,MBR CYCLE ST/SP, RO CY ST/SP,MBR A/M,ETP A/M
	frm.refresh_fields("digital_input");
	frm.set_value("digital_output",non_vfd_tot+vfd_tot+5+28+1);// 28 for pneumatic valve, 1 for electro valve, 5 for INDIACTION ,ALARM,HOOTER
	frm.refresh_fields("digital_output");
	frm.set_value("analog_input2",(vfd_tot*2)+wire2_tot);
	frm.refresh_fields("analog_input2");
	frm.set_value("analog_input",wire4_tot);
	frm.refresh_fields("analog_input");
	frm.set_value("analog_output",vfd_tot);
	frm.refresh_fields("analog_output");
}
