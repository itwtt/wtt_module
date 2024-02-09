// Copyright (c) 2021, wtt_custom and contributors
// For license information, please see license.txt

frappe.ui.form.on('Registration Form', {
	job_status:function(frm){
		if(frm.doc.job_status=='Shortlisted'){
			var ht='3,COLLEGE CROSS ROAD,AVARANKADU\nTIRUPUR\nPIN: 641602\nIndia'
			frm.set_value('location',ht)
		}
	},
	send_mail:function(frm){

		frm.set_value('template',"")
		var htvalue=""
		if(frm.doc.job_status=='Shortlisted'){
			// htvalue+='<h2 style="text-align:center"><u>Interview Confirmation Mail</u></h2>'
			// htvalue+='<br><br><b>Subject line:</b> Interview confirmation with <b>WTT INTERNATIONAL PVT LTD</b> for the <b>'+frm.doc.applying_for_the_post+'</b> position'
			// htvalue+='<br><br>Dear <b>'+frm.doc.name1+'</b>'
			// htvalue+='<br><br><p style="text-indent:70px">I am emailing to confirm your upcoming interview for the <b>'+frm.doc.applying_for_the_post+'</b> position at <b>WTT INTERNATIONAL PVT LTD</b> on '+frm.doc.interview_date+' '+frm.doc.time+'. At this meeting, your interviewer will have a chance to [discuss your skills further/ administer a written test/ review your assignment]. Please find the details of your interview below:'
			// htvalue+='<br><br><b>When:</b> '+frm.doc.interview_date+' '+frm.doc.time+'.'
			// htvalue+='<br><br><b>Where: WTT INTERNATIONAL PVT LTD</b>,No.3, College Cross road, Tirupur - 641602,Tamilnadu .'
			// // htvalue+='<br><br><b>Interviewer:</b> '+frm.doc.manager_name
			// htvalue+='<br><br>If you will be driving, you can find parking [give details on visitor parking]. When you arrive, [provide information on how visitors can enter the building, eg head to the front desk and show the receptionist your ID].'
			// htvalue+='<br><br>If you have any questions about your upcoming interview, please contact me directly by replying to this email or by phoning me at <b>[Phone Number]</b>.'
			// htvalue+='<br><br>Please confirm that you have received this email and will be attending the interview.'
			// htvalue+='<br><br>We are looking forward to meeting with you.'
			// htvalue+='<br><p style="text-align:right;">Regards,'
			// htvalue+='<br><br><p style="text-align:right;"><b>HR Manager - WTT</b>'
			// htvalue+='<br><p style="text-align:right;">**</p>'
			htvalue+='Dear <b>'+frm.doc.name1+'</b>'
			htvalue+='<br><br>Thank you for having interest in working at WTT International Pvt. Ltd.'
			htvalue+='<br>Your profile has been shortlisted for <b>'+frm.doc.applying_for_the_post+'</b> position, and wish you all the best for hiring.'
			htvalue+='<br><p style="text-align:right;">Regards,'
			htvalue+='<br><p style="text-align:right;"><b>HR Manager - WTT</b>'
	
		}
		else if(frm.doc.job_status=='Contacted'){
			htvalue+='<br><br>Dear <b>'+frm.doc.name1+'</b>'
			htvalue+='<br><br>Thank you for interest in working at <b>WTT INNTERNATIONAL PVT. LTD</b>.'
			htvalue+='<br>I would like to discuss your application for the '+frm.doc.applying_for_the_post+' role and tell you more about WTT INTERNATIONAL PVT.LTD.'
			htvalue+='<br>Would you be available for a short introductory phone call '+frm.doc.interview_date+' '+frm.doc.time+'.or [ALTERNATIVE TIMESLOT]?'
			htvalue+='<br>Looking forward to hearing from you,'
			htvalue+='<br><p style="text-align:right;">Regards,'
			htvalue+='<br><p style="text-align:right;"><b>HR Manager - WTT</b>'
		}

		frm.set_value('template',htvalue);
		frm.refresh_field('template');
	}
	// refresh: function(frm) {

	// }
});
