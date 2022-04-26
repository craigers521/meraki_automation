import meraki
import json
import os
from google.cloud import bigquery

# Defining your API key as a variable in source code is not recommended
API_KEY = os.getenv("MERAKI_API")
# Instead, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

dashboard = meraki.DashboardAPI(api_key=API_KEY, suppress_logging=True)

org_id = '1063737'
networks = dashboard.organizations.getOrganizationNetworks(org_id, total_pages='all')
network_ids = [network['id'] for network in networks]

client = bigquery.Client()
#need to update schema for client table yet... 
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField()
    ]
)
job_config.source_format = 'NEWLINE_DELIMITED_JSON'
job_config.autodetect = True
dataset_id = 'test_ds'
table_id = 'test_tbl'
dataset = client.dataset(dataset_id)
table = dataset.table(table_id)

for nid in network_ids:
    meraki_data = dashboard.networks.getNetworkClients(nid, total_pages='all', statuses='Online')
    #load_job = client.load_table_from_json(meraki_data, table, location='US', job_config=job_config)
    #print(load_job.result())
    print(json.dumps(meraki_data, indent=2))

