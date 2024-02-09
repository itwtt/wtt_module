frappe.ui.form.on('Cost Working Tool', {
	setup:function(frm){
		frm.set_query("choose_ro_template", function() {
	        return {
	            "filters": [
	                ["RO Standard Items", "ro_type", "=", "RO"]
            	]
	        };
	    });
	    frm.set_query("choose_rro_template", function() {
	        return {
	            "filters": [
	                ["RO Standard Items", "ro_type", "=", "RRO"]
            	]
	        };
	    });
	    frm.set_query("rewolutte_ro", function() {
	        return {
	            "filters": [
	                ["RO Standard Items", "ro_type", "=", "REWOLUTTE"]
            	]
	        };
	    });
	},
	get_rate:function(frm){
		frm.clear_table("bom_item_rate")
		frm.refresh_field("bom_item_rate");
		var range_list = 0;
		$.each(frm.doc.bio_full_system || [], function(i, v) {
			if(v.item_description == frm.doc.system_list)
			{
				range_list=v.range
			}
		});

		frappe.call({
			method:"wtt_module.wtt_module.doctype.startup_sheet.startup_sheet.get_total_bom_cost",
			args:{
				st_list:frm.doc.system_list,
				range_list:range_list
			},
			callback(r){
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("bom_item_rate");
				frappe.model.set_value(child.doctype, child.name, "item_code", r.message[i].item_code);
				frappe.model.set_value(child.doctype, child.name, "qty", r.message[i].qty);
				frappe.model.set_value(child.doctype, child.name, "unit_price", r.message[i].unit_price);
				frappe.model.set_value(child.doctype, child.name, "total_price", r.message[i].total_price);
				frappe.model.set_value(child.doctype, child.name, "bom", r.message[i].bom);
				frm.refresh_field("bom_item_rate");
				}
			}
		});
	},
	refresh:function(frm){
		if(frappe.session.user=="Administrator"){
			frm.add_custom_button(__('Generate Pdf Document'), function() {
	            frappe.call({
			        method: 'wtt_module.process_and_costing.doctype.cost_working_tool.cost_working_tool.generate_pdf', // Replace with the actual method name
			        args: {
			            docname: frm.doc.name
			        },
			        callback(r) {
			        	frm.set_value("pdf_1",r.message);
			        	frm.refresh_field("pdf_1");
			        	frm.set_value("revision_remarks",JSON.stringify(r.message));
			        	frm.refresh_field("revision_remarks");
			        }
			    });
	        });
		}
			

        frm.add_custom_button(__('Duplicate'), function(){
			frappe.model.open_mapped_doc({
				method: "wtt_module.process_and_costing.doctype.cost_working_tool.cost_working_tool.duplicate",
				frm: frm
			});
		});    
	},
	startup_sheet: function(frm) {
	    var openlink = window.open("https://erp.wttindia.com/app/startup-sheet/"+frm.doc.project_startup_sheet+"","_self");
	},
	mf_not_linked_items:function(frm){
		frm.clear_table("mf_not_linked_table")
		frm.refresh_field("mf_not_linked_table");
		$.each(frm.doc.mf_table || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("mf_not_linked_table");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "req_flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frm.refresh_field("mf_not_linked_table");
			}
		});
	},
	not_linked_items:function(frm){
		frm.clear_table("mbr_koch_not_linked")
		frm.refresh_field("mbr_koch_not_linked");
		$.each(frm.doc.mbr_koch_table || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("mbr_koch_not_linked");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "req_flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frappe.model.set_value(child.doctype, child.name, "motor_cost", v.motor_cost);
				frm.refresh_field("mbr_koch_not_linked");
			}
		});
	},
	bio_not_linked:function(frm){
		frm.clear_table("bio_not_linked_table")
		frm.refresh_field("bio_not_linked_table");
		$.each(frm.doc.pre_treatment_table || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("bio_not_linked_table");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "req_flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frappe.model.set_value(child.doctype, child.name, "system", v.system);
				frm.refresh_field("bio_not_linked_table");
			}
		});
	},
	add_qty:function(frm){
		var ar=[];

		$.each(frm.doc.bio_not_linked_table || [], function(i, v) {
			ar.push(v.item_description)
		});

		frm.refresh_field("bio_not_linked_table");
		$.each(frm.doc.pre_treatment_table || [], function(i, v) {
			if(v.item_description == frm.doc.item_description && !ar.includes(v.item_description))
			{
				var child = frm.add_child("bio_not_linked_table");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "req_flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", frm.doc.qty);
				frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price);
				frappe.model.set_value(child.doctype, child.name, "total_price", v.unit_price*frm.doc.qty);
				frm.refresh_field("bio_not_linked_table");
			}
			else if(v.item_description == frm.doc.item_description && ar.includes(v.item_description))
			{
				$.each(frm.doc.bio_not_linked_table || [], function(i, v) {
					v.w_qty=v.w_qty+frm.doc.qty;
					v.total_price=v.unit_price*(v.w_qty);
				});
				frm.refresh_field("bio_not_linked_table");
			}
		});
	},
	mbr_ovivo_not_linked_button:function(frm){
		frm.clear_table("mbr_ovivo_not_linked_items")
		frm.refresh_field("mbr_ovivo_not_linked_items");
		$.each(frm.doc.mbr_ovivo_table || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("mbr_ovivo_not_linked_items");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "req_flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frappe.model.set_value(child.doctype, child.name, "motor_cost", v.motor_cost);
				frm.refresh_field("mbr_ovivo_not_linked_items");
			}
		});
	},
	cts_not_linked:function(frm){
		frm.clear_table("cts_not_linked_items")
		frm.refresh_field("cts_not_linked_items");
		$.each(frm.doc.cts_items || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("cts_not_linked_items");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "req_flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frm.refresh_field("cts_not_linked_items");
			}
		});
	},
	mbr_cts_not_linked_button:function(frm){
		frm.clear_table("mbr_cts_not_linked_items")
		frm.refresh_field("mbr_cts_not_linked_items");
		$.each(frm.doc.mbr_cts_table || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("mbr_cts_not_linked_items");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "req_flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frappe.model.set_value(child.doctype, child.name, "motor_cost", v.motor_cost);
				frm.refresh_field("mbr_cts_not_linked_items");
			}
		});
	},
	dgt_not_linked:function(frm){
		frm.clear_table("dgt_not_linked_items")
		frm.refresh_field("dgt_not_linked_items");
		$.each(frm.doc.dgt_items || [], function(i, v) {
			if(v.unit_price == 0)
			{
				var child = frm.add_child("dgt_not_linked_items");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "req_flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frm.refresh_field("dgt_not_linked_items");
			}
		});
	},
	ro_recovery:function(frm){
		var hard=((frm.doc.flow)*((100-frm.doc.ro_recovery)/100))
		var clhard=Math.ceil((hard/16) / 5) * 5
		$.each(frm.doc.parameters || [], function(i, v) {
			if(v.system_name=="Hardness and Color Removal System" || v.system_name=="Hardness and Silica Removal System")
			{
				frappe.model.set_value(v.doctype, v.name, "parameter_name", "CAPACITY")
				frappe.model.set_value(v.doctype, v.name, "value", clhard)
				frm.refresh_fields("parameter_name");
				frm.refresh_fields("value");
			}
		});
	},
	project_startup_sheet:function(frm){
		list_electrical_items(frm);
		frm.clear_table("parameters");
		frm.refresh_field("parameters");
		frm.clear_table("standard_cost");
		frm.refresh_fields("standard_cost");
		frm.clear_table("selected_process_system");
		frm.refresh_field("selected_process_system");
		frappe.call({
			method:"wtt_module.wtt_module.doctype.startup_sheet.startup_sheet.get_system",
			args:{
				st:frm.doc.project_startup_sheet
			},
			callback(r){
				for(var i=0;i<r.message.length;i++)
				{
				var child = frm.add_child("selected_process_system");
				frappe.model.set_value(child.doctype, child.name, "selected_system_name", r.message[i].select_system);
				frappe.model.set_value(child.doctype, child.name, "selected_type", r.message[i].selected_type);
				frm.refresh_field("selected_process_system");
				}
			}
		});
	},
	get_bom:function(frm){
		frm.clear_table("bom_cost");frm.refresh_field("bom_cost");
	    frm.clear_table("items");frm.refresh_field("items");
	    var arr=[];
		$.each(frm.doc.parameters || [], function(i, v) {
			arr.push({"system_name":v.system_name,"parameter_name":v.parameter_name,"value":v.value})	
		});
		frappe.call({
    		method:"wtt_module.process_and_costing.doctype.cost_working_tool.cost_working_tool.get_matching_bom",
    		args: {
    			// process_system: frm.doc.parameters[0].system_name,
    			// params: frm.doc.parameters,
    			arr:arr
    		},
    		callback: function (r) {
    			for(var i=0;i<=r.message.length;i++)
    			{
    				var child = frm.add_child("bom_cost");
					frappe.model.set_value(child.doctype, child.name, "bom", r.message[i].name);
					frappe.model.set_value(child.doctype, child.name, "qty", 1);
					frappe.model.set_value(child.doctype, child.name, "cost", r.message[i].cost);
					frm.refresh_field("bom_cost");
    			}
    		},
    	});
	},
	get_proposal:function(frm){
		make_null_to_nil(frm);
		get_proposal_template(frm)
	},
	get_word:function(frm){
		// var documentContent = frm.doc.template;
        // var header = "<html><head><meta charset='utf-8'><title>Your Word Document</title></head><body>";
        // var footer = "</body></html>";
        // var html = header + documentContent + footer;
        // var blob = new Blob([html], { type: 'application/msword' });
        // var link = document.createElement("a");
        // link.href = URL.createObjectURL(blob);
        // link.download = "your_document.doc";
        // link.style.display = "none";
        // document.body.appendChild(link);
        // link.click();
        // document.body.removeChild(link);
        frm.clear_table("proposal_index");
		var ar=["1. Technical And Engineering Details", "1.1. BASIS OF DESIGN", "1.2. INFLUENT QUALITY", "1.3. INFLUENT FLOW DATA", "1.4. OPERATIONAL BASIS", "1.5. PROCESS COMPATIBILITY", "2. Design System Chosen", "2.1. EXPECTED TREATED WATER QUALITY", "3. Scope Of Supply - Equipment, Engineering & Services", "4. Equipment Details For Proposed Systems"];
		var asu=[]
		$.each(frm.doc.selected_process_system, function (index, source_row) {
			asu.push(source_row.selected_system_name)
		});
		var asu_top=[]
		if(asu.length>0){
			if(asu.includes('Rotary Brush Screener'))
			{
				asu_top.push('ROTARY BRUSH SCREENER')
			}
			if(asu.includes('DAF (Dissolved Air Flotation)'))
			{
				asu_top.push('DISSOLVED AIR FLOTATION (DAF) SYSTEM')
			}
			if(asu.includes('Equalization System'))
			{
				asu_top.push('EQUALIZATION SYSTEM')
			}
			if(asu.includes('Neutralization System'))
			{
				asu_top.push('NEUTRALIZATION SYSTEM')
			}
			if(asu.includes('Cooling Tower'))
			{
				asu_top.push('COOLING TOWER')
			}
			if(asu.includes('Biological Oxidation System'))
			{
				asu_top.push('BIOLOGICAL SYSTEM')
			}
			if(asu.includes('Lamella Settler'))
			{
				asu_top.push('LAMELLA SETTLER')
			}
			if(asu.includes('Circular Clarifier System'))
			{
				asu_top.push('CIRCULAR CLARIFIER')
			}
			if(asu.includes('Sludge Thickener with mech'))
			{
				asu_top.push('SLUDGE THICKENER')
			}
			if(asu.includes('Belt Press'))
			{
				asu_top.push('BELT PRESS SYSTEM')
			}
			if(asu.includes('Screw Press'))
			{
				asu_top.push('SCREW PRESS')
			}
			if(asu.includes('Micro Filtration - ASAHI'))
			{
				asu_top.push('MICRO/ULTRA FILTRATION SYSTEM')
			}
			if(asu.includes('Submerged MBR system - KOCH'))
			{
				asu_top.push('SUBMERGED MBR SYSTEM - KOCH')
			}
			if(asu.includes('Submerged MBR system - OVIVO'))
			{
				asu_top.push('SUBMERGED MBR SYSTEM - OVIVO')
			}
			if(asu.includes('Sulphur Black Removal System'))
			{
				asu_top.push('SULPHUR BLACK REMOVAL SYSTEM')
			}
			if(asu.includes('Degasser System'))
			{
				asu_top.push('DEGASSER TOWER SYSTEM')
			}
			if(asu.includes('Reverse Osmosis'))
			{
				asu_top.push('REVERSE OSMOSIS SYSTEM')
			}
		}
		for(var i=0;i<asu_top.length;i++)
		{
			var ind = (i+1)
			ar.push('4.'+ind+'. '+asu_top[i])
		}
		var ar2=["5. Equipment Quantity", "6. Typical Equipment Vendor List", "7. Pricing Detail", "8. Exclusions", "9. Happy Customers", "10. Channel Partners", "11. Process Description Video", "12. Commercial Terms And Conditions", "12.1. TAXES", "12.2. FREIGHT", "12.3. INVOICING AND PAYMENT TERMS", "12.4. EQUIPMENT SHIPMENT", "12.5. PRICING NOTES", "13. Client Scope Of Supply", "13.1. SAFETY AND ENVIRONMENTAL", "13.2. JOBSITE AND INSTALLATION REVIEW<", "13.3. START-UP AND COMMISSIONING", "13.4. FACILITY MANAGEMENT", "13.5. CONDITIONAL OFFERING", "14. Appendix", "14.1. APPENDIX A: CLARIFICATIONS", "14.2. APPENDIX B:  ACCEPTANCE", "14.3. APPENDIX C:  WARRANTY", "14.4. APPENDIX D:  CONFIDENTIALITY"]
		for(var i=0;i<ar2.length;i++){
			ar.push(ar2[i])
		}
		
        frappe.call({
        	method:"wtt_module.process_and_costing.doctype.cost_working_tool.title_and_page_no.page_no",
        	args:{
        		path:"./erp.wttindia.com/public"+frm.doc.pdf_1
        	},
        	callback(r){
        		for(var i=0;i<r.message.length;i++){
        			console.log((ar[i]).toLowerCase().split(' ').join(''))
        			console.log(r.message[i].heading)
        			console.log(r.message[i].page_no)
        			if((ar[i]).toLowerCase().split(' ').join('')==r.message[i].heading){
        				var child = frm.add_child("proposal_index");
						frappe.model.set_value(child.doctype,child.name,"topic",ar[i]);
						frappe.model.set_value(child.doctype,child.name,"page",r.message[i].page_no);
						frm.refresh_field("proposal_index")
        			}
					
				}
				get_proposal_template(frm);
        	}
        })
	},
	mf_generate:function(frm){
		frm.clear_table("mf_plc_items")
		frm.refresh_field("mf_plc_items");
		var ar=["PLC","PANEL"];
		for(var i=0;i<ar.length;i++){
			var child = frm.add_child("mf_plc_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", ar[i]);
			frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
			frappe.model.set_value(child.doctype, child.name, "unit_price", 0);
			frappe.model.set_value(child.doctype, child.name, "total_price", 0);
			frm.refresh_field("mf_plc_items");
		}
		frm.clear_table("mf_full_system")
		frm.refresh_field("mf_full_system");
		$.each(frm.doc.mf_table || [], function(i, v) {
			if(v.unit_price > 0)
			{
				var child = frm.add_child("mf_full_system");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price);
				frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price);
				frm.refresh_field("mf_full_system");
			}
		});
		$.each(frm.doc.mf_not_linked_table || [], function(i, v) {
			var child = frm.add_child("mf_full_system");
			frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
			frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
			frappe.model.set_value(child.doctype, child.name, "flow", v.req_flow);
			frappe.model.set_value(child.doctype, child.name, "range", v.range);
			frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
			frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
			frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
			frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price);
			frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price);
			frm.refresh_field("mf_full_system");
		});
		
	},
	mbr_generate:function(frm){
		frm.clear_table("mbrk_plc_items")
		frm.refresh_field("mbrk_plc_items");
		var ar=["PLC","PANEL"];
		for(var i=0;i<ar.length;i++){
			var child = frm.add_child("mbrk_plc_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", ar[i]);
			frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
			frappe.model.set_value(child.doctype, child.name, "unit_price", 0);
			frappe.model.set_value(child.doctype, child.name, "total_price", 0);
			frm.refresh_field("mbrk_plc_items");
		}
		frm.clear_table("mbrk_full_system")
		frm.refresh_field("mbrk_full_system");
		$.each(frm.doc.mbr_koch_table || [], function(i, v) {
			if(v.unit_price > 0)
			{
				var child = frm.add_child("mbrk_full_system");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price+(v.motor_cost/(v.w_qty+v.sb_qty+v.ssb_qty)));
				frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price);
				frm.refresh_field("mbrk_full_system");
			}
		});
		$.each(frm.doc.mbr_koch_not_linked || [], function(i, v) {
			var child = frm.add_child("mbrk_full_system");
			frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
			frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
			frappe.model.set_value(child.doctype, child.name, "flow", v.req_flow);
			frappe.model.set_value(child.doctype, child.name, "range", v.range);
			frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
			frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
			frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
			frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price+(v.motor_cost/(v.w_qty+v.sb_qty+v.ssb_qty)));
			frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price+v.motor_cost);
			frm.refresh_field("mbrk_full_system");
		});
		
	},
	mbro_generate:function(frm){
		frm.clear_table("mbro_plc_items")
		frm.refresh_field("mbro_plc_items");
		var ar=["PLC","PANEL"];
		for(var i=0;i<ar.length;i++){
			var child = frm.add_child("mbro_plc_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", ar[i]);
			frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
			frappe.model.set_value(child.doctype, child.name, "unit_price", 0);
			frappe.model.set_value(child.doctype, child.name, "total_price", 0);
			frm.refresh_field("mbro_plc_items");
		}
		frm.clear_table("mbro_full_system")
		frm.refresh_field("mbro_full_system");
		$.each(frm.doc.mbr_ovivo_table || [], function(i, v) {
			if(v.unit_price > 0)
			{
				var child = frm.add_child("mbro_full_system");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price+(v.motor_cost/(v.w_qty+v.sb_qty+v.ssb_qty)));
				frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price);
				frm.refresh_field("mbro_full_system");
			}
		});
		$.each(frm.doc.mbr_ovivo_not_linked_items || [], function(i, v) {
			var child = frm.add_child("mbro_full_system");
			frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
			frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
			frappe.model.set_value(child.doctype, child.name, "flow", v.req_flow);
			frappe.model.set_value(child.doctype, child.name, "range", v.range);
			frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
			frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
			frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
			frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price+(v.motor_cost/(v.w_qty+v.sb_qty+v.ssb_qty)));
			frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price+v.motor_cost);
			frm.refresh_field("mbro_full_system");
		});
	},
	bio_generate:function(frm){
		append_bio_plc_items(frm);
		append_bio_full_and_pre_treatment_full(frm);
		append_pre_treatment_special_table(frm);
	},
	bio_calculate:function(frm){
		$.each(frm.doc.pre_treatment_full_system || [], function(i, v) {
			var tp=0
			$.each(frm.doc.bio_all_items || [], function(ii, vv) {
				if(vv.system==v.item_description){
					tp=tp+vv.total_price
				}
			});
			frappe.model.set_value(v.doctype, v.name, "unit_price", tp);
			frappe.model.set_value(v.doctype, v.name, "full_total_price", (tp+v.bom_unit_price)*v.w_qty);
			var total_wo_pipe = ((tp+v.bom_unit_price)*v.w_qty);
			$.each(frm.doc.pipe_escalation || [], function(iii, vvv) {
				var pipe=0
				if(vvv.system_name==v.item_description){
					pipe = total_wo_pipe*(vvv.default_pipe_escalation/100)
					if(vvv.actual_pipe_escalation){
						pipe = total_wo_pipe*(vvv.actual_pipe_escalation/100)
					}
					frappe.model.set_value(v.doctype, v.name, "pipe", pipe);
				}
			})
			var total = ((tp+v.bom_unit_price)*v.w_qty)+v.erection+v.fabrication+v.pipe;
			frappe.model.set_value(v.doctype, v.name, "total_price_with_erefab", total);
			frm.refresh_field("pre_treatment_full_system");
		});
		calculate_pre_treatment_special_table(frm)
	},
	cts_generate:function(frm){
		frm.clear_table("cts_plc_items")
		frm.refresh_field("cts_plc_items");
		var ar=["PLC","PANEL"];
		for(var i=0;i<ar.length;i++){
			var child = frm.add_child("cts_plc_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", ar[i]);
			frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
			frappe.model.set_value(child.doctype, child.name, "unit_price", 0);
			frappe.model.set_value(child.doctype, child.name, "total_price", 0);
			frm.refresh_field("cts_plc_items");
		}
		frm.clear_table("cts_full_system")
		frm.refresh_field("cts_full_system");
		$.each(frm.doc.cts_items || [], function(i, v) {
			if(v.unit_price > 0)
			{
				var child = frm.add_child("cts_full_system");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price);
				frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price);
				frm.refresh_field("cts_full_system");
			}
		});
		$.each(frm.doc.cts_not_linked_items || [], function(i, v) {
			var child = frm.add_child("cts_full_system");
			frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
			frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
			frappe.model.set_value(child.doctype, child.name, "flow", v.req_flow);
			frappe.model.set_value(child.doctype, child.name, "range", v.range);
			frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
			frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
			frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
			frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price);
			frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price);
			frm.refresh_field("cts_full_system");
		});
	},
	mbr_cts_generate:function(frm){
		frm.clear_table("mbr_cts_plc_items")
		frm.refresh_field("mbr_cts_plc_items");
		var ar=["PLC","PANEL"];
		for(var i=0;i<ar.length;i++){
			var child = frm.add_child("mbr_cts_plc_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", ar[i]);
			frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
			frappe.model.set_value(child.doctype, child.name, "unit_price", 0);
			frappe.model.set_value(child.doctype, child.name, "total_price", 0);
			frm.refresh_field("mbr_cts_plc_items");
		}
		frm.clear_table("mbr_cts_full_system")
		frm.refresh_field("mbr_cts_full_system");
		$.each(frm.doc.mbr_cts_table || [], function(i, v) {
			if(v.unit_price > 0)
			{
				var child = frm.add_child("mbr_cts_full_system");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price+(v.motor_cost/(v.w_qty+v.sb_qty+v.ssb_qty)));
				frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price);
				frm.refresh_field("mbr_cts_full_system");
			}
		});
		$.each(frm.doc.mbr_cts_not_linked_items || [], function(i, v) {
			var child = frm.add_child("mbr_cts_full_system");
			frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
			frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
			frappe.model.set_value(child.doctype, child.name, "flow", v.req_flow);
			frappe.model.set_value(child.doctype, child.name, "range", v.range);
			frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
			frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
			frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
			frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price+(v.motor_cost/(v.w_qty+v.sb_qty+v.ssb_qty)));
			frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price+v.motor_cost);
			frm.refresh_field("mbr_cts_full_system");
		});
	},
	dgt_generate:function(frm){
		frm.clear_table("dgt_plc_items")
		frm.refresh_field("dgt_plc_items");
		var ar=["PLC","PANEL"];
		for(var i=0;i<ar.length;i++){
			var child = frm.add_child("dgt_plc_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", ar[i]);
			frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
			frappe.model.set_value(child.doctype, child.name, "unit_price", 0);
			frappe.model.set_value(child.doctype, child.name, "total_price", 0);
			frm.refresh_field("dgt_plc_items");
		}
		frm.clear_table("dgt_full_system")
		frm.refresh_field("dgt_full_system");
		$.each(frm.doc.dgt_items || [], function(i, v) {
			if(v.unit_price > 0)
			{
				var child = frm.add_child("dgt_full_system");
				frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
				frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
				frappe.model.set_value(child.doctype, child.name, "flow", v.flow);
				frappe.model.set_value(child.doctype, child.name, "range", v.range);
				frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
				frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
				frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
				frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price);
				frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price);
				frm.refresh_field("dgt_full_system");
			}
		});
		$.each(frm.doc.dgt_not_linked_items || [], function(i, v) {
			var child = frm.add_child("dgt_full_system");
			frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
			frappe.model.set_value(child.doctype, child.name, "renamed", v.renamed);
			frappe.model.set_value(child.doctype, child.name, "flow", v.req_flow);
			frappe.model.set_value(child.doctype, child.name, "range", v.range);
			frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
			frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
			frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
			frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price);
			frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price);
			frm.refresh_field("dgt_full_system");
		});
	},
	edit:function(frm){
		frappe.call({
			method:"edit_pdf",
			doc:frm.doc
		})
	}
});

