import os
import redis
import psycopg2
from flask import Flask, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

def check_redis_connection(host, port, password=None):
    try:
        client = redis.Redis(host=host, port=port, password=password)
        response = client.ping()
        return "Redis connection successful!" if response else "Redis connection failed."
    except Exception as e:
        return f"Redis connection error: {e}"

def check_postgres_connection(host, port, database, user, password):
    try:
        conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return "PostgreSQL connection successful!" if result and result[0] == 1 else "PostgreSQL connection failed."
    except Exception as e:
        return f"PostgreSQL connection error: {e}"

@app.route('/')
def check_connections():
    load_dotenv()
    
    # Redis configuration
    redis_host = os.getenv("REDIS_HOST")
    redis_port = int(os.getenv("REDIS_PORT"))
    redis_password = os.getenv("REDIS_PASSWORD")

    # PostgreSQL configuration
    pg_host = os.getenv("PG_HOST")
    pg_port = int(os.getenv("PG_PORT"))
    pg_database = os.getenv("PG_DATABASE")
    pg_user = os.getenv("PG_USER")
    pg_password = os.getenv("PG_PASSWORD")

    redis_result = check_redis_connection(redis_host, redis_port, redis_password)
    postgres_result = check_postgres_connection(pg_host, pg_port, pg_database, pg_user, pg_password)

    return jsonify({
        "redis_connection": redis_result,
        "postgres_connection": postgres_result
    })

if __name__ == "__main__":
    app.run(debug=True)
