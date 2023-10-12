# final project part 1
import flask
from flask import jsonify
from flask import request
import creds
from sql import create_connection
from sql import execute_read_query
from sql import execute_query

#objective: GET: Return ALL animals from zoo; POST: add new animal to zoo; PUT: update column given an id; DELETE: delete an animal, given an id
app = flask.Flask(__name__) # sets up application
app.config["DEBUG"] = True # allows errors to show in browser

myCreds = creds.Creds()
conn = create_connection(myCreds.host, myCreds.user, myCreds.password, myCreds.database)

floor= "SELECT * FROM floor"
sql_floor = execute_read_query(conn,floor)

room = "SELECT * FROM room"
sql_room = execute_read_query(conn,room)

resident = "SELECT * FROM resident"
sql_resident = execute_read_query(conn,resident)

# Floor APIs
@app.route('/api/floor', methods = ['GET'])
def return_floor():
    return sql_floor

# Room APIs
@app.route('/api/room', methods = ['GET'])
def return_floor():
    return sql_room

# Resident APIs
@app.route('/api/resident', methods = ['GET'])
def return_floor():
    return sql_resident
app.run()
