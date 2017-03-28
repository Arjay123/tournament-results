-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.



-- Reset then connect to tournament db
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament


-- players table
CREATE TABLE players(
    id serial PRIMARY KEY,
    name text
);

-- matches
CREATE TABLE matches(
    id serial,
    winner integer REFERENCES players(id) CHECK (winner != loser),
    loser integer REFERENCES players(id)
);



-- Views
CREATE VIEW matches_played as 
    SELECT players.id as player_id, count(matches.id) as matches
    FROM players 
    LEFT JOIN matches ON players.id = winner OR players.id = loser 
    GROUP BY players.id;


CREATE VIEW matches_won as
    SELECT players.id as player_id, count(matches.id) as won
    FROM players
    LEFT JOIN matches ON players.id = winner
    GROUP BY players.id;


CREATE VIEW standings as 
    SELECT players.id, players.name, won, matches_played.matches
    FROM players, matches_won, matches_played
    WHERE players.id = matches_won.player_id AND players.id = matches_played.player_id
    ORDER BY won;
