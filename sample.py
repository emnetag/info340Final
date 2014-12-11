import psycopg2
import ppygis

from datetime import datetime

import simplejson

from psycopg2.extras import DictCursor
from psycopg2.extensions import adapt, register_adapter, AsIs


def to_datetime(dateString):
    dt = datetime.strptime(dateString, '%Y-%m-%dT%H:%M:%S')
    return dt


conn = psycopg2.connect("dbname='dnayfeh' user='emnetg' password='gambino'")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


cur.execute("SELECT ST_AsGeoJSON(boundaries) FROM community_area WHERE id = 34")

area_bound = cur.fetchone()

print(area_bound)