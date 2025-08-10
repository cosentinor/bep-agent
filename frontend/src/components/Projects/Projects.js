import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Avatar,
  IconButton,
  Fab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Skeleton,
} from '@mui/material';
import {
  Add,
  Business,
  LocationOn,
  Person,
  Edit,
  Delete,
  Visibility,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../api/client';

const Projects = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    location: '',
    client: '',
    delivery_method: 'Design-Bid-Build',
    description: '',
  });
  const [formErrors, setFormErrors] = useState({});

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      console.log('Fetching projects...');
      const token = localStorage.getItem('token');
      console.log('Token:', token ? 'Present' : 'Missing');
      const response = await api.get('/projects');
      console.log('Projects response:', response.data);
      const data = Array.isArray(response.data) ? { items: response.data } : response.data;
      setProjects(data.items);
    } catch (err) {
      console.error('Error fetching projects:', err);
      console.error('Error response:', err.response);
      setError('Failed to load projects');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateProject = async () => {
    try {
      console.log('Creating project with data:', formData);
      const token = localStorage.getItem('token');
      console.log('Token for project creation:', token ? 'Present' : 'Missing');
      const response = await api.post('/projects', formData);
      console.log('Project created successfully:', response.data);
      setProjects(prev => [response.data, ...prev]);
      setOpenDialog(false);
      resetForm();
    } catch (err) {
      console.error('Error creating project:', err);
      console.error('Error response:', err.response);
      setFormErrors(err.response?.data?.error || {});
    }
  };

  const handleDeleteProject = async (projectId) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await api.delete(`/projects/${projectId}`);
        setProjects(prev => prev.filter(p => p.id !== projectId));
      } catch (err) {
        setError('Failed to delete project');
      }
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      location: '',
      client: '',
      delivery_method: 'Design-Bid-Build',
      description: '',
    });
    setFormErrors({});
  };

  const validateForm = () => {
    const errors = {};
    if (!formData.name) errors.name = 'Project name is required';
    if (!formData.location) errors.location = 'Location is required';
    if (!formData.client) errors.client = 'Client is required';
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      handleCreateProject();
    }
  };

  const canCreateProject = user.role === 'admin' || user.role === 'contributor';
  const canDeleteProject = user.role === 'admin';

  const ProjectCard = ({ project }) => (
    <Card
      component={motion.div}
      whileHover={{ y: -5 }}
      sx={{ height: '100%', cursor: 'pointer' }}
      onClick={() => navigate(`/projects/${project.id}`)}
    >
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
          <Avatar sx={{ bgcolor: 'primary.main' }}>
            <Business />
          </Avatar>
          <Box display="flex" gap={1}>
            <IconButton
              size="small"
              onClick={(e) => {
                e.stopPropagation();
                navigate(`/projects/${project.id}`);
              }}
            >
              <Visibility />
            </IconButton>
            {canDeleteProject && (
              <IconButton
                size="small"
                color="error"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteProject(project.id);
                }}
              >
                <Delete />
              </IconButton>
            )}
          </Box>
        </Box>

        <Typography variant="h6" fontWeight="bold" gutterBottom>
          {project.name}
        </Typography>

        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <LocationOn fontSize="small" color="action" />
          <Typography variant="body2" color="text.secondary">
            {project.location}
          </Typography>
        </Box>

        <Box display="flex" alignItems="center" gap={1} mb={2}>
          <Person fontSize="small" color="action" />
          <Typography variant="body2" color="text.secondary">
            {project.client}
          </Typography>
        </Box>

        {project.description && (
          <Typography variant="body2" color="text.secondary" mb={2}>
            {project.description.length > 100
              ? `${project.description.substring(0, 100)}...`
              : project.description}
          </Typography>
        )}

        <Box display="flex" gap={1} mb={2}>
          <Chip
            label={project.status}
            size="small"
            color={project.status === 'active' ? 'success' : 'default'}
          />
          <Chip
            label={project.delivery_method}
            size="small"
            variant="outlined"
          />
        </Box>

        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="caption" color="text.secondary">
            {project.goals_count} Goals • {project.tidp_count} TIDP
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {new Date(project.created_at).toLocaleDateString()}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Projects
        </Typography>
        <Grid container spacing={3}>
          {[1, 2, 3, 4, 5, 6].map((item) => (
            <Grid item xs={12} sm={6} md={4} key={item}>
              <Card>
                <CardContent>
                  <Skeleton variant="circular" width={40} height={40} />
                  <Skeleton variant="text" sx={{ fontSize: '1.5rem' }} />
                  <Skeleton variant="text" />
                  <Skeleton variant="text" />
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={4}>
        <Box>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Projects
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage your BIM Execution Plans
          </Typography>
        </Box>
        {canCreateProject && (
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setOpenDialog(true)}
          >
            New Project
          </Button>
        )}
      </Box>

      {/* Error Alert */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Projects Grid */}
      <AnimatePresence>
        <Grid container spacing={3}>
          {projects.map((project) => (
            <Grid item xs={12} sm={6} md={4} key={project.id}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <ProjectCard project={project} />
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </AnimatePresence>

      {/* Empty State */}
      {projects.length === 0 && !loading && (
        <Box textAlign="center" py={8}>
          <Business sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
          <Typography variant="h6" color="text.secondary" gutterBottom>
            No projects yet
          </Typography>
          <Typography variant="body2" color="text.secondary" mb={3}>
            {canCreateProject
              ? 'Create your first BIM Execution Plan to get started.'
              : 'No projects have been assigned to you yet.'}
          </Typography>
          {canCreateProject && (
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => setOpenDialog(true)}
            >
              Create First Project
            </Button>
          )}
        </Box>
      )}

      {/* Create Project Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Project</DialogTitle>
        <Box component="form" onSubmit={handleSubmit}>
          <DialogContent>
            <TextField
              fullWidth
              label="Project Name"
              name="name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              error={!!formErrors.name}
              helperText={formErrors.name}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Location"
              name="location"
              value={formData.location}
              onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              error={!!formErrors.location}
              helperText={formErrors.location}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Client"
              name="client"
              value={formData.client}
              onChange={(e) => setFormData({ ...formData, client: e.target.value })}
              error={!!formErrors.client}
              helperText={formErrors.client}
              margin="normal"
              required
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>Delivery Method</InputLabel>
              <Select
                name="delivery_method"
                value={formData.delivery_method}
                onChange={(e) => setFormData({ ...formData, delivery_method: e.target.value })}
                label="Delivery Method"
              >
                <MenuItem value="Design-Bid-Build">Design-Bid-Build</MenuItem>
                <MenuItem value="Design-Build">Design-Build</MenuItem>
                <MenuItem value="Construction Management">Construction Management</MenuItem>
                <MenuItem value="Integrated Project Delivery">Integrated Project Delivery</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Description"
              name="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              margin="normal"
              multiline
              rows={3}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
            <Button type="submit" variant="contained">
              Create Project
            </Button>
          </DialogActions>
        </Box>
      </Dialog>

      {/* Floating Action Button for Mobile */}
      {canCreateProject && (
        <Fab
          color="primary"
          aria-label="add project"
          sx={{ position: 'fixed', bottom: 16, right: 16 }}
          onClick={() => setOpenDialog(true)}
        >
          <Add />
        </Fab>
      )}
    </Box>
  );
};

export default Projects;
