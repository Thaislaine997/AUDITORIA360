"""
Serverless Function Fireworks - AUDITORIA360
Orquestração de Fogo de Artifício de Funções Efêmeras para escalabilidade instantânea.
"""

import asyncio
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import random
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import concurrent.futures
from collections import defaultdict
import threading


@dataclass
class FireworkFunction:
    """Representa uma função serverless efêmera - um "fogo de artifício"."""
    function_id: str
    created_at: float
    execution_start: Optional[float] = None
    execution_end: Optional[float] = None
    cold_start_ms: float = 0
    status: str = 'created'  # created, executing, completed, failed, expired
    request_data: Optional[Dict] = None
    response_data: Optional[Dict] = None
    error: Optional[str] = None
    
    @property
    def lifetime_ms(self) -> float:
        """Tempo de vida total da função."""
        end_time = self.execution_end or time.time()
        return (end_time - self.created_at) * 1000
    
    @property
    def execution_time_ms(self) -> float:
        """Tempo de execução pura (sem cold start)."""
        if self.execution_start and self.execution_end:
            return (self.execution_end - self.execution_start) * 1000
        return 0


class ServerlessFunctionFireworks:
    """
    Orquestrador do Fogo de Artifício de Funções Serverless.
    
    Cada pedido API não vai para um servidor - ele acende uma função efêmera
    que brilha por milissegundos para executar sua tarefa e depois desaparece
    sem deixar rastro. A escalabilidade é uma propriedade inerente do universo
    serverless, tão natural como a expansão do cosmos.
    """
    
    def __init__(self):
        self.active_functions: Dict[str, FireworkFunction] = {}
        self.completed_functions: List[FireworkFunction] = []
        self.metrics = {
            'total_invocations': 0,
            'concurrent_peak': 0,
            'total_execution_time_ms': 0,
            'errors': 0,
            'cold_starts': 0
        }
        self.visualization_data = defaultdict(list)
        self._lock = threading.Lock()
        
    async def ignite_function(self, 
                            function_type: str,
                            request_data: Dict[str, Any],
                            simulate_cold_start: bool = True) -> FireworkFunction:
        """
        Acende uma nova função serverless - um novo fogo de artifício no céu digital.
        """
        function_id = f"{function_type}_{int(time.time() * 1000000)}"
        
        # Criar função efêmera
        firework = FireworkFunction(
            function_id=function_id,
            created_at=time.time(),
            request_data=request_data
        )
        
        with self._lock:
            self.active_functions[function_id] = firework
            self.metrics['total_invocations'] += 1
            self.metrics['concurrent_peak'] = max(
                self.metrics['concurrent_peak'], 
                len(self.active_functions)
            )
        
        # Simular cold start baseado no tipo de função
        if simulate_cold_start:
            cold_start_time = self._calculate_cold_start(function_type, request_data)
            firework.cold_start_ms = cold_start_time
            await asyncio.sleep(cold_start_time / 1000)  # Converter para segundos
            
            if cold_start_time > 0:
                with self._lock:
                    self.metrics['cold_starts'] += 1
        
        return firework
    
    async def execute_function(self, firework: FireworkFunction) -> FireworkFunction:
        """
        Executa a função efêmera - o momento de brilho do fogo de artifício.
        """
        firework.execution_start = time.time()
        firework.status = 'executing'
        
        try:
            # Registrar para visualização em tempo real
            self._record_execution_event(firework, 'started')
            
            # Executar lógica baseada no tipo de função
            function_type = firework.function_id.split('_')[0]
            result = await self._execute_function_logic(function_type, firework.request_data)
            
            firework.response_data = result
            firework.status = 'completed'
            firework.execution_end = time.time()
            
            # Registrar conclusão
            self._record_execution_event(firework, 'completed')
            
        except Exception as e:
            firework.error = str(e)
            firework.status = 'failed'
            firework.execution_end = time.time()
            
            with self._lock:
                self.metrics['errors'] += 1
            
            self._record_execution_event(firework, 'failed')
        
        # Registrar métricas
        with self._lock:
            self.metrics['total_execution_time_ms'] += firework.execution_time_ms
        
        return firework
    
    async def extinguish_function(self, firework: FireworkFunction):
        """
        Apaga a função após execução - o fogo de artifício desaparece sem rastro.
        """
        with self._lock:
            if firework.function_id in self.active_functions:
                del self.active_functions[firework.function_id]
                self.completed_functions.append(firework)
                
                # Limitar histórico para não consumir muita memória
                if len(self.completed_functions) > 10000:
                    self.completed_functions = self.completed_functions[-5000:]
        
        # Registrar extinção para visualização
        self._record_execution_event(firework, 'extinguished')
    
    def _calculate_cold_start(self, function_type: str, request_data: Dict) -> float:
        """
        Calcula tempo de cold start baseado no tipo de função e dependências.
        Simula o modelo de ML para predição de cold start.
        """
        base_cold_start = {
            'analytics': 100,    # Funções de analytics (DuckDB) - mais pesadas
            'api': 50,          # APIs simples
            'auth': 30,         # Autenticação - mais leve
            'notification': 40,  # Notificações
            'audit': 80,        # Auditoria - média complexidade
            'ml': 200,          # Machine Learning - mais pesado
            'report': 90        # Relatórios
        }.get(function_type, 60)
        
        # Fatores que influenciam cold start
        data_size_factor = len(str(request_data)) / 1000  # Tamanho dos dados
        complexity_factor = request_data.get('complexity', 1)  # Complexidade da operação
        
        # Adicionar variação aleatória para simular condições reais
        variation = random.uniform(0.8, 1.2)
        
        cold_start_ms = (base_cold_start + data_size_factor + complexity_factor * 20) * variation
        
        # 20% das funções têm cold start zero (função já aquecida)
        if random.random() < 0.2:
            cold_start_ms = 0
        
        return cold_start_ms
    
    async def _execute_function_logic(self, function_type: str, request_data: Dict) -> Dict[str, Any]:
        """Executa a lógica específica da função baseada no tipo."""
        # Simular tempo de execução variado
        execution_time = {
            'analytics': random.uniform(0.1, 0.5),  # 100-500ms
            'api': random.uniform(0.05, 0.2),       # 50-200ms
            'auth': random.uniform(0.02, 0.1),      # 20-100ms
            'notification': random.uniform(0.03, 0.15),  # 30-150ms
            'audit': random.uniform(0.2, 0.8),      # 200-800ms
            'ml': random.uniform(0.5, 2.0),         # 500ms-2s
            'report': random.uniform(0.3, 1.0)      # 300ms-1s
        }.get(function_type, 0.1)
        
        await asyncio.sleep(execution_time)
        
        # Simular resultado baseado no tipo
        if function_type == 'analytics':
            return {
                'query_result': f"Processed {random.randint(100, 10000)} records",
                'execution_time_ms': execution_time * 1000,
                'cache_hit': random.choice([True, False])
            }
        elif function_type == 'api':
            return {
                'status': 'success',
                'data': {'id': random.randint(1000, 9999)},
                'response_time_ms': execution_time * 1000
            }
        elif function_type == 'auth':
            return {
                'authenticated': random.choice([True, False]),
                'user_id': f"user_{random.randint(1, 1000)}",
                'session_token': f"token_{random.randint(10000, 99999)}"
            }
        else:
            return {
                'status': 'completed',
                'result': f"{function_type}_result_{random.randint(1, 1000)}",
                'processing_time_ms': execution_time * 1000
            }
    
    def _record_execution_event(self, firework: FireworkFunction, event_type: str):
        """Registra evento para visualização em tempo real."""
        timestamp = time.time()
        
        with self._lock:
            self.visualization_data['timestamps'].append(timestamp)
            self.visualization_data['events'].append(event_type)
            self.visualization_data['function_ids'].append(firework.function_id)
            self.visualization_data['function_types'].append(
                firework.function_id.split('_')[0]
            )
            
            # Manter apenas os últimos 1000 eventos para visualização
            if len(self.visualization_data['timestamps']) > 1000:
                for key in self.visualization_data:
                    self.visualization_data[key] = self.visualization_data[key][-500:]
    
    async def fireworks_storm_simulation(self, 
                                       target_rps: int = 20000,
                                       ramp_up_seconds: int = 10,
                                       sustain_seconds: int = 60) -> Dict[str, Any]:
        """
        Simulação de Tempestade de Fogo de Artifício:
        Teste de carga de 0 a 20.000 RPS em 10s, mantendo por 1 minuto.
        """
        print(f"🎆 INICIANDO TEMPESTADE DE FOGO DE ARTIFÍCIO")
        print(f"   🎯 Meta: {target_rps} RPS")
        print(f"   ⏱️ Ramp-up: {ramp_up_seconds}s")
        print(f"   🕐 Sustentação: {sustain_seconds}s")
        
        start_time = time.time()
        test_results = {
            'start_time': start_time,
            'target_rps': target_rps,
            'ramp_up_seconds': ramp_up_seconds,
            'sustain_seconds': sustain_seconds,
            'requests_sent': 0,
            'requests_completed': 0,
            'throttling_errors': 0,
            'total_errors': 0,
            'peak_concurrent_functions': 0,
            'average_response_time_ms': 0,
            'phases': []
        }
        
        # FASE 1: Ramp-up (0 a target_rps)
        print(f"\n🚀 FASE 1: Ramp-up (0 → {target_rps} RPS)")
        ramp_up_results = await self._execute_ramp_up_phase(
            target_rps, ramp_up_seconds, start_time
        )
        test_results['phases'].append(ramp_up_results)
        test_results['requests_sent'] += ramp_up_results['requests_sent']
        
        # FASE 2: Sustentação (target_rps constante)
        print(f"\n💥 FASE 2: Sustentação ({target_rps} RPS por {sustain_seconds}s)")
        sustain_results = await self._execute_sustain_phase(
            target_rps, sustain_seconds
        )
        test_results['phases'].append(sustain_results)
        test_results['requests_sent'] += sustain_results['requests_sent']
        
        # Aguardar conclusão de todas as funções ativas
        print(f"\n⏳ Aguardando conclusão das funções ativas...")
        await self._wait_for_completion()
        
        # Calcular métricas finais
        total_time = time.time() - start_time
        test_results.update({
            'total_time_seconds': total_time,
            'requests_completed': len(self.completed_functions),
            'total_errors': self.metrics['errors'],
            'peak_concurrent_functions': self.metrics['concurrent_peak'],
            'success_rate_percentage': (len(self.completed_functions) / max(test_results['requests_sent'], 1)) * 100,
            'average_rps': test_results['requests_sent'] / total_time,
            'test_passed': self.metrics['errors'] == 0  # Sem throttling
        })
        
        if self.completed_functions:
            avg_response_time = sum(f.execution_time_ms for f in self.completed_functions) / len(self.completed_functions)
            test_results['average_response_time_ms'] = avg_response_time
        
        print(f"\n🎉 TEMPESTADE CONCLUÍDA!")
        print(f"   📊 Requests enviados: {test_results['requests_sent']:,}")
        print(f"   ✅ Requests concluídos: {test_results['requests_completed']:,}")
        print(f"   📈 Pico de concorrência: {test_results['peak_concurrent_functions']:,}")
        print(f"   🎯 Taxa de sucesso: {test_results['success_rate_percentage']:.1f}%")
        print(f"   ⚡ RPS médio: {test_results['average_rps']:.0f}")
        print(f"   🚫 Erros de throttling: {test_results['throttling_errors']}")
        print(f"   {'✅ TESTE APROVADO!' if test_results['test_passed'] else '❌ TESTE REPROVADO!'}")
        
        return test_results
    
    async def _execute_ramp_up_phase(self, target_rps: int, duration_seconds: int, start_time: float) -> Dict[str, Any]:
        """Executa fase de ramp-up do teste de carga."""
        tasks = []
        requests_sent = 0
        
        for second in range(duration_seconds):
            # Calcular RPS atual (crescimento linear)
            current_rps = int((second + 1) * target_rps / duration_seconds)
            
            # Gerar requests para este segundo
            for _ in range(current_rps):
                request_data = self._generate_test_request()
                task = self._process_single_request(request_data)
                tasks.append(task)
                requests_sent += 1
            
            # Log de progresso
            if second % 2 == 0:  # A cada 2 segundos
                print(f"   ⚡ {second+1}s: {current_rps} RPS ({len(self.active_functions)} funções ativas)")
            
            # Aguardar próximo segundo
            await asyncio.sleep(1.0)
        
        return {
            'phase': 'ramp_up',
            'duration_seconds': duration_seconds,
            'target_rps': target_rps,
            'requests_sent': requests_sent,
            'functions_created': len(tasks)
        }
    
    async def _execute_sustain_phase(self, target_rps: int, duration_seconds: int) -> Dict[str, Any]:
        """Executa fase de sustentação do teste de carga."""
        tasks = []
        requests_sent = 0
        
        for second in range(duration_seconds):
            # Gerar requests constantes
            for _ in range(target_rps):
                request_data = self._generate_test_request()
                task = self._process_single_request(request_data)
                tasks.append(task)
                requests_sent += 1
            
            # Log de progresso a cada 10 segundos
            if second % 10 == 0:
                print(f"   💥 {second+1}s: {target_rps} RPS ({len(self.active_functions)} funções ativas)")
            
            # Aguardar próximo segundo
            await asyncio.sleep(1.0)
        
        return {
            'phase': 'sustain',
            'duration_seconds': duration_seconds,
            'target_rps': target_rps,
            'requests_sent': requests_sent,
            'functions_created': len(tasks)
        }
    
    async def _process_single_request(self, request_data: Dict[str, Any]):
        """Processa uma única request como função serverless."""
        try:
            # Acender função
            firework = await self.ignite_function(
                request_data['function_type'],
                request_data
            )
            
            # Executar função
            await self.execute_function(firework)
            
            # Apagar função
            await self.extinguish_function(firework)
            
        except Exception as e:
            # Simular erro de throttling em sobrecarga extrema
            if len(self.active_functions) > 50000:  # Limite simulado
                with self._lock:
                    self.metrics['errors'] += 1
                print(f"⚠️ Throttling simulado: {e}")
    
    def _generate_test_request(self) -> Dict[str, Any]:
        """Gera request de teste variada."""
        function_types = ['analytics', 'api', 'auth', 'notification', 'audit', 'ml', 'report']
        
        return {
            'function_type': random.choice(function_types),
            'complexity': random.randint(1, 5),
            'data_size': random.randint(100, 10000),
            'user_id': f"user_{random.randint(1, 10000)}",
            'timestamp': time.time()
        }
    
    async def _wait_for_completion(self, timeout_seconds: int = 30):
        """Aguarda conclusão de todas as funções ativas."""
        start_wait = time.time()
        
        while self.active_functions and (time.time() - start_wait) < timeout_seconds:
            print(f"   ⏳ Aguardando {len(self.active_functions)} funções ativas...")
            await asyncio.sleep(2)
        
        # Forçar limpeza das funções restantes
        remaining_functions = list(self.active_functions.values())
        for firework in remaining_functions:
            firework.status = 'timeout'
            firework.execution_end = time.time()
            await self.extinguish_function(firework)
    
    def generate_fireworks_visualization(self, save_path: str = "/tmp/fireworks_visualization.png"):
        """
        Gera visualização do 'fogo de artifício' mostrando funções explodindo e desaparecendo.
        """
        print(f"🎨 Gerando visualização do fogo de artifício...")
        
        if not self.visualization_data['timestamps']:
            print("⚠️ Nenhum dado de visualização disponível")
            return
        
        # Preparar dados para visualização
        timestamps = np.array(self.visualization_data['timestamps'])
        events = self.visualization_data['events']
        function_types = self.visualization_data['function_types']
        
        # Normalizar timestamps para começar em 0
        timestamps = timestamps - timestamps[0]
        
        # Criar figura com múltiplos subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🎆 Fogo de Artifício de Funções Serverless - AUDITORIA360', fontsize=16, fontweight='bold')
        
        # 1. Timeline de eventos (o fogo de artifício principal)
        event_colors = {
            'started': 'yellow',
            'completed': 'green', 
            'failed': 'red',
            'extinguished': 'gray'
        }
        
        for i, (timestamp, event, func_type) in enumerate(zip(timestamps, events, function_types)):
            color = event_colors.get(event, 'blue')
            size = 50 if event == 'started' else 20
            alpha = 0.8 if event in ['started', 'completed'] else 0.3
            
            ax1.scatter(timestamp, i % 10, c=color, s=size, alpha=alpha)
        
        ax1.set_xlabel('Tempo (segundos)')
        ax1.set_ylabel('Funções (mod 10)')
        ax1.set_title('🎇 Timeline de Execução das Funções')
        ax1.grid(True, alpha=0.3)
        
        # 2. Distribuição por tipo de função
        func_type_counts = {}
        for func_type in function_types:
            func_type_counts[func_type] = func_type_counts.get(func_type, 0) + 1
        
        if func_type_counts:
            types = list(func_type_counts.keys())
            counts = list(func_type_counts.values())
            colors = plt.cm.Set3(np.linspace(0, 1, len(types)))
            
            ax2.pie(counts, labels=types, colors=colors, autopct='%1.1f%%', startangle=90)
            ax2.set_title('📊 Distribuição por Tipo de Função')
        
        # 3. Funções ativas ao longo do tempo
        active_functions_timeline = []
        active_count = 0
        timeline_points = []
        
        for timestamp, event in zip(timestamps, events):
            if event == 'started':
                active_count += 1
            elif event in ['completed', 'failed', 'extinguished']:
                active_count = max(0, active_count - 1)
            
            timeline_points.append(timestamp)
            active_functions_timeline.append(active_count)
        
        ax3.plot(timeline_points, active_functions_timeline, 'b-', linewidth=2)
        ax3.fill_between(timeline_points, active_functions_timeline, alpha=0.3)
        ax3.set_xlabel('Tempo (segundos)')
        ax3.set_ylabel('Funções Ativas')
        ax3.set_title('📈 Funções Ativas ao Longo do Tempo')
        ax3.grid(True, alpha=0.3)
        
        # 4. Heatmap de intensidade de execução
        if len(timestamps) > 0:
            # Dividir timeline em bins de 1 segundo
            max_time = int(timestamps[-1]) + 1
            time_bins = np.arange(0, max_time, 1)
            
            # Contar eventos por segundo
            event_counts = []
            for i in range(len(time_bins) - 1):
                count = sum(1 for t in timestamps if time_bins[i] <= t < time_bins[i+1])
                event_counts.append(count)
            
            # Reshape para criar heatmap
            if event_counts:
                rows = int(np.ceil(len(event_counts) / 10))
                padded_counts = event_counts + [0] * (rows * 10 - len(event_counts))
                heatmap_data = np.array(padded_counts).reshape(rows, 10)
                
                im = ax4.imshow(heatmap_data, cmap='hot', aspect='auto')
                ax4.set_title('🔥 Intensidade de Execução (eventos/segundo)')
                ax4.set_xlabel('Segundo (mod 10)')
                ax4.set_ylabel('Década de segundos')
                plt.colorbar(im, ax=ax4)
        
        # Adicionar legenda global
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='yellow', markersize=10, label='Função Iniciada'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Função Completada'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Função Falhada'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=10, label='Função Extinta')
        ]
        fig.legend(handles=legend_elements, loc='lower center', ncol=4, bbox_to_anchor=(0.5, 0.02))
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.1)
        
        # Salvar visualização
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"🎨 Visualização salva em: {save_path}")
        
        return str(save_path)
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Retorna métricas de performance do sistema."""
        if not self.completed_functions:
            return {'error': 'Nenhuma função executada ainda'}
        
        execution_times = [f.execution_time_ms for f in self.completed_functions if f.execution_time_ms > 0]
        cold_start_times = [f.cold_start_ms for f in self.completed_functions if f.cold_start_ms > 0]
        
        return {
            'total_functions_executed': len(self.completed_functions),
            'total_functions_failed': sum(1 for f in self.completed_functions if f.status == 'failed'),
            'peak_concurrent_functions': self.metrics['concurrent_peak'],
            'execution_time_stats': {
                'avg_ms': np.mean(execution_times) if execution_times else 0,
                'p50_ms': np.percentile(execution_times, 50) if execution_times else 0,
                'p95_ms': np.percentile(execution_times, 95) if execution_times else 0,
                'p99_ms': np.percentile(execution_times, 99) if execution_times else 0,
                'min_ms': np.min(execution_times) if execution_times else 0,
                'max_ms': np.max(execution_times) if execution_times else 0,
            },
            'cold_start_stats': {
                'avg_ms': np.mean(cold_start_times) if cold_start_times else 0,
                'percentage_with_cold_start': (len(cold_start_times) / len(self.completed_functions)) * 100,
                'total_cold_starts': len(cold_start_times)
            },
            'throughput': {
                'functions_per_second': len(self.completed_functions) / max(self.metrics.get('total_execution_time_ms', 1) / 1000, 1)
            }
        }


async def demo_serverless_fireworks():
    """Demonstração completa do sistema de Fogo de Artifício Serverless."""
    print("🎆 === DEMO: FOGO DE ARTIFÍCIO DE FUNÇÕES SERVERLESS ===")
    
    # Inicializar orquestrador
    fireworks = ServerlessFunctionFireworks()
    
    # 1. Teste básico de funções individuais
    print("\n🎯 FASE 1: Teste de Funções Individuais")
    test_functions = ['analytics', 'api', 'auth', 'notification', 'audit']
    
    for func_type in test_functions:
        request_data = {
            'function_type': func_type,
            'complexity': 2,
            'data_size': 1000
        }
        
        firework = await fireworks.ignite_function(func_type, request_data)
        await fireworks.execute_function(firework)
        await fireworks.extinguish_function(firework)
        
        print(f"   ✨ {func_type}: {firework.execution_time_ms:.1f}ms (cold start: {firework.cold_start_ms:.1f}ms)")
    
    # 2. Simulação de tempestade reduzida para demo
    print("\n🎯 FASE 2: Tempestade de Fogo de Artifício (Demo)")
    storm_results = await fireworks.fireworks_storm_simulation(
        target_rps=500,     # Reduzido para demo
        ramp_up_seconds=5,  # Reduzido para demo
        sustain_seconds=10  # Reduzido para demo
    )
    
    # 3. Gerar visualização
    print("\n🎯 FASE 3: Visualização do Fogo de Artifício")
    viz_path = fireworks.generate_fireworks_visualization()
    
    # 4. Métricas de performance
    print("\n🎯 FASE 4: Métricas de Performance")
    metrics = fireworks.get_performance_metrics()
    
    print(f"\n📊 RESUMO DE PERFORMANCE:")
    print(f"   • Funções executadas: {metrics['total_functions_executed']:,}")
    print(f"   • Pico de concorrência: {metrics['peak_concurrent_functions']:,}")
    print(f"   • Tempo P99: {metrics['execution_time_stats']['p99_ms']:.1f}ms")
    print(f"   • Cold starts: {metrics['cold_start_stats']['percentage_with_cold_start']:.1f}%")
    print(f"   • Throughput: {metrics['throughput']['functions_per_second']:.0f} funções/seg")
    
    return {
        'storm_results': storm_results,
        'performance_metrics': metrics,
        'visualization_path': viz_path
    }


if __name__ == "__main__":
    # Executar demonstração
    asyncio.run(demo_serverless_fireworks())