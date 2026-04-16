import frappe
from frappe.utils import today, add_to_date, date_diff

def enqueue_document_expiration_job():
    frappe.enqueue(
        "employee_document.background_jobs.expired_document.create_document_expiration",
        queue="long",
        timeout=600,
        job_name=f"create_document_expiration_{frappe.utils.nowdate()}",
    )

def enqueue_document_before_expiration_job():
    frappe.enqueue(
        "employee_document.background_jobs.expired_document.create_document_before_expiration",
        queue="long",
        timeout=600,
        job_name=f"create_document_before_expiration_{frappe.utils.nowdate()}",
    )

def create_document_before_expiration():
    employee_documents = frappe.get_all(
        "Employee Document",
        filters={
            "notify_before_expiry": 1,
            "expiry_date": [">", today()],
        },
        fields=[
            "name",
            "type",
            "issue_date",
            "expiry_date",
            "document_number",
            "parent",
            "parenttype",
            "notify_before_expiry",
            "notify_before_days",
        ],
    )

    if not employee_documents:
        return
    
    for employee_document in employee_documents:
        days_to_reminder = -int(employee_document.notify_before_days)
        reminder_date = add_to_date(employee_document.expiry_date, days=days_to_reminder)
        difference_of_date = date_diff(reminder_date, today())
        
        if (difference_of_date == 0):
            document_expiration_data = get_employee_document_expiration(employee_document)
            if employee_document.parenttype == "Employee":
                employee_doc = frappe.get_doc("Employee", employee_document.parent)
                if not employee_doc:
                    continue
                document_expiration_data.update({
                    "employee_cell_number": employee_doc.cell_number,
                    "employee_name": employee_doc.employee_name,
                    "employee_number": employee_doc.employee_number,
                    "notify_before_expiry": employee_document.notify_before_expiry,
                    "notify_before_days": employee_document.notify_before_days,
                })            
            
            document_expiration = frappe.get_doc(document_expiration_data).insert(ignore_permissions=True)

    frappe.db.commit()

def create_document_expiration():
    # get the all the Employee Document where the expiry_date is today (child table)
    employee_documents = frappe.get_all(
        "Employee Document",
        filters={"expiry_date": frappe.utils.nowdate()},
        fields=[
            "name",
            "type",
            "issue_date",
            "expiry_date",
            "document_number",
            "parent",
            "parenttype"
        ],
    )

    if not employee_documents:
        return

    for employee_document in employee_documents:
        document_expiration_data = get_employee_document_expiration(employee_document)
        if employee_document.parenttype == "Employee":
            employee_doc = frappe.get_doc("Employee", employee_document.parent)
            if not employee_doc:
                continue
            document_expiration_data.update({
                "employee_cell_number": employee_doc.cell_number,
                "employee_name": employee_doc.employee_name,
                "employee_number": employee_doc.employee_number,
            })
        
        document_expiration = frappe.get_doc(document_expiration_data).insert(ignore_permissions=True)

    frappe.db.commit()

def get_employee_document_expiration(employee_document):
    document_expiration_data = {
        "doctype": "Document Expiration",
        "document_typee": employee_document.type,
        "issue_date": employee_document.issue_date,
        "expiry_date": employee_document.expiry_date,
        "document_number": employee_document.document_number,
        "reference_doctype": employee_document.parenttype,
        "reference_name": employee_document.parent
    }

    return document_expiration_data