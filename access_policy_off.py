import meraki
import os

api_key = os.getenv("MERAKI_KEY")
org_id = os.getenv("ORG_ID")
ptype = ['switch']

def getSwitches():
    switch_list = dash.organizations.getOrganizationDevices(org_id, total_pages='all', productTypes=ptype)
    return switch_list

def changePolicy(switches):
    result_list = []
    for switch in switches:
        ports = dash.switch.getDeviceSwitchPorts(switch['serial'])
        for port in ports:
            if port['accessPolicyType'] != 'Open':
                result = dash.switch.updateDeviceSwitchPort(switch['serial'], port['portId'], accessPolicyType='Open' )
                result_list.append(result)
    return result_list

if __name__ == "__main__":
    dash = meraki.DashboardAPI(api_key, suppress_logging=True)
    switch_list = getSwitches()
    results = changePolicy(switch_list)
    print(results)