// Copyright (c) 2023, smart and contributors
// For license information, please see license.txt

frappe.ui.form.on('Final Settlement', {
	refresh: function(frm) {
		frm.events.hidden_zero_field(frm)
		frm.set_query("clearance_form", function () {
			return {
			  filters: [
				["docstatus", "=", 1],
			  ],
			};
		  });
	   
		
	},
	clearance_form:async function(frm){
		await frm.call({
			method: "calc_service_duration",
			doc: frm.doc,
			callback: function(r) {
				
				
			}
			
		});
		frm.events.hidden_zero_field(frm)

	},

	hidden_zero_field:function(frm){
		
		if (frm.doc.extra_work==0){frm.set_df_property('extra_work', 'hidden', 1)}
		if (frm.doc.transportation_allowance==0){frm.set_df_property('transportation_allowance', 'hidden', 1)}
		if (frm.doc.housing_allowance==0){frm.set_df_property('housing_allowance', 'hidden', 1)}
		if (frm.doc.other_allowances==0){frm.set_df_property('other_allowances', 'hidden', 1)}
		if (frm.doc.basic_salary==0){frm.set_df_property('basic_salary', 'hidden', 1)}
		if (frm.doc.nature_of_work==0){frm.set_df_property('nature_of_work', 'hidden', 1)}



	}
});
