# pdjson2mongo

Insert ProjectDiscovery's tools json output to MongoDB

## Usage

```shell
usage: json2mongo.py [-h] [-a ADDRESS] [-p PORT] -d DATABASE -c COLLECTION -f FILE

Insert JSON data into MongoDB

options:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        MongoDB host address
  -p PORT, --port PORT  MongoDB port
  -d DATABASE, --database DATABASE
                        Specificing database name
  -c COLLECTION, --collection COLLECTION
                        Specificing collection name
  -f FILE, --file FILE  JSON file path
```
