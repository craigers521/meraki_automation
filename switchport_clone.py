import meraki
import os
import batch_helper

API_KEY = os.getenv("MERAKI_KEY")
ORG_ID = "1280364"

def get_networks():
    networks = dash.organizations.getOrganizationNetworks(ORG_ID, total_pages='all', tags=['migrate'], tagsFilterTyle='withAnyTags')
    
    return networks

def get_switches(networks,mytags):
    net_ids = [network['id'] for network in networks]
    tags = list(sum(mytags, ()))
    switches = dash.organizations.getOrganizationDevices(ORG_ID, networkIds=net_ids, productTypes=['switch'], tags=tags, tagsFilterType='withAnyTags')
    src_switches,dst_switches = [], []
    for tag in mytags:
        assert tag[0][-1] == tag[1][-1], f"tag pairs do not match"
        taggroup = tag[0][-1]
        tagtypesrc = tag[0][:3]
        tagtypedst = tag[1][:3]
        src_switches.extend([switch for switch in switches if tagtypesrc+taggroup in switch['tags']])
        dst_switches.extend([switch for switch in switches if tagtypedst+taggroup in switch['tags']])

    return src_switches,dst_switches

def create_port_actions(src_switches, dst_switches, tags):
    assert len(src_switches) == len(dst_switches), f"Total source switches does not match total destination switches"
    port_configs = [dash.switch.getDeviceSwitchPorts(switch['serial']) for switch in src_switches]
    actions = []
    for i,ports in enumerate(port_configs):
        for port in ports:
            try:
                if eval(port['portId']) > 24:
                    continue
            except Exception:
                continue
            if 'accessPolicyNumber' in port:
                action = dash.batch.switch.updateDeviceSwitchPort(
                    serial=[dst_switches[i]['serial']],
                    portId=port['portId'],
                    name=port['name'],
                    type=port['type'],
                    vlan=port['vlan'],
                    voiceVlan=port['voiceVlan'],
                    allowedVlans=port['allowedVlans'],
                    accessPolicyType=port['accessPolicyType'],
                    accessPolicyNumber=port['accessPolicyNumber']
                )
            else:
                action = dash.batch.switch.updateDeviceSwitchPort(
                    serial=dst_switches[i]['serial'],
                    portId=port['portId'],
                    name=port['name'],
                    type=port['type'],
                    vlan=port['vlan'],
                    voiceVlan=port['voiceVlan'],
                    allowedVlans=port['allowedVlans'],
                    accessPolicyType=port['accessPolicyType']
                )
            actions.append(action)
    return actions


def batch_actions(actions):
    helper = batch_helper.BatchHelper(dash, ORG_ID, actions)
    helper.prepare()
    helper.generate_preview()
    helper.execute()


def main():
    network_list = get_networks()
    tags = [('srcA', 'dstA')]
    src_switches,dst_switches = get_switches(network_list, tags)
    actions = create_port_actions(src_switches, dst_switches, tags)
    batches = batch_actions(actions)


if __name__ == "__main__":
    dash = meraki.DashboardAPI(API_KEY, suppress_logging=True)
    main()