frappe.ui.form.on('Cost Working Tool BOM', {
	qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_cost", child.qty * child.cost);
	},
	cost:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_cost", child.qty * child.cost);
	} 
});

frappe.ui.form.on('Cost Working Tool Exploded Item',{
	qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", child.qty * child.rate);
	},
	rate:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "amount", child.qty * child.rate);
	}
});
frappe.ui.form.on('Erection Cost Table', {
	qty:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.unit_price*child.qty);
		frm.refresh_field("total_price");
	}
});

frappe.ui.form.on('MF Not linked items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('MBR KOCH Not linked', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('MBR Ovivo Not Linked Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('Bio Not Linked Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('MBR CTS Not Linked Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('CTS Not Linked Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('Degasser System Not linked items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});

frappe.ui.form.on("MF Electrical Items",{
	kw:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		if(child.kw>5.5){
			frappe.model.set_value(cdt, cdn, "type","S/D FEEDER");
		}
		else{
			frappe.model.set_value(cdt, cdn, "type","DOL FEEDER");
		}
	}
})
frappe.ui.form.on("MBR Electrical Items",{
	kw:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		if(child.kw>5.5){
			frappe.model.set_value(cdt, cdn, "type","S/D FEEDER");
		}
		else{
			frappe.model.set_value(cdt, cdn, "type","DOL FEEDER");
		}
	}
})
frappe.ui.form.on("MBR Ovivo Electrical Items",{
	kw:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		if(child.kw>5.5){
			frappe.model.set_value(cdt, cdn, "type","S/D FEEDER");
		}
		else{
			frappe.model.set_value(cdt, cdn, "type","DOL FEEDER");
		}
	}
})
frappe.ui.form.on("Bio Electrical Items",{
	kw:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		if(child.kw>5.5){
			frappe.model.set_value(cdt, cdn, "type","S/D FEEDER");
		}
		else{
			frappe.model.set_value(cdt, cdn, "type","DOL FEEDER");
		}
	}
})
frappe.ui.form.on("CTS Electrical Items",{
	kw:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		if(child.kw>5.5){
			frappe.model.set_value(cdt, cdn, "type","S/D FEEDER");
		}
		else{
			frappe.model.set_value(cdt, cdn, "type","DOL FEEDER");
		}
	}
})
frappe.ui.form.on("Degasser System Electrical Items",{
	kw:function(frm,cdt,cdn){
		var child = locals[cdt][cdn];
		if(child.kw>5.5){
			frappe.model.set_value(cdt, cdn, "type","S/D FEEDER");
		}
		else{
			frappe.model.set_value(cdt, cdn, "type","DOL FEEDER");
		}
	}
})

frappe.ui.form.on('MF Full System', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('Koch Full System', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('Ovivo Full System', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('Pre Treatment Full System', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});

frappe.ui.form.on('CTS Full System', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('CTS MBR Full System', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('Degasser Full System', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",(child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('MF PLC Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('MBR KOCH PLC Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('MBR OVIVO PLC Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('BIO PLC Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('CTS PLC Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('MBR CTS PLC Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('DGT PLC Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",child.w_qty*child.unit_price);
		frm.refresh_field("total_price");
	}
});
frappe.ui.form.on('Bio All Items', {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",((child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price)+child.motor_cost);
		frm.refresh_field("total_price");
	},
	sb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",((child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price)+child.motor_cost);
		frm.refresh_field("total_price");
	},
	ssb_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",((child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price)+child.motor_cost);
		frm.refresh_field("total_price");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",((child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price)+child.motor_cost);
		frm.refresh_field("total_price");
	},
	motor_cost: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price",((child.w_qty+child.sb_qty+child.ssb_qty)*child.unit_price)+child.motor_cost);
		frm.refresh_field("total_price");
	}
});
var list_electrical_items = function (frm) {
	if(frm.doc.mf_electrical_items){

	}
	else{
		var mf_ele=["PRE-FILTER","FEED PUMP", "BACKWASH PUMP", "CIP PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "SULPHUR BLACK DOSING PUMP","PANEL","PLC"]
		var item37=["PRE-FILTER"]
		var item18=["SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "SULPHUR BLACK DOSING PUMP"]
		var plc=["PANEL","PLC"]
		for(var i=0;i<mf_ele.length;i++)
		{
		var child = frm.add_child("mf_electrical_items");
		frappe.model.set_value(child.doctype, child.name, "item_description", mf_ele[i]);
		frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
		if(item37.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 0.37);
			frm.refresh_field("kw");
		}
		if(item18.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 0.18);
			frm.refresh_field("kw");
		}
		if(plc.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 1);
			frm.refresh_field("kw");
		}
		frm.refresh_field("mf_electrical_items");
		}
	}
	if(frm.doc.mbr_electrical_items){

	}
	else{
		var mbr_ele=["FEED PUMP", "PERMEATE/BACKWASH/CIP PUMP","BLOWER", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3", "SULPHUR BLACK DOSING PUMP", "PANEL", "PLC"]
		var items018=["CIP DOSING PUMP-1","CIP DOSING PUMP-2","SULPHUR BLACK DOSING PUMP"];
		var items037=["PRE-FILTER"];
		var plc=["PANEL","PLC"]
		for(var i=0;i<mbr_ele.length;i++)
		{
		var child = frm.add_child("mbr_electrical_items");
		frappe.model.set_value(child.doctype, child.name, "item_description", mbr_ele[i]);
		frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
		if(item37.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 0.37);
			frm.refresh_field("kw");
		}
		if(item18.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 0.18);
			frm.refresh_field("kw");
		}
		if(plc.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 1);
			frm.refresh_field("kw");
		}
		frm.refresh_field("mbr_electrical_items");
		}
	}
	if(frm.doc.ovivo_electrical_items){

	}
	else{
		var ovivo_ele=["FEED PUMP", "PERMEATE PUMP", "BACKWASH/CIP PUMP", "SLUDGE EXTRACT PUMP", "SLUDGE RECIRCULATION PUMP", "SPRINKLER PUMP", "SULPHUR BLACK SLUDGE PUMP", "CIP DOSING PUMP-1", "CIP DOSING PUMP-2", "CIP DOSING PUMP-3", "SULPHUR BLACK DOSING PUMP", "PANEL", "PLC"]
		var items018=["CIP DOSING PUMP-1","CIP DOSING PUMP-2","SULPHUR BLACK DOSING PUMP"];
		var items037=["PRE-FILTER"];
		var plc=["PANEL","PLC"]
		for(var i=0;i<ovivo_ele.length;i++)
		{
		var child = frm.add_child("ovivo_electrical_items");
		frappe.model.set_value(child.doctype, child.name, "item_description", ovivo_ele[i]);
		frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
		if(item37.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 0.37);
			frm.refresh_field("kw");
		}
		if(item18.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 0.18);
			frm.refresh_field("kw");
		}
		if(plc.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 1);
			frm.refresh_field("kw");
		}
		frm.refresh_field("ovivo_electrical_items");
		}
	}
	if(frm.doc.bio_electrical_items){

	}
	else{
		var bio_ele=["LIFTING SUMP PUMP", "EQT BLOWER", "EQT FLOW MAKER", "DAF BUBBLE GENERATION PUMP", "DAF SLUDGE PUMP", "NT PUMP", "NT DOSING PUMP", "DNT FLOW MAKER", "DNT PUMP", "BIO BLOWER", "BIO FLOW MAKER","WASHING PUMP", "PANEL", "PLC"]
		var plc=["PANEL","PLC"]
		for(var i=0;i<bio_ele.length;i++)
		{
		var child = frm.add_child("bio_electrical_items");
		frappe.model.set_value(child.doctype, child.name, "item_description", bio_ele[i]);
		frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
		frappe.model.set_value(child.doctype, child.name, "kw", 0.18);
		if(plc.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 1);
		}
		frm.refresh_field("bio_electrical_items");
		}
	}
	if(frm.doc.cts_electrical_items){

	}
	else{
		var cts_ele=["FEED PUMP", "SLUDGE PUMP", "DOSING PUMP-1", "DOSING PUMP-2", "DOSING PUMP-3", "DOSING PUMP-4", "DOSING PUMP-5", "AGITATOR", "CIRCULAR CLARIFIER","PANEL","PLC"]
		var plc=["PANEL","PLC"]
		for(var i=0;i<cts_ele.length;i++)
		{
		var child = frm.add_child("cts_electrical_items");
		frappe.model.set_value(child.doctype, child.name, "item_description", cts_ele[i]);
		frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
		frappe.model.set_value(child.doctype, child.name, "kw", 0.18);
		if(plc.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 1);
		}
		frm.refresh_field("cts_electrical_items");
		}
	}
	if(frm.doc.dgt_electrical_items){

	}
	else{
		var dgt_ele=["BLOWER","DOSING PUMP","PANEL","PLC"]
		var plc=["PANEL","PLC"]
		for(var i=0;i<dgt_ele.length;i++)
		{
		var child = frm.add_child("dgt_electrical_items");
		frappe.model.set_value(child.doctype, child.name, "item_description", dgt_ele[i]);
		frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
		frappe.model.set_value(child.doctype, child.name, "kw", 0.18);
		if(plc.includes(child.item_description)){
			frappe.model.set_value(child.doctype, child.name, "kw", 1);
		}
		frm.refresh_field("dgt_electrical_items");
		}
	}
}
var make_null_to_nil = function(frm){
	if(frm.doc.bod_v>0){frm.doc.bod_v=frm.doc.bod_v}else{frm.doc.bod_v="NIL"}
	if(frm.doc.cod_v>0){frm.doc.cod_v=frm.doc.cod_v}else{frm.doc.cod_v="NIL"}
	if(frm.doc.tdsmgl>0){frm.doc.tdsmgl=frm.doc.tdsmgl}else{frm.doc.tdsmgl="NIL"}
	if(frm.doc.tss>0){frm.doc.tss=frm.doc.tss}else{frm.doc.tss="NIL"}
	if(frm.doc.tkn>0){frm.doc.tkn=frm.doc.tkn}else{frm.doc.tkn="NIL"}
	if(frm.doc.pva>0){frm.doc.pva=frm.doc.pva}else{frm.doc.pva="NIL"}
	if(frm.doc.iron>0){frm.doc.iron=frm.doc.iron}else{frm.doc.iron="NIL"}
	if(frm.doc.silica>0){frm.doc.silica=frm.doc.silica}else{frm.doc.silica="NIL"}
	if(frm.doc.hardness>0){frm.doc.hardness=frm.doc.hardness}else{frm.doc.hardness="NIL"}
	if(frm.doc.alkali>0){frm.doc.alkali=frm.doc.alkali}else{frm.doc.alkali="NIL"}
	if(frm.doc.temperature>0){frm.doc.temperature=frm.doc.temperature}else{frm.doc.temperature="NIL"}
	if(frm.doc.oil_grease>0){frm.doc.oil_grease=frm.doc.oil_grease}else{frm.doc.oil_grease="NIL"}
	if(frm.doc.sulphate>0){frm.doc.sulphate=frm.doc.sulphate}else{frm.doc.sulphate="NIL"}
	if(frm.doc.chloride>0){frm.doc.chloride=frm.doc.chloride}else{frm.doc.chloride="NIL"}
}

frappe.ui.form.on("Bio Full System", {
	go_to_reference: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		var openlink = window.open("https://erp.wttindia.com/app/query-report/BOM?bom="+child.bom_reference+"","_target");
		// var child = locals[cdt][cdn];
		// if(child.item_description == 'PRESSURE VESSEL')
		// {
		// 	var vvs = Math.ceil((child.range * 14.5038) / 10) * 10
		// 	frappe.model.set_value(cdt, cdn, "model_no", vvs);
		// 	refresh_field("model_no");
		// }
	}
});


frappe.ui.form.on("Pre Treatment Full System", {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "full_total_price", child.w_qty * (child.unit_price+child.bom_unit_price));
		refresh_field("full_total_price");

		frappe.model.set_value(cdt, cdn, "total_price_with_erefab", child.full_total_price + child.erection + child.fabrication + child.pipe);
		refresh_field("total_price_with_erefab");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "full_total_price", child.w_qty * (child.unit_price+child.bom_unit_price));
		refresh_field("full_total_price");

		frappe.model.set_value(cdt, cdn, "total_price_with_erefab", child.full_total_price + child.erection + child.fabrication + child.pipe);
		refresh_field("total_price_with_erefab");
	},
	erection: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price_with_erefab", child.full_total_price + child.erection + child.fabrication + child.pipe);
		refresh_field("total_price_with_erefab");
	},
	fabrication: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price_with_erefab", child.full_total_price + child.erection + child.fabrication + child.pipe);
		refresh_field("total_price_with_erefab");
	},
	pipe: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price_with_erefab", child.full_total_price + child.erection + child.fabrication + child.pipe);
		refresh_field("total_price_with_erefab");
	}
});
frappe.ui.form.on("Pre Treatment Special Table", {
	w_qty: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "full_total_price", child.w_qty * (child.unit_price+child.bom_unit_price));
		refresh_field("full_total_price");

		frappe.model.set_value(cdt, cdn, "total_price_with_erefab", child.full_total_price + child.erection + child.fabrication + child.pipe);
		refresh_field("total_price_with_erefab");
	},
	unit_price: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "full_total_price", child.w_qty * (child.unit_price+child.bom_unit_price));
		refresh_field("full_total_price");

		frappe.model.set_value(cdt, cdn, "total_price_with_erefab", child.full_total_price + child.erection + child.fabrication + child.pipe);
		refresh_field("total_price_with_erefab");
	},
	erection: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price_with_erefab", child.full_total_price + child.erection + child.fabrication + child.pipe);
		refresh_field("total_price_with_erefab");
	},
	fabrication: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price_with_erefab", child.full_total_price + child.erection + child.fabrication + child.pipe);
		refresh_field("total_price_with_erefab");
	},
	pipe: function(frm,cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.model.set_value(cdt, cdn, "total_price_with_erefab", child.full_total_price + child.erection + child.fabrication + child.pipe);
		refresh_field("total_price_with_erefab");
	}
});

