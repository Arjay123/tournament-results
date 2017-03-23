-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.



-- Connect to tournament db
\c tournament

-- RESET
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;


-- players table
CREATE TABLE players(
    id serial PRIMARY KEY,
    name text
);

-- matches
CREATE TABLE matches(
    id serial,
    winner serial REFERENCES players(id),
    loser serial REFERENCES players(id)
);