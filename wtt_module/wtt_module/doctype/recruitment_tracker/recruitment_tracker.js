// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt
frappe.ui.form.on('Recruitment Tracker', {
	refresh: function(frm) {
		frm.add_custom_button("SEND",()=>{
			frappe.call({
				method:"send_mail",
				doc:frm.doc
			})
		})
		// frm.add_custom_button("Get Recruitment DB",()=>{
		// 	// frappe.call({
		// 	// 	method:"send_mail",
		// 	// 	doc:frm.doc
		// 	// })
		// 	frm.event.get_recruit(frm);
		// })
		frm.add_custom_button(__('Recruitment DB'), () => frm.events.get_recruit(frm),
				__("Get Items From"));
		if(frm.doc.job_applicant)
		{
			frm.add_custom_button("Schedule Interview",()=>{
			frappe.model.open_mapped_doc({
				method: "wtt_module.wtt_module.doctype.recruitment_tracker.recruitment_tracker.schedule_interview",
				frm: frm
			});
			});
		}
	},
	get_recruit:function(frm){
		erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.recruitment_tracker.recruitment_tracker.get_data",
					source_doctype: "Recruitment Database",
					target: frm,
					setters: {
						candidate_name:frm.doc.candidate_name,
						qualification: frm.doc.qualification
					},
					get_query_filters: {
						docstatus: 0
					}
				});
	},
	mail_template:function(frm){
		var htvalue="";
		var datetime=frm.doc.schedule_date+" "+frm.doc.time
		var aa=new Date(datetime)
		const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
		const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
		var hours=aa.getHours()
		var AmorPm = hours >= 12 ? 'PM' : 'AM';
		hours = (hours % 12) || 12;
		var interview_date_and_time=month[aa.getMonth()]+" "+aa.getDate()+", "+aa.getFullYear()+ " "+hours+":"+aa.getMinutes()+" "+AmorPm
		var interview_date=month[aa.getMonth()]+" "+aa.getDate()+", "+aa.getFullYear()
		var interview_time=hours+":"+aa.getMinutes()+" "+AmorPm



		if(frm.doc.mail_template=="Invitation"){
			htvalue+='<h3 style="text-align:center">INTERVIEW INVITATION</h3>'
			htvalue+='<div>Hi '+frm.doc.candidate_name+',<br><p>&nbsp;&nbsp;   This refers to our discussion today regarding your application, we would like to inform you that your application has been shortlisted for further review for the <b>'+frm.doc.applying_for_the_post+'</b> role. Following that, I\'m contacting you to confirm your scheduled interview for the position of <b>'+frm.doc.applying_for_the_post+'</b> at WTT International private limited on '+frm.doc.schedule_date+' '+frm.doc.time+'</div>'
			htvalue+='<br><b>INTERVIEW TYPE</b> : '+frm.doc.interview_type
			htvalue+='<br><br>'
			htvalue+='<u><b>Interviewer Details:</b></u><br><ul><li>• Technical Interview : '+frm.doc.technical_interviewer_name+'</li><li>• Final Interviewer : '+frm.doc.final_interviewer_name+'</li><li>• Interview Duration: 20-45 minutes</li></ul>'
			htvalue+='<u><b>Bring the below documents to the interview;</b></u><br><br><ul><li>1. Updated Resume</li><li>2. Aadhaar card - 1 copy</li><li>2. Passport Size Photo - 1 copy</li><li>4. Salary Proof - 3 months Bank Statement (If you are Experienced)</li><li>5. Experience Certificate (If you are experienced)</li></ul><br>'
			htvalue+='Kindly fill out this application link (<a href="https://erp.wttindia.com/job-application/new">https://erp.wttindia.com/job-application/new</a>) before the interview.<br>'
			htvalue+='<br><u><b>Interview Location:</b></u><br>No 3, College Cross Road, Avarankadu, Tirupur -641602<br><a href="https://goo.gl/maps/ubkY8KguBsofujSk6">https://goo.gl/maps/ubkY8KguBsofujSk6</a>'
			htvalue+='<br><br><b>Who we are;</b><br>Website: <a href="https://www.wttint.com">https://www.wttint.com</a><br>Linkedin: <a href="https://in.linkedin.com/company/wttinternational">https://in.linkedin.com/company/wttinternational</a><br>Youtube: <a href="https://www.youtube.com/@wttinternational5688">https://www.youtube.com/@wttinternational5688</a>'
			htvalue+='<br><br>'
			htvalue+='Best Regards<br>S.Praveen,<br>Assistant Manager - HR'

			// htvalue+='<div><p>Hi <b>'+frm.doc.candidate_name+'</b>,</p><p style="text-indent:70px">Congratulations! Your application has been selected for further review for the <b>'+frm.doc.applying_for_the_post+'</b>. Immediately after, I\'m contacting to confirm your scheduled interview for the position of&nbsp;Management Trainee&nbsp;at WTT International private limited on <b>'+interview_date_and_time+'</b></p>'
			// htvalue+='<p><b>Interview Details:</b></p><p style="text-indent:70px"><b>HR Interview : </b> 15 to 30 Minutes </p><p style="text-indent:70px"><b>Technical Interview : </b> 15 to 30 Minutes</p><p style="text-indent:70px"><b>Tool Test : </b> If applicable (30 to 45 Minutes)</p><p style="text-indent:70px"><b>Final Interview : </b> 15 to 30 Minutes</p>'
			// htvalue+='<p>Bring the below documents to the interview; </p><p style="text-indent:70px">1. Updated Resume</p><p style="text-indent:70px">2. Experience certificate (Photocopies) -if have</p><p style="text-indent:70px">3. Salary Proof (If have) - if have</p><p style="text-indent:70px">4. Passport size&nbsp;photo-1nos</p><p style="text-indent:70px">5. Educational certificate (photocopies)</p>'
			// htvalue+='<p>Before the interview you have to fill this application link (https://erp.wttindia.com/job-app.)</p><p><b>Interview Location : </b> No 3, college cross&nbsp;road, Avarankadu, Tirupur-641602. </p><p>(&nbsp;https://goo.gl/maps/ubkY8KguBsofujSk6&nbsp;)</p><p>If you have any questions about your upcoming&nbsp;interview, please feel free to contact me directly by replying to this email or phoning&nbsp;me at <b>7845009920</b>.</p><p>Please confirm that you have&nbsp;received this email and will be attending the interview.</p><p>Best Regards&nbsp;</p><p>S. Praveen (HR executive)</p></div>'
		}
		else if(frm.doc.mail_template=="Remainder"){
			htvalue+='<div><p>Hello <b>'+frm.doc.candidate_name+'</b>,</p>'
			htvalue+='<p>This is a reminder that our scheduled interview will take place at [https://goo.gl/maps/ubkY8KguBsofujSk6].</p><p>We hope to see you tomorrow at <b>'+interview_time+'</b> to discuss more.</p>';
			htvalue+='<p>If you didn\'t reach out our interview invitation, once kindly check your email.</p><p>Let me know if you need any support by texting/calling this number.Thank you and see you soon!</p>'
			htvalue+='<p>Regards,</p><p>S.Praveen</p><p>7845009920,</p><p>hr@wttindia.com</p>'
		}
		else if(frm.doc.mail_template=="Result"){
			if(frm.doc.status=="Shortlisted"){
				htvalue+='<div><p>Hello <b>'+frm.doc.candidate_name+'</b>,</p>'
				htvalue+='<p>Warm Greeting from WTT International Pvt Ltd, This has reference to your application dated <b>'+interview_date+'</b> for the post of <b>'+frm.doc.applying_for_the_post+'</b> and the subsequent interview you had with us.</p>'
				htvalue+='<p>We are pleased to inform you that you have been shortlisted for the said position ,your offer letter will be sent to your email address soon.</p>'
				htvalue+='<p>Regards,</p><p>S.Praveen (HR Executive)</p>'				
			}
			else if(frm.doc.status=="Rejected"){
				htvalue+='<div><p>Hello <b>'+frm.doc.candidate_name+'</b>,</p>'
				htvalue+='<p>Warm Greeting from WTT International Pvt Ltd, This has reference to your application dated <b>'+interview_date+'</b> for the post of <b>'+frm.doc.applying_for_the_post+'</b> and the subsequent interview you had with us.</p>'
				htvalue+='<p>We are sorry to inform you that your application has not been selected, so we cant process your application further.</p>'
				htvalue+='<p>Regards,</p><p>S.Praveen (HR Executive)</p>'
			}
			else if(frm.doc.status=="Hold"){
				htvalue+='<div><p>Hello <b>'+frm.doc.candidate_name+'</b>,</p>'
				htvalue+='<p>Warm Greeting from WTT International Pvt Ltd, This has reference to your application dated <b>'+interview_date+'</b> for the post of <b>'+frm.doc.applying_for_the_post+'</b> and the subsequent interview you had with us.</p>'
				htvalue+='<p>We are sorry to inform you that your application has been hold, we will contact you shortly in future period.</p>'
				htvalue+='<p>Regards,</p><p>S.Praveen (HR Executive)</p>'
			}
			else if(frm.doc.status==undefined){
				msgprint("Interview Status is Required to Send Mail")
			}
		}
		frm.set_value('message',htvalue);
		frm.refresh_field('message');
	},
	create_job_applicant:function(frm)
	{
		frappe.call({
				method:"create_job_applicant",
				doc:frm.doc
		})
	}
});
