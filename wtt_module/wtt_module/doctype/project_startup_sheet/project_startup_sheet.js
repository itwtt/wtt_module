// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Startup Sheet', {
	refresh: function(frm) {

	},
	validate:function(frm){
		frm.set_value("bod_value",((frm.doc.flow*frm.doc.bod)/1000));
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
			frm.set_value("designing",((frm.doc.real_o2_hr/frm.doc.des_per)*100));
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

		frm.set_value("ret_in_day_dt",(frm.doc.ret_in_hr_dt/24));
		frm.refresh_field("ret_in_day_dt");
		var ar_val1=(frm.doc.flow*frm.doc.ret_in_day_dt)/frm.doc.tank_height;
		frm.set_value("area_dt",ar_val1);
		frm.refresh_field("area_dt");
		frm.set_value("diffuser_dt",(ar_val1/frm.doc.div_point_diffuser));
		frm.refresh_field("diffuser_dt");

		frm.set_value("ret_in_day_srs",(frm.doc.ret_in_hr_srs/24));
		frm.refresh_field("ret_in_day_srs");
		var ar_val2=(frm.doc.flow*frm.doc.ret_in_day_srs)/frm.doc.tank_height;
		frm.set_value("area_srs",ar_val2);
		frm.refresh_field("area_srs");
		frm.set_value("diffuser_srs",(ar_val2/frm.doc.div_point_diffuser));
		frm.refresh_field("diffuser_srs");

		frm.set_value("ret_in_day_cft",(frm.doc.ret_in_hr_cft/24));
		frm.refresh_field("ret_in_day_cft");
		var ar_val3=(frm.doc.flow*frm.doc.ret_in_day_cft)/frm.doc.tank_height;
		frm.set_value("area_cft",ar_val3);
		frm.refresh_field("area_cft");
		frm.set_value("diffuser_cft",(ar_val3/frm.doc.div_point_diffuser));
		frm.refresh_field("diffuser_cft");

		frm.set_value("ret_in_day_nt",(frm.doc.ret_in_hr_nt/24));
		frm.refresh_field("ret_in_day_nt");
		var ar_val4=(frm.doc.flow*frm.doc.ret_in_day_nt)/frm.doc.tank_height;
		frm.set_value("area_nt",ar_val4);
		frm.refresh_field("area_nt");
		frm.set_value("diffuser_nt",(ar_val4/frm.doc.div_point_diffuser));
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
		frm.set_value("blower_cpa",frm.doc.designing + (frm.doc.eqtk*2) + (frm.doc.only_air*2));
		frm.refresh_field("blower_cpa");
		frm.set_value("total_diffusers",frm.doc.eqtk + frm.doc.only_air + frm.doc.bio_tank);
		frm.refresh_field("total_diffusers");
		frm.set_value("each_blower",frm.doc.blower_cpa/frm.doc.total_blower);
		frm.refresh_field("each_blower");

		frm.set_value("influent_flow_rate_to_be_treated",frm.doc.flow*(1+(frm.doc.design_clarifier/100)));
		frm.refresh_field("influent_flow_rate_to_be_treated");
		frm.set_value("ras_flow_rate_per_clarifier",frm.doc.enter_ras_flow_rate/frm.doc.enter_number_of_clarifiers_in_service);
		frm.refresh_field("ras_flow_rate_per_clarifier");
		frm.set_value("ras_flow_rate_percentage",(frm.doc.flow/frm.doc.ras_flow_rate_per_clarifier)*100);
		frm.refresh_field("ras_flow_rate_percentage");
		frm.set_value("calculate_surface_area",0.785*Math.pow(frm.doc.enter_tank_diameter,2));
		frm.refresh_field("calculate_surface_area");
		frm.set_value("calculate_clarifier_volume",frm.doc.calculate_surface_area*frm.doc.enter_side_water_depth);
		frm.refresh_field("calculate_clarifier_volume");
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
		frm.set_value("modules_per_loop",rounded/frm.doc.no_of_loops);
		frm.refresh_field("modules_per_loop");
		frm.set_value("feed_pump",(rounded * frm.doc.mf_for_feed_flow)/frm.doc.feed_qty);
		frm.refresh_field("feed_pump");
		if(frm.doc.loop_operation=="Single")
		{
			frm.set_value("bw_pump",(frm.doc.mf_for_bw_flow * rounded)/frm.doc.bw_qty);
			frm.refresh_field("bw_pump");
			frm.set_value("cip_pump",rounded * frm.doc.mf_for_cip_flow);
			frm.refresh_field("cip_pump");
			frm.set_value("air_flow",rounded * frm.doc.mf_for_air_flow);
			frm.refresh_field("air_flow");
			frm.set_value("feed_qty",1);
			frm.refresh_field("feed_qty");
			frm.set_value("bw_qty",0);
			frm.refresh_field("bw_qty");
		}
		else
		{
			frm.set_value("bw_pump",(frm.doc.modules_per_loop*frm.doc.mf_for_bw_flow)/frm.doc.bw_qty);
			frm.refresh_field("bw_pump");
			frm.set_value("cip_pump",(rounded * frm.doc.mf_for_cip_flow)/frm.doc.no_of_loops);
			frm.refresh_field("cip_pump");
			frm.set_value("air_flow",(rounded * frm.doc.mf_for_air_flow)/frm.doc.no_of_loops);
			frm.refresh_field("air_flow");
			frm.set_value("feed_qty",2);
			frm.refresh_field("feed_qty");
			frm.set_value("bw_qty",1);
			frm.refresh_field("bw_qty");
		}
		frm.set_value("actual_area",rounded*frm.doc.area);
		frm.refresh_field("actual_area");
		frm.set_value("actual_flux",(frm.doc.permeate_flow *1000)/frm.doc.actual_area);
		frm.refresh_field("actual_flux");
		frm.set_value("mbr_permeate_flow",frm.doc.permeate_capacity/frm.doc.mbr_operating_hours);
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

		if(frm.doc.sludge_pit=="Required")
		{
			var exact_time=60;
		}
		else
		{
			var exact_time=20;
		}
		var slud = (water_volume / frm.doc.design_no_of_trains) * (60/exact_time);
		var cirt = ((frm.doc.permeate_capacity * 4)/24)/ (frm.doc.design_no_of_trains);
		if(frm.doc.mbr_type=="SUB-UF")
		{
			frm.set_value("mbr_sludge_pump",slud/frm.doc.design_no_of_trains);
			frm.set_value("mbr_circulation_pump",0);
		}
		else
		{
			frm.set_value("mbr_sludge_pump",0);
			frm.set_value("mbr_circulation_pump",cirt);
		}

		if(frm.doc.mbr_type=="SUB-UF")
		{
			var fd_value = (frm.doc.permeate_capacity/(24*0.9))/frm.doc.design_no_of_trains;
			frm.set_value("mbr_feed_pump",fd_value);
		}
		else
		{
			var fd_value = (frm.doc.permeate_capacity*5/24)/frm.doc.design_no_of_trains;
			frm.set_value("mbr_feed_pump",fd_value);
		}
		var cip_train = ((frm.doc.mbr_cip_flux * frm.doc.design_total_area)/(frm.doc.design_no_of_trains * 1000))/frm.doc.design_no_of_trains;
		frm.set_value("mbr_cip_pump__train",cip_train);
		var brain=(frm.doc.mbr_air_req_membrane_row * frm.doc.mbr_membrane_modules * frm.doc.design_total_no_of_modules)/(frm.doc.design_no_of_trains)*(frm.doc.design_no_of_trains);
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
		var cip=Math.max((frm.doc.permeate_capacity * (0.7/100)),(frm.doc.mbr_cip_pump__train * 45/60)*1000);
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

		frm.set_value("sludge_pro",fin);
		frm.refresh_field("sludge_pro");

		frm.set_value("ras",((frm.doc.flow*(frm.doc.mlss-frm.doc.tss))-(divfin*1000))/(frm.doc.tss_cf_waste-frm.doc.mlss));
		frm.refresh_field("ras");

		frm.set_value("was",(frm.doc.flow*(frm.doc.tss-frm.doc.tss_cf_eff)+(divfin*1000))/(frm.doc.tss_cf_waste-frm.doc.tss_cf_eff));
		frm.refresh_field("was");

		frm.set_value("without_mechanism",(frm.doc.was/20));
		var s=(8000*frm.doc.was)/1000;
		var t=(s*1000)/15000;
		frm.set_value("with_mechanism",(t/20));
		frm.refresh_field("with_mechanism");

		frm.set_value("pump_qty",frm.doc.design_modules_train);
		frm.refresh_field("pump_qty");

		frm.set_value("circulation_pump_qty",frm.doc.design_modules_train);
		frm.refresh_field("circulation_pump_qty");

		frm.set_value("feed_pump_qty",frm.doc.design_modules_train);
		frm.refresh_field("feed_pump_qty");

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
	},
	enquiry_no:function(frm){
		frappe.db.get_value("Process Enquiry Sheet", {"name": frm.doc.enquiry_no}, "capacity_to_be_treated_avg", function(value) {
		frm.set_value("flow",value.capacity_to_be_treated_avg);
		frm.refresh_field("flow");
		});
		frappe.call({
				method:"wtt_module.wtt_module.doctype.project_startup_sheet.project_startup_sheet.get_all_value",
				args:{
					enq:frm.doc.enquiry_no
				},
				callback(r){
					frm.set_value("tss",r.message[0].tss);
					frm.set_value("cod",r.message[1].cod);
					frm.set_value("bod",r.message[2].bod);
					frm.refresh_field("tss");
					frm.refresh_field("cod");
					frm.refresh_field("bod");
				}
			});
	}
});
