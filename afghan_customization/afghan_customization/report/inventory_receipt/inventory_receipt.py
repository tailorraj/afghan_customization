# Copyright (c) 2023, Raaj Tailor and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data



def get_data(filters):
    inventory_receipt_data = get_inventory_receipt_data(filters)
    inventory_data = []

    for item in inventory_receipt_data:
        pr_no = item['purchase_receipt']
        item_code_data = item['item_code']
        asset_tag_data = frappe.db.sql(
            """
            SELECT asset_tag_no, purchase_receipt, item_code
            FROM `tabAsset`
            WHERE asset_tag_no IS NOT NULL AND purchase_receipt = %(purchase_receipt)s AND item_code = %(item_code)s
            """,
            {'purchase_receipt': pr_no, 'item_code': item_code_data},
            as_dict=True
        )

        item['asset_tags'] = [asset['asset_tag_no'] for asset in asset_tag_data]

        # Calculate the outstanding_qty directly here
        item['outstanding_qty'] = item['po_qty'] - item['pr_qty']

        inventory_data.append({
            "item_code": item["item_code"],
            "description": item["description"],
            "serial_no": item["serial_no"],
            "make": item['make'],
            "model": item['model'],
            "capacity": item['capacity'],
            "po_requester": item['po_requester'],
            "purchase_receipt": item['purchase_receipt'],
            "purchase_order": item['purchase_order'],
            "supplier": item['supplier'],
            "set_warehouse": item['set_warehouse'],
            "po_qty": item['po_qty'],
            "pr_qty": item['pr_qty'],
            "outstanding_qty": item['outstanding_qty'],
            "rejected_qty": item['rejected_qty'],
            "posting_date": item['posting_date'],
            "assigned_representative": item['assigned_representative'],
            "status": item['status'],
            "asset_tags": ", ".join(item['asset_tags'])
        })

    return inventory_data

def get_inventory_receipt_data(filters):
	inventory_receipt_data = frappe.db.sql("""
		SELECT
			pri.item_code, pri.description, pri.serial_no, pri.make, pri.model, pri.capacity, pr.po_requester,
			pr.name as purchase_receipt, pri.purchase_order, po.transaction_date, pr.supplier, pr.set_warehouse,
			SUM(poi.qty) as po_qty, pri.qty as pr_qty, SUM(poi.qty - pri.received_qty) as outstanding_qty, pri.rejected_qty,
			pr.posting_date, pri.assigned_representative, po.status
		FROM `tabPurchase Receipt` pr
			INNER JOIN `tabPurchase Receipt Item` pri ON pr.name = pri.parent
			LEFT JOIN `tabPurchase Order` po ON po.name = pri.purchase_order
			INNER JOIN `tabPurchase Order Item` poi ON po.name = poi.parent
		WHERE 
			pr.docstatus = 1 {conditions}
		GROUP BY pri.item_code, pri.description, pri.serial_no, pri.make, pri.model, pri.capacity, pr.po_requester,
		pr.name, pri.purchase_order, po.transaction_date, pr.supplier, pr.set_warehouse,
		pri.qty, pri.rejected_qty, pr.posting_date, pri.assigned_representative, po.status
	""".format(conditions=get_conditions(filters)), filters, as_dict=1)
	return inventory_receipt_data


def get_conditions(filters):
	conditions = []
	

	if filters.get("item_code"):
		conditions.append("pri.item_code=%(item_code)s")

	if filters.get("purchase_receipt"):
		conditions.append("pr.name=%(purchase_receipt)s")

	if filters.get("purchase_order"):
		conditions.append("pri.purchase_order=%(purchase_order)s")

	if filters.get("set_warehouse"):
		conditions.append("pr.set_warehouse=%(set_warehouse)s")

	if filters.get("user_approver"):
		conditions.append("pri.assigned_representative=%(user_approver)s")	

	if filters.get("po_requester_name"):
		conditions.append("pr.po_requester=%(po_requester_name)s")

	if filters.get("po_status"):
		conditions.append("po.status=%(po_status)s")	
				

	return "and {}".format(" and ".join(conditions)) if conditions else ""	

def get_columns(filters):
	columns =[
		{
			"label":_("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Item Description"),
			"fieldname": "description",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Serial No"),
			"fieldname": "serial_no",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Make"),
			"fieldname": "make",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Model"),
			"fieldname": "model",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Capacity"),
			"fieldname": "capacity",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("PR No"),
			"fieldname": "purchase_receipt",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("PO No"),
			"fieldname": "purchase_order",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Vendor Name"),
			"fieldname": "supplier",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Location/WH"),
			"fieldname": "set_warehouse",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("PO Qty"),
			"fieldname": "po_qty",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"label":_("Qty Received"),
			"fieldname": "pr_qty",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"label":_("Tag Number"),
			"fieldname": "asset_tags",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Outstanding Qty"),
			"fieldname": "outstanding_qty",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"label":_("Qty Cancelled"),
			"fieldname": "rejected_qty",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"label":_("Date Received"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label":_("User Approver"),
			"fieldname": "assigned_representative",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("PO Requster"),
			"fieldname": "po_requester",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("PO Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 120
		},
		
	]
	return columns
