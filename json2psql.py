import argparse
import psycopg2
import json

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def init_argparse():
    args = argparse.ArgumentParser(description="Insert JSON data into Postgres SQL database", formatter_class=argparse.RawTextHelpFormatter)
    args.add_argument("-a", "--address", default="127.0.0.1", help="Postgres host address, default 127.0.0.1")
    args.add_argument("-p", "--port", default=5432, help="Portgres port, default 5432")

    args.add_argument("-u", "--user", help="MongoDB username")
    args.add_argument("-P", "--password", help="MongoDB password")

    args.add_argument("-k", "--key", help="Specificing key to use as primary key in psql, the key must be existed in input json data", required=True)
    args.add_argument("-d", "--database", help="Specificing database name", required=True)
    args.add_argument("-t", "--table", help="Specificing table name", required=True)
    args.add_argument("-f", "--file", help="JSON file path", required=True)

    return args.parse_args()


def connect(database, user, password, server, port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=server,
            port=port,
        )
        return connection
    except psycopg2.OperationalError as e:
        connection = connect("postgres", user, password, server, port)  # connection to postgres in order to run create database query
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {database};")  #! may sql injectable, need test
        if connection:
            connection.close()  # close connection after database is created
        return connect(database, user, password, server, port)
    except Exception as e:
        print(e)
        return None


def check_table_existence(connection, table):
    cursor = connection.cursor()

    query = f"""SELECT EXISTS (SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = '{table}');"""
    cursor.execute(query)

    result = cursor.fetchone()[0]
    cursor.close()

    return result


def create_table(connection, name, key_col):
    cursor = connection.cursor()

    try:
        query = f"CREATE TABLE {name} ({key_col} varchar NOT NULL primary key, data json);"
        cursor.execute(query)
    except Exception as e:
        print(e)

    connection.commit()
    if cursor:
        cursor.close()


def read_file_content(file_path: str) -> list[dict]:
    print(f"Loading JSON file: {file_path}")
    try:
        with open(file_path, "r") as f:
            try:
                return json.load(f)  # when input file is: [{}, {}, {}]
            except json.decoder.JSONDecodeError:
                # when input file is: {}\n{}\n{}\n...\n{}
                f.seek(0)
                return [json.loads(line.strip()) for line in f]
    except FileNotFoundError:
        print(f"File not found: {file_path}")


def extract_key_for_json_data(json_data, key):
    """
    extra key from json_data (list of dict) so that the data can be inserted to psql
    """
    results = []

    for i in range(len(json_data)):
        temp = {
            f"{key}": json_data[i][f"{key}"],
            "data": json_data[i]
        }
        results.append(temp)
    return results


def main(client, table, file_path, key):
    # TODO: check insert many for psql in python
    new_table = False # flag to indicate if table is newly created. True => insert many; False => upsert one by one

    # create table if not exists
    table_exist = check_table_existence(client, table)
    if not table_exist:
        create_table(client, table, key)
        new_table = True

    # TODO: read json file and insert to database
    json_data = read_file_content(file_path)
    ready2insert = extract_key_for_json_data(json_data, key)

    # TODO: extract this into a function
    for data in ready2insert:
        cursor = client.cursor()
        cursor.execute(f"INSERT INTO {table} ({key}, data) VALUES ('{data[key]}', '{json.dumps(data['data'])}');")

    client.commit()

if __name__ == "__main__":
    args = init_argparse()
    client = connect(args.database, args.user, args.password, args.address, args.port)

    if client:
        main(client, args.table, args.file, args.key)
        client.close()
