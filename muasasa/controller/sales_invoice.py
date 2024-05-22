import frappe

from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults


# def validate_item_cost_center(self, event):
#     get_item_cost_center(self)


@frappe.whitelist()
def get_item_cost_center(item_code, name, company):
    # for item in self.items:
    # item
    args = {"item_code": item_code, "company": company}
    selling_cost_center, income_account = frappe.db.get_value(
        "Item Default",
        fieldname=["selling_cost_center", "income_account"],
        filters={"parent": item_code, "parenttype": "Item", "company": company},
    )

    return selling_cost_center, income_account
    # if cost_center:
    #     item.cost_center = cost_center
    #     continue
    #     # item group
    # item_group = frappe.db.get_value("Item", {"item_code": item.item_code}, ["item_group"])
    # cost_center = frappe.db.get_value(
    #     "Item Default",
    #     fieldname=["buying_cost_center"],
    #     filters={"parent": item_group, "parenttype": "Item Group"},
    # )
    # if cost_center:
    #     item.cost_center = cost_center
    #     continue
    # # company

    # cost_center = frappe.get_cached_value("Company", self.company, "cost_center")

    # if cost_center:
    #     item.cost_center = cost_center
    #     continue
