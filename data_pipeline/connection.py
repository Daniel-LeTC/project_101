import psycopg2
import os
from  dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

def import_csv_to_postgresql(query):
    if query is None:
        return None
    try:
        with (psycopg2.connect(
            user        =os.getenv('DB_USERNAME'),
            password    =os.getenv('DB_PASSWORD'),
            dbname      =os.getenv('DB_NAME'),
            host        =os.getenv('DB_HOST'),
            port        =os.getenv('DB_PORT'))
        as connection):
            with connection.cursor() as cursor:
                cursor.execute(query)
        return {
            "status": "OK",
            "message":"Successfully imported data from PostgreSQL"
        }

    except psycopg2.Error as e:
        return {
            "status": "ERROR",
            "state": f"{e.pgcode}",
            "message":f"{e.pgerror}"
        }
