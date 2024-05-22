// Copyright (c) 2023, smart and contributors
// For license information, please see license.txt

frappe.ui.form.on('Clearance Form', {
	employee:function(frm){
		
		frappe.db.get_doc('Department managers', 'Department managers')
			.then(doc => {
				
					
				frm.set_value('finance_name', doc.finance_manager)
				frm.set_value('hr_name', doc.hr_manager)
				frm.set_value('movement_department_name', doc.movement_manager)
				frm.set_value('top_management_name', doc.top_manager)
				frm.set_value('name_itdep', doc.it_manager)
				frm.set_value('customer_accountant_name', doc.customer_accountant)
				frm.set_value('warehouses_name', doc.warehouses_manager)
				
				
			})
		}
});
