import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Chip,
  Button,
  Grid,
  Tabs,
  Tab,
  Alert,
  Skeleton,
} from '@mui/material';
import {
  Business,
  LocationOn,
  Person,
  Schedule,
  Flag,
  Comment,
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import api from '../../api/client';

const ProjectDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    fetchProject();
  }, [id]);

  const fetchProject = async () => {
    try {
      setLoading(true);
      const response = await api.get(`/projects/${id}`);
      setProject(response.data);
    } catch (err) {
      setError('Failed to load project details');
      console.error('Error fetching project:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  if (loading) {
    return (
      <Box>
        <Skeleton variant="text" sx={{ fontSize: '2rem' }} />
        <Skeleton variant="text" />
        <Grid container spacing={3} mt={3}>
          <Grid item xs={12} md={8}>
            <Skeleton variant="rectangular" height={200} />
          </Grid>
          <Grid item xs={12} md={4}>
            <Skeleton variant="rectangular" height={200} />
          </Grid>
        </Grid>
      </Box>
    );
  }

  if (error || !project) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error || 'Project not found'}
      </Alert>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box mb={4}>
        <Typography variant="h3" fontWeight="bold" gutterBottom>
          {project.name}
        </Typography>
        <Box display="flex" alignItems="center" gap={2} mb={2}>
          <Chip
            label={project.status}
            color={project.status === 'active' ? 'success' : 'default'}
          />
          <Chip label={project.delivery_method} variant="outlined" />
        </Box>
      </Box>

      {/* Project Info Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Project Information
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <LocationOn color="action" />
                    <Typography variant="body2" color="text.secondary">
                      {project.location}
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <Person color="action" />
                    <Typography variant="body2" color="text.secondary">
                      {project.client}
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <Business color="action" />
                    <Typography variant="body2" color="text.secondary">
                      Owner: {project.owner_name}
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Box display="flex" alignItems="center" gap={1} mb={2}>
                    <Schedule color="action" />
                    <Typography variant="body2" color="text.secondary">
                      Created: {new Date(project.created_at).toLocaleDateString()}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
              {project.description && (
                <Box mt={2}>
                  <Typography variant="body2" color="text.secondary">
                    {project.description}
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight="bold" gutterBottom>
                Quick Stats
              </Typography>
              <Box display="flex" flexDirection="column" gap={2}>
                <Box display="flex" alignItems="center" gap={1}>
                  <Flag color="primary" />
                  <Typography variant="body2">
                    {project.goals_count} Goals
                  </Typography>
                </Box>
                <Box display="flex" alignItems="center" gap={1}>
                  <Schedule color="primary" />
                  <Typography variant="body2">
                    {project.tidp_count} TIDP Entries
                  </Typography>
                </Box>
                <Box display="flex" alignItems="center" gap={1}>
                  <Comment color="primary" />
                  <Typography variant="body2">
                    {project.comments_count} Comments
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Navigation Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={handleTabChange}>
          <Tab
            label="Goals & BIM Uses"
            icon={<Flag />}
            iconPosition="start"
            onClick={() => navigate(`/projects/${id}/goals`)}
          />
          <Tab
            label="TIDP Schedule"
            icon={<Schedule />}
            iconPosition="start"
            onClick={() => navigate(`/projects/${id}/tidp`)}
          />
          <Tab
            label="Comments"
            icon={<Comment />}
            iconPosition="start"
            onClick={() => navigate(`/projects/${id}/comments`)}
          />
        </Tabs>
      </Box>

      {/* Content Area */}
      <Box>
        <Typography variant="h6" gutterBottom>
          Select a tab above to view project details
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Navigate to Goals & BIM Uses, TIDP Schedule, or Comments to manage project components.
        </Typography>
      </Box>
    </Box>
  );
};

export default ProjectDetail;
