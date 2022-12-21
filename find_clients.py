import meraki
import os
import json
import sys
import getopt

api_key = os.getenv("MERAKI_KEY")
org_id = "1160673"


def parse_args(args):
    mac = None
    try:
        opts, args = getopt.getopt(args, "hm:", ["mac="])
    except getopt.GetoptError:
        print("you're doing it wrong")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("this is a help message")
            sys.exit()
        elif opt in ("-m", "--mac"):
            mac = arg
    return mac


def get_networks():
    networks = dash.organizations.getOrganizationNetworks(org_id, total_pages="all")
    network_ids = [network["id"] for network in networks]
    return network_ids


def find_clients(networks, filter_mac):
    found_clients = []
    for network in networks:
        client_list = dash.networks.getNetworkClients(network, mac=filter_mac)
        if len(client_list) > 0:
            client_info = [
                {k: d[k] for k in ("id", "mac", "ip", "switchport")}
                for d in client_list
            ]
            for device in client_info:
                device["network"] = network
                found_clients.append(device)
    return found_clients


if __name__ == "__main__":
    mac = parse_args(sys.argv[1:])
    dash = meraki.DashboardAPI(api_key, suppress_logging=True)
    network_ids = get_networks()
    found_clients = find_clients(network_ids, mac)
    print(found_clients)
