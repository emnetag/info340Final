import simplejson
import ppygis

import codecs

import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extensions import adapt, register_adapter, AsIs

import time
from datetime import datetime, timedelta
from email.utils import parsedate_tz


def to_datetime(dateString):
    time_tuple = parsedate_tz(dateString.strip())
    dt = datetime(*time_tuple[:6])
    return dt

conn = psycopg2.connect("dbname='dnayfeh' user='emnetg' password='gambino'")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

raw_data = codecs.open('CommAreas.json', encoding='utf-8', mode='r')

def insert_community(properties, boundary):
    area_id = properties['AREA_NUMBER']
    area_name = properties['COMMUNITY']

    try:
        cur.execute("INSERT INTO community_area (id, name, boundaries) VALUES (%s, %s, ST_GeomFromGeoJSON(%s));", (area_id, area_name, simplejson.dumps(boundary)))
    except psycopg2.Error, e:
        print e.pgerror

try:
    cur.execute("SELECT AddGeometryColumn ( 'community_area', 'boundaries', 0, 'POLYGON', 2);")
except psycopg2.Error, e:
    print e.pgerror

for line in raw_data:
    community_area = simplejson.loads(line) 
    insert_community(community_area['properties'], community_area['geometry'])

conn.commit()
cur.close()
conn.close()
