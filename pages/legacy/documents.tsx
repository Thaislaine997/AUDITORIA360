import React, { useState, useEffect } from "react";
import Head from 'next/head';
import { useRouter } from 'next/router';
import {
  Container,
  Typography,
  Paper,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Chip,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import {
  Search as SearchIcon,
  CloudUpload as UploadIcon,
  Visibility as ViewIcon,
} from "@mui/icons-material";
import { authHelpers } from '../../lib/supabaseClient';

interface Document {
  id: number;
  title: string;
  category: string;
  upload_date: string;
  size: string;
  uploaded_by: string;
  status?: string;
}

export default function DocumentsPage() {
  const [user, setUser] = useState(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [filteredDocuments, setFilteredDocuments] = useState<Document[]>([]);
  const [categoryFilter, setCategoryFilter] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkUser = async () => {
      try {
        const currentUser = await authHelpers.getCurrentUser();
        if (!currentUser) {
          router.push('/login');
          return;
        }
        setUser(currentUser);
        // Mock data for now
        const mockDocs: Document[] = [
          {
            id: 1,
            title: "Relatório Mensal - Janeiro 2024",
            category: "Relatórios",
            upload_date: "2024-01-15",
            size: "2.5 MB",
            uploaded_by: "Admin",
            status: "Ativo"
          },
          {
            id: 2,
            title: "Certificado ISO 9001",
            category: "Certificações",
            upload_date: "2024-01-10",
            size: "1.2 MB",
            uploaded_by: "Admin",
            status: "Ativo"
          }
        ];
        setDocuments(mockDocs);
        setFilteredDocuments(mockDocs);
      } catch (error) {
        console.error('Error checking user:', error);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    checkUser();
  }, [router]);

  const handleSearch = (term: string) => {
    setSearchTerm(term);
    const filtered = documents.filter(doc => 
      doc.title.toLowerCase().includes(term.toLowerCase()) ||
      doc.category.toLowerCase().includes(term.toLowerCase())
    );
    setFilteredDocuments(filtered);
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography>Carregando...</Typography>
      </Container>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <>
      <Head>
        <title>Documentos - AUDITORIA360</title>
        <meta name="description" content="Gestão de documentos do AUDITORIA360" />
        <meta name="robots" content="noindex" />
      </Head>
      
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Documentos
        </Typography>
        
        <Paper sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center', flexWrap: 'wrap' }}>
            <TextField
              placeholder="Buscar documentos..."
              variant="outlined"
              size="small"
              value={searchTerm}
              onChange={(e) => handleSearch(e.target.value)}
              InputProps={{
                startAdornment: <SearchIcon color="action" />,
              }}
              sx={{ minWidth: 250 }}
            />
            
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Categoria</InputLabel>
              <Select
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                label="Categoria"
              >
                <MenuItem value="">Todas</MenuItem>
                <MenuItem value="Relatórios">Relatórios</MenuItem>
                <MenuItem value="Certificações">Certificações</MenuItem>
              </Select>
            </FormControl>
            
            <Button
              variant="contained"
              startIcon={<UploadIcon />}
              color="primary"
            >
              Upload Documento
            </Button>
          </Box>
          
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Título</TableCell>
                  <TableCell>Categoria</TableCell>
                  <TableCell>Data Upload</TableCell>
                  <TableCell>Tamanho</TableCell>
                  <TableCell>Enviado por</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredDocuments.map((doc) => (
                  <TableRow key={doc.id}>
                    <TableCell>{doc.title}</TableCell>
                    <TableCell>{doc.category}</TableCell>
                    <TableCell>{doc.upload_date}</TableCell>
                    <TableCell>{doc.size}</TableCell>
                    <TableCell>{doc.uploaded_by}</TableCell>
                    <TableCell>
                      <Chip
                        label={doc.status}
                        color="success"
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        startIcon={<ViewIcon />}
                        onClick={() => console.log('View document:', doc.id)}
                      >
                        Ver
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Container>
    </>
  );
}