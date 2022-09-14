import requests, time, csv

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


now = time.time()
lastweek = now - 7 * 24 * 60 * 60
yesterday = now - 24 * 60 * 60

newnodes = [n for n in nodes3 if n['created'] > lastweek and n['updatedAt'] > yesterday]

countries = {n['location']['country']: 0 for n in newnodes}

for n in newnodes:
    countries[n['location']['country']] += 1

print('Total: ' + str(len(newnodes)))

for c, i in countries.items():
    print('* ' + c + ': ' + str(i))
