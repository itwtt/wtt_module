// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Questions for Interview', {
	refresh: function(frm) {
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Job App List'), () => frm.events.get_candidate_list(frm),
				__("Get Candidate List"));
		}
	},
	get_candidate_list:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.questions_for_interview.questions_for_interview.make_candidate_list",
					source_doctype: "Job App",
					target: frm,
					date_field: "date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 0
					}
				});
	},
	get_questions:function(frm){
		if(frm.doc.list=='Others')
		{
		frappe.call({
			method:"wtt_module.wtt_module.doctype.questions_for_interview.questions_for_interview.make_query",
			callback(r){
				frm.set_value("question_1",r.message[0].question1);
				frm.set_value("question_2",r.message[1].question1);
				frm.set_value("question_3",r.message[2].question1);
				frm.set_value("question_4",r.message[3].question1);
				frm.set_value("question_5",r.message[4].question1);
				frm.set_value("question_6",r.message[5].question1);
				frm.set_value("question_7",r.message[6].question1);
				frm.set_value("question_8",r.message[7].question1);
				frm.set_value("question_9",r.message[8].question1);
				frm.set_value("question_10",r.message[9].question1);
			}
		});
		}
		else if(frm.doc.list=='Managers')
		{
			frappe.call({
			method:"wtt_module.wtt_module.doctype.questions_for_interview.questions_for_interview.make_query_managers",
			callback(r){
				frm.set_value("questionmg_1",r.message[0].question2);
				frm.set_value("questionmg_2",r.message[1].question2);
				frm.set_value("questionmg_3",r.message[2].question2);
				frm.set_value("questionmg_4",r.message[3].question2);
				frm.set_value("questionmg_5",r.message[4].question2);
				frm.set_value("questionmg_6",r.message[5].question2);
				frm.set_value("questionmg_7",r.message[6].question2);
				frm.set_value("questionmg_8",r.message[7].question2);
				frm.set_value("questionmg_9",r.message[8].question2);
				frm.set_value("questionmg_10",r.message[9].question2);
				}
			});
		}
	}
});
