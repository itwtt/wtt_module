// Copyright (c) 2021, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('SWOT', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on("Strength", {
	weightage_score: function(frm,cdt, cdn){
		calculate_priority(frm, cdt, cdn);
	}
});

var calculate_priority = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	if(child.weightage_score<=4)
	{
		frappe.model.set_value(cdt, cdn, "priority","High");
	}
	else if(child.weightage_score<=7)
	{
		frappe.model.set_value(cdt, cdn, "priority","Medium");
	}
	else if(child.weightage_score<=10)
	{
		frappe.model.set_value(cdt, cdn, "priority","Low");
	}
};

frappe.ui.form.on("Weakness", {
	weightage_score: function(frm,cdt, cdn){
		calculate_priority1(frm, cdt, cdn);
	}
});

var calculate_priority1 = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	if(child.weightage_score<=4)
	{
		frappe.model.set_value(cdt, cdn, "priority","Low");
	}
	else if(child.weightage_score<=7)
	{
		frappe.model.set_value(cdt, cdn, "priority","Medium");
	}
	else if(child.weightage_score<=10)
	{
		frappe.model.set_value(cdt, cdn, "priority","High");
	}
};

frappe.ui.form.on("Opportunity Table", {
	weightage_score: function(frm,cdt, cdn){
		calculate_priority2(frm, cdt, cdn);
	}
});

var calculate_priority2 = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	if(child.weightage_score<=4)
	{
		frappe.model.set_value(cdt, cdn, "priority","High");
	}
	else if(child.weightage_score<=7)
	{
		frappe.model.set_value(cdt, cdn, "priority","Medium");
	}
	else if(child.weightage_score<=10)
	{
		frappe.model.set_value(cdt, cdn, "priority","Low");
	}
};

frappe.ui.form.on("Threat", {
	weightage_score: function(frm,cdt, cdn){
		calculate_priority4(frm, cdt, cdn);
	}
});

var calculate_priority4 = function(frm, cdt, cdn) {
	var child = locals[cdt][cdn];
	if(child.weightage_score<=4)
	{
		frappe.model.set_value(cdt, cdn, "priority","Low");
	}
	else if(child.weightage_score<=7)
	{
		frappe.model.set_value(cdt, cdn, "priority","Medium");
	}
	else if(child.weightage_score<=10)
	{
		frappe.model.set_value(cdt, cdn, "priority","High");
	}
};