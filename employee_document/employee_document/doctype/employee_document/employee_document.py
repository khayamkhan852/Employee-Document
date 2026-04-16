# Copyright (c) 2026, khayam khan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EmployeeDocument(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		document_copy: DF.AttachImage | None
		document_number: DF.Data
		expiry_date: DF.Date
		issue_date: DF.Date
		notify_before_days: DF.Int
		notify_before_expiry: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		type: DF.Link
	# end: auto-generated types

	pass
