import csv

import psycopg2

from psycopg2.extras import DictCursor

import codecs

import time
from datetime import datetime, timedelta
from email.utils import parsedate_tz


def to_datetime(dateString):
    time_tuple = parsedate_tz(dateString.strip())
    dt = datetime(*time_tuple[:6])
    return dt

csvfile = open('census_data_2008_2012.csv')

datareader = csv.DictReader(csvfile, delimiter=',')

conn = psycopg2.connect("dbname=dnayfeh user=emnetg password=gambino")

cur = conn.cursor()


for row in datareader:
    try:
        cur.execute("INSERT INTO community_area_info (community_area_id, housing_crowded, households_below_poverty, percent_aged_25_without_hs_diploma, per_capita_income, hardship_index) VALUES (%s, %s, %s, %s, %s, %s)", (row['Community Area Number'], row['PERCENT OF HOUSING CROWDED'], row['PERCENT HOUSEHOLDS BELOW POVERTY'], row['PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA'], row['PER CAPITA INCOME '], row['HARDSHIP INDEX']))
    except psycopg2.Error, e:
        print e.pgerror




conn.commit()
cur.close()
conn.close()
