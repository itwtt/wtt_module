frappe.pages['task-list'].on_page_load = function(wrapper) {
frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Task List')
	});

	let task_page = new TaskPage(wrapper);
	$(wrapper).bind('show', ()=> {
		task_page.show();
	});	
};
class TaskPage {
	constructor(wrapper) {
		this.wrapper = $(wrapper);
		this.page = wrapper.page;
		this.sidebar = this.wrapper.find('.layout-side-section');
		this.main_section = this.wrapper.find('.layout-main-section');
	}
	show() {
		frappe.breadcrumbs.add('wtt_module');
		this.sidebar.empty();
		let me = this;
		me.make_ticket();
	}
	make_ticket()
	{
		var val=frappe.session.user
		return frappe.xcall(
			'wtt_module.wtt_module.page.task_list.task_list.get_result', {
				tkt: val,
			}
		).then(data => {
			if (data) {
				var vtvalue='<style>.ticket-details{background-color: lightgrey;width: 200px;border: 8px solid cornflowerblue;}.ticket_go{font-weight: bold;font-size:18px;}</style>'
				vtvalue+='<br><br><div class="ticket-details"><center><p><b>Pending task count</b></p><p class="ticket_go">'+data[0].count[0]+'</p></center></div><br><br>'
				var htvalue='<style>th{font-size: 15px;text-align:center;color:#3CB371;}</style>'
				htvalue+="<table border='1px' style='margin-top:-1px;'><tr><th>TYPE OF WORK</th><th>DESCRIPTION</th><th>ASSIGNED DATE</th></tr>"
				for(var i in data)
				{
					if(data[i].type_of_work!=undefined)
						htvalue+='<tr style="text-align:center;"><td align="center">'+data[i].type_of_work+'.</td><td align="center">'+data[i].description+'<br></td><td align="left">'+data[i].assign_date+'</td></tr>'
				}
				htvalue+='</table>'

				this.page.set_title(__('Task Page'));
				this.main_section.empty().append(frappe.render_template('task_list',{
				ticket_go:vtvalue,
				arr_val:htvalue
				}));
			}
		});
	}
	/*
	make_button()
	{
		var ov=[]
		var val=frappe.session.user
		return frappe.xcall(
			'wtt_module.wtt_module.page.task_page.task_page.get_table', {
				usr: val,
			}
		).then(data => {
			if (data) {
			var htvalue='<style>th{font-size: 15px;text-align:center;color:#3CB371;}</style>'
			htvalue+="<table border='1px' style='margin-top:-1px;'><tr><th>TYPE OF WORK</th><th>DESCRIPTION</th><th>ASSIGNED DATE</th></tr>"	
			for(var i in data)
			{
				htvalue+='<tr style="text-align:center;"><td align="center">'+data[i].type_of_work+'.</td><td align="center">'+data[i].description+'<br></td><td align="left">'+data[i].assign_date+'</td></tr>'
			}
			htvalue+='</table>'
			this.page.set_title(__('Task Page'));
			this.main_section.empty().append(frappe.render_template('task_page1',{
			arr_val:htvalue
			}));
			}
		});
	}
	*/
}