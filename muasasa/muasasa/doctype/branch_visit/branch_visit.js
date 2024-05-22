// Copyright (c) 2023, smart and contributors
// For license information, please see license.txt

frappe.ui.form.on('Branch Visit', {
	customer: function (frm) {
        var df = frappe.meta.get_docfield("Branch Visit", "customer_branch",frm.doc.name);
        
        if (frm.doc.customer) {
            frappe.call({
                method: "yakhdhoor.yakhdhoor.api.get_customer_branch",
                args: {
                    customer: frm.doc.customer
                },
                callback: function (r) {
                    if (r.message) {
                        var options = r.message.map(function (element) {
                            return element.customer_branch;
                        });
                        df.options = options;
                    } else {
                        df.options = [];
                    }
                    frm.refresh_field('customer_branch');
                }
            });
        } else {
            df.options = [];
            frm.refresh_field('customer_branch');
        }
    },
	onload:function(frm){
		console.log(frm)
		if(frm.is_new()){
		frm.set_value("user",frappe.session.user);}
	},
	customer_branch: function (frm) {
       frm.events.validate_distance(frm)
    },
    validate_distance: function (frm){
		var xc= frappe.call({
			method:"frappe.client.get_value",
			args: {
			   doctype: "Customer Branch",
			   fieldname: ["longitude","latitude"],
			   filters: {
						   name:["=",cur_frm.doc.customer_branch]
				}
		   },
		   async: false,
		  callback: function (data) {
		   
			   if(typeof(data.message) != 'undefined' )
			   {
				   if(data.message.longitude){
					   //cur_frm.refresh();
					   cur_frm.set_value("longitude",data.message.longitude);
					   cur_frm.set_value("latitude",data.message.latitude);
					   refresh_field("longitude");
					   refresh_field("latitude");

				   }
   
			   }
		   }
   });
   var x=0;
   var xc= frappe.call({
			method:"frappe.client.get_value",
			args: {
			   doctype: "Map Settings",
			   fieldname: ["map_distance"]
		   },
		   async: false,
		  callback: function (data) {
			   
			   if(typeof(data.message) != 'undefined' )
			   {
				   if(data.message.map_distance){
					   x= data.message.map_distance;
				   }
   
			   }
		   }
   });
   
   console.log(x)
   var dist = getDistance(cur_frm.doc.latitude, cur_frm.doc.current_latitude,cur_frm.doc.longitude, cur_frm.doc.current_longitude);
   // && frappe.user_roles.includes("Map")
   console.log(dist)
   if(dist > x )
   {
	   console.log(dist.toString());
	   frappe.msgprint('لا يمكنك ادخال فاتورة لهذا العميل لعدم تواجدك في محله');
	   frm.disable_save();

   }
    },
    customer: function (frm) {
		frm.events.set_filter(frm)
        //debugger;
       
		// console.log(df.options)
        var xc= frappe.call({
                 method:"frappe.client.get_value",
                 args: {
    				doctype: "Customer",
    				fieldname: ["longitude","latitude"],
    				filters: {
    	                		name:["=",cur_frm.doc.customer]
                     }
                },
                async: false,
               callback: function (data) {
    				//debugger;
    				if(typeof(data.message) != 'undefined' )
                    {
    					if(data.message.longitude){
    						//cur_frm.refresh();
    						cur_frm.set_value("longitude",data.message.longitude);
    						cur_frm.set_value("latitude",data.message.latitude);
    
    					}
    	
    				}
    			}
    	});
    	//debugger;
   
    },
  
  
    refresh:function(frm) {
		if(frm.is_new()){
		frm.set_value("user",frappe.session.user)
	        if(navigator.geolocation){
	            navigator.geolocation.getCurrentPosition(onPositionRecieved,locationNotRecieved,{ enableHighAccuracy: true});
	        }

	    function onPositionRecieved(position){
	      
	        //debugger;
	        var longitude= position.coords.longitude;
			console.log(longitude)
	        var latitude= position.coords.latitude;
	        cur_frm.set_value("current_longitude",longitude);
	        cur_frm.set_value("current_latitude",latitude);
	        refresh_field("current_longitude");
	        refresh_field("current_latitude");
	        console.log(longitude);
	        console.log(latitude);

	    }
	    
	    function locationNotRecieved(positionError){
	        console.log(positionError);
	    }}

    },

	set_filter: async function(frm){
		let branch_list= []
		await frappe.db.get_list('Customer Branch List', {
		   
		   filters: {
			   parent: frm.doc.customer,
			   parenttype:"Customer"
		   },
		   fields: ['customer_branch']
	   }).then(records => {
		   for(let i in records ){
			   branch_list.push(records[i]["customer_branch"])
		   }
		   
		   
	   })
		
		 frm.set_query("customer_branch", function () {
		
			
			return {
			  filters: [
				["name", "in",branch_list]
				
			]
			};
		  });
	   
	},
	
     
});
var rad = function(x) {
	return x * Math.PI / 180;
  };
  
  var getDistance = function(lat1,lat2,lng1,lng2) {
	var R = 6378137; // Earth’s mean radius in meter
	var dLat = rad(lat2 - lat1);
	var dLong = rad(lng2 - lng1);
	var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
	  Math.cos(rad(lat1)) * Math.cos(rad(lat2)) *
	  Math.sin(dLong / 2) * Math.sin(dLong / 2);
	var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
	var d = R * c;
	return d; // returns the distance in meter
  };

