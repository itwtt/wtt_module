// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Summation', {
	refresh: function(frm) {
		if (frappe.user_roles.includes ("HR User")){
			frm.set_df_property("month","read_only",0);
			frm.set_df_property("head_office","read_only",0);
			frm.set_df_property("project","read_only",0);
			frm.set_df_property("esi","read_only",0);
			frm.set_df_property("epf","read_only",0);
			frm.set_df_property("house_keeping","read_only",0);
			frm.set_df_property("labour_welfare_fund","read_only",0);
			frm.set_df_property("site_worker_salary","read_only",0);
			frm.set_df_property("last_month_arrear","read_only",0);
			frm.set_df_property("security_service","read_only",0);
			frm.add_custom_button("Get From Salary Slip",function(){
				frappe.call({
					method:"get_from_salary_slip",
					doc:frm.doc,
					callback(r){
						frm.set_value("head_office",r.message[0]["HEAD OFFICE"]);
						frm.set_value("project",r.message[0]["WORKSHOP"]);
						frm.set_value("esi",r.message[0]["esi"]);
						frm.set_value("epf",r.message[0]["pf"]);
						frm.set_value("labour_welfare_fund",r.message[0]["ewf"]);

					}
				})
			})
		}
		if(frappe.user_roles.includes ("Purchase Master Manager")){
			// frm.add_custom_button("Go to Salary Report",function(){
			// 	// frappe.set_route('Report', 'Salary','Salary')
			// })
		}
		
	},
	month:function(frm){
		frappe.call({
			method:"set_last_date",
			doc:frm.doc,
			callback(r){
				frm.set_value("posting_date",r.message);
				frm.refresh_field("posting_date");
			}
		})
	}
});
