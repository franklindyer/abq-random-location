import csv
import flask
import sqlite3

RAND_DEST_QUERY = """
    SELECT 
        destination.street_numb AS street_no,
        street.name AS street_name,
        street.type AS street_type,
        destination.street_side AS street_side,
        land_use.desc AS land_use,
        destination.lat AS lat,
        destination.lon AS lon
    FROM destination
    INNER JOIN street ON destination.street_id = street.id
    INNER JOIN land_use ON destination.land_use = land_use.code
    ORDER BY RANDOM() DESC LIMIT 1 
""" 

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_random_addr(con):
    cur = con.cursor()
    res = cur.execute(RAND_DEST_QUERY)
    return res.fetchone()

app = flask.Flask(__name__)

@app.route('/')
def index():
    con = sqlite3.connect("./abq.db")
    con.row_factory = dict_factory
    
    dst = get_random_addr(con)
    return flask.render_template('index.html', dst=dst)

app.run(port=5002)
