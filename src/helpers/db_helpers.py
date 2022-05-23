import pandas as pd
import psycopg2

from src.config.db_credentials import HOST, PORT, PW, USER


def execute_sql_select(command, database, return_result_as_df=False):
    """Use for SELECT statements. Per default returns the result as a pandas DataFrdame"""
    conn = None
    try:
        conn = psycopg2.connect(host=HOST, port=PORT, database=database, user=USER, password=PW, sslmode='require')

        cur = conn.cursor()
        cur.execute(command)
        colnames = [desc[0] for desc in cur.description]
        print("Column names: ", colnames)
        data = cur.fetchall()
        cur.close()
        conn.commit()
        if return_result_as_df is True:
            return pd.DataFrame.from_records(data, columns=colnames)
        else:
            return colnames, data
    finally:
        if conn is not None:
            close_connection(conn)


def open_connection(database, host=HOST, port=PORT, user=USER, password=PW):
    conn_string = "host={} port={} dbname={} user={} password={}".format(host, port, database, user, password)
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    print('Connected to DB.\n')
    return conn, cursor


def close_connection(conn):
    conn.close()
    print('Connection to DB closed')
