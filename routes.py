from flask import render_template, request, redirect, url_for, flash
from flask_app import app, db
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import render_template,send_from_directory
import json
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt

from flask_app import app, db
from flask_app.models import User, Post
from flask_app.forms import PostForm

#-------------------------------------------------GENERAL HTTP CALLS------------------------------------------------------------
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/assets/<path:path>')
def send_imagetest(path):
    response = make_response(send_from_directory('templates', path))
    response.headers['Cache-Control'] = 'public,max-age=0s,must-revalidate'
    del response.headers['Expires']
    return response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/test301', methods=['GET'])
def issueredirect301():
    resp = make_response("",301)
    resp.headers['location'] = 'http://www.google.com'
    return resp

@app.route('/test302', methods=['GET'])
def issueredirect302():
    resp = make_response("",302)
    resp.headers['location'] = 'https://www.ndtv.com'
    return resp

@app.route('/captureheaders', methods=['GET'])
def captureheaders():
    headers = request.headers
    reqheadersArray = str(headers).split('\n')

    reqDict = {}
    for item in reqheadersArray:
        tempArray = item.split(':')
        print(tempArray)
        if len(tempArray) == 2:
            reqDict[tempArray[0]] = tempArray[1].strip('\r')


    responseJson = {}
    resp = make_response(jsonify(responseJson), 200)
    resp.headers['Server'] = 'TestServer'
    respheadersArray = str(resp.headers).split('\n')
    respDict = {}
    for item in respheadersArray:
        tempArray = item.split(':')
        print(tempArray)
        if len(tempArray) == 2:
            respDict[tempArray[0]] = tempArray[1].strip('\r')

    responseJson['ReqHeaders'] = reqDict
    responseJson['RespHeaders'] = respDict

    resp = make_response(jsonify(responseJson), 200)
    return resp


@app.route('/testcustommethod', methods=['KRAMER'])
def customMethod():
    resp = make_response("This is an output of Custom Method",200)
    return resp

@app.route('/testcustomstatus', methods=['GET'])
def customStatusCode():
    resp = make_response("This is an output of Custom Status Code",777)
    return resp

#-------------------------------------------------API METHODS START------------------------------------------------------------
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/todo/api/create/task', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    newtask = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    found = False
    for task in tasks:
        if task['title'] == newtask['title']:
            found = True
            abort(400,{'message': 'Already the Task Exists in the Database'})

    if found == False:
        tasks.append(newtask)
        return jsonify({'task': newtask}), 201


@app.route('/todo/api/update/task/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        print("check here 1")
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/todo/api/delete/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.route('/todo/api/list/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/todo/api/list/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/list/methods', methods=['OPTIONS'])
def get_methods():
    resp = make_response("",204)
    resp.headers['Allow'] = 'OPTIONS,GET,PUT,POST,HEAD,DELETE'
    return resp

#-------------------------------------------------DATASTREAM ENDPOINTS START------------------------------------------------------------
@app.route('/datastream', methods=['GET','POST'])
def datastreamEP():
    if request.method == 'POST':
        req_data = request.get_data()

        with open('/home/flask_app_project/flask_app/dslogs/datastream.txt', 'wb') as outfile:
            outfile.write(req_data)
        resp = jsonify(success=True)
        return resp

    if request.method == 'GET':
        resp = jsonify(success=True)
        return resp

#-------------------------------------------------CloudMonitor ENDPOINTS START------------------------------------------------------------
@app.route('/cloudmonitor', methods=['POST'])
def cloudMonEP():
    if request.method == 'POST':
        req_data = request.get_data()

        with open('/home/flask_app_project/flask_app/cmlogs/cloudmon.txt', 'wb') as outfile:
            outfile.write(req_data)
        resp = jsonify(success=True)
        return resp

#-------------------------------------------------ESI EndPoints START------------------------------------------------------------
@app.route('/esitest')
def esi():
    return render_template("esi.html")
#-------------------------------------------------ESI EndPoints END------------------------------------------------------------