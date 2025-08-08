// src/frontend/src/components/UploadComponent.tsx

import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Box, Typography, Paper, LinearProgress, Alert } from '@mui/material';
import { CloudUpload as CloudUploadIcon } from '@mui/icons-material';
import { supabase } from '../lib/supabaseClient'; // O nosso cliente Supabase do frontend

interface UploadComponentProps {
  onUploadSuccess: (fileName: string) => void;
}

export const UploadComponent: React.FC<UploadComponentProps> = ({ onUploadSuccess }) => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    try {
      setUploading(true);
      setError(null);

      const filePath = `public/${Date.now()}_${file.name}`;

      const { error: uploadError } = await supabase.storage
        .from('documentos-legislacao') // O nome do nosso bucket
        .upload(filePath, file);

      if (uploadError) {
        throw uploadError;
      }

      onUploadSuccess(file.name);

    } catch (error: any) {
      setError(error.message);
    } finally {
      setUploading(false);
    }
  }, [onUploadSuccess]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    multiple: false,
  });

  return (
    <Box sx={{ mb: 4 }}>
      <Paper
        {...getRootProps()}
        sx={{
          p: 4,
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.300',
          backgroundColor: isDragActive ? 'primary.light' : 'background.paper',
          cursor: 'pointer',
          textAlign: 'center',
          transition: 'all 0.3s ease',
          '&:hover': {
            borderColor: 'primary.main',
            backgroundColor: 'action.hover',
          },
        }}
      >
        <input {...getInputProps()} />
        
        <CloudUploadIcon 
          sx={{ 
            fontSize: 48, 
            color: isDragActive ? 'primary.main' : 'text.secondary',
            mb: 2 
          }} 
        />
        
        {uploading ? (
          <Box>
            <Typography variant="body1" color="primary" gutterBottom>
              A enviar...
            </Typography>
            <LinearProgress sx={{ mt: 2 }} />
          </Box>
        ) : (
          <Typography variant="body1" color="text.secondary">
            {isDragActive
              ? 'Solte o PDF aqui...'
              : 'Arraste e solte um ficheiro PDF aqui, ou clique para selecionar'
            }
          </Typography>
        )}
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Box>
  );
};