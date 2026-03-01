"""
Simple RAG (Retrieval-Augmented Generation) Demo
Using Ollama for both embeddings and LLM

Requirements:
    pip install ollama chromadb langchain langchain-community

For PDF support:
    pip install pypdf

First, install and run Ollama:
    1. curl -fsSL https://ollama.ai/install.sh | sh
    2. ollama pull nomic-embed-text
    3. ollama pull llama2
    4. ollama serve
"""

import os
import subprocess
from pathlib import Path

# Third-party imports
try:
    import ollama
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install ollama")
    exit(1)

try:
    from langchain_community.document_loaders import (
        TextLoader, 
        DirectoryLoader, 
        PyPDFLoader,
        UnstructuredMarkdownLoader,
        CSVLoader,
        UnstructuredHTMLLoader
    )
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_community.embeddings import OllamaEmbeddings
    from langchain_community.llms import Ollama
    from langchain.chains import RetrievalQA
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install ollama chromadb langchain langchain-community pypdf python-docx")
    exit(1)


# Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "minimax-m2.5:cloud"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
DOCS_PATH = Path("docs")
PERSIST_DIR = Path("chroma_db")


# Supported file extensions and their loaders
FILE_LOADERS = {
    '.txt': TextLoader,
    '.pdf': PyPDFLoader,
    '.md': TextLoader,  # Can also use UnstructuredMarkdownLoader
    '.markdown': TextLoader,
    '.csv': CSVLoader,
    '.html': UnstructuredHTMLLoader,
    '.htm': UnstructuredHTMLLoader,
}


class SimpleRAG:
    """Simple RAG implementation using Ollama with multi-format support"""
    
    def __init__(
        self,
        docs_path: str = "docs",
        embedding_model: str = EMBEDDING_MODEL,
        llm_model: str = LLM_MODEL,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP
    ):
        self.docs_path = Path(docs_path)
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize embeddings
        self.embeddings = OllamaEmbeddings(
            model=embedding_model,
            base_url=OLLAMA_BASE_URL
        )
        
        # Initialize LLM
        self.llm = Ollama(
            model=llm_model,
            base_url=OLLAMA_BASE_URL
        )
        
        self.vectorstore = None
        self.qa_chain = None
    
    def get_loader(self, file_path: Path):
        """Get appropriate loader for file type"""
        ext = file_path.suffix.lower()
        
        if ext not in FILE_LOADERS:
            print(f"Warning: Unsupported file type {ext}, skipping {file_path}")
            return None
        
        loader_class = FILE_LOADERS[ext]
        
        # Some loaders need special encoding handling
        if ext in ['.txt', '.md', '.markdown']:
            return loader_class(str(file_path), encoding='utf-8')
        elif ext == '.pdf':
            return loader_class(str(file_path))
        else:
            return loader_class(str(file_path))
    
    def load_documents(self) -> list:
        """Load documents from the docs directory - supports multiple formats"""
        if not self.docs_path.exists():
            print(f"Warning: {self.docs_path} does not exist")
            return []
        
        documents = []
        supported_extensions = list(FILE_LOADERS.keys())
        
        # Find all supported files
        files = []
        for ext in supported_extensions:
            files.extend(self.docs_path.glob(f"*{ext}"))
            files.extend(self.docs_path.glob(f"**/*{ext}"))
        
        # Remove duplicates and sort
        files = sorted(set(files))
        
        print(f"Found {len(files)} supported files:")
        for f in files:
            print(f"  - {f.name} ({f.suffix})")
        
        for file_path in files:
            try:
                loader = self.get_loader(file_path)
                if loader:
                    docs = loader.load()
                    # Add source metadata
                    for doc in docs:
                        doc.metadata['source'] = file_path.name
                        doc.metadata['file_type'] = file_path.suffix
                    documents.extend(docs)
                    print(f"Loaded: {file_path.name} ({len(docs)} document(s))")
            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")
        
        print(f"\nTotal: Loaded {len(documents)} document(s)")
        return documents
    
    def split_documents(self, documents: list) -> list:
        """Split documents into chunks"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks
    
    def create_index(self, force_recreate: bool = False):
        """Create vector store index from documents"""
        # Check if index already exists
        if PERSIST_DIR.exists() and not force_recreate:
            print("Loading existing index...")
            self.vectorstore = Chroma(
                persist_directory=str(PERSIST_DIR),
                embedding_function=self.embeddings
            )
        else:
            # Load and process documents
            documents = self.load_documents()
            if not documents:
                print("No documents to index!")
                return
            
            chunks = self.split_documents(documents)
            
            # Create vector store
            print("Creating embeddings and index...")
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=str(PERSIST_DIR)
            )
            print(f"Index created and saved to {PERSIST_DIR}")
        
        # Create QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_kwargs={"k": 3}
            ),
            return_source_documents=True
        )
    
    def query(self, question: str) -> dict:
        """Query the RAG system"""
        if not self.qa_chain:
            raise ValueError("Index not created. Run create_index() first.")
        
        result = self.qa_chain({"query": question})
        
        return {
            "answer": result["result"],
            "source_documents": [
                {
                    "source": doc.metadata.get("source", "Unknown"),
                    "file_type": doc.metadata.get("file_type", "Unknown"),
                    "content": doc.page_content[:200] + "..."
                }
                for doc in result["source_documents"]
            ]
        }
    
    def check_ollama(self) -> bool:
        """Check if Ollama is running and has required models"""
        try:
            # Check if Ollama is running
            client = ollama.Client(host=OLLAMA_BASE_URL)
            models = client.list().models
            
            # Check for required models
            model_names = [m.model for m in models]
            
            print(f"Available models: {model_names}")
            
            has_embedding = any(EMBEDDING_MODEL in name for name in model_names)
            has_llm = any(self.llm_model in name for name in model_names)
            
            if not has_embedding:
                print(f"\nMissing {EMBEDDING_MODEL}. Install with:")
                print(f"  ollama pull {EMBEDDING_MODEL}")
            
            if not has_llm:
                print(f"\nMissing {self.llm_model}. Install with:")
                print(f"  ollama pull {self.llm_model}")
            
            return has_embedding and has_llm
            
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            print("\nMake sure Ollama is running:")
            print("  ollama serve")
            return False
    
    def list_supported_formats(self):
        """List all supported file formats"""
        print("Supported file formats:")
        for ext, loader in FILE_LOADERS.items():
            print(f"  {ext} -> {loader.__name__}")


def demo():
    """Run a demonstration of the RAG system"""
    print("=" * 60)
    print("Simple RAG Demo with Ollama - Multi-Format Support")
    print("=" * 60)
    
    # Show supported formats
    rag = SimpleRAG()
    rag.list_supported_formats()
    
    # Check Ollama
    if not rag.check_ollama():
        print("\nPlease install missing models and try again.")
        return
    
    # Create index
    print("\n--- Creating Index ---")
    # Check if docs exist, if not create sample
    if not Path("docs").exists():
        print("Creating sample documents...")
        create_sample_docs()
    
    rag.create_index()
    
    # Demo queries
    print("\n--- Demo Queries ---")
    
    questions = [
        "What is this document about?",
        "What are the key concepts explained?",
        "Summarize the main points.",
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        print("-" * 40)
        result = rag.query(question)
        print(f"A: {result['answer']}")
        print(f"\nSources:")
        for doc in result["source_documents"]:
            print(f"  - {doc['source']} ({doc['file_type']})")


def create_sample_docs():
    """Create sample documents for demo"""
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    samples = {
        "rag_introduction.txt": """
