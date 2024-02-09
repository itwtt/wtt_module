// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Process Enquiry Sheet', {
	onload: function(frm) {	
		if(frm.doc.parameters)
		{

		}
		else
		{
			var para=["pH", "COD(mg/l)", "BOD(mg/l)", "TDS(mg/l)", "PVA(mg/l)", "TSS(mg/l)", "IRON(mg/l)", "SILICA(mg/l)", "COLOUR(hazen)", "SODIUM(mg/l)", "CALCIUM(mg/l)", "SULPHATES(mg/l)", "CHLORIDES(mg/l)", "MAGNESIUM(mg/l)", "ALKALINITY(mg/l)", "TEMPERATURE(°C)", "OIL GREASE(mg/l)", "TOTAL NITROGEN(mg/l)", "TOTAL HARDNESS(mg/l)"]
			for(var i=0;i<para.length;i++)
			{
			var child = frm.add_child("parameters");
			frappe.model.set_value(child.doctype, child.name, "parameter", para[i]);
			frm.refresh_field("parameters");
			}
		}
		frm.clear_table("system_details")
		frm.refresh_field("system_details");
		var arr=["Rotary Brush Screener", "Bar Screener", "Drum Screener", "Anaerobic Screener", "Anaerobic Equalization", "Anaerobic Neutralization", "Anaerobic System", "Ammonia Striper", "Lifting sump", "Oil & grease trap", "DAF (Dissolved Air Flotation)", "Equalization System", "Neutralization System","Cooling Tower","De-Nitrification System", "Distribution system", "Biological Oxidation System", "Clarifier Feed Tank", "Circular Clarifier System", "Lamella Settler", "DO increase system", "SRS System", "Sand Filter", "Activated Carbon Filter", "Self-Cleaning Filter", "Micro Filtration - ASAHI", "Submerged MBR system - KOCH", "Submerged MBR system - OVIVO", "Sulphur Black Removal System", "Sludge Thickener", "Sludge Thickener with mech", "Screw Press", "Belt Press", "Degasser System", "Reverse Osmosis", "Hardness and Silica Removal System", "Chlorination system", "Hardness and Color Removal System", "Reject Reverse Osmosis", "Evaporator", "Agitated Thin film dryer", "Centrifuge", "Crystallizer", "Nano Filtration", "Care system"]
		var arr1=["Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment","Pre Treatment","Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Filtration", "Filtration", "Filtration", "Filtration", "Filtration", "Filtration", "Filtration", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Pre Treatment", "Filtration", "Filtration", "Filtration", "Filtration", "Filtration", "Filtration", "Rms", "Rms", "Rms", "Rms", "Filtration", "Others"]
		for(var i=0;i<arr.length;i++)
		{
			var child = frm.add_child("system_details");
			frappe.model.set_value(child.doctype, child.name, "system_name", arr[i]);
			frappe.model.set_value(child.doctype, child.name, "type", arr1[i]);
			frm.refresh_field("system_details");
		}

		frm.fields_dict['system_details'].grid.add_custom_button('Add items', () => {
			frm.clear_table("selected_system")
			frm.refresh_field("selected_system");
			var arr2=[]
			$.each(frm.doc.selected_system, function (index, source_row) {
				arr2.push(source_row.selected_system_name)
			});

			$.each(frm.doc.system_details, function (index, source_row) {
			    if(source_row.__checked==true)
			    {   
			    	if(arr2.includes(source_row.system_name)){
			    		console.log("yes")
			    	}
			    	else{
			    		var child = frm.add_child("selected_system");
						frappe.model.set_value(child.doctype, child.name, "selected_system_name",source_row.system_name);
						frappe.model.set_value(child.doctype, child.name, "selected_type",source_row.type);
						frm.refresh_field("selected_system");
			    	}
			    }
			});
		});
	},
	get_flowchart:function(frm){
		var tds=0;
		var selected=[];
		var ro=[];
		
		$.each(frm.doc.parameters, function (index, source_row) {
			if(source_row.parameter=='TDS(mg/l)')
			{
				tds=source_row.value
			}
		});

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
		if(frm.doc.ro_recovery)
		{
			vs+='<table border="1px" cellpadding="5" cellspacing="5" align="right"><tr><th>SYSTEM</th><th>RECOVERY</th></tr><tr><td>RO</td><td>'+frm.doc.ro_recovery+'%</td></tr></table><br><br><br><br>';
		}
		vs+='<div style="background:#da9695;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;">EFFLUENT</div>';
		vs+='<p style="margin-left:15px">'+frm.doc.capacity_to_be_treated_avg+' M<sup>3</sup>/Day || '+tds+' TDS</p>';
		vs+='<p style="margin-top:5px"><span style="margin-left:70px;font-size:30px;">&#8595;</span></p>';
		for(var i=0;i<selected.length;i++)
		{
			if(selected[i].type=="Pre Treatment")
			{
				if(selected[i].system=='DAF (Dissolved Air Flotation)' && frm.doc.daf_with_dosing==1)
				{
					vs+='<table><tr><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">DAF (Dissolved Air Flotation)</p></div></td><td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'	
				}
				else if(selected[i].system=='Submerged MBR system - KOCH' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table><tr><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Submerged MBR system - KOCH</p></div></td><td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Submerged MBR system - OVIVO' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table><tr><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Submerged MBR system - OVIVO</p></div></td><td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#f2d3b7;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Reverse Osmosis')
				{
					vs+='<table><tr><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Reverse Osmosis</p></div></td>'
					for(var j=0;j<ro.length;j++){
						if(j==0){
							vs+='<td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">'+ro[j].system+'</p>'
						}
						else{
							vs+='<br><span style="font-size:30px;">&#8595;</span><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">'+ro[j].system+'</p></div>'
						}
						
					}
					vs+='</td></tr></table>'
				}
				else
				{
					vs+='<div style="background:#f2d3b7;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;">'+selected[i].system+'</div>'
				}	
				if(i==(selected.length-1))
				{

				}
				else
				{
					vs+='<p style="margin-left:15px">'+frm.doc.capacity_to_be_treated_avg+' M<sup>3</sup>/Day || '+tds+' TDS</p>';
					vs+='<p style="margin-top:5px"><span style="margin-left:70px;font-size:30px;">&#8595;</span></p>';
				}
			}
			else if(selected[i].type=="Filtration")
			{
				if(selected[i].system=='DAF (Dissolved Air Flotation)' && frm.doc.daf_with_dosing==1)
				{
					vs+='<table><tr><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">DAF (Dissolved Air Flotation)</p></div></td><td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'	
				}
				else if(selected[i].system=='Submerged MBR system - KOCH' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table><tr><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Submerged MBR system - KOCH</p></div></td><td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Submerged MBR system - OVIVO' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table><tr><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Submerged MBR system - OVIVO</p></div></td><td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Reverse Osmosis')
				{
					vs+='<table><tr><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Reverse Osmosis</p></div></td>'
					for(var j=0;j<ro.length;j++){
						if(j==0){
							vs+='<td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">'+ro[j].system+'</p>'
						}
						else{
							vs+='<br><span style="font-size:30px;">&#8595;</span><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">'+ro[j].system+'</p></div>'
						}
						
					}
					vs+='</td></tr></table>'
				}
				else
				{
					vs+='<div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;">'+selected[i].system+'</div>'
				}
				if(i==(selected.length-1))
				{

				}
				else
				{
					vs+='<p style="margin-left:15px">'+frm.doc.capacity_to_be_treated_avg+' M<sup>3</sup>/Day || '+tds+' TDS</p>';
					vs+='<p style="margin-top:5px"><span style="margin-left:70px;font-size:30px;">&#8595;</span></p>';
				}
			}
			else
			{
				if(selected[i].system=='DAF (Dissolved Air Flotation)' && frm.doc.daf_with_dosing==1)
				{
					vs+='<table><tr><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">DAF (Dissolved Air Flotation)</p></div></td><td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'	
				}
				else if(selected[i].system=='Submerged MBR system - KOCH' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table><tr><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Submerged MBR system - KOCH</p></div></td><td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Submerged MBR system - OVIVO' && frm.doc.mbr_with_dosing==1)
				{
					vs+='<table><tr><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Submerged MBR system - OVIVO</p></div></td><td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#d8e5bc;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Sludge Thickener</p></div></td></tr></table>'
				}
				else if(selected[i].system=='Reverse Osmosis')
				{
					vs+='<table><tr><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">Reverse Osmosis</p></div></td>'
					for(var j=0;j<ro.length;j++){
						if(j==0){
							vs+='<td><span style="font-size:30px;">&#8594;</span></td><td><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">'+ro[j].system+'</p>'
						}
						else{
							vs+='<br><span style="font-size:30px;">&#8595;</span><div style="background:#97b1cd;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;"><p style="font-size:12px">'+ro[j].system+'</p></div>'
						}
						
					}
					vs+='</td></tr></table>'
				}
				else
				{
					vs+='<div style="background:#d8e5bc;border: 1px solid black;width:160px;height:40px;text-align: center;vertical-align: middle;">'+selected[i].system+'</div>'
				}	
				if(i==(selected.length-1))
				{

				}
				else
				{
					vs+='<p style="margin-left:15px">'+frm.doc.capacity_to_be_treated_avg+' M<sup>3</sup>/Day || '+tds+' TDS</p>';
					vs+='<p style="margin-top:5px"><span style="margin-left:70px;font-size:30px;">&#8595;</span></p>';
				}
			}
		}
		frm.set_value('html_editor',vs);
		frm.refresh_field("html_editor");
	}
});
