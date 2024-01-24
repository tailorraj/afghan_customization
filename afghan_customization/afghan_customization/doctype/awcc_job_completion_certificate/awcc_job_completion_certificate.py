# Copyright (c) 2023, Raaj Tailor and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class AWCCJobCompletionCertificate(Document):
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
				'date':self['job_completion_date'],
				'allocated_to':self['work_inspected_by'],
				'description':'ToDo is Created of User: <b>{0}</b> For Job Completion Certification Of This Document <b>{1}</b>'.format(self['work_inspected_by'],self['name']),
				'reference_type':self['doctype'],
				'reference_name':self['name'],
				'assigned_by':self['hod_approval']
			})
			todo_doc.insert(ignore_permissions =1)
			todo = todo_doc.name
			frappe.msgprint("Your Todo Document Name Is: <b>{0}</b> created".format(todo))
		else:
			frappe.msgprint("ToDo Is Already Created For This Asset Request Form!")

	except Exception as e:
		frappe.log_error(message=frappe.get_traceback(),title="Creation Of ToDo From Asset Request Form: ")
		frappe.msgprint("Error occured while creating the ToDo, Kindly check the logs")
