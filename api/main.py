from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from datetime import datetime
import time

# Retry DB connection
while True:
    try:
        conn = psycopg2.connect(
            host="postgres_db",
            port=5432,
            database="user_events",
            user="gakuya",
            password="secret123"
        )
        break
    except psycopg2.OperationalError:
        print("Database not ready, retrying in 2 seconds...")
        time.sleep(2)

cursor = conn.cursor()
app = FastAPI()

class Event(BaseModel):
    user_id: str
    event_type: str

@app.post("/events")
def create_event(event: Event):
    cursor.execute(
        "INSERT INTO events (user_id, event_type, event_time) VALUES (%s, %s, %s)",
        (event.user_id, event.event_type, datetime.utcnow())
    )
    conn.commit()
    return {"status": "success"}
