// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Emergency Leave', {
	get_leave:function(frm,cdt,cdn){
		frappe.call({
			"method":"wtt_module.wtt_module.doctype.leave_request.leave_request.get_leave",
			args:{
				"month":frm.doc.month,
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
	setup: function(frm,cdt,cdn) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
		
	},
});


frappe.ui.form.on('Emergency Table', {
	
	from_date:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt,cdn,"to_date",child.from_date)
		refresh_field("to_date")

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