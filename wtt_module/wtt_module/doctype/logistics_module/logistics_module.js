// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
frappe.ui.form.on('Logistics Module', {
	setup: function(frm,cdt,cdn) {
		frm.set_query("supplier", function() {
			return {
				filters: [
					["Supplier","disabled","=", 0]
				]
			}

		});	

		frm.set_query("from_warehouse", function() {
			return {
				filters: [
					["Warehouse","company","=", frm.doc.company]
				]
			}

		});	

		frm.set_query("to_warehouse", function() {
			return {
				filters: [
					["Warehouse","company","=", frm.doc.company]
				]
			}

		});	

		frm.set_query("project", function() {
			return {
				filters: [
					["Project","status","=", "On going"]
				]
			}

		});		
	},
	supplier:function(frm){
		if(frm.doc.supplier)
		{
			frappe.call({
			method:"wtt_module.wtt_module.doctype.logistics_module.logistics_module.get_bc",
				args:{
					sup:frm.doc.supplier
				},
				callback(r){
					for(var i=0;i<r.message.length;i++)
					{
						frm.set_value("bank_account",r.message[i].bank_acc);
						frm.refresh_field("bank_account");
					}
				}
			})
		}
		else
		{
			frm.set_value("bank_account","");
			frm.refresh_field("bank_account");
		}
	}
});