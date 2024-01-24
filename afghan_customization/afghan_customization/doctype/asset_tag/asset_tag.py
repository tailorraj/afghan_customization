# Copyright (c) 2023, Raaj Tailor and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class AssetTag(Document):
	# pass

	def validate(self):
		if self.asset_id:
			frappe.db.set_value('Asset',self.asset_id,'is_asset_tag_id','1')
			frappe.db.set_value('Asset',self.asset_id,'asset_tag_no',self.name)
			frappe.db.commit()

