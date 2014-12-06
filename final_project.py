import psycopg2

import requests

import codecs

from datetime import datetime

from psycopg2.extensions import adapt, register_adapter, AsIs


def to_datetime(dateString):
    dt = datetime.strptime(dateString, '%Y-%m-%dT%H:%M:%S')
    return dt


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y


def adapt_point(point):
    return AsIs("'(%s, %s)'" % (adapt(point.x), adapt(point.y)))


register_adapter(Point, adapt_point)

conn = psycopg2.connect("dbname='emnetg' user='emnetg' password='gambino'")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

query = ("https://data.cityofchicago.org/resource/ijzp-q8t2.json?"
         "$where=year%20>=%202008%20AND%20year%20<=%202012")

raw_data = requests.get(query).json()

f = codecs.open('CommAreas.json', encoding='utf-8', mode='r')

def insertcrime(crime):
    date = to_datetime(crime['date']).isoformat()

    cur.execute("SELECT * FROM insert_ward(%s)", (crime['ward'], ))
    ward_id = cur.fetchone()[0]

    cur.execute("SELECT * FROM insert_crime_type()")


    if crime.get('location') is not None:
        latitude = float(crime['location']['latitude'])
        longitude = float(crime['location']['longitude'])

        try:
            cur.execute("INSERT INTO final_test (crime_id, case_number, arrest, domestic, community_area, block, description, year, date, fbi_code, location, location_desc, ward) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (crime['id'], crime['case_number'], crime['arrest'], crime['domestic'], crime['community_area'], crime['block'], crime['description'], crime['year'], date, crime['fbi_code'], Point(latitude, longitude), crime['location_description'], crime['ward']))
        except psycopg2.Error, e:
            print e.pgerror
    else:

        try:
            cur.execute("INSERT INTO crimes (crime_id, case_number, arrest, domestic, community_area, block, year, date, fbi_code, crime_type_id, location_desc, ward_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (crime['id'], crime['case_number'], crime['arrest'], crime['domestic'], crime['community_area'],
                crime['block'], crime['year'], crime['date'], crime['fbi_code'], crime['iucr'], crime['location_desc'],
                ward_id))

        print "Inserted crime id: %s" % crime['id']


for crime in raw_data:
    insertcrime(crime)

conn.commit()
cur.close()
conn.close()