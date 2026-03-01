# RAG Demo with Ollama

A simple Retrieval-Augmented Generation (RAG) system using Ollama for both embeddings and LLM. Perfect for demos and learning!

## Features

- 🧠 **Local LLM** - No API calls, runs entirely on your machine
- 📄 **Multi-Format Support** - TXT, PDF, Markdown, CSV, HTML
- 💾 **Persistent Vector Store** - ChromaDB for fast retrieval
- 🔧 **Easy to Customize** - Swap models, change chunk sizes

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
# Pull the embedding model
ollama pull nomic-embed-text

# Pull an LLM
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

### Convert Presentation to PDF

```bash
# Install dependencies
pip install markdown weasyprint

# Convert
python md_to_pdf.py
```

Or use pandoc:
```bash
pandoc RAG_Presentation.md -o RAG_Presentation.pdf --standalone
```

## Supported File Formats

| Format | Extension | Loader |
|--------|-----------|--------|
| Text | `.txt` | TextLoader |
| PDF | `.pdf` | PyPDFLoader |
| Markdown | `.md`, `.markdown` | TextLoader |
| CSV | `.csv` | CSVLoader |
| HTML | `.html`, `.htm` | UnstructuredHTMLLoader |

## Project Structure

```
rag-demo/
├── simple_rag.py           # Main RAG implementation
├── md_to_pdf.py           # Markdown to PDF converter
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── RAG_Presentation.md   # Presentation slides
├── setup.sh               # Setup script
├── docs/                  # Document storage
│   ├── rag_introduction.txt
│   ├── components.txt
│   ├── applications.txt
│   └── best_practices.txt
└── chroma_db/            # Vector store (created on first run)
```

## Usage

### Programmatic Usage

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

### Command Line

```bash
# Re-index documents
python -c "from simple_rag import SimpleRAG; r = SimpleRAG(); r.create_index(force_recreate=True)"
```

## Customization

### Change the LLM

```python
rag = SimpleRAG(llm_model="mistral")  # Faster
rag = SimpleRAG(llm_model="codellama")  # Better for code
```

### Use Your Own Documents

```bash
# Put your files in the docs/ folder
# Supported: .txt, .pdf, .md, .csv, .html

cp your_document.pdf docs/
python simple_rag.py  # Will re-index automatically
```

### Adjust Chunk Size

```python
rag = SimpleRAG(chunk_size=1000, chunk_overlap=100)
```

## For Your Seminar

### Presentation
- See `RAG_Presentation.md` for the slides!
- Convert to PDF: `python md_to_pdf.py`

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

### "Unsupported file type"
Check that your file extension is supported:
```python
from simple_rag import SimpleRAG
rag = SimpleRAG()
rag.list_supported_formats()
```

### Slow performance
- Use a GPU for faster inference
- Try smaller models (phi3 instead of llama2)

## References

- [Ollama](https://ollama.ai) - LLM runtime
- [LangChain](https://langchain.ai) - RAG framework
- [ChromaDB](https://trychroma.com) - Vector database
- [nomic-embed-text](https://ollama.com/library/nomic-embed-text) - Embedding model

---

**License**: MIT  
**Author**: IgotClaws  
**For**: Mission Planning and Dynamics Group - RAG Seminar
