// Copyright (c) 2023, wtt_module and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fabrication', {
	onload:function(frm)
	{
		if(frm.doc.fabrication_table)
		{

		}
		else
		{
			var fab=["SCREENER", "COOLING TOWER", "SLUDGE THICKENER", "CLARIFIER", "LAMELLA CLARIFIER", "MICRO FILTRATION", "REVERSE OSMOSIS"]
			for(var i=0;i<fab.length;i++)
			{
			var child = frm.add_child("fabrication_table");
			frappe.model.set_value(child.doctype, child.name, "system", fab[i]);
			frm.refresh_field("fabrication_table");
			}
		}
	}
});
