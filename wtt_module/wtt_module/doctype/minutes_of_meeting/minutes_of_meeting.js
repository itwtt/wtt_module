// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Minutes of Meeting', {
	get_participants:function(frm,cdt,cdn){
		frappe.call({
		    method: "wtt_module.wtt_module.doctype.minutes_of_meeting.minutes_of_meeting.get_participants",
		    args:
		    {
		    	"conference_hall_booking":frm.doc.conference_hall_booking
		    },
		    callback: function (r) {
		        if (r.message) {
		            var participants = r.message[0].participants.split(',');
		            var formattedParticipants = participants.join(',\n');
		            frm.set_value("participants", formattedParticipants);
		            refresh_field("participants");
		            frm.set_value("from_time", r.message[0].from_time);
		            refresh_field("from_time");
		            frm.set_value("to_time", r.message[0].to_time);
		            refresh_field("to_time");
		            frm.set_value("project", r.message[0].project);
		            refresh_field("project");
		            frm.set_value("review_no", r.message[0].review_no);
		            refresh_field("review_no");
		            frm.set_value("venue", r.message[0].venue);
		            refresh_field("venue");
		        }
		    }
		});
	},
});
