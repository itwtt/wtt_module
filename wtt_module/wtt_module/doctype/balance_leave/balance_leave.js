// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Balance Leave', {
	refresh: function(frm) {
			frm.add_custom_button(__('Proceed'), function(){
				frappe.call({
					method:"wtt_module.wtt_module.doctype.task_allocation.task_allocation.raghul_task",
					args:{
						nn:'success'
					},
					callback(r){
					
					}
			});

			frappe.call({
					method:"wtt_module.wtt_module.doctype.task_allocation.task_allocation.prabhu_task",
					args:{
						nn:'success'
					},
					callback(r){
					
					}
			});
			
			frappe.call({
					method:"wtt_module.wtt_module.doctype.task_allocation.task_allocation.sivakumar_task",
					args:{
						nn:'success'
					},
					callback(r){
					
					}
			});
			frappe.call({
					method:"wtt_module.wtt_module.doctype.task_allocation.task_allocation.ajith_task",
					args:{
						nn:'success'
					},
					callback(r){
					
					}
			});
			frappe.call({
					method:"wtt_module.wtt_module.doctype.task_allocation.task_allocation.create_task",
					args:{
						nn:'success'
					},
					callback(r){
						alert("done")
					}
			});
    	});
  	},
	// before_save: function(frm, cdt, cdn) {
	// 	var temp = frm.doc.balance_leave_table;
	// 	var sum=[]
	// 	$.each(frm.doc.balance_leave_table, function (i, cd) {
	// 	sum.push(cd.balance_leave)
		
	// 	})

	// 	var ss=sum.reduce(add, 0);
	// 	frm.set_value("total",ss);		
	// },
	

	
});
frappe.ui.form.on('Balance Leave Table', {
	balance_leave: function(frm, cdt, cdn) {
		// calculate_total_leave(frm, cdt, cdn);
		
	},
	
});
var calculate_total_leave = function(frm) {
var temp = frm.doc.balance_leave_table;
var i,sum,red_bl=0
for(i=0;i<temp.length;i++)
{
sum+=temp[i].balance_leave;
red_bl+=temp[i].taken_bl;

}
frm.set_value("total",sum-red_bl);
};
function add(accumulator, a) {
  return accumulator + a;
}