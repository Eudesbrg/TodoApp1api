
from flask import Blueprint,Response,request,json,make_response
from .db import get_db
from .auth import middleware
from .utils import build_preflight_response,build_actual_response

bp = Blueprint("todo",__name__,url_prefix='/todos')

@bp.route('/',methods=["OPTIONS"])
def preflight_response():
    response = make_response()
    return build_preflight_response(response)

@bp.route("/",methods=["GET"])
@middleware
def get_todos(email):
    # retrieve data from the database
    db = get_db()

    # check if this user exist
    user = db.execute("SELECT id FROM user WHERE email=?",(email,)).fetchone()

    todos = db.execute("SELECT * FROM todos where user_id = ?",(user["id"],)).fetchall()
    todos = [dict(todo) for todo in todos]

    res = Response(
        response=json.dumps(todos),
        status=200,
        mimetype="application/json"
    )
    return build_actual_response(res)


@bp.route('/',methods=["POST"])
@middleware
def create_todo(email):
    # retrive the user task
    message = request.json["message"]
    print(message)
    # get a connection to the user
    db = get_db()

    # check if this user exist
    user = db.execute("SELECT id FROM user WHERE email=?",(email,)).fetchone()
    user_roles = db.execute("SELECT * FROM user_role JOIN role ON user_role.role_id = role.id JOIN user ON user_role.user_id = user.id WHERE user_id = ?",(user["id"],)).fetchall()
    
    # list all user role.
    roles = [role["title"] for role in user_roles]

    # the case where the user is not possible to "create a task"
    if("create" not in roles):
        res = Response(
            response=json.dumps({"details": "user is not allowed to create a task"}),
            status=403,
            mimetype="application/json"
        )
        return build_actual_response(res)
    
    # create the task in the table
    try:
        db.execute("INSERT INTO todos (message,user_id) VALUES (?,?)",(message,user["id"]))
        db.commit()
    except:
        res = Response(
            response=json.dumps({"message": "Internal Error"}),
            status=500,
            mimetype="application/json"
        )
        return build_actual_response(res)

    res = Response(
        response=json.dumps({"details": "sucessfully created"}),
        status=201,
        mimetype="application/json"
    )
    return build_actual_response(res)


@bp.route('/',methods=["PUT"])
@middleware
def update_todo(email):
    # retrive the user task
    message = request.json["message"]
    todoId = request.json["id"]

    # get a connection to the user
    db = get_db()

    # check if this user exist
    user = db.execute("SELECT id FROM user WHERE email=?",(email,)).fetchone()
    user_roles = db.execute("SELECT * FROM user_role JOIN role ON user_role.role_id = role.id JOIN user ON user_role.user_id = user.id WHERE user_id = ?",(user["id"],)).fetchall()
    
    # list all user role.
    roles = [role["title"] for role in user_roles]

    # the case where the user can't update a task
    if("edit" not in roles):
        res = Response(
            response=json.dumps({"details": "user is not allowed to update a task"}),
            status=403,
            mimetype="application/json"
        )
        return build_actual_response(res)
    
    try:
        db.execute("UPDATE todos SET message = ? where user_id = ? AND id = ?",(message,user["id"],todoId))
        db.commit()
    except:
        res = Response(
            response=json.dumps({"message": "Internal Error"}),
            status=500,
            mimetype="application/json"
        )
        return build_actual_response(res)
    
    res = Response(
        response=json.dumps({"details": "sucessfully updated"}),
        status=200,
        mimetype="application/json"
    )
    return build_actual_response(res)


@bp.route("/",methods=["DELETE"])
@middleware
def delete_todo(email):
    # retrive the user id and the user task
    todoId = request.json["id"]

    # get a connection to the user
    db = get_db()

    # check if this user exist
    user = db.execute("SELECT id FROM user WHERE email=?",(email,)).fetchone()

    user_roles = db.execute("SELECT * FROM user_role JOIN role ON user_role.role_id = role.id JOIN user ON user_role.user_id = user.id WHERE user_id = ?",(user["id"],)).fetchall()
    
    # list all user role.
    roles = [role["title"] for role in user_roles]

    # the case where the user can't update a task
    if("delete" not in roles):
        res = Response(
            response=json.dumps({"details": "user is not allowed to delete a task"}),
            status=403,
            mimetype="application/json"
        )
        return build_actual_response(res)
    
    try:
        db.execute("DELETE from todos WHERE user_id = ? AND id = ?",(user["id"],todoId))
        db.commit()
    except Exception as e:
        res = Response(
            response=json.dumps({"message": "Internal Error"}),
            status=500,
            mimetype="application/json"
        )
        return build_actual_response(res)
    
    res = Response(
        response=json.dumps({"details": "sucessfully deleted"}),
        status=200,
        mimetype="application/json"
    )
    return build_actual_response(res)
