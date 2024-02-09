// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Material Analysis"] = {
	"filters": [
	{
		"label":"Project",
		"fieldname":"project",
		"fieldtype":"Link",
		"options":"Project",
		"default":"WTT-0450",
		"reqd":1,
		"get_query": function() {
				return {
					filters: {
						"status": "On going"
					}
				};
			}
	}
	],
	onload: function(report) {
		report.page.add_inner_button(__("Show Pending"), function() {
				var get_pro = frappe.query_report.get_filter('project');
				// frappe.prompt('Project', ({ get_pro }) => console.log(get_pro))
				// let d = new frappe.ui.Dialog({
				//     title: 'Pending Details',
				//     fields: [
				//         {
				//             label: 'Project',
				//             fieldname: 'project',
				//             fieldtype: 'HTML',
				//             default:'<b>'+get_pro.value+'</b>'
				//         }
				//     ],
				//     size: 'small',
				//     primary_action_label: 'Submit',
				//     primary_action(values) {
				//         console.log(values);
				//         d.hide();
				//     }
				// });
				// d.show();
		});
	}
};
