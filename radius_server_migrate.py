import meraki
import os

api_key = os.getenv("MERAKI_KEY")
org_id = os.getenv("ORG_ID")
net_ids = ['someids']
radserv_ips = ['10.10.10.10', '10.10.10.11']
radpsk = 'mysecret'

def build_rad_array():
    radservs = []
    for ip in radserv_ips:
        radservs.append({'host': ip, 'port': '1812', 'secret': radpsk })
    return radservs

def update_radius(radservs):
    results = []
    for network in net_ids:
        result = dash.wireless.updateNetworkWirelessSsid(network, 1, radiusServers=radservs)
        results.append(result)
    return results


if __name__ == "__main__":
    dash = meraki.DashboardAPI(api_key, suppress_logging=True)
    radservs = build_rad_array()
    result = update_radius(radservs)
    print(result)
