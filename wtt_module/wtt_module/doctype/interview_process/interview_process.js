// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Interview process', {
	// refresh: function(frm) {

	// }
	onload:function(frm){
		if(frm.doc.educational_background<5 && frm.doc.educational_background>2)
		{
			var ed='<h5 style="color:#cc7a00">Educational Background (5 out of):<b>'+frm.doc.educational_background+'</b></h5>'
		}
		else if(frm.doc.educational_background==5)
		{
			var ed='<h5 style="color:green">Educational Background (5 out of):<b>'+frm.doc.educational_background+'</b></h5>'
		}
		else
		{
			var ed='<h5 style="color:red">Educational Background (5 out of):<b>'+frm.doc.educational_background+'</b></h5>'
		}

		if(frm.doc.verbal_communication<5 && frm.doc.verbal_communication>2)
		{
			var vc='<h5 style="color:#cc7a00">Verbal Communication (5 out of): <b>'+frm.doc.verbal_communication+'</b></h5>'
		}
		else if(frm.doc.verbal_communication==5)
		{
			var vc='<h5 style="color:green">Verbal Communication (5 out of): <b>'+frm.doc.verbal_communication+'</b></h5>'
		}
		else
		{
			var vc='<h5 style="color:red">Verbal Communication (5 out of): <b>'+frm.doc.verbal_communication+'</b></h5>'
		}

		if(frm.doc.candidate_interest_5_out_of<5 && frm.doc.candidate_interest_5_out_of>2)
		{
			var ci='<h5 style="color:#cc7a00">Candidate Interest (5 out of): <b>'+frm.doc.candidate_interest_5_out_of+'</b></h5>'
		}
		else if(frm.doc.candidate_interest_5_out_of==5)
		{
			var ci='<h5 style="color:green">Candidate Interest (5 out of): <b>'+frm.doc.candidate_interest_5_out_of+'</b></h5>'
		}
		else
		{
			var ci='<h5 style="color:red">Candidate Interest (5 out of): <b>'+frm.doc.candidate_interest_5_out_of+'</b></h5>'
		}

		if(frm.doc.knowledge_of_organization<5 && frm.doc.knowledge_of_organization>2)
		{
			var koo='<h5 style="color:#cc7a00">Knowledge of Organization (5 out of): <b>'+frm.doc.knowledge_of_organization+'</b></h5>'
		}
		else if(frm.doc.knowledge_of_organization==5)
		{
			var koo='<h5 style="color:green">Knowledge of Organization (5 out of): <b>'+frm.doc.knowledge_of_organization+'</b></h5>'
		}
		else
		{
			var koo='<h5 style="color:red">Knowledge of Organization (5 out of): <b>'+frm.doc.knowledge_of_organization+'</b></h5>'
		}

		if(frm.doc.teambuilding_interpersonal_skills<5 && frm.doc.teambuilding_interpersonal_skills>2)
		{
			var tis='<h5 style="color:#cc7a00">Teambuilding/ Interpersonal Skills (5 out of): <b>'+frm.doc.teambuilding_interpersonal_skills+'</b></h5>'
		}
		else if(frm.doc.teambuilding_interpersonal_skills==5)
		{
			var tis='<h5 style="color:green">Teambuilding/ Interpersonal Skills (5 out of): <b>'+frm.doc.teambuilding_interpersonal_skills+'</b></h5>'
		}
		else
		{
			var tis='<h5 style="color:red">Teambuilding/ Interpersonal Skills (5 out of): <b>'+frm.doc.teambuilding_interpersonal_skills+'</b></h5>'
		}

		if(frm.doc.initiative<5 && frm.doc.initiative>2)
		{
			var init='<h5 style="color:#cc7a00">Initiative (5 out of): <b>'+frm.doc.initiative+'</b></h5><br>'
		}
		else if(frm.doc.initiative==5)
		{
			var init='<h5 style="color:green">Initiative (5 out of): <b>'+frm.doc.initiative+'</b></h5><br>'
		}
		else
		{
			var init='<h5 style="color:red">Initiative (5 out of): <b>'+frm.doc.initiative+'</b></h5><br>'
		}
//technical team
		if(frm.doc.prior_work_experience<5 && frm.doc.prior_work_experience>2)
		{
			var pw='<h5 style="color:#cc7a00">Prior Work Experience (5 out of): <b>'+frm.doc.prior_work_experience+'</b></h5>'
		}
		else if(frm.doc.prior_work_experience==5)
		{
			var pw='<h5 style="color:green">Prior Work Experience (5 out of): <b>'+frm.doc.prior_work_experience+'</b></h5>'
		}
		else
		{
			var pw='<h5 style="color:red">Prior Work Experience (5 out of): <b>'+frm.doc.prior_work_experience+'</b></h5>'
		}

		if(frm.doc.technical_qualification<5 && frm.doc.technical_qualification>2)
		{
			var tq='<h5 style="color:#cc7a00">Technical Qualification (5 out of): <b>'+frm.doc.technical_qualification+'</b></h5><br>'
		}
		else if(frm.doc.technical_qualification==5)
		{
			var tq='<h5 style="color:green">Technical Qualification (5 out of): <b>'+frm.doc.technical_qualification+'</b></h5><br>'
		}
		else
		{
			var tq='<h5 style="color:red">Technical Qualification (5 out of): <b>'+frm.doc.technical_qualification+'</b></h5><br>'
		}


		var total_hr=parseInt(frm.doc.educational_background)+parseInt(frm.doc.verbal_communication)+parseInt(frm.doc.candidate_interest_5_out_of)+parseInt(frm.doc.knowledge_of_organization)+parseInt(frm.doc.teambuilding_interpersonal_skills)+parseInt(frm.doc.initiative)
		var total_tech=parseInt(frm.doc.prior_work_experience)+parseInt(frm.doc.technical_qualification)
		var htvalue='<h2 style="color:#4A55AE">Final Analysis</h2><br>'
		htvalue+='<h4 style="color:cornflowerblue"><b>HR Team: </b></h4><br>'
		htvalue+=ed
		htvalue+=vc
		htvalue+=ci
		htvalue+=koo
		htvalue+=tis
		htvalue+=init
		htvalue+='<h4 style="color:cornflowerblue"><b>Technical Team: </b></h4><br>'
		htvalue+=pw
		htvalue+=tq
		htvalue+='<h4 style="color:cornflowerblue"><b>Results: </b></h4><br>'
		htvalue+='<h5 style="color:#008055"><b>HR TEAM POINTS (30 out of): '+total_hr+'</b></h5>'
		htvalue+='<h5 style="color:#008055"><b>TECHNICAL TEAM POINTS (10 out of): '+total_tech+'</b></h5><br>'
		htvalue+='<h5 style="color:#008055"><b>OVERALL HR RESULT: '+frm.doc.hr_result+'</b></h5>'
		htvalue+='<h5 style="color:#008055"><b>OVERALL TECHNICAL RESULT: '+frm.doc.tech_result+'</b></h5><br>'
		$(frm.fields_dict['overall_chart'].wrapper).html(htvalue);
	}
});
