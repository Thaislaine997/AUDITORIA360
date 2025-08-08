"""
Test suite for AUDITORIA360 Phase 4 Observability and Monitoring
"""


import requests


class TestMonitoringEndpoints:
    """Test monitoring and observability endpoints"""

    BASE_URL = "http://localhost:8000"

    def test_prometheus_metrics_endpoint(self):
        """Test that Prometheus metrics endpoint returns valid data"""
        response = requests.get(f"{self.BASE_URL}/metrics")

        assert response.status_code == 200
        assert "text/plain" in response.headers.get("content-type", "")

        content = response.text
        assert "auditoria360_api_info" in content
        assert "auditorias_processadas_total" in content
        assert "usuarios_ativos_total" in content
        assert "relatorios_gerados_total" in content

    def test_business_metrics_endpoint(self):
        """Test business metrics endpoint"""
        response = requests.get(f"{self.BASE_URL}/api/v1/monitoring/business-metrics")

        assert response.status_code == 200
        data = response.json()

        # Check required business metrics
        required_metrics = [
            "auditorias_processadas",
            "usuarios_ativos",
            "relatorios_gerados",
            "compliance_score",
            "tempo_medio_processamento",
            "taxa_sucesso",
        ]

        for metric in required_metrics:
            assert metric in data
            assert isinstance(data[metric], (int, float))

    def test_monitoring_dashboard_endpoint(self):
        """Test monitoring dashboard endpoint"""
        response = requests.get(f"{self.BASE_URL}/api/v1/monitoring/dashboard")

        assert response.status_code == 200
        data = response.json()

        # Check dashboard structure
        assert "system_status" in data
        assert "metrics_summary" in data
        assert "active_alerts" in data
        assert "health_checks" in data

        assert data["system_status"] in ["healthy", "degraded", "unhealthy"]

    def test_traces_endpoint(self):
        """Test distributed tracing endpoint"""
        response = requests.get(f"{self.BASE_URL}/api/v1/monitoring/traces")

        assert response.status_code == 200
        data = response.json()

        # Should return dictionary (may be empty)
        assert isinstance(data, dict)

    def test_business_event_recording(self):
        """Test business event recording"""
        event_data = {
            "type": "audit_completed",
            "data": {
                "audit_id": "test_001",
                "audit_type": "compliance",
                "duration": 5.2,
                "status": "success",
            },
        }

        response = requests.post(
            f"{self.BASE_URL}/api/v1/monitoring/business-events", json=event_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.BASE_URL}/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "environment" in data
        assert "version" in data

    def test_system_status_endpoint(self):
        """Test system status endpoint"""
        response = requests.get(f"{self.BASE_URL}/api/v1/system/status")

        assert response.status_code == 200
        data = response.json()

        assert "api_version" in data
        assert "components" in data
        assert "monitoring" in data

        # Check components health
        components = data["components"]
        for component in ["database", "storage", "analytics", "ocr", "ai"]:
            assert component in components
            assert components[component]["status"] == "healthy"


class TestMetricsFormat:
    """Test Prometheus metrics format compliance"""

    BASE_URL = "http://localhost:8000"

    def test_prometheus_format_compliance(self):
        """Test that metrics follow Prometheus format"""
        response = requests.get(f"{self.BASE_URL}/metrics")
        lines = response.text.strip().split("\n")

        help_lines = [line for line in lines if line.startswith("# HELP")]
        type_lines = [line for line in lines if line.startswith("# TYPE")]
        metric_lines = [
            line for line in lines if not line.startswith("#") and line.strip()
        ]

        # Should have help and type comments
        assert len(help_lines) > 0
        assert len(type_lines) > 0
        assert len(metric_lines) > 0

        # Check metric line format
        for line in metric_lines:
            assert "{" in line  # Should have labels
            assert "}" in line
            parts = line.split("}")
            assert len(parts) == 2  # metric{labels} value timestamp

    def test_business_metrics_values(self):
        """Test that business metrics have reasonable values"""
        response = requests.get(f"{self.BASE_URL}/api/v1/monitoring/business-metrics")
        data = response.json()

        # Auditorias processadas should be non-negative
        assert data["auditorias_processadas"] >= 0

        # Usuários ativos should be non-negative
        assert data["usuarios_ativos"] >= 0

        # Compliance score should be between 0-100
        assert 0 <= data["compliance_score"] <= 100

        # Taxa de sucesso should be between 0-100
        assert 0 <= data["taxa_sucesso"] <= 100

        # Tempo médio should be positive
        assert data["tempo_medio_processamento"] > 0


def run_monitoring_validation():
    """Run comprehensive monitoring validation"""
    print("🔍 Validando implementação de observabilidade...")

    base_url = "http://localhost:8000"

    # Test 1: Prometheus metrics
    print("\n1. Testando endpoint de métricas Prometheus...")
    try:
        response = requests.get(f"{base_url}/metrics")
        assert response.status_code == 200
        assert "auditoria360_api_info" in response.text
        print("✅ Métricas Prometheus funcionando")
    except Exception as e:
        print(f"❌ Erro nas métricas Prometheus: {e}")

    # Test 2: Business metrics
    print("\n2. Testando métricas de negócio...")
    try:
        response = requests.get(f"{base_url}/api/v1/monitoring/business-metrics")
        data = response.json()
        assert "auditorias_processadas" in data
        print("✅ Métricas de negócio funcionando")
    except Exception as e:
        print(f"❌ Erro nas métricas de negócio: {e}")

    # Test 3: Dashboard
    print("\n3. Testando dashboard de monitoramento...")
    try:
        response = requests.get(f"{base_url}/api/v1/monitoring/dashboard")
        data = response.json()
        assert "system_status" in data
        print("✅ Dashboard de monitoramento funcionando")
    except Exception as e:
        print(f"❌ Erro no dashboard: {e}")

    # Test 4: Business event recording
    print("\n4. Testando gravação de eventos de negócio...")
    try:
        event_data = {
            "type": "audit_completed",
            "data": {"audit_id": "validation_test", "status": "success"},
        }
        response = requests.post(
            f"{base_url}/api/v1/monitoring/business-events", json=event_data
        )
        assert response.status_code == 200
        print("✅ Gravação de eventos funcionando")
    except Exception as e:
        print(f"❌ Erro na gravação de eventos: {e}")

    print("\n🎉 Validação da Fase 4 concluída!")
    print("\nPróximos passos:")
    print(
        "1. Configurar Grafana: docker-compose -f docker-compose.monitoring.yml up -d"
    )
    print("2. Acessar Grafana: http://localhost:3001 (admin/auditoria360)")
    print("3. Importar dashboards de monitoring/dashboards/")


if __name__ == "__main__":
    run_monitoring_validation()
