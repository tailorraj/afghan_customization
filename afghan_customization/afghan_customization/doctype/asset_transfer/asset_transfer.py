# Copyright (c) 2023, Raaj Tailor and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AssetTransfer(Document):
	# pass
	def on_submit(self):
		create_asset_movement(self)


def create_asset_movement(self):
    success = False

    try:
        am_doc = frappe.get_doc({
            'doctype': 'Asset Movement',
            'transaction_date': self.date,
            'purpose': 'Transfer',
            'assets': [], 
        })

        for d in self.item_table:
            am_item = {
                'doctype': 'Asset Movement Item',
                'asset': d.asset,
                'asset_name': frappe.db.get_value('Item', d.item, 'item_name'),
                'source_location': self.location,
                'asset_tag': d.asset_tag,
                'make': d.make,
                'model': d.model,
                'capacity': d.capacity,
                'target_location': self.to_location,
            }
            
            am_doc.append('assets', am_item)

        am_doc.insert(ignore_permissions=1)
        success = True

    except:
        frappe.log_error(message=frappe.get_traceback(), title="Creation Of Asset Movement From Asset Transfer: ")
        frappe.msgprint("Error occurred while creating the Asset Movement, Kindly check the logs")

    if success:
        frappe.msgprint("Asset Movement created successfully!")

