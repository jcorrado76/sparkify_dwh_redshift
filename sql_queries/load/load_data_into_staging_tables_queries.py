"""This module defines the queries to copy the data from the S3 buckets into the
staging tables
"""

import configparser
import sys
sys.path.insert("..")
config = configparser.ConfigParser()
config.read('dwh.cfg')

table_names_config = configparser.ConfigParser()
table_names_config.read("table_names.cfg")

staging_events_copy = ("""
COPY {} 
FROM '{}'
CREDENTIALS 'aws_iam_role={}'
REGION 'US-WEST-2';
""").format(table_names_config["STAGING"]["events"],
            config["S3"]["LOG_DATA"],
            config["IAM_ROLE"]["ARN"])


staging_songs_copy = ("""
COPY {} 
FROM '{}'
CREDENTIALS 'aws_iam_role={}'
FORMAT AS JSON 'auto'
REGION 'US-WEST-2';
""").format(table_names_config["STAGING"]["songs"],
            config["S3"]["SONG_DATA"],
            config["IAM_ROLE"]["ARN"])

copy_table_queries = [staging_events_copy,
        staging_songs_copy]
