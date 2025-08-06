"""
Predictive Cold Start ML Model - AUDITORIA360
Modelo de Machine Learning para predição de tempos de cold start de funções serverless.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import ast
import os
import json
from typing import Dict, List, Tuple, Any
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns


class ColdStartPredictor:
    """
    Modelo de ML para predição de tempos de cold start de funções serverless.
    
    Analisa dependências, tamanho de pacotes e características das funções
    para prever o tempo de arranque a frio e sugerir otimizações.
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_importance = {}
        self.trained = False
        
    def analyze_function_dependencies(self, function_path: str) -> Dict[str, Any]:
        """
        Analisa dependências de uma função serverless.
        
        Args:
            function_path: Caminho para o arquivo da função
            
        Returns:
            Dict com análise de dependências
        """
        try:
            with open(function_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extrair imports
            imports = self._extract_imports(content)
            
            # Calcular métricas de complexidade
            complexity_metrics = self._calculate_complexity_metrics(content)
            
            # Estimar tamanho de dependências
            dependency_size = self._estimate_dependency_size(imports)
            
            analysis = {
                'file_path': function_path,
                'file_size_kb': len(content.encode('utf-8')) / 1024,
                'line_count': len(content.split('\n')),
                'import_count': len(imports),
                'imports': imports,
                'dependency_size_mb': dependency_size,
                'complexity_score': complexity_metrics['complexity_score'],
                'async_functions': complexity_metrics['async_functions'],
                'class_count': complexity_metrics['class_count'],
                'function_count': complexity_metrics['function_count'],
                'has_ml_dependencies': self._has_ml_dependencies(imports),
                'has_db_dependencies': self._has_db_dependencies(imports),
                'has_heavy_dependencies': self._has_heavy_dependencies(imports),
            }
            
            return analysis
            
        except Exception as e:
            return {
                'file_path': function_path,
                'error': str(e),
                'file_size_kb': 0,
                'import_count': 0,
                'dependency_size_mb': 0,
                'complexity_score': 0
            }
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extrai imports do código Python."""
        imports = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                imports.append(line)
        
        return imports
    
    def _calculate_complexity_metrics(self, content: str) -> Dict[str, int]:
        """Calcula métricas de complexidade do código."""
        lines = content.split('\n')
        
        metrics = {
            'complexity_score': 0,
            'async_functions': 0,
            'class_count': 0,
            'function_count': 0,
            'if_statements': 0,
            'for_loops': 0,
            'try_except_blocks': 0
        }
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('async def '):
                metrics['async_functions'] += 1
                metrics['complexity_score'] += 2
            elif line.startswith('def '):
                metrics['function_count'] += 1
                metrics['complexity_score'] += 1
            elif line.startswith('class '):
                metrics['class_count'] += 1
                metrics['complexity_score'] += 3
            elif line.startswith('if ') or ' if ' in line:
                metrics['if_statements'] += 1
                metrics['complexity_score'] += 1
            elif line.startswith('for ') or line.startswith('while '):
                metrics['for_loops'] += 1
                metrics['complexity_score'] += 1
            elif line.startswith('try:') or line.startswith('except'):
                metrics['try_except_blocks'] += 1
                metrics['complexity_score'] += 1
        
        return metrics
    
    def _estimate_dependency_size(self, imports: List[str]) -> float:
        """Estima tamanho das dependências em MB."""
        # Mapeamento de dependências conhecidas para tamanhos estimados
        dependency_sizes = {
            'pandas': 50.0,
            'numpy': 25.0,
            'matplotlib': 30.0,
            'seaborn': 15.0,
            'sklearn': 80.0,
            'tensorflow': 200.0,
            'torch': 180.0,
            'duckdb': 40.0,
            'boto3': 30.0,
            'fastapi': 15.0,
            'sqlalchemy': 20.0,
            'requests': 5.0,
            'asyncio': 2.0,
            'json': 0.1,
            'os': 0.1,
            'sys': 0.1,
            'time': 0.1,
            'datetime': 1.0,
            'pathlib': 1.0,
            'typing': 0.5,
            'paddleocr': 150.0,
            'paddlepaddle': 120.0,
            'openai': 10.0,
            'prefect': 25.0,
            'plotly': 35.0,
        }
        
        total_size = 0.0
        
        for import_line in imports:
            # Extrair nome do pacote principal
            if 'import ' in import_line:
                package = import_line.split('import ')[1].split('.')[0].split(' ')[0]
                total_size += dependency_sizes.get(package, 5.0)  # Default 5MB
        
        return total_size
    
    def _has_ml_dependencies(self, imports: List[str]) -> bool:
        """Verifica se tem dependências de ML pesadas."""
        ml_packages = ['sklearn', 'tensorflow', 'torch', 'paddleocr', 'paddlepaddle']
        import_text = ' '.join(imports).lower()
        return any(pkg in import_text for pkg in ml_packages)
    
    def _has_db_dependencies(self, imports: List[str]) -> bool:
        """Verifica se tem dependências de banco de dados."""
        db_packages = ['sqlalchemy', 'psycopg2', 'duckdb', 'sqlite']
        import_text = ' '.join(imports).lower()
        return any(pkg in import_text for pkg in db_packages)
    
    def _has_heavy_dependencies(self, imports: List[str]) -> bool:
        """Verifica se tem dependências pesadas."""
        heavy_packages = ['pandas', 'matplotlib', 'seaborn', 'plotly', 'boto3']
        import_text = ' '.join(imports).lower()
        return any(pkg in import_text for pkg in heavy_packages)
    
    def scan_codebase_functions(self, base_path: str = "/home/runner/work/AUDITORIA360/AUDITORIA360") -> List[Dict[str, Any]]:
        """
        Escaneia toda a base de código para analisar funções.
        
        Returns:
            Lista de análises de todas as funções encontradas
        """
        print(f"🔍 Escaneando base de código em: {base_path}")
        
        function_analyses = []
        python_files = []
        
        # Encontrar todos os arquivos Python
        for root, dirs, files in os.walk(base_path):
            # Pular diretórios irrelevantes
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.endswith('.py') and not file.startswith('.'):
                    python_files.append(os.path.join(root, file))
        
        print(f"📁 Encontrados {len(python_files)} arquivos Python")
        
        # Analisar cada arquivo
        for file_path in python_files:
            try:
                analysis = self.analyze_function_dependencies(file_path)
                
                # Adicionar informações contextuais
                relative_path = os.path.relpath(file_path, base_path)
                analysis['relative_path'] = relative_path
                analysis['module_type'] = self._classify_module_type(relative_path)
                
                function_analyses.append(analysis)
                
            except Exception as e:
                print(f"⚠️ Erro analisando {file_path}: {e}")
        
        print(f"✅ Análise concluída: {len(function_analyses)} módulos analisados")
        return function_analyses
    
    def _classify_module_type(self, relative_path: str) -> str:
        """Classifica o tipo de módulo baseado no caminho."""
        path_lower = relative_path.lower()
        
        if 'api' in path_lower or 'router' in path_lower:
            return 'api'
        elif 'service' in path_lower:
            return 'service'
        elif 'model' in path_lower:
            return 'model'
        elif 'util' in path_lower or 'helper' in path_lower:
            return 'utility'
        elif 'test' in path_lower:
            return 'test'
        elif 'example' in path_lower:
            return 'example'
        elif 'serverless' in path_lower:
            return 'serverless'
        elif 'auth' in path_lower:
            return 'auth'
        elif 'monitoring' in path_lower:
            return 'monitoring'
        else:
            return 'other'
    
    def generate_training_data(self, function_analyses: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Gera dados de treinamento com cold start times simulados baseados nas características.
        
        Returns:
            DataFrame com features e targets para treinamento
        """
        print("🎯 Gerando dados de treinamento...")
        
        training_data = []
        
        for analysis in function_analyses:
            if 'error' in analysis:
                continue
            
            # Calcular cold start time baseado nas características
            base_cold_start = 50  # 50ms base
            
            # Fatores que influenciam cold start
            size_factor = analysis['file_size_kb'] * 0.5
            dependency_factor = analysis['dependency_size_mb'] * 2.0
            complexity_factor = analysis['complexity_score'] * 1.5
            import_factor = analysis['import_count'] * 3.0
            
            # Penalidades por tipo de dependência
            ml_penalty = 200 if analysis['has_ml_dependencies'] else 0
            db_penalty = 100 if analysis['has_db_dependencies'] else 0
            heavy_penalty = 80 if analysis['has_heavy_dependencies'] else 0
            
            # Calcular cold start time
            predicted_cold_start = (
                base_cold_start + 
                size_factor + 
                dependency_factor + 
                complexity_factor + 
                import_factor + 
                ml_penalty + 
                db_penalty + 
                heavy_penalty
            )
            
            # Adicionar variação aleatória
            predicted_cold_start *= np.random.uniform(0.8, 1.2)
            
            # Garantir valores realistas
            predicted_cold_start = max(10, min(predicted_cold_start, 5000))
            
            training_data.append({
                **analysis,
                'cold_start_ms': predicted_cold_start
            })
        
        df = pd.DataFrame(training_data)
        
        print(f"📊 Dataset de treinamento criado:")
        print(f"   • {len(df)} amostras")
        print(f"   • Cold start médio: {df['cold_start_ms'].mean():.1f}ms")
        print(f"   • Cold start mínimo: {df['cold_start_ms'].min():.1f}ms")
        print(f"   • Cold start máximo: {df['cold_start_ms'].max():.1f}ms")
        
        return df
    
    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepara features para treinamento do modelo.
        
        Returns:
            X: Features preparadas
            y: Target (cold_start_ms)
        """
        print("🔧 Preparando features para o modelo...")
        
        # Selecionar features relevantes
        feature_columns = [
            'file_size_kb',
            'line_count', 
            'import_count',
            'dependency_size_mb',
            'complexity_score',
            'async_functions',
            'class_count',
            'function_count',
            'has_ml_dependencies',
            'has_db_dependencies', 
            'has_heavy_dependencies',
            'module_type'
        ]
        
        # Criar DataFrame de features
        X_df = df[feature_columns].copy()
        
        # Codificar variáveis categóricas
        if 'module_type' not in self.label_encoders:
            self.label_encoders['module_type'] = LabelEncoder()
            X_df['module_type'] = self.label_encoders['module_type'].fit_transform(X_df['module_type'].fillna('other'))
        else:
            X_df['module_type'] = self.label_encoders['module_type'].transform(X_df['module_type'].fillna('other'))
        
        # Converter booleanos para int
        bool_columns = ['has_ml_dependencies', 'has_db_dependencies', 'has_heavy_dependencies']
        for col in bool_columns:
            X_df[col] = X_df[col].astype(int)
        
        # Preencher valores faltantes
        X_df = X_df.fillna(0)
        
        # Normalizar features
        X = self.scaler.fit_transform(X_df)
        y = df['cold_start_ms'].values
        
        print(f"✅ Features preparadas: {X.shape}")
        
        return X, y
    
    def train_model(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Treina modelo de ML para predição de cold start.
        
        Returns:
            Dict com métricas de avaliação
        """
        print("🤖 Treinando modelo de ML...")
        
        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Treinar múltiplos modelos
        models = {
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                random_state=42
            )
        }
        
        best_model = None
        best_score = float('inf')
        results = {}
        
        for name, model in models.items():
            print(f"   🔥 Treinando {name}...")
            
            # Treinar modelo
            model.fit(X_train, y_train)
            
            # Predições
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            
            # Métricas
            train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
            test_r2 = r2_score(y_test, y_pred_test)
            test_mae = mean_absolute_error(y_test, y_pred_test)
            
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
            cv_rmse = np.sqrt(-cv_scores.mean())
            
            results[name] = {
                'train_rmse': train_rmse,
                'test_rmse': test_rmse,
                'test_r2': test_r2,
                'test_mae': test_mae,
                'cv_rmse': cv_rmse
            }
            
            print(f"      • RMSE teste: {test_rmse:.1f}ms")
            print(f"      • R²: {test_r2:.3f}")
            print(f"      • MAE: {test_mae:.1f}ms")
            
            # Selecionar melhor modelo
            if test_rmse < best_score:
                best_score = test_rmse
                best_model = model
                best_name = name
        
        # Salvar melhor modelo
        self.model = best_model
        self.trained = True
        
        # Feature importance
        if hasattr(best_model, 'feature_importances_'):
            feature_names = [
                'file_size_kb', 'line_count', 'import_count', 'dependency_size_mb',
                'complexity_score', 'async_functions', 'class_count', 'function_count',
                'has_ml_dependencies', 'has_db_dependencies', 'has_heavy_dependencies', 'module_type'
            ]
            
            self.feature_importance = dict(zip(feature_names, best_model.feature_importances_))
        
        print(f"✅ Melhor modelo: {best_name} (RMSE: {best_score:.1f}ms)")
        
        return {
            'best_model': best_name,
            'best_score': best_score,
            'all_results': results,
            'feature_importance': self.feature_importance
        }
    
    def predict_cold_start(self, function_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prediz cold start time para uma função específica.
        
        Returns:
            Dict com predição e análise
        """
        if not self.trained:
            raise ValueError("Modelo não foi treinado ainda")
        
        # Preparar features da função
        features = [
            function_analysis.get('file_size_kb', 0),
            function_analysis.get('line_count', 0),
            function_analysis.get('import_count', 0),
            function_analysis.get('dependency_size_mb', 0),
            function_analysis.get('complexity_score', 0),
            function_analysis.get('async_functions', 0),
            function_analysis.get('class_count', 0),
            function_analysis.get('function_count', 0),
            int(function_analysis.get('has_ml_dependencies', False)),
            int(function_analysis.get('has_db_dependencies', False)),
            int(function_analysis.get('has_heavy_dependencies', False)),
            self.label_encoders['module_type'].transform([function_analysis.get('module_type', 'other')])[0]
        ]
        
        # Normalizar
        features_scaled = self.scaler.transform([features])
        
        # Predizer
        predicted_cold_start = self.model.predict(features_scaled)[0]
        
        return {
            'predicted_cold_start_ms': predicted_cold_start,
            'confidence': 'high' if predicted_cold_start < 500 else 'medium' if predicted_cold_start < 1500 else 'low',
            'category': 'fast' if predicted_cold_start < 200 else 'medium' if predicted_cold_start < 800 else 'slow'
        }
    
    def analyze_top_slow_functions(self, function_analyses: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Analisa as funções com maior tempo de cold start previsto e sugere otimizações.
        
        Returns:
            Lista das top N funções mais lentas com sugestões de otimização
        """
        if not self.trained:
            raise ValueError("Modelo não foi treinado ainda")
        
        print(f"🔍 Analisando top {top_n} funções mais lentas...")
        
        # Predizer cold start para todas as funções
        predictions = []
        
        for analysis in function_analyses:
            if 'error' in analysis:
                continue
                
            try:
                prediction = self.predict_cold_start(analysis)
                predictions.append({
                    **analysis,
                    **prediction
                })
            except Exception as e:
                print(f"⚠️ Erro predizendo {analysis.get('relative_path', 'unknown')}: {e}")
        
        # Ordenar por cold start previsto
        predictions.sort(key=lambda x: x['predicted_cold_start_ms'], reverse=True)
        
        # Analisar top N funções
        top_slow_functions = []
        
        for i, func in enumerate(predictions[:top_n]):
            optimization_suggestions = self._generate_optimization_suggestions(func)
            
            top_slow_functions.append({
                'rank': i + 1,
                'file_path': func['relative_path'],
                'predicted_cold_start_ms': func['predicted_cold_start_ms'],
                'main_issues': self._identify_main_issues(func),
                'optimization_suggestions': optimization_suggestions,
                'potential_improvement_ms': self._estimate_potential_improvement(func, optimization_suggestions)
            })
        
        print(f"📊 Top {top_n} funções mais lentas:")
        for func in top_slow_functions:
            print(f"   {func['rank']}. {func['file_path']}: {func['predicted_cold_start_ms']:.0f}ms")
        
        return top_slow_functions
    
    def _identify_main_issues(self, function_analysis: Dict[str, Any]) -> List[str]:
        """Identifica principais problemas que causam cold start lento."""
        issues = []
        
        if function_analysis.get('dependency_size_mb', 0) > 100:
            issues.append("Dependências muito pesadas")
        
        if function_analysis.get('import_count', 0) > 20:
            issues.append("Muitos imports")
        
        if function_analysis.get('has_ml_dependencies'):
            issues.append("Dependências de ML pesadas")
        
        if function_analysis.get('file_size_kb', 0) > 50:
            issues.append("Arquivo muito grande")
        
        if function_analysis.get('complexity_score', 0) > 50:
            issues.append("Código muito complexo")
        
        return issues
    
    def _generate_optimization_suggestions(self, function_analysis: Dict[str, Any]) -> List[str]:
        """Gera sugestões de otimização específicas."""
        suggestions = []
        
        # Análise de dependências
        if function_analysis.get('has_ml_dependencies'):
            suggestions.append("Considere usar importação dinâmica para dependências ML")
            suggestions.append("Implemente cache de modelos pré-carregados")
        
        if function_analysis.get('dependency_size_mb', 0) > 50:
            suggestions.append("Divida em múltiplas funções menores")
            suggestions.append("Use layers do Lambda para dependências comuns")
        
        # Análise de código
        if function_analysis.get('import_count', 0) > 15:
            suggestions.append("Mova imports para dentro das funções (lazy loading)")
            suggestions.append("Remova imports não utilizados")
        
        if function_analysis.get('file_size_kb', 0) > 30:
            suggestions.append("Refatore código em módulos menores")
            suggestions.append("Extraia constantes e configurações para arquivos separados")
        
        if function_analysis.get('complexity_score', 0) > 30:
            suggestions.append("Simplifique lógica complexa")
            suggestions.append("Use padrão Strategy para algoritmos complexos")
        
        # Sugestões específicas por tipo
        module_type = function_analysis.get('module_type', '')
        if module_type == 'api':
            suggestions.append("Implemente cache de resposta para APIs")
            suggestions.append("Use connection pooling para databases")
        elif module_type == 'service':
            suggestions.append("Inicialize recursos pesados uma única vez")
            suggestions.append("Use singleton pattern para serviços")
        
        return suggestions
    
    def _estimate_potential_improvement(self, function_analysis: Dict[str, Any], suggestions: List[str]) -> float:
        """Estima melhoria potencial em ms aplicando as sugestões."""
        current_cold_start = function_analysis['predicted_cold_start_ms']
        
        # Estimativa de melhoria baseada nas sugestões
        improvement_factors = {
            'importação dinâmica': 0.3,
            'cache': 0.4,
            'refatoração': 0.2,
            'lazy loading': 0.25,
            'otimização de dependências': 0.35
        }
        
        total_improvement = 0
        for suggestion in suggestions:
            for keyword, factor in improvement_factors.items():
                if keyword in suggestion.lower():
                    total_improvement += factor
                    break
        
        # Limite máximo de melhoria de 70%
        total_improvement = min(total_improvement, 0.7)
        
        return current_cold_start * total_improvement
    
    def save_model(self, model_path: str = "/tmp/cold_start_predictor.joblib"):
        """Salva modelo treinado."""
        if not self.trained:
            raise ValueError("Modelo não foi treinado ainda")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_importance': self.feature_importance
        }
        
        joblib.dump(model_data, model_path)
        print(f"💾 Modelo salvo em: {model_path}")
    
    def load_model(self, model_path: str = "/tmp/cold_start_predictor.joblib"):
        """Carrega modelo salvo."""
        model_data = joblib.load(model_path)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_importance = model_data['feature_importance']
        self.trained = True
        
        print(f"📥 Modelo carregado de: {model_path}")
    
    def generate_analysis_report(self, function_analyses: List[Dict[str, Any]], top_slow_functions: List[Dict[str, Any]]) -> str:
        """Gera relatório completo da análise."""
        report_path = "/tmp/cold_start_analysis_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# 🚀 Relatório de Análise de Cold Start - AUDITORIA360\n\n")
            
            # Resumo executivo
            f.write("## 📊 Resumo Executivo\n\n")
            f.write(f"- **Total de funções analisadas**: {len(function_analyses)}\n")
            f.write(f"- **Funções com dependências ML**: {sum(1 for f in function_analyses if f.get('has_ml_dependencies'))}\n")
            f.write(f"- **Dependência média**: {np.mean([f.get('dependency_size_mb', 0) for f in function_analyses]):.1f} MB\n")
            f.write(f"- **Complexidade média**: {np.mean([f.get('complexity_score', 0) for f in function_analyses]):.1f}\n\n")
            
            # Top funções lentas
            f.write("## 🐌 Top Funções com Maior Cold Start Previsto\n\n")
            for func in top_slow_functions:
                f.write(f"### {func['rank']}. {func['file_path']}\n")
                f.write(f"- **Cold start previsto**: {func['predicted_cold_start_ms']:.0f}ms\n")
                f.write(f"- **Principais problemas**:\n")
                for issue in func['main_issues']:
                    f.write(f"  - {issue}\n")
                f.write(f"- **Sugestões de otimização**:\n")
                for suggestion in func['optimization_suggestions']:
                    f.write(f"  - {suggestion}\n")
                f.write(f"- **Melhoria potencial**: -{func['potential_improvement_ms']:.0f}ms\n\n")
            
            # Feature importance
            f.write("## 🎯 Importância das Features\n\n")
            if self.feature_importance:
                sorted_features = sorted(self.feature_importance.items(), key=lambda x: x[1], reverse=True)
                for feature, importance in sorted_features:
                    f.write(f"- **{feature}**: {importance:.3f}\n")
            
            f.write("\n---\n")
            f.write("*Relatório gerado automaticamente pelo Cold Start Predictor*\n")
        
        print(f"📄 Relatório salvo em: {report_path}")
        return report_path


