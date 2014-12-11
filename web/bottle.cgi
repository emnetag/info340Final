#!/usr/bin/python
# import bottle web framework
from bottle import route, run, template, debug, jinja2_view
# used to set default template folder
import functools

# import the postgres module
import psycopg2

# import goodies to make SELECT statments eaiser
# Returns values from a SELECT as a dictionary. Yay!
from psycopg2.extras import DictCursor

# Connect to the database using the dictionary cursor
# Replace your database, username, and password
# conn = psycopg2.connect("dbname= user= password=")
conn = psycopg2.connect("dbname=dnayfeh user=emnetg password=gambino")

# Create a cursor
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# set default template folder to be 'templates'
view = functools.partial(jinja2_view, template_lookup=['templates'])

# Turn on debug mode, so errors are shown in the browser
debug(True)

# Give a list of works
# URL format is /
@route('/')                                                                         
# set template file for this route (templates/works.html)
@view('communities.html')
def home():
    # Select all of the works from our databse
    cur.execute(""" 
        SELECT ca.name AS area, ca.id AS id, info.housing_crowded AS crowded, info.households_below_poverty AS poverty, 
        info.per_capita_income AS per_capita 
        FROM community_area_info info JOIN community_area ca ON ca.id = info.community_area_id
        """
    )
    # Fetch them all at once
    # We will give this list to the template so it can build a table
    communities = cur.fetchall()
    # Render the template with all of the variables
    # The template expects a dictionary of values
    return {'communities':communities}


# Give details about a work
# URL format is work/<workid>
@route('/communities/<areaid>')
# set template file for this route (templates/title.html)
@view('title.html')
def community(areaid=None):
    if areaid:
        #Get census stats for the area
        cur.execute("SELECT ca.name AS name, info.housing_crowded AS crowded, info.households_below_poverty AS poverty, info.per_capita_income AS per_capita FROM community_area_info info JOIN community_area ca on info.community_area_id = ca.id WHERE ca.id = %s;", (areaid,))
        area_info = cur.fetchone()

        cur.execute("SELECT LOWER(ct.primary_desc) AS type, count(c.crime_id) AS count FROM crime c JOIN crime_type ct ON ct.id = c.crime_type_id WHERE c.community_area = %s GROUP BY type ORDER BY count DESC LIMIT 5;", (areaid,))
        crime_types = cur.fetchall()

        return {'area_info':area_info, 'crime_types':crime_types}
    else:
        home()


run(server='cgi')