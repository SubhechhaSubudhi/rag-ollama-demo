# RAG Demo with Ollama

A simple Retrieval-Augmented Generation (RAG) system using Ollama for both embeddings and LLM. Perfect for demos and learning!

## Prerequisites

### 1. Install Ollama

```bash
# macOS / Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows (WSL2 recommended)
# Follow: https://github.com/ollama/ollama
```

### 2. Pull Required Models

```bash
# Pull the embedding model (nomic-embed-text is free and excellent!)
ollama pull nomic-embed-text

# Pull an LLM (llama2 is good for general use, mistral is faster)
ollama pull llama2

# Other options:
# ollama pull mistral    # Fast, good quality
# ollama pull codellama  # For code-related questions
```

### 3. Start Ollama Server

```bash
# In a terminal, keep this running:
ollama serve
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Run the Demo

```bash
python simple_rag.py
```

This will:
1. Load sample documents from `docs/`
2. Create embeddings using `nomic-embed-text`
3. Build a vector store in `chroma_db/`
4. Run demo queries through Llama2

### Use Programmatically

```python
from simple_rag import SimpleRAG

# Initialize RAG system
rag = SimpleRAG(docs_path="docs")

# Create or load index
rag.create_index()

# Ask questions
result = rag.query("What is RAG?")
print(result["answer"])

# View sources
for doc in result["source_documents"]:
    print(f"Source: {doc['source']}")
```

## Project Structure

```
rag-demo/
├── simple_rag.py       # Main RAG implementation
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── docs/              # Document storage
│   ├── rag_introduction.txt
│   ├── components.txt
│   ├── applications.txt
│   └── best_practices.txt
└── chroma_db/         # Vector store (created on first run)
```

## Customization

### Change the LLM

```python
rag = SimpleRAG(llm_model="mistral")  # Faster
rag = SimpleRAG(llm_model="codellama")  # Better for code
```

### Use Your Own Documents

```bash
# Put your .txt files in the docs/ folder
cp your_document.txt docs/
python simple_rag.py  # Will re-index automatically
```

### Adjust Chunk Size

```python
rag = SimpleRAG(chunk_size=1000, chunk_overlap=100)
```

## Troubleshooting

### "Ollama not running"
```bash
# Start Ollama server
ollama serve
```

### "Model not found"
```bash
# Pull the model
ollama pull nomic-embed-text
ollama pull llama2
```

### Slow performance
- Use a GPU for faster inference
- Try smaller models (phi3 instead of llama2)

## For Your Seminar

### Presentation
See `RAG_Presentation.md` for the slides!

### Demo Flow
1. Show the architecture diagram
2. Run `python simple_rag.py`
3. Ask questions like:
   - "What is RAG?"
   - "What are the components?"
   - "What are the applications?"
4. Show how sources are cited

### Key Talking Points
1. **Privacy**: All data stays local
2. **No API costs**: Using open-source models
3. **Customizable**: Any documents, any domain
4. **Educational**: Great for learning RAG concepts

## References

- [Ollama](https://ollama.ai) - LLM runtime
- [LangChain](https://langchain.ai) - RAG framework
- [ChromaDB](https://trychroma.com) - Vector database
- [nomic-embed-text](https://ollama.com/library/nomic-embed-text) - Embedding model

---

**License**: MIT  
**Author**: IgotClaws  
**For**: Mission Planning and Dynamics Group - RAG Seminar
