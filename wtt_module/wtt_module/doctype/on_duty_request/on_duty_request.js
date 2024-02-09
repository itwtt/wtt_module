// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('On duty request', {
	setup: function(frm,cdt,cdn) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
		
	},
	// validate(frm) {
	//     function onPositionRecieved(position){
	//         var longitude= position.coords.longitude;
	//         var latitude= position.coords.latitude;
	//         frm.set_value('longitude',longitude);
	//         frm.set_value('latitude',latitude);
	//         console.log(longitude);
	//         console.log(latitude);
	//         fetch('https://api.opencagedata.com/geocode/v1/json?q='+latitude+'+'+longitude+'&key=de1bf3be66b546b89645e500ec3a3a28')
	//          .then(response => response.json())
 //            .then(data => {
 //                var city=data['results'][0].components.city;
 //                var state=data['results'][0].components.state;
 //                var area=data['results'][0].components.residential;
 //                frm.set_value('city',city);
 //                frm.set_value('state',state);
 //                frm.set_value('area',area);
 //                console.log(data);
 //            })
 //            .catch(err => console.log(err));
	//         frm.set_df_property('my_location','options','<div class="mapouter"><div class="gmap_canvas"><iframe width=100% height="300" id="gmap_canvas" src="https://maps.google.com/maps?q='+latitude+','+longitude+'&t=&z=17&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe><a href="https://yt2.org/youtube-to-mp3-ALeKk00qEW0sxByTDSpzaRvl8WxdMAeMytQ1611842368056QMMlSYKLwAsWUsAfLipqwCA2ahUKEwiikKDe5L7uAhVFCuwKHUuFBoYQ8tMDegUAQCSAQCYAQCqAQdnd3Mtd2l6"></a><br><style>.mapouter{position:relative;text-align:right;height:300px;width:100%;}</style><style>.gmap_canvas {overflow:hidden;background:none!important;height:300px;width:100%;}</style></div></div>');
 //            frm.refresh_field('my_location');
	//     }
	    
	//     function locationNotRecieved(positionError){
	//         console.log(positionError);
	//     }
	    
	//     if(frm.doc.longitude && frm.doc.latitude){
	//         frm.set_df_property('my_location','options','<div class="mapouter"><div class="gmap_canvas"><iframe width=100% height="300" id="gmap_canvas" src="https://maps.google.com/maps?q='+frm.doc.latitude+','+frm.doc.longitude+'&t=&z=17&ie=UTF8&iwloc=&output=embed" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe><a href="https://yt2.org/youtube-to-mp3-ALeKk00qEW0sxByTDSpzaRvl8WxdMAeMytQ1611842368056QMMlSYKLwAsWUsAfLipqwCA2ahUKEwiikKDe5L7uAhVFCuwKHUuFBoYQ8tMDegUAQCSAQCYAQCqAQdnd3Mtd2l6"></a><br><style>.mapouter{position:relative;text-align:right;height:300px;width:100%;}</style><style>.gmap_canvas {overflow:hidden;background:none!important;height:300px;width:100%;}</style></div></div>');
 //            frm.refresh_field('my_location');
	//     } else {
	//         if(navigator.geolocation){
	//             navigator.geolocation.getCurrentPosition(onPositionRecieved,locationNotRecieved,{ enableHighAccuracy: true});
	//         }
	//     }
 //    },
	from_time: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
		frm.events.check_date(frm);
	},
	check_date:function(frm){
		return frappe.call({
				method: 'check_date',
				doc: frm.doc,
				
			});
	},

	to_time: function(frm, cdt, cdn) {
		var time_diff = (moment(frm.doc.to_time).diff(moment(frm.doc.from_time),"seconds")) / ( 60 * 60 * 24);
		var std_working_hours = 0;

		if(frm._setting_hours) return;

		var hours = moment(frm.doc.to_time).diff(moment(frm.doc.from_time), "seconds") / 3600;
		std_working_hours = time_diff * frappe.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			frm.set_value("hours", std_working_hours);
		} else {
			frm.set_value("hours", hours);
		}
	},
	hours: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	}
});

var calculate_end_time = function(frm, cdt, cdn) {
	if(!frm.doc.from_time) {
		// if from_time value is not available then set the current datetime
		frm.set_value("from_time", frappe.datetime.get_datetime_as_string());
	}

	let d = moment(frm.doc.from_time);
	if(frm.doc.hours) {
		var time_diff = (moment(frm.doc.to_time).diff(moment(frm.doc.from_time),"seconds")) / (60 * 60 * 24);
		var std_working_hours = 0;
		var hours = moment(frm.doc.to_time).diff(moment(frm.doc.from_time), "seconds") / 3600;

		std_working_hours = time_diff * frappe.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			frm.set_value("hours", std_working_hours);
			frm.set_value("to_time", d.add(hours, "hours").format(frappe.defaultDatetimeFormat));
		} else {
			d.add(frm.doc.hours, "hours");
			frm._setting_hours = true;
			frm.set_value("to_time",
				d.format(frappe.defaultDatetimeFormat)).then(() => {
				frm._setting_hours = false;
			});
		}
	}
};