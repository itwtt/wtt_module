// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Appreciation', {
	rating:function(frm){
		frm.set_value("emoji","");
	},
	emoji: function(frm) {
		var html='<p style="font-size:30px">'
		if(frm.doc.emoji=='Smiley'){
			if(frm.doc.rating==1){html+='&#128522;</p>'}
			else if(frm.doc.rating==2){html+='&#128522;&#128522;</p>'}
			else if(frm.doc.rating==3){html+='&#128522;&#128522;&#128522;</p>'}
			else if(frm.doc.rating==4){html+='&#128522;&#128522;&#128522;&#128522;</p>'}
			else if(frm.doc.rating==5){html+='&#128522;&#128522;&#128522;&#128522;&#128522;</p>'}
		}
		else if(frm.doc.emoji=='Hug'){
			if(frm.doc.rating==1){html+='&#129303;</p>'}
			else if(frm.doc.rating==2){html+='&#129303;&#129303;</p>'}
			else if(frm.doc.rating==3){html+='&#129303;&#129303;&#129303;</p>'}
			else if(frm.doc.rating==4){html+='&#129303;&#129303;&#129303;&#129303;</p>'}
			else if(frm.doc.rating==5){html+='&#129303;&#129303;&#129303;&#129303;&#129303;</p>'}
		}
		else if(frm.doc.emoji=='Claps'){
			if(frm.doc.rating==1){html+='&#128079;</p>'}
			else if(frm.doc.rating==2){html+='&#128079;&#128079;</p>'}
			else if(frm.doc.rating==3){html+='&#128079;&#128079;&#128079;</p>'}
			else if(frm.doc.rating==4){html+='&#128079;&#128079;&#128079;&#128079;</p>'}
			else if(frm.doc.rating==5){html+='&#128079;&#128079;&#128079;&#128079;&#128079;</p>'}
		}
		else if(frm.doc.emoji=='Thumbs Up'){
			if(frm.doc.rating==1){html+='&#128077;</p>'}
			else if(frm.doc.rating==2){html+='&#128077;&#128077;</p>'}
			else if(frm.doc.rating==3){html+='&#128077;&#128077;&#128077;</p>'}
			else if(frm.doc.rating==4){html+='&#128077;&#128077;&#128077;&#128077;</p>'}
			else if(frm.doc.rating==5){html+='&#128077;&#128077;&#128077;&#128077;&#128077;</p>'}
		}
		else if(frm.doc.emoji=='Anger'){
			if(frm.doc.rating==1){html+='&#128545;</p>'}
			else if(frm.doc.rating==2){html+='&#128545;&#128545;</p>'}
			else if(frm.doc.rating==3){html+='&#128545;&#128545;&#128545;</p>'}
			else if(frm.doc.rating==4){html+='&#128545;&#128545;&#128545;&#128545;</p>'}
			else if(frm.doc.rating==5){html+='&#128545;&#128545;&#128545;&#128545;&#128545;</p>'}
		}
		$(frm.fields_dict['html_emoji'].wrapper).html(html);

	},
	refresh: function(frm) {
		var html='<p style="font-size:30px">'
		if(frm.doc.emoji=='Smiley'){
			if(frm.doc.rating==1){html+='&#128522;</p>'}
			else if(frm.doc.rating==2){html+='&#128522;&#128522;</p>'}
			else if(frm.doc.rating==3){html+='&#128522;&#128522;&#128522;</p>'}
			else if(frm.doc.rating==4){html+='&#128522;&#128522;&#128522;&#128522;</p>'}
			else if(frm.doc.rating==5){html+='&#128522;&#128522;&#128522;&#128522;&#128522;</p>'}
		}
		else if(frm.doc.emoji=='Hug'){
			if(frm.doc.rating==1){html+='&#129303;</p>'}
			else if(frm.doc.rating==2){html+='&#129303;&#129303;</p>'}
			else if(frm.doc.rating==3){html+='&#129303;&#129303;&#129303;</p>'}
			else if(frm.doc.rating==4){html+='&#129303;&#129303;&#129303;&#129303;</p>'}
			else if(frm.doc.rating==5){html+='&#129303;&#129303;&#129303;&#129303;&#129303;</p>'}
		}
		else if(frm.doc.emoji=='Claps'){
			if(frm.doc.rating==1){html+='&#128079;</p>'}
			else if(frm.doc.rating==2){html+='&#128079;&#128079;</p>'}
			else if(frm.doc.rating==3){html+='&#128079;&#128079;&#128079;</p>'}
			else if(frm.doc.rating==4){html+='&#128079;&#128079;&#128079;&#128079;</p>'}
			else if(frm.doc.rating==5){html+='&#128079;&#128079;&#128079;&#128079;&#128079;</p>'}
		}
		else if(frm.doc.emoji=='Thumbs Up'){
			if(frm.doc.rating==1){html+='&#128077;</p>'}
			else if(frm.doc.rating==2){html+='&#128077;&#128077;</p>'}
			else if(frm.doc.rating==3){html+='&#128077;&#128077;&#128077;</p>'}
			else if(frm.doc.rating==4){html+='&#128077;&#128077;&#128077;&#128077;</p>'}
			else if(frm.doc.rating==5){html+='&#128077;&#128077;&#128077;&#128077;&#128077;</p>'}
		}
		else if(frm.doc.emoji=='Anger'){
			if(frm.doc.rating==1){html+='&#128545;</p>'}
			else if(frm.doc.rating==2){html+='&#128545;&#128545;</p>'}
			else if(frm.doc.rating==3){html+='&#128545;&#128545;&#128545;</p>'}
			else if(frm.doc.rating==4){html+='&#128545;&#128545;&#128545;&#128545;</p>'}
			else if(frm.doc.rating==5){html+='&#128545;&#128545;&#128545;&#128545;&#128545;</p>'}
		}
		$(frm.fields_dict['html_emoji'].wrapper).html(html);

	}
});
