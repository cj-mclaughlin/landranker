# Manage Serving of Images for Matchups (S3/PostgreSQL)
import psycopg2 as psql

def connect_db():
    """
    Establish connection to postgres database

    Returns:
        tuple of postgres connection and cursor objects (conn, cur)
    """
    dbname = "landranker"
    user = "postgres"
    password = "devpassword"
    host = "landranker-test.cp4haaxrm2p8.us-east-1.rds.amazonaws.com"
    port = 5432
    conn = psql.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cur = conn.cursor()
    return conn, cur

def disconnect_db(conn, cur):
    """
    End postgres connection/cursor

    Args:
        conn: postgres connection object
        cur: postgres cursor object
    """
    cur.close()
    conn.close()

def query_land_objects(land_id1, land_id2):
    """
    Query land data by ids from postgres 
    and return associated information

    Args:
        land_id1: integer id of land value for match
        land_id2: integer id of land value for match

    Returns:
        Tuple of objects containing land data for each id
    """
    sql1 = f"SELECT land_id, s3_url, elo FROM lands WHERE land_id = {land_id1}"
    sql2 = f"SELECT land_id, s3_url, elo FROM lands WHERE land_id = {land_id2}"
    land1, land2 = None, None
    try:
        conn, cur = connect_db()
        cur.execute(sql1)
        assert cur.rowcount == 1
        land1 = psql_to_object(cur.fetchone())
        cur.execute(sql2)
        assert cur.rowcount == 1
        land2 = psql_to_object(cur.fetchone())
        disconnect_db(conn, cur)
    except (Exception, psql.DatabaseError) as error:
        print(error)
    print(land1, land2)
    return land1, land2


def psql_to_object(psql_land):
    """
    Convert tuple (as given from psql) into dictionary object

    Args:
        psql_land: tuple response from psql query of land table

    Returns:
        dictionary object containing land data indexed as in schema
    """
    land = {}
    land["land_id"] = psql_land[0]
    land["s3_url"] = psql_land[1]
    land["elo"] = psql_land[2]
    return land


def update_land_elo(land_id, new_elo):
    """
    Update elo rating of specific land

    Args: 
        land_id: integer id of land to modify
        new_elo: integer post-match elo of land
    """
    sql = f"UPDATE lands SET elo = {new_elo} WHERE land_id = {land_id}"
    try:
        conn, cur = connect_db()
        cur.execute(sql)
        conn.commit()
        disconnect_db(conn, cur)
    except (Exception, psql.DatabaseError) as error:
        print(error)


def add_match_result(land_id1, land_id2, result):
    """
    Add land match result to records table

    Args:
        land_id1: integer id of land value for match
        land_id2: integer id of land value for match
        result: boolean true if land1 wins, false if land2
    """
    sql = f"INSERT INTO records (land_id1, land_id2, result) VALUES ({land_id1}, {land_id2}, {result})"
    try:
        conn, cur = connect_db()
        cur.execute(sql)
        conn.commit()
        disconnect_db(conn, cur)
    except (Exception, psql.DatabaseError) as error:
        print(error)


def sample_random_lands(land_type=None):
    """
    Sample a pair of land objects for ranking match

    Args:
        land_type: (optional) specific type of land to sample (see string enum in schema)

    Returns:
        tuple of land objects
    """
    sql = ""
    # debated using TABLESAMPLE SYSTEM_ROWS() for sampling... but doesn't work with small datasets like we have now
    if land_type == None:
        sql = "SELECT land_id, s3_url, elo FROM lands ORDER BY RANDOM() LIMIT 2"
    else:
        sql = f"SELECT land_id, s3_url, elo FROM lands WHERE type = '{land_type}' ORDER BY RANDOM() LIMIT 2"
    try:
        conn, cur = connect_db()
        cur.execute(sql)
        assert cur.rowcount == 2
        psql_lands = cur.fetchall()
        land1 = psql_to_object(psql_lands[0])
        land2 = psql_to_object(psql_lands[1])
        disconnect_db(conn, cur)
        return land1, land2
    except (Exception, psql.DatabaseError) as error:
        print(error)

