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
    return '<h1> Welcome to our home page! </h1>'


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
    

# ---------------------------------------------------
# Room APIs
@app.route('/api/rooms', methods = ['GET'])
def return_room():
    return rooms

@app.route('/api/rooms/add', methods = ['POST'])
def add_floor():
    req_data = request.get_json() # json request for postman
    new_capacity = req_data.get('capacity')
    new_number =  req_data.get('number')
    new_floor = req_data.get('floor')

    sql_insert = """INSERT INTO room (capacity, number, floor) VALUES (%s, %s, %s)""" % (new_capacity, new_number, new_floor)
    execute_query(conn, sql_insert)
    return "New floor added."






# Resident APIs
@app.route('/api/residents', methods = ['GET'])
def return_resident():
    return residents






app.run()


# References
# https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/example-foreign-keys.html
