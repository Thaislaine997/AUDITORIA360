from prometheus_client import Counter, Histogram

ingestion_duration_seconds = Histogram('ingestion_duration_seconds', 'Duração da ingestão de dados')
entities_extracted_count = Counter('entities_extracted_count', 'Total de entidades extraídas')
ml_training_time_seconds = Histogram('ml_training_time_seconds', 'Tempo de treinamento do modelo ML')
