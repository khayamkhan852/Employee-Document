# Copyright (c) 2026, khayam khan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class DocumentExpiration(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		document_number: DF.Data
		document_typee: DF.Link
		employee_cell_number: DF.Data | None
		employee_name: DF.Data | None
		employee_number: DF.Data | None
		expiry_date: DF.Date
		issue_date: DF.Date
		notify_before_days: DF.Int
		notify_before_expiry: DF.Check
		reference_doctype: DF.Link | None
		reference_name: DF.DynamicLink | None
	# end: auto-generated types

	pass
