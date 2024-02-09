frappe.ui.form.on('Proposal', {
	// get_proposal:function(frm){
	// 	var pc=0;
	// 	if(frm.doc.proposal_no!=undefined){
	// 		pc=frm.doc.proposal_no
	// 	}
	// 	var rc=0;
	// 	if(frm.doc.revision!=undefined){
	// 		rc=frm.doc.revision
	// 	}
	// 	frappe.call({
	// 		method:"wtt_module.process_and_costing.doctype.proposal.proposal.get_proposal",
	// 		args:{
	// 			att:frm.doc.attach,
	// 			company:frm.doc.organization,
	// 			client:frm.doc.client_name,
	// 			city:frm.doc.city,
	// 			capacity:frm.doc.capacity
	// 			// prop_cnt:pc,
	// 			// rev_cnt:rc
	// 			},
	// 		callback(r){
	// 			// alert(JSON.stringify(r.message))
	// 			frm.set_value("attach2",r.message[0]);
	// 			frm.refresh_field("attach2")
	// 			frm.set_value("proposal_no",r.message[1]);
	// 			frm.refresh_field("proposal_no");
	// 			frm.set_value("revision",r.message[2]);
	// 			frm.refresh_field("revision");
	// 		}
	// 	});
	// }
});
