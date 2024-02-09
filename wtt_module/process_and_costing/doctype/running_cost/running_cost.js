// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Running Cost', {
	setup:function(frm){
		handle_ro_fields(frm);
	},
	refresh:function(frm){
		handle_ro_fields(frm);
	},
	startup_sheet:function(frm)
	{
		frm.clear_table("selected_system");
		frm.refresh_field("selected_system");
		frappe.call({
			method:"wtt_module.wtt_module.doctype.startup_sheet.startup_sheet.get_system",
			args:{
				st:frm.doc.startup_sheet
			},
			callback(r){
				for(var i=0;i<r.message.length;i++)
				{
					var child = frm.add_child("selected_system");
					frappe.model.set_value(child.doctype, child.name, "selected_system_name", r.message[i].select_system);
					frappe.model.set_value(child.doctype, child.name, "selected_type", r.message[i].selected_type);
					frm.refresh_field("selected_system");
				}
			}
		});

	},
	get_cleaning:function(frm)
	{
		frm.clear_table("final_chemical");
		frm.refresh_field("final_chemical");
		var finalsys = []
		var selected_system_array=[];
		$.each(frm.doc.selected_system || [], function(ii, vv) {
			selected_system_array.push(vv.selected_system_name);
		});
		if(selected_system_array.includes("Rotary Brush Screener"))
		{
			finalsys.push("NT")
		}	

		if(selected_system_array.includes("Belt Press"))
		{
			finalsys.push("BELT PRESS")
		}

		if(selected_system_array.includes("DAF (Dissolved Air Flotation)"))
		{
			finalsys.push("DAF")
		}

		if(selected_system_array.includes("Anaerobic Neutralization"))
		{
			finalsys.push("AN. NT")
		}

		if(selected_system_array.includes("Sulphur Black Removal System"))
		{
			finalsys.push("SBT")
		}

		if(selected_system_array.includes("Submerged MBR system - KOCH"))
		{
			finalsys.push("MBR (KOCH)")
		}
		if(selected_system_array.includes("Submerged MBR system - OVIVO"))
		{
			finalsys.push("MBR (OVIVO)")
		}
		if(selected_system_array.includes("CTS MBR"))
		{
			finalsys.push("CTS MBR")
		}
		if(selected_system_array.includes("Micro Filtration - ASAHI"))
		{
			finalsys.push("MF")
		}
		if(selected_system_array.includes("Degasser System"))
		{
			finalsys.push("DGT")
		}
		if(selected_system_array.includes("Reverse Osmosis"))
		{
			finalsys.push("RO")
			finalsys.push("RO WO DGT")
		}
		if(selected_system_array.includes("Rewolutte RO"))
		{
			finalsys.push("Rewolutte")
		}
		if(selected_system_array.includes("Hardness and Color Removal System"))
		{
			finalsys.push("CTS")
			finalsys.push("CTS WO DGT")
		}
		if(selected_system_array.includes("Chlorination system"))
		{
			finalsys.push("CHLORINATION")
		}
		if(selected_system_array.includes("Reject Reverse Osmosis"))
		{
			finalsys.push("R.RO")
		}
		// var finalsys = ["NT", "BELT PRESS", "DAF", "AN. NT", "QF", "SBT", "MBR", "MF", "DGT", "RO", "RO WO DGT", "CTS", "CTS WO DGT", "CHLORINATION", "R. MF", "R. DGT", "R.RO"]
		for(var i=0;i<finalsys.length;i++)
		{
			var child = frm.add_child("final_chemical");
			frappe.model.set_value(child.doctype, child.name, "system",finalsys[i]);
			frm.refresh_field("final_chemical");
		}
		frm.clear_table("running_chemical");
		frm.refresh_field("running_chemical");
		var runsystem=[]
		var runchem=[]
		var runcon=[]
		if(selected_system_array.includes("Neutralization System")){
			extend(runsystem,["NT"])
			extend(runchem,["H₂SO₄ - 98%"])
			extend(runcon,[490])
		}
		if(selected_system_array.includes("Belt Press")){
			extend(runsystem,["BELT PRESS"])
			extend(runchem,["POLYMER - C"])
			extend(runcon,[2])
		}
		if(selected_system_array.includes("DAF (Dissolved Air Flotation)")){
			extend(runsystem,["DAF", "DAF"])
			extend(runchem,["PAC", "POLYMER - A"])
			extend(runcon,[5,5])
		}
		if(selected_system_array.includes("Anaerobic Neutralization")){
			extend(runsystem,["AN. NT"])
			extend(runchem,["H₂SO₄ - 98%"])
			extend(runcon,[350])
		}
		if(selected_system_array.includes("Submerged MBR system - OVIVO")){
			extend(runsystem,["MBR (OVIVO)", "MBR (OVIVO)"])
			extend(runchem,["KMnO₄", "Hypochlorite"])
			extend(runcon,[40,12])
		}
		if(selected_system_array.includes("Degasser System")){
			extend(runsystem,["DGT"])
			extend(runchem,["HCl - 33%"])
			extend(runcon,[1116])
		}
		if(selected_system_array.includes("Reverse Osmosis")){
			extend(runsystem,["RO", "RO", "RO"])
			extend(runchem,["HCl - 33%", "WTTCHEM - 4111", "SMBS"])
			extend(runcon,[5,5,5])
		}
		if(selected_system_array.includes("Rewolutte RO")){
			extend(runsystem,["REW RO", "REW RO", "REW RO"])
			extend(runchem,["HCl - 33%", "WTTCHEM - 4111", "SMBS"])
			extend(runcon,[5,5,5])
		}
		if(selected_system_array.includes("Reverse Osmosis") && !selected_system_array.includes("Degasser System")){
			extend(runsystem,["RO WO DGT", "RO WO DGT", "RO WO DGT"])
			extend(runchem,["HCl - 33%","WTTCHEM - 4111", "PAC"])
			extend(runcon,[3, 3, 5])
		}
		if(selected_system_array.includes("Hardness and Silica Removal System") || selected_system_array.includes("Hardness and Color Removal System")){
			extend(runsystem,["CTS", "CTS", "CTS", "CTS", "CTS"])
			extend(runchem,["HCl - 33%", "SMBS", "WTTCHEM - 4111", "WTTCHEM - 1217", "LIME"])
			extend(runcon,[5, 10, 203, 800, 800])
		}
		if((selected_system_array.includes("Hardness and Silica Removal System") || selected_system_array.includes("Hardness and Color Removal System")) && !selected_system_array.includes("Degasser System")){
			extend(runsystem,["CTS WO DGT", "CTS WO DGT", "CTS WO DGT", "CTS WO DGT", "CTS WO DGT"])
			extend(runchem,["SODA ASH", "POLYMER - A", "HCl - 33%", "WTTCHEM - 1217", "LIME"])
			extend(runcon,[3, 2600, 203, 3570, 3570])
		}
		if(selected_system_array.includes("CTS MBR")){
			extend(runsystem,["CTS MBR", "CTS MBR"])
			extend(runchem,["PAC", "Hypochlorite"])
			extend(runcon,[84, 84])
		}
		if(selected_system_array.includes("Chlorination system")){
			extend(runsystem,["CHLORINATION", "CHLORINATION"])
			extend(runchem,["SODA ASH", "POLYMER - A"])
			extend(runcon,[3, 12750])
		}
		if(selected_system_array.includes("Reject Reverse Osmosis") && selected_system_array.includes("Degasser System")){
			extend(runsystem,["R. DGT"])
			extend(runchem,["HCl - 33%"])
			extend(runcon,[350])
		}
		if(selected_system_array.includes("Reject Reverse Osmosis")){
			extend(runsystem,["R.RO", "R.RO", "R.RO"])
			extend(runchem,["HCl - 33%", "SMBS", "WTTCHEM - 4111"])
			extend(runcon,[5, 5, 5])
		}
		console.log(runsystem)


		// var runsystem = ["NT", "BELT PRESS", "DAF", "DAF", "AN. NT", "QF","MBR (OVIVO)", "MBR (OVIVO)", "DGT", "RO", "RO", "RO", "SBT", "RO WO DGT", "RO WO DGT", "RO WO DGT","CTS", "CTS", "CTS", "CTS", "CTS","CTS WO DGT", "CTS WO DGT", "CTS WO DGT", "CTS WO DGT", "CTS WO DGT", "CHLORINATION", "CHLORINATION", "R. DGT", "R.RO", "R.RO", "R.RO"];
		// var runchem = ["H₂SO₄ - 98%", "POLYMER - C", "PAC", "POLYMER - A", "H₂SO₄ - 98%", "KMnO₄", "Hypochlorite", "PAC", "HCl - 33%", "HCl - 33%", "SMBS","WTTCHEM - 4111", "PAC","HCl - 33%", "SMBS", "WTTCHEM - 4111", "WTTCHEM - 1217", "LIME","SODA ASH", "POLYMER - A", "HCl - 33%", "WTTCHEM - 1217", "LIME", "SODA ASH", "POLYMER - A", "HCl - 33%", "CHLORINE GAS", "SMBS", "HCl - 33%", "HCl - 33%", "SMBS", "WTTCHEM - 4111"];
		// var runcon = [490, 2, 5, 5, 350, 10, 2, 30, 1250, 5, 5,3, 3, 5, 5, 10, 203, 800, 800, 3, 2600, 203, 3570, 3570, 3, 12750, 350, 70, 750, 5, 5, 5]
		for(var i=0;i<runsystem.length;i++)
		{
			var child = frm.add_child("running_chemical");
			frappe.model.set_value(child.doctype, child.name, "system",runsystem[i]);
			frappe.model.set_value(child.doctype, child.name, "chemical_name",runchem[i]);
			frappe.model.set_value(child.doctype, child.name, "concentration",runcon[i]);
			frm.refresh_field("running_chemical");
		}
		frm.clear_table("cleaning_chemical")
		frm.refresh_field("cleaning_chemical");
		var arrsystem = [];
		var arrchemical = [];
		var concen = [];
		var days = [];
		// ["MF", "MF", "MF", "MF", "MF", "MBR (KOCH)", "MBR (KOCH)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)",
		//  "RO", "RO", "RO", "RO", "RO", "RO", "RO WO DGT", "RO WO DGT", "RO WO DGT", "RO WO DGT", "RO WO DGT", "RO WO DGT", "R. MF", "R. MF", "R. MF", "R. MF", "R. MF", "R.RO", "R.RO", "R.RO"];
		// ["Hypochlorite", "Caustic flakes - 40%", "Citric acid - CG", "Nitric Acid", "HCl - 33%", 
		// "Hypochlorite", "Citric acid - CG", "Hypochlorite", "HCl - 33%", "Hypochlorite", "Caustic flakes - 40%", "Citric acid - CG", "Hypochlorite", "Caustic flakes - 40%", "Citric acid - CG", 
		// "Caustic flakes - 40%", "EDTA", "OSMOCHEM - 9126", "HCl - 33%", "Citric acid - CG", "OSMOCHEM - 7525", "Caustic flakes - 40%", "EDTA", "OSMOCHEM - 9126", "HCl - 33%", "Citric acid - CG", "OSMOCHEM - 7525", "Hypochlorite", "Caustic flakes - 40%", "Citric acid - CG", "Nitric Acid", "HCl - 33%", "HCl - 33%", "Citric acid - CG", "OSMOCHEM - 7525"];
		// // var concen = [700, 10000, 5000, 7500, 4000, 2000, 7000, 175, 550, 5900, 2380, 1150, 11650, 2380, 1160, 1170, 3000, 5000, 4440, 3000, 2500, 1170, 3000, 5000, 4440, 3000, 2500, 700, 10000, 5000, 7500, 4000, 4440, 3000, 2500];
		// var days = [1, 15, 15, 30, 30, 1, 7,0,0,0,0,0,0,0,0,15, 7, 30, 15, 7, 30, 7, 3, 15, 7, 3, 15, 1, 15, 15, 30, 20, 7, 3, 30];
		
		if(selected_system_array.includes("Micro Filtration - ASAHI")){
			extend(arrsystem,["MF", "MF", "MF", "MF", "MF"])
			extend(arrchemical,["Hypochlorite", "Caustic flakes - 40%", "Citric acid - CG", "Nitric Acid", "HCl - 33%"])
			extend(concen,[700, 10000, 5000, 7500, 4000])
			extend(days,[1, 15, 15, 30, 30])
		}
		if(selected_system_array.includes("Submerged MBR system - KOCH")){
			extend(arrsystem,["MBR (KOCH)", "MBR (KOCH)"])
			extend(arrchemical,["Hypochlorite", "Citric acid - CG"])
			extend(concen,[2000, 7000])
			extend(days,[1, 7])
		}
		if(selected_system_array.includes("Submerged MBR system - OVIVO")){
			extend(arrsystem,["MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)", "MBR (OVIVO)"])
			extend(arrchemical,["Hypochlorite", "HCl - 33%", "Hypochlorite", "Caustic flakes - 40%", "Citric acid - CG", "Hypochlorite", "Caustic flakes - 40%", "Citric acid - CG"])
			extend(concen,[175, 550, 5900, 2380, 1150, 11650, 2380, 1160])
			extend(days,[0,0,0,0,0,0,0,0])
		}
		if(selected_system_array.includes("Reverse Osmosis")){
			extend(arrsystem,["RO", "RO", "RO", "RO", "RO", "RO"])
			extend(arrchemical,["Caustic flakes - 40%", "EDTA", "OSMOCHEM - 9126", "HCl - 33%", "Citric acid - CG", "OSMOCHEM - 7525"])
			extend(concen,[1170, 3000, 5000, 4440, 3000, 2500])
			extend(days,[15, 7, 30, 15, 7, 30])
		}
		if(selected_system_array.includes("Rewolutte RO")){
			extend(arrsystem,["REW RO", "REW RO", "REW RO", "REW RO", "REW RO", "REW RO"])
			extend(arrchemical,["Caustic flakes - 40%", "EDTA", "OSMOCHEM - 9126", "HCl - 33%", "Citric acid - CG", "OSMOCHEM - 7525"])
			extend(concen,[1170, 3000, 5000, 4440, 3000, 2500])
			extend(days,[15, 7, 30, 15, 7, 30])
		}
		if(selected_system_array.includes("Reverse Osmosis") && !selected_system_array.includes("Degasser System")){
			extend(arrsystem,["RO WO DGT", "RO WO DGT", "RO WO DGT", "RO WO DGT", "RO WO DGT", "RO WO DGT"])
			extend(arrchemical,["Caustic flakes - 40%", "EDTA", "OSMOCHEM - 9126", "HCl - 33%", "Citric acid - CG", "OSMOCHEM - 7525"])
			extend(concen,[1170, 3000, 5000, 4440, 3000, 2500])
			extend(days,[7, 3, 15, 7, 3, 15])
		}
		if(selected_system_array.includes("CTS MBR")){
			extend(arrsystem,["CTS MBR", "CTS MBR", "CTS MBR", "CTS MBR", "CTS MBR", "CTS MBR", "CTS MBR", "CTS MBR"])
			extend(arrchemical,["Hypochlorite", "HCl - 33%", "Hypochlorite", "Caustic flakes - 40%", "Citric acid - CG", "Hypochlorite", "Caustic flakes - 40%", "Citric acid - CG"])
			extend(concen,[175, 550, 5900, 2380, 1150, 11650, 2380, 1160])
			extend(days,[0.5, 0.5, 30, 30, 30, 350, 350, 350])
		}
		if(selected_system_array.includes("Reject Reverse Osmosis") && selected_system_array.includes("Micro Filtration - ASAHI")){
			extend(arrsystem,["R. MF", "R. MF", "R. MF", "R. MF", "R. MF"])
			extend(arrchemical,["Hypochlorite","Caustic flakes - 40%", "Citric acid - CG", "Nitric Acid", "HCl - 33%"])
			extend(concen,[700, 10000, 5000, 7500, 4000])
			extend(days,[1, 15, 15, 30, 20])
		}
		if(selected_system_array.includes("Reject Reverse Osmosis")){
			extend(arrsystem,["R.RO", "R.RO", "R.RO"])
			extend(arrchemical,["HCl - 33%","Citric acid - CG", "OSMOCHEM - 7525"])
			extend(concen,[4440, 3000, 2500])
			extend(days,[7, 3, 30])
		}

		for(var i=0;i<arrsystem.length;i++)
		{
			var child = frm.add_child("cleaning_chemical");
			frappe.model.set_value(child.doctype, child.name, "system",arrsystem[i]);
			frappe.model.set_value(child.doctype, child.name, "chemical_name",arrchemical[i]);
			frappe.model.set_value(child.doctype, child.name, "concentration",concen[i]);
			frappe.model.set_value(child.doctype, child.name, "cleaning_frequencyday",days[i]);
			frm.refresh_field("cleaning_chemical");
		}


		frm.clear_table("consumables");
		frm.refresh_field("consumables");
		var consys=[]
		var presys=[]
		var size=[]
		var dds=[]
		if(selected_system_array.includes("Reverse Osmosis"))
		{
			consys.push("RO")
			presys.push("Bag filter")
			size.push(32)
			dds.push(30.00)

			consys.push("RO")
			presys.push("Cartridge filter - W")
			size.push(40)
			dds.push(30.00)

			consys.push("RO WO")
			presys.push("Bag filter")
			size.push(32)
			dds.push(20.00)
			
			consys.push("RO WO")
			presys.push("Cartridge filter - W")
			size.push(40)
			dds.push(20.00)
		}
		if(selected_system_array.includes("Rewolutte RO"))
		{
			consys.push("REW RO")
			presys.push("Bag filter")
			size.push(32)
			dds.push(30.00)

			consys.push("REW RO")
			presys.push("Cartridge filter - W")
			size.push(40)
			dds.push(30.00)
		}
		if(selected_system_array.includes("Reject Reverse Osmosis"))
		{
			consys.push("R.RO")
			presys.push("Cartridge filter - W")
			size.push(40)
			dds.push(30.00)
		}
		// var consys = ["RO", "RO", "RO WO", "RO WO", "R.RO"];
		// var presys = ["Bag filter", "Cartridge filter - W", "Bag filter", "Cartridge filter - W", "Cartridge filter - W"];
		// var size = [32, 40, 32, 40, 40];
		// var dds = [30.00, 30.00, 20.00, 20.00, 30.00];
		for(var i=0;i<consys.length;i++)
		{
			var child = frm.add_child("consumables");
			frappe.model.set_value(child.doctype, child.name, "system",consys[i]);
			frappe.model.set_value(child.doctype, child.name, "prefilter",presys[i]);
			frappe.model.set_value(child.doctype, child.name, "size",size[i]);
			frappe.model.set_value(child.doctype, child.name, "replacing_fre",dds[i]);
			frm.refresh_field("consumables");
		}
	}
});

var extend = function (ar1,otherArray) {
    for (var i = 0; i < otherArray.length; i++) {
        ar1.push(otherArray[i]);
    }
}
var handle_ro_fields = function(frm){
	var selected_system_array = [];
	$.each(frm.doc.selected_system || [], function(i, v) {
		selected_system_array.push(v.selected_system_name);
	});
	// console.clear()
	if(selected_system_array.includes("Reverse Osmosis") && selected_system_array.includes("Degasser System")){
		if(frm.doc.ro_without==1){
			frm.set_value("ro_without_dgt",0);
			frm.refresh_field("ro_without_dgt");			
		}
		frm.set_df_property("ro_without_dgt_section","hidden",1);
	}
	else if(selected_system_array.includes("Reverse Osmosis") && !selected_system_array.includes("Degasser System")){
		if(frm.doc.ro_without!=1){
			frm.set_value("ro_without_dgt",1);
			frm.refresh_field("ro_without_dgt");			
		}
		frm.set_df_property("ro_with_dgt_section","hidden",1);
	}
}
