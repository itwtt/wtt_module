// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Technical Interview', {
	refresh: function(frm) {
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Job App List'), () => frm.events.get_job_candidate(frm),
				__("Get Shortlisted List"));
		}
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Hr Interview List'), () => frm.events.get_shortlisted_candidate(frm),
				__("Get Shortlisted List"));
		}
	},
	get_shortlisted_candidate:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.hr_interview.hr_interview.make_shortlisted",
					source_doctype: "HR interview",
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
		},
	get_job_candidate:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.job_app.job_app.make_job_candidate",
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
		}
	});
