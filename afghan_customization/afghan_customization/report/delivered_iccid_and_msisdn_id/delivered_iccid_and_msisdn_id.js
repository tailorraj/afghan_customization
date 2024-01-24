// Copyright (c) 2023, Raaj Tailor and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Delivered ICCID And MSISDN ID"] = {
	"filters": [
		{
			"fieldname":"sales_invoice",
			"label":__("Sales Invoice"),
			"fieldtype":"Link",
			"options":"Sales Invoice"
		},
		{
			"fieldname":"name",
			"label":__("Serial No"),
			"fieldtype":"Data"
		},
		{
			"fieldname":"msisdn",
			"label":__("MSISDN"),
			"fieldtype":"Data"
		}
	]
};
