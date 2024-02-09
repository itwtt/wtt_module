// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Technical Criteria', {
	setup: function(frm,cdt,cdn) {
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
		frm.set_query("hod_id", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
		
	},
	
	refresh: function(frm) {
		
		 var hidebtn1 = $('*[data-fieldname="position_specific"]');
		 var hidebtn2 = $('*[data-fieldname="industry_specific"]');
		 var hidebtn3 = $('*[data-fieldname="common_skills"]');

			hidebtn1 .find('.grid-add-row').hide();
			hidebtn1 .find('.grid-remove-rows').hide();

			hidebtn2 .find('.grid-add-row').hide();
			hidebtn2 .find('.grid-remove-rows').hide();

			hidebtn3 .find('.grid-add-row').hide();
			hidebtn3 .find('.grid-remove-rows').hide();

	},
	employee:function(frm)
	{
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.technical_criteria.technical_criteria.update_technical',
			args: { 
				emp:frm.doc.employee
			},
			callback(r) {
				frm.clear_table("position_specific")
				frm.refresh_field("position_specific");
				frm.clear_table("industry_specific")
				frm.refresh_field("industry_specific");
				frm.clear_table("common_skills")
				frm.refresh_field("common_skills");
				for(var i=0;i<r.message.length;i++)
				{
					if(r.message[i].perfor=='POSITION SPECIFIC')
					{
						var child = frm.add_child("position_specific");
						frappe.model.set_value(child.doctype, child.name, "criteria", r.message[i].techcri);
						frm.refresh_field("position_specific");
					}

					if(r.message[i].perfor=='INDUSTRY SPECIFIC')
					{
						var child = frm.add_child("industry_specific");
						frappe.model.set_value(child.doctype, child.name, "criteria", r.message[i].techcri);
						frm.refresh_field("industry_specific");
					}

					if(r.message[i].perfor=='COMMON SKILLS')
					{
						var child = frm.add_child("common_skills");
						frappe.model.set_value(child.doctype, child.name, "criteria", r.message[i].techcri);
						frm.refresh_field("common_skills");
					}
				}
			}
		});
	}
});
