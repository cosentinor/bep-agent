from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.goal import Goal
from models.project import Project
from models.user import User
from datetime import datetime
from marshmallow import ValidationError
from app.schemas import GoalCreateSchema

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_goals(project_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this project
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    page = max(int(request.args.get('page', 1)), 1)
    per_page = min(max(int(request.args.get('per_page', 50)), 1), 200)
    pagination = Goal.query.filter_by(project_id=project_id).order_by(Goal.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [g.to_dict() for g in pagination.items],
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages,
    }), 200

@goals_bp.route('/', methods=['POST'])
@jwt_required()
def create_goal():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if current_user.role not in ['admin', 'contributor']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    try:
        data = GoalCreateSchema().load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    # Check if user has access to the project
    project = Project.query.get_or_404(data['project_id'])
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    goal = Goal(
        project_id=data['project_id'],
        description=data['description'],
        bim_use=data['bim_use'],
        success_metric=data.get('success_metric', ''),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'pending')
    )
    
    db.session.add(goal)
    db.session.commit()
    
    return jsonify(goal.to_dict()), 201

@goals_bp.route('/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_goal(goal_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    goal = Goal.query.get_or_404(goal_id)
    project = Project.query.get_or_404(goal.project_id)
    
    # Check permissions
    if current_user.role not in ['admin', 'contributor']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    if data.get('description'):
        goal.description = data['description']
    if data.get('bim_use'):
        goal.bim_use = data['bim_use']
    if data.get('success_metric') is not None:
        goal.success_metric = data['success_metric']
    if data.get('priority'):
        goal.priority = data['priority']
    if data.get('status'):
        goal.status = data['status']
    
    goal.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(goal.to_dict()), 200

@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_goal(goal_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    goal = Goal.query.get_or_404(goal_id)
    project = Project.query.get_or_404(goal.project_id)
    
    # Check permissions
    if current_user.role not in ['admin', 'contributor']:
        return jsonify({'error': 'Insufficient permissions'}), 403
    
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({'message': 'Goal deleted successfully'}), 200