async def demo_cold_start_predictor():
    """Demonstração completa do preditor de cold start."""
    print("🔮 === DEMO: PREDITOR DE COLD START ML ===")
    
    # Inicializar preditor
    predictor = ColdStartPredictor()
    
    # 1. Escanear base de código
    print("\n🎯 FASE 1: Escaneamento da Base de Código")
    function_analyses = predictor.scan_codebase_functions()
    
    # 2. Gerar dados de treinamento
    print("\n🎯 FASE 2: Geração de Dados de Treinamento")
    training_df = predictor.generate_training_data(function_analyses)
    
    # 3. Treinar modelo
    print("\n🎯 FASE 3: Treinamento do Modelo ML")
    X, y = predictor.prepare_features(training_df)
    training_results = predictor.train_model(X, y)
    
    # 4. Analisar funções mais lentas
    print("\n🎯 FASE 4: Análise das Funções Mais Lentas")
    top_slow_functions = predictor.analyze_top_slow_functions(function_analyses, top_n=3)
    
    # 5. Gerar relatório
    print("\n🎯 FASE 5: Geração de Relatório")
    report_path = predictor.generate_analysis_report(function_analyses, top_slow_functions)
    
    # 6. Salvar modelo
    print("\n🎯 FASE 6: Salvamento do Modelo")
    predictor.save_model()
    
    print(f"\n🎉 === ANÁLISE CONCLUÍDA ===")
    print(f"✅ Modelo treinado com RMSE: {training_results['best_score']:.1f}ms")
    print(f"✅ Top 3 funções mais lentas identificadas")
    print(f"✅ Sugestões de otimização geradas")
    print(f"✅ Relatório disponível em: {report_path}")
    
    return {
        'training_results': training_results,
        'top_slow_functions': top_slow_functions,
        'report_path': report_path,
        'total_functions_analyzed': len(function_analyses)
    }


if __name__ == "__main__":
    # Executar demonstração
    import asyncio
    asyncio.run(demo_cold_start_predictor())