RAG (Retrieval-Augmented Generation) is a powerful technique that combines
the strengths of large language models with external knowledge bases.

Traditional LLMs have a knowledge cutoff - they can only answer questions
based on what they learned during training. RAG solves this by:

1. Retrieving relevant information from a knowledge base
2. Augmenting the prompt with this context
3. Generating answers grounded in actual documents

This approach reduces hallucinations and allows LLMs to answer questions
about documents they never saw during training.
""",
        "components.txt": """
The main components of a RAG system are:

1. DOCUMENT LOADERS: Extract text from various sources (PDFs, websites, databases)

2. TEXT CHUNKING: Split documents into smaller, manageable pieces.
   Typical chunk sizes range from 256 to 1024 tokens.

3. EMBEDDING MODELS: Convert text into vector representations.
   Popular choices include nomic-embed-text, bge, and OpenAI embeddings.

4. VECTOR DATABASE: Store embeddings for fast similarity search.
   Options include ChromaDB, FAISS, Milvus, and Pinecone.

5. RETRIEVAL SYSTEM: Find the most relevant documents for a query.
   Uses semantic similarity (cosine similarity) between query and document vectors.

6. LLM: Generates the final answer using the retrieved context.
   Ollama supports Llama2, Mistral, Codellama, and many others.
""",
        "applications.txt": """
RAG has many practical applications:

1. ENTERPRISE Q&A: Answer questions about internal documents, policies,
   and procedures without exposing sensitive data to external APIs.

2. CUSTOMER SUPPORT: Build chatbots that can access product documentation
   and previous support tickets.

3. TECHNICAL DOCUMENTATION: Create searchable knowledge bases for
   software APIs, engineering manuals, and scientific papers.

4. RESEARCH ASSISTANTS: Help researchers find relevant papers and
   summarize findings from large document collections.

5. LEGAL RESEARCH: Search through case law and legal documents
   to find relevant precedents.

6. FINANCIAL ANALYSIS: Query annual reports, earnings calls, and
   market research documents.
""",
        "best_practices.txt": """
Best practices for implementing RAG:

1. CHUNKING STRATEGY:
   - Use 256-512 tokens for semantic chunks
   - Maintain 10-20% overlap between chunks
   - Consider structural boundaries (paragraphs, sections)

2. EMBEDDING SELECTION:
   - nomic-embed-text is excellent and free
   - Consider bge-m3 for multilingual support
   - Evaluate on your specific domain

3. RETRIEVAL OPTIMIZATION:
   - Start with top-k=3 to 5 documents
   - Use hybrid search (keyword + semantic)
   - Consider re-ranking for better results

4. PROMPT ENGINEERING:
   - Include instructions to cite sources
   - Ask the LLM to use only retrieved context
   - Handle cases where context is insufficient

5. EVALUATION:
   - Track retrieval precision and recall
   - Measure answer quality with human feedback
   - Monitor for degradation over time
"""
    }
    
    for filename, content in samples.items():
        (docs_dir / filename).write_text(content)
        print(f"Created: docs/{filename}")


if __name__ == "__main__":
    # First, create sample docs if needed
    if not Path("docs").exists():
        create_sample_docs()
    
    demo()
