# Copyright (c) 2023, Raaj Tailor and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.desk.reportview import get_filters_cond, get_match_cond

class AssetMovementConfiguration(Document):
	# pass
    def on_submit(self):
        create_asset_movement(self)
        for item in self.asset_item:
            frappe.db.set_value('AWCC Request Item',{'item':item.item,'parent':self.asset_request_form},'asset_tag',item.asset_tag) 
            frappe.db.set_value('AWCC Request Item',{'item':item.item,'parent':self.asset_request_form},'asset',item.asset) 

            frappe.db.commit()

def create_asset_movement(self):
    try:
        am_doc = frappe.get_doc({
            'doctype':'Asset Movement',
            'company':'Afghan Wireless Communication Company',
            'purpose':'Transfer',
            'transaction_date':self.date,
            'reference_doctype':'',
            'reference_name':''
        })
        for item in self.asset_item:
            asset_from = frappe.db.get_value('Asset',item.asset,'purchase_receipt')
            if asset_from:
                reference_name = asset_from
                reference_type = 'Purchase Receipt'
            else:
                reference_name = frappe.db.get_value('Asset',item.asset,'purchase_invoice')
                reference_type = 'Purchase Invoice'   
            
            am_item_doc = {
                'doctype':'Asset Movement Item',
                'asset':item.asset,
                'source_location':item.from_location,
                'target_location':item.target_location,
                'make':item.make,
                'model':item.model,
                'capacity':item.capacity,
                'asset_tag':item.asset_tag
            }
            am_doc.append('assets',am_item_doc)
        
        am_doc.reference_name = reference_name
        am_doc.reference_doctype = reference_type

        am_doc.insert(ignore_permissions = 1)
        frappe.msgprint("Your Assets Movement Has Been Transfered")
    except:
        frappe.log_error(message=frappe.get_traceback(),title="Creation Of Asset Movement")
        frappe.msgprint("Error occured while creating the Asset Movement, Kindly check the logs")     



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def asset_list_filter(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT a.name,a.make,a.model,a.capacity
        FROM `tabAsset` a
        Left Join`tabItem` i on i.name = a.item_code 
        WHERE a.item_code = %(item)s AND a.model = %(model)s AND a.make = %(make)s AND a.capacity = %(capacity)s AND a.docstatus = 1 AND a.status = 'Submitted' AND i.name LIKE %(txt)s
        {mcond}
        """.format(**{
            'key': searchfield,
            'mcond':get_match_cond(doctype)
        }),
        {
        "item" :filters.get("item") ,
        "model":filters.get("model"),
        "make":filters.get("make"),
        "capacity":filters.get("capacity"),
        'txt': "%{}%".format(txt),
        '_txt': txt.replace("%", "")
        }
    )


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def asset_tag_filter(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT at.name,a.name
        FROM `tabAsset` a
        Left Join`tabAsset Tag` at on a.name = at.asset_id 
        WHERE a.name = %(asset_id)s AND at.name LIKE %(txt)s
        {mcond}
        """.format(**{
            'key': searchfield,
            'mcond':get_match_cond(doctype)
        }),
        {
        "asset_id" :filters.get("asset_id"),
        'txt': "%{}%".format(txt),
        '_txt': txt.replace("%", "")
        }
    )
