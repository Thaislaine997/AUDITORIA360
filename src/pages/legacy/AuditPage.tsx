import { Container, Typography, Paper } from "@mui/material";

export default function AuditPage() {
	return (
		<Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
			<Typography variant="h4" gutterBottom>
				Auditoria
			</Typography>
			<Paper sx={{ p: 3 }}>
				<Typography variant="body1">
					Sistema de auditoria em desenvolvimento.
				</Typography>
			</Paper>
		</Container>
	);
}
