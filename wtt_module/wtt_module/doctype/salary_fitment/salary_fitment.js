// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Fitment', {
	setup: function(frm) {
		frm.set_query("revised_from", function() {
			return {
				filters: [
					["Salary Fitment","docstatus","=", 1],
					["Salary Fitment","employee_name","=", frm.doc.employee_name]

				]
			}
		});
	},
	refresh:function(frm){
		if (frm.doc.docstatus===1){
			if(frappe.session.user=='venkat@wttindia.com' || frappe.session.user=='sarnita@wttindia.com' || frappe.session.user=='Administrator')
			{
			frm.add_custom_button(__('Revised'), () => {
			frappe.call({
			method: 'wtt_module.wtt_module.doctype.salary_fitment.salary_fitment.revision',
			args: { name: frm.doc.name },
				callback(r) {
					if (!r.exc) {
						frm.reload_doc();
					}
				}
			});	
			});
			}
		}
	},
	calculate:function(frm,cdt,cdn){
		var gross=frm.doc.gross
		var bs=gross*0.25;
		var hra=bs*0.4
		var oa=gross-(bs+hra)
		if(frm.doc.hra!=1){oa=gross-bs;hra=0}

		// earnings and deduction calculation
		frm.clear_table("earnings");
		frm.clear_table("deduction");
		var child=frm.add_child("earnings");
		frappe.model.set_value(child.doctype,child.name,"salary_component","Basic Salary");
		frappe.model.set_value(child.doctype,child.name,"amount",bs);
		if(hra>0){
			var child=frm.add_child("earnings");
			frappe.model.set_value(child.doctype,child.name,"salary_component","House Rent Allowance");
			frappe.model.set_value(child.doctype,child.name,"amount",hra);
		}
		var child=frm.add_child("earnings");
		frappe.model.set_value(child.doctype,child.name,"salary_component","Other Allowance");
		frappe.model.set_value(child.doctype,child.name,"amount",oa);
		
		frm.refresh_field("earnings");

		var esi=0;
		var pf=0;
		var esi2=0;
		var pf2=0;
		if(frm.doc.esi==1){
			if(gross<=21000){
				esi=gross*0.75/100
				esi2=gross*3.25/100
			}
		}
		if(frm.doc.pf==1){
			if(bs+oa>15000){
				pf=15000*12/100
				pf2=15000*13/100
			}
			else{
				pf=(bs+oa)*12/100
				pf2=(bs+oa)*13/100
			}
		}

		var tab=frm.add_child("deduction");
		frappe.model.set_value(tab.doctype,tab.name,"salary_component","Provident Fund");
		frappe.model.set_value(tab.doctype,tab.name,"amount",pf);
		var tab=frm.add_child("deduction");
		frappe.model.set_value(tab.doctype,tab.name,"salary_component","ESI");
		frappe.model.set_value(tab.doctype,tab.name,"amount",esi);
		frm.refresh_field("deduction");

		frm.set_value("earnings_total",bs+hra+oa);frm.refresh_field("earnings_total");
		frm.set_value("deductions_total",esi+pf);frm.refresh_field("deductions_total");
		frm.set_value("take_home",frm.doc.earnings_total-frm.doc.deductions_total);frm.refresh_field("take_home");

		// bonus,gratuity,ctc,otherallowance calculation
		var bonus = bs*0.0833
		var gratuity = bs*0.0481
		frm.set_value("bonus",bonus);frm.refresh_field("bonus");
		frm.set_value("gratuity",gratuity);frm.refresh_field("gratuity");
		frm.set_value("esi_employer_contribution",esi2);frm.refresh_field("esi_employer_contribution");
		frm.set_value("pf_employer_contribution",pf2);frm.refresh_field("pf_employer_contribution");

		var other_allowance=0
		if(esi>0){
			if(frm.doc.location=="HEAD OFFICE"){
	        	other_allowance=2300
	        	if(frm.doc.eligible_for_shoe_allowance)
	        	{
	        		other_allowance=other_allowance+400
	        	}
	        }
	        else if(frm.doc.location=="WORKSHOP"){
	        	other_allowance=2300
	        	if(frm.doc.eligible_for_shoe_allowance)
	        	{
	        		other_allowance=other_allowance+400
	        	}
	        }
		}
		else{
			if(frm.doc.location=="HEAD OFFICE"){
	        	other_allowance=5000
	        	if(frm.doc.eligible_for_shoe_allowance)
	        	{
	        		other_allowance=other_allowance+400
	        	}
	        }
	        else if(frm.doc.location=="WORKSHOP"){
	        	other_allowance=5000
	        	if(frm.doc.eligible_for_shoe_allowance)
	        	{
	        		other_allowance=other_allowance+400
	        	}
	        }
		}
	    frm.set_value("other_allowance",other_allowance);frm.refresh_field("other_allowance");

	    frm.set_value("total_b",(frm.doc.bonus * 12) + (frm.doc.gratuity * 12) + (frm.doc.esi_employer_contribution * 12) + (frm.doc.pf_employer_contribution * 12) + frm.doc.other_allowance);
	    frm.refresh_field("total_b");

	    var ctc=gross+esi2+pf2+(other_allowance/12)+bonus+gratuity;
	    frm.set_value("cost_to_company",ctc);frm.refresh_field("cost_to_company");

	}

});
