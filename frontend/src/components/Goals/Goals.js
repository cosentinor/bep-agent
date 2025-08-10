import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  Chip,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  Alert,
  IconButton,
} from '@mui/material';
import { Flag, Add, Delete, Edit } from '@mui/icons-material';
import { useParams } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../api/client';

const Goals = () => {
  const { id: projectId } = useParams();
  const { user } = useAuth();
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({
    description: '',
    bim_use: '',
    success_metric: '',
    priority: 'medium',
    status: 'pending',
  });

  const canEdit = user.role === 'admin' || user.role === 'contributor';

  useEffect(() => {
    fetchGoals();
  }, [projectId]);

  const fetchGoals = async () => {
    try {
      setLoading(true);
      const res = await api.get(`/goals/project/${projectId}`);
      const data = Array.isArray(res.data) ? { items: res.data } : res.data;
      setGoals(data.items);
    } catch (e) {
      setError('Failed to load goals');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async () => {
    try {
      const payload = { ...form, project_id: Number(projectId) };
      const res = await api.post('/goals', payload);
      setGoals((prev) => [res.data, ...prev]);
      setOpen(false);
      setForm({ description: '', bim_use: '', success_metric: '', priority: 'medium', status: 'pending' });
    } catch (e) {
      setError(e.response?.data?.error ? JSON.stringify(e.response.data.error) : 'Failed to create goal');
    }
  };

  const handleDelete = async (goalId) => {
    if (!window.confirm('Delete this goal?')) return;
    try {
      await api.delete(`/goals/${goalId}`);
      setGoals((prev) => prev.filter((g) => g.id !== goalId));
    } catch (e) {
      setError('Failed to delete goal');
    }
  };

  return (
    <Box>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={4}>
        <Box>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Goals & BIM Uses
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage project goals and BIM use cases
          </Typography>
        </Box>
        {canEdit && (
          <Button variant="contained" startIcon={<Add />} onClick={() => setOpen(true)}>
            Add Goal
          </Button>
        )}
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {goals.map((goal) => (
          <Grid item xs={12} md={6} key={goal.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="start" mb={1}>
                  <Typography variant="h6" fontWeight="bold">
                    {goal.bim_use}
                  </Typography>
                  {canEdit && (
                    <Box>
                      <IconButton size="small" color="error" onClick={() => handleDelete(goal.id)}>
                        <Delete fontSize="small" />
                      </IconButton>
                    </Box>
                  )}
                </Box>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {goal.description}
                </Typography>
                <Box display="flex" gap={1}>
                  <Chip label={`Priority: ${goal.priority}`} size="small" />
                  <Chip label={`Status: ${goal.status}`} size="small" />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Goal</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="BIM Use"
            value={form.bim_use}
            onChange={(e) => setForm((f) => ({ ...f, bim_use: e.target.value }))}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Description"
            value={form.description}
            onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
            margin="normal"
            multiline
            rows={3}
            required
          />
          <TextField
            fullWidth
            label="Success Metric"
            value={form.success_metric}
            onChange={(e) => setForm((f) => ({ ...f, success_metric: e.target.value }))}
            margin="normal"
          />
          <TextField
            select
            fullWidth
            label="Priority"
            value={form.priority}
            onChange={(e) => setForm((f) => ({ ...f, priority: e.target.value }))}
            margin="normal"
          >
            <MenuItem value="low">Low</MenuItem>
            <MenuItem value="medium">Medium</MenuItem>
            <MenuItem value="high">High</MenuItem>
          </TextField>
          <TextField
            select
            fullWidth
            label="Status"
            value={form.status}
            onChange={(e) => setForm((f) => ({ ...f, status: e.target.value }))}
            margin="normal"
          >
            <MenuItem value="pending">Pending</MenuItem>
            <MenuItem value="in-progress">In Progress</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
          </TextField>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleCreate}>
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Goals;
