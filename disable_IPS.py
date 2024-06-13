import meraki
import os
import json
import sys
import getopt
import csv

api_key = os.getenv("MERAKI_KEY")
org_id = "1160673"



def get_networks():
    networks = dash.organizations.getOrganizationNetworks(org_id, total_pages="all")
    network_ids = [network["id"] for network in networks]
    return network_ids


def disable_ips(networks):
    


if __name__ == "__main__":
    dash = meraki.DashboardAPI(api_key, suppress_logging=True)
    network_ids = get_networks()
    disable_ips(network_ids)
