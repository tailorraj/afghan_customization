# Copyright (c) 2023, Raaj Tailor and contributors
# For license information, please see license.txt

from multiprocessing import Condition
import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters), get_data( filters)
	return columns, data

def get_data(filters):
	data = frappe.db.sql("""
		Select
		sn.delivery_document_no,
		sn.delivery_date,
		sn.name,
		sn.item_code,
		sn.msisdn,
		si.customer_name,
		si.set_warehouse


		From
		`tabSerial No` sn
		INNER JOIN `tabSales Invoice` si on sn.delivery_document_no = si.name

		Where
		sn.status = "Delivered" and sn.delivery_document_type = "Sales Invoice" {conditions}
	""".format(conditions=get_conditions(filters)),filters, as_dict=1)
	return data

def get_conditions(filters):
	conditions = []
	

	if filters.get("sales_invoice"):
		conditions.append("sn.delivered_document_no=%(sales_invoice)s")

	if filters.get("name"):
		conditions.append("sn.name=%(name)s")

	if filters.get("msisdn"):
		conditions.append("sn.msisdn=%(msisdn)s")
				

	return "and {}".format(" and ".join(conditions)) if conditions else ""	

def get_columns(filters):
	columns =[
		{
			"label":_("Delivered Document No"),
			"fieldname": "delivery_document_no",
			"fieldtype": "Data",
			"width": 220
		},
		{
			"label":_("Delivered Date"),
			"fieldname": "delivery_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label":_("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options":"Item",
			"width": 150
		},
		{
			"label":_("Customer"),
			"fieldname": "customer_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label":_("Serial No"),
			"fieldname": "name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label":_("MSISDN"),
			"fieldname": "msisdn",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label":_("Warehouse"),
			"fieldname": "set_warehouse",
			"fieldtype": "Data",
			"width": 150
		},
	]
	return columns