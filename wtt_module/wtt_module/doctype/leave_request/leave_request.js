// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt
frappe.ui.form.on('Leave Request', {
	setup: function(frm,cdt,cdn) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});		
	},
	get_leave:function(frm){
		frappe.call({
			"method":"wtt_module.wtt_module.doctype.leave_request.leave_request.get_leave",
			args:{
				"month":frm.doc.month,
				"year":frm.doc.year,
				"emp":frm.doc.employee
			},
			callback(r){
				for(var i=0;i<=r.message.length;i++){
				var html='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>' 
				html+="<table border='1px' width=100% text-align='center'><tr><th>Date</th><th>Leave Type</th><th>Record</th><th>REQUEST</th></tr>"
				$.each(r.message, function(i, v) {
				html+="<tr style='text-align:center;';><td>"+v.from_date+"</td><td>"+v.leave_type+"</td><td>"+v.remarks+"</td><td>"+v.request+"</td></tr>"
				})
				}
				$(frm.fields_dict['html'].wrapper).html(html)
			}
		});
	},
	refresh:function(frm){
		if(frappe.session.user=='venkat@wttindia.com'|| frappe.session.user=='sarnita@wttindia.com' || frappe.session.user=='harshini@wttindia.com' || frappe.session.user=='priya@wttindia.com' || frappe.session.user=='Administrator'){
			frm.set_df_property("proceed_to_take_leave","hidden",0);
		}
		if(frm.doc.employee==undefined){
			$(frm.fields_dict['html'].wrapper).html("")
			$(frm.fields_dict['check_leave'].wrapper).html("")
		}
		else{
			get_leaves_available(frm)
		}
	},
	onload:function(frm){
		if(frm.doc.employee==undefined){
			$(frm.fields_dict['html'].wrapper).html("")
			$(frm.fields_dict['check_leave'].wrapper).html("")
		}
		else{
			get_leaves_available(frm)
		}
	},
	employee:function(frm){
		if(frm.doc.employee==undefined){
			$(frm.fields_dict['html'].wrapper).html("")
			$(frm.fields_dict['check_leave'].wrapper).html("")
		}
		else{
			get_leaves_available(frm)
		}
	},
	year:function(frm){
		if(frm.doc.employee==undefined){
			$(frm.fields_dict['html'].wrapper).html("")
			$(frm.fields_dict['check_leave'].wrapper).html("")
		}
		else{
			get_leaves_available(frm)
		}
	}

});
frappe.ui.form.on('Leave table', {
	// leave_type:function(frm,cdt,cdn){
	// 	var child = locals[cdt][cdn];
	// 	frappe.call({
	// 		method:"casual_leave_availability",
	// 		doc:frm.doc,
	// 		callback(r){
	// 			if(r.message=="error"){
	// 				frappe.model.set_value(cdt, cdn, "leave_type","Leave Without Pay");
	// 				refresh_field("leave_type");
	// 				msgprint("This Casual Leave is Not Available for You")
	// 			}
	// 		}
	// 	})
	// },
	from_date:function(frm,cdt,cdn){
		
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt,cdn,"to_date",child.from_date)
		refresh_field("to_date");
		const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
		var set_month = month[new Date(child.from_date).getMonth()];
		frm.set_value("month",set_month);
		frm.refresh_field("month");

	},
	to_date: function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	if(child.day=="Half day (FN)" || child.day=="Half day (AN)")
{
frappe.model.set_value(cdt, cdn, "no_of_days",(frappe.datetime.get_day_diff(child.to_date,child.from_date)+1)-0.5);
refresh_field("no_of_days");
}
else
{
frappe.model.set_value(cdt, cdn, "no_of_days",frappe.datetime.get_day_diff(child.to_date,child.from_date)+1);
refresh_field("no_of_days");	
}	
},
day:function(frm,cdt,cdn)
{
var child = locals[cdt][cdn];
if(child.day=="Half day (FN)" || child.day=="Half day (AN)")
{
frappe.model.set_value(cdt, cdn, "no_of_days",(frappe.datetime.get_day_diff(child.to_date,child.from_date)+1)-0.5);
refresh_field("no_of_days");
}
else
{
frappe.model.set_value(cdt, cdn, "no_of_days",frappe.datetime.get_day_diff(child.to_date,child.from_date)+1);
refresh_field("no_of_days");	
}
}
});
var get_leaves_available = function (frm) {
	$(frm.fields_dict['html'].wrapper).html("")
	$(frm.fields_dict['check_leave'].wrapper).html("")
	frappe.call({
		method:"wtt_module.wtt_module.doctype.leave_request.leave_request.check_leave",
		args:{
			"emp":frm.doc.employee,
			"year":frm.doc.year
		},
		callback(r){
			console.log(r.message)
			if(r.message.length>0){
				for(var i=0;i<=r.message.length;i++){
					var html='<style>th{font-size: 15px;text-align:center;}</style>' 
					$.each(r.message, function(i, v) {
					if(i==0){
						if(v.balance_leave>0){
							html+="<table border='1px' width=75% text-align='center'><tr><th colspan='2'>Sick Leave</th><th colspan='2'>Earned Leave</th><th colspan='2'>Casual Leave</th><th>Balance Leave</th></tr>"
							html+="<tr style='text-align:center;'><td><b>Total</b></td><td><b>Taken</b></td><td><b>Total</b></td><td><b>Taken</b></td><td><b>Total</b></td><td><b>Taken</b></td><td><b>From 2022</b></td></tr>"
						}
						else{
							html+="<table border='1px' width=75% text-align='center'><tr><th colspan='2'>Sick Leave</th><th colspan='2'>Earned Leave</th><th colspan='2'>Casual Leave</th></tr>"
							html+="<tr style='text-align:center;'><td><b>Total</b></td><td><b>Taken</b></td><td><b>Total</b></td><td><b>Taken</b></td><td><b>Total</b></td><td><b>Taken</b></td></tr>"
						}							
					}
					var tol_sl=0
					var tol_cl=0
					if(v.total_cl>6)
					{
						tol_cl=6
					}
					else
					{
						tol_cl=v.total_cl
					}

					if(v.total_sl>6)
					{
						tol_sl=6
					}
					else
					{
						tol_sl=v.total_sl
					}
					html+="<tr style='text-align:center;';><td>"+tol_sl+"</td><td>"+v.sl_taken+"</td><td>"+v.total_el+"</td><td>"+v.el_taken+"</td><td>"+tol_cl+"</td><td>"+v.cl_taken+"</td>"
					if(v.balance_leave>0){
						html+="<td>"+v.balance_leave+"</td>"
					}
					html+="</tr>"
					})
				}
				html+="<br><h6 style='color:green'>As soon as the salary slip for this month is approved, the casual leave will be updated.</h6>"
				$(frm.fields_dict['check_leave'].wrapper).html(html)
			}
			else{
				$(frm.fields_dict['check_leave'].wrapper).html("")
			}
		}
	});
	// $(frm.fields_dict['html'].wrapper).html("")
	// frappe.call({
	// 	method:"wtt_module.wtt_module.doctype.leave_request.leave_request.check_leave",
	// 	args:{
	// 		"emp":frm.doc.employee
	// 	},
	// 	callback(r){
	// 		console.log(r.message)
	// 		if(r.message.length>0){
	// 			for(var i=0;i<=r.message.length;i++){
	// 				var html='<style>th{font-size: 15px;text-align:center;}</style>' 
	// 				$.each(r.message, function(i, v) {
	// 				if(i==0){
	// 					if(v.balance_leave>0){
	// 						html+="<table border='1px' width=75% text-align='center'><tr><th colspan='3'>Sick Leave</th><th colspan='3'>Casual Leave</th><th>Balance Leave</th></tr>"
	// 						html+="<tr style='text-align:center;'><td><b>Total</b></td><td><b>Taken</b></td><td><b>Applied</b></td><td><b>Total</b></td><td><b>Taken</b></td><td><b>Applied</b></td><td><b>From 2022</b></td></tr>"
	// 					}
	// 					else{
	// 						html+="<table border='1px' width=75% text-align='center'><tr><th colspan='3'>Sick Leave</th><th colspan='3'>Casual Leave</th></tr>"
	// 						html+="<tr style='text-align:center;'><td><b>Total</b></td><td><b>Taken</b></td><td><b>Applied</b></td><td><b>Total</b></td><td><b>Taken</b></td><td><b>Applied</b></td></tr>"
	// 					}							
	// 				}
	// 				html+="<tr style='text-align:center;';><td>"+v.total_sl+"</td><td>"+v.sl_taken+"</td><td>"+v.sl_applied+"</td><td>"+v.total_cl+"</td><td>"+v.cl_taken+"</td><td>"+v.cl_applied+"</td>"
	// 				if(v.balance_leave>0){
	// 					html+="<td>"+v.balance_leave+"</td>"
	// 				}
	// 				html+="</tr>"
	// 				})
	// 			}
	// 			html+="<br><h6 style='color:green'>As soon as the salary slip for this month is approved, the casual leave will be updated.</h6>"
	// 			$(frm.fields_dict['check_leave'].wrapper).html(html)
	// 		}
	// 		else{
	// 			$(frm.fields_dict['check_leave'].wrapper).html("")
	// 		}
	// 	}
	// });
}
