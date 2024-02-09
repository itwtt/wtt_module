// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sulphur Black Removal', {
	mbr_tank_volume:function(frm){
		if(frm.doc.mbr_tank_volume!=undefined && frm.doc.no_of_drains_per_day!=undefined && frm.doc.no_of_trains!=undefined){
			calculate_volume_drained(frm)
		}
	},
	no_of_drains_per_day:function(frm){
		if(frm.doc.mbr_tank_volume!=undefined && frm.doc.no_of_drains_per_day!=undefined && frm.doc.no_of_trains!=undefined){
			calculate_volume_drained(frm)
		}
	},
	no_of_trains:function(frm){
		if(frm.doc.mbr_tank_volume!=undefined && frm.doc.no_of_drains_per_day!=undefined && frm.doc.no_of_trains!=undefined){
			calculate_volume_drained(frm)
		}
	},
	volume_drained_in_a_day:function(frm){
		if(frm.doc.volume_drained_in_a_day!=undefined && frm.doc.suspends_mgl!=undefined){
			calculate_suspends_kgday(frm)
		}
		if(frm.doc.volume_drained_in_a_day!=undefined && frm.doc.sludge_pump_operating_hours!=undefined && frm.doc.pac_dosage!=undefined && frm.doc.pac_concentration!=undefined){
			calculate_dosing_pump(frm);
		}
		
		calculate_lamella_settler(frm);
	},
	suspends_mgl:function(frm){
		if(frm.doc.volume_drained_in_a_day!=undefined && frm.doc.suspends_mgl!=undefined){
			calculate_suspends_kgday(frm)
		}
		if(frm.doc.total_reject_flow_rate_m3day!=undefined && frm.doc.suspends_mgl!=undefined){
			calculate_suspends_kgday2(frm)
		}
	},
	suspends_kgday:function(frm){
		if(frm.doc.suspends_kgday!=undefined && frm.doc.sludge_concentration!=undefined){
			calculate_volume_of_sludge(frm);
		}
	},
	sludge_concentration:function(frm){
		if(frm.doc.suspends_kgday!=undefined && frm.doc.sludge_concentration!=undefined){
			calculate_volume_of_sludge(frm);
		}
	},
	volume_of_sludge_m3day:function(frm){
		if(frm.doc.volume_of_sludge_m3day!=undefined && frm.doc.sludge_pump_operating_hours!=undefined){
			calculate_sludge_pump_capacity(frm);
		}
		if(frm.doc.volume_of_sludge_m3day!=undefined && frm.doc.sludge_pump_operating_hours!=undefined && frm.doc.pac_dosage!=undefined && frm.doc.pac_concentration!=undefined){
			calculate_dosing_pump(frm);
		}
		calculate_lamella_settler(frm);
	},
	sludge_pump_operating_hours:function(frm){
		if(frm.doc.volume_of_sludge_m3day!=undefined && frm.doc.sludge_pump_operating_hours!=undefined){
			calculate_sludge_pump_capacity(frm);
		}
		if(frm.doc.volume_drained_in_a_day!=undefined && frm.doc.sludge_pump_operating_hours!=undefined && frm.doc.pac_dosage!=undefined && frm.doc.pac_concentration!=undefined){
			calculate_dosing_pump(frm);
		}
		if(frm.doc.volume_of_sludge_m3day!=undefined && frm.doc.sludge_pump_operating_hours!=undefined && frm.doc.pac_dosage!=undefined && frm.doc.pac_concentration!=undefined){
			calculate_dosing_pump(frm);
		}
	},
	pac_dosage:function(frm){
		if(frm.doc.volume_drained_in_a_day!=undefined && frm.doc.sludge_pump_operating_hours!=undefined && frm.doc.pac_dosage!=undefined && frm.doc.pac_concentration!=undefined){
			calculate_dosing_pump(frm);
		}
		if(frm.doc.volume_of_sludge_m3day!=undefined && frm.doc.sludge_pump_operating_hours!=undefined && frm.doc.pac_dosage!=undefined && frm.doc.pac_concentration!=undefined){
			calculate_dosing_pump(frm);
		}
	},
	pac_concentration:function(frm){
		if(frm.doc.volume_drained_in_a_day!=undefined && frm.doc.sludge_pump_operating_hours!=undefined && frm.doc.pac_dosage!=undefined && frm.doc.pac_concentration!=undefined){
			calculate_dosing_pump(frm);
		}
		if(frm.doc.volume_of_sludge_m3day!=undefined && frm.doc.sludge_pump_operating_hours!=undefined && frm.doc.pac_dosage!=undefined && frm.doc.pac_concentration!=undefined){
			calculate_dosing_pump(frm);
		}
	},
	total_reject_flow_rate_m3hr:function(frm){
		if(frm.doc.total_reject_flow_rate_m3hr!=undefined && frm.doc.hours_of_operation_hours!=undefined){
			calculate_total_reject_flow_rate_m3day(frm);
		}
	},
	hours_of_operation_hours:function(frm){
		if(frm.doc.total_reject_flow_rate_m3hr!=undefined && frm.doc.hours_of_operation_hours!=undefined){
			calculate_total_reject_flow_rate_m3day(frm);
		}
	}
});
var calculate_volume_drained=function(frm){
	var drain=0;
	if(frm.doc.category=='KOCH-MBR' || frm.doc.category=='OVIVO-MBR'){
		drain = frm.doc.mbr_tank_volume*frm.doc.no_of_drains_per_day*frm.doc.no_of_trains;
		frm.set_value("volume_drained_in_a_day",drain);
		frm.refresh_field("volume_drained_in_a_day");
	}

}
var calculate_suspends_kgday = function(frm) {
	var value = 0;
	if(frm.doc.category=='KOCH-MBR' || frm.doc.category=='OVIVO-MBR'){
		value = (frm.doc.volume_drained_in_a_day*frm.doc.suspends_mgl)/1000;
		frm.set_value("suspends_kgday",value);
		frm.refresh_field("suspends_kgday");
	}
}
var calculate_suspends_kgday2 = function(frm) {
	var value = 0;
	if(frm.doc.category=='ASAHI KASEI-MF'){
		value = (frm.doc.total_reject_flow_rate_m3day*frm.doc.suspends_mgl)/1000;
		frm.set_value("suspends_kgday",value);
		frm.refresh_field("suspends_kgday");
	}
}
var calculate_volume_of_sludge = function(frm){
	var value = 0;
	value = (frm.doc.suspends_kgday/frm.doc.sludge_concentration)*100;
	frm.set_value("volume_of_sludge_kgday",value);
	frm.refresh_field("volume_of_sludge_kgday");

	frm.set_value("volume_of_sludge_m3day",value/1000);
	frm.refresh_field("volume_of_sludge_m3day");
	
}
var calculate_sludge_pump_capacity = function(frm){
	var value = 0;
	value = frm.doc.volume_of_sludge_m3day/frm.doc.sludge_pump_operating_hours;
	frm.set_value("sludge_pump_capacity",value);
	frm.refresh_field("sludge_pump_capacity");
	
}
var calculate_lamella_settler = function(frm){
	var value=0;
	if(frm.doc.category=='KOCH-MBR' || frm.doc.category=='OVIVO-MBR'){
		if(frm.doc.volume_drained_in_a_day/18<=5){value=5;}
		else if(frm.doc.volume_drained_in_a_day/18<=10){value=10;}
		else if(frm.doc.volume_drained_in_a_day/18<=15){value=15;}
		else if(frm.doc.volume_drained_in_a_day/18<=20){value=20;}
		frm.set_value("lamella_settler",value);
		frm.refresh_field("lamella_settler");
	}
	if(frm.doc.category=='ASAHI KASEI-MF'){
		if(frm.doc.volume_of_sludge_m3day/18<=5){value=5;}
		else if(frm.doc.volume_of_sludge_m3day/18<=10){value=10;}
		else if(frm.doc.volume_of_sludge_m3day/18<=15){value=15;}
		else if(frm.doc.volume_of_sludge_m3day/18<=20){value=20;}
		frm.set_value("lamella_settler",value);
		frm.refresh_field("lamella_settler");
	}
}
var calculate_dosing_pump=function(frm){
	var value=0;
	if(frm.doc.category=='KOCH-MBR' || frm.doc.category=='OVIVO-MBR'){
		value = (((frm.doc.pac_dosage/frm.doc.pac_concentration)*100)*frm.doc.volume_drained_in_a_day)/(frm.doc.sludge_pump_operating_hours*1000);
		frm.set_value("dosing_pump",value);
		frm.refresh_field("dosing_pump");
	}
	if(frm.doc.category=='ASAHI KASEI-MF'){
		value = (((frm.doc.pac_dosage/frm.doc.pac_concentration)*100)*frm.doc.volume_of_sludge_m3day)/(frm.doc.sludge_pump_operating_hours*1000);
		frm.set_value("dosing_pump",value);
		frm.refresh_field("dosing_pump");
	}
}
var calculate_total_reject_flow_rate_m3day = function(frm){
	var value = 0;
	if(frm.doc.category=='ASAHI KASEI-MF'){
		value = frm.doc.total_reject_flow_rate_m3hr*frm.doc.hours_of_operation_hours;
		frm.set_value("total_reject_flow_rate_m3day",value);
		frm.refresh_field("total_reject_flow_rate_m3day");
	}
}