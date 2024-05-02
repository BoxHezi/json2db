# pdjson2mongo

Utility convert JSON data and insert to MongoDB

## Usage

```shell
usage: json2mongo.py [-h] [-a ADDRESS] [-p PORT] [-u USER] [-P PASSWORD] [-k KEY] -d DATABASE -c COLLECTION -f FILE

Insert JSON data into MongoDB

options:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        MongoDB host address
  -p PORT, --port PORT  MongoDB port
  -u USER, --user USER  MongoDB username
  -P PASSWORD, --password PASSWORD
                        MongoDB password
  -k KEY, --key KEY     Specificing key to check for upsert operation
                        If not specified, all records will be inserted
  -d DATABASE, --database DATABASE
                        Specificing database name
  -c COLLECTION, --collection COLLECTION
                        Specificing collection name
  -f FILE, --file FILE  JSON file path
```
