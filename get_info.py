import meraki
import os
import csv

api_key = os.getenv("MERAKI_KEY")
org_id = os.getenv("ORG_ID")
ptype = ['appliance']
columns = ['name', 'address', 'lanIp']

dash = meraki.DashboardAPI(api_key, suppress_logging=True)
device_list = dash.organizations.getOrganizationDevices(org_id, total_pages='all', productType=ptype)

with open('mx_data.csv', 'w') as file:
    csvwriter = csv.DictWriter(file, fieldnames=columns, extrasaction='ignore')
    csvwriter.writeheader()
    csvwriter.writerows(device_list)
    