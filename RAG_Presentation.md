# RAG (Retrieval-Augmented Generation)
## A Practical Introduction for Technical Audiences

---

# Agenda

1. **What is RAG?**
2. **Why RAG?**
3. **How RAG Works**
4. **Architecture Components**
5. **Live Demo** (Ollama-powered)
6. **When to Use RAG**
7. **Implementation Considerations**
8. **Q&A**

---

# What is RAG?

**Retrieval-Augmented Generation (RAG)** is a pattern that combines:
- **Retrieval** – Finding relevant documents from a knowledge base
- **Augmentation** – Injecting retrieved context into the prompt
- **Generation** – Using an LLM to generate the final answer

```
User Query → Retrieve Relevant Docs → Add to Prompt → LLM Generates Answer
```

---

# Why RAG?

| Challenge | Without RAG | With RAG |
|-----------|-------------|----------|
| Knowledge cutoff | LLM only knows training data | Can access up-to-date info |
| hallucinations | May fabricate facts | Grounded in retrieved context |
| Domain knowledge | Generic responses | Customized to your data |
| Data privacy | Send sensitive data to LLM | Keep data local |

---

# How RAG Works

```
┌─────────────┐    ┌──────────────────┐    ┌─────────────┐
│   Query     │───▶│  Embedding Model │───▶│   Vector    │
│  "What is..?"│    │  (Ollama)        │    │   Store     │
└─────────────┘    └──────────────────┘    └──────┬──────┘
                                                 │
                     ┌───────────────────────────┘
                     ▼
              ┌─────────────┐    ┌──────────────────┐    ┌─────────────┐
              │  Retrieve  │───▶│  Build Prompt    │───▶│     LLM     │
              │ Top-K Docs │    │ + Context        │    │  (Ollama)  │
              └─────────────┘    └──────────────────┘    └──────┬──────┘
                                                               │
                                                               ▼
                                                        ┌─────────────┐
                                                        │   Answer    │
                                                        │ + Citations │
                                                        └─────────────┘
```

---

# Key Components

## 1. **Document Processing**
- Text chunking/splitting
- Metadata extraction
- Cleaning & normalization

## 2. **Embedding Model**
- Converts text to vectors
- Example: `nomic-embed-text` (Ollama)

## 3. **Vector Database**
- Stores embeddings for similarity search
- Options: ChromaDB, FAISS, Milvus, Pinecone

## 4. **Retrieval System**
- Semantic search (not keyword!)
- Re-ranking (optional)

## 5. **Generation Model**
- LLM generates answer from retrieved context
- Ollama supports many models

---

# Why Ollama?

| Feature | Benefit |
|---------|---------|
| **Local execution** | Privacy, no API costs |
| **Open source models** | Llama 2, Mistral, CodeLlama |
| **Easy setup** | Single command install |
| **GPU support** | Fast inference |
| **Embedding models** | nomic-embed-text available |

---

# Demo Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Our RAG System                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📄 Documents    ──▶  🔪 Chunker  ──▶  📦 Chunks   │
│                                                     │
│  📦 Chunks      ──▶  🧠 Ollama   ──▶  💾 Vectors   │
│                   (nomic-embed-text)                │
│                                                     │
│  ❓ Query       ──▶  🔍 Retrieve ──▶  📄 Context   │
│                                                     │
│  📄 Context     ──▶  🤖 LLM      ──▶  💬 Answer    │
│                   (llama2/mistral)                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# Live Demo

We'll show:
1. **Setup** – Loading documents
2. **Indexing** – Creating embeddings
3. **Query** – Asking questions
4. **Results** – Seeing RAG in action

---

# When to Use RAG

## ✅ Good Use Cases
- Q&A over internal documents
- Technical documentation search
- Customer support automation
- Knowledge base queries

## ❌ Maybe Not
- Simple Q&A with fixed answers
- Tasks requiring world knowledge only
- Real-time aggregation of changing data

---

# Implementation Considerations

| Aspect | Recommendation |
|--------|----------------|
| **Chunk size** | 256-512 tokens typically |
| **Overlap** | 10-20% for context continuity |
| **Top-K** | 3-5 relevant documents |
| **Embedding model** | nomic-embed-text (free, good quality) |
| **LLM** | Llama 2 7B for speed, 70B for quality |
| **Vector DB** | ChromaDB for demos, Milvus/Pinecone for production |

---

# Retrieval Evaluation

```python
# Key metrics to track
retrieval_precision = relevant_retrieved / total_retrieved
retrieval_recall = relevant_retrieved / relevant_total
mrr = mean(reciprocal_rank_of_first_relevant)
```

---

# Production Tips

1. **Caching** – Cache embeddings for fast retrieval
2. **Hybrid search** – Combine keyword + semantic
3. **Re-ranking** – Cross-encoder for better results
4. **Monitoring** – Track retrieval quality
5. **Updates** – Periodic re-indexing of documents

---

# Tools & Resources

| Category | Tools |
|----------|-------|
| LLM Runtime | **Ollama** (ollama.ai) |
| Vector DB | ChromaDB, FAISS, Milvus |
| Embeddings | nomic-embed-text, bge |
| Frameworks | LangChain, LlamaIndex |
| Deployment | Docker, Kubernetes |

---

# Questions?

## Let's see the code!

**Repository**: [Will be created]

**Key files**:
- `simple_rag.py` – Core RAG implementation
- `requirements.txt` – Dependencies
- `docs/` – Sample documents for demo

---

# Backup Slides

---

# Embedding Models Available in Ollama

```
ollama pull nomic-embed-text   # Best open embedding
ollama pull mxbai-embed-large  # High quality
ollama pull bge-m3             # Multilingual
```

---

# LLM Models in Ollama

```
ollama pull llama2            # General purpose
ollama pull mistral           # Fast, good quality
ollama pull codellama         # Code-focused
ollama pull phi3              # Lightweight
```

---

# Vector Database Comparison

| DB | Type | Best For |
|----|------|----------|
| **ChromaDB** | Embeddable | Prototyping, demos |
| **FAISS** | Library | Fast similarity search |
| **Milvus** | Server | Production scale |
| **Pinecone** | SaaS | Managed solution |
| **Weaviate** | Server | Graph + vector hybrid |

