// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
frappe.ui.form.on("Delivery Note", {
	setup:function(frm,cdt,cdn){
		frm.set_query("party_type", function() {
		return {
			filters: [
				["DocType","name","in","Supplier,Customer"]
			]
		}

	});

	},
	validate:function(frm,cdt,cdn){
		var mr=""
		var po=""
		var dnr=""
		$.each(frm.doc.items || [], function(i, v) {
			if(i==0){
			if(v.material_request){
				mr+=v.material_request
			}
			if(v.purchase_order){
				po+=v.purchase_order
			}
			if(v.delivery_note_request){
				dnr+=v.delivery_note_request
			}
			}
			else{
			if(v.material_request){
				mr+=", "+v.material_request
			}
			if(v.purchase_order){
				po+=", "+v.purchase_order
			}
			if(v.delivery_note_request){
				dnr+=", "+v.delivery_note_request
			}	
			}
			
		});
		frm.set_value("ref_mr",mr);
		frm.set_value("ref_po",po);
		frm.set_value("ref_se",dnr);
	},
	refresh: function(frm) {
		$(frm.fields_dict['html'].wrapper).html("");
		frm.set_df_property("hide","hidden",1);
		if (frm.doc.docstatus===0) {
			frm.add_custom_button(__('Material Request'), () => frm.events.get_items_from_mat(frm),
				__("Get Items From"));

			// frm.add_custom_button(__('Delivery Note Request'), () => frm.events.get_items_from_mr(frm),
			// 	__("Get Items From"));

			frm.add_custom_button(__('Job Order'), () => frm.events.get_items_from_job(frm),
				__("Get Items From"));

			frm.add_custom_button(__('Purchase Order'), () => frm.events.get_items_from_po(frm),
				__("Get Items From"));
			frm.add_custom_button(__('QC for DC'), () => frm.events.get_items_from_qc(frm),
				__("Get Items From"));
		}
		
	},
	onload:function(frm){
		if(frm.doc.docstatus == 0)
		{
			if(frappe.session.user=='Administrator' || frappe.session.user=='venkat@wttindia.com' || frappe.session.user == 'sarnita@wttindia.com')
			{
				frm.add_custom_button(__('Bypass DC'), () => {
					if(frm.doc.by_pass_delivery_note == "Approved Bypass")
					{
						frm.set_value("by_pass_delivery_note","")
						frm.refresh_field("by_pass_delivery_note");
						frm.save();
					}
					else
					{
						frm.set_value("by_pass_delivery_note","Approved Bypass")
						frm.refresh_field("by_pass_delivery_note");
						frm.save();
					}
				});
			}
		}
	},
	get_items_from_po:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.customization.custom.delivery_note.make_dnr",
					source_doctype: "Purchase Order",
					target: frm,
					date_field: "schedule_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1
					}
				});
	},
	get_items_from_qc:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.customization.custom.delivery_note.make_qc",
					source_doctype: "QC for DC",
					target: frm,
					date_field: "date",
					setters: {
						
					},
					get_query_filters: {
						docstatus: 1
					}
				});
	},
	preview:function(frm){
		frm.set_df_property("hide","hidden",0);
		frm.set_df_property("preview","hidden",1);
		var htvalue='<style>th{font-size: 15px;text-align:center;color:#6A5ACD;}</style>'
		htvalue+="<table border='1px' style='margin-top:-1px;width:100%'><tr><th style='width:1%;'>S.NO</th><th style='width:2%'>DESCRIPTION</th><th style='width:15%'>TECHNICAL DESCRIPTION</th><th style='text-align:center;width:5%'>QTY</th><th style='width:8%'>TERMS OF DELIVERY</th></tr>"
		$.each(frm.doc.items || [], function(i, v) {
			var result=''
			var re=''
			
			if(v.technical_description)
			{
			var go=[]
			var val=v.technical_description.split(",")
			var gg='<br>'
			for(var g in val)
			{
				go.push(val[g])
				go.push(gg)
			}
			result = go.toString().replace(/,/g, "");
			}
			if(v.remarks)
			{
				re=v.remarks
			}
			htvalue+='<tr style="text-align:center;"><td align="center">'+v.idx+'.</td><td align="center">'+v.description+'<br></td><td align="left">'+result+'</td><td>'+v.qty+'</td><td>'+v.terms_of_delivery+'</td></tr>'
		});
		$(frm.fields_dict['html'].wrapper).html(htvalue);
	},
	hide:function(frm){
		frm.set_df_property("hide","hidden",1);
		frm.set_df_property("preview","hidden",0);
		$(frm.fields_dict['html'].wrapper).html("");
	},
	// get_items_from_mr:function(frm){
	// 	erpnext.utils.map_current_doc({
	// 				method: "wtt_module.wtt_module.doctype.delivery_note_request.delivery_note_request.make_delivery_note",
	// 				source_doctype: "Delivery Note Request",
	// 				target: frm,
	// 				date_field: "transaction_date",
	// 				setters: {
	// 					company: frm.doc.company,
	// 				},
	// 				get_query_filters: {
	// 					docstatus: 1	
	// 				}
	// 			});
	// 	},
	get_items_from_mat:function(frm){
		erpnext.utils.map_current_doc({
			method: "wtt_module.customization.custom.delivery_note.make_mat",
			source_doctype: "Material Request",
			target: frm,
			setters: {
				schedule_date: undefined,
				status: undefined
			},
			get_query_filters: {
				material_request_type: "Purchase",
				docstatus: 1,
				status: ["!=", "Stopped"],
				company: frm.doc.company
			},
			allow_child_item_selection: true,
			child_fieldname: "items",
			child_columns: ["idx", "description", "item_code"]
		})
		},
	get_items_from_job:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.customization.custom.delivery_note.make_job",
					source_doctype: "Job Order",
					target: frm,
					date_field: "posting_date",
					setters: {
						company: frm.doc.company,
					},
					get_query_filters: {
						docstatus: 1,
						job_order_type:["=", "Job Order Request"]
					}
				});
		}
});