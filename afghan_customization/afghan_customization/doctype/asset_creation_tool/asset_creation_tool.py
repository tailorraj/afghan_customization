# Copyright (c) 2023, Raaj Tailor and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class AssetCreationTool(Document):
	pass

@frappe.whitelist()
def generate_event_tags(initial_tag_no, initiator, total_qty):
    event_tags = []
    initiator = initiator.zfill(9)
    
    for i in range(int(total_qty)):
        # Increment the initiator value for each iteration
        current_initiator = str(int(initiator) + i).zfill(9)
        event_tags.append(f"{initial_tag_no}{current_initiator}")

    return event_tags


@frappe.whitelist()
def create_tag(self):
	try:
		self = json.loads(self)
		if self['asset_item']:
			for item in self['asset_item']:
				tag_doc = frappe.get_doc({
					'doctype': 'Asset Tag',
					'asset_tag_name': item['asset_tag_no'],
					'asset_id':item['asset_id'],
					'purchase_receipt':self['purchase_receipt'],
					'supplier':self['supplier']
				})
				tag_doc.save(ignore_permissions = 1)

			frappe.msgprint("Your Asset Tag Is Generated")
		else:
			frappe.msgprint("Asset Item Should Not Be Blank")	
	except:
		frappe.log_error(message=frappe.get_traceback(),title="Creation Of Asset Tag: ")
		frappe.msgprint("Error occured while creating the Asset Tag, Kindly check the logs")	

@frappe.whitelist()
def fetch_assets_from_asset(purchase_receipt):
	try:
		asset_data = frappe.db.sql("""select name from`tabAsset` where purchase_receipt = %(purchase_receipt)s and is_asset_tag_required = 1 """,({'purchase_receipt':purchase_receipt}),as_dict=1)
		if asset_data:
			return asset_data
		else:
			frappe.msgprint("No Asset Data Found For This Purchase Receipt: <b>{0}</b>".format(purchase_receipt))
	except:
		frappe.log_error(message=frappe.get_traceback(),title="Finding Of Asset From Asset: ")
		frappe.msgprint("Error occured while Finding the Asset, Kindly check the logs")		
