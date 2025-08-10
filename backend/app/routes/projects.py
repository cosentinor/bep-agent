from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.project import Project
from models.user import User
from datetime import datetime
from marshmallow import ValidationError
from app.schemas import ProjectCreateSchema
import logging

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/', methods=['GET'])
@projects_bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user:
            logging.warning("User with ID %s not found during get_projects", user_id)
            return jsonify({'error': 'User not found'}), 404
    except Exception as exc:
        logging.exception("Error in get_projects: %s", exc)
        return jsonify({'error': 'Authentication error'}), 422

    # Pagination params
    page = max(int(request.args.get('page', 1)), 1)
    per_page = min(max(int(request.args.get('per_page', 20)), 1), 100)

    query = Project.query
    if current_user.role != 'admin':
        query = query.filter_by(owner_id=user_id)

    pagination = db.paginate(query.order_by(Project.created_at.desc()), page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [p.to_dict() for p in pagination.items],
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages,
    }), 200

@projects_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this project
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(project.to_dict()), 200

@projects_bp.route('/', methods=['POST'])
@projects_bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    try:
        user_id = get_jwt_identity()
        print(f"Create project - JWT Identity: {user_id}")
        current_user = User.query.get(user_id)
        print(f"Create project - Current user: {current_user.name if current_user else 'None'}")
        
        if not current_user:
            print(f"User with ID {user_id} not found in database")
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        print(f"Error in create_project: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Authentication error'}), 422
    
    if current_user.role not in ['admin', 'contributor']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        data = ProjectCreateSchema().load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    project = Project(
        name=data['name'],
        location=data['location'],
        client=data['client'],
        delivery_method=data.get('delivery_method', 'Design-Bid-Build'),
        description=data.get('description', ''),
        owner_id=user_id
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify(project.to_dict()), 201

@projects_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    project = Project.query.get_or_404(project_id)
    
    # Check permissions
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    if data.get('name'):
        project.name = data['name']
    if data.get('location'):
        project.location = data['location']
    if data.get('client'):
        project.client = data['client']
    if data.get('delivery_method'):
        project.delivery_method = data['delivery_method']
    if data.get('description') is not None:
        project.description = data['description']
    if data.get('status'):
        project.status = data['status']
    
    project.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(project.to_dict()), 200

@projects_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    project = Project.query.get_or_404(project_id)
    
    # Only admins or project owners can delete
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(project)
    db.session.commit()
    
    return jsonify({'message': 'Project deleted successfully'}), 200
