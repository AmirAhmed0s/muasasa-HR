// Copyright (c) 2023, smart and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
    validate:async function(frm){
      
      
        if (frm.doc.items.length > 1) {
      for(let i in frm.doc.items){
    
        if (!frm.doc.items[i].cost_center ){
            
            
         await  frappe.call({
            method:"muasasa.controller.sales_invoice.get_item_cost_center",
            args:{"item_code":frm.doc.items[i].item_code,
            "name":frm.doc.items[i].name,
            "company":frm.doc.company
        },
            callback:async function(r){
                cur_frm.get_field("items").grid.grid_rows[i].doc.cost_center =r.message[0]
                cur_frm.get_field("items").grid.grid_rows[i].doc.income_account =r.message[1]
              
            cur_frm.get_field("items").grid.grid_rows[i].refresh_field("cost_center");
            cur_frm.get_field("items").grid.grid_rows[i].refresh_field("income_account");
             
                
            }
        }) }
    } }}
})
