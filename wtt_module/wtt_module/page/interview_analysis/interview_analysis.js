frappe.pages['interview-analysis'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Interview Analysis',
		single_column: true
	});

	wrapper.sales_funnel = new erpnext.SalesFunnel(wrapper);
	frappe.breadcrumbs.add("wtt_module");
}

erpnext.SalesFunnel = class SalesFunnel {
	constructor(wrapper) {
		var me = this;
		// 0 setTimeout hack - this gives time for canvas to get width and height
		setTimeout(function() {
			me.setup(wrapper);
			me.get_data();
		}, 0);
	}

	setup(wrapper) {
		var me = this;
		this.employee_field = wrapper.page.add_field({"fieldtype": "Link", "fieldname": "interview", "options": "Interview process","label":__("Interview Process"),
			change: function() {
				me.interview = this.value;
				me.get_data();
			}
		}),
		this.elements = {
		layout: $(wrapper).find(".layout-main"),
		};

		this.elements.funnel_wrapper = $('<div class="funnel-wrapper text-center"></div>')
			.appendTo(this.elements.layout);
		}
get_data(btn) {
		var me=this;
		if(me.interview)
		{
		frappe.call({
			method: 'wtt_module.wtt_module.page.interview_analysis.interview_analysis.get_interview',
			args: {
				emp:me.interview
			},
			callback(r) {
				me.elements.funnel_wrapper.append(frappe.render_template('ticket_progress',{
				ticket_go:JSON.stringify(r.message)
				}));
			}
		});	
		}
		else
		{
		const $parent = me.elements.funnel_wrapper;
		var vtvalue=''
		$parent.html(__(vtvalue));
		}
}
}