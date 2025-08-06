"""
Test Suite para Validação Quântica - AUDITORIA360
Testes automatizados para validar o Sistema Nervoso Descentralizado
e Fogo de Artifício de Funções Serverless.
"""

import pytest
import asyncio
import time
from pathlib import Path
import tempfile
import pandas as pd
import json

# Import dos módulos serverless
from src.serverless.decentralized_data import DecentralizedDataNervousSystem
from src.serverless.function_fireworks import ServerlessFunctionFireworks
from src.serverless.cold_start_predictor import ColdStartPredictor
from src.serverless.quantum_orchestrator import QuantumValidationOrchestrator


class TestDecentralizedDataNervousSystem:
    """Testes para o Sistema Nervoso de Dados Descentralizado."""
    
    @pytest.fixture
    def nervous_system(self):
        """Fixture para instanciar o sistema nervoso."""
        return DecentralizedDataNervousSystem()
    
    def test_create_optimized_parquet_dataset(self, nervous_system):
        """Testa criação de dataset Parquet otimizado."""
        dataset_info = nervous_system.create_optimized_parquet_dataset(
            "test_dataset", size_gb=0.1  # Pequeno para teste
        )
        
        assert dataset_info['name'] == "test_dataset"
        assert dataset_info['version'] == 1
        assert len(dataset_info['partitions']) > 0
        assert dataset_info['creation_time_seconds'] > 0
        
        # Verificar se partições foram criadas
        for partition in dataset_info['partitions']:
            assert partition['records_count'] > 0
            assert partition['size_bytes'] > 0
            if 'local_path' in partition:
                assert Path(partition['local_path']).exists()
    
    @pytest.mark.asyncio
    async def test_execute_distributed_query(self, nervous_system):
        """Testa execução de consulta distribuída."""
        # Criar dataset primeiro
        dataset_info = nervous_system.create_optimized_parquet_dataset(
            "query_test_dataset", size_gb=0.05
        )
        
        # Executar consulta simples
        query = "SELECT department, COUNT(*) as count FROM query_test_dataset GROUP BY department"
        result = await nervous_system.execute_distributed_query(
            query, "query_test_dataset"
        )
        
        assert result['status'] == 'completed'
        assert result['execution_time_ms'] > 0
        assert result['records_returned'] >= 0
        assert 'function_id' in result
    
    @pytest.mark.asyncio
    async def test_massive_parallel_query_test(self, nervous_system):
        """Testa consultas paralelas massivas."""
        # Criar dataset
        nervous_system.create_optimized_parquet_dataset(
            "parallel_test_dataset", size_gb=0.05
        )
        
        # Executar teste com paralelismo reduzido
        results = await nervous_system.massive_parallel_query_test(
            "parallel_test_dataset", concurrent_functions=10
        )
        
        assert results['test_type'] == 'massive_parallel_query'
        assert results['successful_queries'] > 0
        assert results['performance_metrics']['p99_execution_time_ms'] > 0
        assert results['success_rate_percentage'] > 0
    
    def test_create_immutable_dataset_version(self, nervous_system):
        """Testa criação de versão imutável do dataset."""
        # Criar dataset base
        base_dataset = nervous_system.create_optimized_parquet_dataset(
            "immutable_test_dataset", size_gb=0.05
        )
        
        # Criar versão modificada
        modifications = {
            'filters': ['salary_base > 3000'],
            'transformations': [
                {'type': 'salary_adjustment', 'factor': 1.05}
            ]
        }
        
        version_result = nervous_system.create_immutable_dataset_version(
            "immutable_test_dataset", modifications
        )
        
        assert version_result['version'] == 2
        assert version_result['immutability_verified'] == True
        assert version_result['original_dataset'] == "immutable_test_dataset"
        assert 'new_dataset' in version_result
        assert 'version_pointer' in version_result
    
    def test_rollback_to_version(self, nervous_system):
        """Testa rollback para versão anterior."""
        # Criar dataset e versão
        nervous_system.create_optimized_parquet_dataset(
            "rollback_test_dataset", size_gb=0.05
        )
        
        modifications = {'filters': ['salary_base > 4000']}
        nervous_system.create_immutable_dataset_version(
            "rollback_test_dataset", modifications
        )
        
        # Executar rollback
        rollback_result = nervous_system.rollback_to_version(
            "rollback_test_dataset", 1
        )
        
        assert rollback_result['rollback_successful'] == True
        assert rollback_result['target_version'] == 1
        assert 'previous_active_dataset' in rollback_result
        assert 'new_active_dataset' in rollback_result


