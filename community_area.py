import simplejson
import codecs

import psycopg2
from psycopg2.extensions import adapt, register_adapter, AsIs
import psycopg2.extras

import time
from datetime import datetime, timedelta
from email.utils import parsedate_tz


def to_datetime(dateString):
    time_tuple = parsedate_tz(dateString.strip())
    dt = datetime(*time_tuple[:6])
    return dt

conn = psycopg2.connect("dbname=dnayfeh user=dnayfeh password=rainbow")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

f = codecs.open('CommAreas.json', encoding='utf-8', mode='r').read()

# for line in f:
location = simplejson.loads(f)

for data in location['features']:
    # cur.execute("INSERT INTO community_area (id, name) VALUES (%s, %s)", (data['properties']['area_id'], data['properties']['community'],))
    for coordArray in data['geometry']['coordinates']:
        for coord in coordArray:
            cur.execute("INSERT INTO community_area (id, name, boundary_x, boundary_y) VALUES (%s, %s, %s, %s)", (data['properties']['area_id'], data['properties']['community'], coord[0], coord[1]),)
            # print data['properties']['area_id'], data['properties']['community'], coord[0], coord[1]
    conn.commit()



conn.commit()

cur.close()
conn.close()
