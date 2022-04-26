import meraki
import os
import json

api_key = os.getenv("MERAKI_API")
org_id = "1160673"

def get_networks():
    networks = dash.organizations.getOrganizationNetworks(org_id, total_pages="all")
    network_ids = [network["id"] for network in networks]
    return network_ids

def init_health(network_ids):
    health_dict = {}
    for network in network_ids:
        health_dict[network] = {"health": 100, "status": "healthy"}
    return health_dict

def check_device(update_dict):
    for network in update_dict:
        statuses = dash.organizations.getOrganizationDevicesStatuses(org_id, total_pages="all", networkIds=[network])
        bad_count = status_counter(statuses)
        if bad_count > 0:
            update_dict[network]["health"] -= bad_count
            update_dict[network]["status"] = "APs offline or alerting"
    return update_dict

def status_counter(statuses):
    bad_count = 0
    for device in statuses:
        if device["status"] == "alerting" or device["status"] == "offline":
            bad_count += 1
    bad_avg = (bad_count / len(statuses)) * 100
    return bad_avg

def check_connstats(update_dict):
    for network in update_dict:
        connstats = dash.wireless.getNetworkWirelessConnectionStats(network, timespan=600)
        conn_score = conn_counter(connstats)
        if conn_score["score"] > 0:
            update_dict[network]["health"] -= conn_score["score"]
            update_dict[network]["status"] = conn_score["reason"]
    return update_dict

def conn_counter(connstats):
    total_inter = connstats["auth"] + connstats["dhcp"] + connstats["dns"] + connstats["success"]
    conn_score = {"score": 0, "reason": ""}
    if total_inter > 0:
        if connstats["auth"] > 0:
            #need to figure out how to weight score decrementer for situations with lots of failures and/or no successes
            score_dec = (connstats["auth"] / total_inter) * 100
            conn_score["score"] = score_dec
            conn_score["reason"] += "Authentication Failures;"
        if connstats["dhcp"] > 0:
            score_dec = (connstats["dhcp"] / total_inter) * 100
            conn_score["score"] = score_dec
            conn_score["reason"] += "DHCP Failures;"
        if connstats["dns"] > 0:
            score_dec = (connstats["dns"] / total_inter) * 100
            conn_score["score"] = score_dec
            conn_score["reason"] += "DHCP Failures;"
    return conn_score



def main():

    network_ids = get_networks()
    health_dict = init_health(network_ids)
    health_dict = check_device(health_dict)
    health_dict = check_connstats(health_dict)
    print(json.dumps(health_dict, indent=2))



if __name__ == "__main__":
    dash = meraki.DashboardAPI(api_key, suppress_logging=True)

    main()