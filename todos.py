# todos.py
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Todo
from datetime import datetime

todos = Blueprint('todos', __name__)

@todos.route('/', methods=['GET', 'POST', 'OPTIONS'])
@jwt_required()
def manage_todos():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()

    current_user_id = get_jwt_identity()['id']

    if request.method == 'POST':
        task = request.json.get('task')
        if not task:
            return jsonify({'message': 'Task is required'}), 400
        new_todo = Todo(user_id=current_user_id, task=task)
        db.session.add(new_todo)
        db.session.commit()
        return _corsify_actual_response(jsonify(todo_to_dict(new_todo))), 201

    todos = Todo.query.filter_by(user_id=current_user_id).all()
    return _corsify_actual_response(jsonify([todo_to_dict(todo) for todo in todos])), 200

@todos.route('/<int:todo_id>', methods=['PUT', 'DELETE', 'OPTIONS'])
@jwt_required()
def modify_todo(todo_id):
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()

    current_user_id = get_jwt_identity()['id']
    todo = Todo.query.get(todo_id)

    if not todo or todo.user_id != current_user_id:
        return jsonify({'message': 'Todo not found or not authorized'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        task = data.get('task')
        completed = data.get('completed')
        if task is not None:
            todo.task = task
        if completed is not None:
            todo.completed = completed
            todo.completed_at = datetime.utcnow() if completed else None
        db.session.commit()
        return _corsify_actual_response(jsonify(todo_to_dict(todo))), 200

    if request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return _corsify_actual_response(jsonify({'message': 'Todo removed'})), 200

def todo_to_dict(todo):
    return {
        'id': todo.id,
        'task': todo.task,
        'completed': todo.completed,
        'created_at': todo.created_at.isoformat() + 'Z',  # Append 'Z' to indicate UTC
        'completed_at': todo.completed_at.isoformat() + 'Z' if todo.completed_at else None
    }

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
