# Manage Serving of Images for Matchups (S3/PostgreSQL)
import psycopg2 as pg

def connect_db():
	"""
	Establish connection to postgres database

	Returns:
		tuple of postgres connection and cursor objects (conn, cur)
	"""
	dbname = "landranker-test"
	user = "postgres"
	password = "devpassword"
	host = ""
	port = 5432
	conn = pg.connect(dbname=dbname, user=user, password=password, host=host, port=port)
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
		land1 = cur.fetchone()
		cur.execute(sql2)
		assert cur.rowcount == 1
		land2 = cur.fetchone()
		disconnect_db(conn, cur)
	except (Exception, psycopg2.DatabaseError) as error:
        print(error)
	return land1, land2

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
	except (Exception, psycopg2.DatabaseError) as error:
        print(error)
	return

def add_match_result(land_id1, land_id2, result):
	"""
	Add land match result to records table

	Args:
		land_id1: integer id of land value for match
		land_id2: integer id of land value for match
		result: boolean true if land1 wins, false if land2
	"""
	sql = f"INSERT INTO records VALUES ({land_id1}, {land_id2}, {result})"
	try:
		conn, cur = connect_db()
		cur.execute(sql)
		conn.commit()
		disconnect_db(conn, cur)
	except (Exception, psycopg2.DatabaseError) as error:
        print(error)