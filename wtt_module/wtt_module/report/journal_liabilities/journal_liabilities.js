// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Journal Liabilities"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default":new Date(new Date().getFullYear(),new Date().getMonth(),1),
			"print_hide":1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": new Date(new Date().getFullYear(),new Date().getMonth()+1,0)
		}
	],
	after_datatable_render: function (datatable_obj) {
        $(datatable_obj.wrapper).find(".dt-row-0").find('input[type=checkbox]').click();

    },
    get_datatable_options(options) {

        options.columns.forEach(function(column, i) {
        	if(column.id=="posting_date"){
            	column.fixedColumns=true
        	}            
        });
        delete options['cellHeight']
        return Object.assign(options, {
            freezeMessage: '',
            ScrollX:true,
            ScrollY:true,
		    getEditor: null,
		    serialNoColumn: true,
		    checkboxColumn: true,
		    logs: true,
		    layout: 'fixed', // fixed, fluid, ratio
		    noDataMessage: 'No Data',
		    cellHeight: 35,
		    inlineFilters: true,
		    treeView: false,
		    checkedRowStatus: true,
		    dynamicRowHeight: true,
		    pasteFromClipboard: true,
		    paging:true,
		    frozenColumns:4,
		    treeView:true

		});
    },
    formatter: (value, row, column, data, default_formatter,datum) => {
    	column.editable = true,
        column.width = 100
        if(column.id=="posting_date"){
        	column.freeze = "Left"
        }
        if(column.id=="user_remark"){
        	column.width = 200
        }
        if(value==undefined){
        	value="<center>-</center>"
        }
    return value	
    },
    onload: function(report) {
    	frappe.query_report.page.add_inner_button(__("Approved"), function() {
    	var selected_rows = [];
  		$('.dt-scrollable').find(":input[type=checkbox]").each((idx, row) => {
  			if(row.checked){
  				selected_rows.push(frappe.query_report.data[idx]);
  			}
  		});
    	alert(JSON.stringify(selected_rows))		
    	});
    }
};
