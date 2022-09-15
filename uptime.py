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

  print()
  print('Node ' + str(node))
  print('----------------------')
  print()

  found = False

  for i, u in enumerate(uptimes[:-1]):
      #ud = int(uptimes[i + 1]['uptime']) - int(u['uptime'])
      td = int(uptimes[i + 1]['timestamp']) - int(u['timestamp'])
      month = datetime.datetime.fromtimestamp(int(uptimes[i + 1]['timestamp'])).month

      if int(uptimes[i + 1]['uptime']) < int(u['uptime']) and month in months:
            print('Node went offline: ' + str(datetime.datetime.fromtimestamp(int(u['timestamp']))))
            print('Downtime: ' + str(td - int(uptimes[i + 1]['uptime'])))
            print()
            found = True

      # Nodes should report every two hours, add a little wiggle room
      elif td > 60 * 60 * 2.05 and month in months and month not in (12,1):
        print('Delayed uptime report: ' + str(datetime.datetime.fromtimestamp(int(u['timestamp']))))
        print('Timestamp delta: ' + str(td))
        print()
        found = True

      # During December and January (through ~14), nodes reported every 8 hours
      elif td > 60 * 60 * 8.05 and month in (12,1) and month in months:
        print('Delayed uptime report: ' + str(datetime.datetime.fromtimestamp(int(u['timestamp']))))
        print('Timestamp delta: ' + str(td))
        print()
        found = True

  if not found:
    print('No uptime irregularities found')
  print()

