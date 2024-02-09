frappe.pages['entries-count'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Entries page',
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
		this.employee_field = wrapper.page.add_field({"fieldtype": "Link", "fieldname": "employee", "options": "Employee",
			"label": __("Employee"),
			change: function() {
				me.employee = this.value;
				me.get_data();
			}
		}),

		this.project_field = wrapper.page.add_field({"fieldtype": "Link", "fieldname": "project", "options": "Project",
			"label": __("Project"),
			change: function() {
				me.project = this.value;
				me.get_data();
			}
		}),
			
		this.elements = {
			layout: $(wrapper).find(".layout-main"),
			from_date: wrapper.page.add_date(__("From Date")),
			to_date: wrapper.page.add_date(__("To Date")),
		};

		this.elements.funnel_wrapper = $('<div class="funnel-wrapper text-center"></div>')
			.appendTo(this.elements.layout);

		this.options = {
			from_date: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			to_date: frappe.datetime.get_today(),
		};

		$.each(this.options, function(k, v) {
			if (['from_date', 'to_date'].includes(k)) {
				me.elements[k].val(frappe.datetime.str_to_user(v));
			} else {
				me.elements[k].val(v);
			}

			me.elements[k].on("change", function() {
				if (['from_date', 'to_date'].includes(k)) {
					me.options[k] = frappe.datetime.user_to_str($(this).val()) != 'Invalid date' ? frappe.datetime.user_to_str($(this).val()) : frappe.datetime.get_today();
				} else {
					me.options.chart = $(this).val();
				}
				me.get_data();
			});
		});
	}
	get_data(btn) {
		var me = this;
		if(me.employee && me.project)
		{
		frappe.call({
			method: 'wtt_module.wtt_module.page.entries_count.entries_count.get_value3',
			args: {
				emp:me.employee,
				project:me.project,
				fr_date: me.options.from_date,
				to_date: me.options.to_date
			},
			callback(r) {
				const $parent = me.elements.funnel_wrapper;
				var vtvalue='<style>.ticket-details{background-color: lightgrey;width: 200px;border: 8px solid cornflowerblue;}.ticket_go{font-weight: bold;font-size:18px;}</style>'
				vtvalue+="<br><br><table cellpadding='20' cellspacing='20'><tr><td>"
				vtvalue+='<div class="ticket-details"><center><p><b>Created MR</b></p><p class="ticket_go">'+r.message[0].created[0]+'</p></center></div><br><br>'
				vtvalue+="</td><td>"
				vtvalue+='<div class="ticket-details"><center><p><b>Approved by HOD MR</b></p><p class="ticket_go">'+r.message[1].approved_hod[0]+'</p></center></div><br><br>'
				vtvalue+='</td><td><div class="ticket-details"><center><p><b>Approved by MD MR</b></p><p class="ticket_go">'+r.message[2].approved[0]+'</p></center></div><br><br>'
				vtvalue+="</td></tr></table>"
				$parent.html(__(vtvalue));
			}
		});	
		}
		else if(me.employee)
		{
			frappe.call({
			method: 'wtt_module.wtt_module.page.entries_count.entries_count.get_value1',
			args: {
				emp:me.employee,
				fr_date: me.options.from_date,
				to_date: me.options.to_date
			},
			callback(r) {
				const $parent = me.elements.funnel_wrapper;
				var vtvalue='<style>.ticket-details{background-color: lightgrey;width: 200px;border: 8px solid cornflowerblue;}.ticket_go{font-weight: bold;font-size:18px;}</style>'
				vtvalue+="<br><br><table cellpadding='20' cellspacing='20'><tr><td>"
				vtvalue+='<div class="ticket-details"><center><p><b>Created MR</b></p><p class="ticket_go">'+r.message[0].created[0]+'</p></center></div><br><br>'
				vtvalue+="</td><td>"
				vtvalue+='<div class="ticket-details"><center><p><b>Approved by HOD MR</b></p><p class="ticket_go">'+r.message[1].approved_hod[0]+'</p></center></div><br><br>'
				vtvalue+='</td><td><div class="ticket-details"><center><p><b>Approved by MD MR</b></p><p class="ticket_go">'+r.message[2].approved[0]+'</p></center></div><br><br>'
				vtvalue+="</td></tr></table>"
				$parent.html(__(vtvalue));
			}
		});
		}
		else if(me.project)
		{
			frappe.call({
			method: 'wtt_module.wtt_module.page.entries_count.entries_count.get_value2',
			args: {
				project:me.project,
				fr_date: me.options.from_date,
				to_date: me.options.to_date
			},
			callback(r) {
				const $parent = me.elements.funnel_wrapper;
				var vtvalue='<style>.ticket-details{background-color: lightgrey;width: 200px;border: 8px solid cornflowerblue;}.ticket_go{font-weight: bold;font-size:18px;}</style>'
				vtvalue+="<br><br><table cellpadding='20' cellspacing='20'><tr><td>"
				vtvalue+='<div class="ticket-details"><center><p><b>Created MR</b></p><p class="ticket_go">'+r.message[0].created[0]+'</p></center></div><br><br>'
				vtvalue+="</td><td>"
				vtvalue+='<div class="ticket-details"><center><p><b>Approved by HOD MR</b></p><p class="ticket_go">'+r.message[1].approved_hod[0]+'</p></center></div><br><br>'
				vtvalue+='</td><td><div class="ticket-details"><center><p><b>Approved by MD MR</b></p><p class="ticket_go">'+r.message[2].approved[0]+'</p></center></div><br><br>'
				vtvalue+="</td></tr></table>"
				$parent.html(__(vtvalue));
			}
		});
		}
		else
		{
		frappe.call({
			method: 'wtt_module.wtt_module.page.entries_count.entries_count.get_value',
			args: {
				fr_date: me.options.from_date,
				to_date: me.options.to_date
			},
			callback(r) {
				const $parent = me.elements.funnel_wrapper;
				var vtvalue='<style>.ticket-details{background-color: lightgrey;width: 200px;border: 8px solid cornflowerblue;}.ticket_go{font-weight: bold;font-size:18px;}</style>'
				vtvalue+="<br><br><table cellpadding='20' cellspacing='20'><tr><td>"
				vtvalue+='<div class="ticket-details"><center><p><b>Created MR</b></p><p class="ticket_go">'+r.message[0].created[0]+'</p></center></div><br><br>'
				vtvalue+="</td><td>"
				vtvalue+='<div class="ticket-details"><center><p><b>Approved by HOD MR</b></p><p class="ticket_go">'+r.message[1].approved_hod[0]+'</p></center></div><br><br>'
				vtvalue+='</td><td><div class="ticket-details"><center><p><b>Approved by MD MR</b></p><p class="ticket_go">'+r.message[2].approved[0]+'</p></center></div><br><br>'
				vtvalue+="</td></tr></table>"
				$parent.html(__(vtvalue));
			}
		});
		}
	}
}