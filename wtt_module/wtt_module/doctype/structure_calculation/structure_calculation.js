// Copyright (c) 2022, wtt_module and contributors
// For license information, please see license.txt
// #gokul
frappe.ui.form.on('Structure Calculation', {
	setup:function(frm){
		frm.set_query("employee", function() {
			return {
				filters: [
					["Employee","status","=", 'Active']
				]
			}

		});
	},
	// gross_salary:function(frm){
	// 	var check=(frm.doc.gross_salary/100)*25;
	// 	if(frm.doc.basic_salary>=check){
	// 		var hra=(frm.doc.basic_salary/100)*40;
	// 		var others=frm.doc.gross_salary-(frm.doc.basic_salary+hra);
	// 		frm.set_value("hra",hra);
	// 		if(others<=0){
	// 			frm.set_value("others",0);
	// 		}
	// 		else{
	// 		frm.set_value("others",others);
	// 		}
	// 	}
	// 	else if(check>frm.doc.basic_salary){
	// 		frm.set_value("basic_salary",check);
	// 		var hra=(check/100)*40;
	// 		var others=frm.doc.gross_salary-(check+hra);
	// 		frm.set_value("hra",hra);
	// 		if(others<=0){
	// 			frm.set_value("others",0);
	// 		}
	// 		else{
	// 		frm.set_value("others",others);
	// 		}
	// 	}
	// },
	old_ctc:function(frm){
		frm.set_value("old_ctc_as_per_annum",frm.doc.old_ctc*12);
		frm.refresh_field("old_ctc_as_per_annum");
	},
	ctcperannum:function(frm){
		frappe.db.get_value('Employee', frm.doc.employee, ['esi', 'pf'])
	    .then(r => {
	        if(r.message.esi=="No" && r.message.pf=="No")
			{
				var anctc=frm.doc.ctcperannum;
				if(frm.doc.branch=='WORKSHOP')
				{
					anctc=anctc-5400;
					frm.set_value("tshirt",2000);
					frm.refresh_field("tshirt");
					frm.set_value("shoe",400);
					frm.refresh_field("shoe");
					frm.set_value("insurance",3000);
					frm.refresh_field("insurance");
				}
				 
				else
				{
					anctc=anctc-5000;
					frm.set_value("tshirt",2000);
					frm.refresh_field("tshirt");
					frm.set_value("shoe",0);
					frm.refresh_field("shoe");
					frm.set_value("insurance",3000);
					frm.refresh_field("insurance");
				}
				frm.set_value("ctc",anctc/12);
				frm.refresh_field("ctc");
			}
			else
			{
				var anctc=frm.doc.ctcperannum;
				if(frm.doc.branch=='WORKSHOP')
				{
					if(r.message.esi=="No")
					{
					anctc=anctc-5400;
					frm.set_value("tshirt",2000);
					frm.refresh_field("tshirt");
					frm.set_value("shoe",400);
					frm.refresh_field("shoe");
					frm.set_value("insurance",3000);
					frm.refresh_field("insurance");
					}

					if(r.message.esi=="Yes")
					{
					anctc=anctc-2700;
					frm.set_value("tshirt",2000);
					frm.refresh_field("tshirt");
					frm.set_value("shoe",400);
					frm.refresh_field("shoe");
					frm.set_value("insurance",300);
					frm.refresh_field("insurance");
					}
					frm.set_value('ctc',anctc/12);
					frm.refresh_field("ctc");
				}
				else
				{						
					if(r.message.esi=="No")
					{
						anctc=anctc-5000;
						frm.set_value("tshirt",2000);
						frm.refresh_field("tshirt");
						frm.set_value("shoe",0);
						frm.refresh_field("shoe");
						frm.set_value("insurance",3000);
						frm.refresh_field("insurance");
					}
					if(r.message.esi=="Yes")
					{
						anctc=anctc-2300;
						frm.set_value("tshirt",2000);
						frm.refresh_field("tshirt");
						frm.set_value("shoe",0);
						frm.refresh_field("shoe");
						frm.set_value("insurance",300);
						frm.refresh_field("insurance");
					}						
					frm.set_value('ctc',anctc/12);
					frm.refresh_field("ctc");
				}
			}
	    })
	},
	ctc:function(frm){
		frappe.db.get_value('Employee', frm.doc.employee, ['esi', 'pf'])
	    .then(r => {
	    	if(r.message.esi=="No" && r.message.pf=="No"){
				var ctc=frm.doc.ctc;
				var bs=ctc*0.2420487;
				var hra=bs*0.4;
				var od=ctc*0.629326621;
				var finalbs=bs;
				var finalhra=hra;
				var finalod=od;
				var gross=finalbs+finalhra+finalod;
				var bonus=finalbs*0.0833;
				var gra=finalbs*0.0481;
				var sumof=bonus+gra;
				var bogra=sumof;
				frm.set_value("basic_salary",finalbs);
				frm.refresh_field("basic_salary");
				frm.set_value("hra",finalhra);
				frm.refresh_field("hra");
				frm.set_value("others",finalod);
				frm.refresh_field("others");
				frm.set_value("gross_salary",gross);
				frm.refresh_field("gross_salary");
				frm.set_value("bonus",bonus);
				frm.refresh_field("bonus");
				frm.set_value('gra',gra);
				frm.refresh_field("gra");
				frm.set_value('take_home',gross);
				frm.refresh_field("take_home");
				frm.set_value('total',bogra);
				frm.refresh_field("total");
			}
			else{
				var ctc=frm.doc.ctc;
				var bs=frm.doc.ctc*0.2420487;
				var hra=bs*0.4;
				var od=frm.doc.ctc*0.629326621;
				var finalbs=bs;
				var finalhra=hra;
				var finalod=od;
				var gross=finalbs+finalhra+finalod;
				var pfto=finalbs+finalod;
				var pfcal = 0;
				var esical = 0;
				var esical2=0;
				var pfcal2=0;
				
				if(r.message.pf=="Yes" && r.message.esi=="Yes")
				{
					if(pfto>15000)
					{
					    pfcal=15000*0.13;
					    pfcal2=15000*0.12;
					}
					else
					{
					    pfcal=pfto*0.13;
					    pfcal2=pfto*0.12;
					}
					if(gross>=21000)
					{
					    esical=0;
					    esical2=0;
					}
					else
					{
					    esical=gross*0.0325;
					    esical2=gross*0.0075;
					}
				}
				else if(r.message.pf=="Yes")
				{
					if(pfto>15000)
					{
					    pfcal=15000*0.13;
					    pfcal2=15000*0.12;
					}
					else
					{
					    pfcal=pfto*0.13;
					    pfcal2=pfto*0.12;
					}
				}
				
				else if(r.message.esi=="Yes")
				{
					if(gross>=21000)
					{
					    esical=0;
					    esical2=0;
					}
					else
					{
					    esical=gross*0.0325;
					    esical2=gross*0.0075;
					}
				}
				var bonus=finalbs*0.0833;
				var gra=finalbs*0.0481;
				var sumof=bonus+gra+esical+pfcal;
				var finalcal=gross+sumof;
				if(finalcal==ctc)
				{
				    frm.set_value("basic_salary",finalbs);
				    frm.refresh_field("basic_salary");
					frm.set_value("hra",finalhra);
					frm.refresh_field("hra");
					frm.set_value("others",finalod);
					frm.refresh_field("others");
					frm.set_value("gross_salary",gross);
					frm.refresh_field("gross_salary");
					frm.set_value("take_home",gross-(pfcal2+esical2));
					frm.refresh_field("take_home");
					frm.set_value("esi",esical)
					frm.refresh_field("esi");
					frm.set_value("pf",pfcal)
					frm.refresh_field("pf");
					frm.set_value("esi2",esical2)
					frm.refresh_field("esi2");
					frm.set_value("pf2",pfcal2)
					frm.refresh_field("pf2");
					frm.set_value("bonus",bonus);
					frm.refresh_field("bonus");
					frm.set_value('gra',gra)
					frm.refresh_field("gra");
					frm.set_value('total',sumof)
					frm.refresh_field("total");
				}
			else
			{
			    var diff=finalcal-ctc;
			    var i=0;
			    while(diff!=0)
			    {
			    var newbasic=finalbs-((finalbs/ctc)*diff);
			    var newhra=finalhra-((finalhra/ctc)*diff);
			    var newod=finalod-((finalod/ctc)*diff);
			    var newgross=newbasic+newhra+newod;
			    var newpfto=newbasic+newod;
			    var newpfcal=0;
			    var newesical=0;
			    var newpfcal2=0;
			    var newesical2=0;
			    
			    if(r.message.pf=="Yes" && r.message.pf=="Yes")
				{
					if(newpfto>15000)
				    {
				        newpfcal=15000*0.13;
				        newpfcal2=15000*0.12;
				    }
				    else
				    {
				        newpfcal=newpfto*0.13;
				        newpfcal2=newpfto*0.12;
				    }
				    if(newgross>=21000)
				    {
				        newesical=0;
				        newesical2=0;
				    }
				    else
				    {
				        newesical=newgross*0.0325;
				        newesical2=newgross*0.0075;
				    }
				}
				else if(r.message.pf=="Yes")
				{
					if(newpfto>15000)
				    {
				        newpfcal=15000*0.13;
				        newpfcal2=15000*0.12;
				    }
				    else
				    {
				        newpfcal=newpfto*0.13;
				        newpfcal2=newpfto*0.12;
				    }
				}
			    

			    else if(r.message.esi=="Yes")
				{
					if(newgross>=21000)
				    {
				        newesical=0;
				        newesical2=0;
				    }
				    else
				    {
				        newesical=newgross*0.0325;
				        newesical2=newgross*0.0075;
				    }
				}
			    var newbonus=newbasic*0.0833;
			    var newgra=newbasic*0.0481;
			    var newsumof=newbonus+newgra+newpfcal+newesical;
			    var newfinalcal=newgross+newsumof;
			    if(newfinalcal==ctc)
			    {
			    var diff=0;
			    }
			    else
			    {
			     finalbs=newbasic;
			     finalhra=newhra;
			     finalod=newod;
			     diff=newfinalcal-ctc;
			    }
			    i++;
			    if(i>100 && diff<0.000001 && diff>=-0.000001){
			    	console.log(diff)
			    	break;
			    }
			    }
			    frm.set_value("basic_salary",newbasic);
			    frm.refresh_field("basic_salary");
				frm.set_value("hra",newhra);
				frm.refresh_field("hra");
				frm.set_value("others",newod);
				frm.refresh_field("others");
				frm.set_value("gross_salary",newgross);
				frm.refresh_field("gross_salary");
				frm.set_value("take_home",newgross-(newpfcal2+newesical2))
				frm.refresh_field("take_home");
				frm.set_value("esi",newesical)
				frm.refresh_field("esi");
				frm.set_value("pf",newpfcal)
				frm.refresh_field("pf");
				frm.set_value("esi2",newesical2)
				frm.refresh_field("esi2");
				frm.set_value("pf2",newpfcal2)
				frm.refresh_field("pf2");
				frm.set_value("bonus",newbonus);
				frm.refresh_field("bonus");
				frm.set_value('gra',newgra)
				frm.refresh_field("gra");
				frm.set_value('total',newsumof)
				frm.refresh_field("total");
			}
			}
	    })
		

	},
	employee:function(frm){
		frappe.call({
			method:"wtt_module.wtt_module.doctype.structure_calculation.structure_calculation.get_bs",
			args:{
				"employee":frm.doc.employee
			},
			callback:function(r){
				frm.set_value("qualification",r.message[0]);
				frm.refresh_field("qualification");
			}
		})
	}
});
