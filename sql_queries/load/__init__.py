"""This module imports the lists of SQL queries from the scripts defining the
SQL queries for loading data from the S3 buckets into the staging tables, and
then from the staging tables into the final tables
"""
from .load_data_into_staging_tables_queries import copy_table_queries
from .load_data_into_final_tables_queries import insert_table_queries
