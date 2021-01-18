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
For this purpose, to avoid recomputing the timestamp, I created an intermediate temporary table where I computed the conversion of the epoch-based timestamp into a human-readable timestamp.

Then, I used this intermediate timestamp table to populate the start time field of the fact table, and to power the extract commands used to determine the rest of the fields for the time table.
