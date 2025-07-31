"""
Seed data for AUDITORIA360 Blueprint features
Creates initial achievements, skills, onboarding missions, and templates
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import json

from ..models.auth_models import (
    Achievement, 
    Skill, 
    OnboardingMission, 
    NotificationPreference
)
from ..models.client_models import (
    ConfigurationTemplate,
    AIInsight
)


def seed_achievements(db: Session):
    """Seed initial achievements"""
    achievements = [
        {
            "name": "Primeiro Cliente",
            "description": "Cadastrou seu primeiro cliente no sistema",
            "icon": "first_client",
            "badge_class": "bronze",
            "xp_reward": 100,
            "criteria_type": "count",
            "criteria_target": 1,
            "criteria_resource": "clients",
        },
        {
            "name": "Mestre da Configuração", 
            "description": "Completou uma configuração completa de envio",
            "icon": "configuration_master",
            "badge_class": "silver",
            "xp_reward": 250,
            "criteria_type": "count",
            "criteria_target": 1,
            "criteria_resource": "configurations",
        },
        {
            "name": "Invencível",
            "description": "1.000 envios sem nenhuma falha!",
            "icon": "invincible",
            "badge_class": "gold",
            "xp_reward": 500,
            "criteria_type": "streak",
            "criteria_target": 1000,
            "criteria_resource": "successful_sends",
        },
        {
            "name": "Expansão Rápida",
            "description": "10 novos clientes cadastrados em uma semana!",
            "icon": "rapid_expansion",
            "badge_class": "platinum",
            "xp_reward": 750,
            "criteria_type": "time_bound_count",
            "criteria_target": 10,
            "criteria_resource": "clients_weekly",
        },
        {
            "name": "Líder de Equipe",
            "description": "Gerenciou uma equipe com sucesso",
            "icon": "team_leader",
            "badge_class": "gold",
            "xp_reward": 400,
            "criteria_type": "role",
            "criteria_target": 1,
            "criteria_resource": "team_management",
        },
        {
            "name": "Guardião da Segurança",
            "description": "Implementou todas as configurações de segurança LGPD",
            "icon": "security_guardian",
            "badge_class": "platinum",
            "xp_reward": 600,
            "criteria_type": "completion",
            "criteria_target": 100,
            "criteria_resource": "security_config",
        },
    ]
    
    for achievement_data in achievements:
        # Check if achievement already exists
        existing = db.query(Achievement).filter(
            Achievement.name == achievement_data["name"]
        ).first()
        
        if not existing:
            achievement = Achievement(**achievement_data)
            db.add(achievement)
    
    db.commit()


def seed_skills(db: Session):
    """Seed skill tree"""
    skills = [
        {
            "name": "Especialista em WhatsApp",
            "description": "Configurou 50+ clientes com envio via WhatsApp",
            "icon": "whatsapp_expert",
            "category": "Comunicação",
            "required_xp": 500,
            "required_actions": 50,
            "action_type": "whatsapp_configurations",
        },
        {
            "name": "Mago da Automação",
            "description": "Criou 5+ templates de configuração",
            "icon": "automation_wizard",
            "category": "Automação",
            "required_xp": 300,
            "required_actions": 5,
            "action_type": "templates_created",
        },
        {
            "name": "Líder de Equipe",
            "description": "Gerenciou uma equipe de 10+ pessoas",
            "icon": "team_leader",
            "category": "Liderança",
            "required_xp": 1000,
            "required_actions": 10,
            "action_type": "team_members_managed",
        },
        {
            "name": "Guardião da Segurança",
            "description": "Implementou todas as configurações de segurança",
            "icon": "security_guardian",
            "category": "Segurança",
            "required_xp": 800,
            "required_actions": 6,
            "action_type": "security_features_enabled",
        },
        {
            "name": "Especialista em Compliance",
            "description": "Resolveu 25+ anomalias de compliance",
            "icon": "compliance_expert",
            "category": "Compliance",
            "required_xp": 600,
            "required_actions": 25,
            "action_type": "anomalies_resolved",
        },
        {
            "name": "Analista de Dados",
            "description": "Criou 10+ relatórios personalizados",
            "icon": "data_analyst",
            "category": "Análise",
            "required_xp": 400,
            "required_actions": 10,
            "action_type": "reports_created",
        },
    ]
    
    for skill_data in skills:
        existing = db.query(Skill).filter(
            Skill.name == skill_data["name"]
        ).first()
        
        if not existing:
            skill = Skill(**skill_data)
            db.add(skill)
    
    db.commit()


def seed_onboarding_missions(db: Session):
    """Seed onboarding missions for different user profiles"""
    
    # Missions for Gestores (Managers)
    gestor_missions = [
        {
            "name": "Configure seu primeiro cliente",
            "description": "Aprenda a cadastrar e configurar um cliente no sistema",
            "instructions": "Clique no botão 'Cadastrar Cliente' e preencha as informações básicas. O sistema irá guiá-lo através do processo.",
            "order_sequence": 1,
            "profile_target": "gestor",
            "xp_reward": 100,
            "badge_reward": "Primeiro Cliente",
            "completion_criteria": json.dumps({"action": "client_created", "count": 1}),
            "is_optional": False,
        },
        {
            "name": "Configure a automação de envios",
            "description": "Configure o envio automático de documentos para seu cliente",
            "instructions": "Acesse a configuração do cliente e defina os documentos que devem ser enviados automaticamente e os canais de envio (Email, WhatsApp).",
            "order_sequence": 2,
            "profile_target": "gestor",
            "xp_reward": 250,
            "badge_reward": "Mestre da Configuração",
            "completion_criteria": json.dumps({"action": "automation_configured", "count": 1}),
            "is_optional": False,
        },
        {
            "name": "Convide sua equipe",
            "description": "Adicione analistas à sua equipe para colaboração",
            "instructions": "Use a área de gerenciamento de usuários para convidar analistas e definir suas permissões.",
            "order_sequence": 3,
            "profile_target": "gestor",
            "xp_reward": 150,
            "badge_reward": "Líder de Equipe",
            "completion_criteria": json.dumps({"action": "team_member_invited", "count": 1}),
            "is_optional": True,
        },
        {
            "name": "Explore o Dashboard Executivo",
            "description": "Conheça as métricas e indicadores disponíveis",
            "instructions": "Navegue pelo dashboard e personalize os widgets de acordo com suas necessidades de gestão.",
            "order_sequence": 4,
            "profile_target": "gestor",
            "xp_reward": 100,
            "badge_reward": None,
            "completion_criteria": json.dumps({"action": "dashboard_customized", "count": 1}),
            "is_optional": True,
        },
    ]
    
    # Missions for Analistas (Analysts)
    analista_missions = [
        {
            "name": "Faça seu primeiro envio",
            "description": "Aprenda a enviar documentos para um cliente",
            "instructions": "Selecione um cliente e use a funcionalidade de envio para mandar documentos via email ou WhatsApp.",
            "order_sequence": 1,
            "profile_target": "analista",
            "xp_reward": 100,
            "badge_reward": "Primeiro Envio",
            "completion_criteria": json.dumps({"action": "document_sent", "count": 1}),
            "is_optional": False,
        },
        {
            "name": "Configure destinatários",
            "description": "Adicione novos destinatários para um cliente",
            "instructions": "Acesse a configuração do cliente e adicione contatos que devem receber os documentos.",
            "order_sequence": 2,
            "profile_target": "analista", 
            "xp_reward": 150,
            "badge_reward": "Organizador",
            "completion_criteria": json.dumps({"action": "recipients_added", "count": 1}),
            "is_optional": False,
        },
        {
            "name": "Use os templates de configuração",
            "description": "Aprenda a usar templates para agilizar configurações",
            "instructions": "Explore os templates disponíveis e aplique um template adequado ao perfil do cliente.",
            "order_sequence": 3,
            "profile_target": "analista",
            "xp_reward": 200,
            "badge_reward": "Eficiência",
            "completion_criteria": json.dumps({"action": "template_applied", "count": 1}),
            "is_optional": False,
        },
        {
            "name": "Monitore os envios",
            "description": "Acompanhe o status dos envios e resolva problemas",
            "instructions": "Use a área de logs para monitorar envios e identificar possíveis falhas.",
            "order_sequence": 4,
            "profile_target": "analista",
            "xp_reward": 100,
            "badge_reward": None,
            "completion_criteria": json.dumps({"action": "logs_checked", "count": 1}),
            "is_optional": True,
        },
    ]
    
    all_missions = gestor_missions + analista_missions
    
    for mission_data in all_missions:
        existing = db.query(OnboardingMission).filter(
            OnboardingMission.name == mission_data["name"],
            OnboardingMission.profile_target == mission_data["profile_target"]
        ).first()
        
        if not existing:
            mission = OnboardingMission(**mission_data)
            db.add(mission)
    
    db.commit()


def seed_configuration_templates(db: Session):
    """Seed configuration templates for different business segments"""
    templates = [
        {
            "name": "Template para Startups",
            "description": "Configuração otimizada para startups e empresas de tecnologia",
            "business_segment": "Startups",
            "tax_regime": "Simples Nacional",
            "revenue_min": 0,
            "revenue_max": 4800000,
            "template_data": {
                "documents": ["DAS", "Declaração do Simples", "RAIS", "CAGED"],
                "channels": ["email", "whatsapp"],
                "frequency": "monthly",
                "auto_send": True,
                "notification_preferences": {
                    "send_confirmation": True,
                    "failure_alerts": True
                }
            },
            "conditional_rules": {
                "if_revenue_gt_1m": {
                    "add_documents": ["DEFIS"]
                },
                "if_employees_gt_10": {
                    "add_documents": ["RAIS_Detalhada"]
                }
            },
            "suggested_documents": ["GFIP", "DIRF"],
            "success_rate": 0.92,
            "is_active": True,
        },
        {
            "name": "Template para Varejo",
            "description": "Configuração para empresas do setor de varejo",
            "business_segment": "Varejo",
            "tax_regime": "Lucro Presumido",
            "revenue_min": 0,
            "revenue_max": 78000000,
            "template_data": {
                "documents": ["DARF", "DIPJ", "DIRF", "RAIS", "CAGED"],
                "channels": ["email"],
                "frequency": "monthly",
                "auto_send": True,
                "notification_preferences": {
                    "send_confirmation": True,
                    "failure_alerts": True
                }
            },
            "conditional_rules": {
                "if_revenue_gt_10m": {
                    "add_documents": ["ECF", "ECD"]
                }
            },
            "suggested_documents": ["GFIP", "DCTF"],
            "success_rate": 0.89,
            "is_active": True,
        },
        {
            "name": "Template para Serviços de Saúde",
            "description": "Configuração específica para clínicas e hospitais",
            "business_segment": "Serviços de Saúde",
            "tax_regime": "Lucro Real",
            "revenue_min": 0,
            "revenue_max": None,
            "template_data": {
                "documents": ["DARF", "DIPJ", "DIRF", "RAIS", "CAGED", "GFIP"],
                "channels": ["email", "system"],
                "frequency": "monthly",
                "auto_send": True,
                "special_compliance": True,
                "notification_preferences": {
                    "send_confirmation": True,
                    "failure_alerts": True,
                    "compliance_alerts": True
                }
            },
            "conditional_rules": {
                "always": {
                    "add_documents": ["Certificações_Sanitárias"]
                }
            },
            "suggested_documents": ["ANVISA_Reports", "CNS_Documents"],
            "success_rate": 0.95,
            "is_active": True,
        },
    ]
    
    for template_data in templates:
        existing = db.query(ConfigurationTemplate).filter(
            ConfigurationTemplate.name == template_data["name"]
        ).first()
        
        if not existing:
            template = ConfigurationTemplate(**template_data)
            db.add(template)
    
    db.commit()


def seed_default_notification_preferences(db: Session):
    """Create default notification preferences for existing users"""
    # This would typically be run as a migration for existing users
    users_without_preferences = db.execute(text("""
        SELECT u.id FROM users u 
        LEFT JOIN enhanced_notification_preferences enp ON u.id = enp.user_id 
        WHERE enp.user_id IS NULL
    """)).fetchall()
    
    for user_row in users_without_preferences:
        user_id = user_row[0]
        
        # Create default preferences
        default_prefs = NotificationPreference(
            user_id=user_id,
            email_enabled=True,
            email_critical_failures_only=False,
            email_digest_frequency="daily",
            notify_success_sends=False,
            notify_failure_sends=True,
            notify_client_activity=True,
            notify_configuration_changes=True,
            notify_compliance_alerts=True,
            notify_churn_risks=True,
            notify_anomaly_detection=True,
            notify_achievements=True,
            notify_system_updates=False,
            group_similar_notifications=True,
            max_notifications_per_digest=10,
            auto_dismiss_read_notifications=False,
            enable_sound_notifications=True,
            enable_desktop_notifications=True,
            preferred_sound="default"
        )
        db.add(default_prefs)
    
    db.commit()


def seed_sample_ai_insights(db: Session):
    """Seed some sample AI insights"""
    insights = [
        {
            "insight_type": "optimization",
            "title": "Oportunidade de automação detectada",
            "description": "Você pode automatizar 73% das configurações de clientes usando templates condicionais baseados no regime tributário.",
            "confidence_score": 0.87,
            "related_resource": "configuration",
            "related_resource_id": None,
            "model_version": "1.0.0",
            "generation_prompt": "Analyze configuration patterns for automation opportunities",
        },
        {
            "insight_type": "suggestion",
            "title": "Melhoria na taxa de sucesso de envios",
            "description": "Clientes que usam WhatsApp como canal secundário têm 15% menos falhas de entrega. Considere sugerir este canal para clientes com histórico de falhas por email.",
            "confidence_score": 0.92,
            "related_resource": "channel",
            "related_resource_id": None,
            "model_version": "1.0.0",
            "generation_prompt": "Analyze delivery success rates by channel",
        },
        {
            "insight_type": "summary",
            "title": "Resumo da atividade da última semana",
            "description": "Foram processados 247 envios com 94% de taxa de sucesso. 3 clientes apresentaram risco elevado de churn e 2 anomalias de compliance foram detectadas e resolvidas.",
            "confidence_score": 1.0,
            "related_resource": "activity",
            "related_resource_id": None,
            "model_version": "1.0.0",
            "generation_prompt": "Summarize weekly activity and performance",
        },
    ]
    
    # These would be generated per user, but for demo we'll leave user_id null
    for insight_data in insights:
        insight = AIInsight(**insight_data)
        db.add(insight)
    
    db.commit()


def run_all_seeds(db: Session):
    """Run all seed functions"""
    print("🌱 Seeding achievements...")
    seed_achievements(db)
    
    print("🌱 Seeding skills...")
    seed_skills(db)
    
    print("🌱 Seeding onboarding missions...")
    seed_onboarding_missions(db)
    
    print("🌱 Seeding configuration templates...")
    seed_configuration_templates(db)
    
    print("🌱 Seeding notification preferences...")
    seed_default_notification_preferences(db)
    
    print("🌱 Seeding AI insights...")
    seed_sample_ai_insights(db)
    
    print("✅ All seeds completed successfully!")


if __name__ == "__main__":
    from .models.database import SessionLocal
    
    db = SessionLocal()
    try:
        run_all_seeds(db)
    finally:
        db.close()