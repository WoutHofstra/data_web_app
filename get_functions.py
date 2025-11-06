import psycopg
from google import genai
from google.genai import types


def get_functions():
	conn = psycopg.connect("dbname=dataduck user=postgres password=postgres host=localhost")
	cur = conn.cursor()

	cur.execute("SELECT id, name FROM functions;")
	rows = cur.fetchall()

	for row in rows:
		return row

	cur.close()
	conn.close()


schema_get_functions = types.FunctionDeclaration(
	name="get_functions",
	description="Returns all the rows in the functions table in the database",
)
