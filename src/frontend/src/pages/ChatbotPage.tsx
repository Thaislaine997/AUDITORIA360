import React from "react";
import { Container, Typography, Paper } from "@mui/material";

const ChatbotPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Chatbot
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="body1">
          Sistema de chatbot em desenvolvimento.
        </Typography>
      </Paper>
    </Container>
  );
};

export default ChatbotPage;
