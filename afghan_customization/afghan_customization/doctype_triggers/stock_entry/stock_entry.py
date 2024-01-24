import frappe

@frappe.whitelist()
def get_msisdn_value(serials):
    serials = serials.split("\n")
    str_serial = ""
    for i in serials:
        if str_serial == "":
            str_serial = "'" + i + "'"
        else:
            str_serial = str_serial + "," + "'" + i + "'"

    # ser_data = frappe.db.sql("select sn.name as serial_name,sn.msisdn as msisdn  from `tabSerial No` sn inner join `tabItem` im on im.name = sn.item_code where sn.name in (%s) and sn.status = 'Active' group by sn.item_code"%(str_serial), as_dict = True)
    ser_data = frappe.db.sql("select group_concat(sn.name separator '\n') as serial_name,group_concat(sn.msisdn separator '\n') as msisdn  from `tabSerial No` sn inner join `tabItem` im on im.name = sn.item_code where sn.name in (%s) and sn.status = 'Active' group by sn.item_code"%(str_serial), as_dict = True)
    return ser_data