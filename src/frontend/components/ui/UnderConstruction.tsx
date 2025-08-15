import React from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
} from "@mui/material";
import {
  Construction,
  Schedule,
  Star,
  Lightbulb,
} from "@mui/icons-material";

interface UnderConstructionProps {
  title: string;
  description: string;
  features?: string[];
  estimatedDate?: string;
}

const UnderConstruction: React.FC<UnderConstructionProps> = ({
  title,
  description,
  features = [],
  estimatedDate,
}) => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 8, textAlign: "center" }}>
        <Paper
          elevation={0}
          sx={{
            p: 6,
            borderRadius: 3,
            bgcolor: "background.paper",
            border: "1px solid",
            borderColor: "divider",
          }}
        >
          <Construction
            sx={{
              fontSize: 80,
              color: "primary.main",
              mb: 3,
            }}
          />
          
          <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
            {title}
          </Typography>
          
          <Typography
            variant="h6"
            color="text.secondary"
            sx={{ mb: 4, maxWidth: 600, mx: "auto" }}
          >
            {description}
          </Typography>

          <Chip
            icon={<Construction />}
            label="Em Desenvolvimento"
            color="warning"
            variant="outlined"
            sx={{ mb: 4, fontSize: "1rem", py: 2, px: 1 }}
          />

          {features.length > 0 && (
            <Box sx={{ mt: 5 }}>
              <Typography variant="h5" gutterBottom sx={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 1 }}>
                <Lightbulb color="primary" />
                Funcionalidades Planejadas
              </Typography>
              
              <Grid container spacing={2} sx={{ mt: 2 }}>
                {features.map((feature, index) => (
                  <Grid item xs={12} md={6} key={index}>
                    <Card variant="outlined" sx={{ height: "100%" }}>
                      <CardContent>
                        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                          <Star color="primary" fontSize="small" />
                          <Typography variant="body1" fontWeight={500}>
                            {feature}
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </Box>
          )}

          {estimatedDate && (
            <Box sx={{ mt: 4, display: "flex", alignItems: "center", justifyContent: "center", gap: 1 }}>
              <Schedule color="info" />
              <Typography variant="body1" color="text.secondary">
                Previsão de lançamento: <strong>{estimatedDate}</strong>
              </Typography>
            </Box>
          )}

          <Box sx={{ mt: 5 }}>
            <Button
              variant="outlined"
              color="primary"
              size="large"
              onClick={() => window.history.back()}
            >
              Voltar
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default UnderConstruction;