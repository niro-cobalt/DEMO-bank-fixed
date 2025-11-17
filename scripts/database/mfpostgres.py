"""
Copyright 2010 – 2024 Rocket Software, Inc. or its affiliates. 
This software may be used, modified, and distributed
(provided this notice is included without modification)
solely for internal demonstration purposes with other
Rocket® products, and is otherwise subject to the EULA at
https://www.rocketsoftware.com/company/trust/agreements.

THIS SOFTWARE IS PROVIDED "AS IS" AND ALL IMPLIED
WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE,
SHALL NOT APPLY.
TO THE EXTENT PERMITTED BY LAW, IN NO EVENT WILL
ROCKET SOFTWARE HAVE ANY LIABILITY WHATSOEVER IN CONNECTION
WITH THIS SOFTWARE.

Description:  PostGres utility functions. 
"""
import psycopg2

def connect_to_pg_server(database_host, database_port, database_name, database_user, database_password):

    connection_details = 'host={} port={} dbname={} user={} password={}'.format(database_host, database_port, database_name, database_user, database_password)
    pgconn = psycopg2.connect (connection_details)

    pgconn.autocommit = True

    return pgconn

def execute_pg_command(pgconn, sql_command):

    pgcursor = pgconn.cursor()

    pgcursor.execute(sql_command)

def disconnect_from_pg_server(pgconn):

    pgconn.close