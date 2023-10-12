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

# masterUsername = 
# masterPassword = 

sql_floor= "SELECT * FROM floor"
floors = execute_read_query(conn,sql_floor)

sql_room = "SELECT * FROM room"
rooms = execute_read_query(conn,sql_room)

sql_resident = "SELECT * FROM resident"
residents = execute_read_query(conn,sql_resident)

# # token authentication
# @app.route('/login', methods = ['GET'])
# def auth_test():
#     if request.authorization:
#         encoded = request.authorization.password.encode #unicode encoding
#         hashedResult = hashlib.sha256(encoded) #hashing
#         if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
#             return '<h1> Authorized user access </h1>'
#     return make_response('Could not verify.', 401, {'WWW-Authenticate': 'Basic realm = "Login required."'})


# Welcome page
@app.route('/home', methods = ['GET'])
def welcome_page():
    return '<h1> Home page </h1>'


# Floor APIs
@app.route('/api/floors', methods = ['GET'])
def return_floor():
    return floors

# @app.route('/api/floor/addentry', methods=['POST'])
# def new_floor():
    




# Room APIs
@app.route('/api/rooms', methods = ['GET'])
def return_room():
    return rooms






# Resident APIs
@app.route('/api/residents', methods = ['GET'])
def return_resident():
    return residents






app.run()


# References
# https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/example-foreign-keys.html
