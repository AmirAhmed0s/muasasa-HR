// Copyright (c) 2023, smart and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Credit Balance Extensions"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			fieldname: "territory",
			label: __("Territory"),
			fieldtype: "MultiSelectList",
			options: ["Territory"],
			depends_on: "eval:!doc.party",
			get_data: function (txt) {
			  return frappe.db.get_link_options("Territory", txt);
			},
		  },
		  {
			fieldname: "customer_group",
			label: __("Customer Group"),
			fieldtype: "MultiSelectList",
			options: ["Customer Group"],
			depends_on: "eval:!doc.party",
			get_data: function (txt) {
			  return frappe.db.get_link_options("Customer Group", txt);
			},
		  },
		{
			fieldname: "payment_terms",
			label: __("Payment Terms"),
			fieldtype: "MultiSelectList",
			options: ["Payment Terms Template"],
			depends_on: "eval:!doc.party",
			get_data: function (txt) {
			  return frappe.db.get_link_options("Payment Terms Template", txt);
			},
		  },
	]
}