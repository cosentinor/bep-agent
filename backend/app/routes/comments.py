from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.comment import Comment
from models.project import Project
from models.user import User
from datetime import datetime

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/project/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project_comments(project_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this project
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    # Pagination
    page = max(int(request.args.get('page', 1)), 1)
    per_page = min(max(int(request.args.get('per_page', 20)), 1), 100)
    query = Comment.query.filter_by(project_id=project_id, parent_id=None).order_by(Comment.created_at.desc())
    pagination = db.paginate(query, page=page, per_page=per_page, error_out=False)
    return jsonify({
        'items': [c.to_dict() for c in pagination.items],
        'page': pagination.page,
        'per_page': pagination.per_page,
        'total': pagination.total,
        'pages': pagination.pages,
    }), 200

@comments_bp.route('/replies/<int:comment_id>', methods=['GET'])
@jwt_required()
def get_comment_replies(comment_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    parent_comment = Comment.query.get_or_404(comment_id)
    project = Project.query.get_or_404(parent_comment.project_id)
    
    # Check if user has access to this project
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    replies = Comment.query.filter_by(parent_id=comment_id).order_by(Comment.created_at.asc()).all()
    return jsonify([reply.to_dict() for reply in replies]), 200

@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    data = request.get_json()
    
    if not data or not data.get('project_id') or not data.get('text'):
        return jsonify({'error': 'Project ID and text are required'}), 400
    
    # Check if user has access to the project
    project = Project.query.get_or_404(data['project_id'])
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    # If this is a reply, check if parent comment exists and belongs to the same project
    if data.get('parent_id'):
        parent_comment = Comment.query.get_or_404(data['parent_id'])
        if parent_comment.project_id != data['project_id']:
            return jsonify({'error': 'Parent comment does not belong to this project'}), 400
    
    comment = Comment(
        project_id=data['project_id'],
        user_id=user_id,
        text=data['text'],
        parent_id=data.get('parent_id')
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify(comment.to_dict()), 201

@comments_bp.route('/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    comment = Comment.query.get_or_404(comment_id)
    project = Project.query.get_or_404(comment.project_id)
    
    # Check permissions - only comment author or admin can edit
    if current_user.role != 'admin' and comment.user_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    # Check if user has access to the project
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    if data.get('text'):
        comment.text = data['text']
    
    comment.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(comment.to_dict()), 200

@comments_bp.route('/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    comment = Comment.query.get_or_404(comment_id)
    project = Project.query.get_or_404(comment.project_id)
    
    # Check permissions - only comment author, project owner, or admin can delete
    if current_user.role != 'admin' and comment.user_id != user_id and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    # Check if user has access to the project
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    # Delete replies first
    Comment.query.filter_by(parent_id=comment_id).delete()
    
    # Delete the comment
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment deleted successfully'}), 200
