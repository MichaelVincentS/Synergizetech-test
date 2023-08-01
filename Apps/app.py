import os
from dotenv import load_dotenv
import psycopg2
import redis

# Load environment variables from .env file
load_dotenv()

# PostgreSQL configuration
PG_HOST = os.getenv("PG_HOST")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")

# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=PG_HOST,
    port=PG_PORT,
    user=PG_USER,
    password=PG_PASSWORD,
    database=PG_DATABASE,
)

# Connect to Redis
redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def insert_user(name, email):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))

def get_all_users():
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()

def set_user_in_redis(user_id, name, email):
    user_data = {"id": user_id, "name": name, "email": email}
    redis_conn.hmset(f"user:{user_id}", user_data)

def get_user_from_redis(user_id):
    return redis_conn.hgetall(f"user:{user_id}")

if __name__ == "__main__":
    # Example usage
    insert_user("John Doe", "john@example.com")
    insert_user("Jane Smith", "jane@example.com")

    all_users = get_all_users()
    print("All Users:")
    for user in all_users:
        print(user)

    user_id = 1
    set_user_in_redis(user_id, "John Doe", "john@example.com")
    user_data = get_user_from_redis(user_id)
    print(f"User {user_id} from Redis:", user_data)
