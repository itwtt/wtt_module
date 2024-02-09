// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('HR Templates', {
	setup: function(frm) {
		frm.set_query("hr_manager", function() {
			return {
				filters: [
					["Employee","department","in", ["Human Resources - WTT","Hr & Admin - WTT"]],
					["Employee","status","=","Active"] 
				]
			}
		});
	},

	refresh: function(frm,cdt,cdn) {
		frm.add_custom_button(__('Job App'),
			function() {
				erpnext.utils.map_current_doc({
					method: "wtt_module.wtt_module.doctype.hr_templates.hr_templates.get_candidate",
					source_doctype: "Job App",
					target: frm,
					setters: {
						applicant_name:frm.doc.applicant_name,
						company: frm.doc.company
					},
					get_query_filters: {
						company: frm.doc.company
					}
				})
		});
	},
	module:function(frm){
		if(frm.doc.module!='Recruitment'){
			frm.set_value('template',"");
			frm.refresh_field('template');
		}
	},
	get_template:function(frm){
		var post=""
		if(frm.doc.position=='OTHERS'){
			post=frm.doc.position_name
		}
		else{
			post+=post
		}

	if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Acknowledgement'){
		var htvalue='<h2 style="text-align:center"><u>Application acknowledgement email template</u></h2><br><br>'
		htvalue+='Dear <b>'+frm.doc.candidate_name+',</b><br>'
		htvalue+='<p style="text-indent: 100px;">Thank you very much for applying for <b>'+post+'</b> position at <b>WTT INTERNATIONAL PVT LTD.</b> I will be reviewing your application along with the others that we have received in the next couple of days. If you are selected for the next phase of the recruitment process, you will be contacted for an interview session.We appreciate your interest in our company and wish you the very best in this selection process.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerly,<br><b>'+frm.doc.hr_name+'</b><br>Head of human Resource'
		
		}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Intake meeting to Hiring Manager'){
		var htvalue='<h2 style="text-align:center"><u>Request for an Intake Meeting</u></h2><br><br>'
		htvalue+='<b>Subject line</b>: Intake meeting about <b>'+post+'</b> position / Let’s discuss <b>'+post+'</b> position'
		htvalue+='<br><br>Hi <b>'+frm.doc.manager_name+',</b><br>'
		htvalue+='<p style="text-indent:100px">I’d like to schedule a meeting so that we discuss requirements and candidate profiles for the <b>'+post+'</b> role we’re about to open. </p>'
		htvalue+='<br><p style="text-indent:100px">Before this meeting, could you have a think on the basics of the open role and the hiring process? For example, here’s some information I’ll need :<p>'
		htvalue+='<br><p style="text-indent:100px"><ul><li>Employment type (full-time or part-time, permanent or fixed-term contract)</li><li>Salary range</li><li>Job duties (five to ten regular tasks)</li><li>Requirements (including relevant experience and knowledge of specific tools)</li><li>Evaluation methods (like screening calls, assignments and online tests)</li><li>Timeline (ideal start date)</li></ul></p>'
		htvalue+='<br><p>Also, if you have specific people in mind that would be good candidates (like internal candidates or past applicants), let me know in this meeting so I can reach out as soon as possible.</p>'
		htvalue+='<br><p>To start you off, I’m attaching a job description template [that we’ve used in the past for a similar position]. You can tweak, remove and add job duties and requirements. Or we can review it together during the meeting if you like.</p>'
		htvalue+='<br><ul><li>[Tuesday, 10-11 a.m.]</li><li>[Tuesday, 2-3 p.m.]</li><li>[Wednesday, 1:30-2:30 p.m.]</li></ul>'
		htvalue+='<br><p.If none of these time slots work for you, let me know when you’ll be available and we can find a time that works. [Also, if you think that it’d be helpful if someone else form the hiring team joins this meeting, please let me know.]</p>'
		htvalue+='<br><p style="text-align:center;"><br>Thank you,'
		htvalue+='<br><p style="text-align:right;"><br><b>'+frm.doc.hr_name+'</b><br>'
		
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Successful Candidate'){
		var htvalue='<h2 style="text-align:center"><u>Email to successful candidate after interview</u></h2><br><br>'
		htvalue+='<b>Subject line:</b> Your interview with <b>WTT INTERNATIONAL PVT LTD</b> for the <b>'+post+'</b> position.'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><p style="text-indent:100px">Thank you very much for meeting with us to talk about the open <b>'+post+'</b> position. It was a pleasure getting to know you. We have finished conducting our interviews.'
		htvalue+='<br><br>On behalf of <b>WTT INTERNATIONAL PVT LTD</b>, I am delighted to inform you that we have determined that you are the best candidate for this position.'
		htvalue+='<br><br>We would like to invite you to a meeting with our CEO to further discuss the details of the position. You will be able to ask any questions you may have about the job and job duties.'
		htvalue+='<br><br>I am looking forward to your response,'
		htvalue+='<br><p style="text-align:right;"><br>Regards,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">**</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Assignment'){
		if(frm.doc.assignment=='Send a Task'){
		var htvalue='<h2 style="text-align:center"><u>ASSIGNMENT FOR '+post+' POSITION</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br>Thank you again for applying for <b>'+post+'</b> position. As a part of our selection process, we send assignments to selected candidates, and you are one of them!'
		htvalue+='<br><br>In the attachment, you will find the assignment itself as well as detailed instructions about how to complete the assignment. Please make sure to read all the instructions as they will help you complete the assignment more successfully.'
		htvalue+='<br><br>In this assignment, there are no right or wrong answers. The assignment mostly consists of situations relevant to <b>'+post+'</b> position, and we want to evaluate you skills and behaviour when facing situations like that.'
		htvalue+='<br><br>The due date to return the assignment is <b>dd/mm/yyyy</b>'
		htvalue+="<br><br>If you have any other questions about the assignment, please don't hesitate to ask!"
		htvalue+='<br><br>Good luck with the assignment, and I am looking forward to reading your answers,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">**</p>'
		}
		else if(frm.doc.assignment=='Task Received'){
		var htvalue='<h2 style="text-align:center"><u>Your Assignment has been Received</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:100px">Thank you for completing and sending over the assignment. Our <b>**departmentname**</b> team will review and evaluate your answers. After that, we will get back to you with detailed feedback and any further information we may have.</p>'
		htvalue+="<br><br>Enjoy the rest of your day, and please don't hesitate to ask any questions you may have!"
		htvalue+='<br><br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">**</p>'
		}
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Update to Hiring Manager'){
		var htvalue='<h2 style="text-align:center"><u>Hiring Update</u></h2>'
		htvalue+='<br><br>Hi <b>'+frm.doc.manager_name+'</b>,'
		htvalue+='<br><br><p>I’m sending you an update on where we stand with the <b>'+post+'</b> Role:'
		htvalue+='<br><br><ul><li><b>Number of phone screening calls conducted:</b> **</li>'
		htvalue+='<li><b>Number of applicants we advanced to the assignment phase:</b> **</li>'
		htvalue+='<li><b>Number of phone screening calls scheduled for next week:</b> **</li>'
		htvalue+='<li><b>Deadline for assignment submission:</b> [e.g. 6/20/2017]</li></ul>'
		htvalue+='<br><br>Here’s an overview of the qualified candidates:'
		htvalue+='<br><br><ul><li><b>[Candidate1_name]:</b> Doesn’t have relevant experience, but has researched our company and is genuinely interested in the role. We had a very pleasant discussion and I would like to see the assignment results.</li>'
		htvalue+='<li><b>[Candidate2_name]:</b> Has two years of work experience in a similar role and knows a lot about the industry. The tone of our discussion was formal.</li></ul>'
		htvalue+='<br><br>For more detailed information, feel free to refer to my notes [attach file to email.]'
		htvalue+='<br><br>Please let me know if you need more information. We can schedule a quick [e.g. call or meeting] to follow up.'
		htvalue+='<br><br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">**</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Interview Cancellation'){
		var htvalue='<h2 style="text-align:center"><u>Interview Cancellation Mail</u></h2>'
		htvalue+='<br><br><b>Subject line:</b> Information regarding interview cancellation for the post of <b>'+post+'</b>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br><p style="text-indent:70px">I would very sadly here to inform you that the interview session organised for the post of <b>'+post+'</b> on **(mention the date)** at **(mention the time and place)** is been cancelled for a reason (mention and explain the complete reason e.g. the opening for the requirement of scheduled post is been closed by the higher authorities of the company, any sudden event is being organised by the company and at busy schedule of all the responsible officers interview is been rescheduled etc.). Our company (company name) always respect the talented person and we assure to be with you in any of the suitable further openings.<p>'
		htvalue+='<br><br>Thank you for investing your valuable time for applying for the post of <b>'+post+'</b> in our company <b>WTT INTERNATIONAL PVT LTD.</b>'
		htvalue+='<br><br>Thank you and Have a great Day'
		htvalue+='<br><br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">**</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Interview Confirmation'){
		var htvalue='<h2 style="text-align:center"><u>Interview Confirmation Mail</u></h2>'
		htvalue+='<br><br><b>Subject line:</b> Interview confirmation with <b>WTT INTERNATIONAL PVT LTD</b> for the <b>'+post+'</b> position'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br><p style="text-indent:70px">I am emailing to confirm your upcoming interview for the <b>'+post+'</b> position at <b>WTT INTERNATIONAL PVT LTD</b> on *[date]* at *[Time]*. At this meeting, your interviewer <b>'+frm.doc.manager_name+'</b> will have a chance to [discuss your skills further/ administer a written test/ review your assignment]. Please find the details of your interview below:'
		htvalue+='<br><br><b>When:</b> **[Date and Time, eg Monday, May 27th, at 2:30pm]**. The estimated duration is **[give an estimated length of interview]**.'
		htvalue+='<br><br><b>Where: WTT INTERNATIONAL PVT LTD</b>,No.3, College Cross road, Tirupur - 641602,Tamilnadu .'
		htvalue+='<br><br><b>Interviewer:</b> '+frm.doc.manager_name
		htvalue+='<br><br>If you will be driving, you can find parking [give details on visitor parking]. When you arrive, [provide information on how visitors can enter the building, eg head to the front desk and show the receptionist your ID].'
		htvalue+='<br><br>If you have any questions about your upcoming interview, please contact me directly by replying to this email or by phoning me at <b>[Phone Number]</b>.'
		htvalue+='<br><br>Please confirm that you have received this email and will be attending the interview.'
		htvalue+='<br><br>We are looking forward to meeting with you.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">**</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='No Show'){
		var htvalue='<h2 style="text-align:center"><u>Interview No-Show Mail</u></h2>'
		htvalue+='<br><br><b>Subject:</b> Interview for <b>'+post+'</b> position at <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>Our <b>*[interview/phone conversation/video call]*</b> was scheduled for today at <b>*[time, eg 2pm]*</b> but I didn’t hear from you. I hope you are well.'
		htvalue+='<br><br>At your earliest convenience could you please let me know if you are still interested in the <b>'+post+'</b> position? If you are, we can reschedule the interview. If not, I can delete your application.'
		htvalue+='<br><br>Thanks again for your interest in working at <b>WTT INTERNATIONAL PVT LTD.</b>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">**</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Interview remainder'){
		var htvalue='<h2 style="text-align:center"><u>Interview Remainder</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>I wanted to remind you of your scheduled interview for the <b>'+post+'</b> role at <b>WTT INTERNATIONAL PVT LTD</b> on <b>*Date*</b> at <b>*Time*</b>.'
		htvalue+='<br><br>Your interviewer, <b>'+frm.doc.manager_name+'</b>, is looking forward to hearing about how your {skill 1 or qualification 1} and {skill 2 or qualification 2} would make you a great fit for the position.'
		htvalue+='<br><br>Please find a summary of some important interview details below as well as a bit more information about our organization.'
		htvalue+='<br><br>Key Interview Details<ol><li>Role: <b>'+post+'</b></li><li>Date: </li> <li>Start Time: </li><li>End Time: </li></ol>'
		htvalue+='<br><br>Location:  WTT INTERNATIONAL PVT LTD</b>,No.3, College Cross road, Tirupur - 641602,Tamilnadu . <br>Interviewer Details: <b>'+frm.doc.manager_name+'</b>, {Interviewer Job Title}'
		htvalue+='<br><br>I recommend arriving 10 minutes prior to your interview, so you give yourself adequate time to check in at reception. Don’t forget, our office attire must be <b>Formal</b>.'
		htvalue+='<br><br>About <b>WTT INTERNATIONAL PVT LTD</b><br><ol><li>*two sentence</li><li>about WTT*</li></ol>'
		htvalue+='<br><br>Please confirm that you received this message and that we can expect to see you at the interview.<br><br>We’re very much looking forward to meeting you in person.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">**</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Phone interview Confirmation'){
		var htvalue='<h2 style="text-align:center"><u>Phone Interview Confirmation</u></h2>'
		htvalue+='<br><br><b>Subject:</b>  Phone Interview Confirmation for the post of <b>'+post+'</b> at <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>Thank you very much for the invitation to interview for the <b>'+post+'</b>. I appreciate the opportunity, and I look forward to a telephonic meeting with <b>'+frm.doc.manager_name+'</b> on <b>*date*</b> at <b>*time*</b> estimated interview time may be 30 minutes.'
		htvalue+='<br><br><p style="text-align:left;"><b>Name: </b>'+frm.doc.manager_name
		htvalue+='<br><p style="text-align:left;"><b>I will call on:</b>'
		htvalue+='<br><p style="text-align:left;"><b>Job Title: </b></p>'
		htvalue+='<br>If you need with any further information prior to the interview, please let me know.'
		htvalue+='<br><p style="text-align:right;">Best Regards,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;"><b>*mail*</b>'
		htvalue+='<br><p style="text-align:right;">*Ph.No*</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Phone Interview Email'){
		var htvalue='<h2 style="text-align:center"><u>Phone Interview Schedule</u></h2>'
		htvalue+='<br><br>Subject line: Invitation for a phone interview with WTT INTERNATIONAL PVT LTD'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>Firstly, I want to thank you again for applying for <b>'+post+'</b> role with us.'
		htvalue+='<br><br>Also, I would like to inform you that, after reviewing your application, we have selected you for the next round, which is a phone interview.'
		htvalue+='<br><br>The main purpose of this phone interview is for us to get to know you better, and for you to ask any questions you may have.'
		htvalue+='<br><br>Are you available for a short phone call? It will not take longer than *[X minutes]*.'
		htvalue+='<br><br>Here are a few options I have available:<br><ul><li>[Monday, date, time]</li><li>[Tuesday, date, time]</li><li>[Wednesday, date, time]</li><li>[Thursday, date, time]</li><li>[Friday, date, time]</li></ul>'
		htvalue+='<br><br>If none of these options work for you, please let me know and I will give my best to adjust.'
		htvalue+='<br><br>Please send me a confirmation email with the chosen time as well as your phone number.'
		htvalue+='<br><br>I am looking forward to get to know you better,'
		htvalue+='<br><p style="text-align:right;">Best Regards,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Reschedule Interview'){
		var htvalue='<h2 style="text-align:center"><u>Interview Rescheduled</u></h2>'
		htvalue+='<br><br>Subject line: Rescheduling your Interview at WTT INTERNATIONAL PVT LTD for <b>'+post+'</b>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>I’m writing to inform you that, unfortunately, we will need to reschedule our interview for the open '+post+' position that we had set up for *[Date and Time of Interview, eg. August 29th at 11:15 a.m.]*.'
		htvalue+='<br><br>[Briefly discuss why you need to reschedule, eg. Due to a serious family illness, our hiring manager [Hiring Manager Name] will be unavailable for some time.]'
		htvalue+='<br><br>[Suggest a possible date and time for the interview, or let the candidate know when they will hear back from you, eg. As we are currently unaware when our hiring manager will be back to work, I am unable to suggest a possible date and time for your interview. We expect to hear back from her in the next few days, and I will reach out to you personally with the updated information so that we can select a date and time for you to come into the office.]'
		htvalue+='<br><br>Please accept my sincerest apologies for the delay and any inconvenience. If you have any questions at all, don’t hesitate to reach out to me via [email/phone].'
		htvalue+='<br><br><p style="text-align:center;">Thank you for your patience,</p>'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Scheduling Interview'){
		var htvalue='<h2 style="text-align:center"><u>Scheduled Interview</u></h2>'
		htvalue+='<br><br>Subject line: Invitation to Interview - <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>Thank you for applying to WTT INTERNATIONAL PVT LTD.'
		htvalue+='<br><br>Your application for the <b>'+post+'</b> position stood out to us and we would like to invite you for an interview at our office[s] to get to know you a bit better.'
		htvalue+='<br><br>You will meet with the <b>*[Department_name]*</b> department manager. The interview will last about *[X]* minutes and you’ll have the chance to discuss the <b>'+post+'</b> position and learn more about our company. [If applicable: Insert information about what the candidate might need to bring with them e.g. ID to pass from the security/reception, resume or portfolio.]'
		htvalue+='<br><br>Would you be available on *[date and time - or, range of dates/times]?*'
		htvalue+='<br><br>Looking forward to hearing from you,'
		htvalue+='<br><br>All the best / Kind regards,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Second Interview Confirmation'){
		var htvalue='<h2 style="text-align:center"><u>Second Interview Confirmation</u></h2>'
		htvalue+='<br><br><b>Subject line:</b> Invitation to Second Interview - <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>I am reaching back to you happy to inform you that you have been selected for the second interview for <b>'+post+'</b> position.'
		htvalue+='<br><br>After the first interview, we got the chance to know you better, and understand your characteristics, goals and ambitious.'
		htvalue+='<br><br>We would like to meet with you one more time in order to make sure that this role would be a good fit for you.'
		htvalue+='<br><br>In case that you accept this invitation, you will meet with *[position, name]*. The interview will take up to *[X minutes]*'
		htvalue+='<br><br>Here are a few options I have available:<br><ul><li>[Monday, date, time]</li><li>[Tuesday, date, time]</li><li>[Wednesday, date, time]</li><li>[Thursday, date, time]</li><li>[Friday, date, time]</li></ul>'
		htvalue+='<br><br>If none of these options work for you, please let me know and I will give my best to adjust.'
		htvalue+='<br><br>We can’t wait to meet with you again,'		
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Second Interview Email'){
		var htvalue='<h2 style="text-align:center"><u>Second Interview Email</u></h2>'
		htvalue+='<br><br><b>Subject line: </b>Invitation to second interview with <b>WTT INTERNATIONAL PVT LTD</b> for the open <b>'+post+'</b> position.</b>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>Thank you for taking the time to discuss the <b>'+post+'</b> role with us at your interview on *[Date of First Interview]*. We enjoyed getting to know you and learning more about your skills. [Personalize this with information from the first interview, e.g. Especially impressive was your time spent working for Google and the projects you participated in while working there.] We would like to invite you back for a second interview.'
		htvalue+='<br><br>This interview would be with <b>'+frm.doc.manager_name+'</b>, our <b>'+frm.doc.designation+'</b>. [Briefly discuss the purpose of the second interview, e.g. We’d like you to take a short test, then we will be going over your score.] We expect the whole interview to take [length of time, e.g. 30 minutes]. '
		htvalue+='<br><br>Are you available to come into our office at WTT INTERNATIONAL PVT LTD</b>,No.3, College Cross road, Tirupur - 641602,Tamilnadu on *[Date and Time, e.g. Monday Oct 7th at 10:45am]*, or between *[range of dates or times, e.g. June 8th-11th in the mornings]?* Let me know if another date or time would work better for you. '
		htvalue+='<br><br>Please remember to bring your ID to this interview. When you arrive you’ll need to show it at the reception desk.'
		htvalue+='<br><br>Looking forward to seeing you again,'	
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Skype Invitation'){
		var htvalue='<h2 style="text-align:center"><u>Skype Invitation</u></h2>'
		htvalue+='<br><br>Subject line: Invitation for Skype interview with WTT INTERNATIONAL PVT LTD'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>Firstly, I want to thank you for applying for <b>'+post+'</b> role with us.'
		htvalue+='<br><br>Also, I would like to inform you that, after reviewing your application, we have selected you for the next round, which is an interview via Skype.'
		htvalue+='<br><br>The main purpose of this Skype interview is for me to get to know you better, and for you to ask any questions you may have.'
		htvalue+='<br><br>Are you available for a short Skype call? It will not take longer than *[X minutes]*.'
		htvalue+='<br><br>Here are a few options I have available:<br><ul><li>[Monday, date, time]</li><li>[Tuesday, date, time]</li><li>[Wednesday, date, time]</li><li>[Thursday, date, time]</li><li>[Friday, date, time]</li></ul>'
		htvalue+='<br><br>If none of these options work for you, please let me know and I will give my best to adjust.'
		htvalue+='<br><br>Please send me a confirmation email with the chosen time as well as your Skype name.'
		htvalue+='<br><br>I am looking forward to get to know you better,'
		htvalue+='<br><p style="text-align:right;">Kind Regards,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Video Call Interview'){
		var htvalue='<h2 style="text-align:center"><u>Video interview</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>Thank you for your application for the position of <b>'+post+'</b>.'
		htvalue+='<br><br>At <b>WTT INTERNATIONAL PVT LTD</b>, we’re looking for dedicated, motivated and hardworking people to join our team. We take pride in the culture we have created and we look for people who will join us in achieving our vision. We look for the following things:'
		htvalue+='<br><br><ul><li>What you are looking for in an employer</li><li>How your personality will fit in with the team and if you’ll be happy in this working environment</li><li>If you are looking to grow with a business and go the extra mile</li></ul>'
		htvalue+='<br><br>With that in mind, we’d love to get to know a bit more about you. We’d like to invite you to complete a profile) one-way video introduction and interview on (date) at (Time).'
		htvalue+='<br><br>Are you available for a short video call? It will not take longer than *[X minutes]*.'
		htvalue+='<br><br>Here are a few options I have available:<br><ul><li>[Monday, date, time]</li><li>[Tuesday, date, time]</li><li>[Wednesday, date, time]</li><li>[Thursday, date, time]</li><li>[Friday, date, time]</li></ul>'
		htvalue+='<br><br>If none of these options work for you, please let me know and I will give my best to adjust.'
		htvalue+='<br><br>I really look forward to meeting you. Please let me know as soon as possible if you have any queries.'
		htvalue+='<br><p style="text-align:right;">Kind Regards,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'		
	}
	else if(frm.doc.template=='Job Interview' && frm.doc.subject1=='Text Messages'){
		var htvalue='<h2 style="text-align:center"><u>Text Message Template</u></h2>'
		htvalue+='<br><br><b>To get a hold of the candidate, plain and simple</b>'
		htvalue+='<br><br><b>'+frm.doc.candidate_name+'</b>, are you interested in the <b>'+post+'</b> role with <b>WTT INTERNATIONAL PVT LTD</b>?'
		htvalue+='<br><br><b>To schedule a call or interview. For example:</b>'
		htvalue+='<br><br>Hi <b>'+frm.doc.candidate_name+'</b>, are you free <DATE> at <TIME> for an interview at our offices at  <b>WTT INTERNATIONAL PVT LTD</b>,No.3, College Cross road, Tirupur - 641602,Tamilnadu?'
		htvalue+='<br><br><b>To confirm interviews. For example:</b>'
		htvalue+='<br><br><b>'+frm.doc.candidate_name+'</b>, you have an interview with <b>'+frm.doc.candidate_name+'</b> on <DATE> at <TIME>. Can you confirm that still works for you? A YES or NO will do!'
		htvalue+='<br><br><b>To share just-in-time information, such as directions to your office on the morning of their job interview. For example:</b>'
		htvalue+='<br><br><b>'+frm.doc.candidate_name+'</b>, we’re looking forward to meeting you this morning! To help you find your way, here are directions to our office: <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+='<br><br><b>To follow up with candidates and ask for their feedback. For example:</b>'
		htvalue+='<br><br>Hi <b>'+frm.doc.candidate_name+'</b>. Thanks for spending the time letting us get to know you – we’d love to hear your feedback: <SURVEY URL>.'
		htvalue+='<br><br><b>To qualify candidates with simple screening questions. For example</b>'
		htvalue+='<br><br>Do you have at least 1 year’s experience working in an Agile development environment?'
		htvalue+='<br><br><b>To answer candidate questions. For example:</b>'
		htvalue+='<br><br>Hi <b>'+frm.doc.candidate_name+'</b>, the benefits package does include a monthly transit pass.'
		htvalue+='<br><br><b>To ask contacts for referrals. For example:</b>'
		htvalue+='<br><br>Hi <b>'+frm.doc.candidate_name+'</b>, do you know any colleagues who might be interested in <b>'+post+'</b> with <b>WTT INTERNATIONAL PVT LTD</b> in No.3, College Cross road, Tirupur - 641602? We offer a referral award – so do let me know.'
		htvalue+='<br><br><b>When you haven’t asked their permission.</b><br><br>May I text you at <PHONE #> with further questions or updates?'
		htvalue+='<br><br><b>When sharing complex information.</b><br><br>You can read the details of the benefits package here: <URL>'
	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Background Verification'){
		var htvalue='<h2 style="text-align:center"><u>Background Verification</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>I hope all is well with you. I wanted to check in and let you know we *[haven’t gotten the results of your background check from X yet / haven’t reviewed your background check yet]*. We are expecting to finish with the process by the end of the week. I will contact you again as soon as I have any news.'
		htvalue+='<br><br>In the meantime, feel free to reach me via email or at [phone number], if you have any questions.'
		htvalue+='<br><br>All the best / Kind regards,'		
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'		

	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Contract Employee'){
		var arr=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		var htvalue='<h2 style="text-align:center"><u>Contract Employee Offer Letter</u></h2>'
		htvalue+='<br><br>REF NO: WTT INTERNATIONAL PVT LTD/ *department*/ '+arr[new Date().getMonth()]+'-'+  new Date().getFullYear()+'/ OFFER NO'
		htvalue+='<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear();
		htvalue+='<br><b>'+frm.doc.candidate_name+'</b><br>'+post
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>We are pleased to offer you the position of <b>'+post+'</b> in our <Name of Function> based at<Location of Posting>.'
		htvalue+='<br><br>Your immediate supervisor will be<Name of Reporting Manager>. We trust that your knowledge, skills and experience will be among our most valuable assets.As discussed, and agreed with you, you will be eligible to receive the following beginning on your joining date:'
		htvalue+='<br><br><ul><li><b>Salary:</b> Annual gross starting salary of Rs.< Annual CTC>, subject to tax and other statutory deductions</li><li><b>Sales Incentive:</b> As per the prevailing company scheme < Only Applicable for Sales personnel></li><li>Business Travel allowance and reimbursements as per company policy</li></ul>'
		htvalue+='<br><br>This offer letter is valid till < Expected date of joining>.  Please send a signed copy of this letter indicating your acceptance to join and resignation acceptance letter from your current employer to our HR.'
		htvalue+='<br><br>Your Appointment Letter will be issued on the date of joining. The joining formalities and induction will be carried out in our WTT INTERNATIONAL PVT LMT Office. '
		htvalue+='<br><br>Please submit the following documents to HR at the time of your joining:<ol><li>Photocopies of your Degree Certificates</li><li>Certifications,if Any</li><li>Experience Or relieving Letter</li><li>Two- Color Passport Size Photo</li><li>Latest Salary Slip from Your Previous Company</li><li>Proof of Address</li></ol>'
		htvalue+='<br><br>We look forward to welcome you aboard. '	
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'		
	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Developer Job'){
		var arr=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
		var htvalue='<h2 style="text-align:center"><u>Developer Job Offer Letter</u></h2>'
		htvalue+='<br><br>REF NO: WTT INTERNATIONAL PVT LTD/ *department*/ '+arr[new Date().getMonth()]+'-'+  new Date().getFullYear()+'/ OFFER NO'
		htvalue+='<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear();		
		htvalue+='<br><b>'+frm.doc.candidate_name+'</b><br>'+post
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>We are pleased to offer you the [full-time, part-time, etc.] position of <b>'+post+'</b> at <b>WTT INTERNATIONAL PVT LTD</b> with a start date of [start date], contingent upon [background check, I-9 form, etc.]. You will be reporting directly to <b>'+frm.doc.manager_name+'</b> at [workplace location]. We believe your skills and experience are an excellent match for our company'
		htvalue+='<br><br>In this role, you will be required to [briefly mention relevant job duties and responsibilities].'
		htvalue+='<br><br>The annual starting salary for this position is [amount] to be paid on a [monthly, semi-monthly, weekly, etc.] basis by [direct deposit, check, etc.], starting on [first pay period]. In addition to this starting salary, we’re offering you [discuss stock options, bonuses, commission structures, etc.].'
		htvalue+='<br><br>Your employment with <b>WTT INTERNATIONAL PVT LTD</b> will be on an at-will basis, which means you and the company are free to terminate the employment relationship at any time for any reason. This letter is not a contract or guarantee of employment for a definite amount of time.'
		htvalue+='<br><br>As an employee of <b>WTT INTERNATIONAL PVT LTD</b>, you are also eligible for our benefits program, which includes [medical insurance, vacation time, etc.], and other benefits which will be described in more detail in the [employee handbook, orientation package, etc.].'
		htvalue+='<br><br>Please confirm your acceptance of this offer by signing and returning this letter by [offer expiration date].'
		htvalue+='<br><br>We are excited to have you join our team! If you have any questions, please feel free to reach out at any time.'	
		htvalue+='<br><p style="text-align:right;">Regards'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">HR Department'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Formal Job'){
		var htvalue='<h2 style="text-align:center"><u>Formal Job Offer Letter</u></h2>'
		htvalue+='<br><br><b>'+frm.doc.candidate_name+'</b>,<br>'+post+',<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+',<br>WTT INTERNATIONAL PVT LTD,<br>No.3, College Cross road,<br> Tirupur - 641602,Tamilnadu'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>We are pleased to offer you employment at <b>WTT INTERNATIONAL PVT LTD.</b> We feel that your skills and background will be valuable assets to our team. '
		htvalue+='<br><br>Per our discussion, the <b>'+post+'</b> is POSITION APPLIED FOR. Your *Starting date* will be DATE TO START. The enclosed employee handbook outlines the medical and retirement benefits that our company offers. '
		htvalue+='<br><br>If you choose to accept this offer, please sign the second copy of this letter in the space provided and return it to us. A stamped, self-addressed envelope is enclosed for your convenience.'
		htvalue+='<br><br>We look forward to welcoming you as a new employee at <b>WTT INTERNATIONAL PVT LTD.</b> '
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Informal Job'){
		var htvalue='<h2 style="text-align:center"><u>Informal Job Offer Letter</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>We are very happy to offer you the job <b>'+post+'</b> in <b>WTT INTERNATIONAL PVT LTD</b>. We believe that your skills and experience is valuable to our company. You are joining as a short-timer in our company. You can enjoy all the standard benefits according to the company’s policy.'
		htvalue+='<br><br>The basic salary will be (salary amount) with monthly instalments. You can enjoy (number of days) for sick leave. There will be support for medical and dental health along with health insurance. There will be (number of the plan) for a retirement plan. There will be additional benefits such as tuition and development courses.'
		htvalue+='<br><br>Certain facilities are based on availability.'
		htvalue+='<br><br>There will be childcare for free.'
		htvalue+='<br><br>You have to sign and date this offer letter to us on the following address (address/email). We will consider that as acceptance from you. We would love to see you in our company. You shall work as <b>'+post+'</b> at our company <b>WTT INTERNATIONAL PVT LTD</b>. If you have any doubt about the post, make sure to contact me at (email/phone no). I would love to clear your doubts and questions.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Internal Promotion'){
		var htvalue='<h2 style="text-align:center"><u>Internal Promotion</u></h2>'
		htvalue+='<br><br>Hi All,'
		htvalue+='<br><br>I am very pleased to announce that <b>'+frm.doc.candidate_name+'</b> is transferring to the <b>*previous_post*</b> department to work as our new <b>*promoted_post*</b>.'
		htvalue+='<br><br>In the past <b>*aa*</b> years, <b>'+frm.doc.candidate_name+'</b> has achieved great things with the sales team helping us to maintain a fully functional website by bridging the gap between the sales and marketing departments. He has put in extra hours and taken on more responsibility, his record with our customers and co-workers is impressive by far. Now, he will bring his deep knowledge and experience to expand our customer base through the use of new marketing channels.'
		htvalue+='<br><br>If you have any queries about what <b>'+frm.doc.candidate_name+'</b> new position might mean for your new working relationship, don’t hesitate to direct any questions to me.'
		htvalue+='<br><br>Please join me in sending <b>'+frm.doc.candidate_name+'</b> a big congratulations and wishing him the best of luck in his new role.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Job Offer'){
		var htvalue='<h2 style="text-align:center"><u>Job Offer Letter</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>We have all really enjoyed speaking with you and getting to know you over the course of the last few weeks. The team and I have been impressed with your background and approach and would love to formally offer you a position as a <b>'+post+'</b> at <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+='<br><br>We can offer you a [$X] annual base salary [bonus and equity information, if equitable]. We offer [benefits details] and [number of days] of vacation per year. We can discuss start dates based on what is possible on your end, but we’d be excited to have you start [as soon as possible / on XYZ date].'
		htvalue+='<br><br>Please let me know if you have any questions or would like to discuss the offer in more detail. We would be thrilled to welcome you to the team!'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Sample Offer'){
		var htvalue='<h2 style="text-align:center"><u>Offer Letter</u></h2>'
		htvalue+='<br><br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br><b>'+frm.doc.candidate_name+'</b>,<br>'+post+',<br>WTT INTERNATIONAL PVT LTD,<br>No.3, College Cross road,<br>Tirupur - 641602,Tamilnadu'
		htvalue+='<br><br>We are pleased to offer you employment at <b>WTT INTERNATIONAL PVT LTD</b>. We feel that your skills and background will be valuable assets to our team. '
		htvalue+='<br><br>Per our discussion, the <b>'+post+'</b> is POSITION APPLIED FOR. Your starting date will be DATE TO START. The enclosed employee handbook outlines the medical and retirement benefits that our company offers. '
		htvalue+='<br><br>If you choose to accept this offer, please sign the second copy of this letter in the space provided and return it to us. A stamped, self-addressed envelope is enclosed for your convenience. '
		htvalue+='<br><br>We look forward to welcoming you as a new employee at <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Part Time to Full Time'){
		var htvalue='<h2 style="text-align:center"><u>Part-Time to Full-Time Offer Letter</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>I am <b>*Your Post*</b> is here to inform and congratulate you about one of the positive decision about your employment status. The company team has decided to extend the status of employment from part-time to full-time. The complete team is very much contented with your performance and dedication towards work. Hence we are here to provide you with the opportunity to work with our team as a full-time employee. The salary structure and other benefits will be surely provided you as per the company policy for the post of <b>'+post+'</b>.'
		htvalue+='<br><br>Please find the attachments regarding revised salary structure and revised job description about your post offered. Please provide your confirmation as soon as possible.'
		htvalue+='<br><br>We are looking forward to working with you ahead.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Salary Negotiation'){
		var htvalue='<h2 style="text-align:center"><u>Salary Negotiation</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>I truly enjoy my role as <b>'+post+'</b> here at <b>WTT INTERNATIONAL PVT LTD</b> Over the past year, I have gained a great deal of experience working with <b>*department_name*</b> team. Not only have I had the opportunity to build on my skill set, I’ve been able to bring additional knowledge to the table, including my work on the recent rebranding project.'
		htvalue+='<br><br>As my role has adapted since my initial hire, I am writing to request a meeting to discuss my current compensation. I value my position within the team, and I look forward to bringing additional insight to our future projects.'
		htvalue+='<br><br>I would love the opportunity to meet with you to discuss a salary increase. Certainly, let me know when you might be available. I appreciate your consideration.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Job Offer' && frm.doc.subject2=='Sales Job Offer'){
		var htvalue='<h2 style="text-align:center"><u>Sales Job Offer</u></h2>'
		htvalue+='<br><br><b>From</b><br>*Name*<br>*Position*<br>WTT INTERNATIONAL PVT LTD<br>Tirupur - 641602'
		htvalue+='<br><br><b>To<br></b>'+frm.doc.candidate_name+'<br>*address*<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Respected <b>'+frm.doc.candidate_name+'</b>,<br><p style="text-align:center"><b>Subject: Appointment Letter for Sales Manager</b>'
		htvalue+='<br><p style="text-indent:80px">I am very pleased to inform you that you have been appointed in <b>WTT INTERNATIONAL PVT LTD</b>, as a <b>'+post+'</b> in our Sales & Marketing Department from ______________. We consider that you will be a fine addition to our sales team. As discussed over interview, you will be appointed as a full-time employee with starting salary of Rs. 0000.'
		htvalue+='<br><br>We look forward to a mutually rewarding employment experience for you at <b>WTT INTERNATIONAL PVT LTD</b>. It is our anticipation that you will find this position exciting and rewarding.'
		htvalue+='<br><br>You will be required to sign a Company Confidentiality and Non-Compete Agreement, which is enclosed with the attached commission schedule. To confirm your acceptance of this offer, please return a signed copy of the same.'
		htvalue+='<br><br>If you have any question regarding this offer, kindly contact me.<br><p style="text-align:center">Accept our congratulations.'
		htvalue+='<br><p style="text-align:right;">Best Regards,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Referral' && frm.doc.subject3=='Employee Referral Bonus'){
		var htvalue='<h2 style="text-align:center"><u>Employee Referral Bonus</u></h2>'
		htvalue+='<br><br><b>Subject Line:</b> Help us find an awesome candidate for <b>'+post+'</b>?'
		htvalue+='<br><br>Hii All,'
		htvalue+='<br><br>As you all already know, we are constantly growing. For that reason, we are in a constant need for talented people like you! Since we know that, in your network, you have some great people you hang out with, we wanted to engage you in our recruiting process.'
		htvalue+='<br><br>We know that you, our current employees, know best who our ideal candidates are. Because of that, we truly believe that you, acting as recruiters, can bring our Talent Acquisition strategy to the next level.'
		htvalue+='<br><br>For you to better understand how the process will work, here are a few details I will include in every referral request:'
		htvalue+='<br><br><ul><li>Reasons why referrals are important for you?</li><li>How employees should refer candidates?</li><li>What information about referrals do we need?</li><li>How long does the process take?</li><li>How does the bonus/reward program work?</li></ul>'
		htvalue+="<br><br>I will be asking you to refer your friends, but I also encourage you to regularly visit our careers page to check for any new job opening we may have.<br>If you have any further questions about our Employee Referral Program, please don't hesitate to ask."
		htvalue+='<br><br>Thank you all in advance for your help!'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Referral' && frm.doc.subject3=='Employee Referral Program'){
		var htvalue='<h2 style="text-align:center"><u>Employee Referral Program</u></h2>'
		htvalue+='<br><br><b>Subject line:</b> Do you know about our Employee Referral Bonus Program?'
		htvalue+='<br><br>As you already know, we are constantly growing. Consequently, we are in a constant need for talented people like you.'
		htvalue+='<br><br>For this process to work even better, we have also came up with a new Referral Bonus Program. This is how the bonuses will be structured:'
		htvalue+='<br><br><ul><li>For every referral you get [Rsx]</li><li>For every candidate who makes it to the interview stage you get [$x]</li><li>For every new hire you get [xRs.]</li><li>If the new hire stays over [x] months you get [xRs.]</li></ul>'
		htvalue+="<br><br>We are currently looking for a person who would be a good fit for our [position] open position. If you know someone who would be a good fit for this position and for our company's culture, please send them our way :)"
		htvalue+='<br><br>In order to refer someone, I just need you all to answer a few questions: '
		htvalue+="<br><br><ul><li>Person's name and last time?</li><li>How do you know the person?</li><li>What position do you think this person would be a good fit for?</li><li>What is the person's expertise and most valuable skills for our company?</li><li>Why do you think this person would be a good fit for us?</li></ul>"
		htvalue+='<br><br>I am sure some of you have at least one person in your network who would be a great addition to our team!'
		htvalue+='<br><br>Also, I encourage you all to, from time to time, check our career page for any new job openings we may have. Here is the link to our career site: [insert link]. '
		htvalue+="<br><br>If you ever have someone on mind you would like to refer, please don't hesitate to do so.<br>If you have any questions about our referral process, please ask me at any time!<br>Thank you all for your help!"
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Referral' && frm.doc.subject3=='Employee Referral from  External Network'){
		var htvalue='<h2 style="text-align:center"><u>Employee Referral fom External Network</u></h2>'
		htvalue+='<br><br><b>Subject Line:</b> We’re hiring!'
		htvalue+='<br><br>Hi <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br><p style="text-indent:70px">Word on the street is that <b>WTT INTERNATIONAL PVT LTD</b> launched a search for a <b>'+post+'</b>. '
		htvalue=='<br><br>As you may already know, here at <b>WTT INTERNATIONAL PVT LTD</b>, we always want to collaborate with talented people and we’d like your help to find our next team member.'
		htvalue+='<br><br>This person will be responsible for [Include 1-2 key duties and link to the job description, e.g. “This person will join our team of mobile developers and will be responsible for improving our iOS applications.”]'
		htvalue+='<br><br>[It’s best to add some must-have requirements for the position, e.g. “Experience with Swift and interest in mobile technologies are required for this role.”]'
		htvalue+='<br><br>It’s a great opportunity for a <b>'+post+'</b> who wants to [e.g. work in a diverse environment and serve customers like X, Y, Z / to be part of a growing team and help us build X product / join our X team, work with high-end technology and attend global conferences that will help them develop professionally.]'
		htvalue+='<br><br>If you know someone who you think would be a good fit, it would be great if you could refer them [e.g. by emailing their contact details or resume.]'
		htvalue+='<br><br>Please feel free to contact me via email or at [e.g. 1-444-555-2222], if you have any questions.</p>'
		htvalue+='<br><br><p style="text-align:center">Thank You,</p>'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Referral' && frm.doc.subject3=='Refer A Friend'){
		var htvalue='<h2 style="text-align:center"><u>Refer A Friend</u></h2>'
		htvalue+='<br><br>Hi <b>'+frm.doc.candidate_name+'</b>'
		htvalue+="<br><br><p style='text-indent:70px'>How are you? I hope all is well. I know your organization is currently recruiting for a position of. I don’t know if you are open to referrals for this position, but in case you are, I would like to put in a good word for a <friend/former colleague/classmate/friend’s kid/etc.> of mine,</p>"
		htvalue+='<br>I’ve known for the last # years, and in my experience, he is (reliable, trustworthy, hard-working, collegial etc.). We worked together on XYZ project, and he was one of the best contributors to the team. Our challenge was (XYZ) and he helped solve the problem by. <br>He also has a proven commitment to the field of as shown by his years of experience/volunteering in the field. Last but not least, he is very dedicated to your cause and he told me this would be a dream job for him.'
		htvalue+='<br><br>I would be glad to answer any questions you may have about. Thanks for your consideration and have a great day.'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Referral' && frm.doc.subject3=='Referral Program Procedure'){
		var htvalue='<h2 style="text-align:center"><u>Referral Program Procedures</u></h2>'
		htvalue+="<br><br>Description<b></b><br><p style='text-indent:70px'><b>WTT INTERNATIONAL PVT LTD</b> is always looking for good people, and you can help. Research has shown, and our own experience supports, that new hires who come into a company through employee referrals are excellent contributors, stay with the company longer and are more cost-effective recruits."
		htvalue+="<br>That's where you come in! If you know someone who would be a good addition to <b>WTT INTERNATIONAL PVT LTD</b>, you may be awarded a referral bonus of [dollar amount] (less taxes) if you refer a candidate and he or she is hired.Employees must refer candidates to Human Resources through the employee referral program link on <b>WTT INTERNATION PVT LMT</b> intranet or by using the attached candidate referral form. </p>"
		htvalue+='<br><br><b>Quarterly Drawing </b><br><p style="text-indent:70px">At the end of each quarter, we will hold a drawing for a valuable prize. For every qualified referral you make during the quarter, your name will be entered in the drawing. '
		htvalue+='<br><br><b>Program Rules</b><br><ul>'
		htvalue+='<li>All <b>WTT INTERNATIONAL PVT LTD</b>employees, except those at vice president level and above, Human Resources personnel, and managers with hiring authority over the referred candidates, are eligible for the referral bonus and quarterly drawing. </li>'
		htvalue+='<li>The referral date cannot be earlier than the date the job opening is posted. The hiring of a referred employee must occur within 180 days (six months) of the initial referral date.</li>'
		htvalue+="<li>The referral must represent the candidate's first contact with <b>WTT INTERNATIONAL PVT LTD</b>.Temporary, summer, contract and former employees of <b>WTT INTERNATIONAL PVT LTD</b>are not eligible candidates for referral awards. </li>"
		htvalue+='<li>To be eligible for an award, an employee must submit a referral to Human Resources with a candidate referral form and a resume or employment application. </li>'
		htvalue+='<li>The referring employee must agree to have his or her name used when the company contacts the candidate. </li>'
		htvalue+='<li>The first employee to refer a candidate will be the only referring employee eligible for payment. </li>'
		htvalue+='<li>Only candidates who meet the essential qualifications for the position will be considered. </li>'
		htvalue+='<li>All candidates will be evaluated for employment consistent with company policies and procedures. </li>'
		htvalue+='<li>All information regarding the hiring decision will remain strictly confidential. </li>'
		htvalue+="<li>The referring employee must be employed by <b>WTT INTERNATIONAL PVT LTD</b>during the hired candidate's first 30 days of employment to receive payment of the referral bonus and entry into the quarterly drawing.</li>"
		htvalue+='<li></li>Any disputes or interpretations of this employee referral program will be handled through Human Resources. '
		htvalue+="<li></li>All referral bonus payments will be paid within 30 days after the referred employee's first day of employment at <b>WTT INTERNATIONAL PVT LTD</b>"
		htvalue+='</ul><br><br><b>Candidate Referral Form </b><br>'
		htvalue+='<br><table style="border:0px;text-align:center"><tr><td>Job Title:<input type="text"></td><td>Job Requisition:<input type="text"></td></tr><tr><td>Candidate name:<input type="text"></td><td>Referral Date:<input type="text"></td></tr>'
		htvalue+="<tr><td colspan='2'>Referring Employee's Name:<input type='text'></td></tr><tr><td>Work Phone:<input type='text'></td><td>Work Email:<input type='text'></td></table><br><p style='text-align:center'>I have read and understand the referral program rules.</p><br><br>"
		htvalue+="<table style='text-align:center'><tr><td> </td><td></td></tr><tr><td>Signature of Employee</td><td>Date</td></tr><u style='text-align:center'>Attach the candidate's resume or application and submit this form to Human Resources.</u></tr></table><br>"
		htvalue+="<table style='text-align:left;margin-left:auto;margin-right:auto'><tr><td><b>INTERNAL USE ONLY</b></td></tr><tr><td>To: Payroll</td></tr><tr><td>From: Human Resources</td></tr><tr><td>Charge To:</td></tr><tr><td>Target Date for award payment: (within 30 days of hire date below)</td></tr><tr><td>Referred candidate's hire date:</td></tr></table>"
	}
	else if(frm.doc.template=='Referral' && frm.doc.subject3=='Referred Candidate Email Template'){
		var htvalue='<h2 style="text-align:center"><u>Referred candidate Mail Template</u></h2>'
		htvalue+='<br>><br><b>Subject line:</b> Referral from <b>'+frm.doc.candidate_name+'</b> referred you for our new position of <b>'+post+'</b>'
		htvalue+='<br><br>Hi <b>'+frm.doc.candidate_name+'</b>'
		htvalue+='<br><br>I am <b>{your name}, {your job_title}</b> at <b>WTT INTERNATIONAL PVT LTD</b>. At the moment we are looking for a great candidate for our newly open position a <b>'+post+'</b> and {Employee_name} suggested you beacuse you are a perfect fit.'
		htvalue+='<br><br>After reviewing your {for example LinkedIn, GitHub, etc.} profile, I thought your background and experience are impressive and relevant to what your duties would be for this position. At <b>WTT INTERNATIONAL PVT LTD</b>, we are always on a lookout for more talented people like {Employee_name}, so we would enjoy meeting you.'
		htvalue+='<br><br>Are you interested in learning a more about our company and the position? We would love to present you our proposition and we will be happy to answer any of your questions. Are you available for a quick intro call [include date and time]? If you prefer some other time better, please let me know and I will give my best to coordinate.'
		htvalue+='<br><br>Have a wonderful day, and I hope to hear back from you,'
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Rejection' && frm.doc.subject4=='Applicant Rejection Letter'){
		var htvalue='<h2 style="text-align:center"><u>Applicant Rejection Letter</u></h2>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+="<br><br><p style='text-indent:70px'>Thank you for your application for the <b>"+post+"</b> at <b>WTT INTERNATIONAL PVT LTD</b>. We really appreciate your interest in joining our company and we want to thank you for the time and energy you invested in applying for our job opening."
		htvalue+="<br><br>We received a large number of applications, and after carefully reviewing all of them, unfortunately, we have to inform you that this time we won’t be able to invite you to the next phase of our selection process.<br>Though your qualifications are impressive, we have decided to move forward with a candidate whose experiences better meet our needs for this particular role."
		htvalue+="<br><br>However, we really do appreciate your interest in our company. We hope you’ll keep us in mind and apply again in the future should you see a job opening for which you qualify.<br>If you have any questions or need additional information, please don’t hesitate to contact me by email <b>[insert your email address]</b> or phone <b>[insert your phone number]</b>."
		htvalue+="<br><br>We wish you every personal and professional success in your future endeavors.<br>Once again, thank you for your interest in working with us.1"
		htvalue+='<br><p style="text-align:right;"><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br><p style="text-align:right;">*Signature*</p>'
	}
	else if(frm.doc.template=='Rejection' && frm.doc.subject4=='Candidate Rejection Email'){
		var htvalue='<h2 style="text-align:center"><u>Candidate Rejection Mail</u></h2>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br>Thank you for your application for the <b>'+post+'</b> at <b>WTT INTERNATIONAL PVT LTD</b>. We really appreciate your interest in joining our company and we want to thank you for the time and energy you invested in your <b>[insert applicable: job application/job assignment]</b>.'
		htvalue+=',br><br>We received a large number of <b>[insert applicable: job application/job assignment]</b>, and after carefully reviewing all of them, unfortunately, we have to inform you that this time we won’t be able to invite you to the next phase of our selection process.'
		htvalue+='<br><br>Though your <b>[insert applicable: education/qualifications/working experience/skills]</b> are impressive, we have decided to move forward with a candidate whose <b>[insert applicable: education/qualifications/working experience/skills]</b> better meet our needs for this particular role.'
		htvalue=='<br><br>We truly appreciate your expertise in <b>[insert applicable industry]</b> and interest in our company. We hope you’ll keep us in mind and apply again in the future.<br>If you have any questions or need additional information, please don’t hesitate to contact me by email <b>[insert your email address]</b> or phone <b>[insert your phone number]</b>.'
		htvalue=='<br><br>We wish you every personal and professional success in your future endeavors.<br>Once again, thank you for your interest in working with us.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Rejection' && frm.doc.subject4=='Candidate Rejection Letter'){
		var htvalue='<h2 style="text-align:center"><u>Candidate Rejection Letter</u></h2>'
		htvalue+='<br><br><b>To<br></b>'+frm.doc.candidate_name+'<br>*address*<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br>As you know, we interviewed a number of candidates for the <b>'+post+'</b> position, and we have decided to offer the position to another candidate. So, the purpose of this letter is to let you know that you have not been selected for the position.'
		htvalue+='<br><br>Thank you so much for taking the time to come to <b>WTT INTERNATIONAL PVT LTD</b> to meet our interview team. We enjoyed meeting you and our discussions.'
		htvalue+='<br><br>Please feel free to apply for open positions, for which you qualify, in our company in the future.'
		htvalue+='<br><br>We wish you every personal and professional success with your job search and in the future. Thank you for your interest in our organization.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Rejection' && frm.doc.subject4=='Interview Feedback'){
		var htvalue='<h2 style="text-align:center"><u>Interview Feedback to Candidate</u></h2>'
		htvalue+='<br><br><b>Subject line:</b> Your interview with <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">Thank you for very much for applying for our <b>'+post+'</b> position at <b>WTT INTERNATIONAL PVT LTD</b>. We’d like to let you know that we have chosen to move forward with a different candidate for this position.'		
		htvalue+='<br><br>Although we were very impressed with your [Choose a quality or qualification the candidate possessed that you liked, e.g. specific degree, experience using a certain program, in-person communication], we are looking for a candidate who [Mention something that the candidate lacked but could reasonably attain in the future, e.g. has experience with managing sales teams, is able to speak French fluently].'
		htvalue+='<br><br>After having the chance to get to know you better and learn more about your qualifications, we’d like to keep your resume and application on file for any future openings we have that would be a good fit. If you are interested in an open position in the future. And you feel qualified for it, please feel free to reach out and apply for it. '
		htvalue+='<br><br>Thank you again for your interest in working at <b>WTT INTERNATIONAL PVT LTD</b>.<br> We wish you the best of luck with your job search.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Rejection' && frm.doc.subject4=='Application Rejection'){
		var htvalue='<h2 style="text-align:center"><u>Application Rejection</u></h2>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">Thank you for taking the time to meet with our team about the <b>'+post+'</b> position at <b>WTT INTERNATIONAL PVT LTD</b>. It was a pleasure to learn more about your skills and accomplishments.'
		htvalue+='<br><br>Unfortunately, our team did not select you for further consideration.'
		htvalue+='<br>I would like to note that competition for jobs at <b>WTT INTERNATIONAL PVT LTD</b> is always strong and that we often have to make difficult choices between many high-calibre candidates. Now that we’ve had the chance to know more about you, we will be keeping your resume on file for future openings that better fit your profile.'
		htvalue+='<br><br>I am happy to answer your questions if you would like any specific feedback about your application or interviews.'
		htvalue+='<br>Thanks again for your interest in <b>WTT INTERNATIONAL PVT LTD</b> and best of luck with your job search.</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Rejection' && frm.doc.subject4=='Post Interview Sample Letter'){
		var htvalue='<h2 style="text-align:center"><u>Post Interview Sample</u></h2>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">Thank you very much for investing your time and effort to interview with our team about our <b>'+post+'</b> position at <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+='<br>All of us really enjoyed meeting you, learning about your skills and experiences and having a really interesting conversation.'
		htvalue+="<br><br>Unfortunately, at this time, we decided to proceed with our selection process with another candidate.<br>It is a decision we didn't make easily because you are really a strong candidate with a wonderful personality."
		htvalue+='<br><br>We will definitely keep your resume in our talent database, and in case that we have a job opening that better fits your profile, we will make sure to get in touch with you.'
		htvalue+="<br><br>If you have any further questions or need more feedback, please do not hesitate to ask. I will be more than happy to answer any of your questions.<br>I wish you the best of luck in your future endeavors and hope we'll have a chance to meet again soon."
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Rejection' && frm.doc.subject4=='Rejecting Overqualified Candidate'){
		var htvalue='<h2 style="text-align:center"><u>Rejecting Overqualified Candidate</u></h2>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">Thank you for very much for applying for our <b>'+post+'</b> position at <b>WTT INTERNATIONAL PVT LTD</b>. It was a pleasure getting to know you better and learning about your accomplishments. We’d like to let you know that we have chosen to move forward with a different candidate for this position.'
		htvalue+='<br><br>We were all extremely impressed by your qualifications and your in-person communication skills. I’d like to stay in touch with you and contact you if a position better suited to your abilities opens up. '
		htvalue+="<br><br>I’d be happy to answer any questions you have or offer specific feedback about your interview if you’d like. Feel free to reach out via [email/phone]. "
		htvalue+='<br><br>Thank you again for your interest in working at <b>WTT INTERNATIONAL PVT LTD</b>. We wish you the best of luck with your job search.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Sourcing a Referred Candidate'){
		var htvalue='<h2 style="text-align:center"><u>Sourcing a Referred Candidate</u></h2>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br>Subject line: Referral from <b>[Employee Name]</b> mentioned you’re a great <b>'+post+'</b>'
		htvalue+='<br><br><p style="text-indent:70px">I am <b>[your name], [your job_title] at WTT INTERNATIONAL PVT LTD</b>. We are currently looking to hire a <b>'+post+'</b> and [Employee_name] mentioned that you might be a good fit.'
		htvalue+='<br><br>From what I have seen in your [e.g. LinkedIn or GitHub] profile, your background is impressive and you’ve done some interesting things, similar to our projects. [It’s best if you mention something that specifically caught your eye.] Here, at <b>WTT INTERNATIONAL PVT LTD</b>, we’re always looking for more great people like <b>[Employee_name]</b>, so we’d like to get to know you.'
		htvalue+='<br><br>Would you be available for a quick intro call [include date and time or a period of time, e.g. ‘sometime this week’] to learn a little bit more about our position? I’m also happy to coordinate via email or LinkedIn, if you prefer.'
		htvalue+='<br><br>I hope you have a great day,</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Internal Job posting'){
		var htvalue='<h2 style="text-align:center"><u>Internal Job Posting</u></h2>'
		htvalue+='<br><br><b>Subject:</b> Internal job opening with '+post
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">You are aware of the vacancy at our company for the post of <b>'+post+'</b>. This post will go through the external channel, but we would like to get some eligible candidates for our company from the current employee.'
		htvalue+='<br><br>There will be new vacancies with <b>'+post+'</b> in no time. You have to follow three main duties. We would appreciate some experienced candidates in our company for the role of <b>'+post+'</b>.'
		htvalue+='<br><br>You should be free to contact us for the following information <b>(phone and email)</b>. If you want to apply for the post, make sure to reply to this email with your resume.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Job Opportunities'){
		var htvalue='<h2 style="text-align:center"><u>Job Opportunity</u></h2>'
		htvalue+='<br><br><b>Subject line: WTT INTERNATIONAL PVT LTD</b>has an exciting job opportunity for you'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">I would like to present to you our new job opportunity I think you may find interesting. '
		htvalue+='<br><br>We have a job opening for <b>'+post+'</b>, and according to your skills and experience, I think you may be a good fit. '
		htvalue+='<br><br>As a <b>'+post+'</b>, you would be responsible for [short job description]. '
		htvalue+='<br><br>If you are interested to learn more about this opportunity, please check it out on our career site [link to the job opening]. '
		htvalue+='<br><br>Also, to learn more about what is like to be a <b>WTT INTERNATIONAL PVT LTD</b> employee, please read more about current employees and company culture [link to your career site]. '
		htvalue+="<br><br>If you have any additional questions, please don't hesitate to ask. <br>I hope to hear back from you!</p>"
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Keeping Candidates Warm'){
		var htvalue='<h2 style="text-align:center"><u>Job Opportunity</u></h2>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">I hope your week is going well! I wanted to check in and let you know that I’m still gathering feedback after your interview with the search committee.'
		htvalue+='<br><br>It may take a few more days to hear from all of the search committee members, and I didn’t want you to think I had forgotten about you.'
		htvalue+='<br><br>You may have questions for me, and I hope you’ll let me know if that is the case. I will be in touch as soon as the search committee’s feedback is complete, but I am always happy to answer your questions in the meantime.'
		htvalue+='<br><br>Thanks, and have an outstanding day!</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'

	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Passive Candidate'){
		var htvalue='<h2 style="text-align:center"><u>Passive-Candidate</u></h2>'
		htvalue+='<br><br><b>Subject line: </b>Join Our Amazing Team at <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">I am <b>[your name]</b>, <b>[your job_title]</b> at <b>[company_name}</b>. I just saw your profile on [Social Media or Job Board], and I am very impressed with your skills and experience in [name a specific skill that you see valuable].'
		htvalue+='<br><br>We are currently looking for a <b>'+post+'</b> to join our amazing team, and I think you would be a great fit. We are currently working on cool projects such as [project description], and I thought you would find that interesting. '
		htvalue+='<br><br>If this is something that interests you, please reach back to me.'
		htvalue+='<br><br>I have also included some of our employee testimonials and stories, so that you can learn about what is it like to work for <b>WTT INTERNATIONAL PVT LTD</b>. '
		htvalue+='<br><br>Have a great rest of the day, and I hope to hear back from you,</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Recruiter Introduction to Candidate'){
		var htvalue='<h2 style="text-align:center"><u>Recruiter Indroduction to Candidate</u></h2>'
		htvalue+='<br><br>Dear All'
		htvalue+='<br><br><p style="text-indent:70px">I am <b>[your name]</b> working at <b>WTT INTERNATIONAL PVT LTD</b> for the role of <b>[your job title]</b>. I found your profile on LinkedIn that really impressed me. Especially the achievements [mention the achievements field here] mentioned on your resume was eye catching.'
		htvalue+='<br><br>Working here at our <b>WTT INTERNATIONAL PVT LTD</b> allows candidates to indulge through the team of growing talent. Talented people are allowed to work together and collaborate with the clients [X, Y, Z client company’s name] for larger achievements.'
		htvalue+='<br><br>As you know we are presently hiring for profile of [role type with all necessary details] for one of our renowned clients. So, it would be a pleasure to know more about you and throw a point of light more on this position importance and requirements.'
		htvalue+='<br><br>If you are available then let me know such that I could set a call for you, or else contact via mails as preferred.'
		htvalue+='<br><br>Hope you have a great day.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Recruiting Bilingual Candidate'){
		var htvalue='<h2 style="text-align:center"><u>Recruiting bilingual candidates</u></h2>'
		htvalue+='<br><br>Subject line: <b>WTT INTERNATIONAL PVT LTD</b> is looking for a <b>'+post+'</b> / Interested in joining our team at <b>WTT INTERNATIONAL PVT LTD</b>?'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">I am <b>[your_name]</b>,<b> [your job_title]</b> at <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+='<br>I found your profile on [add specific website or social network] / I got your resume through [e.g. community or college] and I was impressed with your background. [It’s best to include a specific achievement that grabbed your attention.] '
		htvalue+='<br><br>Here, at <b>WTT INTERNATIONAL PVT LTD</b>, we are always looking to foster a multicultural work environment and currently, we have an opening for a [job_title – add link to the job description.] We are looking for someone who’ll [e.g. act as our company representative for our global clients / create engaging online content to attract global clients / support our international customer base.] '
		htvalue+='<br><br>Your language skills along with your [e.g. customer service] experience would be great assets to our team. [Mention benefits and perks that you offer, e.g. “Our benefits package includes college tuition assistance for you and your family members.” or “We offer daily meals with diverse food cuisines and organize regular in-house events for our expats.”]'
		htvalue+='<br><br>I’d like to tell you a little more about this position and learn a few things about you, as well.'
		htvalue+='<br><br>Are you available [include date and time or a period of time, e.g. “sometime this week”]? If so, I’d be happy to set up a call. I’m also happy to coordinate via email or LinkedIn, if you prefer.'
		htvalue+='<br>I hope you have a great day,</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Sourcing Developer Candidate'){
		var htvalue='<h2 style="text-align:center"><u>Sourcing Developer candidates</u></h2>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+="<br><br><p style='text-indent:70px'>I've been scouting for [Your_Town]’s best developers for a while now, and no one has impressed me as much as you!"
		htvalue+='<br><br>Your experience, knowledge and skills, particularly [Skills], make you a great fit for what we were trying to do over at <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+="<br><br>I'd love to tell you a bit more about <b>WTT INTERNATIONAL PVT LTD</b>, the newly opened <b>"+post+"</b> position, and why I think you would love it!"
		htvalue+='<br><br>Do you have time on <b>[Day]</b> at <b>[Time]</b> for a chat?</p.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='From Employer to Recruitment Agency'){
		var htvalue='<h2 style="text-align:center"><u>Email from employer to a recruitment agency or external recruiter</u></h2>'
		htvalue+='<br><br><b>Subject:</b> New job requisition from <b>WTT INTERNATIONAL PVT LTD</b> / New open role at <b>WTT INTERNATIONAL PVT LTD</b>: <b>'+post+'</b>'
		htvalue+='<br><br>Dear <b>[Partner Name]</b>'
		htvalue+'<br><br>As discussed, we’d like to hire a new <b>'+post+'</b> for our <b>[department]</b>. We’re looking for a professional with at least [4] years of relevant work experience with expertise in [X technology] who’ll be able to [build mobile applications from scratch]. This is a [full time] position and the salary range is [XY - XXZ]. Attached you’ll find the detailed job description you can use to advertise the job and source candidates. '
		htvalue+='<br><br>Ideally, we’d like to have our new hire onboard on [date]. So, we should have a shortlist of [five] candidates by [date]. Please let me know if this sounds like a reasonable timeframe for the particular position.    '
		htvalue+='<br><br>Feel free to reach out if you need me to clarify the qualification criteria or the scope of responsibilities. I’m also happy to answer any other questions you may have about the position.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Sourcing Marketing Candidate'){
		var htvalue='<h2 style="text-align:center"><u>Sourcing marketing candidates email template </u></h2>'
		htvalue+='<br><br>Subject line: <b>WTT INTERNATIONAL PVT LTD</b> is looking for a <b>'+post+'</b> / Interested in joining our team at  <b>WTT INTERNATIONAL PVT LTD</b>?'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">I am <b>[your_name]</b>,<b> [your job_title]</b> at <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+='<ul><li>I saw your profile on [e.g. LinkedIn] and I was really impressed by your experience with [add specific software, e.g. SalesForce or specific field, e.g. email marketing campaigns.] I was particularly excited to see [add specific achievement that caught your eye]. We are currently looking for a <b>'+post+'</b>[ – add link to the job description] to join our team/ to manage [add marketing specific project.] I’d love to tell you more about this position and discuss how we could achieve great things together.</li>'
		htvalue+='<li>I saw your online portfolio on [e.g. Behance or Dribbble] and I was really impressed by your work on [mention specific field, e.g. company logos.] Here, at <b>WTT INTERNATIONAL PVT LTD</b>, we are always looking to collaborate with creative people who can freshen up our designs. Currently, we want to expand our team with a <b>'+post+'</b>[ – add link to the job description]. I’d love to tell you a little more about this position and learn a few things about you, as well.</li>'
		htvalue+='<li>We met [mention specific time e.g. one month ago] at [X event/conference] / We’ve previously interacted [mention specific social platform, e.g. X Slack group] and I couldn’t help but notice how you made a good first impression and maintained pleasant discussions. Here, at <b>WTT INTERNATIONAL PVT LTD</b>, we prioritize our client satisfaction and, currently, we’re looking for a <b>'+post+'</b>[ – add link to the job description] who’ll positively represent our brand both online and offline. I’d love to tell you a little more about this position and learn a few things about you, as well.</li>'
		htvalue+='<li>I saw your profile [e.g. on Twitter or Quora] and I was really impressed by the way you reply to [e.g. customers or people.] Here, at <b>WTT INTERNATIONAL PVT LTD</b>, we are always looking to build strong relationships with our audience. Currently, we’d like to grow our team with a <b>'+post+'</b> [– add link to the job description] who will [e.g. contact customers online or manage our social media pages.] I’d love to tell you a little more about this position and learn a few things about you, as well.</li></ul>'
		htvalue+='<br><br>Are you available [include date and time or a period of time, e.g. ‘sometime this week’]? If so, I’d be happy to set up a call. I’m also happy to coordinate via email or LinkedIn, if you prefer'
		htvalue+='<br><br>I hope you have a great day,</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Sourcing Veteran Candidate'){
		var htvalue='<h2 style="text-align:center"><u>Sourcing veteran candidates email template </u></h2>'
		htvalue+='<br><br><b>Subject line:</b> <b>WTT INTERNATIONAL PVT LTD</b> is looking for a <b>'+post+'</b> '
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">I am <b>[your_name]</b>,<b> [your job_title]</b> at <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+='<br><br>I found your profile on [add specific website or social network] / I got your resume through [e.g. job fair or college] and I was impressed by your achievements while serving in the military. [It’s best to include a specific achievement that grabbed your attention.] Thank you for your service.'
		htvalue+='<br><br>Here, at <b>WTT INTERNATIONAL PVT LTD</b>, we are always looking to collaborate with skilled and dedicated people and currently, we have an opening for a [<b>'+post+'</b>  – add link to the job description.] Your leadership skills along with your experience as part of a team would be great assets for our company. [Mention benefits that you offer, e.g. “To help our new employees adjust, we offer additional educational packages and on-the-job training sessions”  or “Our benefits package includes college tuition assistance for you and your family members.”] '
		htvalue+='<br><br>I’d like to tell you a little more about this position and learn a few things about you, as well.<br>Are you available [include date and time or a period of time, e.g. “sometime this week”]? If so, I’d be happy to set up a call. I’m also happy to coordinate via email or LinkedIn, if you prefer.'
		htvalue+='<br><br>I hope you have a great day,</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template=='Sourcing' && frm.doc.subject5=='Sourcing Sales Candidate'){
		var htvalue='<h2 style="text-align:center"><u>Sourcing Sales candidates email template </u></h2>'
		htvalue+='<br><br><b>Subject line:</b> <b>WTT INTERNATIONAL PVT LTD</b> is looking for a <b>'+post+'</b> '
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">I am <b>[your_name]</b>,<b> [your job_title]</b> at <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+='<br><ul><li>I saw your profile on [e.g. LinkedIn] and I was really impressed by your experience with [add specific software, e.g. SalesForce or specific field, e.g. B2B sales experience.] I was particularly excited to see [add specific achievement or cooperation that caught your eye]. We are currently looking for a [<b>'+post+'</b> – add link to the job description] to join our team/ to manage [add sales specific project.] I’d love to tell you more about this position and discuss how we could achieve great things together. </li>'
		htvalue+='<li>I saw on your  [e.g. on Meetup.com or Twitter] profile that you regularly participate in [e.g. Public Speaking and Sales] [meetings/events/seminars.] We are always looking for people who can present themselves and our company confidently. Currently, we’d like to expand our sales team with a [<b>'+post+'</b>- add link to the job description.] I’d love to tell you a little more about this position and learn a few things about you, as well. </li>'
		htvalue+='<li>We met [e.g. recently / around 2 months ago], when you applied for the <b>'+post+'</b>position. Even though we decided to move on with a different candidate at that time, your profile really stood out and we’ve kept you in mind for future openings. Particularly, your communication and presentation skills during our interview were impressive. We feel you’d be a good fit for our [<b>'+post+'</b>- add link to the job description.] I’d love to learn about what you’ve been up to since we last met and tell you a little bit more about this position.</li>'
		htvalue+='<li>I saw your profile [e.g. on Twitter or Quora] and I was really impressed by the way you reply to [e.g. customers or people.] Here <b>WTT INTERNATIONAL PVT LTD</b>, we are always looking to build strong relationships with our customers. Currently, we’d like to grow our team with a [<b>'+post+'</b>– add link to the job description] who will contact customers [e.g. via email and/or social media.] I’d love to tell you a little more about this position and learn a few things about you, as well. </li></ul>'
		htvalue+='<br><br>Are you available [include date and time or a period of time, e.g. ‘sometime this week’]? If so, I’d be happy to set up a call. I’m also happy to coordinate via email or LinkedIn, if you prefer.'
		htvalue+='<br>I hope you have a great day,</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template3=='Joining Bonus'){
		var htvalue='<h2 style="text-align:center"><u>Joining Bonus Letter with Retention Clause </u></h2>'
		htvalue+='<br><br><b>To<br></b>'+frm.doc.candidate_name+'<br>*address*<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br>We are pleased to welcome you on-board at our Company. We feel that your skills and background will be valuable assets to our team.'
		htvalue+='<br><br>Per our discussion, the position is <b>'+post+'</b>. The enclosed employee handbook outlines the medical and retirement benefits that our company offers. '
		htvalue+='<br><br>The Company is pleased to offer you a Joining Bonus of <b><AMOUNT></b>. You will be subjected to complete a minimum period of 2 years. If during the retention period, you wish to transition from your role, you will be subjected to forfeit the joining bonus paid to you and the amount will have to be paid back to the company.'
		htvalue+='<br><br>A stamped, self-addressed envelope is enclosed for your convenience. '
		htvalue+='<br><br>We look forward to welcoming you as a new employee at <b>WTT INTERNATIONAL PVT LTD</b>. '
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template3=='Job Offer'){
		var htvalue='<h2 style="text-align:center"><u>JOB OFFER</u></h2>'
		htvalue+='<br><br><b>Subject: </b>Job Offer from <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br>We were all very excited to meet and get to know you over the past few days. We have been impressed with your background and would like to formally offer you the position of <b>'+post+'</b>. This is a [full/part] time position [mention working days and hours.] You will be reporting to the head of the <b>[Department_name]</b> department. [If applicable: Please note that <b>WTT INTERNATIONAL PVT LTD</b> is an at-will employer. That means that either you or <b>WTT INTERNATIONAL PVT LTD</b> are free to end the employment relationship at any time, with or without notice or cause.]'
		htvalue+='<br<br>We will be offering you an annual gross salary of [$X] and [mention bonus programs, if applicable.] You will also have [mention benefits as per company policy, like health and insurance plan, corporate mobile or travel expenses] and [X] days of paid vacation per year.<br>[optional: I am attaching a letter with more details about your compensation plan.]'
		htvalue+='<br><br>Your expected starting date is <b>[date.]</b> You will be asked to sign a contract of [contract_duration, if applicable] and [mention agreements, like confidentiality, nondisclosure, and non-compete] at the beginning of your employment.'
		htvalue+='<br><br>We would like to have your response by <b>[date.]</b> In the meantime, please feel free to contact me or <b>[Manager_name]</b> via email or phone on [provide contact details], should you have any questions.'
		htvalue+='<br><br>We are all looking forward to having you on our team.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template3=='New Employee Announcement'){
		var htvalue='<h2 style="text-align:center"><u>New Employee Announcement</u></h2>'
		htvalue+='<br><br><b>Subject: </b>: Welcoming <b>'+frm.doc.candidate_name+'</b> to <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><br>Hi All,'
		htvalue+='<br><br><p style="text-indent:70px">I am very pleased to announce that <b>'+frm.doc.candidate_name+'</b> will be joining us as a <b>'+post+'</b> on <b>[Start date.]</b>'
		htvalue+='<br><br><b>'+frm.doc.candidate_name+'</b> will work with <b>[department/ team]</b> to [Add information about what they’ll be doing / what they’ll be responsible for, e.g. ‘help us grow our sales department’] He/She has previously worked at/in [Add information about employment background] / He/She has recently graduated from [Insert information about academic background.]'
		htvalue+='<br><br>Please come to meet <b>'+frm.doc.candidate_name+'</b> on [Start date] at [specific time] and welcome him/her to the team!'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template3=='New Employee Welcome'){
		var htvalue='<h2 style="text-align:center"><u>New Employee Welcome</u></h2>'
		htvalue+='<br><br><b>Subject: </b>Welcome to <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><br>Dear Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br>We are all excited to welcome you to our team! '
		htvalue+='<br><br>As agreed, your start date is [date.] We expect you to be in our offices by [time] and our dress code is [casual/ business casual.] <br>[If necessary, remind your employees that they need to bring their ID/ paperwork.]'
		htvalue+='<br><br>At <b>WTT INTERNATIONAL PVT LTD</b>, we care about giving our employees everything they need to perform their best. As you will soon see, we have prepared your workstation with all the necessary equipment. Our team will help you set up your computer, software, and online accounts on your first day. [Plus, if applicable, mention any extra things you’ve prepared for your new hire, like a parking spot, a coffee mug with their name or a company t-shirt.]'
		htvalue+='<br><br>We’ve planned your first days to help you settle in properly. You can find more details in the enclosed agenda. As you will see, you’ll have plenty of time to read and complete your employment paperwork (HR will be there to help you during this process!) You will also meet with your hiring manager to discuss your first steps. For your first week, we have also planned a few training sessions to give you a better understanding of our company and operations.'
		htvalue+='<br><br>Our team is excited to meet you and look forward to introducing themselves to you during [planned event/ lunchtime].'
		htvalue+='<br><br>If you have any questions before your arrival, please feel free to email or call me and I’ll be more than happy to help you.'
		htvalue+='<br><br>We are looking forward to working with you and seeing you achieve great things!'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template4=='Breach Of Employment'){
		var htvalue='<h2 style="text-align:center"><u>New Employee Welcome</u></h2>'
		htvalue+='<br><br>Hello Mr./Ms. <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br>Trust you are doing well,'
		htvalue+='<br><br>We have noticed a breach from your end regarding your employment contract with the company.'
		htvalue+='<br><br>Keeping the company’s rights and values in mind we are forced to take strong action.'
		htvalue+='<br><br>The breach was <b>_________</b><br>Keeping your track record and performance over the years in mind we are taking this as your first warning, however if this continues we will be left with no option but to terminate your employment with the company.'
		htvalue+='<br><br>If you have any questions regarding this please contact me at <b>___</b> or email me at <b>___</b>.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template5=='Appraisal'){
		var htvalue='Mr/ Ms. <b>'+frm.doc.candidate_name+'</b><br>Department : Name of Department<br><br>Dear,<br><br><p style="text-indent:70px">Thank you for your contribution to the business over the last year.<br><br>I am particularly pleased to see that you have earned a “Significantly Exceeds Expectations” rating in your performance review.  This is just reward for your dedication, passion and commitment to excellence.  <br>Congratulation on your promotion to <b>_________________</b>.<br>Effective April 1, YYYY, your salary has been revised to <b>Rs. /- per annum</b>.  This includes a Variable Pay component of <b>Rs. /- payable annually</b> (upon the end of the fiscal year 20YY-YY) based on performance parameters that shall be communicated to you separately. <br><br>The details of your revised compensation package have been attached.<br><br>Through the last financial year, we have consolidated our business and we now look forward to a year of strong growth. I am confident of a great year ahead in which we will surpass all our targets with your commitment and contribution.'
		htvalue+='<br><br>[OR]<br><br>Dear,<br><br><p style="text-indent:70px">Thank you for your contribution to the business over the last year. <br><br>I am happy to see that you have earned an“Exceeds Expectations” rating in your performance review.  This is just rewarding for your dedication, passion and commitment to excellence. <br><br>Effective April 1, 20YY, your salary has been revised to <b>Rs. /- per annum</b>.  This includes a Variable Pay component of <b>Rs. /- payable annually</b> (upon the end of the fiscal year 20YY-YY) based on performance parameters that shall be communicated to you separately. <br>The details of your revised compensation package have been attached.<br><br>Through the last financial year, we have consolidated our business and we now look forward to a year of strong growth. I am confident of a great year ahead in which we will surpass all our targets with your commitment and contribution.'
		htvalue+='<br><br>[OR]<br><br>Dear,<br><br><p style="text-indent:70px">Thank you for your contribution to the business over the last year. <br><br>You have earned a <b>“Meets Expectations”</b> rating in your performance review.  With your potential, we hope to see you excel in your work and grow significantly higher in the future.<br><br>Effective April 1, 20YY, your salary has been revised to <b>Rs. /- per annum</b>.  This includes a Variable Pay component of <b>Rs. /- payable annually</b> (upon end of the fiscal year 20YY-YY) based on performance parameters that shall be communicated to you separately. <br><br>The details of your revised compensation package have been attached.<br><br>Through the last financial year, we have consolidated our business and we now look forward to a year of strong growth. I am confident of a great year ahead in which we will surpass all our targets with your commitment and contribution.'
		htvalue+='<br><br>[OR]<br><br>Dear <b>'+frm.doc.candidate_name+'</b>,<br><br><p style="text-indent:70px">The Annual Review for the period April – March <b>YYYY</b> rated you below the average company performance standards at “Below Expectations”.<br><br>Since we sense potential in you, we would like you to work on your performance and bring it to acceptable standards. During this period, we advise you to work closely with your immediate supervisor to achieve this. We will continually review your performance over the next 60 days – documentation of the acceptable Performance standards for you, will be forwarded to you by your immediate supervisor within 2 weeks.  If you are unable to bring your performance to the acceptable standard, we will be forced to take action.<br><br>We sincerely hope the guidance and feedback given during the review will help you in fulfilling your potential. We look forward to seeing you excel at work.<br><br>Please contact your immediate supervisor or Human Resources for any clarification that you may require in this regard.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>'+frm.doc.hr_name+'</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template5=='Warning'){
		var htvalue='Mr/ Ms. <b>'+frm.doc.candidate_name+'</b><br>Department : Name of Department<br><br>Dear,<br><br><p style="text-indent:70px">We have observed that you have been rated below the company average performance standards for the Review period April YYYY to March YYYY.<br><br>We will closely monitor your performance for the next 30 days starting today. During this period, your immediate supervisor will work closely with you and coach you on improving your performance. A review of your performance after 30 days will be conducted to see if you require any further assistance.<br><br>We sincerely hope the guidance and feedback given will help you in meeting the company standards. We look forward to see you excel in your work and continue to be an asset for the organization.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>Human Resources</b>'
		htvalue+='<br>*Signature/ mail*</p>'
	}
	else if(frm.doc.template7=='Background Check'){
		var htvalue='<h2 style="text-align:center"><u>Background Check Verification</u></h2>'
		htvalue+='<br><br>To <b>'+frm.doc.candidate_name+',</b>'
		htvalue+='<br><br><p style="text-indent:70px">The purpose of this letter is to verify that the given employee worked with our organization <b>'+frm.doc.candidate_name+',</b> was an employee of our company for the duration of <b>___</b> year/months from <b>hire date</b> to <b>term date</b>. He was employed as <b>____</b>. His/Her gross salary was <b>___</b>. He/she was part/full-time employee.<br><br>He/She was a very dedicated employee with exceptional skills.<br><br>Please feel free to contact us if there is a need for any question or additional information that you think is required.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Birthday Wish'){
		var htvalue='<h2 style="text-align:center"><u>Happy Birthday!</u></h2>'
		htvalue+='<br><br>To <b>'+frm.doc.candidate_name+',</b>'
		htvalue+="<br><br><p style='text-indent:70px'>Happy Birthday Mrs./Mr ______. We want to personally thank you for your continuous effort and dedication.<br><br>You have been an <b>_____</b> figure for several employees and a dependable employee for the company.<br><br>We’d like to take this opportunity to thank you for your continuous effort and growth with our company.<br><br>To show you our appreciation we’ve prepared a gift basket for you. Please find it on your desk tomorrow.<br><br>We can happily say that the company and your team are glad to have you on board. We hope to see you have a prosperous year ahead.<br><br>Warm regard,</p>"
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Bonus Announcement'){
		var htvalue='<h2 style="text-align:center"><u>Bonus Announcement</u></h2>'
		htvalue+='<br><br>Hello <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">We are pleased to inform you that this year the company’s revenues have grown by <b>_____</b> per cent. <br>This truly wouldn’t have been possible without your hard work and commitment to the company. We at <b>_____</b> believe that our victories should be shared with everyone in the company.Therefore, we’ve decided on giving every employee a <b>_____ %</b> bonus based on their salary. Your bonus will be credited with your salary.<br>Once again, thank you for your enthusiasm and focus. We hope to see it continue in the future.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Branch Transfer'){
		var htvalue='<h2 style="text-align:center"><u>Branch Transfer</u></h2>'
		htvalue+='<br><br>To <b>'+frm.doc.candidate_name+',</b>'
		htvalue+='<br><br><p style="text-indent:70px">Your position as the <b>'+post+'</b> has been transferred to the <b>___</b> branch. This change will be applicable from <b>____</b>.<br><br>The decision has been made to _________ ( reasons to change ADD as per your application requesting the change, due to strategic change )<br><br>You need not worry, the terms and conditions of your employment agreement will remain the same.'
		htvalue+='<br>At this location, ll the necessary arrangements to make In this location, you will be provided with <b>___</b>. You must report to the location <b>________</b> on _____ and will be reporting to </b>______</b> . <br><br>In case of any queries please contact the HR department of the branch _____.<br><br>We wish you luck with your new workplace and hope to see you keep growing.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Breach of Employment'){
		var htvalue='<h2 style="text-align:center"><u>Breach of Employment</u></h2>'
		htvalue+='<br><br>To <b>'+frm.doc.candidate_name+',</b>'
		htvalue+='<br><br><p style="text-indent:70px">Happy Birthday Mrs./Mr ______. We want to personally thank you for your continuous effort and dedication.<br>You have been an _____ figure for several employees and a dependable employee for the company.<br>We’d like to take this opportunity to thank you for your continuous effort and growth with our company.<br><br>To show you our appreciation we’ve prepared a gift basket for you. Please find it on your desk tomorrow.<br><br>We can happily say that the company and your team are glad to have you on board. We hope to see you have a prosperous year ahead.<br><br>Warm regard,'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Condolence Letter'){
		var htvalue='<br><br>To <b>'+frm.doc.candidate_name+',</b>'
		htvalue+='<br><br><p style="text-indent:70px">We’re so sorry to hear about your ____’s death. Losing a loved one is always a difficult experience to endure. It changes who we are as people.<br><br>You are entitled to _ days of paid leave as per the company policy. If business-related work or travel are involved you can request for leaves up to a week. You can contact your manager for the same.<br><br>We wish for them to be in a better place and be happier where they are now. We are here to help you through this time. If there are other ways that we can help you, please let us know.<br><br>Warm Regards,</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>__________</b>'
	}
	else if(frm.doc.template7=='Contract Termination'){
		var htvalue='<br><br>To <b>'+frm.doc.candidate_name+',</b>'
		htvalue+='<br><br><p style="text-indent:70px">We regretfully inform you that the services of your company will no longer be required. Therefore, we seek the termination of our contract. This letter serves as an official notice for termination of the contract we will be serving the notice period of 30 days as per the signed contract.<br><br>Following are the reason for the termination<br><ul><li>Inability to deliver</li><li>Untimely delivery</li><li>Unprofessional behaviour</li><li>Lack of requirement of the products</li></ul><br><br>However, we will not cancel any orders already agreed to before this letter, unless clearly mentioned otherwise. Ideally, these services should be completed as normal. Please send any pending payment invoices, we will process them at our normal payment cycle.<br><br>We thank you for providing your services to us for __ years.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Critical Employee Talent Pool'){
		var htvalue='<h2 style="text-align:center"><u>Talent Pool</u></h2>'
		htvalue+='<br><br><p style="text-align:right">Date: <DATE></p><br><p style="text-align:left">To, <br>NAME,<br>COMPANY NAME,<br>ADD1,<br>ADD2,<br>CITY - PINCODE<br>STATE.<br><br><br>Dear <b>'+frm.doc.candidate_name+',</b></p>'
		htvalue+='<br><br><p style="text-indent:70px">Every company functions like a machine and every part is important. However there are certain key components which are directly related to the output. At <COMPANY NAME>, we hold our critical talent pool in really high regards and you certainly belong to the elite group.<br>With our Vision and Missions aligned, we really appreciate your contributions to achieving our objectives and goals as an organization and as well as your colleagues.<br><br>That being said, the Company will continue to look forward to your invaluable contributions and working towards future goals and ambitions. Additionally, the company would like you to undertake certain responsibilities apart from your job description to have you more involved in the company’s core business. We’ll be setting up a face-to-face meeting to gauge these further and get your views on the same.<br><br>Thanks in advance!</p.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Demotion Letter'){
		var htvalue='<h2 style="text-align:center"><u>Demotion Letter</u></h2>'
		htvalue+='<br><br><p style="text-align:right">Date: <DATE></p><br><p style="text-align:left">To, <br>NAME,<br>COMPANY NAME,<br>ADD1,<br>ADD2,<br>CITY - PINCODE<br>STATE.<br><br><br>Dear <b>'+frm.doc.candidate_name+',</b></p>'
		htvalue+='<br><br><p style="text-indent:70px">As discussed, this letter is an official notice to inform you regarding the changes in your position as a ___ (mention the changes compensation, reporting, etc) due to lack of performance after repeated warnings.<br><br>(Or due to underperformance in the performance report due to the inability to deal with changing environment due to unprofessional behaviour.<br>due to the company facing financial problems<br>due to the restructuring of the company.<br>due to a financial crisis )<br><br>You will now report to __ and your cost to the company will be ____.<br>Your job role will include -<br><br>We will review this decision in six months. We sincerely hope you take this as a challenge and work on improving your skill set with feedback from your seniors.<br>>br>Kindly report to ___ on ___ to be briefed regarding your new role. Please read through the job description attached to the letter.<br>Please reply with an acknowledgement to the mail.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Educational Reference Check'){
		var htvalue='<h2 style="text-align:center"><u>Educational Reference Check</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b>'
		htvalue+='<br><br>Hope you have a good day!<br><p style="text-indent:70px">Your contact information was provided to us by our job applicant _____ for our company the_____. He/She mentioned that they graduated _________ from your university in _____.<br><br>We are sending this mail to inform you regarding the same and confirm the above information. I have attached his/her resume below along with auxiliary documents.<br><br>If the above information is accurate we request you to please confirm that by replying to the email. If there are any queries please feel free to contact me at _____.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Employee Recognition'){
		var htvalue='<h2 style="text-align:center"><u>We appreciate your efforts and your services</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b>'
		htvalue+='<br><br><p style="text-indent:70px">We would like to take this opportunity to recognise your great services for the company. Your efforts to make the __ project successful are duly noted. Your ability to ___ and ___ have proved extremely valuable in the tense situation.<br><br>You were able to meet the difficult deadline with quality work, which shows your true capabilities. All of us and your co-workers are impressed by your work.<br><br>We are grateful to have an employee like you with us who isn’t just focused but an inspiration to other employees too. We hope you keep growing in the same way and wish you all the very best for the future.<br><br>Thank you,'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Employee Retention'){
		var htvalue='<h2 style="text-align:center"><u>EMPLOYEE RETENTION BONUS AGREEMENT</u></h2>'
		htvalue+='<br><br><b>TERMS: </b><br><br>You can refer to this list if you are not familiar with the terms mentioned throughout this Employee Retention Bonus Agreement. <ul><li><b>Incentive</b> - It encourages or motivates employees to work harder and aim for a better output. This usually comes in the form of, but not limited to, cash bonuses.</li><b>Retention Bonus</b> - It is a monetary, sometimes non-monetary incentive given by employers to employees as a way to make them stay with the company. This is usually given to an employee who is considering leaving the company. </li><li><b>Retention Period</b> - The duration of time an employee has to stay on a company for compliance purposes. ,/li.</ul>'
		htvalue+='<br><br><b>PURPOSE:</b><br><br>This Employee Retention Bonus Agreement serves as a contract between <b>WTT INTERNATIONAL PVT LTD</b> and <b>'+frm.doc.candidate_name+'</b>, whereby the company agrees to pay a bonus to the mentioned employee as an incentive if he/she continues to serve the company within the given period. Whereas, the employee agrees to continue his/her service with the company with conviction and dedication throughout the retention period, which is essential for the continuity and success of the business. <br><br>Furthermore, the bonus provided is in consideration of the performance exerted and the satisfaction of the executive as determined based on the criteria mentioned in Responsibilities. '
		htvalue+='<br><br><b>TERMS AND AGREEMENT</b><br><br>The terms of this Employee Retention Bonus Agreement shall take effect from [AGREED START DATE] to [AGREED END DATE]. The agreement shall expire on the termination date and <b>WTT INTERNATIONAL PVT LTD</b> shall have no more obligations with <b>'+frm.doc.candidate_name+'</b>, at that time. Any disagreement in this law entered by both parties in the state of [STATE] shall be arbitrated by [THIRD PARTY].'
		htvalue+='<br><br><b>SCOPE & LIMITATIONS</b><br><br><ul><li>This Employee Retention Bonus Agreement shall only be applied to the above-mentioned employee and non-transferable to any other employees or its successor.  </li><li>This Employee Retention Bonus Agreement is considered null and void if found out to be inactive or if any of the Section B violations mentioned in this agreement are performed.</li><li>This Employee Retention Bonus Agreement shall only be received if the employee remains employed at <b>WTT INTERNATIONAL PVT LTD</b> from [AGREED START DATE] to [AGREED END DATE] unless terminated early by the company.,/li></ul>'
		htvalue+='<br><br><b>EMPLOYMENT PERIOD:</b><br><br>As acknowledged and agreed by <b>'+frm.doc.candidate_name+'</b>, and <b>WTT INTERNATIONAL PVT LTD</b>, the employee shall remain employed as <b>'+post+'</b> at <b>WTT INTERNATIONAL PVT LTD</b> from [DATE] to [DATE]. The work shall be from [DATE] to [DATE], and your shift shall start from [TIME] to [TIME] with a total of [NUMBER] shift hours. '
		htvalue+='<br><br><b>ORGANIZATION STRUCTURE:</b><br><br>The employee shall be placed in the [NAME OF DEPARTMENT] under the management of [NAME OF SUPERVISOR].<br>The employee will immediately report to [NAME OF SUPERVISOR] to receive further instructions'
		htvalue+='<br><br><b>RESPONSIBILITIES:</b><br><br>In accordance with the company protocol and office guidelines, the employee shall be responsible for executing the following throughout the retention period:<br><b>a.	PRODUCTIVITY</b><ul><li.produce quality outputs</li><li>meet the daily or monthly target productivity</li><li>finish tasks and responsibilities within the given time</li><li>[INSERT OTHER RESPONSIBILITIES HERE] </li></ul><br><b>b.	WORK ETHICS</b><br><ul><li>avoid tardiness and absences</li><li>work with expertise, honesty, and professionalism</li><li>follow the company rules and regulations </li>[INSERT OTHER RESPONSIBILITIES HERE]</li></ul><br><br><b>COMPENSATION AND BENEFITS:</b><br><br>The employee shall be provided with the following compensation during and after his/her retention period from [DATE] to [DATE]:<br><ul><li>a compensation of [INSERT AMOUNT] per month</li><li>Health Maintenance Organization (HMO) insurance with [NUMBER] dependents</li><li>a bonus of [INSERT AMOUNT] once the retention period is completed</li><li>an incentive of [INSERT AMOUNT] for after quotas and perfect attendance</li><li>[INSERT OTHER COMPENSATION AND BENEFITS HERE]</li></ul><br><br><b>RETENTION BONUS:</b><br><br>The employee will receive a retention bonus equivalent to no less than [NUMBER]% of his/her salary if he/she successfully completes the following on or before the end of his/her retention period on [DATE]:<ul<li>submit the necessary documents for the assigned projects </li><li>finish the projects in hand within the given time frame</li><li>[INSERT OTHER RETENTION BONUS REQUIREMENT],</li></ul>'
		htvalue+='<br><br><b>SAFETY AND SECURITY:</b><br><br>To ensure that the employee will not be injured and/or harmed throughout his/her employment, the following measures will be established:<br><ul><li>Undergo a physical examination as some accidents are due to the inability to perform physically.</li><li>Training about the importance of following the company’s safety guidelines </li><li>Monitor safety measures </li><li>Provide protection equipment </li><li>[INSERT MORE SAFETY AND SECURITY MEASURES HERE]</li></ul>'
		htvalue+='<br><br><b>VIOLATIONS:</b><br><br>The following actions will be considered in violation of this Employee Retention Bonus Agreement and may subject the employee for disciplinary actions or hinder the employee from getting the promised bonus, as will be determined by an authorized representative from the human resources department.<br><br><b>Section A</b><br><ul><li>Failure to submit daily tasks by the end of the shift</li><li>[INSERT NUMBER HERE] consecutive tardiness and absences</li><li>Refusing to follow instructions provided by the company or team lead</li><li>Dishonesty and falsification</li><li>Misuse of any equipment provided by the company</li><li>[INSERT OTHER VIOLATIONS HERE]</li></ul>'
		htvalue+='<br><br><b>Section B</b><br><ul><li>Bringing of illegal drugs and paraphernalia or firearms within the company premises</li><li>Posing verbal and nonverbal abuse or threat to co-employee(s) </li><li>Performing harmful acts that lead to another person in danger</li><li>[INSERT OTHER VIOLATIONS HERE]</li></ul><br><br>When any of the violations in Section A is performed, a Notice to Explain (NTE) shall follow. This may or may not lead to a revocation in this Employee Retention Bonus Agreement. Any of the violations performed in Section B will automatically consider this Employee Retention Bonus Agreement as null and void.'
		htvalue+='<br><br><b>INTELLECTUAL PROPERTY:</b><br><br>Any and all of the regulations specified in this Employee Retention Bonus Agreement are considered confidential and may not be used for any other purpose/s not specified by <b>WTT INTERNATIONAL PVT LTD</b>.'
		htvalue+='<br><br><b>IN WITNESS WHEREOF</b> the following are the names of individuals who agree to all of the rules and regulations specified in this Employee Retention Bonus Agreement signed this [DATE] at [VENUE]:'
		htvalue+='<br><br><p style="text-align:left">Signature of Admin</p><p style="text-align:right">Signature of Employee</p>'
	}
	else if(frm.doc.template7=='Farewell Letter'){
		var htvalue='<h2 style="text-align:center"><u>We’re sad to see you go</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+'</b>,'
		htvalue+='<br><br><p style="text-indent:70px">We are aware that tomorrow will be your last official day with the company. We are happy that you are moving on to_____.<br><br>Having you in the company has been a great decision. Your skills are exceptional, however, it is your personality that truly brightens up the office. We all will awfully miss your presence here.<br><br>However, some difficult steps are required to be taken. A farewell basket will be on your desk tomorrow. We hope you’ve had as memorable a time with us as we did with you.<br><br>We wish you all the very best for the future.Thank you for your service to the company.'
		htvalue+='<br><p style="text-align:right;">Best Regards,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Festival Bonus'){
		var htvalue='<h2 style="text-align:center"><u>Festival Bonus</u></h2>'
		htvalue+='<br><br><p style="text-align:right">Date: <DATE></p><br><p style="text-align:left">To, <br>NAME,<br>COMPANY NAME,<br>ADD1,<br>ADD2,<br>CITY - PINCODE<br>STATE.<br><br><br>Dear <b>'+frm.doc.candidate_name+',</b></p>'
		htvalue+='<br><br><p style="text-indent:70px">This year has really been a handful globally with the onset of Covid-19 pandemic and it surely has been hard on the company as well. The company hereby wants to express their deepest gratitude to you for being a strong part of our journey.<br><br>To show our appreciation and with the auspicious festival of Diwali, the Company has decided for a Bonus pay-out of <PERCENTAGE>% on your annual CTC.'
		htvalue+='<br><br><b>Applicability:</b><br><ol><li>The Bonus shall only be applicable to employees who have completed a minimum of <No. of months> months in the current financial year</li><li>The Bonus shall be paid out with your next monthly salary</li><li>The Bonus shall be pro-rated according to number of months completed in this Financial Year</li>No Bonus amount shall be paid to employees serving their notice period or have been terminated from the company on or before the date of announcement of the Bonus</li></ol>'
		htvalue+='<br><br>Please feel free to contact us if there is a need for any question or additional information that you think is required.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Diwali Festival'){
		var htvalue='<h2 style="text-align:center"><u>Happy Diwali!</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b>'
		htvalue+='<br><br>Hope you have a good day!<br><br><p style="text-indent:70px">On behalf of the company, we wish you a very Happy Diwali. This year we would like to take this time and appreciate all the effort and work put into making people’s lives better with _____ (product)<br><br>It has been a pleasure to watch each one of our employees grow steadily and fit better to their respective goals. This has resulted in increased revenue for our company. We are looking to reach our target of __ % year on year growth by April. That is because of you all.<br><<br>We welcome the festival of lights with all our hearts and hope your homes are also filled with laughter and happiness. To help put a smile on your faces we’ll besending out your salaries a lot earlier. So you don’t have to wait to start celebrating the festival of lights.<br><br>Furthermore, as per company policy, you will also receive __ days of paid leave.<br><br>We hope you have good celebrations and come back rejuvenated with brand new energy!'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Independence Day'){
		var htvalue='<h2 style="text-align:center"><u>Independence Day</u></h2>'
		htvalue+='<br><br>Hello <b>'+frm.doc.candidate_name+',</b><br><br>We wish you a very Happy ___ Day! Today is a special day for our country. As a proud company based in India, we take immense pride to celebrate the _____ day of our country.<br><br>As per our company policies, the __ of ___ will be a holiday for all our employees.<br><br>We urge you to take part in any celebration or recital of a national anthem on that day. We will also gather together on the __ for honouring our national flag and singing the national anthem together.<br><br>We hope to see you there for the same.<br><br>Jai Hind.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Christmas'){
		var htvalue='<h2 style="text-align:center"><u>Merry Christmas!</u></h2>'
		htvalue+='<br><br>Hello <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">On behalf of the company, we wish you a very Merry Christmas. We hope all your stockings are full of love and joy.<br><br>This evening we’ll have cookies along with coffee in the cafeteria for you. We invite you to join the merriment along with your coworkers.<br><br>As per company policy, the 25th of December ___ will be a paid leave.<br><br>We hope you have a wonderful time with your family and join us back on the 26th.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='EID'){
		var htvalue='<h2 style="text-align:center"><u>EID MUBARAK</u></h2>'
		htvalue+='<br><br>Hello <b>'+frm.doc.candidate_name+',</b><br><br>Eid Mubarak to all our employees from the company’s behalf. We wish prosperity and growth in each one of your lives.<br><br>We appreciate the sincerity and hard work you put into the company’s everyday tasks. Which is why this Eid will be a holiday for all our employees. We only wish for you all to keep growing and achieving bigger and better things.<br><br>We wish you all the best for the year ahead and hope you enjoy your celebrations with great zeal and gusto.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'

	}
	else if(frm.doc.template7=='Holi'){
		var htvalue='<h2 style="text-align:center"><u>Holy HOli!</u></h2>'
		htvalue+='<br><br>Hello <b>'+frm.doc.candidate_name+',</b><br><br>We wish you a very happy Holi on behalf of the company. We hope you have a joyful celebration of the day created to celebrate good over evil.<br><br>Though we welcome all celebrations and festivities we urge our employees to refrain from using water this year.<br><br>We hope you have a great year ahead and wish you all the best for your future.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Follow Up'){
		var htvalue='<h2 style="text-align:center"><u>Follow Up</u></h2>'
		htvalue+='<br><br><p style="text-align:right">Date: DATE</p><br><p style="text-align:left">To, <br><br><br>Dear <b>'+frm.doc.candidate_name+',</b></p>'
		htvalue+='<br><br><p style="text-indent:70px">Trust this mail finds you well.<br><br>Just circling back to follow up regarding the ____ I had sent across to you on _____. Could you please share a timeline from your side regarding the same.<br>Do let me know if you have any questions regarding the same.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Granting Permission'){
		var htvalue='<h2 style="text-align:center"><u>Granting Permission</u></h2>'
		htvalue+='<br><br>Hello <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">I have received your request for ______. I am writing this letter to grant ___ permission to ____ for the ____.<br><br>We, ______, fully support your decision and encourage you to _____. Kindly inform yourmanager and team regarding the same.<br><br>We hope you succeed in this new endeavour and wish you all the best for the future. If there are any further queries or requirements please feel free to contact me.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b>'
	}
	else if(frm.doc.template7=='Incident Report'){
		var htvalue='<h2 style="text-align:center"><u>Clarification regarding a recent incident</u></h2>'
		htvalue+='<br><br>Hello <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">In light of recent events, there have been several speculations regarding the recent incident. We believe that our employees have the right to know the reason behind certain decisions that the company must make. Therefore, we have attached the complete incident report below, shedding light on the recent incident that has taken place in the company.<br>This letter is to document clear information regarding the incident that occurred on ___ of __ .<br><br>On the __ of ____ 20_ at ____ Ram used the company laptop to communicate with thecompany’s competitors. He shared sensitive financial data with them through the laptop. Evidence of the same has been found through the company server and through our CCTV cameras.<br>This made our security team spring to action and inform Ram’s manager and the HR department at __.<br><br>We checked the evidence and have heard Ram’s explanation. A committee was set up on __ to discuss this matter which resulted in Ram’s termination. However, due to our vigilant security guards, we were able to avoid a major financial loss.We have informed Ram regarding the immediate termination of his services and will take further steps to improve the security of our workplace.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
		htvalue+='<br><br><b>Points to keep in mind -</b><br><ul><li>Write in the first-person voice</li><li>Mention the clear details of the event with time stamps</li><li>Conclude with actions that the company has taken regarding the incident,/li></ul>'
	}
	else if(frm.doc.template7=='Inter-Department Transfer Letter'){
		var htvalue='<h2 style="text-align:center"><u>Inter-Department Transfer Letter</u></h2>'
		htvalue+='<br><br><p style="text-align:right">Date: DATE</p><br><p style="text-align:left">To, <br><br><br>Dear <b>'+frm.doc.candidate_name+',</b></p>'
		htvalue+='<br><p style="text-indent:70px">This letter will serve as an official notice to inform<br>We are writing this letter to inform you that your role will be transferred from the ___ department to the _____ department from ___.<br>This is because ________of the ____ department. We believe your skillset will be able to fulfill the requirement in the department.<br>We’re excited to see you join the department. We are sure you will be fit in perfectly.<br>You must report to _____ at ____ am. If you have any questions please get in touch with ____ .'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Job Transfer'){
		var htvalue='<h2 style="text-align:center"><u>JOB TRANSFER</u></h2>'
		htvalue+='<br><br><p style="text-align:right">Date: DATE</p><br><p style="text-align:left">To, <br>NAME,<br>COMPANY NAME,<br>ADD1,<br>ADD2,<br>CITY - PINCODE<br>STATE.<br><br><br>Dear <b>'+frm.doc.candidate_name+',</b></p>'
		htvalue+='<br><br><p style="text-indent:70px">Trust you are doing well!Due to internal restructuring and re-allocation of resources, the company has decided to reassign your position as a <b>'+post+'</b> in the <b>DEPARTMENT NAME</b> to our <b>BRANCH NAME</b> effective from <b>EFFECTIVE DATE</b>.<br>Your new role in the branch will be as a <b>NEW DESIGNATION</b> in the <b>NEW DEPARTMENT</b>.<br><br>Your new responsibilities will be as follows,<br><ul><li>RESPONSIBILITY1</li><li>RESPONSIBILITY2</li><li>RESPONSIBILITY3</li></ul><br>The company has also decided to increase your CTC to <b>REVISED CTC</b>.In all other aspects, the terms and conditions of your employment will remain the same. Your new reporting manager at the branch will be <b>REPORTING MANAGER</b>.Feel free to reach out in case of any queries. </p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Letter Commenting for Emergency'){
		var htvalue='<h2 style="text-align:center"><u>You Are A Hero!</u></h2>'
		htvalue+='<br><br><p style="text-align:right">Date: DATE</p><br><p style="text-align:left">To, <br><br><br>Dear <b>'+frm.doc.candidate_name+',</b></p>'
		htvalue+='<br><br><p style="text-indent:70px">I am writing this letter, on behalf of the company to commend you for handling the emergency situation that occurred on ____ well.<br><br>Your ability to stay calm under a tense situation has not only saved us money but has also protected the company’s reputation. We commend your quick wit and resourceful nature. Thank you for being present and stepping up in the face of danger.<br><br>Thank you for your courage in times of despair.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Opportunities for Voluntary Services'){
		var htvalue='<h2 style="text-align:center"><u>An opportunity for voluntary services</u></h2>'
		htvalue+='<br><br><p style="text-align:right">Date: DATE</p><br><p style="text-align:left">To, <br><br><br>Dear <b>'+frm.doc.candidate_name+',</b></p>'
		htvalue+='<br><br><p style="text-indent:70px">With immense pleasure, the company would like to inform you that the company has joined hands with the ____ NGO to ______ the _____. As per, the association the company will be undertaking the task of ____ at the ____ premise.<br><br>This brings a unique opportunity to sign up for volunteering service and reconnect with your co-workers while giving back to society at the same time. If we see employee participation we will continue to bring such volunteering opportunities to you time and again.<br><br>If you are interested to join in, simply reply to this mail with your<br><ul><li>Name</li><li>Employee ID</li><li>Contact number</li></ul><br>Do so before the __ of ___ 20_.<br><br>Hope to see you there</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Inviting Employee to Investigatory Interview'){
		var htvalue='<h2 style="text-align:center"><u>Inviting Employee to Investigatory Interview</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px"><b>Notification of investigatory interview </b><br><br>I am writing to inform you that the company has decided it is necessary to conduct an investigation into the following allegation of misconduct:<br><ul><li>[Summarise details of each issue being investigated in bullet points]</li></ul>The aim of the investigation is to establish the facts of the matter by gathering as much relevant facts and information as possible. It is currently expected that the investigation will be completed by <b>[day, month]</b> or as soon as reasonably possible. <br>You are required to attend an investigation meeting on <b>[date of the meeting]</b> at [time of the meeting] at [location of the meeting]. <br><br>In attendance at the meeting will be <b>[name of investigating manager]</b> and [name of note-taker], who will be present to take notes. Please bring with you any information that you think might be useful to the investigation.<br><br>Once the investigation has been completed, you will be informed in writing of its outcome. If it is found that there is a case to answer, you will be invited to attend a formal disciplinary hearing.  <br><br>In the meantime, should you have any information that might be of assistance to the investigation or wish to discuss anything, please do not hesitate to contact [name of investigator/line manager/HR department]. Their contact details are [telephone number, email address].<br><br>To ensure that the investigation can be conducted as fairly as possible we request that you keep the matter confidential. Any breach of confidentiality may be considered to be a disciplinary matter. </p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Letter for Appointment'){
		var htvalue='<h2 style="text-align:center"><u>Letter for Appointment</u></h2>'
		htvalue+='<br><br><p style="text-align:right">Date: DATE</p><br><p style="text-align:left">To, <br>NAME,<br>COMPANY NAME,<br>ADD1,<br>ADD2,<br>CITY - PINCODE<br>STATE.<br><br><br>Dear <b>'+frm.doc.candidate_name+',</b></p>'
		htvalue+="<br><br><p style='text-indent:70px'>Appointment as <b>...............</b>.<br><br>We refer to your recent interview for the above position and are pleased to advise that <br>we are offering you the position with our Company effective from ...................................... under the following terms and conditions: <b>1.SALARY </b><br>Your salary will commence at <b>₹...................</b> per month. <br><br><b>2.PROBATIONARY PERIOD: </b><br>Your appointment will be subject to a probationary period of 3 months. An official confirmation of your appointment will be notified to you in writing. <br><br><b>3.WORKING HOURS: </b><br>Your working hours will be as follows:  <br>Mon - Fri   : <br>Lunch Break  :    <br>br>At times, you may be required to work irregular hours, including Saturday and Sunday. <br><br>Appropriate time off will be considered for work performed outside normal operational hours. <br><br><b>4.LEAVE OF ABSENCE </b>Leave of absence whether medical or annual will be given in accordance with the Company's Employee Handbook. Application on prescribed form for leave must be made one week in advance. " 
		htvalue+="<br><br><b>5.PAID LEAVE </b><br><b>5.1 ANNUAL LEAVE </b><br>The annual leave will be as follows:- <br>    a)Employed for 1 – 3 years        :        days <br>    b)Employed for 4 – 5 years        :        days <br>    c)Employed for more than 5 years        :        days <br>The maximum leave will be fixed at <b>.............</b> days. The leave will be taken at interval periods unless requested for special reasons such as an overseas trip. No leave will be granted immediately before/after Public Holidays. Employee may carry forward a maximum of … working days' unutilized leave to the following year and must be utilized by end of that year. <br><br><b>5.2 MARRIAGE LEAVE  </b><br>Permanent employees are entitled to ….days’ Marriage Leave.  <br><br><b>5.3 COMPASSIONATE LEAVE  </b><br>Permanent employees are entitled to:- <br>    a) days - death of spouse, child or parent <br>    b) day - death of parent-in-law, brother, sister or grandparent "
		htvalue+="<br><br><b>6.BONUS:</b><br><br>Bonus is dependent upon the Company's profitability and your performance. It is only payable at the end of one year’s service and will be paid before Chinese New Year. "
		htvalue+="<br><br><b>7. MPF </b><br>Deduction of employee’s contribution and employer’s share of contribution will be in accordance with the respective Ordinance currently enforced. <br><br><b>8.PERIOD OF NOTICE FOR TERMINATION OF EMPLOYMENT </b><br>Period of notice for termination of employment or salary in lieu shall be as follows:-  <br>    <b>a)First month of probation</b> — without notice  <br>    <b>b)Second month till probation end</b> — 7 days  <br>    <b>    c)After probation</b> — 1 month <br>Leave cannot be utilized as resignation notice. <br><br><b>9. FRINGE BENEFITS   </b><br>Upon satisfactory completion of the probation period, you will become our permanent employee and are entitled to the fringe benefits specified in the Employee Handbook. <br>You are required to serve the Company with loyalty and honesty and strictly follow all instructions given to you by your supervisors in carrying out your duties. <br>You shall not take or engage in any other employment, trade, business, whatsoever outside the business of the Company during the period of your employment. <br><br><b>10. CONFIDENTIALITY </b><br>You shall not at any time during or after your employment term with the Company reveal any of the affairs or secrets of the Company to any other person(s) nor use or attempt to use any information which you may acquire in the course of your employment in any manner which may injure or cause loss to the Company. <br><br><b>11. RESIGNATION/TERMINATION </b><br>The Company shall be at liberty at any time by notice in writing summarily terminate the service of the employee if:- <br>    a) she/he is guilty of misconduct; <br>    b) she/he is negligent in the discharge of her/his duties; or  <br>    c) being absent or being unable to perform her/his duties and alleging ill-health as the cause thereof, she/he shall refuse to practitioner nominated by the company to examine her/him or shall fail to give to such medical practitioner the information necessary to report upon her/his state of health. <br><br>Upon resignation or termination of service, you shall deliver to the person in charge all documents in your possession which belong to the company. "
		htvalue+="<br><br>To avoid any doubt, it is hereby declared that the property and all such documents used in the course of your work belong to the company. <br><br>If you are agreeable to the above terms and conditions of the appointment, kindly confirm your acceptance by signing and returning the duplicate copy of this letter for our file and records. </p>"
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Employee Pending Disciplinary Investigation'){
		var htvalue='<h2 style="text-align:center"><u>Letter suspending employee pending disciplinary investigation </u></h2>'
		htvalue+='<br>Employees should only be suspended in cases of suspected gross misconduct where it is considered there may be a real risk to persons, property or evidence if the employee remains in the workplace.'
		htvalue+='<br><br><p style="text-align:right">Date: DATE</p><br><p style="text-align:left">To, <br>NAME,<br>COMPANY NAME,<br>ADD1,<br>ADD2,<br>CITY - PINCODE<br>STATE.<br><br><br>Dear <b>'+frm.doc.candidate_name+',</b></p>'
		htvalue+="<br><br><p style='text-align:center'><b>Suspension pending disciplinary investigation</b><br><br></p><p style='text-indent:70px'>I am writing to confirm that you have been suspended from work until further notice with immediate effect pending investigation into the following allegation of gross misconduct: <br><ul<li>[Summarise details of allegation]</li></ul><br>Your suspension does not amout to disciplinary action and does not imply that you are guilty of any misconduct. We will keep the matter under review and will aim to make the period of suspension no longer than is necessary..<br><br>During your suspension, we shall continue to pay your salary in the normal way. You are also entitled to your normal contractual benefits. You remain bound by your contract of employment during your suspension. <br><br>You are required to co-operate in our investigations and may be required to attend investigatory interviews or disciplinary hearings. You should not attend the workplace unless authorised by [NAME] to do so. You must not communicate with any of our employees, contractors or customers unless authorised by [NAME]. However, you are required to be available to answer any work-related queries. <br><br>A copy of our Disciplinary Procedure is enclosed. When we have completed the investigation, we will write to confirm whether you will be required to attend a disciplinary hearing. If we consider that there are grounds for disciplinary action we will inform you of those grounds in writing and you will have the opportunity to state your case at the hearing, in accordance with the Disciplinary Procedure.<br><br>If you have any queries about this matter or the terms of your suspension please feel free to contact me.</p>"
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='College Internship'){
		var htvalue='<b>To</b><br>The Principal/Placement Committee,<br>__________ College,<br>Place.<br><br><b>Respected Sir/Madam,</b><p style="text-align:center"><b>SUB:</b> INTERNSHIP AVAILABLE BETWEEN __________ AND _____________</p><br><br><b>Introducton :</b><br>_____________________________________<br>_____________________________________ '
		htvalue+='<br><br><b>Internship Summary</b><br><br>Website: ____________________________________<br>Location for Internship: _____________________<br>DURATION: ______________ Month(Can be extended upon availability)<br>Number of Internships available: ______________________<br><br><b>Who can apply: </b>Only those candidates can apply who:<ul><li>Are available for full time (in-office) Internship.</li><li>Can start the internship between _______________ and ___________</li><li>Are available for duration of _____ months</li>'
		htvalue+='<li>Have relevant skills and interests</li><li>Students from morning and evening batch can apply</li></ul><br><b>Responsibilities and Duties : </b><br><ul<li>Assisting the other employees </li>Coordinating with clients</li></ul><br>(Insert here Work to be done by the intern)<br><br><b>Key Skills : </b>MS-Office, MS-Word and MS-Excel<br><br><b>Benefits : </b>Certificate, Letter of recommendation, Flexible work hours, Mentoring.<br>It will be a Full-time Internship, Stipend of <b>Rs. _____________/- per month</b> will be paid to the intern.<br>If any further clarification is required kindly feel free to drop an email to the undersigned.<br><p style="text-align:center">Thanking You,</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Employee Disciplinary Hearing - Confirming'){
		var htvalue='<h2 style="text-align:center"><u>Letter to Employee confirming outcome of Disciplinary Appeal Hearing</u></h2>'
		htvalue+='<br><br>[Employee name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">I am writing to inform you of the outcome of the appeal hearing conducted on [date]. <br>I have decided to [uphold OR change] our original decision that [DETAILS OF ORIGINAL DECISION]. <br><br>[My new decision is that [DETAILS OF NEW DECISION].]<br><br>The arrangements for dismissal set out in the letter of [DATE] [remain the same] OR [are [revoked] OR [will be varied as follows [INSERT NEW ARRANGEMENTS INCLUDING EFFECT ON CONTINUITY OF EMPLOYMENT AND SALARY]].<br><br>You have now exercised your right of appeal under the Disciplinary Procedure and this decision is final. '
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Employee Disciplinary Hearing - Dismissal'){
		var htvalue='<h2 style="text-align:center"><u>Letter to Employee confirming outcome of Disciplinary Appeal Hearing - Dismissal</u></h2>'
		htvalue+='<br><br>[Employee name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">You attended a disciplinary hearing on [DATE]. I am writing to confirm that it has been decided that your employment should be terminated on grounds of your conduct.<br><br>At the disciplinary hearing, the following allegations were found proven: [set out each allegation of misconduct and summarise the findings in respect of each]. <br><br>You were previously given warnings on [DATES] about your conduct. Your final written warning dated [DATE], which is still active, warned you that if there was any further misconduct prior to its expiry, you may be dismissed. <br><br>If you wish to appeal against this decision you should inform [NAME] in writing by [DATE], stating your grounds of appeal in full.<br><br>The following arrangements apply with immediate effect (but may be varied or revoked in the event of a successful appeal):<br><ul><li>[You are entitled to [LENGTH] notice under your contract of employment and your final day of employment will be [TERMINATION DATE]] OR [Your employment will terminate with immediate effect from [DATE] and you will receive [AMOUNT] pay in lieu of notice in accordance with your contract of employment.]</li><li>[You will be paid for [NUMBER] days’ accrued but outstanding holiday, calculated pro rata up to the end of your employment] OR [You have taken [NUMBER] days’ holiday in excess of your pro rated holiday entitlement and the sum of £[AMOUNT] will therefore be deducted from your final salary payment. </li><li>[You will be reimbursed for any genuine expense claims submitted by [DATE] with your final payment of salary.]</li>'
		htvalue+='<li>You must return all company property including [INSERT DETAILS SUCH AS MOBILE PHONE, LAPTOP COMPUTER, CONFIDENTIAL DOCUMENTS] belonging to us in good condition by [DATE].</li><li>Your final payment of salary shall be made on [DATE], subject to normal deductions of tax and National Insurance contributions. We shall forward your P45 to you in due course.</li></ul><br><br>You will remain bound by any confidentiality and restrictive covenant clauses in your contract of employment. <br>If you have any further questions please do not hesitate to contact me.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Employee Disciplinary Hearing - Final Warning'){
		var htvalue='<h2 style="text-align:center"><u>Letter to Employee confirming outcome of Disciplinary Appeal Hearing - First and Final Warning</u></h2>'
		htvalue+='<br><br>[Employee name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">You attended a disciplinary hearing on [date]. At this hearing, the following allegations were found proven: [set out allegations that were upheld].<br><br>It has therefore been decided to issue you with a [first] OR [final] written warning.<br>This warning will be placed in your personal file but will be disregarded for disciplinary purposes after a period of [Number] months. [ACAS suggests that first written warnings should remain active for 6 months and final written warnings for 12 months, but these figures are not set in stone] months, provided your conduct improves to a satisfactory level.<br><br>The conduct improvement expected is: [explain the standards of improvement expected] <br><br>The likely consequence of further misconduct during the period of this warning is:  [a final written warning] OR [Dismissal].<br><br>If you wish to appeal against this decision you should inform [NAME] in writing by [DATE], stating your grounds of appeal in full.<br><br>If you have any questions regarding this warning please contact [NAME].'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Employee Disciplinary Hearing - Dismissal for Gross Misconduct'){
		var htvalue='<h2 style="text-align:center"><u>Letter to Employee confirming outcome of Disciplinary Appeal Hearing - Dismissal for Gross Misconduct</u></h2>'
		htvalue+='<br><br>[Employee name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">You attended a disciplinary hearing on [DATE]. I am writing to confirm that it has been decided that your employment should be terminated with immediate effect on grounds of your gross misconduct.<br><br>At the disciplinary hearing, the following allegations were found proven: [set out each allegation of misconduct and summarise the findings in respect of each. Explain why the conduct was so serious as to warrant summary dismissal]. <br><br>You were previously given warnings on [DATES] about your conduct. Your final written warning dated [DATE], which is still active, warned you that if there was any further misconduct prior to its expiry, you may be dismissed. <br><br>If you wish to appeal against this decision you should inform [NAME] in writing by [DATE], stating your grounds of appeal in full.'
		htvalue+='<br><br>The following arrangements apply with immediate effect (but may be varied or revoked in the event of a successful appeal):<br><ul><li>You are not entitled to receive any notice or notice pay.  Your employment will terminate with effect from [DATE]. </li><li>[You will be paid for [NUMBER] days’ accrued but outstanding holiday, calculated pro rata up to the end of your employment] OR [You have taken [NUMBER] days’ holiday in excess of your pro rated holiday entitlement and the sum of £[AMOUNT] will therefore be deducted from your final salary payment. </li><li>[You will be reimbursed for any genuine expense claims submitted by [DATE] with your final payment of salary.]</li><li>You must return all company property including [INSERT DETAILS SUCH AS MOBILE PHONE, LAPTOP COMPUTER, CONFIDENTIAL DOCUMENTS] belonging to us in good condition by [DATE].</li><li>Your final payment of salary shall be made on [DATE], subject to normal deductions of tax and National Insurance contributions. We shall forward your P45 to you in due course.</li><li>You will remain bound by any confidentiality and restrictive covenant clauses in your contract of employment.</li></ul><br><br>If you have any further questions please do not hesitate to contact me.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'		
	}
	else if(frm.doc.template7=='Employee Inviting to Disciplinary Appeal Hearing'){
		var htvalue='<h2 style="text-align:center"><u>Employee Inviting to Disciplinary Appeal Hearing</u></h2>'
		htvalue+='<br><br>[Employee name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">I am writing to inform you that you are required to attend an appeal hearing at [PLACE] on [DATE] at [TIME]. The purpose of the hearing is to consider your appeal against the decision taken at the disciplinary hearing held on [DATE] that you be [issued with a first OR final written warning] OR [dismissed with notice OR with immediate effect]. <br><br>The hearing will be conducted by [NAME] who will be accompanied by [NAME] to take a note of the hearing. You are entitled to bring a colleague or a trade union representative to the meeting in accordance with our Disciplinary Procedure. If you wish to bring a companion, please let me know their name as soon as possible.<br><br>I enclose copies of relevant documentation for use at the appeal. If there are any documents you wish to be considered at the appeal, please provide copies as soon as possible and in any event by no later than [DATE]. <br><br>If, for any unavoidable reason, you or your companion cannot attend at that time please contact me as soon as possible. If you have any questions, please also contact me as soon as possible.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Mediclaim'){
		var htvalue='<h2 style="text-align:center"><u>Letter to File MediClaim</u></h2><br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><p style="text-align:left"><b>To,</b><br>....<br>......<br>......<br><br><p style="text-align:center"><b>Subject</b> - Medi claim number_______</p>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">Hope this mail finds you well.<br><br>I work as the ____ of the ___ company. I would like to claim the medical insurance on behalf of our employee ____ under the insurance policy number ____.<br><br>On ___, He/She had a medical emergency ___ and was taken to the ____hospital. He/She was<br>(Describe the medical situation and about the employee’s condition).<br><br>I have attached all the required medical reports, bills and insurance details with this letter. I hope that our employee will be reimbursed by your company. Thank you for your cooperation.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Invite Employee to Disciplinary Hearing'){
		var htvalue='<h2 style="text-align:center"><u>Employee Inviting to Disciplinary Appeal Hearing</u></h2>'
		htvalue+='<br><br>[Employee name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">I am writing to inform you that you are required to attend a disciplinary hearing at [PLACE] on [DATE] at [TIME]. The purpose of the hearing is to consider the following allegation of [misconduct OR gross misconduct] against you:<br><ul><li>[SET OUT FACTUAL ALLEGATION - FOR EXAMPLE, "at [time] on [date] at [location] you assaulted another employee by [describe the assault]"].</li></ul><br><br>I enclose copies of relevant documents and statements from the investigation which may be used at the disciplinary hearing. [We intend to call the following witnesses to the hearing: [GIVE NAMES OF WITNESSES] OR We do not intend to call any witnesses to the hearing.] If you wish to call any relevant witnesses to the hearing please let us have their names as soon as possible and no later than [DATE]. If there are any further documents you wish to be considered at the hearing, please provide copies no later than [DATE]. <br><br>The hearing will be held in accordance with the company’s Disciplinary Procedure which is attached. If you are found guilty of misconduct we may decide to [issue you with a written warning or a final written warning OR dismiss you with notice or pay in lieu of notice]. [If you are found guilty of gross misconduct, you may be dismissed without notice or pay in lieu of notice.]<br><br>The hearing will be conducted by [NAME] who will be accompanied by [NAME] to take a note of the hearing. You are entitled to bring a colleague or a trade union representative to the meeting in accordance with our Disciplinary Procedure. If you wish to bring a companion, please let me know their name as soon as possible.<br>[Your suspension on full pay will continue pending the outcome of the disciplinary hearing.]<br><br>If, for any unavoidable reason, you or your companion cannot attend at that time please contact me as soon as possible. If you have any questions, please also contact me as soon as possible.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Reschedule Meeting'){
		var htvalue='<h2 style="text-align:center"><u>Request for Reschedule Meeting</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">I am writing this letter to inform you that unfortunately, the meeting that we had scheduled for __ has to be cancelled. This is due to the _______<br><br>However, we are still very much looking forward to meeting with you to discuss the ____. Would ______ work for you? Please let me know if it does.<br><br>Once again, you have my sincerest apologies regarding the inconvenience caused to you. I reached out to you as soon as I was informed regarding the change.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>____________</b></p>'
	}
	else if(frm.doc.template7=='Promotion'){
		var htvalue='<h2 style="text-align:center"><u>Promotion Letter</u></h2>'
		htvalue+='<br><br><b>To</b><br>[Employee name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">It is with immense pleasure and pride that we offer you a promotion from the role of ____ to the role of ____.<br><br>We appreciate your efforts and hard work for the company. Your recent work on _____ and your ability to handle _____ has proven that you’ll be extremely capable of fitting into this role.<br><br>Your annual cost to the company will be increased to ___ and you will be reporting to _____.<br><br>We will set up a review meeting in _ months of time to review your work in the new position. If we reach a positive conclusion in that meeting you will then be promoted permanently.<br><br>Please let us know about your acceptance by or before the ____ by signing the enclosed document to start the documentation process. If you have any question or require more information regarding this, you can contact _______.<br><br>We hope to see you in your new role soon.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Query Letter to Employee'){
		var htvalue='<h2 style="text-align:center"><u>Request for Reschedule Meeting</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">I am writing this letter to ask you a query regarding __ .<br><br>Please share the concerned details regarding the same. Please mention the ___ and the __.<br><br>Thank you for your time.'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Quotation Approval'){
		var htvalue='<h2 style="text-align:center"><u>Quotation Approval</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">We’d like to thank you for your quotation no. ____ It fits our budget. Therefore, we will be approving your quotation and will be placing an order with you.<br><br>We’ve attached the purchase order below and will be looking at the ___.<br>Please share the payment details. We’ll be awaiting the delivery by ____.</p><br><br><p style="text-align:center">Thank you,</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='Quotation Negotiation'){
		var htvalue='<h2 style="text-align:center"><u>Quotation Negotiation</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">Thank you for your quote of __ for __. However, we have to inform you that it goes a little over-budget for us. Please review our budget for the same.</p><br><table border="1" width="100%" style="text-align:center"><tr><td><b>PARTICULLAR</b></td><td><b>QUANTITY</b></td><td><b>QUOTE</b></td><td><b>OUR BUDGET</b></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr></table><br><br>'
		htvalue+='<p>We are looking at a price around ___. We can provide __ as an additional incentive for accepting our offer. Additionally, kindly let us know if there are any additional services being provided from your end for the product.<br><br>We hope to see a positive answer from your side. As soon as the price factor is accomplished, we’ll place the order immediately.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='Quotation Rejection'){
		var htvalue='<h2 style="text-align:center"><u>Quotation Approval</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">Thank you for sharing your price with us but we regretfully cannot match your price.<br><br>We, therefore, will not be placing an order with you.</p><br><p style="text-align:center">Thank You,</p><br>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='Quotation Request'){
		var htvalue='<h2 style="text-align:center"><u>Quotation Request</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">Sir, I am writing this letter to request a quotation for the _____ from you. We are looking to change our _____ for ___. Therefore, we will require ____ [quantity] of ____.</p><br><table border="1" width="100%" style="text-align:center"><tr><td><b>PARTICULLAR</b></td><td><b>QUANTITY</b></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr></table><br><br>'
		htvalue+='<br><p>I request you to please share your quote regarding the same. We hope your prices are according to the market standards. We’ve heard about your reputation, therefore, are relying on your service.</p><p style="text-align:center">Thank You,</p><br>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='Recommendation for Scholarship'){
		var htvalue='<h2 style="text-align:center"><u>Recommendation for Scholarship</u></h2>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">I am writing this letter on Mr/Mrs ____ request for a recommendation letter required for the ___ scholarship for your academic institution. It is with great pleasure that I recommend ___ to your institution.<br><br>____ has been a part of the organisation for __ years and has shown incredible talent in handling and managing all her responsibilities and roles. Under her supervision, the _ team has achieved great heights and has been able to deliver __ % better revenue for our organisation. His/Her abilities to adapt to new situations and make logical decisions are what truly set her apart as an employee and will set her apart as a student.I am confident that your institution ____ will be equally impressed by Mr/Mrs ___ ‘s capabilities as our company is. If you have any more questions or require any specific information please feel free to contact me at _____.</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='Request for Background Verification'){
		var htvalue='<h2 style="text-align:center"><u>Background Verification to Ex-Employee</u></h2>'
		htvalue+='<br><br><b>To</b><br>[Officer name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">This letter is to verify that the Applicant ____who has applied for employment with our company <b>WTT INTERNATIONAL PVT LTD</b>, and he/she has listed your company as part of their employment history. We request you to verify the details that were provided by ____on his/her resume and ancillary documents.<br><ul<li>Duration of employment from the date of to joining to last working day</li><li>Job title held by him/her in your organization</li><li>The annual gross salary</li><li>he /she adhere to the company policies and procedures</li><li>If he/she is currently employed by your company or has turned in a resignation letter</li><li>Is there any other information you can provide about the applicant’s job performance. We are also attaching the documents submitted by the employee for your reference. We request for your verification of the same at the earliest. In case of any queries, you can contact us at ___.</li></ul></p><p style="text-align:center">Thank you for your time and consideration. </p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>__________</b></p>'

	}
	else if(frm.doc.template7=='Request for Labour Officer'){
		var htvalue='<h2 style="text-align:center"><u>Request for Labour Officer</u></h2>'
		htvalue+='<br><br><b>To</b><br>[Officer name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">I am writing this letter on behalf of <b>WTT INTERNATIONAL PVT LTD</b> in response to the notice received on <DATE> bearing the reference no. <REF No.>. We are aware about the discontent of our ex-employee<br><br>Our internal team has constituted a committee to investigate the matter. Upon initial investigation, our team has found the following facts,<ul><li>FACT 1</li><li>FACT 2</li><li>FACT 3</li></ul><br><br>We are hereby attaching the necessary documents along with this letter for your perusal.<br><br>Our company representative <EMPLOYEE NAME> with the employee ID <ID> to be present on the hearing date on our company’s behalf.</p><p style="text-align:center">Thanks in advance!</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='Request to Bank Reference'){
		var htvalue='<h2 style="text-align:center"><u>Request to Bank Reference</u></h2>'
		htvalue+='<br><br><b>To</b><br>[Officer name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">I am writing this letter regarding your request for verification of ___.<br><br>We’d like to confirm ___ is a part of our organisation ___ and works in the role of a __. Their current CTC is ___.<br><br>I hope I have answered all your questions. If you have any further queries feel free to reply to this mail.</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='Shift Change Letter'){
		var htvalue='<h2 style="text-align:center"><u>Shift Change Letter</u></h2>'
		htvalue+='<br><br><b>To</b><br>[Officer name]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">I am writing this letter to inform you that your shift from _ to _ as a ____ has been shifted. This change will be applicable from ____.<br><br>The decision has been made as per the requirements of the branch. The terms and conditions of your employment agreement will remain the same.<br><br>During this shift, you will be reporting to ______. In case of any queries please contact the HR department of the branch _____.<br><br>We wish you luck and hope to see you growing.</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='TDS Defaulter'){
		var htvalue='<h2 style="text-align:center"><u>TDS Defaulter</u></h2>'
		htvalue+='<br><br><b>To</b><br>[Officer name]<br>[Company]<br>[Address]<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">While conducting a TDS reconciliation of our books, it has come to our notice that an amount of Rs. <AMOUNT> is yet to deposited by your company as TDS.<br>We are hereby attaching a copy of our FORM-26AS and the ledger for your reference.<br>Requesting you to kindly clear your TDS dues with the government or transfer the amount back to us.<br>In case you have already paid the same, kindly share the TDS Certificate for our reference.</p><p style="text-align:center">Thanks in advance!</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='Termination (Absenteeism)'){
		var htvalue='<h2 style="text-align:center"><u>Termination (Absenteeism)</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">As discussed, this letter is an official notice to inform you about the termination of your employment due to excessive absenteeism.<br><br>We have formally warned you regarding this several times however, we haven’t seen any improvement in your behaviour. We, therefore, are being forced to take a strict decision.<br><br>Your notice period of one month commences from the ____.<br><br>Please follow the exit process in an orderly format by submitting your handover to your manager.<br><br>Thank you for your association with the company and we wish you the best of luck for the future.</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='Termination (Substance Abuse)'){
		var htvalue='<h2 style="text-align:center"><u>Termination (Absenteeism)</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">As discussed, this letter is an official notice to inform you about the termination of your employment due to testing positive in our annual check-ups for drugs. According to the laws of our country these substances are illegal for consumption.<br><br>We have warned all our employees regarding our severe intolerance of the use of substances time and again. We, therefore, are being forced to take a strict decision.<br><br>Since this is a serious offence you will vacate the company premises by the closing hours of ___.</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>__________</b></p>'
	}
	else if(frm.doc.template7=='Employment Termination'){
		var htvalue='<h2 style="text-align:center"><u>Employment Termination</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">I am writing to you about the termination of your employment with insert company/ partnership/ sole trader name and the trading name of business.<br><br>I refer to our meeting on insert date which was attended by you and insert name of others at the meeting. During the meeting we discussed insert details of serious misconduct.<br><br>This meeting was attended by you and insert names of people at the meeting and we spoke about insert details of the serious misconduct incident, including the date it occurred.<br>As discussed during the meeting, your conduct during that incident: <br>Delete the points not applicable or add other if you believe they warrant summary dismissal. Seek legal advice if you are unsure if the actions warrant termination of employment without notice.<br><ul><li>Was wilful or deliberate behaviour by you that is inconsistent with the continuation of your contract of employment.</li>'
		htvalue+="<li>Caused a serious and imminent risk to the health or safety of a person.</li><li>Caused a serious and imminent risk to the reputation, viability or profitability of the Employer's business in that insert details.</li><li>Was conduct in the course of your employment engaging in theft, and in the circumstances your continued employment during a notice period would be unreasonable.</li><li>Was conduct in the course of your employment engaging in fraud, and in the circumstances your continued employment during a notice period would be unreasonable.</li><li>Was conduct in the course of your employment engaging in assault and in the circumstances your continued employment during a notice period would be unreasonable.</li><li>You were intoxicated at work, to the extent that you were so impaired that you were unfit to be entrusted with your employment duties.</li><li>You refused to carry out a lawful and reasonable instruction that was consistent with your contract of employment, and in the circumstances your continued employment during a notice period would be unreasonable.</li></ul><br>We consider that your actions constitute serious misconduct warranting summary dismissal. <br><br> You will also be paid your accrued entitlements and any outstanding pay up to and including your last day of employment. This includes the balance of any time off instead of overtime paid accrued but not yet taken (paid at the overtime rate applicable when the overtime was worked), and superannuation.<br><br>If you have been paid annual leave in advance, any amount still owing will be deducted from your final pay.  <br><br>Some termination payments may give rise to waiting periods for any applicable Centrelink payments. If you need to lodge a claim for payment you should contact company HR immediately to find out if there is a waiting period."
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Account Termination'){
		var htvalue='<h2 style="text-align:center"><u>Account Termination</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">As discussed, this letter is an official notice of immediate termination of your employment from the company. This will come into effect from ___ 20__.<br><br>This is a decision taken by the company on the basis of the recent investigation about the fraud against our company. The auditor has found _____in your record which has resulted in a missing amount of ___.<br><br>Your actions have caused the company to suffer huge financial losses. Therefore, apart from terminating you, we plan on initiating legal action against you. However, you can avoid that by simply returning the amount back to the company.<br><br>If we do not see the amount returned by ___. We will take legal actions against you.</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Thanking for Award Nomination'){
		var htvalue='<h2 style="text-align:center"><u>Thanking for Award Nomination</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">We want to extend our heartiest thank you for nominating us for the _______ award.<br><br>We’ve heard great things about your award ceremonies and unbiased awards. We, therefore, are honoured to be considered for the award along with several great companies.<br><br>We’ve attached a few documents that can help you in your decision-making process. We hope the right company wins.</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Thanking for Award Received'){
		var htvalue='<h2 style="text-align:center"><u>Thanking for Award Received</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">I am writing this letter to thank you for awarding us with the ____ award. It is an absolute pleasure to receive this award by ____. Your platform gives upcoming and unique companies a chance to shine.<br><br>Our teams are immensely excited and thrilled to place the award on the wall. We thank you for that opportunity.<br><br>Thank you for all your efforts in creating a wonderful platform that fairly awards businesses.'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template7=='Work Anniversary'){
		var htvalue='<h2 style="text-align:center"><u>Thanking for Award Received</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><b>Respected Sir,</b><br><br><p style="text-indent:70px">Hearty congratulations on completing _____ years with _____. We want to personally thank you for your continuous effort and dedication.<br><br>You have truly inspired other employees in the company. We want to thank you for your continuous effort and growth with our company.<br>To show you our appreciation we’ve prepared a gift basket for you. Please find it on your desk.<br><br>We can happily say that the company and your team are glad to have you on board. We hope to see you keep on growing and inspiring others.</p>'
		htvalue+='<br><p style="text-align:right;">Regards,'
		htvalue+='<br><b>Human Resources Department</b></p>'
	}
	else if(frm.doc.template6=='Acceptance of Employee Apology'){
		var htvalue='<h2 style="text-align:center"><u>Acceptance of Apology</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">This letter is in reference to the apology letter you sent to our HR team on #apology receipt date#. <br><br>We have received and acknowledged your apology in regards to #reason for apology#. On behalf of the HR team and the organization as a whole, I would like to inform you that we have accepted your apology and hope to see immediate and sustained improvements from you, as you have assured.<br><br>In case you are facing any obstacles in establishing the required improvements on the job, please do let us know. We are always ready and willing to support or assist you in whatever possible way from our side.<br><br>On behalf of <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Adhoc Designation Change Certificate'){
		var htvalue='<h2 style="text-align:center"><u>Adhoc Designation Change Certificate</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">Consequent to the decision taken by our HR Team and Management in its meeting held on #meeting date# and subsequent to our discussion with you about the same, we’re revising your designation to #new designation# with effect from #new designation start date#.<br><br>All the other terms and conditions of your employment will remain the same.<br><br>Congratulations on the new position! We are confident you will make best use of this change offered to you and contribute substantially to the success of our organisation as you have done in the past to fully justify the confidence we have placed in you.<br><br>For  <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Adhoc Increment Certificate'){
		var htvalue='<h2 style="text-align:center"><u>Adhoc Increment Certificate</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">Consequent to the decision taken by our HR Team and Management in its meeting held on #meeting date# and subsequent to our discussion with you about the same, we are pleased to inform you that it has been decided to increment your Annual CTC package and revised it to #revised amount# including applicable taxes, if any, with effect from #revision date#.<br><br>All the other terms and conditions of your employment will remain the same.<br><br>We are confident you will make best use of this increment offered to you and contribute substantially to the success of our organisation as you have done in the past to fully justify the confidence we have placed in you.<br><br>We wish you all the best for greater success. Congratulations and keep up the spirit!<br><br>For  <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Appraisal Certificate'){
		var htvalue='<h2 style="text-align:center"><u>Appraisal Certificate</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">The company has vigilantly monitored and evaluated your performance during the last #evaluation period#, and it was analyzed that your #briefly describe positive or good performance attributes# should recognized and rewarded. Management and the HR department has also decided that you can be entrusted with greater responsibilities based on your effectiveness and efficiency at work the place. <br><br>Hence, consequent to this review, we are pleased to promote you to the position of #new designation#, and as part of your appraisal, we are pleased to increment your annual CTC package to #revised amount# w. e. f. from #revision date#. All other terms of your employment remain the same. <br><br>We are confident you will make best use of the opportunity offered to you and contribute substantially to the success of our organisation as you have done in the past and fully justify the confidence we have placed in you.<br><br>We wish you all the best for greater success. Congratulations and keep up the spirit!<br><br>For  <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Appraisal Certificate with Promotion'){
		var htvalue='<h2 style="text-align:center"><u>Appraisal Certificate with Promotion</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">The company has vigilantly monitored and evaluated your performance during #evaluation period#, and it was analyzed that your #briefly describe positive or good performance attributes# should be rewarded. Management and the company HR has decided that you can be entrusted with higher responsibilities based on your effectiveness and efficiency at work place. <br><br>Hence, consequent to this review of your performance, we are pleased to promote you to the position of #*designation#, and as part of your appraisal. As discussed during our meeting, your annual CTC package and all other terms of your employment remain the same. <br><br>We are confident you will make best use of the opportunity offered to you and contribute substantially to the success of our organisation as you have done in the past and fully justify the confidence we have placed in you.<br><br>We wish you all the best for greater success. Congratulations and keep up the spirit!<br><br>For <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Experience or Relieving Letter with Praise'){
		var htvalue='<h2 style="text-align:center"><u>Relieving letter</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">With reference to your resignation letter dated on #resignation date# we hereby relieve you you’re your duties. We confirm that you have been working in our organization from #*dateofjoining*# to #*dateofexit*#. <br><br>During your employment with us as #*designation*# we found you to be hard working, diligent and honest in performing your duties. We’re sad to see you leave our organization and regret your absence from our office.<br><br>We sincerely thank you for your service and wish you the best in your future endeavors.<br><br>For <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	
	else if(frm.doc.template6=='Experience or Relieving Letter'){
		var htvalue='<h2 style="text-align:center"><u>Acceptance of Resignation</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">We are in receipt of your resignation letter dated #date of resignation#. This letter is the acknowledgement and acceptance of your resignation. You will be relieved of your duties on #proposed exit date# after the closure of office hours.<br><br>We expect you to perform your duties with full dedication and without any shortfalls up till your exit from the organization. Please ensure you adequately handover the required tasks, documentation, knowledge and information as per the requirements mentioned by your supervisor.<br><br>You are requested to settle your dues, if any, from the Accounts Department and obtain the clearance certificate accordingly.<br><br>For  <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='First Attendance Warning'){
		var htvalue='<h2 style="text-align:center"><u>Warning Notice for Attendance Issues</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">On #formal warning date#, you were placed on Formal Warning due to #repeated attendance policy violations#. Previously, you were placed on Informal Verbal Warning for the same issue as well. At that time, you were clearly informed of our expectations for your attendance at work and your need to improve the same. We discussed the negative impact of your poor attendance on your own productivity and others workload as well. Despite these warnings, you have not adhered to our attendance policies repeatedly again.<br><br>As a result of your #absenteeism or late attendance or lack of adequate work hours#, you are now being placed on Final Warning. During the next #specify period in months or weeks or days#, you will be ineligible for any paid leaves, salary increases, promotions or transfers, and you will be expected to strictly comply with attendance policies. Failure to show immediate and sustained improvement will result in immediate termination.<br><br>We are still ready and willing to assist you in meeting our attendance policies. Please let us know if there are any obstacles preventing you from meeting our expectations. <br><br>On behalf of <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Behavioral Final Warning'){
		var htvalue='<h2 style="text-align:center"><u>Warning Notice for Behaviour Issues</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">On #formal warning date#, you were placed on Formal Warning due to #behavioural issues or misconduct# at work. Previously, you were placed on Informal Verbal Warning for the same issue as well. At that time, you were clearly informed of our expectations for your behaviour at work and your need to improve the same. We discussed the negative impact of your poor behaviour not only on your performance evaluation but also on your coworkers, and the overall work environment. Despite previous warnings, you have not adhered to our requests for rectifications and improvements in your behaviour at work.<br><br>As a result of #repeated or consistent misconduct#, you are now being placed on Final Warning. <br><br>During the next #specify period in months or weeks or days#, you will be ineligible for any paid leaves, salary increases, promotions or transfers, and you will be expected to strictly comply with our code of conduct. Failure to show immediate and sustained improvement will result in immediate termination.<br><br>We are still ready and willing to assist you with counselling on this front. Please let us know if there are any obstacles preventing you from meeting the our expectations. <br><br>On behalf of <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Final Performance Warning'){
		var htvalue='<h2 style="text-align:center"><u>Warning Notice for Performance Issues</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">On #formal warning date#, you were placed on Formal Warning due to #lack of performance or unachieved targets or unmet goals#. Previously, you were placed on Informal Verbal Warning for the same issue as well. At that time, you were clearly informed of our expectations for your performance at work and the need to improve the same. We discussed the negative impact of your poor performance on your own productivity and others workload as well. Despite these warnings, youve not shown any noticeable improvement since the last discussion about this matter.<br><br>As a result of your repeated performance issues in spite of previous intimations for improvements, you are now being placed on Final Warning. During the next #observation period in months or weeks or days#, you will be ineligible for any paid leaves, salary increases, promotions or transfers, and you will be expected to catch up on lost time and get up to speed with performance expectations which are set for you. Failure to show immediate and sustained performance improvement will result in immediate termination.<br><br>We are still ready and willing to assist you to meet the set performance expectations which your position demands. Please do let us know if there are any obstacles preventing you from meeting your goals. <br><br>On behalf of <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Final Settlement with Confirmation'){
		var htvalue='<h2 style="text-align:center"><u>Full-n-Final Settlement with Confirmation</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br><br>'
		htvalue+='<br><br><p style="text-indent:70px">With reference to your Resignation Letter dated #date of resignation#, the management has duly accepted the same and accordingly you are being relieved from the services of the company as #*designation*# with effect from #*dateofexit*#.<br><br>Herewith, please find enclosed the cheque amounting to #Amount#, along with the computation sheet towards your Full and Final Settlement. Kindly acknowledge the same by returning a signed copy of this document for our records.<br><br>We wish you all the best and success for your future endeavors.<br><br>For <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Intern Offer'){
		var htvalue='<h2 style="text-align:center"><u>OFFER LETTER FOR PAID INTERN</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>Name<br>Address<br>City, State Zip Code<br><br>'
		htvalue+='<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style="text-indent:70px">On behalf of <b>WTT INTERNATIONAL PVT LTD</b>, I am pleased to extend to you this offer of temporary employment as an Intern, reporting to __.  If you and accept this offer, you will begin your internship with the Company on _______ will be expected to work ____ days per week.<br><br>You will be paid per month, less all applicable taxes and withholdings, payable	.<br>As an intern you will be receive “temporary employment” status. As a temporary employee, you will not receive any of the employee benefits that regular Company employees receive, including, but not limited to, health insurance, vacation or sick pay, paid holidays, or participation in the Company’s employee benefit plan plan.<br><br>Your internship is expected to end on ________. However, your internship with the Company is “at-will,” which means that either you or the Company may terminate your internship at any time, with or without cause and with or without notice.<br><br>During your employment, you may have access to trade secrets and confidential business information belonging to the Company. By accepting this offer of employment, you acknowledge that you must keep all of this information strictly confidential, and refrain from using it for your own purposes or from disclosing it to anyone outside the Company. In addition, you agree that, upon conclusion of your employment, you will immediately return to the Company all of its property, equipment, and documents, including electronically stored information.<br><br>By accepting this offer, you agree that throughout your internship, you will observe all policies and practices governing the conduct of our business and employees, including our policies prohibiting discrimination and harassment. This letter sets forth the complete offer we are extending to you, and supersedes and replaces any prior inconsistent statements or discussions. It may be changed only by a subsequent written agreement.<br><br>I hope that your association with the Company will be successful and rewarding. Please indicate your acceptance of this offer by signing below and returning it to contact me.</p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:center">I accept employment with the Company on the terms and conditions set out in this letter.</p>'
		htvalue+='<br><p style="text-align:right;">Candidate Signature: __________________________'
		htvalue+='<br>Candidate Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
		htvalue+='<h2 style="text-align:center"><u>OFFER LETTER FOR UNPAID INTERN</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>Name<br>Address<br>City, State Zip Code<br><br>'
		htvalue+="<br><br>Dear <b>'+frm.doc.candidate_name+',</b><br><br><p style='text-indent:70px'>We are pleased to offer you an internship with	<b>WTT INTERNATIONAL PVT LTD</b>. This is an educational internship.<br>As we discussed, your internship is expected to last from ______ to _______, hours per week.[OPTIONAL : However at the sole discretion of the Company, the duration of the internship may be extended or shortened with or without advance notice.][OPTIONAL: Include description of Internship program and training.]<br><br>As an intern, you will not be a Company employee. Therefore, you will not receive a salary, wages, or other compensation. In addition, you will not be eligible for any benefits that the Company offers its employees, including, but not limited to, health benefits, holiday pay, vacation pay, sick leave, retirement benefits, or participation in the Company's employment plan. You understand that participation in the internship program is not an offer of employment, and successful completion of the internship does not entitle you to employment with the Company.<br><br>During your internship, you may have access to confidential, proprietary, and/or trade secret information belonging to the Company. You agree that you will keep all of this information strictly confidential and refrain from using it for your own purposes or from disclosing it to anyone outside the Company. In addition, you agree that, upon conclusion of the internship, you will immediately return to the Company all of its property, equipment, and documents, including electronically stored information.<br><br>By accepting this offer, you agree that you will follow all of the Company's policies that apply to non-employee interns, including, for example, the Company's anti-harassment policy.<br><br>This letter constitutes the complete understanding between you and the Company regarding your internship and supersedes all prior discussions or agreements. This letter may only be modified by a written agreement signed by both of us. Please indicate your acceptance of this offer by signing below and returning it to.<br><br>I hope that your internship with the Company will be successful and rewarding. Please indicate  your  acceptance  of  this  offer  by  signing  below  and  returning  it  to .  If you </p>"
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:center">I accept employment with the Company on the terms and conditions set out in this letter.</p>'
		htvalue+='<br><p style="text-align:right;">Candidate Signature: __________________________'
		htvalue+='<br>Candidate Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Intern Experience with Praise'){
		var htvalue='<h2 style="text-align:center"><u>Certificate of Experience</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">This is to certify that #*firstname*# #*lastname*# was hired as an intern at our organization from #internship start date# to #internship end date#. This internship was in our #*department*# department under the guidance of #Mentor Name#.<br><br>We have found the intern to be a self starter who is motivated, duty bound and hard-working who not only worked sincerely on given assignments and but also delivered excellent performance on the job.<br><br>For <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Intern Experience'){
		var htvalue='<h2 style="text-align:center"><u>Certificate of Experience</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">This letter is to certify that #*firstname*# #*lastname*# has successfully completed his or her internship program for a period of #internship duration# with our organization. This internship tenure was from #internship start date# to #internship end date#. The said intern was working with #*department*# and was actively, diligently and sincerely involved in the projects and tasks assigned.During this internship, we found the intern to be punctual and hardworking person. <br><br>For <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Suspension'){
		var htvalue='<h2 style="text-align:center"><u>Suspension during Misconduct Investigation</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">This is an official intimation for suspension of employment being served to you, as per our #meeting# on #meeting date#, when we discussed the allegations of gross misconduct made against you which claim #briefly describe misconduct#.<br><br>In accordance with the our disciplinary procedure, you are suspended from work #with or without pay#, while a full investigation is carried out into this misconduct accusation. Your suspension is purely to enable us to conduct a fair, thorough and speedy investigation, and does not in itself carry any implication of guilt or prejudgement. Nor does it constitute any form of disciplinary action against you, at the moment.<br><br>During your suspension, you are instructed not to contact by any means directly or indirectly with any vendors, customers, staff or colleagues of our organization. <br><br>If you have any queries in relation to this matter, please contact only the #HR department or specific names#. Failure to comply with these instructions may in itself constitute misconduct or, if this investigation is undermined in any way, gross misconduct, which may result in further disciplinary action against you.<br><br>We will contact you at the earliest opportunity to inform you of the outcome of this investigation. If you are required to attend a disciplinary hearing, you will be given full details of the allegations against you and the results of the investigation in advance of the hearing. You are required to remain available during your suspension, so that we are able to contact you if the need arises.<br><br>For <b>WTT INTERNATIONAL PVT LTD</b></p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Lay-off due to Shutdown'){
		var htvalue='<h2 style="text-align:center"><u>Employment Lay-off due to Shutdown</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br>Dear Sir/Madam,<br><br><p style="text-indent:70px">With a heavy heart, I officially announce the decision to close down #Company or BU or Dept Name# on a permanent basis. We are experiencing much difficulty in staying afloat for the past #struggle or loss period# and I believe that it is now time to bring things to an end.<br><br>Since inception, we have crossed some significant milestones with this team, however, current circumstances do not allow us to continue working with the same fervour that we exhibited back then.<br><br>We truly appreciate your professionalism and loyalty to the organization and will be happy to offer all the support making this difficult last step as comfortable as possible.<br><br>#Last Date of business# will be our last operational day. As part of our retrenchment policy, you will be given a #No. of days or months# salary to support you until you find new employment. You may contact #HR contact name# for further details on this. We will keep your records with us and if in future we are able to re-establish ourselves, you will be our first choice for a similar position.<br><br>We do not consider this the end and we hope that you will be successful in everything that you do in future.</p>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Letter to Bank'){
		var htvalue='<h2 style="text-align:center"><u>Salary Transfer</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br>Dear Sir/Madam,<br><p style="text-indent:70px">We confirm that Mr./Ms. ____________________________________has been an employee of this company since ___________. <br><br>He/ She is presently working in the capacity of a _________________ with a total remuneration of AED ___________________ per month, including fixed allowances only. Moreover, he/she has completed the probation period successfully.<br><br>We confirm that we will transfer directly his/her net salary each month into his/her a/c #______________ with you. We will not transfer his/her salary to any other bank or account unless we get a clearance certificate from you.<br><br>Should the employment cease, the company will notify you accordingly.This letter is issued upon the employee’s request and it does not constitute a financial guarantee on our part.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Manager’s Name & Designation<br>(Authorized Signatory)<br>Company Stamp.</b></p>'
		htvalue+='<br><br>[OR]<br><br><h2 style="text-align:center"><u>Disbursement of Salary for the month of November, 2019 </u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br>Dear Sir/Madam,<br> Ref: A/c No._______________________ <br><p style="text-indent:70px">Enclosed please find herewith salary data of our employees for Rs…………………………….. (Rupees ………………………………………… only). Kindly disburse the salary for the month of November, 2019 by debiting our A/c No. ________________ maintained with you. <br><br>Please send us the confirmation of disbursement of salary to the individual account of the employees.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>WTT INTERNATIONAL PVT LID</b></p>'
		htvalue+='<br><br>[OR]<br><br><h2 style="text-align:center"><u>Opening of salary account for our employee – (Name of the employee)</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br>Dear Sir/Madam,<br><p style="text-indent:70px">We are maintaining salary accounts for all our employees with your branch office of…….Bank. We would now like to open a salary account for another employee, whose details are given below.<br><br>Name of Employee….<br>Designation…..<br>Department Name…..<br>Date of joining…..<br>Salary p.m …...<br>Present address…..<br><br>Please help him in opening a saving account with your bank at the earliest.<br><br>This letter is being issued at the employee’s request and the company takes no responsibility of his any kind of liabilities with the bank. But we do expect then bank to provide him with benefits as per our contract.</p>'
		htvalue+='<br><p style="text-align:right;">Sincerely,'
		htvalue+='<br><b>Name<br>Manager Human Resource</b></p>'
	}
	else if(frm.doc.template6=='Workshop NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Attending Workshop</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This letter is to show complete No Objection on Mr. _____________ to attend Marketing Skills workshop conducted at ‘Landmark Mall’ on 10th March 2015. He is allowed to take off from office from 9am to 2pm.</li><li>He will be representation _______________ Association as a Marketing Manager. </li><li>This certificate is issued as per demand of workshop trainers.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'
	}
	else if(frm.doc.template6=='Bank Account NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Bank Account</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This letter is to certify that Mr. ________________ is working with our organization since March, 2015 as Project Manager. He need to open a bank account for salary transactions on company’s behalf. </li><li>We have complete no objection upon this and this letter is issued as per request of _______________ Bank. In case of any query, feel free to contact.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'
	}
	else if(frm.doc.template6=='Credit Card NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Credit Card</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This letter is to certify that Miss. _______________ has been working with our organization as a Finance Manager. This NOC is issued upon her request for ______________ Bank.</li><li>That we at ____________ Association have no objection if she applies for Credit Card in the Bank’s __________ Branch, on the basis of her account for official use.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'
	}
	else if(frm.doc.template6=='Double Shift NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Double Shift</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This letter shows complete No Objection on Mr. _____________ if he works in double shifts at his designation of Customer Relation Officer. </li><li>We are satisfied by his workings and management have got no issue if he works for our organization in morning and evening shifts. This letter is issued upon his request.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Work in Other Organization NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Employees to Work in Other Organization</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This is to claim that the workers of our organization are skillful and they are allowed to do work in any other company on contract or part time basis. The management has no objection upon their working. </li><li>This No Objection Certificate is issued on particular request of employees and may be useful for them in future or as per requirement of any other organization. If any further queries are to be discussed, you can feel free to contact.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Organizing Event NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Organizing Event</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This letter is to certify that we have got complete no objection upon the event ‘ABC’ which is about to take place in ‘XYZ’ auditorium on 5th May, 2016. This event is sponsored by —– and the entire management along with decorum maintenance responsibility is upon the sponsor. </li><li>We are not responsible for any sort of mismanagement. This NOC is issued upon the request of the —– and is only valid for the date of 5th May, 2016 and will be automatically nullified afterwards. In case of any other query feel free to contact.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Part- Time NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Part Time Job</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>It is  certified that the employees working in (Company Name) are not bound with the company except their working hours from 9 am to 5 pm. After this, they are allowed to work anywhere part time, without the behalf of company. Employees can do part time job in other organization but keeping the Company’s personal documents safe.</li><li.This No Objection Certificate certifies  the permission from company’s management.</li></ol>In case of particular discussion, call at ________________.'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Personal Loan NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Personal Loan</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This letter is issued upon request of Mr. __________________ (employee) working as Marketing Manager in our organization. He has requested for loan of Rs. _________________/- from Bank (__________Bank Name) and the need of loan is for personal basis.,/li><li>The Administration has no object upon this but organization is not responsible for any activity related to his personal loan. For any queries you may feel free to contact.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Tourist Visa NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Tourist Visa</u></h2>'
		htvalue+='<b>From</b><br>Name of the Employer,<br>WTT INTERNATIONAL PVT LTD</b>,<br>No.3, College Cross road, Tirupur - 641602<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br><b>To</b><br>Full Address of the Embassy/Consulate<br><br>Respected Sie/ Madam,<br><br><b>Subject : </b>No Objection Certificate for (Employee’s Name)<br><br>This letter is to confirm that Mr. /Mrs. _________ is an employee with our company since _____ on a full-time basis. He is currently working as a ________(designation) at ________(company name) and his annual salary is USD _____ P.A.<br><br>Mr. /Mrs. ______ has expressed his/her interest in visiting _______(name of the country you’re visiting) for leisure and tourism purpose. Our company has no objection regarding his visit to ______(name of the country) for _____ days.<br><br>I’d also like to let you know that his/her leaves have been approved from ______ (leave starting date) to _______(leave ending date) for this overseas trip. We’re expecting Mr./Mrs._______ to report for work on _____ (date) on the expiry of his approved leave.<br><br>If your office requires any further details for enquiry, please feel free to contact us.'
		htvalue+='<br><br><p style="text-align:right">Yours sincerely,<br><br>(Undersigned, with round seal of the office/department along with stamp)<br>Name of the employer<br>Designation<br></p>'
		htvalue+='<br><br>[OR]<br><br><b>From</b><br>Name of the Employer,<br>WTT INTERNATIONAL PVT LTD</b>,<br>No.3, College Cross road, Tirupur - 641602<br>'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()
		htvalue+='<br><br><b>To</b><br>Full Address of the Embassy/Consulate<br><br>Respected Sie/ Madam,<br><br><b>Subject : </b>: No Objection Certificate for (Employee’s Name)<br><br>This letter is to formally introduce Mr./Mrs._______, who holds the position of ______ (designation) with ___________(name of the company), is visiting ________(city and country) on ______ (date). We do not have any objection regarding his overseas business visit.<br><br>During his stay in ______(country), Mr. /Mrs. ___________ will be attending certain business meetings with _________ (name of client) as a representative of our company.<br><br>Since the meetings are strictly related to sales, it would not involve any kind of technical training or assistance. The stay in _______ (country) would not exceed the legally permitted period, and Mr._______ does not have any intentions of immigrating to ______(country).<br><br>Furthermore, the company is completely taking responsibility of all the expenses during his stay in _______(country), including the flight tickets from ______(home country) to _____(visiting country) and back.<br>Your assistance in granting him a visa would be greatly appreciated.'
		htvalue+='<br><br><p style="text-align:right">Yours sincerely,<br><br>(Undersigned, with round seal of the office/department along with stamp)<br>Name of the employer<br>Designation<br>'
	}
	else if(frm.doc.template6=='Trainee Student NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Trainee Student</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This is to certify that Mr./Miss________ (name) student of _____ (institution) has joined or want to join our organization_________ (name) as a Trainee. Our company welcome the freshers and new comers. We appreciate his/her effort to be here as a trainee. </li><li>This letter shows our completely no objection upon him/her to work at our place as a trainee and this letter is issued as per request of Mr./Miss______ (name). We wish for his/her bright career and future.</li><li>In case of any query, feel free to contact.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Visiting Abroad NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC for Visiting Abroad</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This letter is to claim complete No Objection, if  Mr. ____________ employee at _____________ is going on a visit tour abroad. </li><li>He has informed the management before his action and this letter is issued as per the request of employee. According to provided details the date of visit will be from 6th June to 20th June, 2015.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Department Change NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC Letter for Department Change</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This NOC is to verify that Mr ______________(employee name) has been serving our institution since _____ years as a ____________(degeneration). Now he has completed his MBA in human Resource and, he would like to join Human Resource Department because its his field of study. Human Resource department is seeking a person for recruitment.</li><li>This letter shows that we have complete no objection upon change the department. Mr _________________ is very hard-working employee and can perform their duties in Human Resource department. We wish him good luck for future.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Job Change NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC Letter for Job Change</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This is to certify that Mr. ________________ has been working in our organization, ______________ Group of companies since ________ years as a Deputy Manager.</li><li>During his working tenure within our company he has been sincere, loyal, punctual and hardworking. This No Objection Certificate is issued as per request of the employee. It would be useful for him for various concerns.</li><li>This shows our complete no objection on him to continue his job with any organization. If any further queries are to be discussed, you can feel free to contact.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Studies NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC Letter for Studies</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This is to certify that Ms. _______________ CNIC No _____________ has been working in the capacity of “________________” at Roshni Association _____________ Campus since 10th Jan 2011 till date</li><li>She is a dedicated and hardworking employee and organization has no objection if she continues further studies.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Visa NOC'){
		var htvalue='<h2 style="text-align:center"><u>NOC Letter to Employee For Visa</u></h2>'
		htvalue+='<br><p style="text-align:right;">Date: '+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'<br>Ref No. _____________</p>'
		htvalue+='<br><br>Dear <b>To Whom It May Concern</b>,<br><br><ol><li>This is to certify that Mr. _________________ is a sincere employee of our organization and he is working with us since _______ years as a Operation Manager. He is going to official visit of (NAME OF COUNTRY) and this letter is issued as per requirement of the Visa provider.</li><li>We have no objection upon him and he is loyal to his job. This letter can be used for his further concerns.</li></ol>'
		htvalue+='<br><br><p style="text-align:right">Yours Sincerely,<br>(Sign & Stamp)<br><br>HR Manger,<br><b>WTT INTERNATIONAL PVT LTD</b>'	
	}
	else if(frm.doc.template6=='Post Probation Increment'){
		var htvalue='<h2 style="text-align:center"><u>Confirmation of Employment after Probation with Increment</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">We are pleased to inform you that subsequent to assessments of your performance during probation, you have successfully completed your probationary period of #probation period#.<br><br>We would like to recognize the fine work you have done for our organization in this short duration, and we are very confident that you will meet the new responsibilities which accompany your position, with the same level of enthusiasm which you have exhibited already.<br><br>This is to certify that you are being confirmed for employment with our organization at the #*designation*# position, with an increment in your remuneration package which will be revised to #amount# per annum, with effect from #increment effective date#.<br><br>The terms of your employment continue to apply as per employment contracts currently in effect between you and our organization.<br><br>We are optimistic that you will use this opportunity to not only help our company achieve greater heights but also enhance your career graphs within the organization hierarchy, year after year. <br><br>We look forward to yourlong standing association with us.<br><br>For <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Relieving after Resignation'){
		var htvalue='<h2 style="text-align:center"><u>Relieving letter</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">This is with reference to your resignation letter, dated #date of resignation# wherein you expressed your desire to be relieved from the services of our company on #requested exit date#.<br><br>We would like to inform you that you have served the notice period and your resignation has been accepted. Your relieving date is the same as agreed when accepting your resignation.<br><br>Your salary, perks and other benefits have been settled with the organization and you can collect the same on the day of relieving, after the office hours.<br><br>Your contribution to the organization toward its growth and success will always be appreciated. Wish you all the best in your future endeavors.<br><br>For <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Resignation Acceptance - Key Employee'){
		var htvalue='<h2 style="text-align:center"><u>Resignation Acceptance</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">This is in reference to your letter of resignation from the position of #*designation*# submitted on #resignation date#. With great regret and disappointment, the management has accepted your resignation. We are really sorry that you have decided to leave, but we can only respect your decision and wish you the best in your next endeavour. <br><br>As agreed during our #discussion or meeting# in this regard, you will be relieved of your responsibilities at the end of your last working day on #exit date#.<br><br>We appreciate your advance notice and your commitment to hand over your duties as complete as possible. The HR Team will separately discuss the exit formalities with you, including the handover of any projects, official data or documents, materials or assets belonging to the company. <br><br>We would also like to thank you for your dedication, efforts and performance while you have worked with us so far. It has been a pleasure having you as one of our employee.<br><br>For <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Resignation Acceptance'){
		var htvalue='<h2 style="text-align:center"><u>Resignation Acceptance</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">This is in reference to your letter of resignation from the position of #*designation*# submitted on #resignation date#. Your resignation has been approved by the organization and you will be relieved of your responsibilities at the end of your last working day on #exit date#.<br><br>It has been a pleasure having you as one of our employees and we wish you success in your future endeavours. <br><br>The HR Team will separately discuss the exit formalities with you, including the handover of any projects, official data or documents, materials or assets belonging to the company. <br><br>For <b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Resignation Withdrawal for Growth Prospects'){
		var htvalue='<h2 style="text-align:center"><u>Withdrawal of Resignation</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">Further to my resignation letter dated #resignation date# and our conversation following the same, I write to confirm that I would like to withdraw my resignation with immediate effect.<br><br>Having spent #experience in months or years# here in my current role, I felt that perhaps it was time to move on to a different challenge and gain valuable career experience elsewhere. However, in our discussions since then you have persuaded and convinced me about the exciting growth opportunities available to me at our very own organization. These growth prospects are the key reason for my change of mind.<br><br>I would like to thank you for helping me come to this decision and hope that my work here can be even more fulfilling and productive than before.'
		htvalue+='<br><br><b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'

	}
	else if(frm.doc.template6=='Resignation Withdrawal for Role Change'){
		var htvalue='<h2 style="text-align:center"><u>Withdrawal of Resignation</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">Further to my resignation letter dated #resignation date# and our conversation following the same, I write to confirm that I would like to withdraw my resignation with immediate effect.<br><br>Having spent #experience in months or years# here with the organization, I felt that perhaps it was time to move on to a different challenge and gain valuable career experience elsewhere. However, in our discussions since then, you have persuaded and convinced me about the growth opportunities at our own organization and have very kindly offered me a new position as #new position or role# which I am delighted to accept. This new role is the key reason for my change of mind.<br><br>I would like to thank you for helping me come to this decision and hope that my work here can be even more fulfilling and productive than before.'
		htvalue+='<br><br><b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Stationary Request'){
		var htvalue='<h2 style="text-align:center"><u>Stationary Request</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p>Employee Name: ____________<br>Department: ________________<br>Location: _____________'
		htvalue+='<br><table width="100%" border="1" style="text-align:center"><tr><td><b>S.No</b></td><td><b>Item</b></td><td><b>Purpose</b></td><td><b>Qty</b></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td><b>Total Qty</b></td><td></td></tr></table>'
		htvalue+='<br><br><br><br><b>APPROVAL BY HOD</b><br><br><u><b>FOR OFFICE USE ONLY:</b></u><br>ORDER NO: _________<br>Dear Sir,<br><p style="text-indent:50px">We would like to place an order for the following items and would request you to deliver the same as soon as possible to the address given below. Payments will be subject to the delivery of goods as per the order form.</p><p style="text-align:right">________<br>Admin Signature</p.'
	}
	else if(frm.doc.template6=='Attendance Warning'){
		var htvalue='<h2 style="text-align:center"><u>Warning Notice for Attendance Issues</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">This letter of warning is being issued because of your excessive #absenteeism or late punch-ins or early punch-outs# and your failure to follow our our attendance policies. Additionally, our attendance rules require an employee to #contact or phone or email or SMS# her or his supervisor in advance if she or he will be absent or unexpectedly late for work, on repeated occassions you have not been able to meet these rules either. <br><br>All this has occurred in spite of our discussions regarding the company attendance policies with you more than once in the past, including when you joined our organization. <br><br>Hence, you are hereby warned to ensure complete adherence to our HR policies, especially the Attendance policies and requirements in this regard. Failure to do so shall invoke appropriate action. Please consider this as a strict and official warning regarding the same.<br><br>You are further advised to submit a written apology and acknowledgement as soon as you receive this letter.</p>'
		htvalue+='<br><br><b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='General Behavioral Warning'){
		var htvalue='<h2 style="text-align:center"><u>Warning Notice for General Behaviour Issues</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">It has been observed that your behaviour towards #Subordinates or Manager or Colleagues or Specify Names# is not appropriate or suitable for our work environment. Such behaviour is against the code of conduct in our organization, and, this misconduct makes you liable for necessary action, as per our company policy.<br><br>Hence, you are hereby warned to refrain from repeating such behaviour and to be careful with your actions in future. Failure to do so shall invoke appropriate action. Please consider this as a strict and official warning in this regard.<br><br>You are further advised to submit a written explanation on your unethical act as soon as you receive this letter.</p>'
		htvalue+='<br><br><b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'

	}
	else if(frm.doc.template6=='Misbehavior Warning'){
		var htvalue='<h2 style="text-align:center"><u>Warning Notice for Misbehaviour on Specific Occasion</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">It has come to our notice that your behaviour on #date of occurrence# towards #Subordinates or Managers or Colleagues or Specify Name# was uncalled for and inappropriate. Such behaviour is detrimental to the decorum and dignity of our work environment, going against the sanctity of respect towards colleagues. <br><br>We take very serious cognizance of your actions and consider it a violation of the code of conduct in our organization.  This misconduct makes you liable for necessary action, as per our company policy.<br><br>Hence, you are hereby strictly warned to refrain from repeating such behaviour and to be very careful with your actions in future. Failure to do so may result in further corrective action up to and including termination of your employment with us. <br><br>You are further advised to submit a written explanation on your unethical act as soon as you receive this letter.'
		htvalue+='<br><br><b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}
	else if(frm.doc.template6=='Performance Warning'){
		var htvalue='<h2 style="text-align:center"><u>Warning Notice for Performance Issues</u></h2>'
		htvalue+='<br><br><p style="text-align:right">'+(new Date().getMonth() + 1) + "-" +  new Date().getDate() +"-" +  new Date().getFullYear()+'</p><b>To</b><br>___<br>___<br>___'
		htvalue+='<br><br><p style="text-indent:70px">On #discussion date#,  we discussed your performance evaluation which assessed you as #needs improvement or below expectations# in the areas of #mention areas which lack performance#.  <br><br>Since #start period of evaluation# till date we’ve observed a below par performance from you on repeated occasions. Considering your role, responsibilities and the direct impact of your work in the department, this lack of performance is unacceptable to the organization. Your negative performance affects not only your personal growth here, but workload of other team members, departmental results and overall #revenue or reputation o rservice quality# of the company.<br><br>We expect you to improve your performance to an acceptable level on immediate and sustained basis. Failure to meet our expectations may result in further corrective action up to and including dismissal.<br><br>You are further advised to submit a written apology, explanation and acknowledgement with reference to this letter. <br><br>We hope and wish to see you rise up to mark soon and assure you of our full support in achieving your #targets or results or goals#.'
		htvalue+='<br><br><b>WTT INTERNATIONAL PVT LTD</b>'
		htvalue+='<br><p style="text-align:left;">______________'
		htvalue+='<br>#<b>Signing Authority Designation</b>#,'
		htvalue+='<br>#<b>Signing Authority Name</b>#,</p>'
		htvalue+='<br><p style="text-align:right;">Employee Signature: __________________________'
		htvalue+='<br>Employee Name: __________________________,'
		htvalue+='<br>Date: __________________________,</p>'
	}

	frm.set_value('body',htvalue);
	frm.refresh_field('body');
	}
});





