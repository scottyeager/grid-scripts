import requests, time, csv
#from requests_futures.sessions import FuturesSession

# Grid 2

explorer = 'https://explorer.grid.tf/api/v1/nodes'
nodes2 = []

r = requests.get(explorer)
pages = int(r.headers['Pages'])

for i in range(2, pages):
    nodes2 += r.json()
    r = requests.get(explorer + '?page=' + str(i))

# session = FuturesSession(max_workers=50)
# futures = []
# for i in range(pages - 1):    
# 	f = session.get(explorer + '?page=' + str(i + 2))
# 	futures.append(f)

# for f in futures:
# 	r = f.result()
# 	nodes2 += r.json()


# Grid 3

subnets = ['.dev', '.test', '']
proxy_base = 'https://gridproxy{}.grid.tf/nodes'

nodes3 = []
for net in subnets:
    proxy = proxy_base.format(net)

    # Grid proxy doesn't return a page count, so use serial requests here
    r = requests.get(proxy)
    page = 2
    while r.json():
        nodes3 += r.json()
        r = requests.get(proxy + '?page=' + str(page))
        page += 1

with open('grid2.csv', mode='w') as csv_file:
    fieldnames = ['node_id', 'farm_id', 'uptime', 'created', 'updated', 'country', 'city']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for n in nodes2:
        n['city'] = n['location']['city']
        n['country'] = n['location']['country']
        writer.writerow({k: n[k] for k in fieldnames})

with open('grid3.csv', mode='w') as csv_file:
    fieldnames = ['nodeId', 'farmId', 'uptime', 'created', 'updatedAt', 'country', 'city']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for n in nodes3:
        writer.writerow({k: n[k] for k in fieldnames})