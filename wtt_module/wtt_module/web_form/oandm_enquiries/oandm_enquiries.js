frappe.ready(function(frm) {
    // frappe.web_form.after_load = () => {
    //     frappe.web_form.on('plant', (field, doc) => {
        var arr=['Plant inlet water','Biological tank I/l','Biological tank','Secondary clarifier o/l'];
        frappe.call({
			method: 'wtt_module.wtt_module.web_form.oandm_enquiries.oandm_enquiries.func',
			args: { 
				arr:arr
			},
			callback(r) {
				for(var i=0;i<r.message.length;i++)
				{

				var child = web_form.add_child("parameters");
				frappe.model.set_value(child.doctype, child.name, "tank", r.message[i].tank);
				// frappe.model.set_value(child.doctype, child.name, "rounded_total", r.message[i].rounded_total);
				// frappe.model.set_value(child.doctype, child.name, "salary_id", r.message[i].salary_id);
				web_form.refresh_field("parameters");
				}
			}
		});
        // })
    // }
})

