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
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS players CASCADE;

-- players table
CREATE TABLE players(
    id serial PRIMARY KEY,
    name text
);

-- matches
CREATE TABLE matches(
    id serial,
    winner serial REFERENCES players(id) CHECK (winner != loser),
    loser serial REFERENCES players(id)
);



-- Views
CREATE VIEW matches_played as 
    SELECT players.id as player_id, count(matches.id) as matches
    FROM players 
    LEFT JOIN matches 
    ON players.id = winner OR players.id = loser 
    GROUP BY players.id;


CREATE VIEW matches_won as
    SELECT players.id as player_id, count(*) as won
    FROM players
    LEFT JOIN matches
    ON players.id = winner
    GROUP BY players.id;


CREATE VIEW standings as 
    SELECT players.id, players.name, won, matches_played.matches
    FROM players, matches_won, matches_played
    WHERE players.id = matches_won.player_id AND players.id = matches_played.player_id;
