# Copyright (c) 2023, smart and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today



class BranchVisit(Document):
    def before_submit(self):
        self.submit_date = today()



