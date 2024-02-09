frappe.listview_settings["Payment Module"] = {
    get_indicator: function (doc) {
      if (["Transferred"].includes(doc.payment_status)) {
        return [__(doc.payment_status), "green", "payment_status,=," + doc.payment_status];
      } else if (["Not Transferred"].includes(doc.payment_status)) {
        return [__(doc.payment_status), "red", "payment_status,=," + doc.payment_status];
      } else if (doc.payment_status == "In Progress") {
        return [__(doc.payment_status), "orange", "payment_status,=," + doc.payment_status];
      }
    }
}