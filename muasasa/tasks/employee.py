import frappe
from frappe.utils import today
from frappe.utils.data import date_diff


def validat_employee_expire_date():
    employees = frappe.db.get_list(
        "Employee", filters={"status": "Active"}, fields=["name", "contract_end_date", "release_end_date"]
    )

    for employee in employees:
        employee_doc = frappe.get_doc("Employee", employee["name"])

        if not employee["contract_end_date"] == None:
            if str(employee["contract_end_date"]) <= today():
                employee_doc.contract_status = "Ended"
                employee_doc.save()

            elif date_diff(employee["contract_end_date"], today()) <= 90:
                employee_doc.contract_status = "Almost Ended"
                employee_doc.save()

            else:
                employee_doc.contract_status = "Valid"
                employee_doc.save()
        else:
            employee_doc.contract_status = ""
            employee_doc.save()

        if not employee["release_end_date"] == None:
            if str(employee["release_end_date"]) <= today():
                employee_doc.id_status = "Ended"
                employee_doc.save()

            elif date_diff(employee["release_end_date"], today()) <= 30:
                employee_doc.id_status = "Almost Ended"
                employee_doc.save()

            else:
                employee_doc.id_status = "Valid"
                employee_doc.save()
        else:
            employee_doc.id_status = ""
            employee_doc.save()
