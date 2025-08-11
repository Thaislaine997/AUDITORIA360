"""
Cérebro da IA de Desenvolvimento - AI Brain for Development Assistant

Uses langchain instead of embedchain for better compatibility with existing project dependencies.
"""

import os
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import hashlib
import time

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class CerebroAuditoria360:
    """
    The brain of our AI Development Assistant.
    Learns from all codebase files and provides intelligent responses about the project.
    """
    
    def __init__(self, db_path: str = "db_ia_dev", lista_arquivos_path: str = "lista_arquivos.txt"):
        """
        Initialize the AI brain.
        
        Args:
            db_path: Path for the vector database
            lista_arquivos_path: Path to the file list
        """
        logger.info("🧠 Inicializando o cérebro da IA de Desenvolvimento...")
        
        self.db_path = db_path
        self.lista_arquivos_path = lista_arquivos_path
        self.vectorstore = None
        self.retrieval_chain = None
        
        # Initialize OpenAI components
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Using faster, cheaper model for development
            temperature=0.1,      # Low temperature for more consistent responses
        )
        
        # Setup text splitter for code
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\nclass ", "\n\ndef ", "\n\n", "\n", " ", ""]
        )
        
        # Custom prompt for development assistance
        self.prompt_template = PromptTemplate(
            template="""Você é o assistente de IA interno do projeto AUDITORIA360, especializado em ajudar com desenvolvimento. 
Você tem conhecimento completo de toda a base de código e documentação do projeto.

Contexto relevante do código:
{context}

Pergunta do desenvolvedor: {question}

Instruções:
- Responda de forma técnica e precisa
- Use exemplos do código existente quando relevante  
- Seja conciso mas detalhado o suficiente
- Se não souber algo, admita e sugira onde procurar
- Foque em práticas que seguem os padrões já estabelecidos no projeto

Resposta:""",
            input_variables=["context", "question"]
        )
        
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize or load the knowledge base."""
        try:
            # Check if database already exists
            if os.path.exists(self.db_path) and os.listdir(self.db_path):
                logger.info("📚 Base de conhecimento encontrada. Carregando...")
                self.vectorstore = Chroma(
                    persist_directory=self.db_path,
                    embedding_function=self.embeddings
                )
                logger.info("✅ Base de conhecimento carregada com sucesso!")
            else:
                logger.info("🔍 Base de conhecimento não encontrada. Iniciando treinamento...")
                self._train_on_codebase()
            
            # Setup retrieval chain
            if self.vectorstore:
                self.retrieval_chain = RetrievalQA.from_chain_type(
                    llm=self.llm,
                    chain_type="stuff",
                    retriever=self.vectorstore.as_retriever(
                        search_type="similarity",
                        search_kwargs={"k": 4}  # Retrieve top 4 most relevant chunks
                    ),
                    chain_type_kwargs={"prompt": self.prompt_template},
                    return_source_documents=True
                )
                logger.info("🎯 Sistema de recuperação configurado!")
        
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar base de conhecimento: {e}")
            # Fallback: create minimal response system
            self._setup_fallback_system()
    
    def _setup_fallback_system(self):
        """Setup a fallback system when vector database fails."""
        logger.warning("⚠️ Usando sistema de fallback sem base vetorial")
        # This will allow basic responses even without the vector database
        
    def _train_on_codebase(self):
        """Train the AI on the entire codebase using lista_arquivos.txt."""
        try:
            if not os.path.exists(self.lista_arquivos_path):
                logger.error(f"❌ Arquivo {self.lista_arquivos_path} não encontrado!")
                return
            
            logger.info("📖 Lendo arquivos do projeto...")
            documents = []
            
            with open(self.lista_arquivos_path, "r", encoding="utf-8") as f:
                file_paths = [line.strip() for line in f if line.strip()]
            
            processed_count = 0
            skipped_count = 0
            
            for file_path in file_paths:
                try:
                    # Skip certain files that aren't useful for development assistance
                    if self._should_skip_file(file_path):
                        skipped_count += 1
                        continue
                    
                    if os.path.exists(file_path):
                        content = self._read_file_safely(file_path)
                        if content:
                            # Create document with metadata
                            doc = Document(
                                page_content=content,
                                metadata={
                                    "source": file_path,
                                    "file_type": Path(file_path).suffix,
                                    "file_name": Path(file_path).name
                                }
                            )
                            documents.append(doc)
                            processed_count += 1
                            
                            if processed_count % 10 == 0:
                                logger.info(f"📝 Processados {processed_count} arquivos...")
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erro ao processar {file_path}: {e}")
                    skipped_count += 1
                    continue
            
            if not documents:
                logger.error("❌ Nenhum documento foi processado!")
                return
            
            logger.info(f"📚 Criando base de conhecimento com {len(documents)} documentos...")
            
            # Split documents into chunks
            all_chunks = []
            for doc in documents:
                chunks = self.text_splitter.split_documents([doc])
                all_chunks.extend(chunks)
            
            logger.info(f"✂️ Divididos em {len(all_chunks)} chunks de conhecimento")
            
            # Create vector store
            self.vectorstore = Chroma.from_documents(
                documents=all_chunks,
                embedding=self.embeddings,
                persist_directory=self.db_path
            )
            
            # Persist the database
            self.vectorstore.persist()
            
            logger.info(f"🎉 Treinamento concluído! Processados: {processed_count}, Ignorados: {skipped_count}")
            
        except Exception as e:
            logger.error(f"❌ Erro durante o treinamento: {e}")
            raise
    
    def _should_skip_file(self, file_path: str) -> bool:
        """Determine if a file should be skipped during training."""
        skip_patterns = [
            '.git/', '__pycache__/', '.pytest_cache/', 'node_modules/',
            '.venv/', 'venv/', '.env', '.DS_Store',
            '.jpg', '.png', '.gif', '.pdf', '.ico',
            '.min.js', '.min.css',
            'package-lock.json', 'yarn.lock'
        ]
        
        file_path_lower = file_path.lower()
        return any(pattern in file_path_lower for pattern in skip_patterns)
    
    def _read_file_safely(self, file_path: str) -> Optional[str]:
        """Safely read file content with proper encoding handling."""
        try:
            # Try UTF-8 first
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Skip very large files (>100KB) to avoid memory issues
            if len(content) > 100000:
                logger.warning(f"⚠️ Arquivo muito grande ignorado: {file_path} ({len(content)} chars)")
                return None
            
            return content
            
        except UnicodeDecodeError:
            try:
                # Try latin-1 as fallback
                with open(file_path, "r", encoding="latin-1") as f:
                    return f.read()
            except Exception as e:
                logger.warning(f"⚠️ Erro de encoding em {file_path}: {e}")
                return None
        except Exception as e:
            logger.warning(f"⚠️ Erro ao ler {file_path}: {e}")
            return None
    
    def fazer_pergunta(self, pergunta: str) -> Dict[str, Any]:
        """
        Ask a question to the AI assistant.
        
        Args:
            pergunta: The question to ask
            
        Returns:
            dict: Response with answer and metadata
        """
        try:
            logger.info(f"🤔 Processando pergunta: {pergunta}")
            
            if not pergunta.strip():
                return {
                    "resposta": "Por favor, faça uma pergunta sobre o projeto AUDITORIA360.",
                    "status": "error",
                    "timestamp": time.time()
                }
            
            # If we have the retrieval system, use it
            if self.retrieval_chain:
                result = self.retrieval_chain({"query": pergunta})
                
                response = {
                    "resposta": result["result"],
                    "status": "success",
                    "timestamp": time.time(),
                    "sources": []
                }
                
                # Add source information
                if "source_documents" in result:
                    response["sources"] = [
                        {
                            "file": doc.metadata.get("source", ""),
                            "type": doc.metadata.get("file_type", ""),
                        }
                        for doc in result["source_documents"]
                    ]
                
                logger.info(f"✅ Resposta gerada com {len(response['sources'])} fontes")
                return response
            
            else:
                # Fallback response when no vector database is available
                fallback_response = self._generate_fallback_response(pergunta)
                return {
                    "resposta": fallback_response,
                    "status": "fallback",
                    "timestamp": time.time(),
                    "sources": []
                }
        
        except Exception as e:
            logger.error(f"❌ Erro ao processar pergunta: {e}")
            return {
                "resposta": f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}",
                "status": "error",
                "timestamp": time.time(),
                "sources": []
            }
    
    def _generate_fallback_response(self, pergunta: str) -> str:
        """Generate a fallback response when vector database isn't available."""
        try:
            # Use the LLM directly with basic context about the project
            basic_context = """
            Você está ajudando com o projeto AUDITORIA360, um sistema de auditoria e compliance.
            O projeto inclui:
            - Backend em Python com FastAPI
            - Frontend em React/TypeScript
            - Funcionalidades de IA e machine learning
            - Sistema de gestão de documentos
            - Automação de processos de auditoria
            """
            
            response = self.llm.predict(f"""
            {basic_context}
            
            Pergunta: {pergunta}
            
            Responda de forma útil baseado no conhecimento geral sobre sistemas de auditoria e as tecnologias mencionadas.
            Se não souber especificamente sobre o código, seja honesto e dê orientações gerais.
            """)
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro no fallback: {e}")
            return ("Desculpe, estou com dificuldades para responder no momento. "
                   "Verifique se as configurações da API estão corretas e tente novamente.")
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the AI brain."""
        return {
            "database_exists": os.path.exists(self.db_path) and os.path.isdir(self.db_path),
            "retrieval_ready": self.retrieval_chain is not None,
            "files_processed": self._count_processed_files(),
            "last_training": self._get_last_training_time()
        }
    
    def _count_processed_files(self) -> int:
        """Count how many files are in the vector database."""
        try:
            if self.vectorstore:
                # This is a rough estimation
                return len(self.vectorstore.get()["ids"]) if hasattr(self.vectorstore, 'get') else 0
            return 0
        except:
            return 0
    
    def _get_last_training_time(self) -> Optional[float]:
        """Get the last training time from database directory."""
        try:
            if os.path.exists(self.db_path):
                return os.path.getmtime(self.db_path)
            return None
        except:
            return None


# Factory function for easy initialization
def create_ai_brain(db_path: str = "db_ia_dev") -> CerebroAuditoria360:
    """
    Factory function to create and initialize the AI brain.
    
    Args:
        db_path: Path for the vector database
        
    Returns:
        CerebroAuditoria360: Initialized AI brain instance
    """
    return CerebroAuditoria360(db_path=db_path)