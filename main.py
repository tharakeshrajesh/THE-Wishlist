import flask
import sqlite3

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = flask.Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day"],
    storage_uri="memory://",
)

conn = sqlite3.connect('wishlist.db') 
cursor = conn.cursor()  
cursor.execute('''
    CREATE TABLE IF NOT EXISTS wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        item TEXT NOT NULL
    )
''')
conn.commit()  
conn.close()

@app.get("/")
@limiter.limit("1 per 2 seconds")
def index():
    return flask.send_from_directory("static", "index.html")

@app.get("/wishlist")
@limiter.limit("1 per 2 seconds")
def wishlist():
    return flask.send_from_directory("static/wishlist", "index.html")

@app.post("/req")
@limiter.limit("1 per 1 second")
def create_gift():
    data = flask.request.get_json()
    name = data.get('name')
    item = data.get('item')

    print(item)
    
    conn = sqlite3.connect('wishlist.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO wishlist (name, item) VALUES (?, ?)', (name, item))
    conn.commit()
    conn.close()

    return '', 201
    
@app.get("/req")
@limiter.limit("1 per 1 second")
def get_wishlist_items():
    conn = sqlite3.connect('wishlist.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, item FROM wishlist')
    rows = cursor.fetchall()
    conn.close()
    
    wishlist_items = [{'id': row[0], 'name': row[1], 'item': row[2]} for row in rows]
    return flask.jsonify(wishlist_items)

if __name__ == "__main__":
    app.run()