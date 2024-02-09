// frappe.ui.form.on('Job Applicant', {
//     get_data: function(frm) {
//     	frm.set_value("applicant_name","vishnu")
//   }
// });

frappe.ui.form.on("Job Applicant", {
	refresh:function(frm){
		frm.add_custom_button(__('Job App'), () => frm.events.get_det_from_issue(frm),
				__());

		
	},
		
	get_det_from_issue:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.customization.custom.job_applicant.make_det",
					source_doctype: "Job App",
					target: frm,
					date_field: "date_of_birth",
					setters: {
						applicant_name:frm.doc.applicant_name,
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 0,
						job_status: 'Shortlisted'
					}
				});
	}
});
		
	