class TestServerlessFunctionFireworks:
    """Testes para o sistema de Fogo de Artifício de Funções."""
    
    @pytest.fixture
    def fireworks(self):
        """Fixture para instanciar o sistema de fireworks."""
        return ServerlessFunctionFireworks()
    
    @pytest.mark.asyncio
    async def test_ignite_function(self, fireworks):
        """Testa acendimento de função serverless."""
        request_data = {
            'function_type': 'api',
            'complexity': 1,
            'data_size': 100
        }
        
        firework = await fireworks.ignite_function('api', request_data)
        
        assert firework.function_id.startswith('api_')
        assert firework.status == 'created'
        assert firework.request_data == request_data
        assert firework.cold_start_ms >= 0
    
    @pytest.mark.asyncio
    async def test_execute_function(self, fireworks):
        """Testa execução de função efêmera."""
        request_data = {'function_type': 'api', 'complexity': 1}
        
        firework = await fireworks.ignite_function('api', request_data, simulate_cold_start=False)
        executed_firework = await fireworks.execute_function(firework)
        
        assert executed_firework.status in ['completed', 'failed']
        assert executed_firework.execution_time_ms > 0
        if executed_firework.status == 'completed':
            assert executed_firework.response_data is not None
    
    @pytest.mark.asyncio
    async def test_extinguish_function(self, fireworks):
        """Testa extinção de função após execução."""
        request_data = {'function_type': 'api', 'complexity': 1}
        
        firework = await fireworks.ignite_function('api', request_data, simulate_cold_start=False)
        await fireworks.execute_function(firework)
        
        # Verificar função ativa antes da extinção
        assert firework.function_id in fireworks.active_functions
        
        await fireworks.extinguish_function(firework)
        
        # Verificar função removida após extinção
        assert firework.function_id not in fireworks.active_functions
        assert firework in fireworks.completed_functions
    
    @pytest.mark.asyncio
    async def test_fireworks_storm_simulation(self, fireworks):
        """Testa simulação de tempestade reduzida."""
        results = await fireworks.fireworks_storm_simulation(
            target_rps=50,  # Reduzido para teste
            ramp_up_seconds=2,
            sustain_seconds=3
        )
        
        assert results['target_rps'] == 50
        assert results['requests_sent'] > 0
        assert results['total_time_seconds'] > 0
        assert 'success_rate_percentage' in results
        assert 'peak_concurrent_functions' in results
    
    def test_performance_metrics(self, fireworks):
        """Testa geração de métricas de performance."""
        # Adicionar algumas funções completadas manualmente para teste
        from src.serverless.function_fireworks import FireworkFunction
        
        test_function = FireworkFunction(
            function_id="test_func_1",
            created_at=time.time(),
            execution_start=time.time(),
            execution_end=time.time() + 0.1,
            status='completed'
        )
        fireworks.completed_functions.append(test_function)
        
        metrics = fireworks.get_performance_metrics()
        
        assert 'total_functions_executed' in metrics
        assert 'execution_time_stats' in metrics
        assert 'cold_start_stats' in metrics
        assert 'throughput' in metrics


class TestColdStartPredictor:
    """Testes para o preditor de cold start ML."""
    
    @pytest.fixture
    def predictor(self):
        """Fixture para instanciar o preditor."""
        return ColdStartPredictor()
    
    def test_analyze_function_dependencies(self, predictor):
        """Testa análise de dependências de função."""
        # Criar arquivo temporário de teste
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import duckdb
import asyncio

