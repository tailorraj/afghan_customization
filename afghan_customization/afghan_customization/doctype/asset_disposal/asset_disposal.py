# Copyright (c) 2023, Raaj Tailor and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class AssetDisposal(Document):
	pass


@frappe.whitelist()
def create_todo(self):
	self = json.loads(self)
	try:
		if not frappe.db.exists('ToDo',{'reference_name':self['name']}):
			todo_doc = frappe.get_doc({
				'doctype':'ToDo',
				'status':'Open',
				'priority':'High',
				'date':frappe.utils.today(),
				'allocated_to':self['manager'],
				'description':'Please Check Asset Disposal Form: <b>{0}</b>'.format(self['name']),
				'reference_type':self['doctype'],
				'reference_name':self['name'],
				'assigned_by':self['created_by']
			})
			todo_doc.insert(ignore_permissions =1)
			todo = todo_doc.name
			frappe.msgprint("Your Todo Document Name Is: <b>{0}</b> created".format(todo))
		else:
			frappe.msgprint("ToDo Is Already Created For This Asset Disposal!")

	except Exception as e:
		frappe.log_error(message=frappe.get_traceback(),title="Creation Of ToDo From Asset Disposal: ")
		frappe.msgprint("Error occured while creating the ToDo, Kindly check the logs")	
