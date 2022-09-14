import datetime

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.exceptions import TransportServerError

gql_url = 'https://graphql.grid.tf/graphql'

transport = RequestsHTTPTransport(url=gql_url, verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

nodes = input('Node ids? ')
months = input('Months to check? (leave blank for all) ')
if months:
  months = [int(m) for m in months.split(' ')]
else:
  months = range(1, 12)

for node in nodes.split():

  query = """
  query MyQuery {
    uptimeEvents(where: {nodeID_eq: %s}, orderBy: timestamp_ASC) {
      timestamp
      uptime
    }
  }
  """ % node

  result = client.execute(gql(query))
  uptimes = result['uptimeEvents']
  print("Node id: " + str(node))
  for i, u in enumerate(uptimes[:-1]):
      #ud = int(uptimes[i + 1]['uptime']) - int(u['uptime'])
      td = int(uptimes[i + 1]['timestamp']) - int(u['timestamp'])

      if int(uptimes[i + 1]['uptime']) < int(u['uptime']) and datetime.datetime.fromtimestamp(int(uptimes[i + 1]['timestamp'])).month in months:
            print('Node went offline: ' + str(datetime.datetime.fromtimestamp(int(u['timestamp']))))
            print('Downtime: ' + str(td - int(uptimes[i + 1]['uptime'])))
            print()

      # Nodes should report every two hours, add a little wiggle room
      elif td > 60 * 60 * 2.05 and datetime.datetime.fromtimestamp(int(uptimes[i + 1]['timestamp'])).month in months:
        print('Delayed uptime report: ' + str(datetime.datetime.fromtimestamp(int(u['timestamp']))))
        print('Timestamp delta: ' + str(td))
        print()

  print()

