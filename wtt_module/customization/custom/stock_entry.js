// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors // License: GNU General Public License v3. See license.txt
frappe.ui.form.on('Stock Entry', {
    refresh: function(frm) {   
   if (frm.doc.docstatus===0) {
            frm.add_custom_button(__('Purchase Receipt'), function() {
                erpnext.utils.map_current_doc({
                    method: "wtt_module.customization.custom.purchase_receipt.make_stock_entry",
                    source_doctype: "Purchase Receipt",
                    target: frm,
                    date_field: "posting_date",
                    setters: {
                        supplier: frm.doc.supplier || undefined,
                    },
                    get_query_filters: {
                        docstatus: 1
                    }
                })
            }, __("Get Items From"));
            frm.add_custom_button(__('Job Order Request'), function() {
                erpnext.utils.map_current_doc({
                    method: "wtt_module.customization.custom.purchase_receipt.make_job_order_request",
                    source_doctype: "Job Order Request",
                    target: frm,
                    date_field: "posting_date",
                    setters: {
                        company: frm.doc.company,
                    },
                    get_query_filters: {
                        docstatus: 1
                    }
                })
            }, __("Get Items From"));
            frm.add_custom_button(__('Material Issue'), function() {
                erpnext.utils.map_current_doc({
                    method: "wtt_module.wtt_module.doctype.material_issue.material_issue.make_stock_entry",
                    source_doctype: "Material Issue",
                    target: frm,
                    date_field: "transaction_date",
                    setters: {
                        title: frm.doc.title || undefined,
                    },
                    get_query_filters: {
                        docstatus: 1
                    }
                })
            }, __("Get Items From"))
    }
},
	item_group: function(frm,cdt,cdn){
		fil(frm, cdt, cdn);
	},
	item_template: function(frm,cdt, cdn){
		go(frm, cdt, cdn);
	}
});

var fil = function(frm, cdt, cdn) {
frappe.call({
            "method": "wtt_module.customization.custom.stock_entry.make_filter",
            args: {
                go: frm.doc.item_group
            },
            callback: function (r) {
			frm.set_df_property('item_template','options',r.message);
			frm.refresh_field('item_template');
            }
});
}

var go = function(frm, cdt, cdn) {
var child = locals[cdt][cdn];
frappe.call({
            "method": "wtt_module.customization.custom.stock_entry.make_template",
            args: {
                val1: frm.doc.item_template   
            },
            callback: function (r) {
            	for(var i=0;i<r.message[0].length;i++)
				{
				var ch = frm.add_child("item_filter");
				frappe.model.set_value(ch.doctype, ch.name, "attribute", r.message[0][i].attribute);
				frappe.meta.get_docfield(ch.doctype,'attribute_value',frm.doc.name).options = r.message[1][i];
				frm.refresh_field("item_filter");
				}
            }
        });
frm.fields_dict["item_filter"].grid.add_custom_button(__('Filter'),
			function() {
				var arr=[];
				var arr1=[];
				$.each(frm.doc.item_filter || [], function(i, v) {
				arr.push(v.attribute)
				arr1.push(v.attribute_value)
				});
				frappe.call({
            		"method": "wtt_module.customization.custom.stock_entry.make_filtering",
            		args: {
                		ar:arr,
                		ar1:arr1 
            		},
            callback: function (r) {
            	
            }
        });
        });
}
