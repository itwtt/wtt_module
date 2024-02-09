// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bio Tank Calculation', {
	refresh:function(frm){
		const element = document.querySelector('.btn.btn-xs.btn-default');
		    element.style.background = 'green';
		    element.style.color = 'white';
	},
	onload:function(frm){
		if(frm.doc.bio_items)
		{

		}
		else
		{
			var bioitem=["LIFTING SUMP PUMP", "EQT DIFFUSER", "EQT TANK PIPE", "EQT BLOWER", "EQUALIZATION FLOW MAKER", "NT, DT, CFT & SRS DIFFUSER", "NT, DT, CFT & SRS PIPE", "DAF BUBBLE GENERATION PUMP", "DAF SLUDGE PUMP", "DAF TURBIDITY SENSOR", "NEUTRALIZATION PUMP", "pH SENSOR", "NT DOSING PUMP", "NT PRESSURE GAUGE", "NT PRESSURE TRANSMITTER", "NT DOSING TANK", "NT EMFM", "DENITRIFICATION FLOW MIXER", "DENITRIFICATION PUMP", "BIO BLOWER", "BIO OTT LATERAL", "TOTAL BLOWER", "BIO DIFFUSER", "BIOLOGICAL FLOW MAKER", "BIO COMMON HEADER PIPE", "BIOLOGICAL INDIVIDUAL TANK PIPE", "BLOWER LINE PUMP", "DO SENSOR", "LEVEL TRANSMITTER", "LEVEL FLOAT", "PIPES & FITTINGS", "LIFTING HOIST"]
			var renamed_description=["SUBMERSIBLE PUMP", "DIFFUSER", "PIPE", "BLOWER", "FLOW MAKER", "DIFFUSER", "PIPE", "BUBBLE GENERATION PUMP", "SURFACE MOUNTED PUMP", "TURBIDITY SENSOR", "SUBMERSIBLE PUMP", "PH SENSOR", "DOSING PUMP", "PRESSURE GAUGE", "PRESSURE TRANSMITTER", "TANK", "ELECTROMAGNETIC FLOWMETER", "FLOW MIXER", "SUBMERSIBLE PUMP", "BLOWER", "OTT LATERAL", "BLOWER", "DIFFUSER", "FLOW MAKER", "PIPE", "PIPE", "PIPE", "DO SENSOR", "LEVEL TRANSMITTER", "LEVEL FLOAT", "PIPES & FITTINGS", "LIFTING HOIST"]
			for(var i=0;i<bioitem.length;i++)
			{
			var child = frm.add_child("bio_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", bioitem[i]);
			frappe.model.set_value(child.doctype, child.name, "renamed", renamed_description[i]);
			frm.refresh_field("bio_items");
			}
		}
		if(frm.doc.bio_electrical_items)
		{

		}
		else
		{
			var bio_ele=["LIFTING SUMP PUMP", "EQT BLOWER", "EQUALIZATION FLOW MAKER", "DAF BUBBLE GENERATION PUMP", "DAF SLUDGE PUMP", "NEUTRALIZATION PUMP", "NT DOSING PUMP", "DENITRIFICATION FLOW MIXER", "DENITRIFICATION PUMP", "BIO BLOWER", "TOTAL BLOWER", "BIOLOGICAL FLOW MAKER", "PANEL", "PLC"]
			
			for(var i=0;i<bio_ele.length;i++)
			{
			var child = frm.add_child("bio_electrical_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", bio_ele[i]);
			frm.refresh_field("bio_electrical_items");
			}
		}
	},
	startup_sheet: function(frm) {
	    var openlink = window.open("https://erp.wttindia.com/app/startup-sheet/"+frm.doc.project_startup_sheet+"","_self");
	},
	project_startup_sheet:function(frm){
		frappe.call({
				method:"wtt_module.wtt_module.doctype.mbr_standard_items.mbr_standard_items.get_qty",
				args:{
					st:frm.doc.project_startup_sheet
				},
				callback(r){					
					var rr=r.message[0]
					$.each(frm.doc.bio_items || [], function(i, v) {
						if(v.item_description=="LIFTING SUMP PUMP"){
							frappe.model.set_value(v.doctype, v.name, "flow", Math.round((rr.flow/24)*1.5))
							frm.refresh_fields("flow");
							var vs = (((rr.tank_height/10)+0.5)*100)/100
							frappe.model.set_value(v.doctype, v.name, "range",vs);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1)
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype, v.name, "sb_qty", 1)
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="EQT DIFFUSER"){
							frappe.model.set_value(v.doctype, v.name, "w_qty", rr.eqtk);
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frm.refresh_fields("flow");
						}
						else if(v.item_description=="EQT TANK PIPE"){
							frappe.model.set_value(v.doctype, v.name, "range", rr.e_bio_size);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", rr.e_bio_float);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="EQT BLOWER"){
							frappe.model.set_value(v.doctype, v.name, "flow", rr.eqt_blower);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "range", rr.eqt_blower_model);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="NT, DT, CFT & SRS DIFFUSER"){
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "range", 0);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", rr.only_air);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="NT, DT, CFT & SRS PIPE"){
							frappe.model.set_value(v.doctype, v.name, "flow", 0);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "range", rr.nsc_blower_line_size);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", rr.nsc_blower_line_length);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="EQUALIZATION FLOW MAKER"){
							if(rr.tank_dimension=='Carousel'){
								frappe.model.set_value(v.doctype, v.name, "w_qty", 1);
								frm.refresh_fields("w_qty")
							}
						}
						else if(v.item_description=="BIOLOGICAL FLOW MAKER"){
							if(rr.tank_dimension=='Carousel'){
								frappe.model.set_value(v.doctype, v.name, "w_qty", rr.no_of_bio_tanks);
								frm.refresh_fields("w_qty");
							}
						}
						else if(v.item_description=="NEUTRALIZATION PUMP"){
							frappe.model.set_value(v.doctype, v.name, "flow", Math.round(rr.flow/24));
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "range", Math.round((rr.tank_height/10)+0.7));
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1)
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype, v.name, "sb_qty", 1)
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="pH SENSOR"){
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1)
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frm.refresh_fields("flow");
						}
						else if(v.item_description=="NT DOSING PUMP"){
							frappe.model.set_value(v.doctype, v.name, "flow", Math.round(rr.flow/15));
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1)
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="NT PRESSURE GAUGE"){
							frappe.model.set_value(v.doctype, v.name, "range", 5);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 2)
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="DAF Turbidity Sensor"){
							frappe.model.set_value(v.doctype, v.name, "flow", 1)
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 2)
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="DAF SLUDGE PUMP"){
							frappe.model.set_value(v.doctype, v.name, "flow", Math.round((rr.flow/24)*0.3))
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1)
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype, v.name, "sb_qty", 1);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="DAF BUBBLE GENERATION PUMP"){
							frappe.model.set_value(v.doctype, v.name, "flow", Math.round((rr.flow/24)*0.3))
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1)
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype, v.name, "sb_qty", 1);
							frm.refresh_fields("sb_qty");
						}
						else if(v.item_description=="TOTAL BLOWER"){
							frappe.model.set_value(v.doctype, v.name, "flow", Math.round(rr.each_blower));
							frm.refresh_fields("flow");
							if(rr.seperate_blower_for_equalization_tank == 0)
							{	frappe.model.set_value(v.doctype, v.name, "range", rr.d_model);
							
								frm.refresh_fields("range");
								frappe.model.set_value(v.doctype, v.name, "w_qty", rr.total_blower);
								frm.refresh_fields("w_qty");
								frappe.model.set_value(v.doctype, v.name, "sb_qty", 1);
								frm.refresh_fields("sb_qty");
							}
							else
							{
								frappe.model.set_value(v.doctype, v.name, "range", 0);
								frm.refresh_fields("range");
								frappe.model.set_value(v.doctype, v.name, "w_qty", 0);
								frm.refresh_fields("w_qty");
								frappe.model.set_value(v.doctype, v.name, "sb_qty", 0);
								frm.refresh_fields("sb_qty");
							}
						}
						else if(v.item_description=="BIO BLOWER"){
							frappe.model.set_value(v.doctype, v.name, "flow", Math.round(rr.bio_blower));
							frm.refresh_fields("flow");
							if(rr.seperate_blower_for_equalization_tank == 1)
							{
								frappe.model.set_value(v.doctype, v.name, "range", rr.d_model);
								frm.refresh_fields("range");
								frappe.model.set_value(v.doctype, v.name, "w_qty", rr.total_blower);
								frm.refresh_fields("w_qty");
								frappe.model.set_value(v.doctype, v.name, "sb_qty", 1);
								frm.refresh_fields("sb_qty");
							}
							else
							{
								frappe.model.set_value(v.doctype, v.name, "range", 0);
								frm.refresh_fields("range");
								frappe.model.set_value(v.doctype, v.name, "w_qty", 0);
								frm.refresh_fields("w_qty");
								frappe.model.set_value(v.doctype, v.name, "sb_qty", 0);
								frm.refresh_fields("sb_qty");
							}
						}
						else if(v.item_description=="NT, DT, CFT & SRS DIFFUSER"){
							var value_w_qty = Math.ceil(((rr.diffuser_dt+rr.diffuser_srs+rr.diffuser_cft+rr.diffuser_nt)/5)*5)
							frappe.model.set_value(v.doctype, v.name, "w_qty", value_w_qty);
							frm.refresh_fields("w_qty");							
						}
						else if(v.item_description=="NT PRESSURE TRANSMITTER"){
							frappe.model.set_value(v.doctype, v.name, "range", 5);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1);
							frm.refresh_fields("w_qty");	
						}
						else if(v.item_description=="NT DOSING TANK"){
							frappe.model.set_value(v.doctype, v.name, "flow", 1000);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="NT EMFM"){
							frappe.model.set_value(v.doctype, v.name, "flow", Math.round(rr.flow/24))
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="DENITRIFICATION FLOW MIXER"){
							frappe.model.set_value(v.doctype, v.name, "flow", 1)
							frm.refresh_fields("flow");
							frappe.call({
								method:"wtt_module.wtt_module.doctype.bio_tank_calculation.bio_tank_calculation.check_system",
								args:{
									"pes":frm.doc.project_startup_sheet,
									"system":"De-Nitrification System"
								},
								callback(r){
									if(r.message=="Found"){
										frappe.model.set_value(v.doctype, v.name, "w_qty", 1)
										frm.refresh_fields("w_qty");										
									}
								}
							})
						}
						else if(v.item_description=="DENITRIFICATION PUMP"){
							frappe.call({
								method:"wtt_module.wtt_module.doctype.bio_tank_calculation.bio_tank_calculation.check_system",
								args:{
									"pes":frm.doc.project_startup_sheet,
									"system":"De-Nitrification System"
								},
								callback(r){
									if(r.message=="Found"){
										frappe.model.set_value(v.doctype, v.name, "flow", Math.round((rr.flow/24)*2))
										frm.refresh_fields("flow");
										frappe.model.set_value(v.doctype, v.name, "w_qty", 2)
										frm.refresh_fields("w_qty");
										frappe.model.set_value(v.doctype, v.name, "sb_qty", 1)
										frm.refresh_fields("sb_qty");										
									}
								}
							})
						}
						else if(v.item_description=="BIO DIFFUSER"){
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 1)
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="BIO COMMON HEADER PIPE"){
							if(rr.seperate_blower_for_equalization_tank==1){
								frappe.model.set_value(v.doctype, v.name, "range", rr.s_blower_size);
								frm.refresh_fields("range");
								frappe.model.set_value(v.doctype, v.name, "w_qty", rr.s_blower_length);
								frm.refresh_fields("w_qty");
							}	
							else{
								frappe.model.set_value(v.doctype, v.name, "range", rr.n_s_blower_size);
								frm.refresh_fields("range");
								frappe.model.set_value(v.doctype, v.name, "w_qty", rr.ns_blower_length);
								frm.refresh_fields("w_qty");
							}							
						}
						else if(v.item_description=="BIOLOGICAL INDIVIDUAL TANK PIPE"){
							frappe.model.set_value(v.doctype, v.name, "range", rr.b_bio_size);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", rr.b_bio_length);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="BLOWER LINE PUMP"){
							frappe.model.set_value(v.doctype, v.name, "flow", 0);
							frm.refresh_fields("flow");
							frappe.model.set_value(v.doctype, v.name, "range", rr.d_blower_size);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", rr.d_blower_length);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="DO SENSOR"){
							frappe.model.set_value(v.doctype, v.name, "w_qty", rr.no_of_bio_tanks);
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frm.refresh_fields("flow");
						}
						else if(v.item_description=="LEVEL TRANSMITTER"){
							frappe.model.set_value(v.doctype, v.name, "range", rr.tank_height);
							frm.refresh_fields("range");
							frappe.model.set_value(v.doctype, v.name, "w_qty", 3);
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frm.refresh_fields("flow");
						}
						else if(v.item_description=="LEVEL FLOAT"){
							frappe.model.set_value(v.doctype, v.name, "w_qty", 3);
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype, v.name, "flow", 1);
							frm.refresh_fields("flow");
						}
						else if(v.item_description=="LIFTING HOIST"){
							frappe.model.set_value(v.doctype, v.name, "w_qty", 3);
							frm.refresh_fields("w_qty");
						}
						else if(v.item_description=="BIO OTT LATERAL"){
							frappe.model.set_value(v.doctype, v.name, "w_qty", rr.ott_laterals);
							frm.refresh_fields("w_qty");
							frappe.model.set_value(v.doctype, v.name, "range", "AR"+rr.ott_lateral_size);
							frm.refresh_fields("range");
						}
					});

				}
			});
		frappe.call({
			method:"wtt_module.wtt_module.doctype.startup_sheet.startup_sheet.get_system",
			args:{
				st:frm.doc.project_startup_sheet
			},
			callback(r){
				var vt=0;
				frappe.db.get_value('Startup Sheet',frm.doc.project_startup_sheet, ['enter_tank_diameter','is_with_mechanism','with_mechanism','without_mechanism'])
				    .then(res => {
				    console.log(res.message)		    
					for(var i=0;i<r.message.length;i++)
					{    
						var child = frm.add_child("bio_items");
						if(r.message[i].select_system=="Circular Clarifier System")
						{
							frappe.model.set_value(child.doctype, child.name, "item_description", r.message[i].select_system);
							frappe.model.set_value(child.doctype, child.name, "parameter", "DIAMETER");
							frappe.model.set_value(child.doctype, child.name, "range", res.message.enter_tank_diameter);
						}
						else if(r.message[i].select_system=="Degasser System")
						{
							frappe.model.set_value(child.doctype, child.name, "item_description", r.message[i].select_system);
							frappe.model.set_value(child.doctype, child.name, "parameter", "DIAMETER");
							var dia=0;
							if(frm.doc.flow>=400 && frm.doc.flow<=600)
							{
								dia=1;
							}
							else if(frm.doc.flow>600 && frm.doc.flow<=1000)
							{
								dia=1.4;
							}
							else if(frm.doc.flow>1000 && frm.doc.flow<=1600)
							{
								dia=1.8;
							}
							else if(frm.doc.flow>1600 && frm.doc.flow<=2500)
							{
								dia=2.2;
							}
							else if(frm.doc.flow>2500 && frm.doc.flow<=5000)
							{
								dia=3;
							}
							frappe.model.set_value(child.doctype, child.name, "range", dia);
						}
						else if(r.message[i].select_system=="Rotary Brush Screener")
						{
							frappe.model.set_value(child.doctype, child.name, "item_description", r.message[i].select_system);
							frappe.model.set_value(child.doctype, child.name, "parameter", "WIDTH");
							var width=0;
							if(frm.doc.flow>=0 && frm.doc.flow<=2150)
							{
								width=600;
							}
							else if(frm.doc.flow>2150 && frm.doc.flow<=4600)
							{
								width=800;
							}
							else if(frm.doc.flow>4600 && frm.doc.flow<=7000)
							{
								width=1200;
							}
							else if(frm.doc.flow>7000 && frm.doc.flow<=9000)
							{
								width=1500;
							}
							frappe.model.set_value(child.doctype, child.name, "range", width);
						}
						else if(r.message[i].select_system=="Cooling Tower")
						{
							frappe.model.set_value(child.doctype, child.name, "item_description", r.message[i].select_system);
							frappe.model.set_value(child.doctype, child.name, "parameter", "FLOW");
							var flowrate=0;
							if(frm.doc.flow>=0 && frm.doc.flow<=750)
							{
								flowrate=750;
							}
							else if(frm.doc.flow>750)
							{
								flowrate=1500;
							}
							frappe.model.set_value(child.doctype, child.name, "range", flowrate);
						}
						else if(r.message[i].select_system=="Belt Press")
						{
							frappe.model.set_value(child.doctype, child.name, "item_description", r.message[i].select_system);
							frappe.model.set_value(child.doctype, child.name, "parameter", "EDOM");
							var btvalue=0;	
							if(res.message.is_with_mechanism==1)
							{
								if(res.message.with_mechanism>0 && res.message.with_mechanism<=1.6)
								{
									btvalue=350;	
								}
								else if(res.message.with_mechanism>1.6 && res.message.with_mechanism<=2.5)
								{
									btvalue=500;
								}
								else if(res.message.with_mechanism>2.5 && res.message.with_mechanism<=4.5)
								{
									btvalue=800;
								}
								else if(res.message.with_mechanism>4.5 && res.message.with_mechanism<=6.5)
								{
									btvalue=1000;
								}
								else if(res.message.with_mechanism>6.5 && res.message.with_mechanism<=9.5)
								{
									btvalue=1200;
								}
								else if(res.message.with_mechanism>9.5 && res.message.with_mechanism<=11)
								{
									btvalue=1300;
								}
								else if(res.message.with_mechanism>11 && res.message.with_mechanism<=14)
								{
									btvalue=1500;
								}
								frappe.model.set_value(child.doctype, child.name, "range", btvalue);
							}
							else
							{
								if(res.message.without_mechanism>0 && res.message.without_mechanism<=1.6)
								{
									btvalue=350;	
								}
								else if(res.message.without_mechanism>1.6 && res.message.without_mechanism<=2.5)
								{
									btvalue=500;
								}
								else if(res.message.without_mechanism>2.5 && res.message.without_mechanism<=4.5)
								{
									btvalue=800;
								}
								else if(res.message.without_mechanism>4.5 && res.message.without_mechanism<=6.5)
								{
									btvalue=1000;
								}
								else if(res.message.without_mechanism>6.5 && res.message.without_mechanism<=9.5)
								{
									btvalue=1200;
								}
								else if(res.message.without_mechanism>9.5 && res.message.without_mechanism<=11)
								{
									btvalue=1300;
								}
								else if(res.message.without_mechanism>11 && res.message.without_mechanism<=14)
								{
									btvalue=1500;
								}
								frappe.model.set_value(child.doctype, child.name, "range", btvalue);
							}
						}
						else if(r.message[i].select_system=="Screw Press")
						{
							frappe.model.set_value(child.doctype, child.name, "item_description", r.message[i].select_system);
							frappe.model.set_value(child.doctype, child.name, "parameter", "FLOW / HR");
							var btvalue=0;
							if(res.message.is_with_mechanism==1)
							{
								if(res.message.with_mechanism>0 && res.message.with_mechanism<=3)
								{
									btvalue=3;	
								}
								else if(res.message.with_mechanism>3 && res.message.with_mechanism<=5)
								{
									btvalue=5;
								}
								else if(res.message.with_mechanism>5 && res.message.with_mechanism<=10)
								{
									btvalue=10;
								}
								frappe.model.set_value(child.doctype, child.name, "range", btvalue);
							}
							else
							{
								if(res.message.without_mechanism>0 && res.message.without_mechanism<=3)
								{
									btvalue=3;	
								}
								else if(res.message.without_mechanism>3 && res.message.without_mechanism<=5)
								{
									btvalue=5;
								}
								else if(res.message.without_mechanism>5 && res.message.without_mechanism<=10)
								{
									btvalue=10;
								}
								frappe.model.set_value(child.doctype, child.name, "range", btvalue);
							}
						}
						else if(r.message[i].select_system=="Self-Cleaning Filter")
						{
							frappe.model.set_value(child.doctype, child.name, "item_description", r.message[i].select_system);
							frappe.model.set_value(child.doctype, child.name, "parameter", "FLOW / HR");
							var ts=frm.doc.flow/20;
							var flowhr=0;
							if(ts>0 && ts<=30)
							{
								flowhr=30;
							}
							else if(ts>30 && ts<=41)
							{
								flowhr=41;
							}
							else if(ts>41 && ts<=82)
							{
								flowhr=82;
							}
							else
							{
								flowhr=90;
							}
							frappe.model.set_value(child.doctype, child.name, "range", flowhr);
						}
						else if(r.message[i].select_system=="DAF (Dissolved Air Flotation)")
						{
							frappe.model.set_value(child.doctype, child.name, "item_description", r.message[i].select_system);
							frappe.model.set_value(child.doctype, child.name, "parameter", "DIMENSION");
							var dafdimen=0;
							if(frm.doc.flow>0 && frm.doc.flow<=1150)
							{
								dafdimen="2X5"
							}
							else if(frm.doc.flow>1150 && frm.doc.flow<=1700)
							{
								dafdimen="3X5"
							}
							else if(frm.doc.flow>1700)
							{
								dafdimen="> 1700"
							}
							frappe.model.set_value(child.doctype, child.name, "range", dafdimen);
						}
						else
						{
							frappe.model.set_value(child.doctype, child.name, "item_description", r.message[i].select_system);
						}
						frm.refresh_field("bio_items");
					}
				});
			}
		});	
	},
	not_linked_items:function(frm){
		frm.clear_table("not_linked_table")
		frm.refresh_field("not_linked_table");
		$.each(frm.doc.bio_items || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("not_linked_table");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frm.refresh_field("not_linked_table");
			}
		});
	},
	panel:function(frm,cdt,cdn){
		from_panel_calculate_other_plc_qty(frm,cdt,cdn);
		calculate_missed(frm,cdt,cdn);
	}
});
frappe.ui.form.on('Bio Items', {
	flow:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		var ele=["LIFTING SUMP PUMP", "EQT BLOWER", "EQUALIZATION FLOW MAKER", "DAF BUBBLE GENERATION PUMP", "DAF SLUDGE PUMP", "NEUTRALIZATION PUMP", "DENITRIFICATION FLOW MIXER", "DENITRIFICATION PUMP", "BIOLOGICAL FLOW MAKER"]
		if(child.range!=undefined && ele.includes(child.item_description)){
			update_kw_in_electrical_table(frm,cdt,cdn)
		}
	},
	range:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		var ele=["LIFTING SUMP PUMP", "EQT BLOWER", "EQUALIZATION FLOW MAKER", "DAF BUBBLE GENERATION PUMP", "DAF SLUDGE PUMP", "NEUTRALIZATION PUMP", "DENITRIFICATION FLOW MIXER", "DENITRIFICATION PUMP", "BIOLOGICAL FLOW MAKER"]
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
frappe.ui.form.on('Bio Not linked items', {
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


frappe.ui.form.on('Bio Electrical Items', {
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
	$.each(frm.doc.bio_electrical_items || [],function(i,v){
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
	$.each(frm.doc.bio_electrical_items || [], function(i, v) {
		if(v.item_description==child.item_description)
		{
			frappe.model.set_value(v.doctype, v.name, "w_qty", child.w_qty)
			frm.refresh_fields("w_qty");
		}
	})
}
var update_sbqty_in_child_table2 = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.bio_electrical_items || [],function(i,v){
		if(v.item_description==child.item_description){
			frappe.model.set_value(v.doctype,v.name,"sb_qty",child.sb_qty);
			frm.refresh_fields("sb_qty");
		}
	})
}
var update_ssbqty_in_child_table2 = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.bio_electrical_items || [],function(i,v){
		if(v.item_description==child.item_description){
			frappe.model.set_value(v.doctype,v.name,"ssb_qty",child.ssb_qty);
			frm.refresh_fields("ssb_qty");
		}
	})
}
var from_panel_calculate_other_plc_qty = function(frm,cdt,cdn){
	var child = locals[cdt][cdn];
	$.each(frm.doc.bio_electrical_items || [],function(i,v){
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
	$.each(frm.doc.bio_items || [],function(i,v){
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