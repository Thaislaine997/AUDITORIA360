import React, { useState } from "react";
import {
  Button,
  ButtonGroup,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
} from "@mui/material";
import {
  FileDownload as FileDownloadIcon,
  PictureAsPdf as PdfIcon,
  TableChart as CsvIcon,
  ExpandMore as ExpandMoreIcon,
} from "@mui/icons-material";

interface ExportButtonProps {
  onExportPdf?: () => Promise<void> | void;
  onExportCsv?: () => Promise<void> | void;
  disabled?: boolean;
  size?: "small" | "medium" | "large";
  variant?: "contained" | "outlined" | "text";
}

const ExportButton: React.FC<ExportButtonProps> = ({
  onExportPdf,
  onExportCsv,
  disabled = false,
  size = "medium",
  variant = "outlined",
}) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [exportingPdf, setExportingPdf] = useState(false);
  const [exportingCsv, setExportingCsv] = useState(false);

  const open = Boolean(anchorEl);

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleExportPdf = async () => {
    if (!onExportPdf) return;
    
    setExportingPdf(true);
    try {
      await onExportPdf();
    } catch (error) {
      console.error("Error exporting PDF:", error);
    } finally {
      setExportingPdf(false);
      handleClose();
    }
  };

  const handleExportCsv = async () => {
    if (!onExportCsv) return;
    
    setExportingCsv(true);
    try {
      await onExportCsv();
    } catch (error) {
      console.error("Error exporting CSV:", error);
    } finally {
      setExportingCsv(false);
      handleClose();
    }
  };

  // If only one export option is available, show a single button
  if (!onExportPdf && onExportCsv) {
    return (
      <Button
        variant={variant}
        size={size}
        startIcon={exportingCsv ? <CircularProgress size={16} /> : <CsvIcon />}
        onClick={handleExportCsv}
        disabled={disabled || exportingCsv}
      >
        Exportar CSV
      </Button>
    );
  }

  if (onExportPdf && !onExportCsv) {
    return (
      <Button
        variant={variant}
        size={size}
        startIcon={exportingPdf ? <CircularProgress size={16} /> : <PdfIcon />}
        onClick={handleExportPdf}
        disabled={disabled || exportingPdf}
      >
        Exportar PDF
      </Button>
    );
  }

  // If both options are available, show dropdown menu
  return (
    <>
      <ButtonGroup variant={variant} size={size}>
        <Button
          startIcon={<FileDownloadIcon />}
          onClick={handleClick}
          disabled={disabled}
          endIcon={<ExpandMoreIcon />}
        >
          Exportar
        </Button>
      </ButtonGroup>

      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "right",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
      >
        {onExportPdf && (
          <MenuItem onClick={handleExportPdf} disabled={exportingPdf}>
            <ListItemIcon>
              {exportingPdf ? <CircularProgress size={20} /> : <PdfIcon />}
            </ListItemIcon>
            <ListItemText>Exportar para PDF</ListItemText>
          </MenuItem>
        )}
        {onExportCsv && (
          <MenuItem onClick={handleExportCsv} disabled={exportingCsv}>
            <ListItemIcon>
              {exportingCsv ? <CircularProgress size={20} /> : <CsvIcon />}
            </ListItemIcon>
            <ListItemText>Exportar para CSV</ListItemText>
          </MenuItem>
        )}
      </Menu>
    </>
  );
};

export default ExportButton;