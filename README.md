# BIM Execution Plan (BEP) Web Application

A modern, full-stack web application for streamlining the creation and management of BIM Execution Plans. Built with React, Material-UI, and Python Flask, featuring role-based access control, real-time collaboration, and comprehensive reporting capabilities.

## 🚀 Features

### Core Functionality
- **User & Role Management**: Support for BIM Manager (admin), Contributor, and Viewer roles
- **Project Setup**: Responsive forms with real-time validation and micro-interactions
- **Goals & BIM Uses**: Input and store project goals with associated BIM uses and success metrics
- **Information Exchange Schedule (TIDP)**: CRUD interface for Task Information Delivery Plan entries
- **Collaboration Notes**: Threaded comments and notes for each project
- **Reporting & Export**: Generate PDF and CSV reports with comprehensive project data

### Design & UX
- **Modern UI**: Material-UI based design system with custom design tokens
- **Dark/Light Themes**: Seamless theme switching with localStorage persistence
- **Micro-Interactions**: Subtle animations using Framer Motion
- **Accessibility**: WCAG 2.1 AA compliant with keyboard navigation and screen reader support
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices

### Technical Features
- **Role-Based Permissions**: Granular access control based on user roles
- **Real-Time Validation**: Form validation with immediate feedback
- **Data Visualization**: Interactive charts and progress indicators
- **JWT Authentication**: Secure token-based authentication
- **RESTful API**: Clean, documented API endpoints

## 🛠️ Technology Stack

### Frontend
- **React 19** with TypeScript support
- **Material-UI (MUI)** for component library
- **Framer Motion** for animations
- **React Router** for navigation
- **Axios** for API communication
- **Recharts** for data visualization
- **Date-fns** for date manipulation

### Backend
- **Python Flask** with SQLAlchemy ORM
- **SQLite** database (easily configurable for PostgreSQL)
- **JWT** for authentication
- **Flask-CORS** for cross-origin requests
- **ReportLab** for PDF generation
- **Pandas** for data processing

## 📦 Installation & Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**:
   ```bash
   python run.py
   ```

5. **Seed demo data** (optional):
   Uncomment the `seed_database()` line in `run.py` and run again.

6. **Start the server**:
   ```bash
   python run.py
   ```
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```
   The frontend will be available at `http://localhost:3000`

## 🎨 Design System

### Design Tokens

The application uses a comprehensive design system with the following tokens:

#### Colors
- **Primary**: Blue palette (#1e88e5)
- **Secondary**: Purple palette (#8e24aa)
- **Success**: Green palette (#43a047)
- **Warning**: Orange palette (#ffb300)
- **Error**: Red palette (#e53935)
- **Grey**: Neutral palette (#757575)

#### Typography
- **Font Family**: Inter, Roboto, Helvetica, Arial
- **Headings**: Bold weights with negative letter spacing
- **Body**: Optimized line heights for readability
- **Buttons**: Medium weight, no text transform

#### Spacing
- **Base Unit**: 8px
- **Scale**: xs(4px), sm(8px), md(16px), lg(24px), xl(32px), xxl(48px)

#### Shadows
- **Small**: Subtle elevation for cards
- **Medium**: Standard elevation for buttons
- **Large**: Prominent elevation for modals
- **Extra Large**: Maximum elevation for overlays

### Theme Configuration

The application supports both light and dark themes with automatic switching:

```javascript
// Light theme features
- Light backgrounds with subtle shadows
- High contrast text
- Warm accent colors

// Dark theme features
- Dark backgrounds with enhanced shadows
- Reduced contrast for comfort
- Adjusted color palettes
```

## 🔐 Authentication & Roles

### Demo Users

The application comes with three pre-configured user accounts:

1. **BIM Manager (Admin)**
   - Email: `admin@bep.com`
   - Password: `admin123`
   - Permissions: Full access to all features

2. **Design Lead (Contributor)**
   - Email: `designer@bep.com`
   - Password: `designer123`
   - Permissions: Create/edit projects, goals, TIDP entries, comments

3. **Client Representative (Viewer)**
   - Email: `client@bep.com`
   - Password: `client123`
   - Permissions: View-only access to assigned projects

### Role Permissions

| Feature | Admin | Contributor | Viewer |
|---------|-------|-------------|--------|
| View Projects | ✅ | ✅ | ✅ |
| Create Projects | ✅ | ✅ | ❌ |
| Edit Projects | ✅ | ✅ | ❌ |
| Delete Projects | ✅ | ❌ | ❌ |
| Manage Goals | ✅ | ✅ | ❌ |
| Manage TIDP | ✅ | ✅ | ❌ |
| Add Comments | ✅ | ✅ | ✅ |
| Generate Reports | ✅ | ✅ | ✅ |
| User Management | ✅ | ❌ | ❌ |

## 📊 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user
- `GET /api/auth/users` - Get all users (admin only)

### Projects
- `GET /api/projects` - List projects
- `GET /api/projects/:id` - Get project details
- `POST /api/projects` - Create project
- `PUT /api/projects/:id` - Update project
- `DELETE /api/projects/:id` - Delete project

### Goals
- `GET /api/goals/project/:id` - Get project goals
- `POST /api/goals` - Create goal
- `PUT /api/goals/:id` - Update goal
- `DELETE /api/goals/:id` - Delete goal

### TIDP
- `GET /api/tidp/project/:id` - Get project TIDP entries
- `GET /api/tidp/my-tasks` - Get user's tasks
- `POST /api/tidp` - Create TIDP entry
- `PUT /api/tidp/:id` - Update TIDP entry
- `DELETE /api/tidp/:id` - Delete TIDP entry

### Comments
- `GET /api/comments/project/:id` - Get project comments
- `POST /api/comments` - Create comment
- `PUT /api/comments/:id` - Update comment
- `DELETE /api/comments/:id` - Delete comment

### Reports
- `GET /api/reports/project/:id/pdf` - Generate PDF report
- `GET /api/reports/project/:id/csv` - Generate CSV report

## 🎯 Key Features in Detail

### Personalized Dashboards
Each user role sees a customized dashboard:
- **BIM Managers**: Overall project health, upcoming deadlines, team performance
- **Contributors**: Personal tasks, project assignments, collaboration tools
- **Viewers**: Read-only project overview, progress tracking

### Micro-Interactions
- Button hover effects with elevation changes
- Card flip animations on save
- Smooth page transitions
- Loading states with skeleton screens
- Form validation with real-time feedback

### Accessibility Features
- Keyboard navigation support
- Screen reader labels and descriptions
- High contrast mode support
- Adjustable text sizes
- Focus indicators and skip links

### Data Visualization
- Progress indicators for goals and TIDP
- Status-based color coding
- Interactive charts (planned enhancement)
- Real-time data updates

## 🚀 Deployment

### Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=sqlite:///bep_app.db
FLASK_ENV=development
```

### Production Deployment

1. **Backend**: Deploy to Heroku, AWS, or similar platform
2. **Frontend**: Build and deploy to Netlify, Vercel, or similar
3. **Database**: Use PostgreSQL for production
4. **Environment**: Set production environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the demo credentials for testing

## 🔮 Future Enhancements

- Interactive data visualization with D3.js
- Real-time collaboration with WebSockets
- AI-powered suggestions and automation
- Mobile app with React Native
- Advanced reporting with custom templates
- Integration with BIM software APIs
- Voice commands and accessibility features
