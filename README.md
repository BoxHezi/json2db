# json2mongo

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

## Example

1. `python json2mongo.py -d test -c mytable -f myjson.json`

The above command will read JSON file `myjson.json` and insert data into collection `mytable` in database `test`.

### JSON File

Currently, support two JSON format:

1. Regular JSON with one big list

```json
[
  {
    "name": "myname1",
    "age": 20
  },
  {
    "name": "myname2",
    "age": 30
  }
]
```

2. File which each line is a JSON object

```json
{ "name": "myname1", "age": 20 }
{ "name": "myname2", "age": 30 }
```
