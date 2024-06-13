import meraki
import os
import csv
from datetime import datetime

api_key = os.getenv("MERAKI_KEY")
org_id = "1280364"


def get_networks():
    networks = dash.organizations.getOrganizationNetworks(org_id, total_pages="all")
    network_ids = [network["id"] for network in networks if "wireless" in network["productTypes"]]
    return network_ids


def get_failed(networks):
    conn_logs = []
    for network in networks:
        net_logs = dash.wireless.getNetworkWirelessFailedConnections(network, timespan=604800)
        conn_logs.append(net_logs)
    return conn_logs


def output_csv(logs):
    timestr = datetime.now().strftime("%Y%m%d")
    filename = f"logs-{timestr}.csv"
    if len(logs) > 0:
        with open(filename, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=logs[0][0].keys())
            writer.writeheader()
            for log in logs:
                for entry in log:
                    writer.writerow(entry)
    else:
        print("No failed conns found")

if __name__ == "__main__":
    dash = meraki.DashboardAPI(api_key, suppress_logging=True)
    network_ids = get_networks()
    conn_logs = get_failed(network_ids)
    #print(conn_logs)
    output_csv(conn_logs)
