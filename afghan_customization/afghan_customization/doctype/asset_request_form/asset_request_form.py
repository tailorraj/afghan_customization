# Copyright (c) 2023, Raaj Tailor and contributors
# For license information, please see license.txt

from urllib import request
import frappe
from frappe.model.document import Document
import json
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate

class AssetRequestForm(Document):
	# pass
	def validate(self):
		for item in self.item_request:
			if item.make:
				make_model_value=frappe.db.get_value('Make Model Capacity',{'make':item.make,'parent':item.item},['model','capacity'],as_dict=1)
				if make_model_value:
					item.model = make_model_value.model
					item.capacity = make_model_value.capacity

			# Set received_by from location
			received_by = frappe.db.get_value('Location',self.location,'representative')
			if received_by:
				item.received_by = received_by 

	def on_submit(self):
		for row in self.item_request:
			if row.is_asset_item == 0:
				create_material_request(self)
			elif row.is_asset_item == 1:	
				create_asset_movement_configuration(self)
	


def create_material_request(self):
	try:
		mr_doc = frappe.get_doc({
			'doctype':'Material Request',
			'transaction_date':self.date,
			'material_request_type':'Material Transfer',
			'schedule_date':self.date,
			'asset_request_form':self.name,
			'set_warehouse':frappe.db.get_value('Location',self.location,'warehouse') or 'AWCC Warehouse - AWCC',
			'items':[]		
		})
		for item in self.item_request:
			if item.is_asset_item == 0:
				item_doc = {
					'doctype':'Material Request Item',
					'item_code':item.item,
					'qty':item.qty,
					'warehouse':'AWCC Warehouse - AWCC'
				}
				
				mr_doc.append('items', item_doc)

		mr_doc.insert(ignore_permissions = 1)
		frappe.msgprint("Your Material Request Is Created")
	except:
		frappe.log_error(message=frappe.get_traceback(),title="Creation Of Material Reuest From Asset Request Form: ")
		frappe.throw("Error occured while creating the Material Request, Kindly check the logs")


def create_asset_movement_configuration(self):
	try:
		amc_doc = frappe.get_doc({
			'doctype':'Asset Movement Configuration',
			'date':self.date,
			'asset_request_form':self.name,
			'location':self.location,
			'asset_item':[]
		})
		for row in self.item_request:
			if row.is_asset_item == 1:
				amc_item_doc = {
					'doctype':'Asset Movement Configuration Item',
					'item':row.item,
					'make':row.make,
					'model':row.model,
					'capacity':row.capacity,
					'asset_tag':row.asset_tag,
				}
				amc_doc.append('asset_item',amc_item_doc)
		
		amc_doc.insert(ignore_permissions = 1)
		frappe.msgprint("Your Asset Movement Configuration Is Created")
	except:
		frappe.log_error(message=frappe.get_traceback(),title="Creation Of Asset Movement Configuration From Asset Request Form: ")
		frappe.throw("Error occured while creating the Asset Movement Configuration, Kindly check the logs")

@frappe.whitelist()
def create_todo(self):
	self = json.loads(self)
	try:
		if not frappe.db.exists('ToDo',{'reference_name':self['name']}):
			todo_doc = frappe.get_doc({
				'doctype':'ToDo',
				'status':'Open',
				'priority':'High',
				'date':self['date'],
				'allocated_to':self['hod'],
				'description':'Please Check Asset Request Form: <b>{0}</b>'.format(self['name']),
				'reference_type':'Asset Request Form',
				'reference_name':self['name'],
				'assigned_by':self['requested_by']
			})
			todo_doc.insert(ignore_permissions =1)
			todo = todo_doc.name
			frappe.msgprint("Your Todo Document Name Is: <b>{0}</b> created".format(todo))
		else:
			frappe.msgprint("ToDo Is Already Created For This Asset Request Form!")

	except Exception as e:
		frappe.log_error(message=frappe.get_traceback(),title="Creation Of ToDo From Asset Request Form: ")
		frappe.throw("Error occured while creating the ToDo, Kindly check the logs")	


@frappe.whitelist()
def make_asset_transfer(source_name, target_doc=None):
	 
	doc = get_mapped_doc(
		"Asset Request Form",
		source_name,
		{
			"Asset Request Form": {
				"doctype": "Asset Transfer",
				"validation": {
					"docstatus": ["=", 1],
				},
			},
			"AWCC Request Item": {
				"doctype": "Asset Transfer Item",
				"field_map": {
					"item":"item",
					"make":"make",
					"model":"model",
					"capacity":"capacity",
					"asset_tag":"asset_tag",
					'location':'from_location'
				},
				"condition": lambda row: row.is_asset_item == 1,
			},
		},
		target_doc,
	)
	for item in doc.get("item_table"):
		item.from_location = doc.location

	return doc



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def asset_tag_filter(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT at.name,a.name
        FROM `tabAsset Tag` at
        Left Join`tabAsset` a on at.asset_id = a.name 
        WHERE a.item_code = %(item_code)s AND a.item_code LIKE %(txt)s
        {mcond}
        """.format(**{
            'key': searchfield,
            'mcond':get_match_cond(doctype)
        }),
        {
        "item_code" :filters.get("item_code") ,
        'txt': "%{}%".format(txt),
        '_txt': txt.replace("%", "")
        }
        )

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def item_make_filter(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT ma.make,ma.model,ma.capacity
        FROM `tabMake Model Capacity` ma
        Inner Join`tabItem` i on i.name = ma.parent 
        WHERE i.name = %(item)s AND i.name LIKE %(txt)s
        {mcond}
        """.format(**{
            'key': searchfield,
            'mcond':get_match_cond(doctype)
        }),
        {
        "item" :filters.get("item") ,
        'txt': "%{}%".format(txt),
        '_txt': txt.replace("%", "")
        }
        )