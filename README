These Python scripts provide examples for working with data sources from the ThreeFold Grid, such as querying information about nodes or workloads. It utilizes both the Grid Proxy REST API and the TF Chain GraphQL service. There's more information about these data sources below.

You can install and run the scripts locally (tested and documented for Linux, same commands should work on MacOS, if you try Windows please report your experience in an issue). Alternatively, you can use a free hosted Jupyter notebook provided by Binder.

## Install

The only dependency outside of the standard library is [gql](https://github.com/graphql-python/gql), for the scripts that use GraphQL. We only use the `requests` based provider, which can be installed without additional bloat using:

```
pip install gql[requests]
```

Then clone this repo and execute the scripts using `python`. Using interactive mode to play with the data further can be nice, especially when a larger amount of data is retrieved. For example, after running `new-nodes.py` the list of nodes will be available in the `nodes3` variable in the console:

```
$ python -i new-nodes.py
...
>>> nodes3[0]['location']['country']
'Belgium'
```

## Binder

This repository also includes files that make it compatible with [Binder](https://mybinder.org/), which provides a hosted Jupyter notebook where you can edit and run the scripts in an isolated environment. To launch Binder, click the following badge [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/scottyeager/grid-scripts/HEAD)

## Data Sources

### Grid Proxy

Grid Proxy is a REST API that serves data cached from other sources, namely GraphQL and the nodes themselves. For any data available from Grid Proxy, it's normally the best way to query that data. You can find more details on the API on the [Swagger docs](https://gridproxy.grid.tf/swagger/index.html).

### GraphQL

ThreeFold Chain state and some historical data is made available through a GraphQL interface. This includes all of the available details about nodes, farms, and workload contracts. GraphQL includes a graphical interface for exploring the protocol and data types provided from TF Chain, at the same [link](https://graphql.grid.tf/graphql) used for queries in code.

### Testnet and Devnet

The links above are for mainnet. Links for other networks can be derived according to a predictable scheme.

Testnet:
* https://gridproxy.test.grid.tf/swagger/index.html
* https://graphql.test.grid.tf/graphql

Devnet:
* https://gridproxy.dev.grid.tf/swagger/index.html
* https://graphql.dev.grid.tf/graphql