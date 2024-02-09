// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Task Allocation', {
	setup: function(frm,cdt,cdn) {
		frm.set_query("user", function() {
			return {
				filters: [
					["User","name","=", frappe.session.user]
				]
			}

		});
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
		// frm.set_indicator_formatter('type_of_work',
		// function (doc) {
		// 		if(doc.too_late==1) {
		// 			return "cyan";
		// 		}
		// 		else {
		// 			return (doc.status=='Completed') ? "green" : "orange";					
		// 		}
		// 	}
		// );
		
	},
	onload:function(frm,cdt,cdn){
		
		// $(".grid-add-row").hide();
	},
	refresh: function(frm) {
		if(frm.doc.user==frappe.session.user){
			frm.add_custom_button(__('Give Points'), () => frm.events.give_points());
		}
		if(frm.doc.user==undefined && frm.doc.owner){
		if(frappe.session.user=='ps_cmd@wttindia.com')
		{
		frm.set_value("user",'venkat@wttindia.com')	
		}
		else
		{
		frm.set_value("user",frm.doc.owner)
		}
		}
		else if(frm.doc.user==undefined){
		if(frappe.session.user=='ps_cmd@wttindia.com')
		{
		frm.set_value("user",'venkat@wttindia.com')	
		}
		else
		{
		frm.set_value("user",frappe.session.user)
		}
		}
	},
	// give_points:function(frm,cdt,cdn){
	// 	alert("Testing on process")
	// 	// for(var i in frm.doc.works_table){

	// 	// }
	// },
	validate:function(frm,cdt,cdn){
		calculate_total_points(frm,cdt,cdn);
		calculate_gained_points(frm,cdt,cdn);
	},
	split_task:function(frm,cdt,cdn){
		var arr=[]
		// alert("Test In Process")
		$.each(frm.doc.works_table, function (index, wt) {
			if(wt.__checked==true)
			{   
				var child = frm.add_child("task_split_table");
				frappe.model.set_value(child.doctype, child.name, "employee", "");
				frappe.model.set_value(child.doctype, child.name, "employee_name", "");
				frappe.model.set_value(child.doctype, child.name, "task_from", wt.name);
				frappe.model.set_value(child.doctype, child.name, "type_of_work", wt.type_of_work);
				frappe.model.set_value(child.doctype, child.name, "description", wt.description);
				frappe.model.set_value(child.doctype, child.name, "from_time", wt.from_time);
				frappe.model.set_value(child.doctype, child.name, "to_time", wt.to_time);
				frappe.model.set_value(child.doctype, child.name, "hours",wt.hours);
				frm.refresh_field("task_split_table");
				
			}
		});
	},
	allocate:function(frm,cdt,cdn){
		// alert("Test In Process")
		var arr=[]
		// alert("Test In Process")
		
		$.each(frm.doc.task_split_table, function (index, wt) {
			if(wt.allocated==0)	{
	 		arr.push({
			"employee":wt.employee,
			"employee_name":wt.employee_name,
			"type_of_work":wt.type_of_work,
			"description":wt.description,
			"from_time":wt.from_time,
			"to_time":wt.to_time,
			"hours":wt.hours,
			"split_no":wt.name
			})
			
	 		}
				
		   });
		frappe.call({
			method:"wtt_module.wtt_module.doctype.task_allocation.task_allocation.split_task",
			args:{
				"arr":arr
			}
		})
		
	}
});

