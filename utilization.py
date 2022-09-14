import sys

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.exceptions import TransportServerError

gql_url = 'https://graphql.grid.tf/graphql'

if sys.argv[-1] in ['dev', 'test']:
    gql_url = 'https://graphql.{}.grid.tf/graphql'.format(sys.argv[-1])

transport = RequestsHTTPTransport(url=gql_url, verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

query = """
query MyQuery {
  nodeContracts(where: {state_eq: Created}) {
    deploymentData
    resourcesUsed {
      cru
      hru
      mru
      sru
    }
    nodeID
    numberOfPublicIPs
  }
}
"""

result = client.execute(gql(query))

used = {'cru': 0, 'hru': 0, 'mru': 0, 'sru': 0}

for contract in result['nodeContracts']:
    if contract['resourcesUsed']:
        for k, v in contract['resourcesUsed'].items():
            used[k] += int(v)

# Convert to gigabytes
for k in ['hru', 'mru', 'sru']:
    used[k] = used[k] / 10**9

print('Cores: ' + str(round(used['cru'])))
print('RAM: ' + str(round(used['mru'])) + ' GB')
print('SSD: ' + str(round(used['sru'])) + ' GB')
print('HDD: ' + str(round(used['hru'])) + ' GB')