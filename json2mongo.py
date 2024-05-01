import argparse

import json

import pymongo


def init_argparse():
    args = argparse.ArgumentParser(description="Insert JSON data into MongoDB", formatter_class=argparse.RawTextHelpFormatter)
    args.add_argument("-a", "--address", default="127.0.0.1", help="MongoDB host address")
    args.add_argument("-p", "--port", default=27017, help="MongoDB port")
    args.add_argument("-d", "--database", help="Specificing database name", required=True)
    args.add_argument("-c", "--collection", help="Specificing collection name", required=True)
    args.add_argument("-f", "--file", help="JSON file path", required=True)

    return args.parse_args()


def construct_mongo_uri(address, port):
    return f"mongodb://{address}:{port}"


def main(mongo_str: str, file_path: str, database: str, collection: str):
    client = None
    try:
        client = pymongo.MongoClient(mongo_str)
    except Exception as e:
        print(e)


    # TODO: read JSON file and insert into MongoDB
    data_list = []
    with open(file_path, 'r') as f:
        data_list = [json.loads(line.strip()) for line in f]
    db = client[database]
    table = db[collection]
    for data in data_list:
        table.replace_one({"host": data["host"]}, data, upsert=True)

    if client:
        client.close()


if __name__ == "__main__":
    args = init_argparse()
    mongo_str = construct_mongo_uri(args.address, args.port)
    main(mongo_str, args.file, args.database, args.collection)
