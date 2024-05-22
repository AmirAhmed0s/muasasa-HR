# Copyright (c) 2023, smart and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class ClearanceForm(Document):
    def before_submit(self):
        self.validate_all_department_approved()

    def validate_all_department_approved(self):
        current_doc = self.as_dict()
        fields = [
            "clearance_employee_mangement_section",
            "warehouses_clearance",
            "customer_accountant_clearance",
            "movement_department_clearance",
            "clearance_itdep",
            "clearance_finance",
            "hr_clearance",
            "operation_manager_clearance",
            "top_management_clearance",
        ]
        approval_scan = []
        for field in fields:
            if current_doc[field] == "No":
                approval_scan.append("NO")

        if len(approval_scan) > 0:
            frappe.throw(_("All department must be approved "))
