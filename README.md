## tournament-results
This is a project meant to help run a tournament using the swiss format. More about the swiss format can be read here:<br>
https://en.wikipedia.org/wiki/Swiss-system_tournament

The project consists of a sql file which initializes the database with tables and views, and a python file which will be used to edit that database with new players, standings, set up matches, etc.

## Install

Database used is postgresql: https://www.postgresql.org/ <br>
Psycopg is used to connect python to the database: http://initd.org/psycopg/

To set up the database you must create a database called "tournament", which you can do through the psql shell:
>CREATE DATABASE tournament;

After setting up the database you can import the sql file using the command:
>\i tournament.sql

## Usage

Once the sql file has been imported, you can test the module by running the command:

>python tournament_test.py

