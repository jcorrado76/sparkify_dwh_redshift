"""This module defines the queries to copy the data from the S3 buckets into the
staging tables
"""

import configparser
import sys
config = configparser.ConfigParser()
config.read('sql_queries/dwh.cfg')

table_names_config = configparser.ConfigParser()
table_names_config.read("sql_queries/table_names.cfg")

staging_events_copy = ("""
copy {} from '{}'
iam_role '{}'
format as json '{}'
region 'us-west-2';
""").format(table_names_config["STAGING"]["events"],
            config["S3"]["LOG_DATA"],
            config["IAM_ROLE"]["ARN"],
            config["S3"]["LOG_JSONPATH"])

staging_songs_copy = ("""
copy {} from '{}'
iam_role '{}'
format as json 'auto'
acceptinvchars as '^'
region 'us-west-2';
""").format(table_names_config["STAGING"]["songs"],
            config["S3"]["SONG_DATA"],
            config["IAM_ROLE"]["ARN"])

copy_table_queries = [staging_events_copy,
        staging_songs_copy]
