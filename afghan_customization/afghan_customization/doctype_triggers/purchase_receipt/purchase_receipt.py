import frappe


def on_submit(self,method):

    create_grn(self)
    for item in self.items:
        if item.qa_check == 0:
            frappe.throw("Quality Check For This User:{0} is Remaining".format(item.assigned_representative))

        frappe.db.set_value('Asset', {'item_code':item.item_code,'purchase_receipt':self.name}, {
            'model': item.model,
            'make': item.make,
            'capacity':item.capacity
        })
        frappe.db.commit()      


def create_grn(self):
    try:
        grn_doc = frappe.get_doc({
            'doctype':'Goods Receipt Note',
            'date':self.posting_date,
            'supplier_name':self.supplier,
            'supplier_address':self.supplier_address,
            'supplier_address_display':self.address_display,
            'warehouse':self.set_warehouse,
        })

        for d in self.items:
            grn_item_doc = {
                'doctype':'Goods Receipt Note Item',
                'item':d.item_code,
                'description':d.description,
                'arrival_date':self.posting_date,
                'qty_received':d.qty,
                'unit_cost':d.rate,
                'extended_cost':d.amount,
                'uom':d.uom,
                'reference':self.name,
                'po_number':d.purchase_order
            }
            grn_doc.append('items',grn_item_doc)

        grn = grn_doc.insert(ignore_permissions = 1)
        frappe.db.set_value('Purchase Receipt',self.name,'grn_receipt',grn.name) 
        frappe.msgprint("Goods Receipt Note {0} Created".format(grn.name))   
    except:
        frappe.log_error(message = frappe.get_traceback(),title="Create Goods Receipt Note from Purchase Receipt")
        frappe.throw("Error occured while creating Goods Receipt Note, Kindly check the logs")

@frappe.whitelist()
def create_todo(item_name,qty,user,date,assign_user,name):
    try:
        new_doc = frappe.new_doc("ToDo")
        new_doc.allocated_to = user
        new_doc.date = date
        new_doc.priority = "High"
        new_doc.description = "Quality Check for Item Name: <b>{0}</b>, Qty:<b>{1}</b>".format(item_name,qty)
        new_doc.reference_type = "Purchase Receipt"
        new_doc.reference_name = name
        new_doc.assigned_by = assign_user

        new_doc.insert(ignore_permissions = True)
        todo_doc = new_doc.save()
        return todo_doc.name
    except:
        frappe.log_error(message = frappe.get_traceback(),title="Create ToDo from Purchase Receipt Item")
        frappe.msgprint("Error occured while creating ToDo, Kindly check the logs")