class TestClass:
    def __init__(self):
        pass
    
    async def test_function(self):
        if True:
            for i in range(10):
                try:
                    print(i)
                except:
                    pass
""")
            temp_file = f.name
        
        try:
            analysis = predictor.analyze_function_dependencies(temp_file)
            
            assert 'file_size_kb' in analysis
            assert 'line_count' in analysis
            assert 'import_count' in analysis
            assert 'dependency_size_mb' in analysis
            assert 'complexity_score' in analysis
            assert 'has_ml_dependencies' in analysis
            assert analysis['has_ml_dependencies'] == True  # sklearn presente
            assert analysis['import_count'] > 0
            assert analysis['complexity_score'] > 0
            
        finally:
            Path(temp_file).unlink()
    
    def test_generate_training_data(self, predictor):
        """Testa geração de dados de treinamento."""
        # Criar dados de análise mock
        function_analyses = [
            {
                'file_size_kb': 10.0,
                'line_count': 100,
                'import_count': 5,
                'dependency_size_mb': 25.0,
                'complexity_score': 15,
                'async_functions': 2,
                'class_count': 1,
                'function_count': 3,
                'has_ml_dependencies': True,
                'has_db_dependencies': False,
                'has_heavy_dependencies': True,
                'module_type': 'service'
            },
            {
                'file_size_kb': 5.0,
                'line_count': 50,
                'import_count': 3,
                'dependency_size_mb': 10.0,
                'complexity_score': 8,
                'async_functions': 1,
                'class_count': 0,
                'function_count': 2,
                'has_ml_dependencies': False,
                'has_db_dependencies': True,
                'has_heavy_dependencies': False,
                'module_type': 'api'
            }
        ]
        
        training_df = predictor.generate_training_data(function_analyses)
        
        assert len(training_df) == 2
        assert 'cold_start_ms' in training_df.columns
        assert training_df['cold_start_ms'].iloc[0] > 0
        assert training_df['cold_start_ms'].iloc[1] > 0
        # Função com ML dependencies deve ter cold start maior
        assert training_df['cold_start_ms'].iloc[0] > training_df['cold_start_ms'].iloc[1]
    
    def test_prepare_features(self, predictor):
        """Testa preparação de features."""
        # Criar DataFrame de teste
        test_data = pd.DataFrame([
            {
                'file_size_kb': 10.0,
                'line_count': 100,
                'import_count': 5,
                'dependency_size_mb': 25.0,
                'complexity_score': 15,
                'async_functions': 2,
                'class_count': 1,
                'function_count': 3,
                'has_ml_dependencies': True,
                'has_db_dependencies': False,
                'has_heavy_dependencies': True,
                'module_type': 'service',
                'cold_start_ms': 200.0
            }
        ])
        
        X, y = predictor.prepare_features(test_data)
        
        assert X.shape[0] == 1
        assert X.shape[1] > 0  # Deve ter múltiplas features
        assert len(y) == 1
        assert y[0] == 200.0
    
    def test_train_model(self, predictor):
        """Testa treinamento do modelo."""
        # Gerar dados sintéticos para treinamento
        n_samples = 100
        X = np.random.randn(n_samples, 12)  # 12 features
        y = np.random.uniform(50, 500, n_samples)  # Cold start times
        
        training_results = predictor.train_model(X, y)
        
        assert 'best_model' in training_results
        assert 'best_score' in training_results
        assert 'feature_importance' in training_results
        assert predictor.trained == True
        assert predictor.model is not None


class TestQuantumValidationOrchestrator:
    """Testes para o orquestrador de validação quântica."""
    
    @pytest.fixture
    def orchestrator(self):
        """Fixture para instanciar o orquestrador."""
        return QuantumValidationOrchestrator()
    
    @pytest.mark.asyncio
    async def test_execute_massive_decentralized_query_test(self, orchestrator):
        """Testa execução do teste de consulta massiva."""
        parameters = {
            'dataset_size_gb': 0.1,  # Reduzido para teste
            'concurrent_functions': 10
        }
        
        results = await orchestrator.execute_massive_decentralized_query_test(parameters)
        
        assert results['test_name'] == 'massive_decentralized_query'
        assert 'phases' in results
        assert len(results['phases']) >= 2  # dataset_creation + parallel_queries
        assert 'performance_metrics' in results
        assert 'test_passed' in results
    
    @pytest.mark.asyncio 
    async def test_execute_predictive_cold_start_validation(self, orchestrator):
        """Testa execução do teste de validação de cold start."""
        results = await orchestrator.execute_predictive_cold_start_validation()
        
        assert results['test_name'] == 'predictive_cold_start_validation'
        assert 'phases' in results
        assert len(results['phases']) >= 3  # analysis + training + optimization
        assert 'model_performance' in results
        assert 'optimization_suggestions' in results
    
    @pytest.mark.asyncio
    async def test_execute_fireworks_storm_simulation(self, orchestrator):
        """Testa execução da simulação de tempestade."""
        parameters = {
            'target_rps': 100,  # Reduzido para teste
            'ramp_up_seconds': 2,
            'sustain_seconds': 3
        }
        
        results = await orchestrator.execute_fireworks_storm_simulation(parameters)
        
        assert results['test_name'] == 'fireworks_storm_simulation'
        assert 'phases' in results
        assert 'performance_metrics' in results
        assert 'visualization_path' in results
        assert 'test_passed' in results
    
    @pytest.mark.asyncio
    async def test_execute_immutability_versioning_test(self, orchestrator):
        """Testa execução do teste de imutabilidade."""
        results = await orchestrator.execute_immutability_versioning_test()
        
        assert results['test_name'] == 'immutability_versioning_test'
        assert 'phases' in results
        assert len(results['phases']) >= 3  # base + version + rollback
        assert 'validation_criteria' in results
        assert 'test_passed' in results


class TestIntegrationQuantumValidation:
    """Testes de integração para validação quântica completa."""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_full_quantum_validation_suite(self):
        """Teste de integração completo da suite quântica."""
        orchestrator = QuantumValidationOrchestrator()
        
        # Parâmetros reduzidos para teste de integração
        parameters = {
            'test1': {'dataset_size_gb': 0.05, 'concurrent_functions': 5},
            'test2': {},
            'test3': {'target_rps': 50, 'ramp_up_seconds': 2, 'sustain_seconds': 3},
            'test4': {}
        }
        
        results = await orchestrator.execute_full_quantum_validation(parameters)
        
        # Validações gerais
        assert 'test_id' in results
        assert results['test_suite'] == 'quantum_validation_complete'
        assert 'individual_tests' in results
        assert 'overall_summary' in results
        
        # Validar que todos os 4 testes foram executados
        individual_tests = results['individual_tests']
        expected_tests = [
            'massive_decentralized_query',
            'predictive_cold_start',
            'fireworks_storm',
            'immutability_versioning'
        ]
        
        for test_name in expected_tests:
            assert test_name in individual_tests
            assert 'test_name' in individual_tests[test_name]
            assert 'phases' in individual_tests[test_name]
        
        # Validar sumário geral
        summary = results['overall_summary']
        assert 'all_tests_passed' in summary
        assert 'success_rate_percentage' in summary
        assert 'tests_executed' in summary
        assert summary['tests_executed'] == 4
        assert 'architecture_validation' in summary
        assert 'quantum_properties_verified' in summary
        
        # Imprimir resultados para debug
        print(f"\n🌟 Resultado da Validação Quântica:")
        print(f"   Taxa de sucesso: {summary['success_rate_percentage']:.1f}%")
        print(f"   Testes executados: {summary['tests_executed']}")
        print(f"   Testes aprovados: {summary['tests_passed']}")
        
        # O teste deve ter pelo menos 50% de sucesso
        assert summary['success_rate_percentage'] >= 50.0


# Fixtures globais e configuração
@pytest.fixture(scope="session")
def event_loop():
    """Fixture para loop de eventos asyncio."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


if __name__ == "__main__":
    # Executar testes diretamente
    pytest.main([__file__, "-v", "--tb=short"])