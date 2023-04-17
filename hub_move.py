import meraki
import os
import getopt
import sys

api_key = os.getenv("MERAKI_KEY")
org_id = os.getenv("ORG_ID")

def parse_args(args):
    hub = spoke = None
    try:
        opts, args = getopt.getopt(args, "hb:s:", ["hub=", "spoke="])
    except getopt.GetoptError:
        print("you're doing it wrong")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("this is a help message")
            sys.exit()
        elif opt in ("-b", "--hub"):
            hub = arg
        elif opt in ("-s", "--spoke"):
            spoke = arg
    return hub, spoke

def findTaggedNets(tag):
    networks = dash.organizations.getOrganizationNetworks(org_id, total_pages="all", tags=tag)
    #tagged_nets = [network["id"] for network in networks if tag in network['tags']]
    network_ids = [network["id"] for network in networks]
    return network_ids

def getSubnets(networks):
    subnets = []
    for network in networks:
        lan = dash.appliance.getNetworkApplianceSingleLan(network)
        subnets.append(lan["subnet"])
    return subnets

def updateVPN(hub, spokes, subnets):
    for sp, sub in zip(spokes, subnets):
        response = dash.appliance.updateNetworkApplianceVpnSiteToSiteVpn(sp, mode="spoke",
                                                                         hubs=[{'hubId': hub[0], 'useDefaultRoute': False}],
                                                                         subnets=[{'localSubnet': sub, 'useVpn': True}])
        print(response)
    pass

if __name__ == "__main__":
    dash = meraki.DashboardAPI(api_key, suppress_logging=True)
    hub, spoke = parse_args(sys.argv[1:])
    myhubs = findTaggedNets(hub)
    myspokes = findTaggedNets(spoke)
    mysubs = getSubnets(myspokes)
    updateVPN(myhubs, myspokes, mysubs)