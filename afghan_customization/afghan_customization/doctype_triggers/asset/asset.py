import frappe


def on_submit(self,method):
    if self.is_asset_tag_id == 0 and self.asset_tag_no == None:
        frappe.throw("Can't Submit This Document Without Asset Tag No And Asset Tag Id") 