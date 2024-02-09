frappe.ui.form.on('MF Standard Items', {
	refresh:function(frm){
		const element = document.querySelector('.btn.btn-xs.btn-default');
		    element.style.background = 'green';
		    element.style.color = 'white';
	},
	onload:function(frm){
		if(frm.doc.mf_items){

		}
		else{
			var mf=["PRE-FILTER", "MODULES", "FEED PUMP", "BACKWASH PUMP", "FEED/BACKWASH PUMP", "CIP PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "SULPHUR BLACK DOSING PUMP", "SULPHUR BLACK LAMELLA SETTLER", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "PH SENSOR", "CIP PRE-FILTER", "CIP TANK", "CIP DOSING TANK-1", "CIP DOSING TANK-2", "MF SKID FRAME", "CIP SKID FRAME", "CIP DOSING SKID FRAME", "FAB. & ERECTION"]
			var renamed_items=["PRE-FILTER", "MICRO FILTER", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "SURFACE MOUNTED PUMP", "DOSING PUMP", "DOSING PUMP", "DOSING PUMP", "TUBE SETTLER MEDIA", "LEVEL TRANSMITTER", "LEVEL FLOAT", "ELECTROMAGNETIC FLOWMETER", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "PH SENSOR", "BAG FILTER", "TANK", "TANK", "TANK", "MF SKID FRAME", "CIP SKID FRAME", "CIP DOSING SKID FRAME", "FAB. & ERECTION"]
			console.log(mf.length)
			console.log(renamed_items.length)
			for(var i=0;i<mf.length;i++)
			{
			var child = frm.add_child("mf_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", mf[i]);
			frappe.model.set_value(child.doctype, child.name, "renamed", renamed_items[i]);
			frm.refresh_field("mf_items");
			}
		}
		if(frm.doc.mf_electrical_items){

		}
		else{
			var mf_ele=["PRE-FILTER","FEED PUMP", "BACKWASH PUMP", "CIP PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "SULPHUR BLACK DOSING PUMP","PANEL","PLC"]

			for(var i=0;i<mf_ele.length;i++)
			{
			var child = frm.add_child("mf_electrical_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", mf_ele[i]);
			frm.refresh_field("mf_electrical_items");
			}
		}
	},
	startup_sheet: function(frm) {
	    var openlink = window.open("https://erp.wttindia.com/app/startup-sheet/"+frm.doc.project_startup_sheet+"","_self");
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
						frappe.model.set_value(v.doctype, v.name, "flow", 1)
						var roundmodule=Math.round(r.message[0].total_modules);
						frappe.model.set_value(v.doctype, v.name, "w_qty", roundmodule);
						frm.refresh_fields("flow");
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
						frappe.model.set_value(v.doctype, v.name, "flow", 1);
						frappe.model.set_value(v.doctype, v.name, "range", range);
						frm.refresh_fields("flow");
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
					else if(v.item_description=="CIP DOSING PUMP-1" || v.item_description=="CIP DOSING PUMP-2" || v.item_description=="CIP DOSING TANK-1" || v.item_description=="CIP DOSING TANK-2" || v.item_description=="SULPHUR BLACK DOSING PUMP")
					{

						frappe.model.set_value(v.doctype, v.name, "flow", 50);
						frappe.model.set_value(v.doctype, v.name, "w_qty", 1);
						frappe.model.set_value(v.doctype, v.name, "ssb_qty", 1);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
						frm.refresh_fields("ssb_qty");
					}
					else if(v.item_description=="LEVEL FLOAT" || v.item_description=="PRESSURE TRANSMITTER" || v.item_description=="PRESSURE GAUGE" || v.item_description=="PH SENSOR")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", 1);
						frappe.model.set_value(v.doctype, v.name, "w_qty", 1);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
				});
					$.each(frm.doc.mf_electrical_items || [], function(i, v) {
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
					else if(v.item_description=="CIP PUMP")
					{
						var cip=r.message[0].cip_pump
						var cipqty=r.message[0].cip_qty
						frappe.model.set_value(v.doctype, v.name, "flow", cip);
						frappe.model.set_value(v.doctype, v.name, "w_qty", cipqty);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
					}
					else if(v.item_description=="CIP DOSING PUMP-1" || v.item_description=="CIP DOSING PUMP-2" || v.item_description=="CIP DOSING TANK-1" || v.item_description=="CIP DOSING TANK-2" || v.item_description=="SULPHUR BLACK DOSING PUMP")
					{
						frappe.model.set_value(v.doctype, v.name, "flow", 50);
						frappe.model.set_value(v.doctype, v.name, "w_qty", 1);
						frappe.model.set_value(v.doctype, v.name, "ssb_qty", 1);
						frm.refresh_fields("flow");
						frm.refresh_fields("w_qty");
						frm.refresh_fields("ssb_qty");
					}
				});
				}
			});
	},
	not_linked_items:function(frm){
		frm.clear_table("mf_not_linked_items")
		frm.refresh_field("mf_not_linked_items");
		$.each(frm.doc.mf_items || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("mf_not_linked_items");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "req_flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frm.refresh_field("mf_not_linked_items");
			}
		});
	},
	validate:function(frm){
		var arr=[]
		$.each(frm.doc.mf_items || [], function(i, v) {
			arr.push({"renamed":v.renamed,"flow":v.flow,"range":v.range,"item_description":v.item_description})	
		});
		frappe.call({
				method:"wtt_module.wtt_module.doctype.mf_standard_items.mf_standard_items.get_mf",
				args:{
					arr:arr
				},
				callback(r){
					$.each(frm.doc.mf_items || [], function(i, v) {
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

		var total_amount=0;
		$.each(frm.doc.mf_items, function (i,d) {
			total_amount+=d.total_price;
		});
		frm.set_value("mf_cost",total_amount);
		frm.refresh_fields("mf_cost");
	},
	panel:function(frm,cdt,cdn){
		from_panel_calculate_other_plc_qty(frm,cdt,cdn);
		calculate_missed(frm,cdt,cdn);
	}
});
frappe.ui.form.on('MF Items', {
	flow:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		var ele=["FEED PUMP", "BACKWASH PUMP", "CIP PUMP", "SULPHUR BLACK SLUDGE PUMP","PANEL","PLC"];
		if(child.range!=undefined && ele.includes(child.item_description)){
			update_kw_in_electrical_table(frm,cdt,cdn)
		}
	},
	range:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		var ele=["FEED PUMP", "BACKWASH PUMP", "CIP PUMP", "SULPHUR BLACK SLUDGE PUMP","PANEL","PLC"]
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
frappe.ui.form.on('MF Not linked items', {
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

frappe.ui.form.on('MF Electrical Items', {
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
	$.each(frm.doc.mf_electrical_items || [],function(i,v){
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
	$.each(frm.doc.mf_electrical_items || [], function(i, v) {
		if(v.item_description==child.item_description)
		{
			frappe.model.set_value(v.doctype, v.name, "w_qty", child.w_qty)
			frm.refresh_fields("w_qty");
		}
	})
}
var update_sbqty_in_child_table2 = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.mf_electrical_items || [],function(i,v){
		if(v.item_description==child.item_description){
			frappe.model.set_value(v.doctype,v.name,"sb_qty",child.sb_qty);
			frm.refresh_fields("sb_qty");
		}
	})
}
var update_ssbqty_in_child_table2 = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.mf_electrical_items || [],function(i,v){
		if(v.item_description==child.item_description){
			frappe.model.set_value(v.doctype,v.name,"ssb_qty",child.ssb_qty);
			frm.refresh_fields("ssb_qty");
		}
	})
}
var from_panel_calculate_other_plc_qty = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.mf_electrical_items || [],function(i,v){
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
	var non_vfd=["FEED PUMP", "BACKWASH PUMP", "CIP PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "SULPHUR BLACK DOSING PUMP"];
	var vfd=["BACKWASH PUMP"];
	var wire2=["LEVEL TRANSMITTER", "PRESSURE TRANSMITTER"];
	var wire4=["ELECTROMAGNETIC FLOWMETER", "PH SENSOR"];
	var level_float=["LEVEL FLOAT"];
	$.each(frm.doc.mf_items || [],function(i,v){
		if(non_vfd.includes(v.item_description)){
			if(v.item_description=="BACKWASH PUMP"){
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
	frm.set_value("digital_input",(non_vfd_tot+vfd_tot)*3+level_float_tot+40+10);//40 for pneumatic valve, 10 EMG, CON ON,ACK,RST,MBR CYCLE ST/SP, RO CY ST/SP,MBR A/M,ETP A/M
	frm.refresh_fields("digital_input");
	frm.set_value("digital_output",non_vfd_tot+vfd_tot+5+40);// 40 for pneumatic valve, 5 for INDIACTION ,ALARM,HOOTER
	frm.refresh_fields("digital_output");
	frm.set_value("analog_input2",(vfd_tot*2)+wire2_tot);
	frm.refresh_fields("analog_input2");
	frm.set_value("analog_input",wire4_tot);
	frm.refresh_fields("analog_input");
	frm.set_value("analog_output",vfd_tot);
	frm.refresh_fields("analog_output");
}