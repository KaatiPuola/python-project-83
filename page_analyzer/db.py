import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def connect():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def get_urls_data():
    with connect() as connection:
        with connection.cursor as curs:
            curs.execute('SELECT * FROM urls')
            return curs.fetchall()


def get_id_by_url_name(url_name):
    with connect() as connection:
        with connection.cursor() as curs:
            curs.execute("SELECT * FROM urls WHERE name = %s", (url_name,))
            result = curs.fetchone()
            return result[0] if result else None


def add_url(url_name):
    with connect() as connection:
       with connection.cursor() as curs:
           curs.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                        (url_name, datetime.now()))
           return curs.fetchone()[0]


def get_url_by_id(url_id):
    with connect() as connection:
        with connection.cursor() as curs:
            curs.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            result = curs.fetchone()
            if result:
                return {
                    'id': result[0],
                    'name': result[1],
                    'created_at': result[2]
                }
            else:
                return None
