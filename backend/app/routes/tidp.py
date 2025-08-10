from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.tidp import TIDP
from models.project import Project
from models.user import User
from datetime import datetime
from marshmallow import ValidationError
from app.schemas import TIDPCreateSchema

tidp_bp = Blueprint('tidp', __name__)

@tidp_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_tidp(project_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this project
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    page = max(int(request.args.get('page', 1)), 1)
    per_page = min(max(int(request.args.get('per_page', 50)), 1), 200)
    query = TIDP.query.filter_by(project_id=project_id).order_by(TIDP.due_date.asc())
    pagination = db.paginate(query, page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [e.to_dict() for e in pagination.items],
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages,
    }), 200

@tidp_bp.route('/my-tasks', methods=['GET'])
@jwt_required()
def get_my_tasks():
    user_id = get_jwt_identity()
    page = max(int(request.args.get('page', 1)), 1)
    per_page = min(max(int(request.args.get('per_page', 50)), 1), 200)
    query = TIDP.query.filter_by(responsible_user_id=user_id).order_by(TIDP.due_date.asc())
    pagination = db.paginate(query, page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [e.to_dict() for e in pagination.items],
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages,
    }), 200

@tidp_bp.route('/', methods=['POST'])
@jwt_required()
def create_tidp():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if current_user.role not in ['admin', 'contributor']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        data = TIDPCreateSchema().load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    # Check if user has access to the project
    project = Project.query.get_or_404(data['project_id'])
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    due_date = data['due_date']
    
    tidp_entry = TIDP(
        project_id=data['project_id'],
        description=data['description'],
        responsible_user_id=data.get('responsible_user_id') or user_id,
        due_date=due_date,
        file_format=data.get('file_format', 'IFC'),
        status=data.get('status', 'pending'),
        notes=data.get('notes', '')
    )
    
    db.session.add(tidp_entry)
    db.session.commit()
    
    return jsonify(tidp_entry.to_dict()), 201

@tidp_bp.route('/<int:tidp_id>', methods=['PUT'])
@jwt_required()
def update_tidp(tidp_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    tidp_entry = TIDP.query.get_or_404(tidp_id)
    project = Project.query.get_or_404(tidp_entry.project_id)
    
    # Check permissions
    if current_user.role not in ['admin', 'contributor']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    if current_user.role != 'admin' and project.owner_id != user_id and tidp_entry.responsible_user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    if data.get('description'):
        tidp_entry.description = data['description']
    if data.get('responsible_user_id'):
        tidp_entry.responsible_user_id = data['responsible_user_id']
    if data.get('due_date'):
        try:
            due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
            tidp_entry.due_date = due_date
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    if data.get('file_format'):
        tidp_entry.file_format = data['file_format']
    if data.get('status'):
        tidp_entry.status = data['status']
    if data.get('notes') is not None:
        tidp_entry.notes = data['notes']
    
    tidp_entry.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(tidp_entry.to_dict()), 200

@tidp_bp.route('/<int:tidp_id>', methods=['DELETE'])
@jwt_required()
def delete_tidp(tidp_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    tidp_entry = TIDP.query.get_or_404(tidp_id)
    project = Project.query.get_or_404(tidp_entry.project_id)
    
    # Check permissions
    if current_user.role not in ['admin', 'contributor']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(tidp_entry)
    db.session.commit()
    
    return jsonify({'message': 'TIDP entry deleted successfully'}), 200
