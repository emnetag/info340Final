import simplejson

import codecs

import psycopg2
from psycopg2.extensions import adapt, register_adapter, AsIs

import time
from datetime import datetime, timedelta
from email.utils import parsedate_tz


def to_datetime(dateString):
    time_tuple = parsedate_tz(dateString.strip())
    dt = datetime(*time_tuple[:6])
    return dt

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def adapt_point(point):
    return AsIs("'(%s, %s)'" % (adapt(point.x), adapt(point.y)))

register_adapter(Point, adapt_point)

class Polygon:
    def __init__(self):
        self.vertices = [ ]
    def add_point(self, point):
        self.vertices.append(point)

raw_data = codecs.open('CommAreas.json', mode='r')

for line in raw_data:
    area = simplejson.loads(line)