frappe.ui.form.on('Work Update', {

	get_points:function(frm, cdt, cdn){
		var child = locals[cdt][cdn];
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.task_allocation.task_allocation.update_allocation2',
			args: { 
				assign_date:child.from_time,
				expected:child.to_time,
				hours:child.hours,
				actual:child.actual_time
			},
			callback(r) {
				// alert(JSON.stringify(r.message))
				for(var i=0;i<r.message.length;i++)
				{
					var act=child.actual_hours
				 	var actcompleted=r.message[i].actualcompleted
				 	var v=(actcompleted/act)*100
					if(v>0 && v<80)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 200);
						//+40
					}
					else if(v>80 && v<90)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 160);
						//+40
					}
					else if(v>90 && v<100)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 120);
						//+20
					}
					else if(v==100)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 100);
						//+20
					}
					else if(v>100 && v<=110)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 80);
						//-20
					}
					else if(v>110 && v<120)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 40);
						//-40
					}
					else if(v>120 && v<125)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 0);
						//-40
					}
					else if(v>125 && v<135)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", -20);
						//assign -20
					}
					else if(v>135 && v<145)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", -40);
						//assign -40	
					}
					else if(v>145 && v<=150)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", -100);
						//assign -40
					}
					else if(v>150)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", -200);
					}
					else
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 0);
						//0
					}
				frappe.model.set_value(cdt, cdn, "c_hrs",actcompleted);
				}
			}
		});
	},
	from_time: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
		// if(!frm.is_new()){
		// frappe.db.get_value('Employee', frm.doc.employee, 'user_id')
	 //    .then(r => {
	 //        if(frappe.session.user==r.message.user_id){
	 //        	frappe.throw("You cannot change Time")
	 //        }
	 //    })
		// }
	},
	to_time: function(frm, cdt, cdn) {
		// 
		// if(!frm.is_new()){
		// 	frappe.db.get_value('Employee', frm.doc.employee, 'user_id')
		//     .then(r => {
		//         if(frappe.session.user==r.message.user_id){
		//         	frappe.throw("You cannot change Time")
		//         }
		//     })			
		// }


		var child = locals[cdt][cdn];
		// if(child.to_time<=child.from_time){
		// 	frappe.model.set_value(cdt, cdn, "to_time", 0);
		// 	frappe.model.set_value(cdt, cdn, "hours", 0);
		// 	frappe.throw("Task needs time")
		// }
		var time_diff = (moment(child.to_time).diff(moment(child.from_time),"seconds")) / ( 60 * 60 * 24);
		var std_working_hours = 0;
		if(frm._setting_hours) return;
		var hours = moment(child.to_time).diff(moment(child.from_time), "seconds") / 3600;
		std_working_hours = time_diff * frappe.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			frappe.model.set_value(cdt, cdn, "hours", std_working_hours);
		} else {
			frappe.model.set_value(cdt, cdn, "hours", hours);
		}
	},
	hours: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	},
	// total_points:function(frm,cdt,cdn){
	// 	calculate_total_points(frm,cdt,cdn);
	// },
	// gained_points:function(frm,cdt,cdn){
	// 	calculate_gained_points(frm,cdt,cdn);
	// },
	status:function(frm, cdt, cdn) {

		var child = locals[cdt][cdn];
		if(child.status=='Completed')
		{
		var today = new Date();
		var date = today.getDate()+'-'+(today.getMonth()+1)+'-'+today.getFullYear();
		var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
		var dateTime = date+' '+time;
		frappe.model.set_value(cdt, cdn, "employee_completed_date", dateTime);	
		frappe.call({
			method: 'wtt_module.wtt_module.doctype.task_allocation.task_allocation.update_allocation',
			args: { 
				assign_date:child.from_time,
				expected:child.to_time,
				hours:child.hours
			},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{
					var actual=r.message[i].calculate_hrs
				 	var completed=r.message[i].completehrs-child.holded_hours
					if(child.holded_hours>r.message[i].completehrs){
						var completed=child.holded_hours-r.message[i].completehrs
					}
				 	var v=(completed/actual)*100
					if(v>0 && v<80)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 200);
						//+40
					}
					else if(v>80 && v<90)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 160);
						//+40
					}
					else if(v>90 && v<100)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 120);
						//+20
					}
					else if(v==100)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 100);
						//+20
					}
					else if(v>100 && v<=110)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 80);
						//-20
					}
					else if(v>110 && v<120)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 40);
						//-40
					}
					else if(v>120 && v<125)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 0);
						//-40
					}
					else if(v>125 && v<135)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", -20);
						//assign -20
					}
					else if(v>135 && v<145)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", -40);
						//assign -40	
					}
					else if(v>145 && v<=150)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", -100);
						//assign -40
					}
					else if(v>150)
					{
						frappe.model.set_value(cdt, cdn, "gained_points", -200);
						frappe.model.set_value(cdt, cdn, "too_late", 1);
					}
					else
					{
						frappe.model.set_value(cdt, cdn, "gained_points", 0);
						//0
					}
				frappe.model.set_value(cdt, cdn, "actual_hours", actual);
				frappe.model.set_value(cdt, cdn, "completed_hours",completed);
				}
				}
			
		});
		}
		else{
			frappe.model.set_value(cdt, cdn, "gained_points", 0);
			frappe.model.set_value(cdt, cdn, "too_late", 0);
		}
		// alert("Responding")
	},
	hold_resume:function(frm,cdt,cdn){
		if(frm.doc.user!=frappe.session.user){
			frappe.model.set_value(cdt, cdn, "hold_resume", "");
			frappe.throw("Only Task Allocator can Hold or Resume");

		}
		var child = locals[cdt][cdn];
		var arr=[]
		var currentdate = new Date();
		var datetime = currentdate.getFullYear() + "-" + (currentdate.getMonth()+1) + "-" + currentdate.getDate() + " " +
			currentdate.getHours() + ":" + currentdate.getMinutes() + ":" + currentdate.getSeconds();
		if(child.hold_resume=="Hold"){
			frappe.model.set_value(cdt, cdn, "holded_time", datetime);			
		}
		else if(child.hold_resume=="Resume"){
			if(child.holded_time==undefined){
				msgprint("There is no record that you holded the task");
				frappe.model.set_value(cdt, cdn, "hold_resume", "");
			}
			else{
				var hours = moment(datetime).diff(moment(child.holded_time), "seconds") / 3600;
				frappe.model.set_value(cdt, cdn, "resumed_time", datetime);
				frappe.model.set_value(cdt, cdn, "holded_hours", hours);

				var add_row = frm.add_child("holded_task");
				frappe.model.set_value(add_row.doctype, add_row.name, "task_name", child.type_of_work);
				frappe.model.set_value(add_row.doctype, add_row.name, "paused", child.holded_time);
				frappe.model.set_value(add_row.doctype, add_row.name, "resumed", datetime);
				frappe.model.set_value(add_row.doctype, add_row.name, "hours", hours);
				frappe.db.get_value('User', frappe.session.user, 'first_name')
				.then(r => {
					frappe.model.set_value(add_row.doctype, add_row.name, "hold_by", r.message.first_name);
				})

				frm.refresh_field("holded_task")
			}
		}
		
	},
	
});

