import { useState } from "react";
import {
	Container, Typography, Box, Paper, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Chip, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Grid, Card, CardContent, FormControl, InputLabel, Select, MenuItem, List, ListItem, ListItemText, Divider,
} from "@mui/material";
import {
	Add, Edit, Delete, FileCopy, Visibility, Description, Settings, Preview,
} from "@mui/icons-material";

interface Template {
	id: string;
	nome: string;
	descricao: string;
	categoria: "folha" | "auditoria" | "compliance" | "geral";
	campos: number;
	ultimaModificacao: string;
	status: "ativo" | "rascunho";
	utilizacoes: number;
}

export default function Templates() {
	const [openDialog, setOpenDialog] = useState(false);
	const [editingId, setEditingId] = useState<string | null>(null);
	const [previewTemplate, setPreviewTemplate] = useState<Template | null>(null);

	const [templates, setTemplates] = useState<Template[]>([
		{
			id: "1",
			nome: "Configuração Padrão - Empresa Pequena",
			descricao: "Template básico para empresas de até 50 funcionários",
			categoria: "folha",
			campos: 12,
			ultimaModificacao: "2024-01-15",
			status: "ativo",
			utilizacoes: 25,
		},
		{
			id: "2",
			nome: "Auditoria Trabalhista Completa",
			descricao: "Checklist completo para auditoria trabalhista",
			categoria: "auditoria",
			campos: 35,
			ultimaModificacao: "2024-01-12",
			status: "ativo",
			utilizacoes: 18,
		},
		{
			id: "3",
			nome: "Compliance CCT 2024",
			descricao: "Template de conformidade com CCT atualizada",
			categoria: "compliance",
			campos: 28,
			ultimaModificacao: "2024-01-10",
			status: "rascunho",
			utilizacoes: 5,
		},
	]);

	const handleEdit = (id: string) => {
		setEditingId(id);
		setOpenDialog(true);
	};

	const handleAdd = () => {
		setEditingId(null);
		setOpenDialog(true);
	};

	const handleDelete = (id: string) => {
		if (confirm("Tem certeza que deseja excluir este template?")) {
			setTemplates(prev => prev.filter(t => t.id !== id));
		}
	};

	const handleDuplicate = (template: Template) => {
		const newTemplate = {
			...template,
			id: Date.now().toString(),
			nome: `${template.nome} (Cópia)`,
			utilizacoes: 0,
			status: "rascunho" as const,
		};
		setTemplates(prev => [...prev, newTemplate]);
	};

	const getCategoryLabel = (categoria: string) => {
		switch (categoria) {
			case "folha": return "Folha de Pagamento";
			case "auditoria": return "Auditoria";
			case "compliance": return "Compliance";
			case "geral": return "Geral";
			default: return categoria;
		}
	};

	const getCategoryColor = (categoria: string) => {
		switch (categoria) {
			case "folha": return "primary";
			case "auditoria": return "secondary";
			case "compliance": return "warning";
			case "geral": return "info";
			default: return "default";
		}
	};

	const templateFields = [
		{ nome: "Razão Social", tipo: "texto", obrigatorio: true },
		{ nome: "CNPJ", tipo: "documento", obrigatorio: true },
		{ nome: "Número de Funcionários", tipo: "numero", obrigatorio: true },
		{ nome: "Setor Principal", tipo: "selecao", obrigatorio: false },
		{ nome: "Tipo de Contrato", tipo: "multipla_escolha", obrigatorio: true },
	];

	return (
		<Container maxWidth="xl">
			{/* ...restante do código igual ao legado... */}
		</Container>
	);
}
