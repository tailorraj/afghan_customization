import frappe

@frappe.whitelist()
def fetch_make_model_data(item_name):
    make_model_data = frappe.db.sql(""" select * from`tabMake Model Part` where item = %(item)s
    """,{'item':item_name},as_dict=1)
    return make_model_data