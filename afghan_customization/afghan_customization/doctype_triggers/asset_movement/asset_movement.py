import frappe

def on_submit(self,method):
    for item in self.assets:
        frappe.db.set_value('Asset',item.asset,'location',item.target_location)
        frappe.db.commit()