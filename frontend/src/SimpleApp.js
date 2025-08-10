import React, { useState, useEffect } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Card,
  CardContent,
  Button,
  TextField,
  Box,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import axios from 'axios';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
  },
});

const API_BASE = 'http://localhost:8000';

function SimpleApp() {
  const [user, setUser] = useState(null);
  const [projects, setProjects] = useState([]);
  const [loginForm, setLoginForm] = useState({ email: 'john.smith@example.com', password: 'password123' });
  const [projectForm, setProjectForm] = useState({
    name: '',
    location: '',
    client: '',
    delivery_method: 'design_build'
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [openDialog, setOpenDialog] = useState(false);

  useEffect(() => {
    if (user) {
      fetchProjects();
    }
  }, [user]);

  const fetchProjects = async () => {
    try {
      const response = await axios.get(`${API_BASE}/projects/`);
      setProjects(response.data);
    } catch (err) {
      setError('Failed to fetch projects');
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE}/auth/login`, loginForm);
      setUser(response.data.user);
      setError('');
      setSuccess('Login successful!');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE}/projects/`, projectForm);
      setOpenDialog(false);
      setProjectForm({ name: '', location: '', client: '', delivery_method: 'design_build' });
      setSuccess('Project created successfully!');
      fetchProjects();
    } catch (err) {
      setError('Failed to create project');
    }
  };

  const handleLogout = () => {
    setUser(null);
    setProjects([]);
    setSuccess('Logged out successfully');
  };

  if (!user) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Container maxWidth="sm" sx={{ mt: 8 }}>
          <Card>
            <CardContent>
              <Typography variant="h4" align="center" gutterBottom>
                🏗️ BEP Web Application
              </Typography>
              <Typography variant="h6" align="center" gutterBottom>
                Proof of Concept
              </Typography>
              
              {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
              {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

              <Box component="form" onSubmit={handleLogin}>
                <TextField
                  fullWidth
                  margin="normal"
                  label="Email"
                  type="email"
                  value={loginForm.email}
                  onChange={(e) => setLoginForm({ ...loginForm, email: e.target.value })}
                  required
                />
                <TextField
                  fullWidth
                  margin="normal"
                  label="Password"
                  type="password"
                  value={loginForm.password}
                  onChange={(e) => setLoginForm({ ...loginForm, password: e.target.value })}
                  required
                />
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
                >
                  Sign In
                </Button>
              </Box>

              <Box sx={{ mt: 3, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
                <Typography variant="body2" gutterBottom>
                  <strong>Demo Account (Pre-filled):</strong>
                </Typography>
                <Typography variant="body2">
                  Email: john.smith@example.com
                </Typography>
                <Typography variant="body2">
                  Password: password123
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  Role: BIM Manager (Full Access)
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Container>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            🏗️ BEP Web Application - Welcome, {user.name}
          </Typography>
          <Typography variant="body2" sx={{ mr: 2 }}>
            Role: {user.role.replace('_', ' ').toUpperCase()}
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4 }}>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h4">Projects Dashboard</Typography>
          {user.role === 'bim_manager' && (
            <Button variant="contained" onClick={() => setOpenDialog(true)}>
              Create New Project
            </Button>
          )}
        </Box>

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              🎯 BEP Web Application Features
            </Typography>
            <Typography variant="body2" color="text.secondary">
              This proof-of-concept demonstrates core BEP management features including project creation, 
              role-based access control, and collaborative planning tools.
            </Typography>
          </CardContent>
        </Card>

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>Project Name</strong></TableCell>
                <TableCell><strong>Location</strong></TableCell>
                <TableCell><strong>Client</strong></TableCell>
                <TableCell><strong>Delivery Method</strong></TableCell>
                <TableCell><strong>Created</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {projects.map((project) => (
                <TableRow key={project.id} hover>
                  <TableCell>{project.name}</TableCell>
                  <TableCell>{project.location}</TableCell>
                  <TableCell>{project.client}</TableCell>
                  <TableCell>{project.delivery_method.replace('_', ' ')}</TableCell>
                  <TableCell>{new Date(project.created_at).toLocaleDateString()}</TableCell>
                </TableRow>
              ))}
              {projects.length === 0 && (
                <TableRow>
                  <TableCell colSpan={5} align="center" sx={{ py: 4 }}>
                    <Typography variant="body1" color="text.secondary">
                      No projects found. {user.role === 'bim_manager' ? 'Create your first project to get started!' : 'Contact your BIM Manager to create projects.'}
                    </Typography>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>

        <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
          <DialogTitle>Create New BEP Project</DialogTitle>
          <DialogContent>
            <Box component="form" onSubmit={handleCreateProject} sx={{ mt: 1 }}>
              <TextField
                fullWidth
                margin="normal"
                label="Project Name"
                value={projectForm.name}
                onChange={(e) => setProjectForm({ ...projectForm, name: e.target.value })}
                required
                placeholder="e.g., Downtown Office Complex"
              />
              <TextField
                fullWidth
                margin="normal"
                label="Location"
                value={projectForm.location}
                onChange={(e) => setProjectForm({ ...projectForm, location: e.target.value })}
                required
                placeholder="e.g., 123 Main Street, City"
              />
              <TextField
                fullWidth
                margin="normal"
                label="Client"
                value={projectForm.client}
                onChange={(e) => setProjectForm({ ...projectForm, client: e.target.value })}
                required
                placeholder="e.g., ABC Development Corp"
              />
              <FormControl fullWidth margin="normal">
                <InputLabel>Delivery Method</InputLabel>
                <Select
                  value={projectForm.delivery_method}
                  label="Delivery Method"
                  onChange={(e) => setProjectForm({ ...projectForm, delivery_method: e.target.value })}
                >
                  <MenuItem value="design_bid_build">Design-Bid-Build</MenuItem>
                  <MenuItem value="design_build">Design-Build</MenuItem>
                  <MenuItem value="ipd">Integrated Project Delivery (IPD)</MenuItem>
                  <MenuItem value="cm_at_risk">Construction Manager at Risk</MenuItem>
                </Select>
              </FormControl>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button onClick={handleCreateProject} variant="contained">Create Project</Button>
          </DialogActions>
        </Dialog>
      </Container>
    </ThemeProvider>
  );
}

export default SimpleApp;
