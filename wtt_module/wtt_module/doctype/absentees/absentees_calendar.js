frappe.views.calendar["Absentees"] = {
    field_map: {
        "start": "date",
        "end": "date",
        "id": "name",
        "title": "title",
        "description": "status",
        "color":"color",
        "tooltip":"reason"
    },
  //   gantt: false,
  //   options: {
  //       header: {
  //           left: 'prev, title, next',
  //           center: 'today',
  //           right: 'listOneDay'
  //       },
  //       views: {
  //           listOneDay: {
  //               type: 'list',
  //               titleFormat: 'ddd, DD MMMM YYYY',
  //               duration: { days: 1 },
  //               buttonText: color_map,
  //               noEventsMessage: "No Records for this date"
  //           }
  //       },
  //       defaultView: 'listOneDay',
  //       allDaySlot: true,
  //       slotEventOverlap: false,
  //       editable: true,
		// resources: function(callback) {
  //           return frappe.call({
  //               method: "wtt_module.wtt_module.doctype.absentees.absentees.get_calendar",
  //               type: "GET",
  //               callback: function(r) {
  //                   var resources = r.message || [];
  //                   callback(resources);
  //               }
  //           })
  //       },
  //   },
    color_map: {
        "al": "green",
        "od": "purple",
        "os": "blue",
        "ul": "red",
        "le": "yellow",
        "background": "cyan"
    },
    get_css_class: function(data) {
        if (data.rendering == "background") {
            return "background";
        }
        if (data.status == "Approval Leave") {
            return "al";
        } else if (data.status == "Uninformed Leave") {
            return "ul";
        } else if (data.status == "Late Entry") {
            return "le";
        } else if (data.status == "On duty") {
            return "od";
        } else if (data.status == "On site") {
            return "os";
        } 
    },
    get_events_method: "wtt_module.wtt_module.doctype.absentees.absentees.get_calendar",
}