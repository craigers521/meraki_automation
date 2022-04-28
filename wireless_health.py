"""
Copyright (c) 2022 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied
"""

import meraki
import os
import json

api_key = os.getenv("MERAKI_KEY")
org_id = "398020"


def get_networks():
    networks = dash.organizations.getOrganizationNetworks(org_id, total_pages="all")
    # only store networkIds for combined or wireless networks
    network_ids = [
        network["id"] for network in networks if "wireless" in network["productTypes"]
    ]
    return network_ids


def init_health(network_ids):
    health_dict = {}
    for network in network_ids:
        health_dict[network] = {"health": 100, "status": "healthy"}
    return health_dict


def check_device(update_dict):
    # optimize: make less API calls if made single org call then mapped device status to networks
    for network in update_dict:
        statuses = dash.organizations.getOrganizationDevicesStatuses(
            org_id, total_pages="all", networkIds=[network]
        )
        if len(statuses) > 0:  # check to see if network has devices
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
        connstats = dash.wireless.getNetworkWirelessConnectionStats(
            network, timespan=600
        )
        conn_score = conn_counter(connstats)
        if conn_score["score"] > 0:
            update_dict[network]["health"] -= conn_score["score"]
            update_dict[network]["status"] = conn_score["reason"]
    return update_dict


def conn_counter(connstats):
    total_inter = (
        connstats["auth"] + connstats["dhcp"] + connstats["dns"] + connstats["success"]
    )
    conn_score = {"score": 0, "reason": ""}
    if total_inter > 0:
        if connstats["auth"] > 0:
            # need to figure out how to weight score decrementer for situations with lots of failures and/or no successes
            score_dec = round((connstats["auth"] / total_inter) * 100)
            conn_score["score"] += score_dec
            conn_score["reason"] += "Authentication Failures;"
        if connstats["dhcp"] > 0:
            score_dec = round((connstats["dhcp"] / total_inter) * 100)
            conn_score["score"] += score_dec
            conn_score["reason"] += "DHCP Failures;"
        if connstats["dns"] > 0:
            score_dec = round((connstats["dns"] / total_inter) * 100)
            conn_score["score"] += score_dec
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
