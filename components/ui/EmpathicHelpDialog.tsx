import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography } from '@mui/material';

interface EmpathicHelpDialogProps {
  open: boolean;
  onClose: () => void;
  errorContext: {
    formId: string;
    errorType: string;
    errorCount: number;
  };
}

function EmpathicHelpDialog({ open, onClose, errorContext }: EmpathicHelpDialogProps) {
  const safeContext = errorContext || { formId: '', errorType: '', errorCount: 0 };
  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Ajuda Empática</DialogTitle>
      <DialogContent>
        <Typography variant="body1">
          Ocorreu um erro do tipo <b>{safeContext.errorType}</b> no formulário <b>{safeContext.formId}</b>.
        </Typography>
        <Typography variant="body2" sx={{ mt: 2 }}>
          Número de erros consecutivos: {safeContext.errorCount}
        </Typography>
        <Typography variant="body2" sx={{ mt: 2 }}>
          Precisa de ajuda? Consulte as dicas ou peça suporte.
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Fechar</Button>
      </DialogActions>
    </Dialog>
  );
}

export default EmpathicHelpDialog;