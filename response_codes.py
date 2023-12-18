import meraki
import requests
import os

api_key = os.getenv("MERAKI_KEY")
token = f"Bearer {api_key}"
org_id = "1280364"

def requests_orgs():
    url = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
    payload = None
    headers = {
        "Accept": "application/json",
        "Authorization": token
    }
    response = requests.request('GET', url, headers=headers, data = payload)
    print(response.text.encode('utf8'))
    pass

def sdk_orgs():
    dashboard = meraki.DashboardAPI(api_key)
    response = dashboard.organizations.getOrganizationNetworks(
        org_id, total_pages='all')
    print(response)
    pass

if __name__ == "__main__":
    requests_orgs()
    sdk_orgs()