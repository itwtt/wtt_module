// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Self Appraisal', {
	// refresh: function(frm) {

	// }
	setup:function(frm) {
		// const element = document.querySelector('.btn.btn-xs.btn-default');
		//     element.style.background = 'lightgrey';
	},
	onload:function(frm){
		// const element = document.querySelector('.btn.btn-xs.btn-default');
		//     element.style.background = 'green';
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status", "=", "Active"]
				]
			};
		});
	},
	refresh:function(frm){
		const element = document.querySelector('.btn.btn-xs.btn-default');
		    element.style.background = 'lightgrey';
	},
	next:function(frm){
		
		frm.set_df_property("que1","hidden",1);frm.set_df_property("que2","hidden",1);frm.set_df_property("que3","hidden",1);
		frm.set_df_property("que4","hidden",1);frm.set_df_property("que5","hidden",1);frm.set_df_property("que6","hidden",1);frm.set_df_property("next","hidden",1);
		frm.set_df_property("que7","hidden",0);frm.set_df_property("que8","hidden",0);frm.set_df_property("que9","hidden",0);frm.set_df_property("previous1","hidden",0)
		frm.set_df_property("que10","hidden",0);frm.set_df_property("que11","hidden",0);frm.set_df_property("que12","hidden",0);frm.set_df_property("next1","hidden",0);
	},
	previous1:function(frm){
		frm.set_df_property("que1","hidden",0);frm.set_df_property("que2","hidden",0);frm.set_df_property("que3","hidden",0);
		frm.set_df_property("que4","hidden",0);frm.set_df_property("que5","hidden",0);frm.set_df_property("que6","hidden",0);frm.set_df_property("next","hidden",0);
		frm.set_df_property("que7","hidden",1);frm.set_df_property("que8","hidden",1);frm.set_df_property("que9","hidden",1);frm.set_df_property("previous1","hidden",1)
		frm.set_df_property("que10","hidden",1);frm.set_df_property("que11","hidden",1);frm.set_df_property("que12","hidden",1);frm.set_df_property("next1","hidden",1);
	},
	next1:function(frm){
		frm.set_df_property("que7","hidden",1);frm.set_df_property("que8","hidden",1);frm.set_df_property("que9","hidden",1);frm.set_df_property("previous1","hidden",1)
		frm.set_df_property("que10","hidden",1);frm.set_df_property("que11","hidden",1);frm.set_df_property("que12","hidden",1);frm.set_df_property("next1","hidden",1);
		frm.set_df_property("que15","hidden",0);frm.set_df_property("que13","hidden",0);frm.set_df_property("que14","hidden",0);frm.set_df_property("previous2","hidden",0)
		frm.set_df_property("que16","hidden",0);frm.set_df_property("que17","hidden",0);frm.set_df_property("que18","hidden",0);frm.set_df_property("next2","hidden",0);
	},
	previous2:function(frm){
		frm.set_df_property("que7","hidden",0);frm.set_df_property("que8","hidden",0);frm.set_df_property("que9","hidden",0);frm.set_df_property("previous1","hidden",0)
		frm.set_df_property("que10","hidden",0);frm.set_df_property("que11","hidden",0);frm.set_df_property("que12","hidden",0);frm.set_df_property("next1","hidden",0);
		frm.set_df_property("que15","hidden",1);frm.set_df_property("que13","hidden",1);frm.set_df_property("que14","hidden",1);frm.set_df_property("previous2","hidden",1)
		frm.set_df_property("que16","hidden",1);frm.set_df_property("que17","hidden",1);frm.set_df_property("que18","hidden",1);frm.set_df_property("next2","hidden",1);
	},
	next2:function(frm){
		frm.set_df_property("que15","hidden",1);frm.set_df_property("que13","hidden",1);frm.set_df_property("que14","hidden",1);frm.set_df_property("previous2","hidden",1)
		frm.set_df_property("que16","hidden",1);frm.set_df_property("que17","hidden",1);frm.set_df_property("que18","hidden",1);frm.set_df_property("next2","hidden",1);
		frm.set_df_property("que19","hidden",0);frm.set_df_property("que20","hidden",0);frm.set_df_property("previous3","hidden",0);frm.set_df_property("submit","hidden",0);

	},
	previous3:function(frm) {
		frm.set_df_property("que15","hidden",0);frm.set_df_property("que13","hidden",0);frm.set_df_property("que14","hidden",0);frm.set_df_property("previous2","hidden",0)
		frm.set_df_property("que16","hidden",0);frm.set_df_property("que17","hidden",0);frm.set_df_property("que18","hidden",0);frm.set_df_property("next2","hidden",0);
		frm.set_df_property("que19","hidden",1);frm.set_df_property("que20","hidden",1);frm.set_df_property("previous3","hidden",1);frm.set_df_property("submit","hidden",1);
	},
	submit:function(frm){
		frm.save()
	}

});
