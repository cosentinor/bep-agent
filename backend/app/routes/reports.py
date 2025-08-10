from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.project import Project
from models.goal import Goal
from models.tidp import TIDP
from models.comment import Comment
from models.user import User
# pandas not required for current implementation; keep import only when adding dataframe based exports
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
import csv

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/project/<int:project_id>/pdf', methods=['GET'])
@jwt_required()
def generate_project_pdf(project_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this project
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20
    )
    
    # Title
    story.append(Paragraph(f"BIM Execution Plan - {project.name}", title_style))
    story.append(Spacer(1, 20))
    
    # Project Information
    story.append(Paragraph("Project Information", heading_style))
    project_info = [
        ['Project Name:', project.name],
        ['Location:', project.location],
        ['Client:', project.client],
        ['Delivery Method:', project.delivery_method],
        ['Status:', project.status],
        ['Created:', project.created_at.strftime('%B %d, %Y') if project.created_at else 'N/A']
    ]
    
    if project.description:
        project_info.append(['Description:', project.description])
    
    project_table = Table(project_info, colWidths=[2*inch, 4*inch])
    project_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(project_table)
    story.append(Spacer(1, 20))
    
    # Goals and BIM Uses
    goals = Goal.query.filter_by(project_id=project_id).all()
    if goals:
        story.append(Paragraph("Project Goals & BIM Uses", heading_style))
        goals_data = [['Description', 'BIM Use', 'Success Metric', 'Priority', 'Status']]
        for goal in goals:
            goals_data.append([
                goal.description[:50] + '...' if len(goal.description) > 50 else goal.description,
                goal.bim_use,
                goal.success_metric[:50] + '...' if len(goal.success_metric) > 50 else goal.success_metric,
                goal.priority.title(),
                goal.status.title()
            ])
        
        goals_table = Table(goals_data, colWidths=[1.5*inch, 1.2*inch, 1.5*inch, 0.8*inch, 0.8*inch])
        goals_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(goals_table)
        story.append(Spacer(1, 20))
    
    # TIDP Entries
    tidp_entries = TIDP.query.filter_by(project_id=project_id).all()
    if tidp_entries:
        story.append(Paragraph("Task Information Delivery Plan (TIDP)", heading_style))
        tidp_data = [['Description', 'Responsible', 'Due Date', 'File Format', 'Status']]
        for entry in tidp_entries:
            tidp_data.append([
                entry.description[:40] + '...' if len(entry.description) > 40 else entry.description,
                entry.responsible_user.name if entry.responsible_user else 'N/A',
                entry.due_date.strftime('%Y-%m-%d') if entry.due_date else 'N/A',
                entry.file_format,
                entry.status.title()
            ])
        
        tidp_table = Table(tidp_data, colWidths=[1.8*inch, 1.2*inch, 1*inch, 1*inch, 1*inch])
        tidp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(tidp_table)
        story.append(Spacer(1, 20))
    
    # Recent Comments
    comments = Comment.query.filter_by(project_id=project_id, parent_id=None).order_by(Comment.created_at.desc()).limit(5).all()
    if comments:
        story.append(Paragraph("Recent Comments", heading_style))
        for comment in comments:
            comment_text = f"<b>{comment.user.name}</b> - {comment.created_at.strftime('%Y-%m-%d %H:%M')}"
            story.append(Paragraph(comment_text, styles['Normal']))
            story.append(Paragraph(comment.text, styles['Normal']))
            story.append(Spacer(1, 10))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"BEP_Report_{project.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mimetype='application/pdf'
    )

@reports_bp.route('/project/<int:project_id>/csv', methods=['GET'])
@jwt_required()
def generate_project_csv(project_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this project
    if current_user.role != 'admin' and project.owner_id != user_id:
        return jsonify({'error': 'Access denied'}), 403
    
    # Create CSV buffer
    buffer = BytesIO()
    writer = csv.writer(buffer)
    
    # Project Information
    writer.writerow(['BIM Execution Plan Report'])
    writer.writerow([f'Project: {project.name}'])
    writer.writerow([f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
    writer.writerow([])
    
    writer.writerow(['Project Information'])
    writer.writerow(['Name', 'Location', 'Client', 'Delivery Method', 'Status'])
    writer.writerow([project.name, project.location, project.client, project.delivery_method, project.status])
    writer.writerow([])
    
    # Goals
    goals = Goal.query.filter_by(project_id=project_id).all()
    if goals:
        writer.writerow(['Project Goals & BIM Uses'])
        writer.writerow(['Description', 'BIM Use', 'Success Metric', 'Priority', 'Status'])
        for goal in goals:
            writer.writerow([goal.description, goal.bim_use, goal.success_metric, goal.priority, goal.status])
        writer.writerow([])
    
    # TIDP Entries
    tidp_entries = TIDP.query.filter_by(project_id=project_id).all()
    if tidp_entries:
        writer.writerow(['Task Information Delivery Plan (TIDP)'])
        writer.writerow(['Description', 'Responsible', 'Due Date', 'File Format', 'Status', 'Notes'])
        for entry in tidp_entries:
            writer.writerow([
                entry.description,
                entry.responsible_user.name if entry.responsible_user else 'N/A',
                entry.due_date.strftime('%Y-%m-%d') if entry.due_date else 'N/A',
                entry.file_format,
                entry.status,
                entry.notes or ''
            ])
        writer.writerow([])
    
    # Comments
    comments = Comment.query.filter_by(project_id=project_id, parent_id=None).order_by(Comment.created_at.desc()).all()
    if comments:
        writer.writerow(['Comments'])
        writer.writerow(['User', 'Date', 'Comment'])
        for comment in comments:
            writer.writerow([
                comment.user.name,
                comment.created_at.strftime('%Y-%m-%d %H:%M'),
                comment.text
            ])
    
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"BEP_Report_{project.name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
        mimetype='text/csv'
    )
