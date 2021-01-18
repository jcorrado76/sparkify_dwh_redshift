"""This module is a dunder init file that exposes all of the lists that contain
the queries so that it can be imported at the top level much easier
"""
from create import drop_table_queries, \
        create_staging_tables_queries, \
        create_final_tables_queries
from load import copy_table_queries, \
    insert_table_queries