frappe.ui.form.on('Task Split Table', {
	from_time: function(frm, cdt, cdn) {
		// frappe.db.get_value('Employee', frm.doc.employee, 'user_id')
	 //    .then(r => {
	 //        if(frappe.session.user==r.message.user_id){
	 //        	frappe.throw("You cannot change Time")
	 //        }
	 //    })
		calculate_end_time(frm, cdt, cdn);
	},
	to_time: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		var time_diff = (moment(child.to_time).diff(moment(child.from_time),"seconds")) / ( 60 * 60 * 24);
		var std_working_hours = 0;
		if(frm._setting_hours) return;
		var hours = moment(child.to_time).diff(moment(child.from_time), "seconds") / 3600;
		std_working_hours = time_diff * frappe.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			frappe.model.set_value(cdt, cdn, "hours", std_working_hours);
		} else {
			frappe.model.set_value(cdt, cdn, "hours", hours);
		}
	},
	hours: function(frm, cdt, cdn) {
		calculate_end_time(frm, cdt, cdn);
	}
});
var calculate_end_time = function(frm, cdt, cdn) {
	let child = locals[cdt][cdn];

	if(!child.from_time) {
		// if from_time value is not available then set the current datetime
		frappe.model.set_value(cdt, cdn, "from_time", frappe.datetime.get_datetime_as_string());
	}

	let d = moment(child.from_time);
	if(child.hours) {
		var time_diff = (moment(child.to_time).diff(moment(child.from_time),"seconds")) / (60 * 60 * 24);
		var std_working_hours = 0;
		var hours = moment(child.to_time).diff(moment(child.from_time), "seconds") / 3600;

		std_working_hours = time_diff * frappe.working_hours;

		if (std_working_hours < hours && std_working_hours > 0) {
			frappe.model.set_value(cdt, cdn, "hours", std_working_hours);
			frappe.model.set_value(cdt, cdn, "to_time", d.add(hours, "hours").format(frappe.defaultDatetimeFormat));
		} else {
			d.add(child.hours, "hours");
			frm._setting_hours = true;
			frappe.model.set_value(cdt, cdn, "to_time",
				d.format(frappe.defaultDatetimeFormat)).then(() => {
				frm._setting_hours = false;
			});
		}
	}
};


var calculate_total_points = function(frm) {
var temp = frm.doc.works_table;
var i,sum=0
for(i=0;i<temp.length;i++)
{
sum+=temp[i].total_points;
}
frm.set_value("out_of",sum);
};

var calculate_gained_points = function(frm) {
var temp = frm.doc.works_table;
var i,sum=0
for(i=0;i<temp.length;i++)
{
	if(temp[i].status=='Completed')
	{
		sum+=temp[i].gained_points;
	}
}
frm.set_value("total",sum);
};;