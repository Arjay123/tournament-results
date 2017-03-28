#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(db_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection.

    This block of code was provided by a Udacity reviewer who recommended
    I refactor the connect method to return both the connection and cursor,
    as well as enclose the connection code in a try/except block.

    """
    try:
        db = psycopg2.connect("dbname=%s" % db_name)
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error connecting to database: " % db_name)


def deleteMatches():
    """Remove all the match records from the database."""
    conn, c = connect()
    c.execute("TRUNCATE matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, c = connect()
    c.execute("TRUNCATE players CASCADE;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, c = connect()
    c.execute("select count(*) from players;")
    res = c.fetchone()
    return res[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, c = connect()
    query = "insert into players (name) values (%s)"
    params = (name,)
    c.execute(query, params)
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, c = connect()
    c.execute("select * from standings;")

    standings = c.fetchall()

    conn.close()

    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost

    Throws:
        psycopg2.IntegrityError - if winner and loser are same player, or id
        does not match any registered player
    """
    conn, c = connect()
    query = "insert into matches (winner, loser) values (%s, %s)"
    params = (winner, loser,)
    c.execute(query, params)
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()

    # This line of code is from this
    # stack overflow thread by the user 'Margus'
    # http://stackoverflow.com/a/5389578
    #
    # ex.
    # list1 - standings[::2]  = [A, C, E, G]
    # list2 - standings[1::2] = [B, D, F, H]
    #
    # zip(list1, list2) = [(A, B), (C, D), (E, F), (G, H)]
    zipped_pairs = zip(standings[::2], standings[1::2])

    # extract both tuples (size 2) inside each list tuple element to create
    # a larger tuple (size 4) for each list element
    pairings = [(x[0], x[1], y[0], y[1]) for x, y in zipped_pairs]
    return pairings
