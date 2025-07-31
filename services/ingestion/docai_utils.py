def process_pdf(uri, cfg):
    """
    Processa PDF com Document AI e retorna entidades extraídas (mock/minimal).
    """
    # Aqui seria chamada real ao Document AI
    # Para integração, retorna lista de dicionários simulando entidades
    return [{"campo": "valor1", "outro": 123}, {"campo": "valor2", "outro": 456}]


def process_document(document_path):
    """
    Process document for backward compatibility with tests
    """
    # Mock implementation for testing
    return {"entities": []}


# Mock Google Cloud Document AI for compatibility
class DocumentProcessorServiceClient:
    """Mock Document AI client for testing"""
    
    def __init__(self):
        pass
    
    def process_document(self, request):
        return {"entities": []}
