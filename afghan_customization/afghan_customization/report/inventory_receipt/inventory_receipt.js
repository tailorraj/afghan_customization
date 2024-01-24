// Copyright (c) 2023, Raaj Tailor and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Inventory Receipt"] = {
	"filters": [

		{
			"fieldname":"item_code",
			"label":__("Item"),
			"fieldtype":"Link",
			"options":"Item"
		},
		{
			"fieldname":"purchase_receipt",
			"label":__("PR Number"),
			"fieldtype":"Link",
			"options":"Purchase Receipt"
		},
		{
			"fieldname":"purchase_order",
			"label":__("PO Number"),
			"fieldtype":"Link",
			"options":"Purchase Order"
		},
		{
			"fieldname":"set_warehouse",
			"label":__("Location/WH"),
			"fieldtype":"Link",
			"options":"Warehouse"
		},
		{
			"fieldname":"user_approver",
			"label":__("User Approver"),
			"fieldtype":"Link",
			"options":"User"
		},
		{
			"fieldname":"po_requester_name",
			"label":__("PO Requester"),
			"fieldtype":"Link",
			"options":"User"
		},
		{
			"fieldname":"po_status",
			"label":__("PO Status"),
			"fieldtype":"Select",
			"options":"\nDraft\nOn Hold\nTo Receive and Bill\nTo Bill\nTo Receive\nCompleted\nCancelled\nClose\nDelivered"
		},

	]
};
