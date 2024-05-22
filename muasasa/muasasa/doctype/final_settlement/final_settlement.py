# Copyright (c) 2023, smart and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils.data import date_diff


class FinalSettlement(Document):
    def validate(self):
        self.calc_settlement_totals()

    def calc_settlement_totals(self):
        earning = 0
        deduction = 0
        for entitlements in self.entitlements:
            earning += entitlements.amount
        self.total_entitlements = earning

        for deductions in self.deductions:
            deduction += deductions.amount
        self.total_deductions = deduction

        self.total_settlement = earning - deduction

    @frappe.whitelist()
    def calc_service_duration(self):
        diff_data = get_date_diff(self.last_day_of_work, self.date_of_joining)
        self.service_duration = diff_data

        diff_data_last_days = get_date_diff(self.last_day_of_work, self.actual_start_date)
        self.last_working_period = diff_data_last_days

        try:
            doc = frappe.get_doc("Salary Structure Assignment", {"docstatus": 1, "employee": self.employee})
            self.basic_salary = doc.base
            self.housing_allowance = doc.housing_allowance
            self.other_allowances = doc.other_allowances
            self.nature_of_work = doc.nature_of_work
            self.transportation_allowance = doc.transportation_allowance
            self.extra_work = doc.extra_work
        except frappe.DoesNotExistError:
            pass

        current_doc = self.as_dict()
        fields = [
            "basic_salary",
            "housing_allowance",
            "other_allowances",
            "nature_of_work",
            "transportation_allowance",
            "extra_work",
        ]
        total = 0
        for field in fields:
            total += current_doc[field]
        self.total_salary = total


def get_date_diff(first_date, second_date):
    days = date_diff(first_date, second_date)
    date = days_to_years_months_days(days)
    return "  سنه   {0}   شهر   {1}    يوم    {2}".format(date[0], date[1], date[2])


def days_to_years_months_days(days):
    # Define average days in a month and days in a year
    avg_days_per_month = 30.44  # Average days in a month
    days_per_year = 365.25  # Average days in a year, accounting for leap years

    # Calculate years, months, and remaining days
    years, remainder = divmod(days, days_per_year)
    months, remaining_days = divmod(remainder, avg_days_per_month)

    # Round months to whole number and adjust if it exceeds 12
    months = round(months)
    if months == 12:
        years += 1
        months = 0

    return int(years), int(months), int(remaining_days)
