# final project part 1
import flask
from flask import jsonify
from flask import request, make_response
import hashlib
import creds
from sql import create_connection
from sql import execute_read_query
from sql import execute_query

app = flask.Flask(__name__) # sets up application
app.config["DEBUG"] = True # allows errors to show in browser

myCreds = creds.Creds()
conn = create_connection(myCreds.host, myCreds.user, myCreds.password, myCreds.database)


sql_floor= "SELECT * FROM floor"
floors = execute_read_query(conn,sql_floor)

sql_room = "SELECT * FROM room"
rooms = execute_read_query(conn,sql_room)

sql_resident = "SELECT * FROM resident"
residents = execute_read_query(conn,sql_resident)

masterUsername = "username"
masterPassword = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"


validTokens = {"100", "200", "300", "400"}
authorizedUsers = [
    {
        'username': 'username',
        'password': 'password',
        'token': '12345'

    },
    {
        'username': 'admin',
        'password': 'password',
        'token': '678910'
    }
]

# login and authorization code used from class notes
@app.route('/api/login', methods = ['POST'])
def login():
    req_data = request.get_json()
    username = req_data.get('username')
    password = req_data.get('password')
    
    for authuser in authorizedUsers:
        if authuser['username'] == username and authuser['password'] == password:
            return jsonify('Login successful.')
    return jsonify("Invalid user credentials."), 401

# using authorization header for postman testing
@app.route('/authenticatedroute', methods = ['GET'])
def verify_token():
    if request.authorization:
        encoded = request.authorization.password.encode()
        hashedResult = hashlib.sha256(encoded)
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return '<h1> User access authenticated. </h1>'
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login Required"'})

# Welcome page
@app.route('/home', methods = ['GET'])
def welcome_page():
    return '<h1> Welcome to Shady Grove\'s home page </h1>'



# Floor APIs
@app.route('/api/floors', methods = ['GET'])
def return_floor():
    return floors

@app.route('/api/floors/add', methods = ['POST'])
def add_floor():
    req_data = request.get_json() # json request for postman
    new_level = req_data.get('level')
    new_name =  req_data.get('name')

    sql_insert = """INSERT INTO floor (level, name) VALUES ('%s', '%s')""" % (new_level, new_name)
    execute_query(conn, sql_insert)
    return "New floor added."

# PUT: updates floor name
@app.route('/api/floors/update', methods=['PUT']) # id to change in address; syntax: http://127.0.0.1:5000/api/floors/update?id=<idtochange>
def update_floors():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error. No ID provided."
    req_data = request.get_json()
    update_column = req_data.get('name') # prompts user in postman to update floor name
    update_name = "UPDATE floor SET name = '%s' WHERE id = %s" % (update_column, id)
    execute_query(conn, update_name)
    return "Floor name updated."

# Deletes entry based on id entered
@app.route('/api/floors/delete', methods=['DELETE'])
def delete_floors():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error. No ID provided."
    idToDelete = id
    for i in range(len(floors)-1, -1, -1):
        if floors[i]['id'] == idToDelete:
            delete_query = "DELETE FROM floor WHERE id = %s" % (id)
            execute_query(conn, delete_query)
            return "Floor data removed from table."
        else:
            return "This ID does not exist."

    



# Room APIs
@app.route('/api/rooms', methods = ['GET'])
def return_room(): 
    return jsonify(rooms)

@app.route('/api/rooms/add', methods = ['POST'])
def add_rooms():
    req_data = request.get_json() # json body request for postman
    new_capacity = req_data.get('capacity')
    new_number =  req_data.get('number')
    new_floor = req_data.get('floor')

    sql_insert = """INSERT INTO room (capacity, number, floor) VALUES (%s, %s, %s)""" % (new_capacity, new_number, new_floor)
    execute_query(conn, sql_insert)
    return "New room added."

@app.route('/api/rooms/update', methods = ['PUT'])
def update_rooms():
    
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error. No ID provided."
    req_data = request.get_json() #json body 
    update_column = req_data.get('capacity') # prompts user in postman to update floor name
    update_capacity = "UPDATE room SET capacity = '%s' WHERE id = %s" % (update_column, id)
    execute_query(conn, update_capacity)
    return "Room capacity updated."

@app.route('/api/rooms/delete', methods = ['DELETE'])
def delete_rooms():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error. No ID provided."
    idToDelete = id
    for i in range(len(rooms)-1, -1, -1):
        if rooms[i]['id'] == idToDelete:
            delete_query = "DELETE FROM room WHERE id = %s" % (id)
            execute_query(conn, delete_query)
            return "Room data removed from table."
        else:
            return "This ID does not exist."



# # Resident APIs
@app.route('/api/residents', methods = ['GET'])
def return_resident():
    return residents

@app.route('/api/residents/add', methods = ['POST'])
def add_resident():
    req_data = request.get_json() # json request for postman
    new_firstname = req_data.get('firstname')
    new_lastname =  req_data.get('lastname')
    new_age = req_data.get('age')
    new_room = req_data.get('room')
    
    sql_insert = """INSERT INTO resident (firstname, lastname, age, room) VALUES ('%s', '%s', %s, %s)""" % (new_firstname, new_lastname, new_age, new_room)
    execute_query(conn, sql_insert)
    return "New resident data added."

@app.route('/api/residents/update', methods = ['PUT'])
def update_resident():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error. No ID provided."
    #functionality to update rooms if resident switches rooms
    req_data = request.get_json() #json body 
    update_column = req_data.get('room')
    new_room= "UPDATE resident SET room = '%s' WHERE id = %s" % (update_column, id)
    execute_query(conn, new_room)
    return "Resident room updated."

@app.route('/api/residents/delete', methods = ['DELETE'])
def delete_resident():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error. No ID provided."
    idToDelete = id
    for i in range(len(residents)-1, -1, -1):
        if residents[i]['id'] == idToDelete:
            delete_query = "DELETE FROM resident WHERE id = %s" % (id)
            execute_query(conn, delete_query)
            return "Resident data removed from table."
        else:
            return "This ID does not exist."

app.run()

# References
# https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/example-foreign-keys.html
# https://flask-login.readthedocs.io/en/latest/
# https://flask-httpauth.readthedocs.io/en/latest/
# https://pythonbasics.org/flask-login/
# https://stackoverflow.com/questions/65520316/for-a-rest-api-can-i-use-authentication-mechanism-provided-by-flask-login-or-do