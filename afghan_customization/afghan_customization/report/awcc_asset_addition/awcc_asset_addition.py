# Copyright (c) 2023, Raaj Tailor and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data

def get_data(filters):
	data= frappe.db.sql("""
	select a.name,a.location,a.item_name,a.status,a.asset_tag_no,a.custodian,a.purchase_receipt,a.asset_category,a.purchase_date,
	afb.depreciation_start_date,afb.total_number_of_depreciations
	from`tabAsset` a
	Inner Join`tabAsset Finance Book` afb on afb.parent = a.name
	where
	a.calculate_depreciation = 1 and
	a.docstatus = 1			 
	""",as_dict=1)
	return data


def get_columns(filters):

	columns =[
		{
			"label":_("Asset"),
			"fieldname": "name",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Location"),
			"fieldname": "location",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Description"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Quantity"),
			"fieldname": "quantity",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"label":_("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Asset Serial No"),
			"fieldname": "asset_serial_no",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Tag Number"),
			"fieldname": "asset_tag_no",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Asignee"),
			"fieldname": "custodian",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("PR Number"),
			"fieldname": "purchase_receipt",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Main Category"),
			"fieldname": "asset_category",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Sub Category"),
			"fieldname": "sub_category",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Minor Category"),
			"fieldname": "minor_category",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Date Of Aquistion"),
			"fieldname": "purchase_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label":_("Depreciation Start Date"),
			"fieldname": "depreciation_start_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label":_("Depreciation End Date"),
			"fieldname": "depreciation_end_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label":_("Estimated Useful Life"),
			"fieldname": "estimated_useful_life",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("No of Monts Depreciated"),
			"fieldname": "total_number_of_depreciations",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Remaining Life"),
			"fieldname": "remaining_life",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Addition for the year"),
			"fieldname": "addition_for_the_year",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Cost Adjustment"),
			"fieldname": "cost_adjustment",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("sum_of_cost"),
			"fieldname": "sum_of_cost",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"label":_("Depreciation for the year"),
			"fieldname": "depreciation_for_the_year",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("Acc. Dep Current Year"),
			"fieldname": "acc_dep_current_year",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label":_("NBV B4 Disposal and Impairment"),
			"fieldname": "nbv_b4_disposal_and_impairment",
			"fieldtype": "Data",
			"width": 120
		},
		
	]
	return columns
