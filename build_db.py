import csv
import sqlite3

con = sqlite3.connect("./abq.db")
cur = con.cursor()

land_cats = [ln.split(',') for ln in open("./data/landusecats.txt", 'r').readlines() if len(ln) > 0]
for lc in land_cats:
    cur.execute("INSERT OR IGNORE INTO land_use_cat (code, desc) VALUES (?, ?)", (int(lc[0]),lc[1],))

land_codes = [ln.split('\t') for ln in open("./data/landusecodes.txt", 'r').readlines() if len(ln) > 0]
for lc in land_codes:
    cur.execute("INSERT OR IGNORE INTO land_use (code, desc) VALUES (?, ?)", (int(lc[0]), lc[1],))

with open("./data/destinations.csv", 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in list(reader)[1:]:
        print(row)
        lu_cat = int(row[0].split('-')[0].strip())
        lat = float(row[3])
        lon = float(row[4])
        street_num = int(row[5].strip())
        street_name = row[6].strip()
        street_type = row[7].strip()
        street_quad = row[8].strip()
        street_rec = cur.execute("SELECT id FROM street WHERE name=? AND type=?", (street_name, street_type,))
        street_id = cur.fetchone()
        if street_id is None:
            cur.execute("INSERT INTO street (name, type) VALUES (?, ?)", (street_name, street_type,))
            street_id = cur.lastrowid
        else:
            street_id = street_id[0]
        cur.execute("INSERT OR IGNORE INTO destination (street_numb, street_id, street_side, land_use, lat, lon) VALUES (?, ?, ?, ?, ?, ?)", (street_num, street_id, street_quad, lu_cat, lat, lon))
        # print(lu_cat)

con.commit()
con.close()
