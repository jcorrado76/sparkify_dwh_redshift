# Introduction
***

The purpose of this data warehouse to store the history of song plays in a denormalized table that can eventually be used to power downstream analytics applications and data science initiatives.
A few example uses of this data warehouse are to:
* power interactive dashboards that run queries on the sales by artist, etc.
* commercialize an API to a subset of the data stored in this warehouse
* train machine learning models on this data
* store high level metrics for C level executives in an accessible location
* generate automated reporting


# Database Design
***

This data warehouse has a single fact table, and four dimension tables.

The rows of the fact table correspond to listens of a song by a certain user.
This observable is well suited for being the observational unit of a fact table because the number of listens by song is an additive quantity.

In addition, we have dimension tables for the artist, the user, the song, and time.
This allows downstream analytics to perform group by operations and answer questions such as evolution of listens over time, listens by artist and distribution of listens by user.

For the ETL pipeline, there are a few steps.
First, the data must be loaded from the S3 JSON files into staging tables in Redshift.
Then, we use SELECT INTO commands to generate the fact and dimension tables from the staging tables.

In particular, when trying to generate the time and songplays tables, we needed to convert the given, epoch-based time stamp value into a proper timestamp first.

# Repo Organization
***

This repository is organized in a way that is designed to be modular and extensible without having to change already existing code.
In this way, we could potentially add more tables and more queries as needed, without having to alter pre-existing code.

The driver scripts are `create_tables.py`, which drops any already existing tables, and creates the tables to be used in this project, and `etl.py`, which loads the data from the S3 bucket into the staging tables, and then from the staging tables into the final tables.

The user simply needs to run:
`python create_tables.py`
`python etl.py`

To create the tables and run the ETL logic.
To replicate the same environment that was used for the development of this repo, an `environment.txt` file is provided.
Create a conda environment with:
`conda create --name [env_name] --file environment.txt`

Then, run your python commands.

The SQL queries are defined in the `sql_queries` directory.
Inside the `sql_queries` directory, there are two subdirectories, `create` and `load`.

The `create` subdirectory contains the SQL query definitions for dropping the tables, as well as creating both the staging and the final tables.
The `load` subdirectory contains the SQL query definitions for loading the data from the S3 bucket into the staging tables, and for loading the data from the staging tables into the final tables.

The `__init__.py` files in `sql_queries`, `load` and `create` are written to import the corresponding lists of SQL queries.
This way, if a new user wants to write new driver scripts that access those SQL queries, they just have to write something of the form:
`from sql_queries.load import [which_query you want]`.

In addition, as a result of this modular nature, changes to the table names, or the SQL contents don't require changes in any other location in the code.
