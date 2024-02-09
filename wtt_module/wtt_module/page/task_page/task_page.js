/*
frappe.pages['task-page'].on_page_load = function(wrapper) {
	new MyPage(wrapper);
}

MyPage = Class.extend({
	init: function(wrapper) {
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'Pending Works',
			single_column: true
		});
		this.make();
	},
	make: function() {
		val=frappe.session.user
		return frappe.xcall(
			'wtt_module.wtt_module.page.task_page.task_page.get_result', {
				tkt: val,
			}
		).then(data => {
			if (data) {
			$(frappe.render_template("task_page", this)).appendTo(this.page.main);
			//	this.page.set_title(__('Pending task'));
			//	this.main_section.empty().append(frappe.render_template('task_page',{
			//	ticket_go:data
			//}));
			}
		});		
		//$(frappe.render_template("task_page", this)).appendTo(this.page.main);
	}
})
*/
frappe.pages['task-page'].on_page_load = function(wrapper) {
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

		let ticketno1 = frappe.ui.form.make_control({
			parent: me.sidebar,
			df: {
				fieldtype: 'Button',
				fieldname: 'btn',
				label:'Get count',
				click: () => {
					me.make_ticket();
				}
			}
		});
		ticketno1.refresh();
		this.sidebar.find('[data-fieldname="ticketno1"]').append('<div class="ticket-info"></div>');

		let ticketno = frappe.ui.form.make_control({
			parent: me.sidebar,
			df: {
				fieldtype: 'Button',
				fieldname: 'btn',
				label:'Get works',
				click: () => {
					me.make_button();
				}
			}
		});
		ticketno.refresh();
		this.sidebar.find('[data-fieldname="ticketno"]').append('<div class="ticket-info"></div>');
	}
	make_ticket()
	{
		var val=frappe.session.user
		return frappe.xcall(
			'wtt_module.wtt_module.page.task_page.task_page.get_result', {
				tkt: val,
			}
		).then(data => {
			if (data) {
				this.page.set_title(__('Task Page'));
				this.main_section.empty().append(frappe.render_template('task_page',{
				ticket_go:data
				}));
			}
		});
	}
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
}