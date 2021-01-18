"""This module is responsible for making a connection to the Redshift cluster,
runing the SQL queries to drop any tables that have been created, and re-create
them using the create SQL queries
"""


import configparser
import psycopg2
from drop_sql_queries import drop_table_queries
from create_staging_tables_queries import create_staging_tables_queries
from create_final_tables_queries import create_final_tables_queries


def drop_tables(cur, conn):
    """This function executes the drop table queries
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """This function executes all of the create table queries
    """
    for query in create_staging_tables_queries:
        cur.execute(query)
        conn.commit()
    for query in create_final_tables_queries:
        cur.execute(query)
        conn.commit()


def main():
    """Driver method for this script
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}"\
            .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
