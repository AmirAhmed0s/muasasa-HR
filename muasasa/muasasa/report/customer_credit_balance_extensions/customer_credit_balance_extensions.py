# Copyright (c) 2023, smart and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt

from erpnext.selling.doctype.customer.customer import get_credit_limit, get_customer_outstanding


def execute(filters=None):
    if not filters:
        filters = {}
    # Check if customer id is according to naming series or customer name
    customer_naming_type = frappe.db.get_value("Selling Settings", None, "cust_master_name")
    columns = get_columns(customer_naming_type)

    data = []

    customer_list = get_details(filters)

    for d in customer_list:
        row = []

        outstanding_amt = get_customer_outstanding(
            d.name, filters.get("company"), ignore_outstanding_sales_order=d.bypass_credit_limit_check
        )

        credit_limit = get_credit_limit(d.name, filters.get("company"))

        bal = flt(credit_limit) - flt(outstanding_amt)

        if customer_naming_type == "Naming Series":
            row = [
                d.name,
                d.customer_name,
                credit_limit,
                outstanding_amt,
                bal,
                d.bypass_credit_limit_check,
                d.is_frozen,
                d.disabled,
            ]
        else:
            row = [
                d.name,
                credit_limit,
                outstanding_amt,
                bal,
                d.bypass_credit_limit_check,
                d.is_frozen,
                d.disabled,
            ]

        if credit_limit:
            data.append(row)

    return columns, data


def get_columns(customer_naming_type):
    columns = [
        _("Customer") + ":Link/Customer:120",
        _("Credit Limit") + ":Currency:120",
        _("Outstanding Amt") + ":Currency:100",
        _("Credit Balance") + ":Currency:120",
        _("Bypass credit check at Sales Order") + ":Check:80",
        _("Is Frozen") + ":Check:80",
        _("Disabled") + ":Check:80",
    ]

    if customer_naming_type == "Naming Series":
        columns.insert(1, _("Customer Name") + ":Data:120")

    return columns


def get_details(filters):
    sql_query = """SELECT
                        c.name, c.customer_name,
                        ccl.bypass_credit_limit_check,
                        c.is_frozen, c.disabled
                    FROM `tabCustomer` c
                    LEFT JOIN `tabCustomer Credit Limit` ccl ON c.name = ccl.parent
                    WHERE ccl.company = %s"""

    # Retrieve the territory list from filters or set it to an empty list if None
    territory_list = filters.get("territory") or []

    # Parameters for the SQL query
    params = [filters.get("company")]

    # If territory_list is not empty, add a condition for territory
    if territory_list:
        # Create placeholders for the IN clause based on the length of territory_list
        placeholders = ", ".join(["%s" for _ in territory_list])
        sql_query += f" AND c.territory IN ({placeholders})"
        params.extend(territory_list)  # Extend the params list with territory values

    # Handle customer_group and payment_terms in a similar way
    for filter_name in ["customer_group", "payment_terms"]:
        filter_value = filters.get(filter_name)
        if filter_value:
            sql_query += f" AND c.{filter_name} = %s"
            params.append(filter_value)

    return frappe.db.sql(sql_query, tuple(params), as_dict=1)
