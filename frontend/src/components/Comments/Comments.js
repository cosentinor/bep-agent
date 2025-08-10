import React, { useEffect, useState } from 'react';
import { Box, Typography, Card, CardContent, Button, Grid, Alert, TextField } from '@mui/material';
import { Comment, Add } from '@mui/icons-material';
import { useParams } from 'react-router-dom';
import api from '../../api/client';
import { useAuth } from '../../contexts/AuthContext';

const Comments = () => {
  const { id: projectId } = useParams();
  const { user } = useAuth();
  const [items, setItems] = useState([]);
  const [text, setText] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchComments();
  }, [projectId]);

  const fetchComments = async () => {
    try {
      const res = await api.get(`/comments/project/${projectId}`);
      const data = Array.isArray(res.data) ? { items: res.data } : res.data;
      setItems(data.items);
    } catch (e) {
      setError('Failed to load comments');
    }
  };

  const addComment = async () => {
    try {
      if (!text.trim()) return;
      const res = await api.post('/comments', { project_id: Number(projectId), text: text.trim() });
      setItems((prev) => [res.data, ...prev]);
      setText('');
    } catch (e) {
      setError('Failed to add comment');
    }
  };

  return (
    <Box>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={4}>
        <Box>
          <Typography variant="h4" fontWeight="bold" gutterBottom>
            Comments & Collaboration
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage project comments and collaboration notes
          </Typography>
        </Box>
        <Box display="flex" gap={1}>
          <TextField size="small" placeholder="Write a comment..." value={text} onChange={(e) => setText(e.target.value)} />
          <Button variant="contained" startIcon={<Add />} onClick={addComment}>
            Add Comment
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Grid container spacing={2}>
        {items.map((c) => (
          <Grid item xs={12} key={c.id}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2">{c.user_name}</Typography>
                <Typography variant="caption" color="text.secondary">
                  {new Date(c.created_at).toLocaleString()}
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  {c.text}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Comments;
