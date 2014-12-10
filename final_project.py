import psycopg2
import ppygis

import requests

from datetime import datetime

import simplejson

from psycopg2.extras import DictCursor
from psycopg2.extensions import adapt, register_adapter, AsIs


def to_datetime(dateString):
    dt = datetime.strptime(dateString, '%Y-%m-%dT%H:%M:%S')
    return dt


conn = psycopg2.connect("dbname='dnayfeh' user='emnetg' password='gambino'")

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

query = ("https://data.cityofchicago.org/resource/ijzp-q8t2.json?"
         "$where=year%20>=%202008&$limit=50000")

raw_data = requests.get(query).json()

def insertcrime(crime):
    date = to_datetime(crime['date']).isoformat()

    cur.execute("SELECT id FROM crime_type WHERE iucr = %s;", [crime['iucr']])
    type_id = cur.fetchone()

    if type_id is None:
        try:
            cur.execute("INSERT INTO crime_type (iucr, primary_desc) VALUES (%s, %s)", (crime['iucr'], crime['primary_type']))
        except psycopg2.Error, e:
            print e.pgerror

    cur.execute("SELECT id FROM crime_type WHERE iucr = %s;", [crime['iucr']])
    type_id = cur.fetchone()[0]

    beat_id = insertbeat(crime['beat'])
    
    #geo_text = 'POINT(' + crime['location']['longitude'] + ' ' + crime['location']['latitude'] + ')'
    #print geo_text

    lat = float(crime['location']['latitude'])
    long = float(crime['location']['longitude'])
    
    point = ppygis.Point(long, lat)
    point.srid = 4326    

    try:
        cur.execute("INSERT INTO crime (crime_id, case_number, beat_id, arrest, domestic, community_area, block, year, date, fbi_code, crime_type_id, description, location, location_desc, ward) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (crime['id'], crime['case_number'], beat_id, crime['arrest'], crime['domestic'], crime['community_area'], crime['block'], crime['year'], date, crime['fbi_code'], type_id, crime['description'], point, crime.get('location_description'), crime['ward']))
    except psycopg2.Error, e:
        print e.pgerror

    print "Inserted crime id: %s" % crime['id']


def insertbeat(beat_num):
    cur.execute("SELECT id FROM beats WHERE beat_code = %s", [beat_num])
    beat_id = cur.fetchone()

    if beat_id is None:
        cur.execute("INSERT INTO beats (beat_code) VALUES (%s)", [beat_num])
        cur.execute("SELECT id FROM beats WHERE beat_code = %s", [beat_num])
        beat_id = cur.fetchone()[0]
    else:
        beat_id = beat_id[0]	
    return beat_id


try:
    cur.execute("CREATE TABLE wards (id serial PRIMARY KEY, ward_num int)")
    cur.execute("CREATE TABLE beats (id serial PRIMARY KEY, beat_code varchar)")
    cur.execute("CREATE TABLE crime_type (id serial PRIMARY KEY, iucr varchar, primary_desc varchar)")
    cur.execute("CREATE TABLE crime (crime_id int PRIMARY KEY, case_number varchar, beat_id int, arrest bool, domestic bool, community_area int, block varchar, year int, date timestamp, fbi_code varchar, crime_type_id int, description varchar, location geometry(POINT, 4326), location_desc text, ward varchar)")
    #cur.execute("ALTER TABLE communities ADD (housing_crowded numeric, households_below_poverty numeric, percent_aged_25_without_hs_diploma numeric, per_capita_income int, harship_index int)")
except psycopg2.Error, e:
    print e.pgerror


for crime in raw_data:
    if crime.get('location') is not None:
        insertcrime(crime)

conn.commit()
cur.close()
conn.close()
