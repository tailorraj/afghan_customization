import frappe
from frappe.desk.reportview import get_filters_cond, get_match_cond
from frappe.model.mapper import get_mapped_doc

def validate(self,method):
    for item in self.items:
        if item.make:
            make_model_value=frappe.db.get_value('Make Model Capacity',{'make':item.make,'parent':item.item_code},['model','capacity'],as_dict=1)
            if make_model_value:
                item.model = make_model_value.model
                item.capacity = make_model_value.capacity


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def filter_make(doctype, txt, searchfield, start, page_len, filters):
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


@frappe.whitelist()
def create_jcc(source_name, target_doc=None):
    
    doclist = get_mapped_doc(
        "Purchase Order",
        source_name, 
        {
            "Purchase Order": {
                "doctype": "AWCC Job Completion Certificate",
                "field_map": {
                    "po_number": "name",
                    "supplier_name": "supplier",
                    "supplier_address":"supplier_address",
                    "address_display" : "supplier_address_display"  
                },
            },
            "Purchase Order Item": {
                "doctype": "AWCC Job Completion Certificate Item",
                "field_map": {
                    "item_table":"items" 
                },
            },
        },
        target_doc
    )
    
    return doclist
