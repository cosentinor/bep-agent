import os
from app import create_app, db
from models.user import User
from models.project import Project
from models.goal import Goal
from models.tidp import TIDP
from models.comment import Comment
from datetime import datetime, timedelta

app = create_app()

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create demo users
        admin = User(
            name='BIM Manager',
            email='admin@bep.com',
            role='admin'
        )
        admin.set_password('admin123')
        
        contributor = User(
            name='Design Lead',
            email='designer@bep.com',
            role='contributor'
        )
        contributor.set_password('designer123')
        
        viewer = User(
            name='Client Representative',
            email='client@bep.com',
            role='viewer'
        )
        viewer.set_password('client123')
        
        db.session.add_all([admin, contributor, viewer])
        db.session.commit()
        
        # Create demo projects
        project1 = Project(
            name='Downtown Office Complex',
            location='New York, NY',
            client='Metro Development Corp',
            delivery_method='Design-Build',
            description='A 25-story office complex with retail space and parking garage',
            owner_id=admin.id
        )
        
        project2 = Project(
            name='Healthcare Center',
            location='Los Angeles, CA',
            client='HealthFirst Medical',
            delivery_method='Design-Bid-Build',
            description='Modern healthcare facility with emergency services and outpatient care',
            owner_id=contributor.id
        )
        
        db.session.add_all([project1, project2])
        db.session.commit()
        
        # Create demo goals
        goals = [
            Goal(
                project_id=project1.id,
                description='Coordinate all MEP systems to avoid conflicts',
                bim_use='3D Coordination',
                success_metric='Zero clashes in final coordination model',
                priority='high',
                status='in-progress'
            ),
            Goal(
                project_id=project1.id,
                description='Create 4D construction sequence',
                bim_use='4D Scheduling',
                success_metric='Accurate construction timeline with 95% confidence',
                priority='medium',
                status='pending'
            ),
            Goal(
                project_id=project2.id,
                description='Energy analysis for LEED certification',
                bim_use='Energy Analysis',
                success_metric='LEED Gold certification achieved',
                priority='high',
                status='completed'
            )
        ]
        
        db.session.add_all(goals)
        db.session.commit()
        
        # Create demo TIDP entries
        tidp_entries = [
            TIDP(
                project_id=project1.id,
                description='Architectural model - Schematic Design',
                responsible_user_id=contributor.id,
                due_date=datetime.now().date() + timedelta(days=30),
                file_format='IFC',
                status='pending'
            ),
            TIDP(
                project_id=project1.id,
                description='Structural model - Design Development',
                responsible_user_id=contributor.id,
                due_date=datetime.now().date() + timedelta(days=45),
                file_format='IFC',
                status='in-progress'
            ),
            TIDP(
                project_id=project2.id,
                description='MEP coordination model',
                responsible_user_id=contributor.id,
                due_date=datetime.now().date() + timedelta(days=15),
                file_format='IFC',
                status='pending'
            )
        ]
        
        db.session.add_all(tidp_entries)
        db.session.commit()
        
        # Create demo comments
        comments = [
            Comment(
                project_id=project1.id,
                user_id=admin.id,
                text='Initial coordination meeting scheduled for next week. All stakeholders should review the current model.'
            ),
            Comment(
                project_id=project1.id,
                user_id=contributor.id,
                text='Structural model is 80% complete. Need input from MEP team for coordination.'
            ),
            Comment(
                project_id=project2.id,
                user_id=viewer.id,
                text='Client approval received for the healthcare center design. Proceed with detailed coordination.'
            )
        ]
        
        db.session.add_all(comments)
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    # Only seed when explicitly requested via env var
    if os.environ.get('SEED_DATABASE') == '1':
        seed_database()

    debug = os.environ.get('FLASK_DEBUG') == '1'
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_RUN_PORT', '5001'))
    app.run(debug=debug, host=host, port=port)
