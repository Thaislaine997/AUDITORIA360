from flask import Blueprint, request, jsonify
from src.bq_loader import ControleFolhaLoader  # Removido _global_config pois não existe
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
folhas_bp = Blueprint('folhas_routes', __name__)

# Carrega apenas de variáveis de ambiente
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
CONTROL_BQ_DATASET_ID = os.getenv('CONTROL_BQ_DATASET_ID')

loader = None
if not GCP_PROJECT_ID or not CONTROL_BQ_DATASET_ID:
    logger.error("GCP_PROJECT_ID ou CONTROL_BQ_DATASET_ID não definidos (via Env Var ou config.json) para rotas de folhas.")
else:
    try:
        loader = ControleFolhaLoader(config={
            "GCP_PROJECT_ID": GCP_PROJECT_ID,
            "CONTROL_BQ_DATASET_ID": CONTROL_BQ_DATASET_ID
        })
        logger.info(f"ControleFolhaLoader inicializado para folhas com projeto '{GCP_PROJECT_ID}' e dataset '{CONTROL_BQ_DATASET_ID}'.")
    except ValueError as e:
        logger.error(f"Erro ao inicializar ControleFolhaLoader para folhas: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado ao inicializar ControleFolhaLoader para folhas: {e}", exc_info=True)

@folhas_bp.route('', methods=['POST'])
def add_folha_route():
    if loader is None:
        return jsonify({"status": "error", "message": "Configuração do loader de folhas ausente."}), 500

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Payload JSON ausente."}), 400

    required_fields = ["id_folha", "codigo_empresa", "cnpj_empresa", "mes_ano", "status"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"status": "error", "message": f"Campos obrigatórios ausentes: {', '.join(missing_fields)}"}), 400

    try:
        # Converte datas se fornecidas
        data_envio_cliente = data.get("data_envio_cliente")
        data_guia_fgts = data.get("data_guia_fgts")
        data_darf_inss = data.get("data_darf_inss")

        folha_data = {
            "id_folha": data.get("id_folha"),
            "codigo_empresa": data.get("codigo_empresa"),
            "cnpj_empresa": data.get("cnpj_empresa"),
            "mes_ano": data.get("mes_ano"), # Espera YYYY-MM-DD como string
            "status": data.get("status"),
            "data_envio_cliente": data_envio_cliente,
            "data_guia_fgts": data_guia_fgts,
            "data_darf_inss": data_darf_inss,
            "observacoes": data.get("observacoes")
        }
        errors = loader.inserir_folha(**folha_data)
        
        if not errors:
            return jsonify({"status": "success", "message": "Folha adicionada com sucesso."}), 201
        else:
            error_messages = [err.get('message', 'Erro desconhecido do BigQuery.') for err_group in errors if 'errors' in err_group for err in err_group['errors']]
            return jsonify({"status": "error", "message": "Falha ao inserir folha.", "details": error_messages}), 400
            
    except ValueError as ve: # Erro de conversão de data ou formato de mes_ano
        logger.error(f"Erro de valor ao processar dados da folha: {ve}")
        return jsonify({"status": "error", "message": f"Erro nos dados fornecidos: {ve}"}), 400
    except Exception as e:
        logger.exception(f"Erro inesperado ao adicionar folha: {e}")
        return jsonify({"status": "error", "message": f"Erro inesperado: {str(e)}"}), 500

@folhas_bp.route('/<string:id_folha>/status', methods=['PUT'])
def update_folha_status_route(id_folha):
    if loader is None:
        return jsonify({"status": "error", "message": "Configuração do loader de folhas ausente."}), 500

    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({"status": "error", "message": "Payload JSON ausente ou campo 'status' não fornecido."}), 400

    novo_status = data['status']
    
    try:
        errors = loader.atualizar_status_folha(id_folha=id_folha, status=novo_status)
        if not errors:
            return jsonify({"status": "success", "message": f"Status da folha '{id_folha}' atualizado para '{novo_status}'."}), 200
        else:
            error_messages = [err.get('message', 'Erro desconhecido do BigQuery.') for err_group in errors if 'errors' in err_group for err in err_group['errors']]
            return jsonify({"status": "error", "message": "Falha ao atualizar status da folha.", "details": error_messages}), 400
    except Exception as e:
        logger.exception(f"Erro inesperado ao atualizar status da folha {id_folha}: {e}")
        return jsonify({"status": "error", "message": f"Erro inesperado: {str(e)}"}), 500

@router.get("/exemplo", response_model=None)
async def exemplo(request: Request = Depends()):
    ...