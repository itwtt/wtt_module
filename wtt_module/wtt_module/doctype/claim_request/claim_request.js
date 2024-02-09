// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Claim Request', {
	setup:function(frm){
		frm.set_query('employee',function(){
			return{
				filters:{status:"Active"}
			}
		})
	},
	refresh:function(frm){
		frm.set_df_property("od_ref","hidden",0);
		if(frappe.session.user=='gm_admin@wttindia.com' || frappe.session.user=='Administrator'){
			frm.set_df_property("approve_claim","hidden",0);	
		}
		else{
			frm.set_df_property("approve_claim","hidden",1);		
		}
		
		$(frm.fields_dict['od'].wrapper).html('')
	},
	onload:function(frm){
		if(frappe.session.user!='Administrator'){
			frm.set_df_property("od_ref","hidden",1);
		}
	},
	od_ref:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		var arr=[]
		$.each(frm.doc.expenses || [], function(i, v) {
			arr.push({"date":v.expense_date})
				
		});
		frappe.call({
			"method":"wtt_module.wtt_module.doctype.claim_request.claim_request.check_od",
			args:{
				'arr':arr,
				'emp':frm.doc.employee
			},
			callback: function(r) {
				var htvalue='<style>th{font-size: 15px;text-align:center;color:tomato;}</style>'
			htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:10%'>DATE</th><th style='width:7%'>HOURS</th><th style='width:15%'>REASON</th><th style='width:10%'>REQUEST</th><th style='width:5%'>STATUS</th></tr>"
			$.each(r.message, function(i, v) {				
				htvalue+='<tr style="text-align:center;padding:100%"><td align="center">'+(i+1)+'<br></td><td align="center">'+v.from_time+'</td><td align="center">'+v.hours+' Hours</td><td align="center">'+v.reason+'<br></td><td align="center">'+v.od_name+'<br></td><td align="center">'+v.status+'<br></td></tr>'
			});
			$(frm.fields_dict['od'].wrapper).html(htvalue)
			}
		});
	},
	reject_claim:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		$.each(frm.doc.expenses || [], function(i, v) {
			if(v.__checked==true){
				v.status='Rejected';
				frm.refresh_field("expenses")
				frm.dirty()
			}
		});
		frm.save()
	},
	validate:function(frm){
		var total=0;
		$.each(frm.doc.expenses || [],function(i,d){
			if(d.status!='Rejected'){
				total+=flt(d.amount);
			}
		});
		frm.set_value('grand_total',total);
	},
	// setup:function(frm){
	// frm.set_indicator_formatter('expence_date',
	// 		function(doc) { return (doc.status=='Rejected') ? "red" : "green" })
	// },
	
});

frappe.ui.form.on('Claim Table',{
	km_if_travel: function(frm,cdt, cdn){
		calculate_total(frm, cdt, cdn);
	}
	// amount:function(frm,cdt,cdn){
	// 	cc(frm,cdt,cdn);
	// },
	// expense_type:function(frm,cdt,cdn){
	// 	ce(frm,cdt,cdn);
	// }
});
var calculate_total = function(frm, cdt, cdn) {
	// if changes in amount should also changed in frappe_call python file for mobile function
	var child = locals[cdt][cdn];
	if(child.expense_type=='Fuel (Bike)')
	{
		frappe.model.set_value(cdt, cdn, "amount", child.km_if_travel * 3.1);
	}
	else if(child.expense_type=='Fuel (Car)')
	{
		frappe.model.set_value(cdt, cdn, "amount", child.km_if_travel * 6.7);
	}
}

// var cc = function(frm, cdt, cdn) {
// 	var child = locals[cdt][cdn];
// 	if(child.expense_type=='Fuel (Bike)')
// 	{
// 		frappe.model.set_value(cdt, cdn, "amount", child.km_if_travel * 3.1);
// 	}
// 	else if(child.expense_type=='Fuel (Car)')
// 	{
// 		frappe.model.set_value(cdt, cdn, "amount", child.km_if_travel * 6.7);
// 	}
// }

// var ce = function(frm, cdt, cdn) {
// 	var child = locals[cdt][cdn];
// 	if(child.expense_type=='Fuel (Bike)')
// 	{
// 		frappe.model.set_value(cdt, cdn, "amount", child.km_if_travel * 3.1);
// 	}
// 	else if(child.expense_type=='Fuel (Car)')
// 	{
// 		frappe.model.set_value(cdt, cdn, "amount", child.km_if_travel * 6.7);
// 	}
// }