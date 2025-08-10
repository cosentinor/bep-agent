import React, { useEffect, useState } from 'react';
import { Box, Typography, Card, CardContent, Button, Chip, Grid, Alert } from '@mui/material';
import { Schedule, Add } from '@mui/icons-material';
import { useParams } from 'react-router-dom';
import api from '../../api/client';
import { useAuth } from '../../contexts/AuthContext';

const TIDP = () => {
  const { id: projectId } = useParams();
  const { user } = useAuth();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchItems();
  }, [projectId]);

  const fetchItems = async () => {
    try {
      setLoading(true);
      const res = await api.get(`/tidp/project/${projectId}`);
      const data = Array.isArray(res.data) ? { items: res.data } : res.data;
      setItems(data.items);
    } catch (e) {
      setError('Failed to load TIDP entries');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={4}>
        <Box>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Task Information Delivery Plan (TIDP)
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage project deliverables and schedules
          </Typography>
        </Box>
        {(user.role === 'admin' || user.role === 'contributor') && (
          <Button variant="contained" startIcon={<Add />}>
            Add TIDP Entry
          </Button>
        )}
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {items.map((t) => (
          <Grid item xs={12} md={6} key={t.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" fontWeight="bold" gutterBottom>
                  {t.description}
                </Typography>
                <Box display="flex" gap={1} mb={1}>
                  <Chip label={`Due: ${new Date(t.due_date).toLocaleDateString()}`} size="small" />
                  <Chip label={`Format: ${t.file_format}`} size="small" />
                </Box>
                <Chip label={t.status} size="small" />
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default TIDP;
