import frappe
from frappe.utils import today
from frappe.utils.data import date_diff

def validate_vehicle_date():
        vehicles=frappe.db.get_list('Vehicle',fields=["name",'end_date', 'periodic_examination_end_date'])
        for vehicle in vehicles:
            vehicle_doc=frappe.get_doc('Vehicle',vehicle["name"])
            if  not vehicle["end_date" ] == None:
               
                if str(vehicle["end_date"]) <= today():
                    vehicle_doc.insurance_status="Ended"
                    vehicle_doc.save()
                elif date_diff(str(vehicle["end_date"]),today())<= 30:
                    vehicle_doc.insurance_status="Almost Ended"
                    vehicle_doc.save()
                else:
                    vehicle_doc.insurance_status="Valid"
                    vehicle_doc.save()
            else: 
                vehicle_doc.insurance_status=""
                vehicle_doc.save()           

            if  not vehicle["periodic_examination_end_date"]== None:
                
               
                    if str(vehicle["periodic_examination_end_date"]) <= today():
                        vehicle_doc.examination_status="Ended"
                        vehicle_doc.save()

                    elif date_diff(str(vehicle["periodic_examination_end_date"]),today())<= 30:
                        vehicle_doc.examination_status="Almost Ended"
                        vehicle_doc.save()

                    else:
                        vehicle_doc.examination_status="Valid"
                        vehicle_doc.save()    
            else:
                vehicle_doc.examination_status=""
                vehicle_doc.save()  
