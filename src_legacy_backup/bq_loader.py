# Placeholder para bq_loader

class ControleFolhaLoader:
    def __init__(self, config=None):
        self.client_id = config.get('client_id') if config else 'simulado'

    def listar_todas_as_empresas(self):
        import pandas as pd
        # Retorna um DataFrame simulado
        return pd.DataFrame([
            {"empresa_id": 1, "nome": "Empresa A", "client_id": self.client_id},
            {"empresa_id": 2, "nome": "Empresa B", "client_id": self.client_id}
        ])

    def get_empresa_by_cnpj(self, cnpj):
        # Retorna um dict simulado
        if cnpj == "12345678000199":
            return {"empresa_id": 1, "nome": "Empresa A", "client_id": self.client_id, "cnpj": cnpj}
        return None
