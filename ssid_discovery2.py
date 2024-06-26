import meraki
import os
import csv


api_key = os.getenv("MERAKI_KEY")
org_id = os.getenv("ORG_ID")

def getNetworks():
    networks = dash.organizations.getOrganizationNetworks(org_id, total_pages=all)
    wireless_nets = [
        network for network in networks if "wireless" in network["productTypes"]
    ]
    return wireless_nets

def findSsidEnabled(networks):
    enabled_nets = []
    for network in networks:
        ssids = dash.wireless.getNetworkWirelessSsids(network['id'])
        enabled_ssids = {"net_name":network['name']}
        for ssid in ssids:
            k = "ssid"+str(ssid['number'])
            enabled_ssids[k] = ssid['name']
        enabled_nets.append(enabled_ssids)
    return enabled_nets

def output_names(networks):
    filename = 'ssids.csv'
    if len(networks) > 0:
        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=networks[0].keys())
            writer.writeheader()
            writer.writerows(networks)
    pass

if __name__ == "__main__":
    dash = meraki.DashboardAPI(api_key, suppress_logging=True)
    networks = getNetworks()
    enabled_nets = findSsidEnabled(networks)
    output_names(enabled_nets)