import meraki
import os
import getopt
import sys
import datetime

api_key = os.getenv("MERAKI_KEY")
org_id = os.getenv("ORG_ID")

def parse_args(args):
    tag = None
    try:
        opts, args = getopt.getopt(args, "ht:", ["tag="])
    except getopt.GetoptError:
        print("you're doing it wrong")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("use -t or --tag to specify tagged network to search")
            sys.exit()
        elif opt in ("-t", "--tag"):
            tag = arg
    return tag

def addMonth():
    newdate = datetime.datetime.utcnow()+datetime.timedelta(days=30)
    formatdate = newdate.strftime("%Y-%m-%dT%H:%M:%SZ") 
    return formatdate

def findTaggedNets(tag):
    networks = dash.organizations.getOrganizationNetworks(org_id, total_pages="all", tags=tag)
    network_ids = [network["id"] for network in networks]
    return network_ids

def findPendingUpgrades():
    response = dash.organizations.getOrganizationFirmwareUpgrades(org_id, status="Pending")
    return response

def stallUpgrades(tagged_nets, upgrades):
    for upgrade in upgrades:
        network_id = upgrade['network']['id']
        prod_type = upgrade['productType']
        if network_id not in tagged_nets:
            response = dash.networks.updateNetworkFirmwareUpgrades(network_id, 
                                                                   products={prod_type: {'nextUpgrade': {'time': newdate}}})
            print(f"Rescheduled firmware upgrade for {prod_type} devices on network {network_id}")
    pass



if __name__ == "__main__":
    dash = meraki.DashboardAPI(api_key, suppress_logging=True)
    tag = parse_args(sys.argv[1:])
    newdate = addMonth()
    tagged_nets = findTaggedNets(tag)
    upgrades = findPendingUpgrades()
    stallUpgrades(tagged_nets, upgrades)