var append_pre_treatment_special_table = function(frm){
	frm.clear_table("pre_treatment_special_table")
	frappe.call({
		method:"lamella_clarifier",
		doc:frm.doc,
		callback(r){
			console.log(r.message)
			for(var i=0;i<r.message.length;i++)
			{
				var child = frm.add_child("pre_treatment_special_table");
				frappe.model.set_value(child.doctype, child.name, "item_description", r.message[i].system);
				frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
				frappe.model.set_value(child.doctype, child.name, "bom_unit_price", r.message[i].price);
				frappe.model.set_value(child.doctype, child.name, "unit_price", 0);
				frappe.model.set_value(child.doctype, child.name, "full_total_price", r.message[i].price);
				frappe.model.set_value(child.doctype, child.name, "total_price_with_erefab", 0);
				frm.refresh_field("pre_treatment_special_table");
				$.each(frm.doc.pre_treatment_special_table || [], function(i, pref) {
					$.each(frm.doc.cost_table || [], function(i, cost) {
						if(pref.item_description==cost.system)
						{
							frappe.model.set_value(pref.doctype, pref.name,'erection',cost.total_price);
							frappe.model.set_value(pref.doctype, pref.name, "total_price_with_erefab", pref.total_price_with_erefab+pref.erection);
							frm.refresh_field("erection");
						}
					});

					$.each(frm.doc.fabrication_table || [], function(i, fab) {
						if(pref.item_description=="Lamella Settler" && fab.system=="LAMELLA CLARIFIER")
			            {
			            	frappe.model.set_value(pref.doctype, pref.name,'fabrication',fab.total_charges);
							frm.refresh_field("fabrication");
			            }
			            else if(pref.item_description=="Circular Clarifier System" && fab.system=="CLARIFIER")
			            {
			            	frappe.model.set_value(pref.doctype, pref.name,'fabrication',fab.total_charges);
							frm.refresh_field("fabrication");
			            }
			            frappe.model.set_value(child.doctype, child.name, "total_price_with_erefab", pref.total_price_with_erefab+pref.fabrication);
					});
				});
			}
			
		}
	})

}
var calculate_pre_treatment_special_table = function(frm){
	$.each(frm.doc.pre_treatment_special_table || [], function(i, v) {
		var tp=0
		$.each(frm.doc.bio_all_items || [], function(ii, vv) {
			if(vv.system==v.item_description){
				tp=tp+vv.total_price
			}
		});
		frappe.model.set_value(v.doctype, v.name, "unit_price", tp);
		frappe.model.set_value(v.doctype, v.name, "full_total_price", (tp+v.bom_unit_price)*v.w_qty);
		var total_wo_pipe = ((tp+v.bom_unit_price)*v.w_qty);
		$.each(frm.doc.pipe_escalation || [], function(iii, vvv) {
			var pipe=0
			if(vvv.system_name==v.item_description){
				pipe = total_wo_pipe*(vvv.default_pipe_escalation/100)
				if(vvv.actual_pipe_escalation){
					pipe = total_wo_pipe*(vvv.actual_pipe_escalation/100)
				}
				frappe.model.set_value(v.doctype, v.name, "pipe", pipe);
			}
		})
		var total = ((tp+v.bom_unit_price)*v.w_qty)+v.erection+v.fabrication+v.pipe;
		frappe.model.set_value(v.doctype, v.name, "total_price_with_erefab", total);
		frm.refresh_field("pre_treatment_special_table");
	});
}
var append_bio_plc_items = function(frm){
	frm.clear_table("bio_plc_items")
	frm.refresh_field("bio_plc_items");
	var ar=["PLC","PANEL"];
	for(var i=0;i<ar.length;i++){
		var child = frm.add_child("bio_plc_items");
		frappe.model.set_value(child.doctype, child.name, "item_description", ar[i]);
		frappe.model.set_value(child.doctype, child.name, "w_qty", 1);
		frappe.model.set_value(child.doctype, child.name, "unit_price", 0);
		frappe.model.set_value(child.doctype, child.name, "total_price", 0);
		frm.refresh_field("bio_plc_items");
	}
}
var append_bio_full_and_pre_treatment_full = function(frm){
	frm.clear_table("bio_all_items")
		frm.refresh_field("bio_all_items");
		$.each(frm.doc.pre_treatment_table || [], function(i, v) {
			var child = frm.add_child("bio_all_items");
			frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
			frappe.model.set_value(child.doctype, child.name, "flow", v.flow);
			frappe.model.set_value(child.doctype, child.name, "range", v.range);
			frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
			frappe.model.set_value(child.doctype, child.name, "sb_qty", v.sb_qty);
			frappe.model.set_value(child.doctype, child.name, "ssb_qty", v.ssb_qty);
			frappe.model.set_value(child.doctype, child.name, "motor_cost", v.motor_cost);
			frappe.model.set_value(child.doctype, child.name, "unit_price", v.unit_price);
			frappe.model.set_value(child.doctype, child.name, "total_price", v.total_price);
			frappe.model.set_value(child.doctype, child.name, "system", v.system);
			frm.refresh_field("bio_all_items");
		});

		frm.clear_table("pre_treatment_full_system")
		frm.refresh_field("pre_treatment_full_system");
		$.each(frm.doc.bio_full_system || [], function(i, v) {
			var child = frm.add_child("pre_treatment_full_system");
			frappe.model.set_value(child.doctype, child.name, "item_description", v.item_description);
			frappe.model.set_value(child.doctype, child.name, "w_qty", v.w_qty);
			frappe.model.set_value(child.doctype, child.name, "bom_unit_price", v.unit_price);
			frappe.model.set_value(child.doctype, child.name, "unit_price", 0);
			frappe.model.set_value(child.doctype, child.name, "full_total_price", 0);
			frappe.model.set_value(child.doctype, child.name, "total_price_with_erefab", 0);
			frm.refresh_field("pre_treatment_full_system");
		});
		$.each(frm.doc.pre_treatment_full_system || [], function(i, pref) {
			$.each(frm.doc.cost_table || [], function(i, cost) {
				if(pref.item_description==cost.system)
				{
					frappe.model.set_value(pref.doctype, pref.name,'erection',cost.total_price);
					frappe.model.set_value(pref.doctype, pref.name, "total_price_with_erefab", pref.total_price_with_erefab+pref.erection);
					frm.refresh_field("erection");
				}
			});

			$.each(frm.doc.fabrication_table || [], function(i, fab) {
				if(pref.item_description=="Sludge Thickener" && fab.system=="SLUDGE THICKENER")
				{
					frappe.model.set_value(pref.doctype, pref.name,'fabrication',fab.total_charges);
					frm.refresh_field("fabrication");
				}
                else if(pref.item_description=="Lamella Settler" && fab.system=="LAMELLA CLARIFIER")
                {
                	frappe.model.set_value(pref.doctype, pref.name,'fabrication',fab.total_charges);
					frm.refresh_field("fabrication");
                }
                else if(pref.item_description=="Rotary Brush Screener" && fab.system=="SCREENER")
                {
                	frappe.model.set_value(pref.doctype, pref.name,'fabrication',fab.total_charges);
					frm.refresh_field("fabrication");
                }
                else if(pref.item_description =="Cooling Tower" && fab.system=="COOLING TOWER")
                {
                	frappe.model.set_value(pref.doctype, pref.name,'fabrication',fab.total_charges);
					frm.refresh_field("fabrication");
                }
                else if(pref.item_description=="Circular Clarifier System" && fab.system=="CLARIFIER")
                {
                	frappe.model.set_value(pref.doctype, pref.name,'fabrication',fab.total_charges);
					frm.refresh_field("fabrication");
                }
                frappe.model.set_value(pref.doctype, pref.name, "total_price_with_erefab", pref.total_price_with_erefab+pref.fabrication);
			});
		});
}
var get_proposal_template = function(frm){
	frappe.call({
			method:"wtt_module.process_and_costing.doctype.cost_working_tool.cost_working_tool.get_values",
			args:{
				startup_sheet:frm.doc.project_startup_sheet,
				ro:frm.doc.choose_ro_template,
				rro:frm.doc.choose_rro_template
			},
			callback(r){
				var ss_ar=r.message[0];
				var ro_ar=r.message[1]
				var rro_ar=r.message[2]
				var selected_system_array=[];
				$.each(frm.doc.selected_process_system || [], function(ii, vv) {
					selected_system_array.push(vv.selected_system_name);
				});
				// console.clear()
				// var vs = '<style>@page{size:A4;}.left-td{text-align:left!important}div{margin: 5px;text-align: justify; text-justify: inter-word;}.vv:not(.nested):before {float: left;width: 0;white-space: nowrap;content:". . . . . . . . . . . . . . . . . . . . "". . . . . . . . . . . . . . . . . . . . "". . . . . . . . . . . . . . . . . . . . "". . . . . . . . . . . . . . . . . . . . "}.vv a:first-child {padding-right: 0.33em;background: white}table, th, td {border: 1px solid black;border-collapse: collapse;text-align:center;}table td{vertical-align: middle;}th{color:#012673}header{position:fixed;top:0;margin: 0px}footer{position:fixed;bottom:0}</style>';
				// var vs = '<style>@page{size:A4;}.left-td{text-align:left!important}div{margin: 5px;text-align: justify; text-justify: inter-word;}.vv a:first-child {padding-right: 0.33em;background: white}table, th, td {border: 1px solid black;border-collapse: collapse;text-align:center;}table td{vertical-align: middle;}th{color:#012673}header{position:fixed;top:0;margin: 0px}footer{position:fixed;bottom:0}</style>';
				var vs='<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">'
				// vs+='<header><center><img width=60 height=90 src="https://erp.wttindia.com/files/wttpng.png"></center></header>'
				vs+='<br><div id="source-html" class="content">';
				const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
				var today = new Date();
				var dd = String(today.getDate()).padStart(2, '0');
				var mm = monthNames[(today.getMonth())]
				var yyyy = today.getFullYear();
				today = dd + '-' + mm + '-' + yyyy;
				var today2 = dd + '.' + mm + '.' + yyyy;
				vs+='<p align="right" style="font-family:Roboto;font-size: 18px;">'+today+'</p>';
				vs+='<p style="font-weight:bold;color:#002063;font-family:Roboto;font-size: 18px;">To,<br><br>';
				if(frm.doc.company_name!=undefined){vs+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;M/s. '+frm.doc.company_name+',<br>'}
				if(frm.doc.district!=undefined){vs+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+frm.doc.district+',<br>'}
				if(frm.doc.state!=undefined){vs+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+frm.doc.state+',<br>'}
				vs+='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+frm.doc.country+'.</p><br>'
				vs+='<p style="font-family:Roboto;font-size: 18px;">Our Ref: Techno Commercial Proposal for '+frm.doc.proposal_for+'</p>'
				var country_code = (frm.doc.country).slice(0, 3);
				if(frm.doc.country=="India"){
					country_code = 'IN'+frm.doc.state_code+'/'+frm.doc.district_code

				}
				frm.set_value("footer_date",today2);frm.refresh_field("footer_date")
				frm.set_value("county_code",country_code);frm.refresh_field("county_code")
				var footer = today2+'/'+frm.doc.project+'/'+country_code+'/'+frm.doc.abbr+'/'+(frm.doc.flow/1000)+'M/U'+frm.doc.unit_code+'/R'+frm.doc.revision_code+'/TCP.'
				vs+='<p style="font-family:Roboto;font-size: 18px;">[Proposal No: '+today2+'/'+frm.doc.project+'/'+country_code.toUpperCase()+'/'+frm.doc.abbr+'/'+(frm.doc.flow/1000)+'M/U'+frm.doc.unit_code+'/R'+frm.doc.revision_code+'/TCP].</p>'
				vs+='<p style="font-family:Roboto;font-size: 18px;"><br>Dear Sir,<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;WTT International Private Limited (WTT) is pleased to provide M/s.'+frm.doc.company_name+', with the Techno Commercial offer for supply of engineering & materials for '+frm.doc.proposal_for+' of capacity '+frm.doc.flow+' M<span>&sup3;</span>/Day. In developing this offer WTT worked with you in an effort to understand your project and business needs. The attached proposal outlines the solutions we feel will best meet these objectives.</p>'
				vs+='<p style="font-family:Roboto;font-size: 18px;"><br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We greatly appreciate your consideration of WTT for this project. Our measure of success is how well we deliver solutions that help our Client to meet their critical business objectives. We hope to have the opportunity to demonstrate this with your good selves.</p>'
				vs+='<p style="font-family:Roboto;font-size: 18px;"><br>Yours Sincerely,</p>'
				vs+='<p style="font-family:Roboto;font-size: 18px;"><br>D.Venkatesh</p>'
				vs+='<p style="font-family:Roboto;font-size: 18px;">Managing Director<br></p>'
				vs+='<p style="page-break-before:always"></p><br>'
				vs+='<p style="font-family:Roboto;font-size: 18px;"><br>Proposal for:</p>'
				vs+='<p style="font-family:Roboto;font-size: 18px;">&nbsp;&nbsp;&nbsp;&nbsp;1) '+frm.doc.proposal_for+' of capacity '+frm.doc.flow+' M<span>&sup3;</span>/Day.</p>'
				vs+='<p style="font-family:Roboto;font-size: 18px;">Proposal No: '+today2+'/'+frm.doc.project+'/'+country_code.toUpperCase()+'/'+frm.doc.abbr+'/'+(frm.doc.flow/1000)+'M/U'+frm.doc.unit_code+'/R'+frm.doc.revision_code+'/TCP.</p>'
				vs+='<br><br><p style="font-weight:bold;color:#002063;font-family:Roboto;font-size: 20px;">CONFIDENTIALITY</p>'
				vs+='<p><i>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;All details, specifications, drawings, images, and all other information submitted by us are only intended to the person/organization to which it is addressed and contains proprietary, confidential and or privileged material. Any review, retransmission, dissemination, or other use of, or of taking action in reliance upon this information by person or entities other than the intended recipient is prohibited. All or part information contained in the document is solely intended to the person or entity addresses and sharing this document in part or in whole is prohibited.</i></p>'
				vs+='<br><p><i>Thanks for understanding…</i></p><br>'
				vs+='<br><br><br><br><br><br><br><br><br><br><center><p style="font-weight:bold;color:#002063;font-family:Roboto;font-size: 20px;">We Feel Delighted to Present Our Patented Systems</p></center><br>'
				vs+='<br><center><img src="https://erp.wttindia.com/files/PATENTED 3 LOGOS.png"></center>'
				vs+='<p style="font-family:Roboto;font-size: 18px;text-align:right;"> '+today2+'/'+frm.doc.project+'/'+country_code.toUpperCase()+'/'+frm.doc.abbr+'/'+(frm.doc.flow/1000)+'M/U'+frm.doc.unit_code+'/R'+frm.doc.revision_code+'/TCP.</p>'
				vs+='<p style="page-break-before:always"></p><br>'
				vs+='<center><p style="font-weight:bold;color:#002063;font-family:Roboto;font-size: 18px;">CONTENT</p></center>'
				var asu=[]
				var asutype=[]
				$.each(frm.doc.selected_process_system, function (index, source_row) {
					asu.push(source_row.selected_system_name)
				});
				$.each(frm.doc.selected_process_system, function (index, source_row) {
					asutype.push(source_row.selected_type)
				});
				var asu_top=[]
				if(asu.length>0){
					if(asu.includes('Rotary Brush Screener')){ asu_top.push('ROTARY BRUSH SCREENER') }
					if(asu.includes('DAF (Dissolved Air Flotation)')){ asu_top.push('DISSOLVED AIR FLOTATION (DAF) SYSTEM') }
					if(asu.includes('Equalization System')){ asu_top.push('EQUALIZATION SYSTEM') }
					if(asu.includes('Neutralization System')){ asu_top.push('NEUTRALIZATION SYSTEM') }
					if(asu.includes('Cooling Tower')){ asu_top.push('COOLING TOWER') }
					if(asu.includes('Biological Oxidation System')){ asu_top.push('BIOLOGICAL SYSTEM') }
					if(asu.includes('Lamella Settler')){ asu_top.push('LAMELLA SETTLER') }
					if(asu.includes('Circular Clarifier System')){ asu_top.push('CIRCULAR CLARIFIER') }
					if(asu.includes('Sludge Thickener with mech')){ asu_top.push('SLUDGE THICKENER') }
					if(asu.includes('Belt Press')){ asu_top.push('BELT PRESS SYSTEM') }
					if(asu.includes('Screw Press')){ asu_top.push('SCREW PRESS') }
					if(asu.includes('Micro Filtration - ASAHI')){ asu_top.push('MICRO/ULTRA FILTRATION SYSTEM') }
					if(asu.includes('Submerged MBR system - KOCH')){ asu_top.push('SUBMERGED MBR SYSTEM - KOCH') }
					if(asu.includes('Submerged MBR system - OVIVO')){ asu_top.push('SUBMERGED MBR SYSTEM - OVIVO') }
					if(asu.includes('Sulphur Black Removal System')){ asu_top.push('SULPHUR BLACK REMOVAL SYSTEM') }
					if(asu.includes('Degasser System')){ asu_top.push('DEGASSER TOWER SYSTEM') }
					if(asu.includes('Reverse Osmosis')){ asu_top.push('REVERSE OSMOSIS SYSTEM') }
				}
				if((frm.doc.proposal_index).length==0){
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>1. Technical And Engineering Details</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno1</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>1.1. BASIS OF DESIGN</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno2</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>1.2. INFLUENT QUALITY</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno3</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>1.3. INFLUENT FLOW DATA</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno4</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>1.4. OPERATIONAL BASIS</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno5</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>1.5. PROCESS COMPATIBILITY</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno6</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>2. Design System Chosen</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno7</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>2.1. EXPECTED TREATED WATER QUALITY</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno8</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>3. Scope Of Supply - Equipment, Engineering & Services</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno9</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>4. Equipment Details For Proposed Systems</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno10</a></div>'
					vs+='</div>'
					for(var i=0;i<asu_top.length;i++)
					{
						var ind = (i+1);
						vs+='<div style="display:inline-flex;width:100%;">'
						vs+='<div class="vv" style="text-align:left;width:90%"><a>4.'+ind+'. '+asu_top[i]+'</a></div>'
						vs+='<div style="text-align:right;width:10%"><a>pageno'+(10+ind)+'</a></div>'
						vs+='</div>'
						// vs+='<p class="vv" align="justify" style="font-family:Roboto;font-size: 18px;"><a>4.'+i+'.  '+asu[i]+'</a></p>'
					}
					var assu = asu_top.length;
					var ind = assu+10
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>5. Equipment Quantity</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+1)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>6. Typical Equipment Vendor List</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+2)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>7. Pricing Detail</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+3)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>8. Exclusions</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+4)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>9. Happy Customers</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+5)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>10. Channel Partners</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+6)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>11. Process Description Video</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+7)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>12. Commercial Terms And Conditions</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+8)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>12.1. TAXES</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+9)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>12.2. FREIGHT</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+10)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>12.3. INVOICING AND PAYMENT TERMS</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+11)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>12.4. EQUIPMENT SHIPMENT</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+12)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>12.5. PRICING NOTES</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+13)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>13. Client Scope Of Supply</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+14)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>13.1. SAFETY AND ENVIRONMENTAL</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+15)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>13.2. JOBSITE AND INSTALLATION REVIEW</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+16)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>13.3. START-UP AND COMMISSIONING</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+17)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>13.4. FACILITY MANAGEMENT</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+18)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>13.5. CONDITIONAL OFFERING</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+19)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>14. Appendix</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+20)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>14.1. APPENDIX A: CLARIFICATIONS</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+21)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>14.2. APPENDIX B:  ACCEPTANCE</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+22)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>14.3. APPENDIX C:  WARRANTY</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+23)+'</a></div>'
					vs+='</div>'
					vs+='<div style="display:inline-flex;width:100%;">'
					vs+='<div class="vv" style="text-align:left;width:90%"><a>14.4. APPENDIX D:  CONFIDENTIALITY</a></div>'
					vs+='<div style="text-align:right;width:10%"><a>pageno'+(ind+24)+'</a></div>'
					vs+='</div>'
				}
				else{
					$.each(frm.doc.proposal_index, function (i, v) {
						vs+='<div style="display:inline-flex;width:100%;">'
						vs+='<div class="vv" style="text-align:left;width:90%"><a>'+v.topic+'</a></div>'
						vs+='<div style="text-align:right;width:10%"><a>'+v.page+'</a></div>'
						vs+='</div>'
					});
				}
				
				vs+='<p style="page-break-before:always"></p><br>'
				// vs+='<center><img width=60 height=90 src="https://erp.wttindia.com/files/wttpng.png"></center><br><br><br>'
				vs+='<div class="pageNumberStarts"><p style="font-weight:bold;color:#002063;font-family:Roboto;font-size: 20px;">1. Technical And Engineering Details</p><br>';
				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">1.1. BASIS OF DESIGN</p><br>';
				vs+='<p style="margin-left:30px;font-family:Roboto;font-size: 18px;">This proposal is based on the following design basis:</p><br>';
				if(asu.includes("Rotary Brush Screener"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Rotary Brush Screener system proposed to remove coarse particles from the Effluent water</li></ul>';
				}
				if(asu.includes("DAF (Dissolved Air Flotation)r"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Dissolved Air Flotation (DAF) system proposed to remove free oil & grease</li></ul>';
				}
				if(asu.includes("Biological Oxidation System") && asu.includes("Neutralization System") && asu.includes("Cooling Tower"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>To maintain optimum pH and Temperature in the Biological Oxidation System, Neutralization system and Cooling Tower proposed</li></ul>';
				}
				else if(asu.includes("Biological Oxidation System") && asu.includes("Neutralization System"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>To maintain optimum pH in the Biological Oxidation System, Neutralization system proposed</li></ul>';
				}
				else if(asu.includes("Biological Oxidation System") && asu.includes("Cooling Tower"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>To maintain optimum Temperature in the Biological Oxidation System, Cooling Tower proposed</li></ul>';
				}
				else
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>To maintain optimum pH in the Biological Oxidation System</li></ul>';
				}
				if(asu.includes("Biological Oxidation System"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Biological Oxidation system proposed with optimum retention time to maximize the pollutant reduction</li></ul>';
				}
				if(asu.includes("Circular Clarifier System"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Circular clarifier system settler proposed for efficient separation of solids and to provide polished influent to filtration systems.</li></ul>';
				}
				if(asu.includes("Lamella Settler"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Lamella settler proposed for efficient separation of solids and to provide polished influent to filtration systems</li></ul>';	
				}
				if(asu.includes("Micro Filtration - ASAHI"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Micro/Ultra Filtration system proposed to reduce Fouling Potential of RO feed water</li></ul>';	
				}
				if(asu.includes("Submerged MBR system - KOCH") || asu.includes("Submerged MBR system - OVIVO"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Submerged MBR system proposed to reduce Fouling Potential of RO feed water</li></ul>';
				}
				if(asu.includes("Sulphur Black Removal System"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Sulphur black removal system proposed to remove sulphur dyes from the effluent water</li></ul>';
				}
				if(asu.includes("Degasser System"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Degasser tower proposed to reduce alkalinity/bicarbonate by stripping CO2 from the effluent</li></ul>';
				}
				if(asu.includes("Reverse Osmosis"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>RO system proposed to achieve recovery of '+frm.doc.ro_recovery+'%</li></ul>';
				}
				vs+='<p style="font-family:Roboto;font-size: 18px;">The following sections summarize the treatment process, the major system components, the main system design parameters and design outputs as well as design details of system components. This section does not define scope of supply. Scope delineation is covered under section 3.</p>'
				vs+='<p style="page-break-before:always"></p><br>'
				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">1.2. INFLUENT QUALITY</p>';
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:30%">PARAMETER</th><th style="width:30%">UNIT</th><th style="width:30%">'+frm.doc.abbr_inlet+' INLET</th></tr>';
				vs+='<tr><td>1. </td><td class="left-td">pH</td><td>--</td><td>8-9</td></tr>'
				vs+='<tr><td>2. </td><td class="left-td">BOD</td><td>mg/l</td><td>'+frm.doc.bod_v+'</td></tr>'
				vs+='<tr><td>3. </td><td class="left-td">COD</td><td>mg/l</td><td>'+frm.doc.cod_v+'</td></tr>'
				vs+='<tr><td>4. </td><td class="left-td">TDS</td><td>mg/l</td><td>'+frm.doc.tdsmgl+'</td></tr>'
				vs+='<tr><td>5. </td><td class="left-td">TSS</td><td>mg/l</td><td>'+frm.doc.tss+'</td></tr>'
				vs+='<tr><td>6. </td><td class="left-td">TKN</td><td>mg/l</td><td>'+frm.doc.tkn+'</td></tr>'
				vs+='<tr><td>7. </td><td class="left-td">PVA</td><td>mg/l</td><td>'+frm.doc.pva+'</td></tr>'
				vs+='<tr><td>8. </td><td class="left-td">IRON</td><td>mg/l</td><td>'+frm.doc.iron+'</td></tr>'
				vs+='<tr><td>9. </td><td class="left-td">SILICA</td><td>mg/l</td><td>'+frm.doc.silica+'</td></tr>'
				vs+='<tr><td>10. </td><td class="left-td">HARDNESS</td><td>mg/l</td><td>'+frm.doc.hardness+'</td></tr>'
				vs+='<tr><td>11. </td><td class="left-td">ALKALINITY</td><td>mg/l</td><td>'+frm.doc.alkali+'</td></tr>'
				vs+='<tr><td>12. </td><td class="left-td">TEMPERATURE</td><td>mg/l</td><td>'+frm.doc.temperature+'</td></tr>'
				vs+='<tr><td>13. </td><td class="left-td">OIL & GREASE</td><td>mg/l</td><td>'+frm.doc.oil_grease+'</td></tr>'
				if(asu.includes("Biological Oxidation System") || asu.includes("Circular Clarifier System")){
					vs+='<tr><td>14. </td><td class="left-td">SULPHATE</td><td>mg/l</td><td>'+frm.doc.sulphate+'</td></tr>'
					vs+='<tr><td>15. </td><td class="left-td">CHLORIDE</td><td>mg/l</td><td>'+frm.doc.chloride+'</td></tr>'
				}
				vs+='</table><br>NOTE: Since the *Parametrical values are not available, it has been considered for the purpose of designing the treatment system. </center>';
				vs+='<br><p style="font-family:Roboto;font-size: 18px;">The design solution proposed is based on the values as presented in the table above at '+frm.doc.abbr_inlet+' inlet. All concentrations refer to max concentrations to be used for the system’s design. Any change in the actual inlet parameters will have impact on Process Design, Engineering Design, Cost and Performance.</p>'
				vs+='<p style="page-break-before:always"></p><br>'
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">1.3. INFLUENT FLOW DATA</p>';
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="text-align:center;width:40%">PARAMETER</th><th style="text-align:center;width:30%;">VALUE</th><th style="text-align:center;width:30%">UNIT</th></tr>';
				vs+='<tr><td>'+frm.doc.abbr_inlet+' Feed Flow Rate</td><td>'+frm.doc.flow+'</td><td>M<span>&sup3;</span>/DAY</td></tr></table></center>'
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">1.4. OPERATIONAL BASIS</p>';
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><td style="width:40%;">Hours Per Day of Operation</td><td style="width:60%;">24</td></tr>';
				vs+='<tr><td>Days Per Year of Operation</td><td>350 days (Downtime for chemical cleaning and other regular annual maintenance work 15 days considered)</td></tr></table></center>'
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">1.5. PROCESS COMPATIBILITY</p><br>';
				if(asu.includes("Biological Oxidation System"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>The incoming raw wastewater shall not contain any substance incompatible with the MOC of the Equipment supplied & inhibitory substances that sufficiently affect the biological treatment stage so as to compromise the operation of any of the system.</li></ul>';
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>The biological treatment is operated and maintained in accordance with good industry practice for wastewater treatment systems.</li></ul>';
				}
				if(asu.includes("Rotary Brush Screener"))
				{
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>The Rotary Brush Screener at the plant inlet are installed and operated in such a way that fibrous material and floatable particles are removed reliably and any bypasses of the screens are impossible.</li></ul>';
				}
				if(!asu.includes("Biological Oxidation System"))
				{
					vs+='<br><center><p style="font-family:Roboto;font-size: 18px;">General</p></center><br>';
					vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>The incoming raw wastewater shall not contain any substance incompatible with the MOC of the Equipment supplied & inhibitory substances that sufficiently affect the operation of any of the system.</li></ul>';
				}
				vs+='<p style="page-break-before:always"></p><br>'
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">2. Design System Chosen</p><br>';
				vs+='<p style="margin-left:30px;font-family:Roboto;font-size: 18px;">The plant will comprise of the following major components (not limited to):</p><br>';
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:60%">PROCESS</th><th style="width:30%">CAPACITY ( M&sup3;/ DAY )</th></tr>';
				var arr=["Rotary Brush Screener", "Bar Screener", "Drum Screener", "Anaerobic Screener", "Anaerobic Equalization", 
						"Anaerobic Neutralization", "Anaerobic System", "Ammonia Striper", "Lifting sump", "Oil & grease trap", 
						"DAF (Dissolved Air Flotation)", "Equalization System", "Neutralization System","Cooling Tower",
						"De-Nitrification System", "Biological Oxidation System", "Circular Clarifier System", "Lamella Settler",
						"DO increase system", "SRS System", "Sand Filter", "Activated Carbon Filter", "Self-Cleaning Filter",
						"Micro Filtration - ASAHI", "Submerged MBR system - KOCH", "Submerged MBR system - OVIVO", 
						"Sulphur Black Removal System", "Sludge Thickener", "Sludge Thickener with mech", 
						"Screw Press", "Belt Press", "Degasser System", "Reverse Osmosis", "Hardness and Silica Removal System", 
						"Chlorination system", "Hardness and Color Removal System", "Reject Reverse Osmosis", "Evaporator", 
						"Agitated Thin film dryer", "Centrifuge", "Crystallizer", "Nano Filtration", "Care system","CTS MBR",
						"CTS Cooling Tower","Rewolutte RO"]
				var system_arr=[];
				for(var i=0;i<arr.length;i++)
				{
					if(asu.includes(arr[i])){
						if(!["Distribution system", "Clarifier Feed Tank", "SRS System", "Self-Cleaning Filter", "Micro Filtration - ASAHI", "Submerged MBR system - KOCH", "Sludge Thickener", "Sludge Thickener with mech"].includes(arr[i])){
							if(arr[i].toUpperCase()=="Submerged MBR system - OVIVO"){arr[i]="SUBMERGED CERAMIC MBR SYSTEM"}
							else if(arr[i].toUpperCase()=="Reject Reverse Osmosis"){arr[i]="BRINEX"}
							else if(arr[i].toUpperCase()=="Circular Clarifier System"){arr[i]="Circular Clarifier"}
								system_arr.push(arr[i].toUpperCase())
						}
					}
				}
				for(var i=0;i<system_arr.length;i++){
					vs+='<tr><td>'+(i+1)+'.</td><td class="left-td">'+system_arr[i]+'</td><td>'+frm.doc.flow+'</td></tr>'
				}
				vs+='</table>*System capacities mentioned above are based on ETP influent flow Rate and the Actual capacities may vary.</center>'
				vs+='<p style="page-break-before:always"></p><br>'
				vs+=''+frm.doc.flowchart+''
				vs+='<p style="page-break-before:always"></p><br>'
				vs+='<center><p style="color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">ETP – STAGEWISE PARAMETERS</p></center><br>';
				var bod_v="NIL"; var bod_v_2="NIL"
				var cod_v="NIL"; var cod_v_2="NIL"
				var tds="NIL"; var tds_2="NIL"
				var tss="NIL"; var tss_2="NIL"
				var tkn="NIL"; var tkn_2="NIL"
				var pva="NIL"; var pva_2="NIL"
				var iron="NIL"; var iron_2="NIL"
				var silica="NIL"; var silica_2="NIL"
				var hardness="NIL"; var hardness_2="NIL"
				var alkali="NIL"; var alkali_2="NIL"
				var temperature="NIL"; var temperature_2="NIL"
				var oil_grease="NIL"; var oil_grease_2="NIL"
				var sulphate="NIL"; var sulphate_2="NIL"
				var chloride="NIL"; var chloride_2="NIL"
		
				if((asu.includes("Biological Oxidation System") && asu.includes("Circular Clarifier System") && !asu.includes("Reverse Osmosis")) || ((asu.includes("Micro Filtration - ASAHI") || asu.includes("Submerged MBR system - KOCH") || asu.includes("Submerged MBR system - OVIVO")) && !asu.includes("Reverse Osmosis")))
				{
					if(frm.doc.bod_v!="NIL"){bod_v = '< '+frm.doc.bod_v*0.1}
					if(frm.doc.cod_v!="NIL"){cod_v = '< '+frm.doc.cod_v*0.1}
					if(frm.doc.tdsmgl!="NIL"){tds = "Same as Inlet"}
					if(frm.doc.tss!="NIL"){tss = '< 50'}
					if(frm.doc.tkn!="NIL"){tkn = '< 5'}
					if(frm.doc.pva!="NIL"){pva = "Same as Inlet"}
					if(frm.doc.silica!="NIL"){silica = "Same as Inlet"}
					if(frm.doc.hardness!="NIL"){hardness = "Same as Inlet"}
					if(frm.doc.alkali!="NIL"){alkali = "Same as Inlet"}
					if(frm.doc.temperature!="NIL"){temperature = '30 - 35'}
					if(frm.doc.oil_grease!="NIL"){oil_grease = "Same as Inlet"}
					else if(frm.doc.oil_grease<10){oil_grease="< 5"}
					if(frm.doc.sulphate!="NIL"){sulphate = "Same as Inlet"}
					if(frm.doc.chloride!="NIL"){chloride = "Same as Inlet"}
					vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:20%">PARAMETER</th><th style="width:20%">UNIT</th><th style="width:20%">'+frm.doc.abbr_inlet+' Inlet</th><th style="width:20%">TREATED WATER</th></tr>';
					vs+='<tr><td>1. </td><td class="left-td">pH</td><td>--</td><td>8 - 9</td><td>7 - 8</td></tr>'
					vs+='<tr><td>2. </td><td class="left-td">BOD</td><td>mg/l</td><td>'+frm.doc.bod_v+'</td><td>< '+bod_v+'</td></tr>'
					vs+='<tr><td>3. </td><td class="left-td">COD</td><td>mg/l</td><td>'+frm.doc.cod_v+'</td><td>< '+cod_v+'</td></tr>'
					vs+='<tr><td>4. </td><td class="left-td">TDS</td><td>mg/l</td><td>'+frm.doc.tdsmgl+'</td><td>'+tds+'</td></tr>'
					vs+='<tr><td>5. </td><td class="left-td">TSS</td><td>mg/l</td><td>'+frm.doc.tss+'</td><td>'+tss+'</td></tr>'
					vs+='<tr><td>6. </td><td class="left-td">TKN</td><td>mg/l</td><td>'+frm.doc.tkn+'</td><td>'+tkn+'</td></tr>'
					vs+='<tr><td>7. </td><td class="left-td">PVA</td><td>mg/l</td><td>'+frm.doc.pva+'</td><td>'+pva+'</td></tr>'
					vs+='<tr><td>7. </td><td class="left-td">IRON</td><td>mg/l</td><td>'+frm.doc.iron+'</td><td>'+iron+'</td></tr>'
					vs+='<tr><td>9. </td><td class="left-td">SILICA</td><td>mg/l</td><td>'+frm.doc.silica+'</td><td>'+silica+'</td></tr>'
					vs+='<tr><td>10. </td><td class="left-td">HARDNESS</td><td>mg/l</td><td>'+frm.doc.hardness+'</td><td>'+hardness+'</td></tr>'
					vs+='<tr><td>11. </td><td class="left-td">ALKALINITY</td><td>mg/l</td><td>'+frm.doc.alkali+'</td><td>'+alkali+'</td></tr>'
					vs+='<tr><td>12. </td><td class="left-td">TEMPERATURE</td><td>mg/l</td><td>'+frm.doc.temperature+'</td><td>'+temperature+'</td></tr>'
					vs+='<tr><td>13. </td><td class="left-td">OIL & GREASE</td><td>mg/l</td><td>'+frm.doc.oil_grease+'</td><td>'+oil_grease+'</td></tr>'
					vs+='<tr><td>14. </td><td class="left-td">SULPHATE</td><td>mg/l</td><td>'+frm.doc.sulphate+'</td><td>'+sulphate+'</td></tr>'
					vs+='<tr><td>15. </td><td class="left-td">CHLORIDE</td><td>mg/l</td><td>'+frm.doc.chloride+'</td><td>'+chloride+'</td></tr>'
					vs+='</table><br>BDL – below detectable limit, NA – not applicable; Values are system generated which may vary with variation in inlet & on operational basis</center>'											
				}
				else if(asu.includes("Reverse Osmosis"))
				{
					if(asu.includes("Reject Reverse Osmosis") || asu.includes("Brinex"))
					{
						vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:20%">PARAMETER</th><th style="width:10%">UNIT</th><th style="width:20%">'+frm.doc.abbr_inlet+'</th><th>REWOLUTTE RO PERMEATE</th><th style="width:20%">REWOLUTTE RO REJECT</th></tr>';
						vs+='<tr><td>1. </td><td class="left-td">pH</td><td>--</td><td>8 - 9</td><td></td><td></td></tr>'
						vs+='<tr><td>2. </td><td class="left-td">BOD</td><td>mg/l</td><td>'+frm.doc.bod_v+'</td><td></td><td></td></tr>'
						vs+='<tr><td>3. </td><td class="left-td">COD</td><td>mg/l</td><td>'+frm.doc.cod_v+'</td><td></td><td></td></tr>'
						vs+='<tr><td>4. </td><td class="left-td">TDS</td><td>mg/l</td><td>'+frm.doc.tdsmgl+'</td><td></td><td></td></tr>'
						vs+='<tr><td>5. </td><td class="left-td">TSS</td><td>mg/l</td><td>'+frm.doc.tss+'</td><td></td><td></td></tr>'
						vs+='<tr><td>6. </td><td class="left-td">TKN</td><td>mg/l</td><td>'+frm.doc.tkn+'</td><td></td><td></td></tr>'
						vs+='<tr><td>7. </td><td class="left-td">PVA</td><td>mg/l</td><td>'+frm.doc.pva+'</td><td></td><td></td></tr>'
						vs+='<tr><td>8. </td><td class="left-td">IRON</td><td>mg/l</td><td>'+frm.doc.iron+'</td><td></td><td></td></tr>'
						vs+='<tr><td>9. </td><td class="left-td">SILICA</td><td>mg/l</td><td>'+frm.doc.silica+'</td><td></td><td></td></tr>'
						vs+='<tr><td>10. </td><td class="left-td">HARDNESS</td><td>mg/l</td><td>'+frm.doc.hardness+'</td><td></td><td></td></tr>'
						vs+='<tr><td>11. </td><td class="left-td">ALKALINITY</td><td>mg/l</td><td>'+frm.doc.alkali+'</td><td></td><td></td></tr>'
						vs+='<tr><td>12. </td><td class="left-td">TEMPERATURE</td><td>mg/l</td><td>'+frm.doc.temperature+'</td><td></td><td></td></tr>'
						vs+='<tr><td>13. </td><td class="left-td">OIL & GREASE</td><td>mg/l</td><td>'+frm.doc.oil_grease+'</td><td></td><td></td></tr>'
						if(asu.includes("Biological Oxidation System") || asu.includes("Circular Clarifier System")){
							vs+='<tr><td>14. </td><td class="left-td">SULPHATE</td><td>mg/l</td><td>'+frm.doc.sulphate+'</td><td></td><td></td></tr>'
							vs+='<tr><td>15. </td><td class="left-td">CHLORIDE</td><td>mg/l</td><td>'+frm.doc.chloride+'</td><td></td><td></td></tr>'
						}
						vs+='</table></br>BDL – below detectable limit, NA – not applicable; Values are system generated which may vary with variation in inlet & on operational basis</center>'
					}
					else{
						if(frm.doc.bod_v!="NIL"){bod_v = 'BDL'; bod_v_2='NA'}
						if(frm.doc.cod_v!="NIL"){cod_v = 'BDL'; cod_v_2=(frm.doc.cod_v * 0.1)/ss_ar[0].proposed_recovery}
						if(frm.doc.tdsmgl!="NIL"){
							tds = frm.doc.tdsmgl*0.06; 
							var tds_2_cal=Math.ceil(((((frm.doc.flow*(frm.doc.tdsmgl))-(frm.doc.flow*(ss_ar[0].proposed_recovery/100)*tds))/(frm.doc.flow-(frm.doc.flow*(ss_ar[0].proposed_recovery/100))))+1000)/500)*500
							tds_2=(tds_2_cal-1000)+' - '+tds_2_cal
						}
						if(frm.doc.tss!="NIL"){tss = 'BDL'; tss_2='NA'}
						if(frm.doc.tkn!="NIL"){tkn = 'BDL'; tkn_2='NA'}
						if(frm.doc.pva!="NIL"){pva = 'BDL'; pva_2=''}
						if(frm.doc.silica!="NIL"){silica = 'BDL'; silica_2=frm.doc.silica/1-(ss_ar[0].proposed_recovery/100)}
						if(frm.doc.hardness!="NIL"){
							hardness = "< 2";
							var hardness_2_cal = Math.ceil((frm.doc.hardness/1-(ss_ar[0].proposed_recovery/100))/200)*200
							hardness_2=(hardness_2_cal-200)+' - '+hardness_2_cal
						}
						if(frm.doc.alkali!="NIL"){
							if(selected_system_array.includes("Degasser System")){
								alkali='< '+(frm.doc.alkali*0.15*0.33)
								var alk_cal = Math.ceil(((frm.doc.alkali*0.15*0.33)/ss_ar[0].proposed_recovery)/200)*200
								alkali_2=(alk_cal-200)+' - '+alk_cal
							}
							else{
								alkali=frm.doc.alkali*0.1
								var alk_cal = Math.ceil(((frm.doc.alkali*0.1)/ss_ar[0].proposed_recovery)/200)*200
								alkali_2=(alk_cal-200)+' - '+alk_cal
							}
						}
						if(frm.doc.temperature!="NIL"){temperature = '30 - 35'; temperature_2='30 - 35'}
						if(frm.doc.oil_grease!="NIL"){oil_grease = "BDL"; oil_grease_2='NA'}
						if(frm.doc.sulphate!="NIL"){
							sulphate = frm.doc.sulphate * 0.015;
							var sulphate_cal = Math.ceil(((frm.doc.sulphate/1-(ss_ar[0].proposed_recovery/100))+500)/500)*500
							sulphate_2=(sulphate_cal-500)+' - '+sulphate_cal
						}
						if(frm.doc.chloride!="NIL"){
							chloride = frm.doc.chloride * 0.015;
							var chloride_cal = Math.ceil(((frm.doc.chloride/1-(ss_ar[0].proposed_recovery/100))+500)/500)*500
							chloride_2=(chloride_cal-500)+' - '+chloride_cal
						}
						vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:20%">PARAMETER</th><th style="width:10%">UNIT</th><th style="width:20%">'+frm.doc.abbr_inlet+'</th><th>RO PERMEATE</th><th style="width:20%">RO REJECT</th></tr>';
						vs+='<tr><td>1. </td><td class="left-td">pH</td><td>--</td><td>8 - 9</td><td>7 - 8</td><td>7 - 8</td></tr>'
						vs+='<tr><td>2. </td><td class="left-td">BOD</td><td>mg/l</td><td>'+frm.doc.bod_v+'</td><td>'+bod_v+'</td><td>'+bod_v_2+'</td></tr>'
						vs+='<tr><td>3. </td><td class="left-td">COD</td><td>mg/l</td><td>'+frm.doc.cod_v+'</td><td>'+cod_v+'</td><td>'+cod_v_2+'</td></tr>'
						vs+='<tr><td>4. </td><td class="left-td">TDS</td><td>mg/l</td><td>'+frm.doc.tdsmgl+'</td><td>'+tds+'</td><td>'+tds_2+'</td></tr>'
						vs+='<tr><td>5. </td><td class="left-td">TSS</td><td>mg/l</td><td>'+frm.doc.tss+'</td><td>'+tss+'</td><td>'+tss_2+'</td></tr>'
						vs+='<tr><td>6. </td><td class="left-td">TKN</td><td>mg/l</td><td>'+frm.doc.tkn+'</td><td>'+tkn+'</td><td>'+tkn_2+'</td></tr>'
						vs+='<tr><td>7. </td><td class="left-td">PVA</td><td>mg/l</td><td>'+frm.doc.pva+'</td><td>'+pva+'</td><td>'+pva_2+'</td></tr>'
						vs+='<tr><td>8. </td><td class="left-td">IRON</td><td>mg/l</td><td>'+frm.doc.iron+'</td><td>'+iron+'</td><td>'+iron_2+'</td></tr>'
						vs+='<tr><td>9. </td><td class="left-td">SILICA</td><td>mg/l</td><td>'+frm.doc.silica+'</td><td>'+silica+'</td><td>'+silica_2+'</td></tr>'
						vs+='<tr><td>10. </td><td class="left-td">HARDNESS</td><td>mg/l</td><td>'+frm.doc.hardness+'</td><td>'+hardness+'</td><td>'+hardness_2+'</td></tr>'
						vs+='<tr><td>11. </td><td class="left-td">ALKALINITY</td><td>mg/l</td><td>'+frm.doc.alkali+'</td><td>'+alkali+'</td><td>'+alkali_2+'</td></tr>'
						vs+='<tr><td>12. </td><td class="left-td">TEMPERATURE</td><td>mg/l</td><td>'+frm.doc.temperature+'</td><td>'+temperature+'</td><td>'+temperature_2+'</td></tr>'
						vs+='<tr><td>13. </td><td class="left-td">OIL & GREASE</td><td>mg/l</td><td>'+frm.doc.oil_grease+'</td><td>'+oil_grease+'</td><td>'+oil_grease_2+'</td></tr>'
						if(asu.includes("Biological Oxidation System") || asu.includes("Circular Clarifier System")){
							vs+='<tr><td>14. </td><td class="left-td">SULPHATE</td><td>mg/l</td><td>'+frm.doc.sulphate+'</td><td>'+sulphate+'</td><td>'+sulphate_2+'</td></tr>'
							vs+='<tr><td>15. </td><td class="left-td">CHLORIDE</td><td>mg/l</td><td>'+frm.doc.chloride+'</td><td>'+chloride+'</td><td>'+chloride_2+'</td></tr>'
						}
						vs+='</table></br>BDL – below detectable limit, NA – not applicable; Values are system generated which may vary with variation in inlet & on operational basis</center>'
					}
				}
				else if(asu.includes("Reject Reverse Osmosis") || asu.includes("Brinex"))
				{
					vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:20%">PARAMETER</th><th style="width:10%">UNIT</th><th style="width:20%">'+frm.doc.abbr_inlet+'</th><th>RRO PERMEATE</th><th style="width:20%">RRO REJECT</th></tr>';
					vs+='<tr><td>1. </td><td class="left-td">pH</td><td>--</td><td>8 - 9</td><td></td><td></td></tr>'
					vs+='<tr><td>2. </td><td class="left-td">BOD</td><td>mg/l</td><td>'+frm.doc.bod_v+'</td><td></td><td></td></tr>'
					vs+='<tr><td>3. </td><td class="left-td">COD</td><td>mg/l</td><td>'+frm.doc.cod_v+'</td><td></td><td></td></tr>'
					vs+='<tr><td>4. </td><td class="left-td">TDS</td><td>mg/l</td><td>'+frm.doc.tdsmgl+'</td><td></td><td></td></tr>'
					vs+='<tr><td>5. </td><td class="left-td">TSS</td><td>mg/l</td><td>'+frm.doc.tss+'</td><td></td><td></td></tr>'
					vs+='<tr><td>6. </td><td class="left-td">TKN</td><td>mg/l</td><td>'+frm.doc.tkn+'</td><td></td><td></td></tr>'
					vs+='<tr><td>7. </td><td class="left-td">PVA</td><td>mg/l</td><td>'+frm.doc.pva+'</td><td></td><td></td></tr>'
					vs+='<tr><td>8. </td><td class="left-td">IRON</td><td>mg/l</td><td>'+frm.doc.iron+'</td><td></td><td></td></tr>'
					vs+='<tr><td>9. </td><td class="left-td">SILICA</td><td>mg/l</td><td>'+frm.doc.silica+'</td><td></td><td></td></tr>'
					vs+='<tr><td>10. </td><td class="left-td">HARDNESS</td><td>mg/l</td><td>'+frm.doc.hardness+'</td><td></td><td></td></tr>'
					vs+='<tr><td>11. </td><td class="left-td">ALKALINITY</td><td>mg/l</td><td>'+frm.doc.alkali+'</td><td></td><td></td></tr>'
					vs+='<tr><td>12. </td><td class="left-td">TEMPERATURE</td><td>mg/l</td><td>'+frm.doc.temperature+'</td><td></td><td></td></tr>'
					vs+='<tr><td>13. </td><td class="left-td">OIL & GREASE</td><td>mg/l</td><td>'+frm.doc.oil_grease+'</td><td></td><td></td></tr>'
					if(asu.includes("Biological Oxidation System") || asu.includes("Circular Clarifier System")){
						vs+='<tr><td>14. </td><td class="left-td">SULPHATE</td><td>mg/l</td><td>'+frm.doc.sulphate+'</td><td></td><td></td></tr>'
						vs+='<tr><td>15. </td><td class="left-td">CHLORIDE</td><td>mg/l</td><td>'+frm.doc.chloride+'</td><td></td><td></td></tr>'
					}
					vs+='</table></br>BDL – below detectable limit, NA – not applicable; Values are system generated which may vary with variation in inlet & on operational basis</center>'
				}
				else if(asu.includes("Rewolutte RO"))
				{
					vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:20%">PARAMETER</th><th style="width:10%">UNIT</th><th style="width:20%">'+frm.doc.abbr_inlet+'</th><th>PERMEATE</th><th style="width:20%">REJECT</th></tr>';
					vs+='<tr><td>1. </td><td class="left-td">pH</td><td>--</td><td>8 - 9</td><td></td><td></td></tr>'
					vs+='<tr><td>2. </td><td class="left-td">BOD</td><td>mg/l</td><td>'+frm.doc.bod_v+'</td><td></td><td></td></tr>'
					vs+='<tr><td>3. </td><td class="left-td">COD</td><td>mg/l</td><td>'+frm.doc.cod_v+'</td><td></td><td></td></tr>'
					vs+='<tr><td>4. </td><td class="left-td">TDS</td><td>mg/l</td><td>'+frm.doc.tdsmgl+'</td><td></td><td></td></tr>'
					vs+='<tr><td>5. </td><td class="left-td">TSS</td><td>mg/l</td><td>'+frm.doc.tss+'</td><td></td><td></td></tr>'
					vs+='<tr><td>6. </td><td class="left-td">TKN</td><td>mg/l</td><td>'+frm.doc.tkn+'</td><td></td><td></td></tr>'
					vs+='<tr><td>7. </td><td class="left-td">PVA</td><td>mg/l</td><td>'+frm.doc.pva+'</td><td></td><td></td></tr>'
					vs+='<tr><td>8. </td><td class="left-td">IRON</td><td>mg/l</td><td>'+frm.doc.iron+'</td><td></td><td></td></tr>'
					vs+='<tr><td>9. </td><td class="left-td">SILICA</td><td>mg/l</td><td>'+frm.doc.silica+'</td><td></td><td></td></tr>'
					vs+='<tr><td>10. </td><td class="left-td">HARDNESS</td><td>mg/l</td><td>'+frm.doc.hardness+'</td><td></td><td></td></tr>'
					vs+='<tr><td>11. </td><td class="left-td">ALKALINITY</td><td>mg/l</td><td>'+frm.doc.alkali+'</td><td></td><td></td></tr>'
					vs+='<tr><td>12. </td><td class="left-td">TEMPERATURE</td><td>mg/l</td><td>'+frm.doc.temperature+'</td><td></td><td></td></tr>'
					vs+='<tr><td>13. </td><td class="left-td">OIL & GREASE</td><td>mg/l</td><td>'+frm.doc.oil_grease+'</td><td></td><td></td></tr>'
					if(asu.includes("Biological Oxidation System") || asu.includes("Circular Clarifier System")){
						vs+='<tr><td>14. </td><td class="left-td">SULPHATE</td><td>mg/l</td><td>'+frm.doc.sulphate+'</td><td></td><td></td></tr>'
						vs+='<tr><td>15. </td><td class="left-td">CHLORIDE</td><td>mg/l</td><td>'+frm.doc.chloride+'</td><td></td><td></td></tr>'
					}
					vs+='</table></br>BDL – below detectable limit, NA – not applicable; Values are system generated which may vary with variation in inlet & on operational basis</center>'
				}
				
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">2.1. EXPECTED TREATED WATER QUALITY</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The following performance parameters are expected under standard operating conditions after equipment start-up based on the data and assumptions listed above and in Appendix, Warranties. In case of conflicting numbers, the ones listed under Appendix take precedence:</p><br>';
				if(asu.includes("Reverse Osmosis")){
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="text-align:center;width:40%">PARAMETER</th><th style="text-align:center;width:40%">TREATED WATER QUALITY</th><th style="text-align:center;width:30%">UNIT</th></tr>';
				vs+='<tr><td>PERMEATE WATER TDS</td><td>150-350</td><td>mg/L</td></tr>'
				}
				if(!asutype.includes("Filtration")){
					if(asu.includes("Biological Oxidation System") && asu.includes("Circular Clarifier System")){
						vs+='<tr><td>PERMEATE WATER COD</td><td>< '+(frm.doc.cod*0.1)+'</td><td>mg/L</td></tr>'
						vs+='<tr><td>PERMEATE WATER TSS</td><td>< 50</td><td>mg/L</td></tr>'				
					}
				}
				vs+='</table></center>'
				vs+='<p style="page-break-before:always"></p><br>'
				vs+='<p style="font-family:Roboto;font-size: 18px;"><b>Notes:</b></p><br>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>All influent quality parameters are based on monthly average values of a minimum of four (4) 24-hour composite samples collected at regular intervals over a month, with testing performed to applicable industry-approved standards.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>The above recovery water quality expectation is based on WTT supplying the system and scope Equipment as per the scope of supply table described in section 3 below. </li></ul>';
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">3. Scope Of Supply - Equipment, Engineering & Services</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The following table shows the list of Equipment for the proposed plant and the scope of supply.</p><br>';
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:90%;">EQUIPMENT & SCOPE DETAILS</th></tr>';
				vs+='<tr><td colspan="3" style="color:#012673"><b>BIOLOGICAL SYSTEM</b></td></tr>'
				
				var arr=["Rotary Brush Screener", "Bar Screener", "Drum Screener", "Anaerobic Screener", "Anaerobic Equalization", 
						"Anaerobic Neutralization", "Anaerobic System", "Ammonia Striper", "Lifting sump", "Oil & grease trap", 
						"DAF (Dissolved Air Flotation)", "Equalization System", "Neutralization System","Cooling Tower",
						"De-Nitrification System", "Biological Oxidation System", "Circular Clarifier System", "Lamella Settler",
						"DO increase system", "SRS System", "Sand Filter", "Activated Carbon Filter", "Self-Cleaning Filter",
						"Micro Filtration - ASAHI", "Submerged MBR system - KOCH", "Submerged MBR system - OVIVO", 
						"Sulphur Black Removal System", "Sludge Thickener", "Sludge Thickener with mech", 
						"Screw Press", "Belt Press", "Degasser System", "Reverse Osmosis", "Hardness and Silica Removal System", 
						"Chlorination system", "Hardness and Color Removal System", "Reject Reverse Osmosis", "Evaporator", 
						"Agitated Thin film dryer", "Centrifuge", "Crystallizer", "Nano Filtration", "Care system","CTS MBR",
						"CTS Cooling Tower","Rewolutte RO"]

				var arr2=[];
				var seperate_blower="No";
				frappe.db.get_value("Startup Sheet",frm.doc.project_startup_sheet,"seperate_blower_for_equalization_tank")
				    .then(r => {
				    	if(r.message.seperate_blower_for_equalization_tank==1){
				        	seperate_blower = "Yes";
				    	}
				    })
				$.each(frm.doc.selected_process_system || [], function(i, v) {
					if(v.selected_type=="Pre Treatment"){
						arr2.push(v.selected_system_name)
					}
				});
				var array_for_html =[]
				for(var j=0;j<arr.length;j++){
					if(arr2.includes(arr[j]))
					{
						// CODING FOR SYSTEM AMENDMENT FOR BIOLOGICAL SYSTEM SYSTEM TRABLE INPUTS BY HARISH
						var sys_name = arr[j];
						if(arr[j]=="Lifting sump") { arr[j]="Lifting Sump Pump" }
						else if(arr[j]=="Equalization System") { arr[j]="EQUALIZATION TANK DIFFUSER GRID"; }
						else if(arr[j]=="Neutralization System") { arr[j]="NEUTRALIZATION TO BIOLOGICAL FEED PUMP" }
						else if(arr[j]=="Biological Oxidation System") { arr[j]="BIOLOGICAL OXIDATION SYSTEM DIFFUSER GRID" }
						else if(arr[j]=="Circular Clarifier System") { arr[j]="CIRCULAR CLARIFIER MECHANISM" }
						else if(arr[j]=="Sludge Thickener") { arr[j]="PIPING FOR SLUDGE THICKENER" }
						else if(arr[j]=="Screw Press") { arr[j]="SCREW PRESS SYSTEM" }
						else if(arr[j]=="Belt Press") { arr[j]="BELT PRESS SYSTEM" }
						else if(arr[j]=="SRS System") { arr[j]="SLUDGE RECIRCULATION PUMP" }
						else if(arr[j]=="DAF (Dissolved Air Flotation)") { arr[j]="DISSLOVED AIR FLOTATION (DAF) MECHANISM" }
						else if(arr[j]=="Drum Screener") { arr[j]="DRUM SCREENER SYSTEM" }

						array_for_html.push(arr[j].toUpperCase())

						if(arr[j]=="NEUTRALIZATION TO BIOLOGICAL FEED PUMP"){array_for_html.push("pH NEUTRALIZING SYSTEM WITH SENSOR")}
						else if(arr[j]=="EQUALIZATION TANK DIFFUSER GRID"){
							if(seperate_blower=="Yes"){array_for_html.push("BLOWER FOR EQUALIZATION TANK")}
						}
						else if(arr[j]=="BIOLOGICAL OXIDATION SYSTEM DIFFUSER GRID"){
							if(seperate_blower=="Yes"){array_for_html.push("BLOWER FOR BIOLOGICAL OXIDATION SYSTEM")}
							else if(seperate_blower=="No"){array_for_html.push("BLOWER FOR EQUALIZATION & BIOLOGICAL OXIDATION SYSTEM ")}
							array_for_html.push("DO SENSOR AUTOMATION FOR BIOLOGICAL OXIDATION SYSTEM")
						}
						else if(arr[j]=="Sludge Thickener with mech"){array_for_html.push("PIPING FOR SLUDGE THICKENER")}
						else if(arr[j]=="NEUTRALIZATION TO BIOLOGICAL FEED PUMP" || arr[j]=="SCREW PRESS SYSTEM" || arr[j]=="BELT PRESS SYSTEM"){
							if(!array_for_html.includes("DOSING PUMP FOR PROPOSED SYSTEM")){array_for_html.push("DOSING PUMP FOR PROPOSED SYSTEM")}
						}
						else if(arr[j]=="DISSLOVED AIR FLOTATION (DAF) MECHANISM"){
							array_for_html.push("BUBBLE GENERATION PUMP FOR DAF SYSTEM")
							array_for_html.push("SLUDGE PUMP FOR DAF SYSTEM")
						}
						else if(arr[j]=="De-Nitrification System"){
							array_for_html.push("FLOW MIXER FOR DE-NITRIFICATION PUMP ")
							array_for_html.push("DE-NITRIFICATION PUMP")
						}
					}
				}
				array_for_html.push("ALL OTHER RELATED INSTRUMENTS, ELECTROMAGNETIC FLOW METER & VALVES REQUIRED")
				array_for_html.push("PIPING IN SS, CPVC, UPVC AND ITS ASSOCIATED ITEMS")
				var ii=0;
				for(var jj=0;jj<array_for_html.length;jj++){
					ii=ii+1;
					vs+='<tr><td>'+ii+'. </td><td class="left-td">'+array_for_html[jj]+' - '+frm.doc.scope+'</td></tr>'
				}
				vs+='</table></center>'
				if(asu.includes('Micro Filtration - ASAHI'))
				{
					vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:90%">EQUIPMENT & SCOPE DETAILS</th></tr>';
					vs+='<tr><td colspan="3" style="color:#012673"><b>MICRO/ULTRA FILTRATION SYSTEM</b></td></tr>'
					vs+='<tr><td>1. </td><td class="left-td">FILTRATION FEED PUMP FOR PROPOSED  SYSTEM - '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>2. </td><td class="left-td">BACKWASH PUMP FOR PROPOSED SYSTEM  - '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>3. </td><td class="left-td">CIP PUMP FOR PROPOSED SYSTEM - '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>4. </td><td class="left-td">PRE-FILTER FOR PROPOSED SYSTEM</td></tr>'
					vs+='<tr><td>5. </td><td class="left-td">MF/UF MODULES – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>6. </td><td class="left-td">CIP TANK FOR FILTRATION SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>7. </td><td class="left-td">ALL OTHER RELATED INSTRUMENTS, ELECTROMAGNETIC FLOW METER, VALVES REQUIRED – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>8. </td><td class="left-td">PIPING IN SS, UPVC AND ITS ASSOCIATED ITEMS – '+frm.doc.scope+'</td></tr>'
					vs+='</table></center>'
				}
				if(asu.includes('Submerged MBR system - KOCH'))
				{
					vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:90%">EQUIPMENT & SCOPE DETAILS</th></tr>';
					vs+='<tr><td colspan="3" style="color:#012673"><b>SUBMERGED MBR SYSTEM - KOCH</b></td></tr>'
					vs+='<tr><td>1. </td><td class="left-td">MBR MODULES FOR PROPOSED SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>2. </td><td class="left-td">FEED PUMP FOR PROPOSED SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>3. </td><td class="left-td">PERMEATE / BACKWASH / CIP PUMP – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>4. </td><td class="left-td">CIRCULATION PUMP – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>5. </td><td class="left-td">SLUDGE PUMP – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>6. </td><td class="left-td">DOSING PUMPS AND CHEMICAL DOSING TANKS FOR MBR SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>7. </td><td class="left-td">BLOWER FOR MBR SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>8. </td><td class="left-td">ALL OTHER RELATED INSTRUMENTS, ELECTROMAGNETIC FLOW METER, VALVES REQUIRED – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>9. </td><td class="left-td">PIPING IN SS, UPVC AND ITS ASSOCIATED ITEMS – '+frm.doc.scope+'</td></tr>'
					vs+='</table></center>'
				}
				if(asu.includes('Submerged MBR system - OVIVO'))
				{
					vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:90%">EQUIPMENT & SCOPE DETAILS</th></tr>';
					vs+='<tr><td colspan="3" style="color:#012673"><b>SUBMERGED MBR SYSTEM - OVIVO</b></td></tr>'
					vs+='<tr><td>1. </td><td class="left-td">MBR MODULES FOR PROPOSED SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>2. </td><td class="left-td">FEED PUMP FOR PROPOSED SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>3. </td><td class="left-td">PERMEATE PUMP – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>4. </td><td class="left-td">BACKWASH PUMP – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>5. </td><td class="left-td">SPRINKLER PUMP – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>6. </td><td class="left-td">SLUDGE PUMP – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>7. </td><td class="left-td">AERATION LINE FROM BIOLOGICAL BLOWER FOR MBR SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>8. </td><td class="left-td">DOSING PUMPS AND CHEMICAL DOSING TANKS FOR MBR SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>9. </td><td class="left-td">ALL OTHER RELATED INSTRUMENTS, ELECTROMAGNETIC FLOW METER, VALVES REQUIRED – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>10. </td><td class="left-td">PIPING IN SS, UPVC AND ITS ASSOCIATED ITEMS – '+frm.doc.scope+'</td></tr>'
					vs+='</table></center>'
				}
				if(asu.includes('Degasser System'))
				{
					vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:90%">EQUIPMENT & SCOPE DETAILS</th></tr>';
					vs+='<tr><td colspan="3" style="color:#012673"><b>DEGASSER TOWER</b></td></tr>'
					vs+='<tr><td>1. </td><td class="left-td">DEGASSER TOWER VESSEL – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>2. </td><td class="left-td">DEGASSER TOWER MEDIA – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>3. </td><td class="left-td">DOSING PUMP – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>4. </td><td class="left-td">BLOWER FOR DEGASSER TOWER – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>5. </td><td class="left-td">pH SENSOR FOR DEGASSER TOWER – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>6. </td><td class="left-td">ALL OTHER RELATED INSTRUMENTS & VALVES REQUIRED – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>7. </td><td class="left-td">PIPING IN UPVC AND ITS ASSOCIATED ITEMS – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>8. </td><td class="left-td">SUPPORTS FOR FEED PIPE AND BLOWER FAN – '+frm.doc.scope+'</td></tr>' 
					vs+='</table></center>'
				}
				if(asu.includes('Reverse Osmosis'))
				{
					vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:90%">EQUIPMENT & SCOPE DETAILS</th></tr>';
					vs+='<tr><td colspan="3" style="color:#012673"><b>REVERSE OSMOSIS SYSTEM</b></td></tr>'
					vs+='<tr><td>1. </td><td class="left-td">FEED PUMPS FOR REVERSE OSMOSIS SYSTEM – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>2. </td><td class="left-td">DOSING PUMPS AND CHEMICAL DOSING TANKS FOR REVERSE OSMOSIS SYSTEM – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>3. </td><td class="left-td">PRE-FILTER FOR REVERSE OSMOSIS SYSTEM – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>4. </td><td class="left-td">PRESSURE VESSELS & MEMBRANES FOR REVERSE OSMOSIS SYSTEM – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>5. </td><td class="left-td">HIGH PRESSURE PUMP FOR REVERSE OSMOSIS SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>6. </td><td class="left-td">BOOSTER PUMPS FOR REVERSE OSMOSIS SYSTEM – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>7. </td><td class="left-td">CIP PUMP FOR REVERSE OSMOSIS SYSTEM – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>8. </td><td class="left-td">CIP TANK FOR REVERSE OSMOSIS SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>9. </td><td class="left-td">pH SENSOR FOR REVERSE OSMOSIS SYSTEM – '+frm.doc.scope+'</td></tr>'
					vs+='<tr><td>10. </td><td class="left-td">ALL OTHER RELATED INSTRUMENTS, ELECTROMAGNETIC FLOW METER, VALVES REQUIRED – '+frm.doc.scope+'</td></tr>' 
					vs+='<tr><td>11. </td><td class="left-td">PIPING IN SS, UPVC AND ITS ASSOCIATED ITEMS – '+frm.doc.scope+'</td></tr>'
					vs+='</table></center>'
				}
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:90%">EQUIPMENT & SCOPE DETAILS</th></tr>';
				vs+='<tr><td colspan="3" style="color:#012673"><b>ELECTRICAL PANEL</b></td></tr>'
				vs+='<tr><td>1. </td><td class="left-td">ELECTRICAL CONTROL PANEL FOR PROPOSED SYSTEM WITH STANDARD AUTOMATION - '+frm.doc.scope+'</td></tr>' 
				vs+='<tr><td>2. </td><td class="left-td">POWER CABLE AND CONTROL CABLE WITHIN THE ELECTRICAL PANEL - '+frm.doc.scope+'</td></tr>' 
				vs+='<tr><td>3. </td><td class="left-td">POWER CABLE AND CONTROL CABLE FROM ELECTRICAL PANEL TO PROPOSED EQUIPMENT - '+frm.doc.scope+'</td></tr>' 
				vs+='</table></center>'

				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:90%">EQUIPMENT & SCOPE DETAILS</th></tr>';
				vs+='<tr><td colspan="3" style="color:#012673"><b>DRAWING</b></td></tr>'
				vs+='<tr><td>1. </td><td class="left-td">GENERAL LAYOUT & CIVIL DETAILED DRAWING FOR PROPOSED SYSTEMS -  SUPPLY</td></tr>'
				vs+='</table></center>'

				var epq=[]
				if(asu.includes('Rotary Brush Screener') || asu.includes('Bar Screener') || asu.includes('Drum Screener'))
				{
					epq.push("TRANSFER OF INFLUENT UP TO PROPOSED SCREENER SYSTEMS – SUPPLY & INSTALLATION")
				}
				if(asu.includes('Biological Oxidation System'))
				{
					epq.push("BULK CHEMICAL STORAGE TANK FOR BIOLOGICAL SYSTEM - SUPPLY & INSTALLATION")
				}
				if(asu.includes('Degasser System'))
				{
					epq.push("BULK CHEMICAL STORAGE TANK FOR DEGASSER TOWER SYSTEM - SUPPLY & INSTALLATION")
				}
				if(asu.includes('Micro Filtration - ASAHI'))
				{
					epq.push("COMPRESSED AIR FOR PROPOSED SYSTEM – SUPPLY & INSTALLATION ")
				}
				if(asu.includes('Submerged MBR system - KOCH') || asu.includes("Submerged MBR system - OVIVO")){}
				{
					epq.push("BACKWASH TANK (RCC) FOR PROPOSED SUBMERGED MBR SYSTEM – SUPPLY & INSTALLATION ")
				}
				if(asu.includes('Reverse Osmosis'))
				{
					epq.push("BULK CHEMICAL STORAGE TANK FOR REVERSE OSMOSIS SYSTEM - SUPPLY & INSTALLATION")
					epq.push("PERMEATE & REJECT WATER TRANSFER REVERSE OSMOSIS SYSTEM – SUPPLY & INSTALLATION")
				}
				if(asutype.includes('Filtration'))
				{
					epq.push("TRANSFER OF CIP/CLEANING WATER OF PROPOSED SYSTEMS – SUPPLY & INSTALLATION")
				}
				epq.push("ALL UNDERGROUND PIPING, PUDDLE FLANGES & PIPING FOR ELECTRICAL CABLE DURING CIVIL WORKS  - SUPPLY & INSTALLATION")
				epq.push("INCOMER CABLE AND ITS CONNECTIONS WITH WTT SUPPLIED ELECTRICAL PANEL - SUPPLY & INSTALLATION")
				epq.push("EARTHING  FOR ALL INDIVIDUAL EQUIPMENT & PANEL - SUPPLY & INSTALLATION")
				epq.push("INPUT POWER TO INDIVIDUAL WTT SUPPLIED ELECTRICAL PANEL - SUPPLY & INSTALLATION")
				epq.push("STRUCTURAL DRAWING FOR PROPOSED SYSTEM - SUPPLY")
				
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S.NO</th><th style="width:90%">EQUIPMENT & SCOPE DETAILS</th></tr>';
				for(var j=0;j<epq.length;j++)
				{
					vs+='<tr><td>'+(j+1)+'</td><td class="left-td">'+epq[j]+'</td></tr>'
				}
				vs+='</table>*Bulk storage tanks capacity can be based on available optimum level of chemical procurement</center>'
				
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">4. Equipment Details For Proposed Systems</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The proposed equipment description and details are summarized below.</p><br>';
				var fullepq=[]
				if(asu.includes('Rotary Brush Screener'))
				{
					fullepq.push('ROTARY BRUSH SCREENER<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Automated Brush Screener separates coarse & medium fine solids of size above 2 mm from influent. This process is a predetermined stage where escaping of solids is completely avoided, where by clogging of pumps & machinery in subsequent steps gets nullified. The collected wastes have to be disposed periodically and the screener is attached with brush.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/screener.jpg"></center>')
				}
				if(asu.includes('DAF (Dissolved Air Flotation)'))
				{
					fullepq.push('DISSOLVED AIR FLOTATION (DAF) SYSTEM<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">DAF system used to remove total suspended solids (TSS) and oils & greases (O&G) from effluent water; this effectively reduces the pollutant load in biological system. Air and water suctioning pump provided for the flotation of suspends and oils. Scrapping mechanism provided for highly efficient separation of floating suspends and Oils & Greases.</p><br><center><img style="width:4IN!important;" src="https://erp.wttindia.com/files/daf.jpg"></center>')
				}
				if(asu.includes('Equalization System'))
				{
					fullepq.push('EQUALIZATION SYSTEM<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Equalization system used to homogenize different wastewater characteristics to achieve uniform pollutant load. The continuous mixing and water movement maintained by diffused aeration to avoid the dead zone bacteria, solids sedimentation and anaerobic fermentation.</p>')
				}
				if(asu.includes('Neutralization System'))
				{
					fullepq.push('NEUTRALIZATION SYSTEM<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The Biological oxidation system requires a neutral or slightly alkaline pH value for the optimum performance. Neutralization is carried out automatically depending on the pH of the inlet water.</p>')
				}
				if(asu.includes('Cooling Tower'))
				{
					fullepq.push('COOLING TOWER<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Cooling tower is a specialized heat exchanger in which air and water are brought into direct contact with each other in cross flow to reduce the inlet water temperature and it is designed to handle high TSS effluent. It is recommended to keep and maintain the biological oxidation system in optimum temperature for better performance.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/cooling.png"></center>')
				}
				if(asu.includes('Biological Oxidation System'))
				{
					fullepq.push('BIOLOGICAL SYSTEM<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The organic matter is aerated in biological tank to bring down the pollutant load using micro-organisms. The micro-organisms metabolize the organic matters and a Part of organic matter is synthesized into new cells. The microbial growth in the wastewater maintaining by providing required DO level.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/bio.png"></center>')
				}
				if(asu.includes('Lamella Settler'))
				{
					fullepq.push('LAMELLA SETTLER<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Lamella settler system removes solid particulates and suspend solids from liquid through gravity settling to provide polished influent for filtration process and also ensures the required retention time for settling of suspends.</p>')
				}
				if(asu.includes('Circular Clarifier System'))
				{
					fullepq.push('CIRCULAR CLARIFIER<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Clarifier system removes solid particulates and suspended solids from liquid through gravity settling to provide polished influent for filtration process and also ensures the required retention time for settling of suspends. Hereby, Thomson profile is provided for proper and even overflow to ensure proper settling of solids.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/clari.png"></center>')
				}
				// if(asu.includes('Sludge Thickener') || asu.includes('Sludge Thickener with mech'))
				if(asu.includes('Sludge Thickener with mech'))
				{
					fullepq.push('SLUDGE THICKENER<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The thickening is a process that increases the solids matter of the sludge, re-moving part of the water associated with it, and consequently reduces its volume. The mix of water and sludge enter and solids settled at the bottom by gravity, from there suitable scrapers lead it to the central part of the cone and extracted.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/slud.png"></center>')
				}
				if(asu.includes('Belt Press'))
				{
					fullepq.push('BELT PRESS SYSTEM<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The belt press system used for solid-liquid separation processes. It contains belt and rollers of various diameters to pressurize the sludge and squeeze out the water from the sludge. It reduces the volume of sludge and in turn minimizes storage and transportation cost. Belt press system provides high rate of sludge dewatering. Belt press is an advanced cleaning facility and employs completely automated system.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/belt.png"></center>')
				}
				if(asu.includes('Screw Press'))
				{
					fullepq.push('SCREW PRESS<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The Screw press system is for dewatering by continuous gravitational drainage. It works by using a coarse screw to convert the rotation of the handle or drive-wheel into a small downward movement of greater force. This system reduces the volume of sludge and in turn minimizes storage and transportation cost.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/screw.png"></center>')
				}
				if(asu.includes('Micro Filtration - ASAHI'))
				{
					fullepq.push('MICRO/ULTRA FILTRATION SYSTEM<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Micro/Ultra filtration is used to pre-treat primarily treated waste water, in downstream of the reverse osmosis unit and operates at low pressure for the removal of colloidal material of size up to 0.1 micron. It is a pre-treatment for reverse osmosis system in order to reduce membrane fouling rate.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/mf.png"></center>')
				}
				if(asu.includes('Submerged MBR system - KOCH'))
				{
					fullepq.push('SUBMERGED MBR SYSTEM - KOCH<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">This system combines conventional biological treatment processes with mem-brane filtration to provide an advanced level of organic and suspended solids removal in reduced foot print. Both clarification and filtration provides polished influent for RO system.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/mbrkoch.jpg"></center>')
				}
				if(asu.includes('Submerged MBR system - OVIVO'))
				{
					fullepq.push('SUBMERGED MBR SYSTEM - OVIVO<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">This system comprises of Eco-friendly & long lasting Ceramic Membranes. Ceramic MBR system operates at low operational flux and easy to clean as the membrane is rigid and do not lose its form over a period of time. The system can be cleaned with Permeate & Chemically Enhanced Backwash technology and Blowers for Air scouring to avoid sludge deposition. The sprinkler pumps ensures that there is no clogging over the membrane surface.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/mbrovivo.png"></center>')
				}
				if(asu.includes('Sulphur Black Removal System'))
				{
					fullepq.push('SULPHUR BLACK REMOVAL SYSTEM<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">In Denim plants, the MBR system undergoes fouling by the accumulation of in-organic compounds like sulphur. These sulphur compounds can be removed from the membrane surface by backwashing and the water has to be treated before being fed back to the biological oxidation system. The sulphur being inorganic does not settle at the biological process and the re-peated circulation of these compounds in membrane feed stream will increase the fouling rate proportionally and so this sulphur compound has to be removed. Removing these sulphur compounds decreases the fouling rates of the membranes. The sludge (or) sulphur removed from this system can be further concentrated in an evaporator for reusing it as a dye for lighter shades of black.</p><br>')
				}
				if(asu.includes('Degasser System'))
				{
					fullepq.push('DEGASSER TOWER SYSTEM<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Degasser tower eliminates the carbonaceous gases from the effluent water by means of a packed decarbonizing tower. The air blown from the bottom of the tower carries away CO2 from wastewater to the top of the tower to reduce the dissolved gases and there by protect the RO membranes from scaling.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/degasser.png"></center>')
				}
				if(asu.includes('Reverse Osmosis'))
				{
					fullepq.push('REVERSE OSMOSIS SYSTEM<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Reverse Osmosis Process is the forced passage of water through a membrane against the natural osmotic pressure to accomplish separation of ions and water. It separates the dissolved salts from the feed water and reduces the TDS level, and this can be reused for industrial process. We can achieve lowest CAPEX and OPEX.</p><br><center><img style="width:4.5IN!important;" src="https://erp.wttindia.com/files/ro.png"></center>')
				}
				for(var v=0;v<fullepq.length;v++)
				{
					
					vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">4.'+(v+1)+'. '+fullepq[v]+'</p>'
				}
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">5. Equipment Quantity</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The proposed equipment quantity detail is summarized in the tables below.</p><br>';
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%"><tr><th colspan="4">PLANT EQUIPMENT LIST</th></tr>';
				var jj=0;
				if(asu.includes("Biological Oxidation System")){
					
					vs+='<tr><th colspan="4">BIOLOGICAL SYSTEM</th></tr>';
					vs+='<tr><th style="width:10%">S.NO</th><th style="text-align:center;width:30%;">DESCRIPTION</th><th style="text-align:center;width:30%">SPECIFICATION</th><th style="text-align:center;width:30%">QUANTITY</th></tr>';
					var append_arr=[];
					if(asu.includes('Rotary Brush Screener')){append_arr.push("SCREENER & LIFTING SUMP")}
					if(asu.includes('Equalization System')){append_arr.push("EQUALIZATION TANK")}
					append_arr.push("BIOLOGICAL OXIDATION SYSTEM")
					append_arr.push("BIOLOGICAL SYSTEM")
					if(asu.includes('Lamella Settler')){append_arr.push("LAMELLA SETTLER & SLUDGE RECIRCULATION SYSTEM")}
					if(asu.includes('Sludge Thickener')){append_arr.push("SLUDGE THICKENER & SCREW PRESS")}
					if(asu.includes('Sludge Thickener with mech')){append_arr.push("SLUDGE THICKENER & BELT PRESS")}
					var qt = '';
					for(var sno=0;sno<append_arr.length;sno++){
						if(append_arr[sno]=="SCREENER & LIFTING SUMP"){
							vs+='<tr><td rowspan="6" style="vertical-align:middle!important;">'+(sno+1)+'</td><td rowspan="6" style="vertical-align:middle!important;">SCREENER & LIFTING SUMP</td><td class="left-td">ROTARY BRUSH SCREENER</td><td>1</td></tr>'
							vs+='<tr><td class="left-td">MESH SIZE</td><td>2MM</td></tr>'
							vs+='<tr><td class="left-td">MOC</td><td>SS316</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="LIFTING SUMP PUMP"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td class="left-td">LIFTING SUMP PUMP</td><td>'+qt+'</td></tr>'
							vs+='<tr><td class="left-td">PUMP SIZE</td><td>CI</td></tr>'
							vs+='<tr><td class="left-td">PUMP TYPE</td><td>SUBMERSIBLE</td></tr>'
						}
						if(append_arr[sno]=="EQUALIZATION TANK"){
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="EQT BLOWER"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							if(ss_ar[0].seperate_blower_for_equalization_tank==1){
								$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="EQT BLOWER"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
								vs+='<tr><td rowspan="7" style="vertical-align:middle!important;">'+(sno+1)+'</td><td rowspan="7" style="vertical-align:middle!important;">EQUALIZATION TANK</td><td class="left-td">BLOWER FOR EQUALIZATION TANK</td><td>'+qt+'</td></tr>'
								if(frm.doc.tank_height<=6){qt="LOBE"}
								else{qt="SCREW"}
								vs+='<tr><td class="left-td">BLOWER TYPE</td><td>'+qt+'</td></tr>'
							}
							else if(ss_ar[0].seperate_blower_for_equalization_tank==0){
								if(frm.doc.tank_height<=6){qt="LOBE"}
								else{qt="SCREW"}
								vs+='<tr><td rowspan="6" style="vertical-align:middle!important;">'+(sno+1)+'</td><td rowspan="6" style="vertical-align:middle!important;">EQUALIZATION TANK</td><td class="left-td">BLOWER TYPE</td><td>'+qt+'</td></tr>'
							}							
							vs+='<tr><td class="left-td">DIFFUSER</td><td>1 LOT</td></tr>'
							vs+='<tr><td class="left-td">DIFFUSER SIZE</td><td>9"</td></tr>'
							vs+='<tr><td class="left-td">DIFFUSER TYPE</td><td>FINE BUBBLE</td></tr>'
							vs+='<tr><td class="left-td">DIFFUSER MOC</td><td>PP-GF disc with SILICON membrane</td></tr>'
							vs+='<tr><td class="left-td">DIFFUSER GRID PIPING MOC</td><td>SS316</td></tr>'
						}
						if(append_arr[sno]=="BIOLOGICAL OXIDATION SYSTEM"){
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="NT PUMP"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td rowspan="13" style="vertical-align:middle!important;">'+(sno+1)+'</td><td rowspan="13" style="vertical-align:middle!important;">BIOLOGICAL OXIDATION SYSTEM</td><td class="left-td">BIOLOGICAL FEED PUMPS</td><td>'+qt+'</td></tr>'
							vs+='<tr><td class="left-td">PUMP MOC</td><td>CI</td></tr>'
							vs+='<tr><td class="left-td">PUMP TYPE</td><td>SUBMERSIBLE</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="NT PH SENSOR"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td class="left-td">pH SENSOR</td><td>'+qt+'</td></tr>'
							vs+='<tr><td class="left-td">pH SENSOR RANGE</td><td>0-14</td></tr>'
							vs+='<tr><td class="left-td">PRESSURE GUAGE</td><td>1</td></tr>'
							vs+='<tr><td class="left-td">PRESSURE GUAGE RANGE</td><td>0-1 BAR</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="NT DOSING PUMP"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td class="left-td">NEUTRALIZATION DOSING PUMPS</td><td>'+qt+'</td></tr>'
							vs+='<tr><td class="left-td">PUMP MOC</td><td>TEFLON</td></tr>'
							vs+='<tr><td class="left-td">ELECTROMAGNETIC FLOWMETER/td><td>1</td></tr>'
							$.each(frm.doc.bio_full_system || [], function(i, v) {
								if(v.item_description=="Cooling Tower"){qt=v.w_qty+'W'}
							});
							vs+='<tr><td class="left-td">COOLING TOWER</td><td>'+qt+'</td></tr>'
							vs+='<tr><td class="left-td">COOLING TOWER MOC</td><td>SS316 FRAME with FRP PANEL</td></tr>'
							vs+='<tr><td class="left-td">MEDIA MOC</td><td>PP</td></tr>'
						}
						if(append_arr[sno]=="BIOLOGICAL SYSTEM"){
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="BIO BLOWER"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td rowspan="10" style="vertical-align:middle!important;">'+(sno+1)+'</td><td rowspan="10" style="vertical-align:middle!important;">BIOLOGICAL SYSTEM</td><td class="left-td">BLOWER FOR BIOLOGICAL TANK AERATION</td><td>'+qt+'</td></tr>'
							if(frm.doc.tank_height<=6){qt="LOBE"}
							else{qt="SCREW"}
							vs+='<tr><td class="left-td">BLOWER TYPE</td><td>'+qt+'</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="DO SENSOR"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td class="left-td">DO SENSOR</td><td>'+qt+'</td></tr>'
							vs+='<tr><td class="left-td">DO SENSOR RANGE</td><td>0-5PPM</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="BIO DIFFUSER"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}							
								}
							});
							vs+='<tr><td class="left-td">DIFFUSER</td><td>'+qt+'</td></tr>'
							vs+='<tr><td class="left-td">DIFFUSER SIZE</td><td>9"</td></tr>'
							vs+='<tr><td class="left-td">DIFFUSER TYPE</td><td>FINE BUBBLE</td></tr>'
							vs+='<tr><td class="left-td">DIFFUSER MOC</td><td>PP-GF disc with SILICON membrane</td></tr>'
							vs+='<tr><td class="left-td">DIFFUSER GRID PIPING</td><td>1 LOT</td></tr>'

							vs+='<tr><td class="left-td">DIFFUSER GRID PIPING MOC</td><td>PP-GF  (AS HARD AS STAINLESS STEEL) (MAKE: OTT, GERMANY) PP-GF</td></tr>'
						}				
						if(append_arr[sno]=='LAMELLA SETTLER & SLUDGE RECIRCULATION SYSTEM'){
							vs+='<tr><td rowspan="6" style="vertical-align:middle!important;">'+(sno+1)+'</td><td rowspan="6" style="vertical-align:middle!important;">LAMELLA SETTLER & SLUDGE RECIRCULATION SYSTEM</td><td class="left-td">LAMELLA SETTLER</td><td>1 LOT</td></tr>'
							vs+='<tr><td class="left-td">LAMELLA SETTLER FRAME MOC</td><td>SS316</td></tr>'
							vs+='<tr><td class="left-td">LAMELLA PACKS MOC</td><td>PVC</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="SRS PUMP"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}							
								}
							});
							vs+='<tr><td class="left-td">SLUDGE RECIRCULATION PUMP</td><td>'+qt+'</td></tr>'
							vs+='<tr><td class="left-td">PUMP MOC</td><td>CI</td></tr>'
							vs+='<tr><td class="left-td">PUMP TYPE</td><td>HORIZONTAL/ CENTRIFUGAL</td></tr>'
						}
						if(append_arr[sno]=='SLUDGE THICKENER & SCREW PRESS'){
							vs+='<tr><td rowspan="6" style="vertical-align:middle!important;">'+(sno+1)+'</td><td rowspan="6" style="vertical-align:middle!important;">SLUDGE THICKENER & SCREW PRESS</td><td class="left-td">PIPING FOR SLUDGE THICKENER</td><td>1 LOT</td></tr>'
							vs+='<tr><td class="left-td">MOC</td><td>SS316</td></tr>'
							$.each(frm.doc.bio_full_system || [], function(i, v) {
								if(v.item_description=="Screw Press"){qt=v.w_qty+'W'}
							});
							vs+='<tr><td class="left-td">SCREW PRESS SYSTEM</td><td>'+qt+'</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="SCREW FEED PUMP"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td class="left-td">SCREW PRESS FEED PUMPS</td><td>'+qt+'</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="SCREW POLY UNIT MODEL"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td class="left-td">SCREW PRESS POLY DOSING PUMP</td><td>'+qt+'</td></tr>'
							vs+='<tr><td class="left-td">POLY PREPARATION UNIT</td><td>'+qt+'</td></tr>'
						}
						if(append_arr[sno]=='SLUDGE THICKENER & BELT PRESS'){
							$.each(frm.doc.bio_full_system || [], function(i, v) {
								if(v.item_description=="Sludge Thickener" || v.item_description=="Sludge Thickener with mech"){
									qt=v.w_qty+'W'
								}
							});
							vs+='<tr><td rowspan="7" style="vertical-align:middle!important;">'+(sno+1)+'</td><td rowspan="7" style="vertical-align:middle!important;">SLUDGE THICKENER & BELT PRESS</td><td class="left-td">SLUDGE THICKENER MECHANISM</td><td>'+qt+'</td></tr>'
							vs+='<tr><td class="left-td">MOC</td><td>SS316</td></tr>'
							$.each(frm.doc.bio_full_system || [], function(i, v) {
								if(v.item_description=="Belt Press"){qt=v.w_qty+'W'}
							});
							vs+='<tr><td class="left-td">BELT PRESS SYSTEM</td><td>'+qt+'</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="BELT PRESS FEED PUMP"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td class="left-td">BELT PRESS FEED PUMPS</td><td>'+qt+'</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="BELT POLY UNIT MODEL"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td class="left-td">BELT PRESS POLY DOSING PUMP</td><td>'+qt+'</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="BELT WASHING PUMP"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td class="left-td">BELT PRESS WASHING PUMP</td><td>'+qt+'</td></tr>'
							$.each(frm.doc.pre_treatment_table || [], function(i, v) {
								if(v.item_description=="BELT POLY UNIT MODEL"){
									qt=''
									if(v.sb_qty==0){qt=v.w_qty+'W'}
									else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
								}
							});
							vs+='<tr><td class="left-td">POLY PREPARATION UNIT</td><td>'+qt+'</td></tr>'
						}
					}
					vs+='</table><br><table>'
				}
				if(asu.includes("Micro Filtration - ASAHI")){
					vs+='<tr><th colspan="4">MICRO/ULTRA FILTRATION SYSTEM</th></tr>';
					vs+='<tr><th style="width:10%">S.NO</th><th style="text-align:center;width:30%;">DESCRIPTION</th><th style="text-align:center;width:30%">SPECIFICATION</th><th style="text-align:center;width:30%">QUANTITY</th></tr>';
					vs+='<tr><td rowspan="11" style="vertical-align:middle!important;">1</td><td rowspan="11" style="vertical-align:middle!important;">MF/ UF SYSTEM</td><td class="left-td">TOTAL NUMBER OF SKIDS</td><td>1</td></tr>'
					vs+='<tr><td class="left-td">SKID MOC</td><td>SS316</td></tr>'
					$.each(frm.doc.mf_table || [], function(i, v) {
						if(v.item_description=="FEED PUMP"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td class="left-td">FEED PUMP</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">PUMP MOC</td><td>CI</td></tr>'
					vs+='<tr><td class="left-td">PUMP TYPE</td><td>HORIZONTAL/ CENTRIFUGAL</td></tr>'
					$.each(frm.doc.mf_table || [], function(i, v) {
						if(v.item_description=="PRE-FILTER"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td class="left-td">PRE FILTER</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">PRE FILTER HOUSING MOC</td><td>SS316</td></tr>'
					vs+='<tr><td class="left-td">MF/ UF MODULES</td><td>1 LOT</td></tr>'
					vs+='<tr><td class="left-td">MODULE MOC</td><td>PVDF</td></tr>'
					vs+='<tr><td class="left-td">ELECTROMAGNETIC FLOWMETER</td><td>PREMEATE</td></tr>'
					vs+='<tr><td class="left-td">CIP TABNK WITH ITE FILTER AND ITS PIPING</td><td>1 SET</td></tr>'
					vs+='</table><br><table>'
				}
				if(asu.includes("Submerged MBR system - KOCH")){
					vs+='<tr><th colspan="4">SUBMERGED MBR SYSTEM - KOCH</th></tr>';
					vs+='<tr><th style="width:10%">S.NO</th><th style="text-align:center;width:30%;">DESCRIPTION</th><th style="text-align:center;width:30%">SPECIFICATION</th><th style="text-align:center;width:30%">QUANTITY</th></tr>';
					vs+='<tr><td rowspan="16" style="vertical-align:middle!important;">1</td><td rowspan="16" style="vertical-align:middle!important;">MBR MODULE</td><td class="left-td">TOTAL NUMBER OF SKIDS</td><td>1</td></tr>'
					vs+='<tr><td class="left-td">NO OF TRAIN</td><td>'+ss_ar[0].design_no_of_trains+'</td></tr>'
					vs+='<tr><td class="left-td">TOTAL FILTRATION AREA</td><td>'+Math.round(ss_ar[0].total_filtration_area)+'</td></tr>'
					vs+='<tr><td class="left-td">MOC OF MODULE</td><td>PVDF, Braided hollow fibre</td></tr>'
					vs+='<tr><td class="left-td">MOC OF RACK</td><td>SS316</td></tr>'			
					$.each(frm.doc.mbr_table || [], function(i, v) {
						if(v.item_description=="PERMEATE/BACKWASH/CIP PUMP"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td class="left-td">PERMEATE/ BACKWASH/ CIP PUMP</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">PUMP MOC</td><td>CI</td></tr>'
					vs+='<tr><td class="left-td">TYPE OF PUMP</td><td>LOBE TYPE</td></tr>'
					vs+='<tr><td class="left-td">OPERATION</td><td>REVERSIBLE LOBE</td></tr>'
					$.each(frm.doc.mbr_table || [], function(i, v) {
						if(v.item_description=="SLUDGE EXTRACT PUMP"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td class="left-td">SLUDGE PUMP</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">PUMP MOC</td><td>CI</td></tr>'
					vs+='<tr><td class="left-td">PUMP TYPE</td><td>HORIZONTAL/ CENTRIFUGAL</td></tr>'
					vs+='<tr><td class="left-td">DOSING PUMP</td><td>3W</td></tr>'
					$.each(frm.doc.mbr_table || [], function(i, v) {
						if(v.item_description=="MBR BLOWER"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td class="left-td">BLOWER</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">BLOWER DISCHARGE PRESSURE</td><td>< 1 BAR</td></tr>'
					vs+='<tr><td class="left-td">ELECTROMAGNETIC FLOWMETER</td><td>PERMEATE</td></tr>'
					vs+='</table><br><table>'
				}
				if(asu.includes("Submerged MBR system - OVIVO")){
					vs+='<tr><th colspan="4">SUBMERGED MBR SYSTEM - OVIVO</th></tr>';
					vs+='<tr><th style="width:10%">S.NO</th><th style="text-align:center;width:30%;">DESCRIPTION</th><th style="text-align:center;width:30%">SPECIFICATION</th><th style="text-align:center;width:30%">QUANTITY</th></tr>';
					$.each(frm.doc.mbr_ovivo_table || [], function(i, v) {
						if(v.item_description=="MBR MODULES"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td rowspan="17" style="vertical-align:middle!important;">1</td><td rowspan="17" style="vertical-align:middle!important;">MBR SYSTEM</td><td class="left-td">NO OF MODULE</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">MOC OF MODULE</td><td>CERAMIC MEMBRANE</td></tr>'
					vs+='<tr><td class="left-td">NUMBER OF TRAINS</td><td>'+ss_ar[0].ovivo_no_of_trains+'</td></tr>'
					vs+='<tr><td class="left-td">NO OF STACKS</td><td>'+ss_ar[0].ovivo_no_of_stacks_required+'</td></tr>'
					vs+='<tr><td class="left-td">STACKS PER TRAIN</td><td>'+ss_ar[0].ovivo_no_of_module_per_train+'</td></tr>'
					vs+='<tr><td class="left-td">TOTAL FILTRATION AREA</td><td>'+ss_ar[0].total_filtration_area+'</td></tr>'
					$.each(frm.doc.mbr_ovivo_table || [], function(i, v) {
						if(v.item_description=="PERMEATE PUMP"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td class="left-td">PERMEATE PUMP</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">PUMP MOC</td><td>CI</td></tr>'
					$.each(frm.doc.mbr_ovivo_table || [], function(i, v) {
						if(v.item_description=="BACKWASH/CIP PUMP"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td class="left-td">BACKWASH/ CIP PUMP</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">PUMP TYPE</td><td>HORIZONTAL/ CENTRIFUGAL</td></tr>'
					vs+='<tr><td class="left-td">PUMP MOC</td><td>CI</td></tr>'
					$.each(frm.doc.mbr_ovivo_table || [], function(i, v) {
						if(v.item_description=="SLUDGE EXTRACT PUMP"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td class="left-td">SLUDGE PUMP</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">PUMP TYPE</td><td>HORIZONTAL/ CENTRIFUGAL</td></tr>'
					vs+='<tr><td class="left-td">PUMP MOC</td><td>CI</td></tr>'

					vs+='<tr><td class="left-td">DOSING PUMP</td><td>3W</td></tr>'
					vs+='<tr><td class="left-td">TURBIDITY SENSOR</td><td>'+Math.round(ss_ar[0].ovivo_no_of_trains)+'</td></tr>'
					vs+='<tr><td class="left-td">ELECTROMAGNETIC FLOWMETER</td><td>EACH PERMEATE LINE</td></tr>'
					vs+='</table><br><table>'
				}
				if(asu.includes("Sulphur Black Removal System")){
					var dd = '';
					if(selected_system_array.includes("Micro Filtration (ASAHI)")){dd=frm.doc.mf_table}
					else if(selected_system_array.includes("Submerged MBR system - KOCH")){dd=frm.doc.mbr_table}
					else if(selected_system_array.includes("Submerged MBR system - OVIVO")){dd=frm.doc.mbr_ovivo_table}
					if(dd!=''){
						$.each(dd || [], function(i, v) {
							if(v.item_description=="SULPHUR BLACK DOSING PUMP"){
								qt=''
								if(v.sb_qty==0){qt=v.w_qty+'W'}
								else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
							}
						});
					}
					vs+='<tr><th colspan="4">SULPHUR BLACK REMOVAL SYSTEM</th></tr>';
					vs+='<tr><th style="width:10%">S.NO</th><th style="text-align:center;width:30%;">DESCRIPTION</th><th style="text-align:center;width:30%">SPECIFICATION</th><th style="text-align:center;width:30%">QUANTITY</th></tr>';
					vs+='<tr><td rowspan="6" style="vertical-align:middle!important;">1</td><td rowspan="6" style="vertical-align:middle!important;">SULPHUR BLACK REMOVAL SYSTEM</td><td class="left-td">DOSING PUMP</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">DOSING PUMP MOC</td><td>PP</td></tr>'
					vs+='<tr><td class="left-td">LAMELLA SETTLER</td><td>1</td></tr>'
					vs+='<tr><td class="left-td">LAMELLA PACKS MOC</td><td>PVC</td></tr>'
					vs+='<tr><td class="left-td">LAMELLA SETTLER FRAME MOC</td><td>SS316</td></tr>'
					if(dd!='' && dd!=frm.doc.mbr_table){
						$.each(dd || [], function(i, v) {
							if(v.item_description=="SLUDGE EXTRACT PUMP"){
								qt=''
								if(v.sb_qty==0){qt=v.w_qty+'W'}
								else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
							}
						});
					}
					vs+='<tr><td class="left-td">SLUDGE PUMP</td><td>'+qt+'</td></tr>'
					vs+='</table><br><table>'
				}
				if(asu.includes("Degasser System")){
					vs+='<tr><th colspan="4">DEGASSER TOWER</th></tr>';
					vs+='<tr><th style="width:10%">S.NO</th><th style="text-align:center;width:30%;">DESCRIPTION</th><th style="text-align:center;width:30%">SPECIFICATION</th><th style="text-align:center;width:30%">QUANTITY</th></tr>';
					$.each(frm.doc.dgt_items || [], function(i, v) {
						if(v.item_description=="Degasser System"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td rowspan="9" style="vertical-align:middle!important;">1</td><td rowspan="9" style="vertical-align:middle!important;">DEGASSER TOWER</td><td class="left-td">DEGASSER TOWER VESSEL</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">TOWER MOC</td><td>FRP</td></tr>'
					$.each(frm.doc.dgt_items || [], function(i, v) {
						if(v.item_description=="PH SENSOR"){
							qt=''
							if(v.sb_qty==0){qt=v.w_qty+'W'}
							else{qt=v.w_qty+'W + '+v.sb_qty+'S'}
						}
					});
					vs+='<tr><td class="left-td">pH SENSOR</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">DEGASSER TOWER MEDIA</td><td>1 LOT</td></tr>'
					vs+='<tr><td class="left-td">MEDIA MOC</td><td>PP</td></tr>'
					vs+='<tr><td class="left-td">DEGASSER TOWER BLOWER FAN</td><td>1</td></tr>'
					vs+='<tr><td class="left-td">BLOWER FAN MOC</td><td>SS304</td></tr>'
					vs+='<tr><td class="left-td">DOSING PUMP FOR DEGASSER TOWER</td><td>fetch_values_from_startup_sheet</td></tr>'
					vs+='<tr><td class="left-td">PUMPS MOC</td><td>PP/ TEFLON</td></tr>'
					vs+='</table><br><table>'
				}
				if(asu.includes("Reverse Osmosis")){
					vs+='<tr><th colspan="4">REVERSE OSMOSIS SYSTEM</th></tr>';
					vs+='<tr><th style="width:10%">S.NO</th><th style="text-align:center;width:30%;">DESCRIPTION</th><th style="text-align:center;width:30%">SPECIFICATION</th><th style="text-align:center;width:30%">QUANTITY</th></tr>';
					vs+='<tr><td rowspan="25" style="vertical-align:middle!important;">1</td><td rowspan="25" style="vertical-align:middle!important;">RO SKID</td><td class="left-td">TOTAL NUMBER OF SKIDS</td><td>1</td></tr>'
					vs+='<tr><td class="left-td">SKID MOC</td><td>SS316</td></tr>'
					vs+='<tr><td class="left-td">NO OF STAGES</td><td>4</td></tr>'
					qt=0;
					for(var iro=0;iro<ro_ar.length;iro++){
						if(ro_ar[iro].item_description=="FEED PUMP"){
							if(ro_ar[iro].sb_qty==0){qt=ro_ar[iro].w_qty+'W'}
							else{qt=ro_ar[iro].w_qty+'W + '+ro_ar[iro].sb_qty+'S'}
						}
					}
					vs+='<tr><td class="left-td">RO FEED PUMP</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">RO FEED PUMP MOC</td><td>CI</td></tr>'
					vs+='<tr><td class="left-td">PUMP TYPE</td><td>HORIZONTAL/ CENTRIFUGAL</td></tr>'
					vs+='<tr><td class="left-td">PRE-FILTER</td><td>1</td></tr>'
					vs+='<tr><td class="left-td">PRE-FILTER HOUSING MOC</td><td>SS316</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<ro_ar.length;iro++){
						if(ro_ar[iro].renamed=="DOSING PUMP"){
							w_qty=w_qty+ro_ar[iro].w_qty
							sb_qty=sb_qty+ro_ar[iro].w_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">DOSING PUMPS</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">DOSING PUMP MOC</td><td>PP</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<ro_ar.length;iro++){
						if(ro_ar[iro].renamed=="TANK"){
							if((ro_ar[iro].item_description).includes("DOSING TANK")){
								w_qty=w_qty+ro_ar[iro].w_qty
								sb_qty=sb_qty+ro_ar[iro].sb_qty
							}
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">DOSING TANKS</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">DOSING TANKS MOC</td><td>LDPE</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<ro_ar.length;iro++){
						if(ro_ar[iro].renamed=="HIGH PRESSURE PUMP"){
							w_qty=w_qty+ro_ar[iro].w_qty
							sb_qty=sb_qty+ro_ar[iro].sb_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">HIGH PRESSURE PUMP WITH INVERTER</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">HIGH PRESSURE PUMP MOC</td><td>SS316</td></tr>'
					vs+='<tr><td class="left-td">HIGH PRESSURE PUMP TYPE</td><td>VERTICAL-MULTI STAGE</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<ro_ar.length;iro++){
						if(ro_ar[iro].item_description=="BOOSTER PUMP"){
							w_qty=w_qty+ro_ar[iro].w_qty
							sb_qty=sb_qty+ro_ar[iro].sb_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">BOOSTER PUMPS WITH INVERTER</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">BOOSTER PUMPS MOC</td><td>SS316</td></tr>'
					vs+='<tr><td class="left-td">BOOSTER PUMPS TYPE</td><td>VERTICAL-MULTI STAGE</td></tr>'
					vs+='<tr><td class="left-td">PRESSURE VESSELS</td><td>1 LOT</td></tr>'
					vs+='<tr><td class="left-td">PRESSURE VESSELS MOC</td><td>COMPOSITE POLYAMIDE</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<ro_ar.length;iro++){
						if(ro_ar[iro].renamed=="PH SENSOR"){
							w_qty=w_qty+ro_ar[iro].w_qty
							sb_qty=sb_qty+ro_ar[iro].sb_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">pH SENSOR</td><td>'+qt+'</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<ro_ar.length;iro++){
						if(ro_ar[iro].renamed=="PRESSURE GAUGE"){
							w_qty=w_qty+ro_ar[iro].w_qty
							sb_qty=sb_qty+ro_ar[iro].sb_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">PRESSURE INDICATOR</td><td>'+qt+'</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<ro_ar.length;iro++){
						if(ro_ar[iro].renamed=="PRESSURE TRANSMITTER"){
							w_qty=w_qty+ro_ar[iro].w_qty
							sb_qty=sb_qty+ro_ar[iro].sb_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">PRESSURE TRANSMITTER</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">ELECTROMAGNETIC FLOWMETER</td><td>FEED/ EACH STAGE PERMEATE</td></tr>'
					vs+='<tr><td class="left-td">CIP DOUBLESS SKID WITH AUTOMATION(INCLUSIVE OF PUMPS WITH ITS FILTER, PH-SENSOR, FLOWMETER, PRESSURE TRANSMITTER, AUTO VALVES & DOSING PUMPS)</td><td>1 SET</td></tr>'
					vs+='</table><br><table>'
				}
				if(frm.doc.is_rewolutte==1 || selected_system_array.includes("Rewolutte RO")){
					vs+='<tr><th colspan="4">REVERSE OSMOSIS SYSTEM (REWOLUTTE)</th></tr>';
					vs+='<tr><th style="width:10%">S.NO</th><th style="text-align:center;width:30%;">DESCRIPTION</th><th style="text-align:center;width:30%">SPECIFICATION</th><th style="text-align:center;width:30%">QUANTITY</th></tr>';
					vs+='<tr><td rowspan="25" style="vertical-align:middle!important;">1</td><td rowspan="25" style="vertical-align:middle!important;">RO SKID</td><td class="left-td">TOTAL NUMBER OF SKIDS</td><td>1</td></tr>'
					vs+='<tr><td class="left-td">SKID MOC</td><td>SS316</td></tr>'
					vs+='<tr><td class="left-td">NO OF STAGES</td><td>4</td></tr>'
					qt=0;
					for(var iro=0;iro<rro_ar.length;iro++){
						if(rro_ar[iro].item_description=="FEED PUMP"){
							if(rro_ar[iro].sb_qty==0){qt=rro_ar[iro].w_qty+'W'}
							else{qt=rro_ar[iro].w_qty+'W + '+rro_ar[iro].sb_qty+'S'}
						}
					}
					vs+='<tr><td class="left-td">RO FEED PUMP</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">RO FEED PUMP MOC</td><td>CI</td></tr>'
					vs+='<tr><td class="left-td">PUMP TYPE</td><td>HORIZONTAL/ CENTRIFUGAL</td></tr>'
					vs+='<tr><td class="left-td">PRE-FILTER</td><td>1</td></tr>'
					vs+='<tr><td class="left-td">PRE-FILTER HOUSING MOC</td><td>SS316</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<rro_ar.length;iro++){
						if(rro_ar[iro].renamed=="DOSING PUMP"){
							w_qty=w_qty+rro_ar[iro].w_qty
							sb_qty=sb_qty+rro_ar[iro].w_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">DOSING PUMPS</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">DOSING PUMP MOC</td><td>PP</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<rro_ar.length;iro++){
						if(rro_ar[iro].renamed=="TANK"){
							if((rro_ar[iro].item_description).includes("DOSING TANK")){
								w_qty=w_qty+rro_ar[iro].w_qty
								sb_qty=sb_qty+rro_ar[iro].sb_qty
							}
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">DOSING TANKS</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">DOSING TANKS MOC</td><td>LDPE</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<rro_ar.length;iro++){
						if(rro_ar[iro].renamed=="HIGH PRESSURE PUMP"){
							w_qty=w_qty+rro_ar[iro].w_qty
							sb_qty=sb_qty+rro_ar[iro].sb_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">HIGH PRESSURE PUMP WITH INVERTER</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">HIGH PRESSURE PUMP MOC</td><td>SS316</td></tr>'
					vs+='<tr><td class="left-td">HIGH PRESSURE PUMP TYPE</td><td>VERTICAL-MULTI STAGE</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<rro_ar.length;iro++){
						if(rro_ar[iro].item_description=="BOOSTER PUMP"){
							w_qty=w_qty+rro_ar[iro].w_qty
							sb_qty=sb_qty+rro_ar[iro].sb_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">BOOSTER PUMPS WITH INVERTER</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">BOOSTER PUMPS MOC</td><td>SS316</td></tr>'
					vs+='<tr><td class="left-td">BOOSTER PUMPS TYPE</td><td>VERTICAL-MULTI STAGE</td></tr>'
					vs+='<tr><td class="left-td">PRESSURE VESSELS</td><td>1 LOT</td></tr>'
					vs+='<tr><td class="left-td">PRESSURE VESSELS MOC</td><td>COMPOSITE POLYAMIDE</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<rro_ar.length;iro++){
						if(rro_ar[iro].renamed=="PH SENSOR"){
							w_qty=w_qty+rro_ar[iro].w_qty
							sb_qty=sb_qty+rro_ar[iro].sb_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">pH SENSOR</td><td>'+qt+'</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<rro_ar.length;iro++){
						if(rro_ar[iro].renamed=="PRESSURE GAUGE"){
							w_qty=w_qty+rro_ar[iro].w_qty
							sb_qty=sb_qty+rro_ar[iro].sb_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">PRESSURE INDICATOR</td><td>'+qt+'</td></tr>'
					qt=''
					var w_qty=0;
					var sb_qty=0;
					for(var iro=0;iro<rro_ar.length;iro++){
						if(rro_ar[iro].renamed=="PRESSURE TRANSMITTER"){
							w_qty=w_qty+rro_ar[iro].w_qty
							sb_qty=sb_qty+rro_ar[iro].sb_qty
						}
					}
					if(sb_qty==0){qt=w_qty+'W'}
					else{qt=w_qty+'W + '+sb_qty+'S'}
					vs+='<tr><td class="left-td">PRESSURE TRANSMITTER</td><td>'+qt+'</td></tr>'
					vs+='<tr><td class="left-td">ELECTROMAGNETIC FLOWMETER</td><td>FEED/ EACH STAGE PERMEATE</td></tr>'
					vs+='<tr><td class="left-td">CIP DOUBLESS SKID WITH AUTOMATION(INCLUSIVE OF PUMPS WITH ITS FILTER, PH-SENSOR, FLOWMETER, PRESSURE TRANSMITTER, AUTO VALVES & DOSING PUMPS)</td><td>1 SET</td></tr>'
					vs+='</table><br><table>'

				}
				vs+='</table></center>'
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">KEY FEATURES</p><br>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Our scope of supplies are of SS316 pipes and tubes for Air line, MBR pipe line, RO pipe line & including the RO skid and materials like UPVC are used only in areas where SS316 is not compatible.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Especially for Biological system Diffuser Grid, PP-GF (OTT-German) – As Hard as Stainless Steel is proposed.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Elegant and durable Rotary Brush Screener with Nylon Bristles made at World Class manufacturing facility.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>We are supplying the DAF system with Nano bubble generation Pump (NIKUNI-Japan) which is KEY IMPORTANCE for our process.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Our DAF equipment’s are made of SS316.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Diffusers made of long lasting PP-GF Silicon membrane and enables utmost mixing by fine bubbles.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Submerged MBR system with a higher membrane life and auto cleaning capabilities.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Sulphur Black Removal system proposed for reducing the low bio-degradable sulphur dyes.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Store standby proposed separately with price for RO high pressure pumps for all stages.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Each stage of RO permeate has individual EMFM for better control and better automation to keep efficiency and life of RO.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>STATE OF ART 2 SKIDS of CIP system for RO with full automation including dosing of chemicals with PH automation and flow with pressure control.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>ALL part of the plant has LEVEL sensors to have complete data on volume of water in each tanks.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Our scope of supplies are of SS316 pipes and tubes for MF pipe line, RO pipe line & including the RO skid and materials like UPVC are used only in areas where SS316 is not compatible</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>MF/UF system with a higher membrane life and auto cleaning capabilities.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>Each stage of RO permeate has individual EMFM for better control and better automation to keep efficiency and life of RO.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>STATE OF ART 2 SKIDS of CIP system for RO with full automation including dosing of chemicals with PH automation and flow with pressure control.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>ALL part of the plant has LEVEL sensors to have complete data on volume of water in each tanks.</i></li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;color:#002063;"><li><i>SCADA, PLC integrated with HMI providing seamlessly integrated control system with live monitoring to minimize the manpower interruption, and by using advanced cloud technology, we can control total plant operation by smartphone or PC.</i></li></ul>';
				var eep=["DIFFUSER", "DIFFUSER GRID (BIOLOGICAL)", "BLOWER", "SUBMERSIBLE PUMP", "PRESSURE PUMP", "SURFACE MOUNTED PUMP", "ROTARY LOBE PUMP", "DAF CIRCULATION PUMP (NANO BUBBLE GENERATION)", "SLUDGE PUMP", "DOSING PUMP", "MBR MEMBRANES", "RO MEMBRANES", "PRESSURE VESSELS", "VARIABLE FREQUENCY DRIVE", "ELECTROMAGNETIC FLOWMETER", "pH-SENSOR", "DO SENSOR", "LEVEL TRANSMITTER", "LEVEL FLOAT", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "AUTOMATION", "ELECTRICAL PANEL", "ELECTRICAL CABLE", "SCREENER", "DISSLOVED AIR FLOTATION (DAF)", "COOLING TOWER", "DEGASSER TOWER"];
				var supp=["OTT / EQUIVALENT", "OTT (GERMAN) / EQUIVALENT", "ROBUSCHI (ITALY) / EQUIVALENT", "XYLEM (USA) / GRUNDFOS (DENMARK) / EQUIVALENT", "LOWARA (ITALY) / GRUNDFOS (DENMARK) / EQUIVALENT", "LOWARA (ITALY) / GRUNDFOS (DENMARK) / EQUIVALENT", "BOERGER (GERMANY) / VOGELSANG (GERMANY) / NETZSCH (GERMANY) / EQUIVALENT", "NIKUNI (JAPAN) / EQUIVALENT", "KIRLOSKAR (INDIA) / JOHNSON (USA) / EQUIVALENT", "PROMINENT (GERMANY) / EQUIVALENT", "KOCH / EQUIVALENT", "HYDRANAUTICS (USA) / EQUIVALENT", "CODELINE (USA) / PROTEC (USA) / EQUIVALENT", "YASKAWA (JAPAN) / ABB (SWITZERLAND) / EQUIVALENT", "E+H (SWITZERLAND) / EQUIVALENT", "E+H (SWITZERLAND) / EQUIVALENT", "E+H (SWITZERLAND) / EQUIVALENT", "E+H (SWITZERLAND) / EQUIVALENT", "FAES (ITALY) / EQUIVALENT", "DANFOSS (DENMARK) / EQUIVALENT", "WIKA (ITALY) / MASS (INDIA) / EQUIVALENT", "BECKHOFF (GERMANY) / EQUIVALENT", "RITTAL (GERMANY) / EQUIVALENT", "LAPP (GERMANY) / EQUIVALENT", "WTT", "WTT", "WTT", "WTT"];
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">6. Typical Equipment Vendor List</p><br>';
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S. NO</th><th style="width:45%">EQUIPMENT</th><th style="width:45%">SUPPLIER (MAKE)</th></tr>';
				for(var i=0;i<eep.length;i++)
				{
					vs+='<tr><td>'+(i+1)+'. </td><td class="left-td">'+eep[i]+'</td><td class="left-td">'+supp[i]+'</td></tr>'
				}
				vs+='</table></center>'
				var eep1=["PRESSURE PUMP", "SURFACE MOUNTED PUMP", "DOSING PUMP", "MF MEMBRANES", "RO MEMBRANES", "PRESSURE VESSELS", "VARIABLE FREQUENCY DRIVE", "ELECTROMAGNETIC FLOWMETER", "pH-SENSOR", "LEVEL TRANSMITTER", "LEVEL FLOAT", "PRESSURE TRANSMITTER", "PRESSURE GAUGE", "AUTOMATION", "ELECTRICAL PANEL", "ELECTRICAL CABLE", "DEGASSER TOWER"];
				var supp1=["LOWARA (ITALY) / GRUNDFOS (DENMARK) / EQUIVALENT", "LOWARA (ITALY) / GRUNDFOS (DENMARK) / EQUIVALENT", "PROMINENT (GERMANY) /MILTON ROY (USA) / EQUIVALENT", "ASAHI KASEI (JAPAN)", "HYDRANAUTICS (USA) / EQUIVALENT", "CODELINE (USA) / PROTEC (SPAIN) / EQUIVALENT", "YASKAWA (JAPAN) / ABB (SWITZERLAND) / EQUIVALENT", "E+H (SWITZERLAND) / EQUIVALENT", "E+H (SWITZERLAND) / EQUIVALENT", "E+H (SWITZERLAND) / EQUIVALENT", "FAES (ITALY) / EQUIVALENT", "DANFOSS (DENMARK) / EQUIVALENT", "WIKA (ITALY) / MASS (INDIA) / FORBES MARSHALL (INDIA) / EQUIVALENT", "BECKHOFF (GERMANY) / EQUIVALENT", "RITTAL (GERMANY) / EQUIVALENT", "LAPP (GERMANY) / EQUIVALENT", "WTT"];
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;"><tr><th style="width:10%">S. NO</th><th style="width:45%">EQUIPMENT</th><th style="width:45%">SUPPLIER (MAKE)</th></tr>';
				for(var i=0;i<eep1.length;i++)
				{
					vs+='<tr><td style="text-align:center;">'+(i+1)+'. </td><td class="left-td">'+eep1[i]+'</td><td class="left-td">'+supp1[i]+'</td></tr>'
				}
				vs+='</table></center>'
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">7. Pricing Detail</p><br>';
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%"><tr><th colspan="3">PRICE FOR PROPOSED SYSTEMS</th></tr>';
				vs+='<tr><th style="text-align:center;width:10%">S. NO</th><th style="text-align:center;width:45%">SYSTEM/EQUIPMENT</th><th style="text-align:center;width:45%">INR IN LAKHS</th></tr>'
				var ct1=0
				$.each(frm.doc.standard_cost || [], function(i, v) {
					if(v.system_name=="Pre Treatment"){
						ct1=v.cost
					}
				});
				vs+='<tr><td>1. </td><td class="left-td">BIOLOGICAL SYSTEM</td><td>₹ '+new Intl.NumberFormat('en-DE').format(Math.round(ct1)/100000)+' LAKHS</td></tr>'
				var ct2=0
				$.each(frm.doc.standard_cost || [], function(i, v) {
					if(v.system_name=="MBR(K)"){
						ct2=v.cost
					}
				});
				vs+='<tr><td>2. </td><td class="left-td">SUBMERGED MBR SYSTEM</td><td>₹ '+new Intl.NumberFormat('en-DE').format(Math.round(ct2)/100000)+' LAKHS</td></tr>'
				var ct3=0
				$.each(frm.doc.standard_cost || [], function(i, v) {
					if(v.system_name=="Degasser System"){
						ct3=v.cost
					}
				});
				vs+='<tr><td>3. </td><td class="left-td">DEGASSER TOWER SYSTEM</td><td>₹ '+new Intl.NumberFormat('en-DE').format(Math.round(ct3)/100000)+' LAKHS</td></tr>'
				var ct4=0
				$.each(frm.doc.standard_cost || [], function(i, v) {
					if(v.system_name=="RO"){
						ct4=v.cost
					}
				});
				vs+='<tr><td>4. </td><td class="left-td">REVERSE OSMOSIS SYSTEM</td><td>₹ '+new Intl.NumberFormat('en-DE').format(Math.round(ct4)/100000)+' LAKHS</td></tr>'
				var total_cost = Math.round(ct1)+Math.round(ct2)+Math.round(ct3)+Math.round(ct4)
				vs+='<tr><td colspan="2">TOTAL PRICE FOR PROPOSED SYSTEMS</td><td>₹ '+new Intl.NumberFormat('en-DE').format(total_cost/100000)+' LAKHS</td></tr>'
				vs+='</table></center>'

				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%"><tr><th colspan="3">PRICE FOR OPTIONAL SYSTEM</th></tr>';
				vs+='<tr><th style="text-align:center;width:10%">S. NO</th><th style="text-align:center;width:45%;">SYSTEM/EQUIPMENT</th><th style="text-align:center;width:45%;">INR IN LAKHS</th></tr>'
				var ct5=0
				$.each(frm.doc.standard_cost || [], function(i, v) {
					if(v.system_name=="MBR(O)"){
						ct5=v.cost
					}
				});
				vs+='<tr><td>1. </td><td class="left-td">WTT - SUBMERGED MBR SYSTEM WITH SULPHUR BLACK REMOVAL SYSTEM</td><td>₹ '+new Intl.NumberFormat('en-DE').format(Math.round(ct5)/100000)+' LAKHS</td></tr>'
				vs+='</table></center>'

				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;">';
				vs+='<tr><th style="text-align:center;width:10%">S. NO</th><th style="text-align:center;width:45%;">SYSTEM/EQUIPMENT</th><th style="text-align:center;width:45%;">INR IN LAKHS</th></tr>'
				vs+='<tr><td>1. </td><td class="left-td">RO HIGH PRESSURE STORE STANDBY PUMPS</td><td>₹ '+new Intl.NumberFormat('en-DE').format(frm.doc.ssb_pressure_pump_cost/100000)+' LAKHS</td></tr>'
				vs+='</table></center>'

				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Pricing provided herein does not include any duties and taxes.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Pricing provided herein is on EXW basis & does not include the freight/insurance charges</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Supervision of erection and commissioning of WTT supplied system shall be extra.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Payment/commercial terms & conditions as per WTT’s General Terms & Conditions of sale.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Price valid for 15 days due to market volatility</li></ul>';
				
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">MAJOR OPERATING COST FOR PROPOSED SYSTEMS TO ACHIEVE 90% OF RECOVERY:</p><br>';
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;">';
				vs+='<tr><th style="text-align:center;width:10%">S.NO</th><th style="text-align:center;width:45%">FLOW: '+frm.doc.flow+' M<span>&sup3;</span>/DAY</th><th style="text-align:center;width:45%">Cost in Rs./M<span>&sup3;</span></th></tr>'
				vs+='<tr><td>1. </td><td class="left-td">CHEMICAL COST</td><td></td></tr>'
				vs+='<tr><td>2. </td><td class="left-td">MEMBRANE REPLACEMENT COST</td><td></td></tr>'
				vs+='<tr><td>3. </td><td class="left-td">ENERGY COST – 8 Rs./kW</td><td></td></tr>'
				vs+='<tr><td colspan="2">TOTAL PRICE FOR PROPOSED SYSTEMS</td><td></td></tr>'
				vs+='</table><br>* Chemical cost doesn’t include Acid consumption for Neutralization as the pH will vary at ETP inlet from time to time.</center>'
				
				vs+='<p style="font-family:Roboto;font-size: 18px;"><b>Notes: Operating cost doesn’t include the following:</b></p><br>';
				vs+='<p style="margin-left:30px;font-family:Roboto;font-size: 18px;">Influent transfer until Proposed System, Permeate & Reject transfer, Evaporator system, Major Repair & Maintenance, Compressed air & Raw water for complete plant, Transport, Taxes & Duties for Chemical & Replacement cost, Cost for Loaders, Cleaners, Vehicles & its consumables, Manpower Cost.</p><br>';
				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">ELECTRICAL LOAD FOR PROPOSED SYSTEMS:</p><br>';
				
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;">';
				vs+='<tr><th style="text-align:center;width:10%">S. NO</th><th style="text-align:center;width:45%">LOAD</th><th style="text-align:center;width:45%">kW</th></tr>'
				vs+='<tr><td>1. </td><td>Total connected load</td><td></td></tr>'
				vs+='<tr><td>2. </td><td>Total absorbed load</td><td></td></tr>'
				vs+='</table></center>'

				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">8. Exclusions</p><br>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Transfer of influent up to proposed system.</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>All civil related works, civil structural drawings, underground piping & piping for electrical cabling during civil works.</li></ul>';  
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Installation of supplied equipment.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>All loading & unloading @ site </li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>All excavation works related with pipe and cables laying.</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Electrical cable & stabilized power supply until WTT panel’s, Internal Individual Earthing as per requirement</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Compressed air supply for proposed equipment.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Raw water supply for whole plant and treated water transfer</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Chemical supply and storage/preparation tanks</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Separate panel, wiring with fans & lights for whole plant & its power supply</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Pre-Shipment Inspection requested by the local authorities</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>All license fees and / or custom duties.</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Provide Food, Accommodation and Local transport to the team of WTT.</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Installation consumables (such as welding electrodes, cutting disk and others).</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Supply and assembly of all drainage lines for rain water, sewers, etc.</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Any construction approval from local Authorities.</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Supply of any hoisting and/or laying equipment (cranes forklift, etc.) both truck mounted or not.</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Construction of site fencing/railing.</li></ul>'; 
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Protection for all field instruments, local switches, motors, etc.,</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Safety handrails for all tanks, safety items like life buoy rings, eye washer, life-jackets, etc.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Removal of all residual debris after construction and thorough cleaning of all tanks before plant start-up.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>General spares for supplied equipment.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Any further item not described in our offer.</li></ul>';

				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">9. Happy Customers</p><br>';
				vs+='<br><center><img src="https://erp.wttindia.com/files/happycustomer.png"></center>'

				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">10. Channel Partners</p><br>';
				vs+='<br><center><img src="https://erp.wttindia.com/files/channel.png"></center>'

				vs+='<br><br><p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">11. Process Description Video</p><br>';
				vs+='<br><center><img style="width:1IN!important;height:1IN!important" src="https://erp.wttindia.com/files/processvideo.png"></center>'

				vs+='<p style="font-weight:bold;color:#002063;font-family:Roboto;font-size: 20px;">12. Commercial Terms And Conditions</p><br>';
				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">12.1. TAXES</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Taxes and Duties shall be extra as applicable. Pricing provided herein does not include any taxes of destination country. If Tax Exemption is applicable, customer has to provide a copy to WTT of any applicable tax exemption certificates as issued by an approved taxation authority for the specific project location. Without an approved tax exemption certificate received by WTT all submitted invoices will include applicable tax. However we reserve the right to revise our price in case of tax exemption.</p><br>';

				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">12.2. FREIGHT</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">All the Equipment and components foresee Ex-works delivery as per I.C.C. Incoterms-2010.</p><br>';

				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">12.3. INVOICING AND PAYMENT TERMS</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The pricing quoted in this proposal is based on the following payment terms, in principally agreed.<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">(1) 30% Advance Payment along with PO.</p><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">(2) 70% by irrevocable Letter of Credit payable at site.</p><br>Equipment shipment is contingent on receipt of earlier milestone payments.</p><br>';

				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">12.4. EQUIPMENT SHIPMENT</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Client and WTT will arrange a kick off meeting after contract acceptance to develop firm shipment schedule. This estimated delivery schedule assumes no more than 1 week for Client review of submittal drawings. Any delays in Client approvals or requested changes may result in additional charges and/or a delay to the schedule. Material supply for the proposed plant in 3 - 6 months is expected. The delivery schedule excludes the months of August & December, the delivery schedule is subject to review and adjustment. Force majeure clause is applicable. Partial shipments are allowed. In case of modifications to the volume of the supply after the emission of the order confirmation, WTT reserves the right to modify the delivery time and the agreed price.</p><br>';

				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">12.5. PRICING NOTES</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">All prices quoted are in INR. Any applicable tax of destination country is not included. Client will pay all applicable Local, State / Provincial, or Federal taxes & Duties. WTT may manufacture and source the Equipment and any part thereof globally in the country or countries of its choosing, provided that the Equipment complies with all of the requirements specified in this Agreement.<br>The Equipment delivery date, start date, and date of commencement of operations are to be negotiated. Title and risk of loss will transfer upon delivery in accordance with the INCOTERMS 2010. Commercial Terms and Conditions shall be in accordance with WTT’s General Terms and Conditions of Sale as included in Appendix.</p><br>';
				

				vs+='<p style="font-weight:bold;color:#002063;font-family:Roboto;font-size: 20px;">13. Client Scope Of Supply</p><br>';
				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">13.1. SAFETY AND ENVIRONMENTAL</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">First aid, emergency medical response, eyewash & safety showers in the water treatment area. Chemical spill response, security & fire protection systems as per local codes. Environmental use and discharge permits for all chemicals at Client facility either listed in this document or proposed for use at a later date. Any special permits required for WTT’s or Client employees to perform work related to the water treatment system at the facility. All site testing, including soil, ground and surface water, and air emissions, etc. Disposal of all solid & liquid waste from WTT’s system including waste materials generated during construction, startup and operation. <br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Provide appropriate protection of the environment & local community, the health and safety of all workers and visitors at the site and the security of the facility. Provide safety related equipment & services such as site security, fire systems, lifting equipment and its operation, fall protection, adequate floor grating, ventilation, and safe access to equipment & electrical systems areas. </p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Equipment and trained support personnel for any confined space entry required during equipment installation/startup/commissioning/servicing. For permit-required confined space entry, a qualified rescue team on stand-by and available to respond within 4 minutes of an emergency.</p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Client will identify and inform WTT’s personnel of any hazards present in the work place that could impact the delivery of WTT’s scope of supply and agrees to work with WTT to remove, monitor, and control the hazards to a practical level. Client will provide training to WTT’s personnel on all relevant & standard company operating procedures and practices for performing work on site.</p></p><br>';

				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">13.2. JOBSITE AND INSTALLATION REVIEW</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Review of WTT’s supplied equipment drawings and specifications. All easements, licenses and permits required by governmental or regulatory authorities in Connection with the supply, erection and operation of the system.<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Overall plant design, detail drawings of all termination points where WTT’s equipment or Materials tie into equipment or materials supplied by others Stamping, signing or Sealing General drawings as per State, or local regulations or codes.</p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">All applicable civil design and works, including any building, site preparation, grading, excavations, foundations and trenches and accessories. All electrical Labor and supplies leading up to jobsite including fittings, conduit, supports, cable trays, wire and hardware, and air-conditioning of panels as required for installation and ongoing operations. All Labor and supplies leading up to jobsite including fittings, conduit, supports, cable trays, wire and hardware, required to appropriately ground / earth the equipment as required for installation and ongoing operations </p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">All mechanical Labor and supplies leading up to jobsite including interconnecting piping, heat tracing (if required), fittings, conduit, pipe supports, and hardware as required for installation and ongoing operations. All instrumentation and automatic pneumatic valves including but not limited to; air/sample line tubing, fittings, conduit, supports, isolating valves as required for installation and ongoing operations.</p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Loading, unloading and transportation of equipment, materials required for WTT to perform duties outlined in WTT’s Scope of Supply to the jobsite and/or warehouse. </p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Client will provide all access structures (scaffolding), mechanical lifting equipment (cranes, forklifts, scissor lifts, etc.), suitable site/shelter for placement of the proposed equipment, either inside appropriate housing, or outdoors.</p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Precaution: electrical equipment including the PLC may require air-conditioned rooms to prevent overheating of sensitive electronic equipment depending on climatic conditions. Bulk chemical storage and tanks, including secondary containment in accordance with local codes. Client will receive, off-load, log, and store all chemical and materials in accordance with Manufacturer’s recommendation that are shipped.</p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Compressed instrument air for pneumatic valves instruments and ejector system Equipment anchor bolts, Laboratory services, operating and maintenance personnel during equipment checkout, start-up and operation. Any on-site painting or touch-up painting of equipment supplied. Disposal of any Preservative.</p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">For erection, WTT will ship the accessories such as pipes, bolts, nuts, screws, cables, valves etc., in excess quantities than required. This is in order to avoid shortages during the assembly due to damage or any other cause as it is hard to procure the accessories locally. It is notified that all the shipped accessories during assembly and the excess accessories after commissioning are always remain the properties of WTT. WTT has the authority to retake the same at any period of time, even before and after commissioning. It is client’s responsibility to preserve the above mentioned items till WTT takes back the same.</p></p><br>';
				
				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">13.3. START-UP AND COMMISSIONING</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Installation & removal of temporary screens on all process lines Flushing and disinfection of all piping and tanks (including process equipment tanks) and verification of removal of all residual debris from construction. Alignments & required materials for rotating equipment MEG testing of all field motor power wiring (as required). Continuity checks for all electrical field wiring as per Installation Checklist, Hydro-testing of all field installed piping. Supply raw materials, oil/lubricants chemicals and utilities during start-up and operation. Electrical & Mechanical support labor for commissioning activities, loading of membranes, stacks, modules, etc.</p><br>';

				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">13.4. FACILITY MANAGEMENT</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Client will provide such warehouse storage space and facilities, as are available at the site, and are reasonably appropriate to store parts, consumables, tools, etc. in accordance with manufacturer’s recommendations. Such warehouse storage space will be a segregated area, secured and protected from adverse climate as may reasonably be required. The storage area shall be facilitated with 24 hours lock & key with security and Client will be responsible for risk of loss of WTT’s parts while in storage at the site. Client will maintain WTT’s parts stored at the site free & clear of any and all liens of Client and lenders, bondholders, contractors & other creditors of any nature.<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Client will afford WTT’s personnel free access and egress of the facility for all authorized work. Provide workshop facilities/area with roof and stabilized power supply, as is reasonably appropriate to carry out machining/fabrication works.</p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Provide adequate illumination and emergency lighting for all areas in which the WTT will be executing the scope of supply.  Identify a Client project contact person to be available to WTT’s personnel to address any issues related to WTT’s execution of WTT’s scope of work. Responsible for the equipment for movement of chemical drums, totes, and resins, as is reasonable. Provide all site utilities such as raw water, instrument quality air, potable water and power required for operation of the proposed equipment included in this scope of supply.</p></p><br>';

				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">13.5. CONDITIONAL OFFERING</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Client understands that this order confirmation has been issued based upon the information provided by Client and currently available to, WTT at the time of proposal issuance. Any changes or discrepancies in site conditions (including but not limited to system influent characteristics, changes in Environmental Health and Safety (“EH&S”) conditions, and/or newly discovered EH&S concerns), Client financial standing, Client requirements, or any other relevant change, or discrepancy in, the factual basis upon which this proposal was created, may lead to changes in the offering, including but not limited to changes in pricing, warranties, quoted specifications, or terms and conditions. WTT’s offering in this proposal is conditioned upon a full WTT EH&S.</p><br>';

				vs+='<p style="font-weight:bold;color:#002063;font-family:Roboto;font-size: 20px;">14. Appendix</p><br>';
				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">14.1. APPENDIX A: CLARIFICATIONS</p><br>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Delivery terms – Ex works - basis (as per I.C.C. Incoterms-2010)</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Pump MOC has been considered as per WTT standard practice.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>The Equipment in WTT scope will be procured as per WTT Standard Vendor List.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>WTT has not envisaged third party equipment inspection before dispatch.</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>WTT has considered instruments as per WTT standard practice</li></ul>';
				vs+='<ul style="margin-left:30px;font-family:Roboto;font-size: 18px;"><li>Painting specifications of WTT supplied equipment is as per standard manufacturer painting specifications.</li></ul>';

				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">14.2. APPENDIX B:  ACCEPTANCE</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">To ensure accurate and prompt order entry, product delivery, billing and accounts receivables processing, please ensure your Purchase Order contains the complete Client and order details.</p><br>';
				vs+='<br><p style="font-family:Roboto;font-size: 18px;">Please communicate your PO through:</p><br>';
				
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;">';
				vs+='<tr><td style="width:45%">Email</td><td style="width:55%">venkat@wttint.com</td></tr>'
				vs+='<tr><td>Postal Mail:(Indian Office)</td><td>WTT INTERNATIONAL PVT. LTD.<br>No. 3, College cross road<br>Avarangadu, Tiruppur,<br>TamilNadu, INDIA – 641602</td></tr>'
				vs+='</table></center>'

				vs+='<br><br><p style="font-family:Roboto;font-size: 18px;"><b>Bank Account Details:</b></p>';
				vs+='<br><center><table cellpadding="10" cellspacing="10" style="width:100%;">';
				vs+='<tr><td style="text-align:left!important;width:45%">Beneficiary Name</td><td style="text-align:left!important;width:55%">WTT INTERNATIONAL PVT. LTD.,</td></tr>'
				vs+='<tr><td style="text-align:left!important;">Bank Name</td><td style="text-align:left!important;">INDIAN BANK LTD</td></tr>'
				vs+='<tr><td style="text-align:left!important;">Branch Name</td><td style="text-align:left!important;">TIRUPUR MSME BRANCH, TIRUPUR, TAMILNADU</td></tr>'
				vs+='<tr><td style="text-align:left!important;">Account Number OD</td><td style="text-align:left!important;">6475173650</td></tr>'
				vs+='<tr><td style="text-align:left!important;">IFSC Code</td><td style="text-align:left!important;">IDIB000I043</td></tr>'
				vs+='</table></center><br>'

				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">14.3. APPENDIX C:  WARRANTY</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The mechanical warranty is only applicable to equipment supplied by WTT. The mechanical warranty period on all equipment supplied, unless otherwise noted, is twelve (12) months from the date of installation or fourteen (14) months from equipment shipment, whichever occurs first. WTT’s obligation under this warranty is to the repair or replace, of any device or part thereof, which shall prove to have been manufacturing defects.<br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">This warranty excludes the diffuser membranes, electrical items, defects, failures, damages or performance limitations caused in whole or in part by normal wear & tear, power failures, surges, fires, floods, snow, ice, lightning, excessive heat or cold, highly corrosive environments, accidents, actions of third parties, or other events outside of WTT’s control. Warranty period for the entire equipment including replaced or repaired parts will be limited to the unexpired portion of the total warranty period. Bought out components are guaranteed only to the extent of guarantees given to us by our suppliers.</p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">WTT assumes no liability for any damage to equipment caused by inadequate storage or handling as per manufacturer’s recommendations in supplied technical literature, or by defective or sub-standard workmanship or materials provided by Client or any other third party responsible for handling, storing or installing the equipment. Client undertakes to give immediate notice to WTT if goods or performance appear defective and to provide WTT with reasonable opportunity to make inspections and tests. If WTT is not at fault, Client shall pay WTT the costs and expenses of the inspections and tests.</p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">Goods shall not be returned to WTT without WTT’s permission. WTT will provide Client with a “Return Goods Authorization” (RGA) number to use for returned goods. All return costs associated with shipping and labor are not included in the mechanical warranty. WTT warrants, subject to the provisions herein after set forth, that after stable operation of the WTT system has been attained and operators have acquired reasonable skills, the Equipment supplied for this project will be capable of producing the results set forth in stage wise parameter table, provided that:</p><br><p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">The Equipment is operated and maintained at all times in accordance with the WTT Operations and Maintenance manual, The Equipment is operated within the mixed liquor characteristics defined in Influent quality table of this section, WTT has, until performance of its obligation herein is met, reasonable access to the Equipment and the operational data relating thereto, Client furnishes adequate and competent operating, supervisory and maintenance staff, and necessary laboratory facilities with test equipment and personnel, Client utilizes the services of WTT until its performance obligations are met, Client supplies all necessary raw materials and services of a quantity and of a quality specified by WTT, An adequate and continuous power supply is available that will enable operation of all required equipment.</p></p><br>';

				vs+='<p style="margin-left:20px;color:#002063;font-weight:bold;font-family:Roboto;font-size: 18px;">14.4. APPENDIX D:  CONFIDENTIALITY</p><br>';
				vs+='<p style="text-indent:1cm;margin-left:30px;font-family:Roboto;font-size: 18px;">All the details, specifications and drawings submitted by us as a part of the proposal are proprietary in nature and shall not be disclosed by the Client to any third party, for whatever reason, without our written consent.</p><br>';
				vs+='</div></div>'
				// vs+='<footer><p style="font-family:Roboto;font-size: 18px;text-align:right"> '+today2+'/'+frm.doc.project+'/'+country_code+'/'+frm.doc.abbr+'/'+(frm.doc.flow/1000)+'M/U'+frm.doc.unit_code+'/R'+frm.doc.revision_code+'/TCP.</p></footer>'
				var vs_html = '<table class="report-container" style="border:0px">'
				vs_html = '<thead class="report-header"><tr><th style="border:0px"><div class="header-info"><center><img height="90" src="https://erp.wttindia.com/files/wttpng.png" width="60"></center></div></th></tr></thead>'
				vs_html = '<tfoot class="report-footer"><tr><td style="border:0px"><div class="footer-info">'+today2+'/'+frm.doc.project+'/'+country_code+'/'+frm.doc.abbr+'/'+(frm.doc.flow/1000)+'M/U'+frm.doc.unit_code+'/R'+frm.doc.revision_code+'/TCP.</div></td></tr></tfoot>'
				vs_html = '<tbody><tr><td style="border:0px">'+vs+'</td></tr></tbody></table>'
				frm.set_value('template',vs_html);
				frm.refresh_field("template");
	},
	});
}