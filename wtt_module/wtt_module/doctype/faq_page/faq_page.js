// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('FAQ Page', {
	refresh: function(frm) {
		frm.page.wrapper.find(".comment-box").css({'display':'none'});
	},
	department:function(frm){
		var ar=["--select--"];
		frappe.db.get_list('FAQ Table', {
		    fields: ['question'],
		    filters: {
		        parent: frm.doc.department
		    }
		}).then(records => {
			for(var i=0;i<records.length;i++){
				// alert(JSON.stringify(records[i].question))
				ar.push(records[i].question)
			}
		    frm.set_df_property("questions","options",ar)
		})
	},
	questions:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.faq_page.faq_page.get_ans",
			args:{
				dept:frm.doc.department,
				ques:frm.doc.questions
			},
			callback:function(r){
				frm.set_value("answer",r.message[0]);
				frm.refresh_field("answer");
				frm.set_value("reference_name",r.message[1]);
				frm.refresh_field("reference_name");
				frm.set_value("comment",r.message[2]);
				frm.refresh_field("comment");
			}
		})
	},
	your_comment:function(frm){
		


		let d = new frappe.ui.Dialog({
		    fields: [
		        {
		            label: 'Employee',
		            fieldname: 'employee',
		            fieldtype: 'Link',
		            options: 'Employee'
		        },
		        {
		            label: 'Employee Name',
		            fieldname: 'employee_name',
		            fieldtype: 'Data',
		            read_only: 1,
		            hidden: 1
		        },
		        {
		            label: 'reference_name',
		            fieldname: 'reference_name',
		            fieldtype: 'Data',
		            read_only: 1,
		            hidden: 1,
		            default: frm.doc.reference_name
		        },
		        {
		            label: 'Comment',
		            fieldname: 'comment',
		            fieldtype: 'Text Editor',
		            reqd: 1
		        }
		    ],
		    primary_action_label: 'Comment',
		    primary_action(values) {
		    	
		    	frappe.db.set_value('FAQ Table', values.reference_name, 'comment', '<p><b>'+values.employee_name+' : </b><br>'+values.comment+' </p>')
			    .then(r => {
			        let doc = r.message;
			        d.hide()
			        frm.refresh_field("comment")

			    })
		        
		    }
		});

		d.show();

		d.fields_dict.employee.refresh();
		d.fields_dict.employee.$input.on("change", function(event){
			frappe.db.get_value('Employee', this.value, ['employee_name'])
		    .then(r => {
		        let values = r.message;
		        d.set_df_property("employee_name","hidden",0)
		        d.set_value("employee_name",values.employee_name)
		    })
		});

	},

	your_answer:function(frm){
		


		let d = new frappe.ui.Dialog({
		    title: 'Answer',
		    fields: [
		        {
		            label: 'Employee',
		            fieldname: 'employee',
		            fieldtype: 'Link',
		            options: 'Employee'
		        },
		        {
		            label: 'Employee Name',
		            fieldname: 'employee_name',
		            fieldtype: 'Data',
		            read_only: 1,
		            hidden: 1
		        },
		        {
		            label: 'reference_name',
		            fieldname: 'reference_name',
		            fieldtype: 'Data',
		            read_only: 1,
		            hidden: 1,
		            default: frm.doc.reference_name
		        },
		        {
		            label: 'Answer',
		            fieldname: 'answer',
		            fieldtype: 'Text Editor',
		            reqd: 1
		        }
		    ],
		    primary_action_label: 'Submit',
		    primary_action(values) {
		    	
		    	frappe.db.set_value('FAQ Table', values.reference_name, 'answer', frm.doc.answer+'<p><b>'+values.employee_name+' : </b><br>'+values.answer+' </p>')
			    .then(r => {
			        let doc = r.message;
			        d.hide()
			        frm.refresh_field("answer")
			    })
		        
		    }
		});

		d.show();

		d.fields_dict.employee.refresh();
		d.fields_dict.employee.$input.on("change", function(event){
			frappe.db.get_value('Employee', this.value, ['employee_name'])
		    .then(r => {
		        let values = r.message;
		        d.set_df_property("employee_name","hidden",0)
		        d.set_value("employee_name",values.employee_name)
		    })
		});

	}
});
