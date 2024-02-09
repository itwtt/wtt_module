frappe.query_reports["Farm Salary"] = {
	"filters": [
		{
			"label":"Month",
			"fieldname":"month",
			"fieldtype":"Select",
			'reqd':1,
			"options":['January','February','March','April','May','June','July','August','September','October','November','December']
		}
	],
	onload:function(){
		if(frappe.session.user=='Administrator' || frappe.session.user=='venkat@wttindia.com'){
		frappe.query_report.page.add_inner_button(__("Approve"), function() {
			var selected_rows = [];
			var v=frappe.query_report.datatable.rowmanager.getCheckedRows();
			var ar=[];
			for(i in v)
			{
			
			ar.push(frappe.query_report.data[v[i]].ref)
			
			
			}
			frappe.call({
				"method":"wtt_module.wtt_module.report.farm_attendance.farm_attendance.salary",
				args:{
					"name":ar,
				}
			})
		});
	}
		
	},
	get_datatable_options(options) {
        return Object.assign(options, {
            checkboxColumn: true,
            editable:true
        });
    }
};
