#!/bin/bash
# Setup script for RAG Demo

set -e

echo "=========================================="
echo "RAG Demo Setup Script"
echo "=========================================="

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found!"
    echo ""
    echo "Install Ollama with:"
    echo "  curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

echo "✅ Ollama found"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo ""
    echo "⚠️  Ollama is not running"
    echo "Start it with: ollama serve"
    echo ""
    echo "Continuing anyway (you'll need to start Ollama manually)..."
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Pull models
echo ""
echo "=========================================="
echo "Pulling required models..."
echo "=========================================="

echo ""
echo "→ Pulling nomic-embed-text (embedding model)..."
ollama pull nomic-embed-text

echo ""
echo "→ Pulling llama2 (LLM)..."
ollama pull llama2

# Create sample docs if they don't exist
if [ ! -d "docs" ] || [ -z "$(ls -A docs/)" ]; then
    echo ""
    echo "Creating sample documents..."
    mkdir -p docs
    # Docs will be created by simple_rag.py on first run
else
    echo ""
    echo "✅ Sample docs already exist"
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To run the demo:"
echo "  1. Start Ollama: ollama serve"
echo "  2. Run demo: python simple_rag.py"
echo ""
echo "For presentation: cat RAG_Presentation.md"
echo ""
