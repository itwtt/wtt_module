// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Startup Sheet', {
	refresh:function(frm){
		// var lavender = ["required_retention_time_hours","tank_height","no_of_bio_tanks","cod_reduction_for_og","total_blower"]
		// var green = ["required_clarifier_diameter","each_blower","bio_blower","eq_blower"]
		// var blue = ["clarifier_diameter"]
		// var elements = document.querySelectorAll('[data-fieldname]');
		// for (var i = 0; i < elements.length; i++) {
		//     var element = elements[i];
		//     var dataField = element.getAttribute('data-fieldname');
		//     if (green.includes(dataField)) {
		//         element.style.color = 'green';
		//     } 
		//     else if (blue.includes(dataField)) {
		//         element.style.color = 'blue';
		//     }
		//     else if (lavender.includes(dataField)) {
		//         element.style.color = 'purple';
		//     }
		// }
	},
	setup:function(frm){
		
	},
	onload:function(frm){
		
		if(frm.doc.cost_working_data)
		{
			if(frm.doc.cost_working_data == "Deleted")
			{

			}
			else
			{
				frm.toggle_display("generate_cost_working", false);
			}
		}
		else
		{

		}
		frm.clear_table("system_details")
		frm.refresh_field("system_details");
		var arr=["Rotary Brush Screener", "Bar Screener", "Drum Screener", "Anaerobic Screener", "Anaerobic Bar Screener","Anaerobic Lifting Pump","Anaerobic Neutralization", "Anaerobic System", "Anaerobic Ammonia Striper","Anaerobic Cooling Tower","Anaerobic Settler","Anaerobic Lamella Settler","Anaerobic CTS", "Ammonia Striper", "Lifting sump", "Oil & grease trap", "DAF (Dissolved Air Flotation)", "Equalization System", "Neutralization System","Cooling Tower","De-Nitrification System", "Distribution system", "Biological Oxidation System", "Clarifier Feed Tank", "Circular Clarifier System", "Lamella Settler", "DO increase system", "SRS System", "Sand Filter", "Activated Carbon Filter", "Self-Cleaning Filter", "Micro Filtration - ASAHI", "Submerged MBR system - KOCH", "Submerged MBR system - OVIVO", "Sulphur Black Removal System", "Sludge Thickener", "Sludge Thickener with mech", "Screw Press", "Belt Press", "Degasser System", "Reverse Osmosis", "Hardness and Silica Removal System", "Chlorination system", "Hardness and Color Removal System", "Reject Reverse Osmosis", "Evaporator", "Agitated Thin film dryer", "Centrifuge", "Crystallizer", "Nano Filtration", "Care system","CTS MBR","CTS Cooling Tower","Rewolutte RO"]
		var arr1=["Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment","Pre Treatment","Pre Treatment","Pre Treatment","Pre Treatment", "Pre Treatment","Pre Treatment","Pre Treatment", "Pre Treatment","Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment","Pre Treatment","Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Filtration", "Filtration", "Filtration", "Filtration", "Filtration", "Filtration", "Filtration", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Filtration", "Filtration", "Filtration", "Filtration", "Filtration", "Filtration", "Rms", "Rms", "Rms", "Rms", "Filtration", "Others","Brinex/Rewolutte","Brinex","Rewolutte"]
		for(var i=0;i<arr.length;i++)
		{
			var child = frm.add_child("system_details");
			frappe.model.set_value(child.doctype, child.name, "system_name", arr[i]);
			frappe.model.set_value(child.doctype, child.name, "type", arr1[i]);
			frm.refresh_field("system_details");
		}

		frm.fields_dict['system_details'].grid.add_custom_button('Add items', () => {
			var arr2=[]
			$.each(frm.doc.selected_system, function (index, source_row) {
				arr2.push(source_row.selected_system_name)
			});

			$.each(frm.doc.system_details, function (index, source_row) {
			    if(source_row.__checked==true)
			    {   
			    	if(source_row.system_name=="Sludge Thickener with mech"){
			    		frm.set_value("is_with_mechanism",1);
			    		frm.refresh_field("is_with_mechanism");
			    	}
			    	if(!arr2.includes(source_row.system_name)){
			    		var child = frm.add_child("selected_system");
						frappe.model.set_value(child.doctype, child.name, "selected_system_name",source_row.system_name);
						frappe.model.set_value(child.doctype, child.name, "selected_type",source_row.type);
						frm.refresh_field("selected_system");
			    	}
			    }
			});
		});
	},
	pretreatment_clarifier:function(frm){
		var ar=["Rotary Brush Screener", "Lifting sump", "Equalization System", "Neutralization System", "Cooling Tower", "Distribution system", "Biological Oxidation System", "Clarifier Feed Tank", "Circular Clarifier System", "SRS System", "Sludge Thickener", "Screw Press"]
		append_selected_system(frm,ar)
		
	},
	pretreatment_lamella:function(frm){
		var ar=["Rotary Brush Screener", "Lifting sump", "Equalization System", "Neutralization System", "Cooling Tower", "Distribution system", "Biological Oxidation System", "Clarifier Feed Tank", "Lamella Settler", "SRS System", "Sludge Thickener", "Screw Press"]
		append_selected_system(frm,ar)
	},
	do_increase:function(frm){
		var ar=["DO increase system"]
		append_selected_system(frm,ar)
	},
	daf:function(frm){
		var ar=["DAF (Dissolved Air Flotation)"]
		append_selected_system(frm,ar)
	},
	anaerobic_settler_b:function(frm){
		var ar=["Anaerobic Screener","Anaerobic Lifting Pump","Anaerobic Neutralization","Anaerobic Cooling Tower","Anaerobic Settler",]
		append_selected_system(frm,ar)
	},
	dnt:function(frm){
		var ar=["De-Nitrification System"]
		append_selected_system(frm,ar)
	},
	filtration_mf:function(frm){
		var ar=["Self-Cleaning Filter", "Micro Filtration - ASAHI"]
		append_selected_system(frm,ar)
	},
	filtration_koch:function(frm){
		var ar=["Submerged MBR system - KOCH"]
		append_selected_system(frm,ar)
	},
	filtration_ovivo:function(frm){
		var ar=["Submerged MBR system - OVIVO"]
		append_selected_system(frm,ar)
	},
	sulphur_black:function(frm){
		var ar=["Sulphur Black Removal System"]
		append_selected_system(frm,ar)
	},
	dgt:function(frm){
		var ar=["Degasser System"]
		append_selected_system(frm,ar)
	},
	ro:function(frm){
		var ar=["Reverse Osmosis"]
		append_selected_system(frm,ar)
	},
	rewolutte:function(frm){
		var ar=["Hardness and Silica Removal System", "Chlorination system", "CTS MBR", "Rewolutte RO"]
		append_selected_system(frm,ar)
	},
	brinex:function(frm){
		var ar=["Hardness and Silica Removal System", "Chlorination system", "CTS MBR", "CTS Cooling Tower", "Reject Reverse Osmosis"]
		append_selected_system(frm,ar)
	},
	evaporator:function(frm){
		var ar=["Evaporator"]
		append_selected_system(frm,ar)
	},
	atfd:function(frm){
		var ar=["Agitated Thin film dryer", "Centrifuge"]
		append_selected_system(frm,ar)
	},
	crystallizer:function(frm){
		var ar=["Crystallizer"]
		append_selected_system(frm,ar)
	},
	care:function(frm){
		var ar=["Care system"]
		append_selected_system(frm,ar)
	},
	ammonia_stream_b:function(frm){
		var ar=["Anaerobic Screener", "Anaerobic Lifting Pump", "Anaerobic Ammonia Striper"]
		append_selected_system(frm,ar)
	},
	anaerobic_cts_b:function(frm){
		var ar=["Anaerobic Screener", "Anaerobic Lifting Pump", "Anaerobic Neutralization", "Anaerobic CTS", "Anaerobic Lamella Settler"]
		append_selected_system(frm,ar)
	},
	clear:function(frm){
		frm.clear_table("selected_system");
		frm.refresh_field("selected_system");
	},
	is_rewolutte:function(frm)
	{
		if(frm.doc.is_rewolutte == 1)
		{
			frm.set_value("cost_working_data","");
			frm.refresh_field("cost_working_data");
		}
	},
	tank_height:function(frm){
		frm.set_value("do_increase_tank_height",frm.doc.tank_height);
		frm.refresh_field("do_increase_tank_height");
	},
	startup_sheet:function(frm){
		frappe.db.get_value('Startup Sheet', frm.doc.startup_sheet, ['flow', 'cod', 'bod','ro_recovery','tdsmgl','tss'])
		    .then(r => {
		        let values = r.message;
		        console.log(values)
		        frm.set_value("flow",(values.flow*(1-(values.ro_recovery/100))*1.05)+values.flow);
		        frm.refresh_field("flow");
		        frm.set_value("cod",values.cod);
		        frm.refresh_field("cod");
		        frm.set_value("bod",values.bod);
		        frm.refresh_field("bod");
		        frm.set_value("tdsmgl",values.tdsmgl);
		        frm.refresh_field("tdsmgl");
		        frm.set_value("tss",values.tss);
		        frm.refresh_field("tss");
		    })
	},
	generate_cost_working:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.startup_sheet.startup_sheet.generate_cost",
			args:{
				nam:frm.doc.name,
				ro_tem:frm.doc.ro_template,
				project:frm.doc.project,
				rewolutte_ro:frm.doc.rewolutte_ro,
				startup_sheet:frm.doc.startup_sheet,
				cip:frm.doc.choose_cip
			},
			callback(r){
				var openlink = window.open("https://erp.wttindia.com/app/cost-working-tool/"+r.message[0]+"");
				frm.set_value("cost_working_data",r.message[0]);
				frm.refresh_field("cost_working_data");
				frm.save();
			}
		});
	},
	cost_working_link:function(frm){
		if(frm.doc.cost_working_data == "Deleted")
		{
			frappe.throw("There is no costworking tool for this startup sheet")
		}
		else
		{
			var openlink = window.open("https://erp.wttindia.com/app/cost-working-tool/"+frm.doc.cost_working_data+"","_self");
		}
	},
	get_flowchart:function(frm){
		var tds=0;
		var selected=[];
		var ro=[];
		var tds = frm.doc.tdsmgl

		$.each(frm.doc.selected_system, function (index, source_row) {
			var after_ro=['Hardness and Silica Removal System','Chlorination system','Hardness and Color Removal System','Reject Reverse Osmosis'];
			if(!after_ro.includes(source_row.selected_system_name)){
				selected.push({
					"system":source_row.selected_system_name,
					"type":source_row.selected_type
				})
			}
			if(after_ro.includes(source_row.selected_system_name))
			ro.push({
				"system":source_row.selected_system_name
			})

		});
		var vs='<br>';
		vs+='<style>.tab-cls{border:0px!important;}.tab-cls th,.tab-cls td,.tab-cls tr{border:0px!important;margin-top:0px;margin-bottom:0px;vertical-align:middle!important}.tab-cls div{margin: 0px;}</style>'
		
		if(frm.doc.ro_recovery)
		{
			vs+='<table border="1px" cellpadding="5" cellspacing="5" align="right" style="width:160px!important"><tr><th>SYSTEM</th><th>RECOVERY</th></tr><tr><td>RO</td><td>'+frm.doc.ro_recovery+'%</td></tr></table><br><br><br><br>';
		}
		vs+='<div style="background:#da9695;border: 1px solid black;width:160px;height:30px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;">Effluent</div>';
		vs+='<div style="display:inline-flex;width:160px"><p style="margin-top: 0px;margin-bottom: 0px;text-align:right;width:33%;">'+frm.doc.flow+'<br>'+tds+'</p><p style="text-align:center;font-size:25px;margin-top:0px;margin-bottom:0px;width:33%;">&#8595;</p><p style="margin-top: 0px;margin-bottom: 0px;text-align:left;width:33%;">M<sup>3</sup>/day<br>TDS</p></div>';
		
		for(var i=0;i<selected.length;i++)
		{
			if(selected[i].type=="Pre Treatment")
			{
				if(selected[i].system=='DAF (Dissolved Air Flotation)' && frm.doc.daf_with_dosing==1)
				{
					vs+='<table class="tab-cls"><tr><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;"><p style="font-size:12px">DAF (Dissolved Air Flotation)</p></div>'
					vs+='</td><td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'	
				}
				else if(selected[i].system=='Submerged MBR system - KOCH' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table class="tab-cls"><tr><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;"><p style="font-size:12px">Submerged MBR system - KOCH</p></div></td><td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Submerged MBR system - OVIVO' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table class="tab-cls"><tr><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;"><p style="font-size:12px">Submerged MBR system - OVIVO</p></div></td><td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Reverse Osmosis')
				{
					vs+='<table class="tab-cls" style="border:0px!important;"><tr><td style="border:0px!important;"><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;"><p style="font-size:12px">Reverse Osmosis</p></div></td>'
					for(var j=0;j<ro.length;j++){
						if(j==0){
							vs+='<td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;"><p style="font-size:12px">'+ro[j].system+'</p>'
						}
						else{
							vs+='<span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8595;</span><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;"><p style="font-size:12px">'+ro[j].system+'</p></div>'
						}
						
					}
					vs+='</td></tr></table>'
				}
				else
				{
					vs+='<div style="background:#f2d3b7;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;margin-top: 0px;margin-bottom: 0px;">'+selected[i].system+'</div>'
				}	
				if(i==(selected.length-1))
				{

				}
				else
				{
					vs+='<div style="display:inline-flex;width:160px"><p style="margin-top: 0px;margin-bottom: 0px;text-align:right;width:33%;">'+frm.doc.flow+'<br>'+tds+'</p><p style="text-align:center;font-size:25px;margin-top:0px;margin-bottom:0px;width:33%;">&#8595;</p><p style="margin-top: 0px;margin-bottom: 0px;text-align:left;width:33%;">M<sup>3</sup>/day<br>TDS</p></div>';
					// vs+='<p style="margin-top:0px;margin-bottom:0px;"><span style="margin-left:70px;font-size:20px;margin-top:0px;margin-bottom:0px;">&#8595;</span></p>';
				}
			}
			else if(selected[i].type=="Filtration")
			{
				if(selected[i].system=='DAF (Dissolved Air Flotation)' && frm.doc.daf_with_dosing==1)
				{
					vs+='<table class="tab-cls"><tr><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">DAF (Dissolved Air Flotation)</p></div></td><td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'	
				}
				else if(selected[i].system=='Submerged MBR system - KOCH' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table class="tab-cls"><tr><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Submerged MBR system - KOCH</p></div></td><td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Submerged MBR system - OVIVO' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table class="tab-cls"><tr><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Submerged MBR system - OVIVO</p></div></td><td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Reverse Osmosis')
				{
					vs+='<table class="tab-cls" style="border:0px!important;"><tr><td style="border:0px!important;"><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Reverse Osmosis</p></div></td>'
					for(var j=0;j<ro.length;j++){
						if(j==0){
							vs+='<td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">'+ro[j].system+'</p>'
						}
						else{
							vs+='<span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8595;</span><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">'+ro[j].system+'</p></div>'
						}
						
					}
					vs+='</td></tr></table>'
				}
				else
				{
					vs+='<div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;">'+selected[i].system+'</div>'
				}
				if(i==(selected.length-1))
				{

				}
				else
				{
					vs+='<div style="display:inline-flex;width:160px"><p style="margin-top: 0px;margin-bottom: 0px;text-align:right;width:33%;">'+frm.doc.flow+'<br>'+tds+'</p><p style="text-align:center;font-size:25px;margin-top:0px;margin-bottom:0px;width:33%;">&#8595;</p><p style="margin-top: 0px;margin-bottom: 0px;text-align:left;width:33%;">M<sup>3</sup>/day<br>TDS</p></div>';
					// vs+='<p style="margin-top:0px;margin-bottom:0px;"><span style="margin-left:70px;font-size:20px;margin-top:0px;margin-bottom:0px;">&#8595;</span></p>';
				}
			}
			else
			{
				if(selected[i].system=='DAF (Dissolved Air Flotation)' && frm.doc.daf_with_dosing==1)
				{
					vs+='<table class="tab-cls"><tr><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">DAF (Dissolved Air Flotation)</p></div></td><td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'	
				}
				else if(selected[i].system=='Submerged MBR system - KOCH' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table class="tab-cls"><tr><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Submerged MBR system - KOCH</p></div></td><td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Submerged MBR system - OVIVO' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table class="tab-cls"><tr><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Submerged MBR system - OVIVO</p></div></td><td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Reverse Osmosis')
				{
					vs+='<table class="tab-cls" style="border:0px!important;"><tr><td style="border:0px!important;"><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Reverse Osmosis</p></div></td>'
					for(var j=0;j<ro.length;j++){
						if(j==0){
							vs+='<td class="right-arrow"><span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">'+ro[j].system+'</p>'
						}
						else{
							vs+='<span style="font-size:20px;margin-top: 0px;margin-bottom: 0px;">&#8595;</span><div style="background:#97b1cd;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;"><p style="font-size:12px">'+ro[j].system+'</p></div>'
						}
						
					}
					vs+='</td></tr></table>'
				}
				else
				{
					vs+='<div style="background:#d8e5bc;border: 1px solid black;width:160px;height:35px;text-align: center;vertical-align: middle;">'+selected[i].system+'</div>'
				}	
				if(i==(selected.length-1))
				{

				}
				else
				{
					vs+='<div style="display:inline-flex;width:160px"><p style="margin-top: 0px;margin-bottom: 0px;text-align:right;width:33%;">'+frm.doc.flow+'<br>'+tds+'</p><p style="text-align:center;font-size:25px;margin-top:0px;margin-bottom:0px;width:33%;">&#8595;</p><p style="margin-top: 0px;margin-bottom: 0px;text-align:left;width:33%;">M<sup>3</sup>/day<br>TDS</p></div>';
					// vs+='<p style="margin-top:0px;margin-bottom:0px;"><span style="margin-left:70px;font-size:20px;margin-top:0px;margin-bottom:0px;">&#8595;</span></p>';
				}
				vs+=''
			}
		}
		frm.set_value('html_editor',vs);
		frm.refresh_field("html_editor");
	},
	pre_treatment_template: function(frm) {
		if(frm.doc.bio_link)
		{
			var openlink = window.open("https://erp.wttindia.com/app/bio-tank-calculation/"+frm.doc.bio_link+"","_self");
		}
		else
		{
			var openlink = window.open("https://erp.wttindia.com/app/bio-tank-calculation/new-bio-tank-calculation-1?project_startup_sheet="+frm.doc.name+"","_self");
		}
	},
	mf_template:function(frm){
		if(frm.doc.mf_link)
		{
			var openlink = window.open("https://erp.wttindia.com/app/mf-standard-items/"+frm.doc.mf_link+"","_self");
		}
		else
		{
			var openlink = window.open("https://erp.wttindia.com/app/mf-standard-items/new-mf-standard-items-1?project_startup_sheet="+frm.doc.name+"","_self");
		}
	},
	mbr_koch_template:function(frm){
		if(frm.doc.mbr_koch)
		{
			var openlink = window.open("https://erp.wttindia.com/app/mbr-standard-items/"+frm.doc.mbr_koch+"","_self");
		}
		else
		{
			var openlink = window.open("https://erp.wttindia.com/app/mbr-standard-items/new-mbr-standard-items-1?project_startup_sheet="+frm.doc.name+"","_self");
		}
	},
	mbr_ovivo_template:function(frm){
		if(frm.doc.mbr_ovivo)
		{
			var openlink = window.open("https://erp.wttindia.com/app/mbr-ovivo-standard-items/"+frm.doc.mbr_ovivo+"","_self");
		}
		else
		{
			var openlink = window.open("https://erp.wttindia.com/app/mbr-ovivo-standard-items/new-mbr-ovivo-standard-items-1?project_startup_sheet="+frm.doc.name+"","_self");
		}
	},
	cost_working_tool:function(frm){
		if(frm.doc.cost_working)
		{
			var openlink = window.open("https://erp.wttindia.com/app/cost-working-tool/"+frm.doc.cost_working+"","_self");
		}
		else
		{
			var openlink = window.open("https://erp.wttindia.com/app/cost-working-tool/new-cost-working-tool-1?project_startup_sheet="+frm.doc.name+"","_self");
		}
	},
	validate:function(frm){
		var selected_system_array=[];
		$.each(frm.doc.selected_system || [], function(ii, vv) {
			selected_system_array.push(vv.selected_system_name);
		});
		if(frm.doc.tank_height>8)
		{
			var ttk_val = (frm.doc.tank_height - 8);
			var soft_per_cal = (20/12)*ttk_val;
			var ttk_val_1 = 8;
			var soft_per_cal_1 = (20/6)*(ttk_val_1-0.3);
			var final_soft = soft_per_cal + soft_per_cal_1
			frm.set_value("soft_per",final_soft);
			frm.refresh_field("soft_per");
		}
		else
		{
			frm.set_value("soft_per",(((20/100)*(frm.doc.tank_height -0.3))/6) *100);
			frm.refresh_field("soft_per");
		}
		frm.set_value("bod_value",(((frm.doc.flow*frm.doc.bod) * (1-((frm.doc.cod_reduction_for_og)/100)) + (frm.doc.tkn * 4.57 * frm.doc.flow)) /1000));
		frm.refresh_field("bod_value");
		frm.set_value("soft",((frm.doc.bod_value/frm.doc.soft_per)*100));
		frm.refresh_field("soft");
		var v=(frm.doc.soft)/(frm.doc.fouling_diffuser*frm.doc.soft_factor);
		frm.set_value("at_o2",v);
		frm.refresh_field("at_o2");
		frm.set_value("real_o2",(frm.doc.at_o2*(100/20)));
		frm.refresh_field("real_o2");
		frm.set_value("real_o2_day",(frm.doc.real_o2/0.8));
		frm.refresh_field("real_o2_day");
		frm.set_value("real_o2_hr",(frm.doc.real_o2_day/24));
		frm.refresh_field("real_o2_hr");
		if(frm.doc.des_per!=0)
		{
			frm.set_value("designing",((frm.doc.real_o2_hr*(1+(frm.doc.des_per/100)))));
			frm.refresh_field("designing");
		}	
		else
		{
			frm.set_value("designing",(frm.doc.real_o2_hr));
			frm.refresh_field("designing");
		}
		frm.set_value("no_of_diff",(frm.doc.real_o2_hr/frm.doc.flow_rate_diffuser));
		frm.refresh_field("no_of_diff");
		frm.set_value("ret_in_day_eqt",(frm.doc.ret_in_hr_eqt/24));
		frm.refresh_field("no_of_diff");
		var ar_val=(frm.doc.flow*frm.doc.ret_in_day_eqt)/frm.doc.tank_height;
		frm.set_value("area_eqt",ar_val);
		frm.refresh_field("area_eqt");
		frm.set_value("diffuser_eqt",(ar_val/frm.doc.div_point_diffuser));
		frm.refresh_field("diffuser_eqt");
		frm.set_value("ret_in_day_rewolutte",(frm.doc.ret_in_hr_rewolutte/24));
		frm.refresh_field("no_of_diff");
		var ar_val_rewolutte=(frm.doc.flow*frm.doc.ret_in_day_rewolutte)/frm.doc.tank_height;
		frm.set_value("area_rewolutte",ar_val_rewolutte);
		frm.refresh_field("area_rewolutte");
		frm.set_value("diffuser_rewolutte",(ar_val_rewolutte/frm.doc.div_point_diffuser));
		frm.refresh_field("diffuser_rewolutte");

		frm.set_value("ret_in_day_dt",(frm.doc.ret_in_hr_dt/24));
		frm.refresh_field("ret_in_day_dt");
		var ar_val1=(frm.doc.flow*frm.doc.ret_in_day_dt)/frm.doc.tank_height;
		frm.set_value("area_dt",ar_val1);
		frm.refresh_field("area_dt");
		frm.set_value("diffuser_dt",Math.ceil((ar_val1/frm.doc.div_point_diffuser) / 2) * 2);
		frm.refresh_field("diffuser_dt");

		frm.set_value("ret_in_day_srs",(frm.doc.ret_in_hr_srs/24));
		frm.refresh_field("ret_in_day_srs");
		var ar_val2=(frm.doc.flow*frm.doc.ret_in_day_srs)/frm.doc.tank_height;
		frm.set_value("area_srs",ar_val2);
		frm.refresh_field("area_srs");
		frm.set_value("diffuser_srs",Math.ceil((ar_val2/frm.doc.div_point_diffuser) / 2) * 2);
		frm.refresh_field("diffuser_srs");

		frm.set_value("ret_in_day_cft",(frm.doc.ret_in_hr_cft/24));
		frm.refresh_field("ret_in_day_cft");
		var ar_val3=(frm.doc.flow*frm.doc.ret_in_day_cft)/frm.doc.tank_height;
		frm.set_value("area_cft",ar_val3);
		frm.refresh_field("area_cft");
		frm.set_value("diffuser_cft",Math.ceil((ar_val3/frm.doc.div_point_diffuser) / 2) * 2);
		frm.refresh_field("diffuser_cft");

		frm.set_value("ret_in_day_nt",(frm.doc.ret_in_hr_nt/24));
		frm.refresh_field("ret_in_day_nt");
		var ar_val4=(frm.doc.flow*frm.doc.ret_in_day_nt)/frm.doc.tank_height;
		frm.set_value("area_nt",ar_val4);
		frm.refresh_field("area_nt");
		frm.set_value("diffuser_nt",Math.ceil((ar_val4/frm.doc.div_point_diffuser) / 2) * 2);
		frm.refresh_field("diffuser_nt");

		frm.set_value("volume",(frm.doc.ret_in_hr1 * frm.doc.flow)/24);
		frm.refresh_field("volume");
		frm.set_value("area1",(frm.doc.volume/frm.doc.tank_height));
		frm.refresh_field("area1");
		frm.set_value("diffue",frm.doc.no_of_diff/frm.doc.area1);
		frm.refresh_field("diffue");
		frm.set_value("aree",frm.doc.area1/frm.doc.no_of_diff);
		frm.refresh_field("aree");
		frm.set_value("eqtk",Math.ceil(frm.doc.diffuser_eqt / 5) * 5);
		frm.refresh_field("eqtk");
		var to = frm.doc.diffuser_dt + frm.doc.diffuser_srs + frm.doc.diffuser_cft + frm.doc.diffuser_nt;
		frm.set_value("only_air",Math.ceil(to / 5) * 5);
		frm.refresh_field("only_air");
		frm.set_value("bio_tank",frm.doc.no_of_diff);
		frm.refresh_field("bio_tank");
		var cal1 = frm.doc.designing + (frm.doc.only_air*2)
		if(selected_system_array.includes("Rewolutte RO")){
			cal1 = frm.doc.designing + (frm.doc.only_air*2) + (frm.doc.diffuser_rewolutte*2)
		}
		if(frm.doc.seperate_blower_for_equalization_tank==1)
		{
			frm.set_value("blower_cpa",0);
			frm.refresh_field("blower_cpa");
			frm.set_value("each_blower",0);
			frm.refresh_field("each_blower");
			if(frm.doc.is_do_increase == 1)
			{
				frm.set_value("bio_blower",(cal1 + frm.doc.do_increase_blower_capacity)/frm.doc.total_blower);
				frm.refresh_field("bio_blower");
			}
			else
			{
				frm.set_value("bio_blower",(cal1)/frm.doc.total_blower);
				frm.refresh_field("bio_blower");
			}
			frm.set_value("eq_blower",(frm.doc.eqtk * 2));
			frm.refresh_field("eq_blower");
			
			
			// frm.set_value("eqt_blower",Math.ceil(frm.doc.diffuser_eqt / 5) * 5);
			// frm.refresh_field("eqt_blower");
		}
		else
		{
			if(selected_system_array.includes("Rewolutte RO")){
				if(frm.doc.is_do_increase == 1)
				{
					frm.set_value("blower_cpa",frm.doc.designing + (frm.doc.eqtk*2) + (frm.doc.only_air*2) + (frm.doc.diffuser_rewolutte*2) + frm.doc.do_increase_blower_capacity);
					frm.refresh_field("blower_cpa");
				}
				else
				{
					frm.set_value("blower_cpa",frm.doc.designing + (frm.doc.eqtk*2) + (frm.doc.only_air*2) + (frm.doc.diffuser_rewolutte*2));
					frm.refresh_field("blower_cpa");
				}
			}
			else{
				if(frm.doc.is_do_increase == 1)
				{
					frm.set_value("blower_cpa",frm.doc.designing + (frm.doc.eqtk*2) + (frm.doc.only_air*2) + frm.doc.do_increase_blower_capacity);
					frm.refresh_field("blower_cpa");
				}
				else
				{
					frm.set_value("blower_cpa",frm.doc.designing + (frm.doc.eqtk*2) + (frm.doc.only_air*2));
					frm.refresh_field("blower_cpa");
				}				
			}
			frm.set_value("each_blower",frm.doc.blower_cpa/frm.doc.total_blower);
			frm.refresh_field("each_blower");
			frm.set_value("bio_blower",0);
			frm.refresh_field("bio_blower");
			frm.set_value("eq_blower",0);
			frm.refresh_field("eq_blower");
		}
		frm.set_value("total_diffusers",frm.doc.eqtk + frm.doc.only_air + frm.doc.bio_tank);
		if(frm.doc.is_rewolutte==1){
			frm.set_value("total_diffusers",frm.doc.eqtk + frm.doc.only_air + frm.doc.bio_tank+frm.doc.diffuser_rewolutte);
		}
		frm.refresh_field("total_diffusers");
		frm.set_value("influent_flow_rate_to_be_treated",frm.doc.flow*(1+(frm.doc.design_clarifier/100)));
		frm.refresh_field("influent_flow_rate_to_be_treated");
		frm.set_value("influent_flow_rate_to_be_treated_m3hr",frm.doc.influent_flow_rate_to_be_treated/24);
		frm.refresh_field("influent_flow_rate_to_be_treated_m3hr");
		frm.set_value("enter_ras_flow_rate",frm.doc.flow/frm.doc.enter_number_of_clarifiers_in_service);
		frm.refresh_field("enter_ras_flow_rate");
		frm.set_value("ras_flow_rate_per_clarifier",frm.doc.enter_ras_flow_rate/frm.doc.enter_number_of_clarifiers_in_service);
		frm.refresh_field("ras_flow_rate_per_clarifier");
		var clar=frm.doc.influent_flow_rate_to_be_treated_m3hr*frm.doc.required_retention_time_hours;
		var clar1=clar/(Math.PI*frm.doc.enter_side_water_depth);
		var clar2=Math.sqrt(clar1);
		var clar3=clar2*2;
		// var clar4=Math.round(clar3/frm.doc.enter_number_of_clarifiers_in_service,2);
		var clar4 = clar3/frm.doc.enter_number_of_clarifiers_in_service
		frm.set_value("required_clarifier_diameter",clar4);
		frm.refresh_field("required_clarifier_diameter");
		if(frm.doc.required_clarifier_diameter>0 && frm.doc.required_clarifier_diameter<=9)
		{
			frm.set_value("clarifier_diameter",9);
			frm.refresh_field("clarifier_diameter");
		}
		else if(frm.doc.required_clarifier_diameter>9 && frm.doc.required_clarifier_diameter<=10)
		{
			frm.set_value("clarifier_diameter",10);
			frm.refresh_field("clarifier_diameter");
		}
		else if(frm.doc.required_clarifier_diameter>10 && frm.doc.required_clarifier_diameter<=16)
		{
			frm.set_value("clarifier_diameter",16);
			frm.refresh_field("clarifier_diameter");
		}
		else if(frm.doc.required_clarifier_diameter>16 && frm.doc.required_clarifier_diameter<=22)
		{
			frm.set_value("clarifier_diameter",22);
			frm.refresh_field("clarifier_diameter");
		}
		else if(frm.doc.required_clarifier_diameter>22 && frm.doc.required_clarifier_diameter<=30)
		{
			frm.set_value("clarifier_diameter",30);
			frm.refresh_field("clarifier_diameter");
		}
		else
		{
			frm.set_value("clarifier_diameter",0);
			frm.refresh_field("clarifier_diameter");
		}
		frm.set_value("current_retention_time_hours",((Math.PI * frm.doc.clarifier_diameter*frm.doc.clarifier_diameter*frm.doc.enter_side_water_depth)/(4*frm.doc.influent_flow_rate_to_be_treated_m3hr)));
		frm.refresh_field("current_retention_time_hours");
		frm.set_value("ras_flow_rate_percentage",(frm.doc.flow/frm.doc.ras_flow_rate_per_clarifier)*100);
		frm.refresh_field("ras_flow_rate_percentage");
		frm.set_value("calculate_surface_area",Math.PI * Math.pow((frm.doc.clarifier_diameter/2),2));
		frm.refresh_field("calculate_surface_area");
		frm.set_value("calculate_clarifier_volume",frm.doc.calculate_surface_area*frm.doc.enter_side_water_depth);
		frm.refresh_field("calculate_clarifier_volume");
		frm.set_value("weir_diameter",(frm.doc.clarifier_diameter));
		frm.refresh_field("weir_diameter")
		frm.set_value("weir_length",Math.PI * frm.doc.weir_diameter);
		frm.refresh_field("weir_length");
		frm.set_value("total_secondary_clarifier_surface_area",frm.doc.calculate_surface_area*frm.doc.enter_number_of_clarifiers_in_service);
		frm.refresh_field("total_secondary_clarifier_surface_area");
		frm.set_value("total_secondary_clarifier_volume",frm.doc.calculate_clarifier_volume * frm.doc.enter_number_of_clarifiers_in_service);
		frm.refresh_field("total_secondary_clarifier_volume");
		frm.set_value("total_weir_length",frm.doc.weir_length * frm.doc.enter_number_of_clarifiers_in_service);
		frm.refresh_field("total_weir_length");
		frm.set_value("calculated_surface_overflow_rate",frm.doc.influent_flow_rate_to_be_treated/frm.doc.total_secondary_clarifier_surface_area);
		frm.refresh_field("calculated_surface_overflow_rate");
		frm.set_value("calculated_weir_overflow_rate",frm.doc.influent_flow_rate_to_be_treated/frm.doc.total_weir_length);
		frm.refresh_field("calculated_weir_overflow_rate");
		frm.set_value("calculated_detention_time",(frm.doc.total_secondary_clarifier_volume/frm.doc.influent_flow_rate_to_be_treated)*24);
		frm.refresh_field("calculated_detention_time");
		frm.set_value("total_overflow_rate",frm.doc.total_weir_length*frm.doc.calculated_weir_overflow_rate);
		frm.refresh_field("total_overflow_rate");
		frm.set_value("permeate_flow",frm.doc.flow/frm.doc.operating_hours);
		frm.refresh_field("permeate_flow");
		frm.set_value("total_area",(frm.doc.permeate_flow*1000)/frm.doc.permeate_flux);
		frm.refresh_field("total_area");
		frm.set_value("total_modules",frm.doc.total_area/frm.doc.area);
		frm.refresh_field("total_modules");
		var rounded = Math.round(frm.doc.total_modules);
		if(frm.doc.loop_operation=="Single")
		{
			frm.set_value("no_of_loops",1);
			frm.refresh_field("no_of_loops")
			frm.set_value("feed_qty",1);
			frm.refresh_field("feed_qty");
			frm.set_value("bw_qty",1);
			frm.refresh_field("bw_qty");
			frm.set_value("feed_pump",frm.doc.total_modules*frm.doc.mf_for_feed_flow);
			frm.refresh_field("feed_pump");
			frm.set_value("bw_pump",(frm.doc.mf_for_bw_flow * rounded)/frm.doc.bw_qty);
			frm.refresh_field("bw_pump");
			frm.set_value("cip_pump",rounded * frm.doc.mf_for_cip_flow);
			frm.refresh_field("cip_pump");
			frm.set_value("air_flow",rounded * frm.doc.mf_for_air_flow);
			frm.refresh_field("air_flow");
		}
		else
		{
			frm.set_value("no_of_loops",2);
			frm.refresh_field("no_of_loops")
			frm.set_value("feed_qty",2);
			frm.refresh_field("feed_qty");
			frm.set_value("bw_qty",1);
			frm.refresh_field("bw_qty");
			frm.set_value("feed_pump",(rounded * frm.doc.mf_for_feed_flow)/frm.doc.feed_qty);
			frm.refresh_field("feed_pump");
			frm.set_value("bw_pump",(frm.doc.modules_per_loop*frm.doc.mf_for_bw_flow)/frm.doc.bw_qty);
			frm.refresh_field("bw_pump");
			frm.set_value("cip_pump",(rounded * frm.doc.mf_for_cip_flow)/frm.doc.no_of_loops);
			frm.refresh_field("cip_pump");
			frm.set_value("air_flow",(rounded * frm.doc.mf_for_air_flow)/frm.doc.no_of_loops);
			frm.refresh_field("air_flow");
		}
		frm.set_value("modules_per_loop",rounded/frm.doc.no_of_loops);
		frm.refresh_field("modules_per_loop");
		frm.set_value("actual_area",rounded*frm.doc.area);
		frm.refresh_field("actual_area");
		frm.set_value("actual_flux",(frm.doc.permeate_flow *1000)/frm.doc.actual_area);
		frm.refresh_field("actual_flux");
		frm.set_value("mbr_permeate_flow",frm.doc.flow/frm.doc.mbr_operating_hours);
		frm.refresh_field("mbr_permeate_flow");

		if(frm.doc.mbr_type=="SUB-UF")
		{
			frm.set_value("mbr_air_req_membrane_row",15);
			frm.refresh_field("mbr_air_req_membrane_row");
		}
		else
		{
			frm.set_value("mbr_air_req_membrane_row",20);
			frm.refresh_field("mbr_air_req_membrane_row");
		}

		if(frm.doc.mbr_model=="PSH 1800-40")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh40);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh40*40.91;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=23.22 * frm.doc.design_total_no_of_modules;
			var water_volume=18.28 * frm.doc.design_total_no_of_modules;

			var do_mc=21;
			var do_rc=588;
			var do_tak=900;
			var do_mc_rc=145;
			var do_tak1=200;

			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		else if(frm.doc.mbr_model=="PSH 1800-44")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh44);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh44*40.91;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=23.22 * frm.doc.design_total_no_of_modules;
			var water_volume=18.28 * frm.doc.design_total_no_of_modules;

			var do_mc=22;
			var do_rc=706;
			var do_tak=1000;
			var do_mc_rc=175;
			var do_tak1=250;

			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		else if(frm.doc.mbr_model=="PSH 1800-36")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh36);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh36*40.91;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=23.22 * frm.doc.design_total_no_of_modules;
			var water_volume=18.28 * frm.doc.design_total_no_of_modules;

			var do_mc=10;
			var do_rc=446;
			var do_tak=800;
			var do_mc_rc=115;
			var do_tak1=150;

			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		else if(frm.doc.mbr_model=="PSH 660-16")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh16);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh16*41.25;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=12.22 * frm.doc.design_total_no_of_modules;
			var water_volume=10.34 * frm.doc.design_total_no_of_modules;

			var do_mc=4;
			var do_rc=132;
			var do_tak=200;
			var do_mc_rc=33;
			var do_tak1=50;

			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		else if(frm.doc.mbr_model=="PSH 330-8")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh8);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh8*41.25;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=8.30 * frm.doc.design_total_no_of_modules;
			var water_volume=7.29 * frm.doc.design_total_no_of_modules;

			var do_mc=2;
			var do_rc=64;
			var do_tak=100;
			var do_mc_rc=16;
			var do_tak1=25;

			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		else if(frm.doc.mbr_model=="PHF 2650-50")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh50);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh50*53;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=23.37 * frm.doc.design_total_no_of_modules;
			var water_volume=18.29 * frm.doc.design_total_no_of_modules;

			var do_mc=0;
			var do_rc=0;
			var do_tak=0;
			var do_mc_rc=0;
			var do_tak1=0;

			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		else if(frm.doc.mbr_model=="PHF 2650-46")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh46);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh46*53;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=23.37 * frm.doc.design_total_no_of_modules;
			var water_volume=18.29 * frm.doc.design_total_no_of_modules;

			var do_mc=0;
			var do_rc=0;
			var do_tak=0;
			var do_mc_rc=0;
			var do_tak1=0;
			
			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		else if(frm.doc.mbr_model=="PHF 2650-42")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh42);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh42*53;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=23.37 * frm.doc.design_total_no_of_modules;
			var water_volume=18.29 * frm.doc.design_total_no_of_modules;

			var do_mc=0;
			var do_rc=0;
			var do_tak=0;
			var do_mc_rc=0;
			var do_tak1=0;

			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		else if(frm.doc.mbr_model=="PHF 2650-38")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh38);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh38*53;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=23.37 * frm.doc.design_total_no_of_modules;
			var water_volume=18.29 * frm.doc.design_total_no_of_modules;

			var do_mc=0;
			var do_rc=0;
			var do_tak=0;
			var do_mc_rc=0;
			var do_tak1=0;

			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		else if(frm.doc.mbr_model=="PHF 960-18")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh18);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh18*53.33;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=12.20 * frm.doc.design_total_no_of_modules;
			var water_volume=10.33 * frm.doc.design_total_no_of_modules;

			var do_mc=0;
			var do_rc=0;
			var do_tak=0;
			var do_mc_rc=0;
			var do_tak1=0;

			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		else if(frm.doc.mbr_model=="PHF 480-9")
		{
			frm.set_value("mbr_membrane_modules",frm.doc.psh9);
			frm.refresh_field("mbr_membrane_modules");
			var toarea=frm.doc.psh9*53.33;
			frm.set_value("mbr_total_area",toarea);
			frm.refresh_field("mbr_total_area");
			var tank_volume=8.28 * frm.doc.design_total_no_of_modules;
			var water_volume=7.28 * frm.doc.design_total_no_of_modules;

			var do_mc=0;
			var do_rc=0;
			var do_tak=0;
			var do_mc_rc=0;
			var do_tak1=0;

			frm.set_value("mbr_tank_volume",water_volume);
			frm.refresh_field("mbr_tank_volume");
		}
		frm.set_value("mbr_area_req_for_filtration",(frm.doc.mbr_permeate_flow*1000)/frm.doc.mbr_permeate_flux);
		frm.refresh_field("mbr_area_req_for_filtration");
		frm.set_value("design_no_module_required",frm.doc.mbr_area_req_for_filtration/frm.doc.mbr_total_area);
		frm.refresh_field("design_no_module_required");
		frm.set_value("design_total_no_of_modules",Math.round(frm.doc.mbr_area_req_for_filtration/frm.doc.mbr_total_area));
		frm.refresh_field("design_total_no_of_modules");
		frm.set_value("design_modules_train",frm.doc.design_total_no_of_modules/frm.doc.design_no_of_trains);
		frm.refresh_field("design_modules_train");
		frm.set_value("design_total_area",frm.doc.mbr_total_area*frm.doc.design_total_no_of_modules);
		frm.refresh_field("design_total_area");
		frm.set_value("mbr_permeate_pump",(frm.doc.mbr_permeate_flow*1.05)/frm.doc.design_no_of_trains);
		frm.refresh_field("mbr_permeate_pump");
		frm.set_value("mbr_backwash_pump",(frm.doc.mbr_backwash_flux*frm.doc.design_total_area)/(frm.doc.design_no_of_trains*1000));
		frm.refresh_field("mbr_backwash_pump");
		if(frm.doc.design_modules_train<=3)
		{
			frm.set_value("blower_pump_qty",1);
			frm.refresh_field("blower_pump_qty");
		}
		else
		{
			frm.set_value("blower_pump_qty",(frm.doc.design_modules_train/2));
			frm.refresh_field("blower_pump_qty");
		}
		if(frm.doc.mbr_model=="PSH 1800-44")
		{
			frm.set_value("total_filtration_area",1800*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PSH 1800-40")
		{
			frm.set_value("total_filtration_area",1636.36*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PSH 1800-36")
		{
			frm.set_value("total_filtration_area",1472.7*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PSH 660-16")
		{
			frm.set_value("total_filtration_area",660*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PSH 330-8")
		{
			frm.set_value("total_filtration_area",330*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PHF 2650-50")
		{
			frm.set_value("total_filtration_area",2650*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PHF 2650-46")
		{
			frm.set_value("total_filtration_area",2438*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PHF 2650-42")
		{
			frm.set_value("total_filtration_area",2226*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PHF 2650-38")
		{
			frm.set_value("total_filtration_area",2014*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PHF 960-18")
		{
			frm.set_value("total_filtration_area",960*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PHF 960-18")
		{
			frm.set_value("total_filtration_area",960*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PHF 960-18")
		{
			frm.set_value("total_filtration_area",960*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}
		else if(frm.doc.mbr_model=="PHF 480-9")
		{
			frm.set_value("total_filtration_area",480*frm.doc.design_total_no_of_modules);
			frm.refresh_field("total_filtration_area");
		}

		frm.set_value("required_flux",(frm.doc.mbr_permeate_flow*1000)/frm.doc.total_filtration_area);
		frm.refresh_field("required_flux");

		if(frm.doc.sludge_pit=="Required")
		{
			var exact_time=60;
		}
		else
		{
			var exact_time=20;
		}
		var slud = (water_volume / frm.doc.design_no_of_trains) * (60/exact_time);
		var cirt = ((frm.doc.flow * 4)/24)/ (frm.doc.design_no_of_trains);
		var sqty = (frm.doc.design_no_of_trains/2)
		if (frm.doc.design_no_of_trains<=3){
			sqty = 1
		} 
		if(frm.doc.mbr_type=="SUB-UF")
		{
			frm.set_value("mbr_sludge_pump",Math.ceil((slud) / 10) * 10);
			frm.set_value("mbr_circulation_pump",0);
			frm.set_value("mbr_sludge_pump_qty",sqty);
		}
		else
		{
			frm.set_value("mbr_sludge_pump",0);
			frm.set_value("mbr_circulation_pump",cirt);
			frm.set_value("mbr_sludge_pump_qty",0);
		}
		if(frm.doc.mbr_type=="SUB-UF")
		{
			frm.set_value("circulation_pump_store_standby_qty",0);
			frm.refresh_field("circulation_pump_store_standby_qty");
		}
		else
		{
			frm.set_value("circulation_pump_store_standby_qty",1);
			frm.refresh_field("circulation_pump_store_standby_qty");
		}
		if(frm.doc.mbr_type=="SUB-UF")
		{
			var fd_value = (frm.doc.flow/(24*0.9))/frm.doc.design_no_of_trains;
			frm.set_value("mbr_feed_pump",fd_value);
		}
		else
		{
			var fd_value = (frm.doc.flow*5/24)/frm.doc.design_no_of_trains;
			frm.set_value("mbr_feed_pump",fd_value);
		}
		var cip_train = ((frm.doc.mbr_cip_flux * frm.doc.design_total_area)/(frm.doc.design_no_of_trains * 1000))/frm.doc.design_no_of_trains;
		frm.set_value("mbr_cip_pump__train",cip_train);
		var brain=(frm.doc.mbr_air_req_membrane_row * frm.doc.mbr_membrane_modules * frm.doc.design_total_no_of_modules)/(frm.doc.design_no_of_trains*frm.doc.blower_pump_qty);
		if(frm.doc.design_no_of_trains>3){
			brain=(frm.doc.mbr_air_req_membrane_row * frm.doc.mbr_membrane_modules * frm.doc.design_total_no_of_modules)/(frm.doc.design_no_of_trains);
		}
		frm.set_value("mbr_blower__train",brain);
		frm.refresh_field("mbr_blower__train");

		frm.set_value("normal_flow",frm.doc.mbr_blower__train/3600);
		frm.refresh_field("normal_flow");
		frm.set_value("p_actual",frm.doc.ambient_pressure + frm.doc.measured_pressure);
		frm.refresh_field("p_actual");
		var at_flow=frm.doc.normal_flow * (frm.doc.ambient_pressure/frm.doc.p_actual) * ((frm.doc.normal_temp + (frm.doc.normal_temp +frm.doc.room_temp))/frm.doc.normal_temp);
		frm.set_value("actual_flow",at_flow);
		frm.refresh_field("actual_flow");
		frm.set_value("mbr_blower__train1",frm.doc.actual_flow *3600);
		frm.refresh_field("mbr_blower__train1");
		var cip=Math.max((frm.doc.flow * (0.7/100)),(frm.doc.mbr_cip_pump__train * 45/60)*1000);
		frm.set_value("cip_tank",cip);
		frm.refresh_field("cip_tank");
		frm.set_value("dosing_pump_mc",do_mc*frm.doc.design_modules_train);
		frm.refresh_field("dosing_pump_mc");
		frm.set_value("dosing_pump_rc",do_rc*frm.doc.design_modules_train);
		frm.refresh_field("dosing_pump_rc");
		frm.set_value("dosing_tank",do_tak*frm.doc.design_modules_train);
		frm.refresh_field("dosing_tank");
		frm.set_value("citric_dosing_pump_mc_and_rc",do_mc_rc*frm.doc.design_modules_train);
		frm.refresh_field("citric_dosing_pump_mc_and_rc");
		frm.set_value("citric_dosing_tank",do_tak1*frm.doc.design_modules_train);
		frm.refresh_field("citric_dosing_tank");

		frm.set_value("bcod",1.6*frm.doc.bod);
		frm.refresh_field("bcod");
		var a=(frm.doc.flow)*(frm.doc.y)*(frm.doc.bod);
		var b=(frm.doc.fd)*(frm.doc.kd)*(frm.doc.ret_in_hr1);
		var c=(frm.doc.kd*frm.doc.ret_in_hr1);
		var fin=(a*(1+b))/(0.85*(1+c));
		var divfin=fin/1000;
		var ras_cal = ((frm.doc.flow*(frm.doc.mlss-frm.doc.tss))-(divfin*1000))/(frm.doc.tss_cf_waste-frm.doc.mlss)
		var was_cal = (frm.doc.flow*(frm.doc.tss-frm.doc.tss_cf_eff)+(divfin*1000))/(frm.doc.tss_cf_waste-frm.doc.tss_cf_eff)

		frm.set_value("sludge_pro",fin);
		frm.refresh_field("sludge_pro");

		frm.set_value("ras",ras_cal);
		frm.refresh_field("ras");

		frm.set_value("was",was_cal);
		frm.refresh_field("was");

		frm.set_value("without_mechanism",(frm.doc.was/20));
		var s=(8000*frm.doc.was)/1000;
		var t=(s*1000)/15000;
		frm.set_value("with_mechanism",(t/20));
		frm.refresh_field("with_mechanism");

		frm.set_value("pump_qty",frm.doc.design_no_of_trains);
		frm.refresh_field("pump_qty");

		frm.set_value("circulation_pump_qty",frm.doc.design_no_of_trains);
		frm.refresh_field("circulation_pump_qty");

		frm.set_value("feed_pump_qty",frm.doc.design_modules_train);
		frm.refresh_field("feed_pump_qty");

		

		//MBR OVIVO 

		frm.set_value("ovivo_permeate_flow_rate",(frm.doc.flow/frm.doc.ovivo_operating_hours));
		frm.refresh_field("ovivo_permeate_flow_rate");

		frm.set_value("ovivo_permeate_flow_rate",(frm.doc.flow/frm.doc.ovivo_operating_hours));
		frm.refresh_field("ovivo_permeate_flow_rate");

		frm.set_value("ovivo_area_required_for_filtration",(frm.doc.ovivo_permeate_flow_rate/frm.doc.ovivo_permeate_flux_lmh)*1000);
		frm.refresh_field("ovivo_area_required_for_filtration");

		frm.set_value("ovivo_permeate_flux_lmd",frm.doc.ovivo_permeate_flux_lmh*frm.doc.ovivo_operating_hours);
		frm.refresh_field("ovivo_permeate_flux_lmd");

		frm.set_value("ovivo_backwash_flux",frm.doc.ovivo_permeate_flux_lmh*2.3);
		frm.refresh_field("ovivo_backwash_flux");

		frm.set_value("ovivo_cip_flux",frm.doc.ovivo_permeate_flux_lmh*1.25);
		frm.refresh_field("ovivo_cip_flux");

		frm.set_value("ovivo_cip_flux",frm.doc.ovivo_permeate_flux_lmh*1.25);
		frm.refresh_field("ovivo_cip_flux");

		frm.set_value("ovivo_permeate_qty",frm.doc.ovivo_no_of_trains);
		frm.refresh_field("ovivo_permeate_qty");

		if(frm.doc.ovivo_no_of_trains<=3)
		{
			frm.set_value("ovivo_backwash_qty",1);
			frm.refresh_field("ovivo_backwash_qty");
		}
		else
		{
			var ovback = frm.doc.ovivo_no_of_trains/2
			frm.set_value("ovivo_backwash_qty",Math.ceil(ovback / 1) * 1);
			frm.refresh_field("ovivo_backwash_qty");
		}

		if(frm.doc.ovivo_type=="S-MBR")
		{
			frm.set_value("ovivo_circulation_qty",frm.doc.ovivo_no_of_trains);
			frm.refresh_field("ovivo_circulation_qty");
			frm.set_value("ovivo_circulation_sqty",1);
			frm.refresh_field("ovivo_circulation_sqty");
		}
		else
		{
			frm.set_value("ovivo_circulation_qty",0);
			frm.refresh_field("ovivo_circulation_qty");
			frm.set_value("ovivo_circulation_sqty",0);
			frm.refresh_field("ovivo_circulation_sqty");
		}

		if(frm.doc.ovivo_type=="S-MBR")
		{
			frm.set_value("ovivo_cip_qty",frm.doc.ovivo_no_of_trains);
			frm.refresh_field("ovivo_cip_qty");
		}
		else
		{
			frm.set_value("ovivo_cip_qty",0);
			frm.refresh_field("ovivo_cip_qty");
		}
		if(frm.doc.feed_pump_required_for_ovivo==1)
		{
			frm.set_value("ovivo_feed_qty",frm.doc.ovivo_no_of_trains);
			frm.refresh_field("ovivo_feed_qty");
		}
		else
		{
			frm.set_value("ovivo_feed_qty",0);
			frm.refresh_field("ovivo_feed_qty");
		}

		if(frm.doc.ovivo_type=="S-UF")
		{
			if(frm.doc.ovivo_no_of_trains<=3)
			{
				frm.set_value("ovivo_blower_qty",1);
				frm.refresh_field("ovivo_blower_qty");
			}
			else
			{
				frm.set_value("ovivo_blower_qty",(frm.doc.ovivo_no_of_trains/2));
				frm.refresh_field("ovivo_blower_qty");	
			}
		}
		else
		{
			frm.set_value("ovivo_blower_qty",frm.doc.ovivo_no_of_trains);
			frm.refresh_field("ovivo_blower_qty");
		}

		if(frm.doc.ovivo_no_of_trains<=3)
		{
			frm.set_value("ovivo_sprinkler_qty",1);
			frm.refresh_field("ovivo_sprinkler_qty");
		}
		else
		{
			var ovspr = frm.doc.ovivo_no_of_trains/2;
			frm.set_value("ovivo_sprinkler_qty",Math.ceil(ovspr / 1) * 1);
			frm.refresh_field("ovivo_sprinkler_qty");
		}

		if(frm.doc.ovivo_no_of_trains<=3)
		{
			frm.set_value("ovivo_sludge_qty",1);
			frm.refresh_field("ovivo_sludge_qty");
		}
		else
		{
			frm.set_value("ovivo_sludge_qty",(frm.doc.ovivo_no_of_trains/2));
			frm.refresh_field("ovivo_sludge_qty");
		}

		var no_mb=Math.round((frm.doc.ovivo_area_required_for_filtration/frm.doc.ovivo_area_per_module) * 10.0) / 10.0
		frm.set_value("ovivo_no_module_required",no_mb)

		frm.set_value("ovivo_no_of_stacks_required",frm.doc.ovivo_no_module_required/frm.doc.ovivo_no_of_module_per_stack);
		frm.refresh_field("ovivo_no_of_stacks_required");

		frm.set_value("ovivo_modules_train",frm.doc.ovivo_no_of_stacks_required/frm.doc.ovivo_no_of_trains);
		frm.refresh_field("ovivo_modules_train");

		frm.set_value("ovivo_permeate_pump",(frm.doc.ovivo_permeate_flow_rate*1.15)/frm.doc.ovivo_permeate_qty);
		frm.refresh_field("ovivo_permeate_pump");

		frm.set_value("ovivo_no_of_module_per_train",frm.doc.ovivo_no_of_stacks_required/frm.doc.ovivo_no_of_trains);
		frm.refresh_field("ovivo_no_of_module_per_train");

		frm.set_value("ovivo_total_area",Math.ceil((frm.doc.ovivo_no_module_required/1)*1)*frm.doc.ovivo_area_per_module);
		frm.refresh_field("ovivo_total_area");

		frm.set_value("ovivo_required_flux",(frm.doc.ovivo_permeate_flow_rate*1000)/frm.doc.ovivo_total_area);
		frm.refresh_field("ovivo_required_flux");

		frm.set_value("ovivo_circulation_pump",((frm.doc.flow)*5)/(24*frm.doc.ovivo_no_of_trains));
		frm.refresh_field("ovivo_circulation_pump");

		frm.set_value("ovivo_blower",(frm.doc.ovivo_air_flow_rate_per_stack*frm.doc.ovivo_no_of_stacks_required)/frm.doc.ovivo_no_of_trains);
		frm.refresh_field("ovivo_blower");

		frm.set_value("ovivo_sprinkler_pump",(12*frm.doc.ovivo_no_of_stacks_required)/frm.doc.ovivo_no_of_trains);
		frm.refresh_field("ovivo_sprinkler_pump");
		var cip_cal = (frm.doc.ovivo_backwash_flux*frm.doc.ovivo_area_required_for_filtration*frm.doc.ovivo_modules_train)/(frm.doc.ovivo_no_of_stacks_required*1000)
		frm.set_value("ovivo_bc",(cip_cal));
		frm.refresh_field("ovivo_bc");

		frm.set_value("ovivo_cip",(cip_cal*frm.doc.cip_flow_conversion));
		frm.refresh_field("ovivo_cip");
		frm.set_value("ovivo_feed_pump",(frm.doc.ovivo_permeate_pump*frm.doc.feed_flow_conversion));
		frm.refresh_field("ovivo_feed_pump");

		var mo_height = ((0.16 * frm.doc.ovivo_no_of_module_per_stack) +0.534);
		var with_f_b1 = mo_height + 0.3 + 0.5;
		var with_f_b2 = (0.72 * frm.doc.ovivo_modules_train)+(0.15 * (frm.doc.ovivo_modules_train+1));
		var with_f_b3 = (0.57 * 1)+0.3;
		var total_vol = with_f_b1 * with_f_b2 * with_f_b3;
		frm.set_value("ovivo_tank_volume",total_vol);
		frm.refresh_field("ovivo_tank_volume");

		// frm.set_value("ovivo_sludge_pump",(frm.doc.ovivo_tank_volume/5)*60);
		// frm.refresh_field("ovivo_sludge_pump");


		frm.set_value("ovivo_sludge_pump",(0.7084 * frm.doc.ovivo_no_of_stacks_required * 8 * frm.doc.ovivo_no_of_trains * ((0.16 * frm.doc.ovivo_no_of_module_per_stack) + 0.72))/frm.doc.ovivo_sludge_pump_hours_of_operation);
		frm.refresh_field("ovivo_sludge_pump");

		frm.set_value("ovivo_total_cycle",60/(frm.doc.ovivo_filtration_min + frm.doc.ovivo_backwash_min));
		frm.refresh_field("ovivo_total_cycle");

		frm.set_value("ovivo_hours_of_operation",frm.doc.ovivo_operating_hours);
		frm.refresh_field("ovivo_hours_of_operation");

		frm.set_value("ovivo_filtration_hr",(frm.doc.ovivo_filtration_min * frm.doc.ovivo_total_cycle * frm.doc.ovivo_hours_of_operation)/60);
		frm.refresh_field("ovivo_filtration_hr");

		frm.set_value("ovivo_backwash_hr",(frm.doc.ovivo_backwash_min * frm.doc.ovivo_total_cycle * frm.doc.ovivo_hours_of_operation)/60);
		frm.refresh_field("ovivo_backwash_hr");

		frm.set_value("ovivo_permeate_m3",(frm.doc.ovivo_filtration_hr * frm.doc.ovivo_permeate_pump * frm.doc.ovivo_no_of_trains));
		frm.refresh_field("ovivo_permeate_m3");

		frm.set_value("ovivo_backwash_m3",(frm.doc.ovivo_backwash_hr * frm.doc.ovivo_bc * frm.doc.ovivo_no_of_trains));
		frm.refresh_field("ovivo_backwash_m3");

		frm.set_value("ovivo_total_permeate",frm.doc.ovivo_permeate_m3 - frm.doc.ovivo_backwash_m3);
		frm.refresh_field("ovivo_total_permeate");

		var vs=(6*frm.doc.ovivo_area_per_module * frm.doc.ovivo_no_module_required)/frm.doc.ovivo_no_of_trains;
		frm.set_value("cip_tank_per_train",(vs * frm.doc.ovivo_no_of_stacks_required)/frm.doc.ovivo_no_of_trains);
		frm.refresh_field("cip_tank_per_train");


		var dp = frm.doc.ovivo_chlorine_dosing_for_each_stack * frm.doc.ovivo_no_of_module_per_train * frm.doc.ovivo_no_of_module_per_stack * frm.doc.ovivo_area_per_module;
		var dp1 = dp * (frm.doc.hypo_cleaning_concentration/100) * 3600;
		var dp2 = dp1 / 100;


		frm.set_value("naocl_dosing_pump_rc",dp2);
		frm.refresh_field("naocl_dosing_pump_rc");

		var dp = frm.doc.ovivo_citric_dosing_for_each_stack * frm.doc.ovivo_no_of_module_per_train * frm.doc.ovivo_no_of_module_per_stack * frm.doc.ovivo_area_per_module;
		var dp1 = dp * (frm.doc.ovivo_hcl_cleaning_cencentration/100) * 3600;
		var dp2 = dp1 / 100;


		frm.set_value("citric_dosing_pump_mc_rc",dp2);
		frm.refresh_field("citric_dosing_pump_mc_rc");

		frm.set_value("hcl_dosing_pump_mc_rc",(frm.doc.ovivo_hcl_dosing_for_each_stack * frm.doc.flow) /  (1000*frm.doc.ovivo_operating_hours));
		frm.refresh_field("hcl_dosing_pump_mc_rc");

		frm.set_value("alum_dosing_pump_mc_rc",(frm.doc.ovivo_alum_dosing_for_each_stack * frm.doc.flow) / (1000*frm.doc.ovivo_operating_hours));
		frm.refresh_field("alum_dosing_pump_mc_rc");

		frm.set_value("ovivo_permeate_capacity",frm.doc.ovivo_permeate_pump*frm.doc.ovivo_permeate_qty*frm.doc.ovivo_filtration_hr);
		frm.refresh_field("ovivo_permeate_capacity");

		//ott calculation

		var ott_total_area=(frm.doc.flow*(frm.doc.ret_in_hr1/24))/frm.doc.tank_height;
		var ott_each_tank = ott_total_area/frm.doc.no_of_bio_tanks;
		if(ott_each_tank<=506.25)
		{
			var power_factor = 2
		} 
		else if(ott_each_tank>506.25 && ott_each_tank<=1012.5)
		{
			var power_factor = 3
		}
		else
		{
			var power_factor = 1
		}
		var length_of_tank = Math.pow(ott_each_tank,(1/power_factor));
		var width_of_tank = ott_each_tank/length_of_tank;
		var act_length =  length_of_tank - (0.15+0.1+0.05)
		var lat_no=0;
		frm.set_value("tank_length",length_of_tank);
		frm.refresh_field("tank_length");
		if(act_length<3.86)
		{
			lat_no=1;
		}
		else if(act_length<5.675)
		{
			lat_no=2;
		}
		else if(act_length<7.49)
		{
			lat_no=3;
		}
		else if(act_length<9.305)
		{
			lat_no=4;
		}
		else if(act_length<11.12)
		{
			lat_no=5;
		}
		else if(act_length<12.935)
		{
			lat_no=6;
		}
		else if(act_length<14.75)
		{
			lat_no=7;
		}
		else if(act_length<16.565)
		{
			lat_no=8;
		}
		else if(act_length<18.38)
		{
			lat_no=9;
		}
		else if(act_length<20.195)
		{
			lat_no=10;
		}
		else if(act_length<22.01)
		{
			lat_no=11;
		}
		else if(act_length<22.5)
		{
			lat_no=12;
		}
		else
		{
			lat_no=0;
		}
		var no_of_ott=(width_of_tank/frm.doc.diffuser_spacing);
		var total_no_of_ott=(no_of_ott*frm.doc.no_of_bio_tanks);
		// var tt_no_ott=Math.ceil(total_no_of_ott / 5) * 5;
		// var tt_no_ott1=(frm.doc.total_diffusers*2)/6;
		// var finalott=Math.max(total_no_of_ott, tt_no_ott1)
		// var finalott = tt_no_ott
		frm.set_value("ott_laterals",total_no_of_ott);
		frm.refresh_field("ott_laterals");
		frm.set_value("ott_lateral_size",lat_no);
		frm.refresh_field("ott_lateral_size");

		var a_f = frm.doc.blower_cpa;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000

		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("n_s_blower_size",ff);
		frm.refresh_field("n_s_blower_size");
		if(frm.doc.blower_cpa!=0)
		{
			frm.set_value("ns_blower_length",10);
			frm.refresh_field("ns_blower_length");
		}
		else
		{
			frm.set_value("ns_blower_length",0);
			frm.refresh_field("ns_blower_length");
		}


		var a_f = frm.doc.blower_cpa/frm.doc.no_of_bio_tanks;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000

		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("b_bio_size",ff);
		frm.refresh_field("b_bio_size");
		frm.set_value("b_bio_length",((width_of_tank+frm.doc.tank_height+0.5)*frm.doc.no_of_bio_tanks));
		frm.refresh_field("b_bio_length");

		if(frm.doc.seperate_blower_for_equalization_tank!=0)
		{
		var a_f = frm.doc.eq_blower;
		var m_v = 20;	
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000
		if(f2>=0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("s_blower_size",ff);
		frm.refresh_field("s_blower_size");
		frm.set_value("s_blower_length",10);
		frm.refresh_field("s_blower_length");


		var a_f = frm.doc.bio_blower/frm.doc.no_of_bio_tanks;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000

		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("b_bio_size",ff);
		frm.refresh_field("b_bio_size");
		frm.set_value("b_bio_length",((width_of_tank+frm.doc.tank_height+0.5)*frm.doc.no_of_bio_tanks));
		frm.refresh_field("b_bio_length");
		}
		else
		{
			frm.set_value("s_blower_size",0);
			frm.refresh_field("s_blower_size");
			frm.set_value("s_blower_length",0);
			frm.refresh_field("s_blower_length");
		}


		//eqt
		var a_f = frm.doc.eqtk*2;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000

		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("e_bio_size",ff);
		frm.refresh_field("e_bio_size");
		frm.set_value("e_bio_float",(length_of_tank+frm.doc.tank_height+10));
		frm.refresh_field("e_bio_float");

		// rewolutte branch pipes and header pipe calculation 
		if(selected_system_array.includes("Rewolutte RO")){
			var a_f = frm.doc.diffuser_rewolutte*2;
			var m_v = 20;	
			var f0 = m_v * 3600
			var f1=a_f/f0
			var f2=Math.sqrt((4*f1)/Math.PI)*1000
			if(f2>=0 && f2<6.99)
			{
				var ff="DN6"
				var ff1=Math.abs(f2-6.99);
			}
			else if(f2>6.99 && f2<10.42)
			{
				var ff="DN8";
				var ff1=Math.abs(f2-10.42);	
			}
			else if(f2>10.42 && f2<13.85)
			{
				var ff="DN10";
				var ff1=Math.abs(f2-13.85);
			}
			else if(f2>13.85 && f2<18.04)
			{
				var ff="DN15";
				var ff1=Math.abs(f2-18.04);
			}
			else if(f2>18.04 && f2<23.37)
			{
				var ff="DN20";
				var ff1=Math.abs(f2-23.37);
			}
			else if(f2>23.37 && f2<30.1)
			{
				var ff="DN25";
				var ff1=Math.abs(f2-30.1);
			}
			else if(f2>30.1 && f2<38.86)
			{
				var ff="DN32";
				var ff1=Math.abs(f2-38.86);
			}
			else if(f2>38.86 && f2<44.96)
			{
				var ff="DN40";
				var ff1=Math.abs(f2-44.96);
			}
			else if(f2>44.96 && f2<57.08)
			{
				var ff="DN50";
				var ff1=Math.abs(f2-57.08);
			}
			else if(f2>57.08 && f2<68.81)
			{
				var ff="DN65";
				var ff1=Math.abs(f2-68.81);
			}
			else if(f2>68.81 && f2<84.68)
			{
				var ff="DN80";
				var ff1=Math.abs(f2-84.68);
			}
			else if(f2>84.68 && f2<110.08)
			{
				var ff="DN100";
				var ff1=Math.abs(f2-110.08);
			}
			else if(f2>110.08 && f2<135.76)
			{
				var ff="DN125";
				var ff1=Math.abs(f2-135.76);
			}
			else if(f2>135.76 && f2<162.72)
			{
				var ff="DN150";
				var ff1=Math.abs(f2-162.72);
			}
			else if(f2>162.72 && f2<213.54)
			{
				var ff="DN200";
				var ff1=Math.abs(f2-213.54);
			}
			else if(f2>213.54 && f2<266.25)
			{
				var ff="DN250";
				var ff1=Math.abs(f2-266.25);
			}
			else if(f2>266.25 && f2<315.93)
			{
				var ff="DN300";
				var ff1=Math.abs(f2-315.93);
			}
			else if(f2>315.93 && f2<347.68)
			{
				var ff="DN350";
				var ff1=Math.abs(f2-347.68);
			}
			else if(f2>347.68 && f2<398.02)
			{
				var ff="DN400";
				var ff1=Math.abs(f2-398.02);
			}
			else if(f2>398.02 && f2<448.62)
			{
				var ff="DN450";
				var ff1=Math.abs(f2-448.62);
			}
			else if(f2>448.62 && f2<498.44)
			{
				var ff="DN500";
				var ff1=Math.abs(f2-498.44);
			}
			else if(f2>498.44 && f2<549.44)
			{
				var ff="DN550";
				var ff1=Math.abs(f2-549.44);
			}
			else if(f2>549.44 && f2<598.92)
			{
				var ff="DN600";
				var ff1=Math.abs(f2-598.92);
			}
			else if(f2>598.92 && f2<749.3)
			{
				var ff="DN750";
				var ff1=Math.abs(f2-749.3);
			}
			frm.set_value("rewolutte_header_pipe_size",ff);
			frm.refresh_field("rewolutte_header_pipe_size");
			frm.set_value("rewolutte_header_pipe_length",frm.doc.tank_length+frm.doc.tank_height+20);
			frm.refresh_field("rewolutte_header_pipe_length");
			// branch pipe
			var a_f = frm.doc.diffuser_rewolutte*2;
			var m_v = 20;
			var f0 = m_v * 3600
			var f1=a_f/f0
			var f2=Math.sqrt((4*f1)/Math.PI)*1000

			if(f2>0 && f2<6.99)
			{
				var ff="DN6"
				var ff1=Math.abs(f2-6.99);
			}
			else if(f2>6.99 && f2<10.42)
			{
				var ff="DN8";
				var ff1=Math.abs(f2-10.42);	
			}
			else if(f2>10.42 && f2<13.85)
			{
				var ff="DN10";
				var ff1=Math.abs(f2-13.85);
			}
			else if(f2>13.85 && f2<18.04)
			{
				var ff="DN15";
				var ff1=Math.abs(f2-18.04);
			}
			else if(f2>18.04 && f2<23.37)
			{
				var ff="DN20";
				var ff1=Math.abs(f2-23.37);
			}
			else if(f2>23.37 && f2<30.1)
			{
				var ff="DN25";
				var ff1=Math.abs(f2-30.1);
			}
			else if(f2>30.1 && f2<38.86)
			{
				var ff="DN32";
				var ff1=Math.abs(f2-38.86);
			}
			else if(f2>38.86 && f2<44.96)
			{
				var ff="DN40";
				var ff1=Math.abs(f2-44.96);
			}
			else if(f2>44.96 && f2<57.08)
			{
				var ff="DN50";
				var ff1=Math.abs(f2-57.08);
			}
			else if(f2>57.08 && f2<68.81)
			{
				var ff="DN65";
				var ff1=Math.abs(f2-68.81);
			}
			else if(f2>68.81 && f2<84.68)
			{
				var ff="DN80";
				var ff1=Math.abs(f2-84.68);
			}
			else if(f2>84.68 && f2<110.08)
			{
				var ff="DN100";
				var ff1=Math.abs(f2-110.08);
			}
			else if(f2>110.08 && f2<135.76)
			{
				var ff="DN125";
				var ff1=Math.abs(f2-135.76);
			}
			else if(f2>135.76 && f2<162.72)
			{
				var ff="DN150";
				var ff1=Math.abs(f2-162.72);
			}
			else if(f2>162.72 && f2<213.54)
			{
				var ff="DN200";
				var ff1=Math.abs(f2-213.54);
			}
			else if(f2>213.54 && f2<266.25)
			{
				var ff="DN250";
				var ff1=Math.abs(f2-266.25);
			}
			else if(f2>266.25 && f2<315.93)
			{
				var ff="DN300";
				var ff1=Math.abs(f2-315.93);
			}
			else if(f2>315.93 && f2<347.68)
			{
				var ff="DN350";
				var ff1=Math.abs(f2-347.68);
			}
			else if(f2>347.68 && f2<398.02)
			{
				var ff="DN400";
				var ff1=Math.abs(f2-398.02);
			}
			else if(f2>398.02 && f2<448.62)
			{
				var ff="DN450";
				var ff1=Math.abs(f2-448.62);
			}
			else if(f2>448.62 && f2<498.44)
			{
				var ff="DN500";
				var ff1=Math.abs(f2-498.44);
			}
			else if(f2>498.44 && f2<549.44)
			{
				var ff="DN550";
				var ff1=Math.abs(f2-549.44);
			}
			else if(f2>549.44 && f2<598.92)
			{
				var ff="DN600";
				var ff1=Math.abs(f2-598.92);
			}
			else if(f2>598.92 && f2<749.3)
			{
				var ff="DN750";
				var ff1=Math.abs(f2-749.3);
			}
			frm.set_value("rewolutte_branch_pipe_size",ff);
			frm.refresh_field("rewolutte_branch_pipe_size");
			frm.set_value("rewolutte_branch_pipe_length",(length_of_tank+10));
			frm.refresh_field("rewolutte_branch_pipe_length");
		}

		//rewolutte diffuser grid pipe size
		var sizearea = ((frm.doc.flow*(1+(1-(frm.doc.rewolutte_ro_recovery/100))) / frm.doc.tank_height) / frm.doc.tank_length);
		var sizearea1 = (frm.doc.diffuser_rewolutte * 2) / sizearea;
		var a_f = sizearea1;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000
		if(f2>0 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("rewolutte_grid_pipe_size",ff);
		frm.refresh_field("rewolutte_grid_pipe_size");

		//air
		var a_f = frm.doc.only_air*2;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000

		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("nsc_blower_line_size",ff);
		frm.refresh_field("nsc_blower_line_size");
		frm.set_value("nsc_blower_line_length",(20+frm.doc.tank_height)*3);
		frm.refresh_field("nsc_blower_line_length");

		var re = frm.doc.flow * (frm.doc.reject_flow/100)
		var re1 = re * (1 + (frm.doc.chemical_volume/100))
		frm.set_value("cts_capacity",re1)
		frm.refresh_field("cts_capacity");

		frm.set_value("do_increase_cod",frm.doc.cod * (1-(frm.doc.cod_dec/100)));
		frm.refresh_field("do_increase_cod");

		frm.set_value("do_increase_bod",frm.doc.bod_value * (1-(frm.doc.cod_dec/100)));
		frm.refresh_field("do_increase_bod");

		frm.set_value("sote",((frm.doc.do_increase_bod/frm.doc.soft_per)*100));
		frm.refresh_field("sote");
		frm.set_value("reject_ro_flow_rate",(frm.doc.cts_capacity/frm.doc.hours_of_operations));
		frm.refresh_field("reject_ro_flow_rate");

		//nt_pipe_size
		var a_f = frm.doc.diffuser_nt * 2;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000

		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		// frm.set_value("nt_pipe_size",ff);
		// frm.refresh_field("nt_pipe_size");
		// frm.set_value("nt_pipe_length",10);//nt diffuser pipe length
		frm.set_value("nt_pipe_length",frm.doc.tank_height+2+2);//nt diffuser pipe length
		frm.refresh_field("nt_pipe_length");

		//dt_pipe_size
		var a_f = frm.doc.diffuser_dt * 2;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000
		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("dt_pipe_size",ff);
		frm.refresh_field("dt_pipe_size");
		frm.set_value("dt_pipe_length",(frm.doc.tank_length+frm.doc.tank_height+2+frm.doc.tank_height+1+2));
		frm.refresh_field("dt_pipe_length");

		//cft_pipe_size
		var a_f = frm.doc.diffuser_cft * 2;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000
		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		// frm.set_value("cft_pipe_size",ff);
		// frm.refresh_field("cft_pipe_size");
		// frm.set_value("cft_pipe_length",(frm.doc.tank_length+frm.doc.tank_height+2+frm.doc.tank_height+1+2));
		frm.set_value("cft_pipe_length",frm.doc.tank_height+2+2);//cft diffuser pipe
		frm.refresh_field("cft_pipe_length");

		//srs_pipe_size
		var a_f = frm.doc.diffuser_srs * 2;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000
		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		// frm.set_value("srs_pipe_size",ff);
		// frm.refresh_field("srs_pipe_size");
		// frm.set_value("srs_pipe_length",(frm.doc.tank_length+frm.doc.tank_height+2+frm.doc.tank_height+1+2));
		frm.set_value("srs_pipe_length",frm.doc.tank_height+2+2);//srs diffuser pipes
		frm.refresh_field("srs_pipe_length");

		//dnt_pipe_size
		var a_f = frm.doc.diffuser_dnt * 2;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000
		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("dnt_pipe_size",ff);
		frm.refresh_field("dnt_pipe_size");
		frm.set_value("dnt_pipe_length",(frm.doc.tank_length+frm.doc.tank_height+2+frm.doc.tank_height+1+2));
		frm.refresh_field("dnt_pipe_length");

		// var vvo =  (frm.doc.flow)/(frm.doc.tank_height * 2.5);
		var vvo =  frm.doc.diffuser_eqt
		var vvo1 = vvo * 1.5 * 1.5 * 1.1;
		frm.set_value("eqt_diffuser_pipe_line_length",vvo1);
		frm.refresh_field("eqt_diffuser_pipe_line_length");

		// rewolutte ro occurs - rewolutte_diffuser_grid
		if(selected_system_array.includes("Rewolutte RO")){
			var vvo =  frm.doc.diffuser_rewolutte
			var vvo1 = vvo * 1.5 * 1.5 * 1.1;
			frm.set_value("rewolutte_diffuser_grid",vvo1);
			frm.refresh_field("rewolutte_diffuser_grid");			
		}

		//eqt_diffuser_pipe_size
		var sizearea = ((frm.doc.flow / frm.doc.tank_height) / frm.doc.tank_length);
		var sizearea1 = (frm.doc.diffuser_eqt * 2) / sizearea;
		var a_f = sizearea1;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000
		if(f2>0 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("eqt_diffuser_pipe_line_size",ff);
		frm.refresh_field("eqt_diffuser_pipe_line_size");

		//do_increase_capacity
		var a_f = frm.doc.do_increase_blower_capacity;
		var m_v = 20;
		var f0 = m_v * 3600
		var f1=a_f/f0
		var f2=Math.sqrt((4*f1)/Math.PI)*1000

		if(f2>0 && f2<6.99)
		{
			var ff="DN6"
			var ff1=Math.abs(f2-6.99);
		}
		else if(f2>6.99 && f2<10.42)
		{
			var ff="DN8";
			var ff1=Math.abs(f2-10.42);	
		}
		else if(f2>10.42 && f2<13.85)
		{
			var ff="DN10";
			var ff1=Math.abs(f2-13.85);
		}
		else if(f2>13.85 && f2<18.04)
		{
			var ff="DN15";
			var ff1=Math.abs(f2-18.04);
		}
		else if(f2>18.04 && f2<23.37)
		{
			var ff="DN20";
			var ff1=Math.abs(f2-23.37);
		}
		else if(f2>23.37 && f2<30.1)
		{
			var ff="DN25";
			var ff1=Math.abs(f2-30.1);
		}
		else if(f2>30.1 && f2<38.86)
		{
			var ff="DN32";
			var ff1=Math.abs(f2-38.86);
		}
		else if(f2>38.86 && f2<44.96)
		{
			var ff="DN40";
			var ff1=Math.abs(f2-44.96);
		}
		else if(f2>44.96 && f2<57.08)
		{
			var ff="DN50";
			var ff1=Math.abs(f2-57.08);
		}
		else if(f2>57.08 && f2<68.81)
		{
			var ff="DN65";
			var ff1=Math.abs(f2-68.81);
		}
		else if(f2>68.81 && f2<84.68)
		{
			var ff="DN80";
			var ff1=Math.abs(f2-84.68);
		}
		else if(f2>84.68 && f2<110.08)
		{
			var ff="DN100";
			var ff1=Math.abs(f2-110.08);
		}
		else if(f2>110.08 && f2<135.76)
		{
			var ff="DN125";
			var ff1=Math.abs(f2-135.76);
		}
		else if(f2>135.76 && f2<162.72)
		{
			var ff="DN150";
			var ff1=Math.abs(f2-162.72);
		}
		else if(f2>162.72 && f2<213.54)
		{
			var ff="DN200";
			var ff1=Math.abs(f2-213.54);
		}
		else if(f2>213.54 && f2<266.25)
		{
			var ff="DN250";
			var ff1=Math.abs(f2-266.25);
		}
		else if(f2>266.25 && f2<315.93)
		{
			var ff="DN300";
			var ff1=Math.abs(f2-315.93);
		}
		else if(f2>315.93 && f2<347.68)
		{
			var ff="DN350";
			var ff1=Math.abs(f2-347.68);
		}
		else if(f2>347.68 && f2<398.02)
		{
			var ff="DN400";
			var ff1=Math.abs(f2-398.02);
		}
		else if(f2>398.02 && f2<448.62)
		{
			var ff="DN450";
			var ff1=Math.abs(f2-448.62);
		}
		else if(f2>448.62 && f2<498.44)
		{
			var ff="DN500";
			var ff1=Math.abs(f2-498.44);
		}
		else if(f2>498.44 && f2<549.44)
		{
			var ff="DN550";
			var ff1=Math.abs(f2-549.44);
		}
		else if(f2>549.44 && f2<598.92)
		{
			var ff="DN600";
			var ff1=Math.abs(f2-598.92);
		}
		else if(f2>598.92 && f2<749.3)
		{
			var ff="DN750";
			var ff1=Math.abs(f2-749.3);
		}
		frm.set_value("do_increase_diffuser_pipe_size",ff);
		frm.refresh_field("do_increase_diffuser_pipe_size");

		var vvo =  frm.doc.do_increase_no_of_diffuser
		var vvo1 = vvo * 1.5 * 1.5 * 1.1;
		frm.set_value("do_increase_diffuser_pipe_length",vvo1);
		frm.refresh_field("do_increase_diffuser_pipe_length");




		var v=(frm.doc.sote)/(frm.doc.fouling_factor * frm.doc.sote_factor);
		var v1 = v;
		var v2 = v1 *(100/20);
		var v3 = v2/0.8;
		var v4 = v3 /24;

		frm.set_value("specific_gravity_day",v3);
		frm.refresh_field("specific_gravity_day");

		frm.set_value("specific_gravity_hr",v4);
		frm.refresh_field("specific_gravity_hr");

		frm.set_value("do_increase_blower_capacity",v4);
		frm.refresh_field("do_increase_blower_capacity");

		frm.set_value("do_increase_no_of_diffuser",(v4/frm.doc.flow_rate_diffuser));
		frm.refresh_field("do_increase_no_of_diffuser");

		// if(frm.doc.seperate_blower_for_equalization_tank==1)
		// {
		// 	frm.set_value("total_do_blower_capacity",(frm.doc.bio_blower + v4));
		// 	frm.refresh_field("total_do_blower_capacity");
		// }
		// else
		// {
		// 	frm.set_value("total_do_blower_capacity",(frm.doc.blower_cpa + v4));
		// 	frm.refresh_field("total_do_blower_capacity");
		// }
		frm.set_value("f_pump_for",frm.doc.feed_pump * frm.doc.feed_qty);
		frm.refresh_field("f_pump_for");
		frm.set_value("f_filtration_for",1640/60);
		frm.refresh_field("f_filtration_for");
		frm.set_value("f_total_cycle_for",frm.doc.operating_hours * 2);
		frm.refresh_field("f_total_cycle_for");
		frm.set_value("f_filtration_day_for",(frm.doc.f_filtration_for * frm.doc.f_total_cycle_for)/60);
		frm.refresh_field("f_filtration_for");
		frm.set_value("f_total_flow_for",frm.doc.f_pump_for * frm.doc.f_filtration_day_for);
		frm.refresh_field("f_total_flow_for");

		var rounded = Math.round(frm.doc.total_modules);
		frm.set_value("r_pump_for",rounded * 0.2);
		frm.refresh_field("r_pump_for");
		frm.set_value("r_filtration_for",frm.doc.f_filtration_for);
		frm.refresh_field("r_filtration_for");

		frm.set_value("r_total_cycle_for",frm.doc.f_total_cycle_for);
		frm.refresh_field("r_total_cycle_for");

		frm.set_value("r_filtration_day_for",frm.doc.f_filtration_day_for);
		frm.refresh_field("r_filtration_for");

		frm.set_value("r_total_flow_for",(frm.doc.r_pump_for)*(frm.doc.f_filtration_day_for));
		frm.refresh_field("r_total_flow_for");

		frm.set_value("p_pump_for",(frm.doc.f_pump_for) - (frm.doc.r_pump_for));
		frm.refresh_field("p_pump_for");

		frm.set_value("p_filtration_for",frm.doc.f_filtration_for);
		frm.refresh_field("p_filtration_for");

		frm.set_value("p_total_cycle_for",frm.doc.f_total_cycle_for);
		frm.refresh_field("p_total_cycle_for");

		frm.set_value("p_filtration_day_for",frm.doc.f_filtration_day_for);
		frm.refresh_field("p_filtration_day_for");

		frm.set_value("p_total_flow_for",frm.doc.p_pump_for * frm.doc.p_filtration_day_for);
		frm.refresh_field("p_total_flow_for");

		frm.set_value("b_pump_for",frm.doc.bw_pump * frm.doc.bw_qty);
		frm.refresh_field("b_pump_for");

		frm.set_value("b_bw_for",1);
		frm.refresh_field("b_bw_for");

		frm.set_value("b_total_cycle_for",frm.doc.f_total_cycle_for);
		frm.refresh_field("b_total_cycle_for");

		frm.set_value("b_bw_day_for",(frm.doc.b_total_cycle_for * frm.doc.b_bw_for /60));
		frm.refresh_field("b_bw_day_for");

		frm.set_value("b_total_flow_for",frm.doc.b_pump_for * frm.doc.b_bw_day_for);
		frm.refresh_field("b_total_flow_for");

		frm.set_value("mf_overall_per_cal",frm.doc.p_total_flow_for - frm.doc.b_total_flow_for);
		frm.refresh_field("mf_overall_per_cal");
		var minval = frm.doc.mf_overall_per_cal - frm.doc.flow;
		frm.set_value("excess_percentage",(minval/frm.doc.flow)*100);
		frm.refresh_field("excess_percentage");

		frm.set_value("recovery",(frm.doc.p_pump_for/frm.doc.f_pump_for)*100);
		frm.refresh_field("recovery");

		//MBR CTS REWOLUTEE

		frm.set_value("cts_ovivo_permeate_flow_rate",(frm.doc.mbr_cts_flow/frm.doc.cts_ovivo_operating_hours));
		frm.refresh_field("cts_ovivo_permeate_flow_rate");

		frm.set_value("cts_ovivo_permeate_flow_rate",(frm.doc.mbr_cts_flow/frm.doc.cts_ovivo_operating_hours));
		frm.refresh_field("cts_ovivo_permeate_flow_rate");
		frm.set_value("cts_ovivo_required_flux",frm.doc.cts_ovivo_permeate_flux_lmh);
		frm.refresh_field("cts_ovivo_required_flux")
		frm.set_value("cts_ovivo_area_required_for_filtration",(frm.doc.cts_ovivo_permeate_flow_rate/frm.doc.cts_ovivo_permeate_flux_lmh)*1000);
		frm.refresh_field("cts_ovivo_area_required_for_filtration");

		frm.set_value("cts_ovivo_permeate_flux_lmd",frm.doc.cts_ovivo_permeate_flux_lmh*frm.doc.cts_ovivo_operating_hours);
		frm.refresh_field("cts_ovivo_permeate_flux_lmd");

		frm.set_value("cts_ovivo_backwash_flux",frm.doc.cts_ovivo_permeate_flux_lmh*2.3);
		frm.refresh_field("cts_ovivo_backwash_flux");

		frm.set_value("cts_ovivo_cip_flux",frm.doc.cts_ovivo_permeate_flux_lmh*1.25);
		frm.refresh_field("cts_ovivo_cip_flux");

		frm.set_value("cts_ovivo_cip_flux",frm.doc.cts_ovivo_permeate_flux_lmh*1.25);
		frm.refresh_field("cts_ovivo_cip_flux");

		frm.set_value("cts_ovivo_permeate_qty",frm.doc.cts_ovivo_no_of_trains);
		frm.refresh_field("cts_ovivo_permeate_qty");
		if(frm.doc.cts_ovivo_no_of_trains<=2)
		{
			frm.set_value("cts_ovivo_backwash_qty",1);
			frm.refresh_field("cts_ovivo_backwash_qty");
		}
		else
		{
			var ovback = frm.doc.cts_ovivo_no_of_trains/2
			frm.set_value("cts_ovivo_backwash_qty",Math.ceil(ovback / 1) * 1);
			frm.refresh_field("cts_ovivo_backwash_qty");
		}

		if(frm.doc.cts_ovivo_type=="S-MBR")
		{
			frm.set_value("cts_ovivo_circulation_qty",frm.doc.cts_ovivo_no_of_trains);
			frm.refresh_field("cts_ovivo_circulation_qty");
			frm.set_value("cts_ovivo_circulation_sqty",1);
			frm.refresh_field("cts_ovivo_circulation_sqty");
		}
		else
		{
			frm.set_value("cts_ovivo_circulation_qty",0);
			frm.refresh_field("cts_ovivo_circulation_qty");
			frm.set_value("cts_ovivo_circulation_sqty",0);
			frm.refresh_field("cts_ovivo_circulation_sqty");
		}

		if(frm.doc.cts_ovivo_type=="S-MBR")
		{
			frm.set_value("cts_ovivo_cip_qty",frm.doc.cts_ovivo_no_of_trains);
			frm.refresh_field("cts_ovivo_cip_qty");
		}
		else
		{
			frm.set_value("cts_ovivo_cip_qty",0);
			frm.refresh_field("cts_ovivo_cip_qty");
		}

		if(frm.doc.cts_ovivo_type=="S-UF")
		{
			if(frm.doc.cts_ovivo_no_of_trains<=3)
			{
				frm.set_value("cts_ovivo_blower_qty",1);
				frm.refresh_field("cts_ovivo_blower_qty");
			}
			else
			{
				frm.set_value("cts_ovivo_blower_qty",(frm.doc.cts_ovivo_no_of_trains/2));
				frm.refresh_field("cts_ovivo_blower_qty");	
			}
		}
		else
		{
			frm.set_value("cts_ovivo_blower_qty",frm.doc.cts_ovivo_no_of_trains);
			frm.refresh_field("cts_ovivo_blower_qty");
		}

		if(frm.doc.cts_ovivo_no_of_trains<=3)
		{
			frm.set_value("cts_ovivo_sprinkler_qty",1);
			frm.refresh_field("cts_ovivo_sprinkler_qty");
		}
		else
		{
			frm.set_value("cts_ovivo_sprinkler_qty",(frm.doc.cts_ovivo_no_of_trains/2));
			frm.refresh_field("cts_ovivo_sprinkler_qty");
		}

		if(frm.doc.cts_ovivo_no_of_trains<=3)
		{
			frm.set_value("cts_ovivo_sludge_qty",1);
			frm.refresh_field("cts_ovivo_sludge_qty");
		}
		else
		{
			frm.set_value("cts_ovivo_sludge_qty",(frm.doc.cts_ovivo_no_of_trains/2));
			frm.refresh_field("cts_ovivo_sludge_qty");
		}

		var no_mb=Math.round((frm.doc.cts_ovivo_area_required_for_filtration/frm.doc.cts_ovivo_area_per_module) * 10.0) / 10.0
		frm.set_value("cts_ovivo_no_module_required",no_mb)

		frm.set_value("cts_ovivo_no_of_stacks_required",frm.doc.cts_ovivo_no_module_required/frm.doc.cts_ovivo_no_of_module_per_stack);
		frm.refresh_field("cts_ovivo_no_of_stacks_required");

		frm.set_value("cts_ovivo_modules_train",frm.doc.cts_ovivo_no_module_required/frm.doc.cts_ovivo_no_of_trains);
		frm.refresh_field("cts_ovivo_modules_train");

		frm.set_value("cts_ovivo_permeate_pump",(frm.doc.cts_ovivo_permeate_flow_rate*1.15)/frm.doc.cts_ovivo_permeate_qty);
		frm.refresh_field("cts_ovivo_permeate_pump");

		frm.set_value("cts_ovivo_no_of_module_per_train",frm.doc.cts_ovivo_no_of_stacks_required/frm.doc.cts_ovivo_no_of_trains);
		frm.refresh_field("cts_ovivo_no_of_module_per_train");

		frm.set_value("cts_ovivo_total_area",frm.doc.cts_ovivo_no_module_required*frm.doc.cts_ovivo_area_per_module);
		frm.refresh_field("cts_ovivo_total_area");

		frm.set_value("cts_ovivo_circulation_pump",((frm.doc.mbr_cts_flow)*5)/(24*frm.doc.cts_ovivo_no_of_trains));
		frm.refresh_field("cts_ovivo_circulation_pump");

		frm.set_value("cts_ovivo_blower",(frm.doc.cts_ovivo_air_flow_rate_per_stack*frm.doc.cts_ovivo_no_of_stacks_required)/frm.doc.cts_ovivo_no_of_trains);
		frm.refresh_field("cts_ovivo_blower");

		frm.set_value("cts_ovivo_sprinkler_pump_2",(12*frm.doc.cts_ovivo_no_of_stacks_required)/frm.doc.cts_ovivo_no_of_trains);
		frm.refresh_field("cts_ovivo_sprinkler_pump_2");

		frm.set_value("cts_ovivo_bc",((frm.doc.cts_ovivo_backwash_flux*frm.doc.cts_ovivo_area_required_for_filtration)/(frm.doc.cts_ovivo_no_of_trains*1000)));
		frm.refresh_field("cts_ovivo_bc");

		frm.set_value("cts_ovivo_cip",((frm.doc.cts_ovivo_backwash_flux*frm.doc.cts_ovivo_area_required_for_filtration)/(frm.doc.cts_ovivo_no_of_trains*1000)));
		frm.refresh_field("cts_ovivo_cip");

		var mo_height = ((0.16 * frm.doc.cts_ovivo_no_of_module_per_stack) +0.534);
		var with_f_b1 = mo_height + 0.3 + 0.5;
		var with_f_b2 = (0.72 * frm.doc.cts_ovivo_modules_train)+(0.15 * (frm.doc.cts_ovivo_modules_train+1));
		var with_f_b3 = (0.57 * 1)+0.3;
		var total_vol = with_f_b1 * with_f_b2 * with_f_b3;
		frm.set_value("cts_ovivo_tank_volume",total_vol);
		frm.refresh_field("cts_ovivo_tank_volume");


		frm.set_value("cts_ovivo_sludge_pump_2",(0.7084 * frm.doc.cts_ovivo_no_of_stacks_required * 8 * frm.doc.cts_ovivo_no_of_trains * ((0.16 * frm.doc.cts_ovivo_no_of_module_per_stack) + 0.72))/frm.doc.cts_ovivo_sludge_pump_hours_of_operation_2);
		frm.refresh_field("cts_ovivo_sludge_pump_2");

		frm.set_value("cts_ovivo_total_cycle",60/(frm.doc.cts_ovivo_filtration_min + frm.doc.cts_ovivo_backwash_min));
		frm.refresh_field("cts_ovivo_total_cycle");

		frm.set_value("cts_ovivo_hours_of_operation",frm.doc.cts_ovivo_operating_hours);
		frm.refresh_field("cts_ovivo_hours_of_operation");

		frm.set_value("cts_ovivo_filtration_hr",(frm.doc.cts_ovivo_filtration_min * frm.doc.cts_ovivo_total_cycle * frm.doc.cts_ovivo_hours_of_operation)/60);
		frm.refresh_field("cts_ovivo_filtration_hr");

		frm.set_value("cts_ovivo_backwash_hr",(frm.doc.cts_ovivo_backwash_min * frm.doc.cts_ovivo_total_cycle * frm.doc.cts_ovivo_hours_of_operation)/60);
		frm.refresh_field("cts_ovivo_backwash_hr");

		frm.set_value("cts_ovivo_permeate_m3",(frm.doc.cts_ovivo_filtration_hr * frm.doc.cts_ovivo_permeate_pump * frm.doc.cts_ovivo_no_of_trains));
		frm.refresh_field("cts_ovivo_permeate_m3");

		frm.set_value("cts_ovivo_backwash_m3",(frm.doc.cts_ovivo_backwash_hr * frm.doc.cts_ovivo_bc * frm.doc.cts_ovivo_no_of_trains));
		frm.refresh_field("cts_ovivo_backwash_m3");

		frm.set_value("cts_ovivo_total_permeate",frm.doc.cts_ovivo_permeate_m3 - frm.doc.cts_ovivo_backwash_m3);
		frm.refresh_field("cts_ovivo_total_permeate");

		var vs=(6*frm.doc.cts_ovivo_area_per_module * frm.doc.cts_ovivo_no_module_required)/frm.doc.cts_ovivo_no_of_trains;
		frm.set_value("cts_cip_tank_per_train",(vs * frm.doc.cts_ovivo_no_of_stacks_required)/frm.doc.cts_ovivo_no_of_trains);
		frm.refresh_field("cts_cip_tank_per_train");

		var dp = frm.doc.cts_ovivo_chlorine_dosing_for_each_stack * frm.doc.cts_ovivo_modules_train * frm.doc.cts_ovivo_area_per_module;
		var dp1 = dp * (frm.doc.cts_ovivo_hypo_cleaning_concentration/100) * 3600;
		var dp2 = dp1 / 100;
		

		frm.set_value("cts_naocl_dosing_pump_rc",dp2);
		frm.refresh_field("cts_naocl_dosing_pump_rc");

		var dp = frm.doc.ovivo_citric_dosing_for_each_stack * frm.doc.cts_ovivo_modules_train * frm.doc.ovivo_area_per_module;
		var dp1 = dp * (frm.doc.ovivo_hcl_cleaning_cencentration/100) * 3600;
		var dp2 = dp1 / 100;

		frm.set_value("cts_citric_dosing_pump_mc_rc",dp2);
		frm.refresh_field("cts_citric_dosing_pump_mc_rc");

		frm.set_value("cts_hcl_dosing_pump_mc_rc",(frm.doc.cts_ovivo_hcl_dosing_for_each_stack * frm.doc.mbr_cts_flow) / (1000*frm.doc.cts_ovivo_operating_hours));
		frm.refresh_field("cts_hcl_dosing_pump_mc_rc");

		frm.set_value("cts_alum_dosing_pump_mc_rc",(frm.doc.cts_ovivo_alum_dosing_for_each_stack * frm.doc.mbr_cts_flow) / (1000*frm.doc.cts_ovivo_operating_hours));
		frm.refresh_field("cts_alum_dosing_pump_mc_rc");

		frm.set_value("cts_ovivo_permeate_capacity",frm.doc.cts_ovivo_permeate_pump*frm.doc.cts_ovivo_permeate_qty*frm.doc.cts_ovivo_filtration_hr);
		frm.refresh_field("cts_ovivo_permeate_capacity");

		//mf sulphur black
		frm.set_value("total_reject_flow_rate_m3hr",frm.doc.total_modules * frm.doc.reject_flow_ref);
		frm.refresh_field("total_reject_flow_rate_m3hr");

		frm.set_value("total_reject_flow_rate_m3day",(frm.doc.total_reject_flow_rate_m3hr * frm.doc.f_filtration_day_for)+frm.doc.mf_for_bw_flow);
		frm.refresh_field("total_reject_flow_rate_m3day");

		frm.set_value("mf_suspends_mgl",50/(1-(frm.doc.recovery/100)));
		frm.refresh_field("mf_suspends_mgl");

		frm.set_value("mf_suspends_kgday",(frm.doc.total_reject_flow_rate_m3day * frm.doc.mf_suspends_mgl)/1000);
		frm.refresh_field("mf_suspends_kgday");

		frm.set_value("mf_sludge_pump_capacity",frm.doc.total_reject_flow_rate_m3day/frm.doc.f_filtration_day_for);
		frm.refresh_field("mf_sludge_pump_capacity");

		frm.set_value("mf_lamella_settler",Math.ceil(frm.doc.total_reject_flow_rate_m3hr / 5) * 5);
		frm.refresh_field("mf_lamella_settler");

		frm.set_value("mf_dosing_pump",((frm.doc.mf_pac_dosage * frm.doc.total_reject_flow_rate_m3day)/(1000 * frm.doc.f_filtration_day_for* (frm.doc.mf_pac_concentration/100))));
		frm.refresh_field("mf_dosing_pump");

		//mbr sulphur black
		frm.set_value("mbr_volume_drained_in_a_day_m3day",frm.doc.design_no_of_trains * frm.doc.mbr_no_of_drains_per_day * frm.doc.mbr_tank_volume);
		frm.refresh_field("mbr_volume_drained_in_a_day_m3day");

		frm.set_value("mbr_volume_drained_in_a_day_m3hr",frm.doc.mbr_volume_drained_in_a_day_m3day/16);
		frm.refresh_field("mbr_volume_drained_in_a_day_m3hr");

		frm.set_value("mbr_suspends_kgday",(frm.doc.mbr_volume_drained_in_a_day_m3day * frm.doc.mbr_suspends_mgl)/1000);
		frm.refresh_field("mbr_suspends_kgday");

		frm.set_value("mbr_sludge_pump_capacity",frm.doc.mbr_volume_drained_in_a_day_m3day/frm.doc.mbr_sludge_pump_operating_hours);
		frm.refresh_field("mbr_sludge_pump_capacity");

		var mbrlam = frm.doc.mbr_volume_drained_in_a_day_m3day/frm.doc.mbr_lamella_operating_hours
		frm.set_value("mbr_lamella_settler",Math.ceil(mbrlam / 5) * 5);
		frm.refresh_field("mbr_lamella_settler");

		frm.set_value("mbr_dosing_pump",((frm.doc.mbr_pac_dosage * frm.doc.mbr_volume_drained_in_a_day_m3day)/(1000 * frm.doc.mbr_lamella_operating_hours* (frm.doc.mbr_pac_concentration/100))));
		frm.refresh_field("mbr_dosing_pump");

		//mbr_ovivo sulphur black
		frm.set_value("mbro_tank_volume",((((160 * frm.doc.ovivo_no_of_module_per_stack)+(553+300))/1000)*0.87)*frm.doc.ovivo_no_of_module_per_train);
		frm.refresh_field("mbro_tank_volume");

		frm.set_value("mbro_volume_drained_in_a_day",frm.doc.mbro_tank_volume * frm.doc.ovivo_no_of_trains * frm.doc.mbro_no_of_drains_per_day);
		frm.refresh_field("mbro_volume_drained_in_a_day");

		frm.set_value("mbro_suspends_kgday",(frm.doc.mbro_volume_drained_in_a_day * frm.doc.mbro_suspends_mgl)/1000);
		frm.refresh_field("mbro_suspends_kgday");

		frm.set_value("mbro_sludge_pump_capacity",frm.doc.mbro_volume_drained_in_a_day/frm.doc.mbro_sludge_pump_operating_hours);
		frm.refresh_field("mbro_sludge_pump_capacity");

		var mbrolam = frm.doc.mbro_volume_drained_in_a_day/frm.doc.mbro_lamella_operating_hours
		frm.set_value("mbro_lamella_settler",Math.ceil(mbrolam / 5) * 5);
		frm.refresh_field("mbro_lamella_settler");

		frm.set_value("mbro_dosing_pump",((frm.doc.mbro_pac_dosage * frm.doc.mbro_volume_drained_in_a_day)/(1000 * frm.doc.mbro_lamella_operating_hours* (frm.doc.mbro_pac_concentration/100))));
		frm.refresh_field("mbro_dosing_pump");
	}
	// enquiry_no:function(frm){
	// 	frappe.db.get_value("Process Enquiry Sheet", {"name": frm.doc.enquiry_no}, "capacity_to_be_treated_avg", function(value) {
	// 	frm.set_value("flow",value.capacity_to_be_treated_avg);
	// 	frm.refresh_field("flow");
	// 	});
	// 	frappe.call({
	// 			method:"wtt_module.wtt_module.doctype.project_startup_sheet.project_startup_sheet.get_all_value",
	// 			args:{
	// 				enq:frm.doc.enquiry_no
	// 			},
	// 			callback(r){
	// 				frm.set_value("tss",r.message[0].tss);
	// 				frm.set_value("cod",r.message[1].cod);
	// 				frm.set_value("cod_reduction_for_og",(r.message[1].cod)*0.8);
	// 				frm.set_value("bod",r.message[2].bod);
	// 				frm.refresh_field("tss");
	// 				frm.refresh_field("cod");
	// 				frm.refresh_field("bod");
	// 			}
	// 		});
	// }
});


frappe.ui.form.on('Selected Process System', {
    before_selected_system_remove: function(frm,cdt,cdn) {
    	var child = locals[cdt][cdn];
    	if(child.selected_system_name=="Sludge Thickener with mech"){
    		frm.set_value("is_with_mechanism",0);
    		frm.refresh_field("is_with_mechanism");
    	}
    }
});
var append_selected_system=function(frm,ar){
	$.each(frm.doc.system_details || [], function(i, v) {
		var ar2=[];
		$.each(frm.doc.selected_system || [], function(ii, vv) {
			ar2.push(vv.selected_system_name);
		});
		for(var j=0;j<ar.length;j++){
			if(ar[j]==v.system_name && !ar2.includes(ar[j])){
				if(v.system_name=="Sludge Thickener with mech"){
		    		frm.set_value("is_with_mechanism",1);
		    		frm.refresh_field("is_with_mechanism");
		    	}
				var addrow = frm.add_child("selected_system");
				addrow.selected_system_name = v.system_name;
				addrow.selected_type = v.type			
			}
		}
	});			
	frm.refresh_field("selected_system");
}