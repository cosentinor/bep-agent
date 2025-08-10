import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Chip,
  Button,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  LinearProgress,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Business,
  Flag,
  Schedule,
  Comment,
  TrendingUp,
  TrendingDown,
  CheckCircle,
  Warning,
  Error,
  Add,
  MoreVert,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { tokens } from '../../theme/theme';
import api from '../../api/client';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    totalProjects: 0,
    activeProjects: 0,
    completedGoals: 0,
    totalGoals: 0,
    upcomingDeadlines: 0,
    overdueTasks: 0,
  });
  const [recentProjects, setRecentProjects] = useState([]);
  const [myTasks, setMyTasks] = useState([]);
  const [recentComments, setRecentComments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch projects
      const projectsResponse = await api.get('/projects');
      const { items: projects, total } = Array.isArray(projectsResponse.data)
        ? { items: projectsResponse.data, total: projectsResponse.data.length }
        : projectsResponse.data;
      
      // Fetch user's tasks if contributor or admin
      let tasks = [];
      if (user.role !== 'viewer') {
        const tasksResponse = await api.get('/tidp/my-tasks');
        const tasksPayload = Array.isArray(tasksResponse.data) ? { items: tasksResponse.data } : tasksResponse.data;
        tasks = tasksPayload.items;
      }
      
      // Calculate stats
      const activeProjects = projects.filter(p => p.status === 'active').length;
      const totalGoals = projects.reduce((sum, p) => sum + p.goals_count, 0);
      const upcomingDeadlines = tasks.filter(t => {
        const dueDate = new Date(t.due_date);
        const today = new Date();
        const diffDays = Math.ceil((dueDate - today) / (1000 * 60 * 60 * 24));
        return diffDays <= 7 && diffDays >= 0;
      }).length;
      const overdueTasks = tasks.filter(t => {
        const dueDate = new Date(t.due_date);
        const today = new Date();
        return dueDate < today && t.status !== 'completed';
      }).length;
      
      setStats({
        totalProjects: projects.length,
        activeProjects,
        completedGoals: Math.floor(totalGoals * 0.7), // Mock data
        totalGoals,
        upcomingDeadlines,
        overdueTasks,
      });
      
      setRecentProjects(projects.slice(0, 3));
      setMyTasks(tasks.slice(0, 5));
      
      // Mock recent comments
      setRecentComments([
        {
          id: 1,
          user_name: 'BIM Manager',
          text: 'Initial coordination meeting scheduled for next week.',
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          user_name: 'Design Lead',
          text: 'Structural model is 80% complete. Need input from MEP team.',
          created_at: new Date(Date.now() - 86400000).toISOString(),
        },
      ]);
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRoleBasedGreeting = () => {
    const hour = new Date().getHours();
    let timeGreeting = '';
    
    if (hour < 12) timeGreeting = 'Good morning';
    else if (hour < 18) timeGreeting = 'Good afternoon';
    else timeGreeting = 'Good evening';
    
    const roleGreeting = {
      admin: 'BIM Manager',
      contributor: 'Design Lead',
      viewer: 'Client Representative',
    };
    
    return `${timeGreeting}, ${user.name}! Welcome to your ${roleGreeting[user.role]} dashboard.`;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'success';
      case 'in-progress': return 'warning';
      case 'pending': return 'info';
      case 'overdue': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return <CheckCircle fontSize="small" />;
      case 'in-progress': return <TrendingUp fontSize="small" />;
      case 'pending': return <Schedule fontSize="small" />;
      case 'overdue': return <Error fontSize="small" />;
      default: return <Schedule fontSize="small" />;
    }
  };

  const StatCard = ({ title, value, icon, color, subtitle }) => (
    <Card
      component={motion.div}
      whileHover={{ y: -5 }}
      sx={{ height: '100%' }}
    >
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography variant="h4" fontWeight="bold" color={color}>
              {value}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {title}
            </Typography>
            {subtitle && (
              <Typography variant="caption" color="text.secondary">
                {subtitle}
              </Typography>
            )}
          </Box>
          <Avatar sx={{ bgcolor: `${color}.light`, color: `${color}.main` }}>
            {icon}
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  );

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
      },
    },
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <LinearProgress sx={{ width: '100%' }} />
      </Box>
    );
  }

  return (
    <Box component={motion.div} variants={containerVariants} initial="hidden" animate="visible">
      {/* Header */}
      <Box mb={4}>
        <Typography variant="h3" fontWeight="bold" gutterBottom>
          {getRoleBasedGreeting()}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here's what's happening with your BIM Execution Plans today.
        </Typography>
      </Box>

      {/* Stats Grid */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <motion.div variants={itemVariants}>
            <StatCard
              title="Total Projects"
              value={stats.totalProjects}
              icon={<Business />}
              color="primary"
            />
          </motion.div>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <motion.div variants={itemVariants}>
            <StatCard
              title="Active Projects"
              value={stats.activeProjects}
              icon={<TrendingUp />}
              color="success"
            />
          </motion.div>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <motion.div variants={itemVariants}>
            <StatCard
              title="Goals Completed"
              value={`${stats.completedGoals}/${stats.totalGoals}`}
              icon={<Flag />}
              color="warning"
              subtitle={`${Math.round((stats.completedGoals / stats.totalGoals) * 100)}%`}
            />
          </motion.div>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <motion.div variants={itemVariants}>
            <StatCard
              title="Upcoming Deadlines"
              value={stats.upcomingDeadlines}
              icon={<Schedule />}
              color="info"
            />
          </motion.div>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Recent Projects */}
        <Grid item xs={12} lg={8}>
          <motion.div variants={itemVariants}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
                  <Typography variant="h6" fontWeight="bold">
                    Recent Projects
                  </Typography>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => navigate('/projects')}
                  >
                    View All
                  </Button>
                </Box>
                
                <List>
                  {recentProjects.map((project, index) => (
                    <React.Fragment key={project.id}>
                      <ListItem
                        button
                        onClick={() => navigate(`/projects/${project.id}`)}
                        sx={{ borderRadius: 2, mb: 1 }}
                      >
                        <ListItemAvatar>
                          <Avatar sx={{ bgcolor: 'primary.main' }}>
                            <Business />
                          </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                          primary={project.name}
                          secondary={
                            <Box>
                              <Typography variant="body2" color="text.secondary">
                                {project.location} • {project.client}
                              </Typography>
                              <Box display="flex" gap={1} mt={1}>
                                <Chip
                                  label={project.status}
                                  size="small"
                                  color={project.status === 'active' ? 'success' : 'default'}
                                />
                                <Chip
                                  label={`${project.goals_count} Goals`}
                                  size="small"
                                  variant="outlined"
                                />
                                <Chip
                                  label={`${project.tidp_count} TIDP`}
                                  size="small"
                                  variant="outlined"
                                />
                              </Box>
                            </Box>
                          }
                        />
                        <IconButton size="small">
                          <MoreVert />
                        </IconButton>
                      </ListItem>
                      {index < recentProjects.length - 1 && <Divider />}
                    </React.Fragment>
                  ))}
                </List>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* My Tasks & Recent Comments */}
        <Grid item xs={12} lg={4}>
          <Grid container spacing={3}>
            {/* My Tasks */}
            {user.role !== 'viewer' && (
              <Grid item xs={12}>
                <motion.div variants={itemVariants}>
                  <Card>
                    <CardContent>
                      <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
                        <Typography variant="h6" fontWeight="bold">
                          My Tasks
                        </Typography>
                        <Tooltip title="Add new task">
                          <IconButton size="small">
                            <Add />
                          </IconButton>
                        </Tooltip>
                      </Box>
                      
                      {myTasks.length > 0 ? (
                        <List dense>
                          {myTasks.map((task) => (
                            <ListItem key={task.id} sx={{ px: 0 }}>
                              <ListItemText
                                primary={
                                  <Typography variant="body2" noWrap>
                                    {task.description}
                                  </Typography>
                                }
                                secondary={
                                  <Box display="flex" alignItems="center" gap={1} mt={0.5}>
                                    <Chip
                                      icon={getStatusIcon(task.status)}
                                      label={task.status}
                                      size="small"
                                      color={getStatusColor(task.status)}
                                    />
                                    <Typography variant="caption" color="text.secondary">
                                      Due: {new Date(task.due_date).toLocaleDateString()}
                                    </Typography>
                                  </Box>
                                }
                              />
                            </ListItem>
                          ))}
                        </List>
                      ) : (
                        <Typography variant="body2" color="text.secondary" textAlign="center">
                          No tasks assigned
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </motion.div>
              </Grid>
            )}

            {/* Recent Comments */}
            <Grid item xs={12}>
              <motion.div variants={itemVariants}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" fontWeight="bold" mb={3}>
                      Recent Comments
                    </Typography>
                    
                    <List dense>
                      {recentComments.map((comment) => (
                        <ListItem key={comment.id} sx={{ px: 0 }}>
                          <ListItemAvatar>
                            <Avatar sx={{ width: 32, height: 32 }}>
                              {comment.user_name.charAt(0)}
                            </Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={
                              <Typography variant="body2" fontWeight="medium">
                                {comment.user_name}
                              </Typography>
                            }
                            secondary={
                              <Box>
                                <Typography variant="body2" color="text.secondary">
                                  {comment.text}
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                  {new Date(comment.created_at).toLocaleDateString()}
                                </Typography>
                              </Box>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
