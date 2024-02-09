// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('HR interview', {
	refresh: function(frm) {
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Job App List'), () => frm.events.get_candidate(frm),
				__("Get Candidate List"));
		}
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Technical Interview List'), () => frm.events.get_technical(frm),
				__("Get Candidate List"));
		}
	},
	get_candidate:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.job_app.job_app.make_candidate",
					source_doctype: "Job App",
					target: frm,
					date_field: "date",
					setters: {
						applicant_name:frm.doc.applicant_name,
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 0
					}
				});
	},
	get_technical:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.technical_interview.technical_interview.make_technical",
					source_doctype: "Technical Interview",
					target: frm,
					date_field: "date",
					setters: {
						candidate_name:frm.doc.candidate_name,
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1
					}
				});
	}

});
