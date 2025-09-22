# AI Assistant with Tools

AI assistant built with Streamlit, LangGraph, and multiple LLM backends (Gemini, Llama). The system provides document processing, OCR capabilities, and tool integration for enhanced question-answering and data analysis.

## Features

- **Multi-Model Support**: Switch between Gemini and Llama LLMs with easy configuration
- **Document Processing**: Upload and query PDF/HTML documents using vector store retrieval
- **OCR Integration**: Extract text from images using EasyOCR with multi-language support
- **Tool Integration**: Built-in tools for calculations, weather, Wikipedia search, and document retrieval
- **Data Analysis**: Query CSV files using pandas DataFrame agents
- **Conversation Memory**: Persistent conversation history with SQLite checkpointing
- **Web Interface**: Clean Streamlit UI with intuitive tab-based navigation
- **Vector Store Management**: Add, search, and reset document collections

## Quick Start

### Prerequisites

- Python 3.12
- Google API Key (for Gemini model - option 1)
- Ollama (for Llama model - option 2)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd ai-assistant-with-tools
   ```

2. **Install dependencies using Make:**

   ```bash
   make setup
   ```

   This will install Python dependencies and set up Ollama with the Llama model.

3. **Run the application:**

   ```bash
   make run-app
   ```

### Alternative Installation

If Make is not available:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Ollama (for Llama support)
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3.2:3b

# Run the application
python -m streamlit run ui/app.py
```

## How to Use

### Model Selection

1. **Choose LLM**: Select either Llama (local) or Gemini (cloud-based) from the sidebar
2. **API Configuration**: For Gemini, enter your Google API key in the form

### Document Management

1. **Upload Documents**: Use the sidebar to upload PDF or HTML files
2. **Vector Store**: Documents are automatically processed and added to the searchable vector store
3. **Reset Option**: Clear all documents using the reset button when needed

### Chat Agent

1. **Ask Questions**: Use the chat tab to ask questions about your documents
2. **Image Context**: Optionally upload images for OCR text extraction
3. **Tool Integration**: The agent automatically uses appropriate tools for calculations, weather, etc.

### CSV Analysis

1. **Upload CSV**: Use the CSV tab to upload data files
2. **Data Preview**: View your data before querying
3. **Natural Language Queries**: Ask questions about your data in plain English

## File Structure

```
ai-assistant-with-tools/
├── models/
│   ├── llm.py                # LLM factory for model creation
│   └── agents.py             # Agent management and creation
├── services/
│   ├── auth.py               # Authentication manager (placeholder)
│   ├── ocr.py                # OCR text extraction from images
│   └── vectorstore.py        # Vector store management and document processing
├── tools/
│   └── tools.py              # Tool definitions and manager
├── ui/
│   └── app.py                # Main Streamlit application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
└── Makefile                  # Build and run automation
```

## Technology Stack

- **Frontend**: Streamlit for web interface
- **AI Framework**: LangGraph for agent orchestration
- **LLM Backends**: Google Gemini, Ollama/Llama
- **Vector Store**: FAISS for document retrieval
- **OCR**: EasyOCR for text extraction from images
- **Data Analysis**: pandas for CSV processing
- **Embeddings**: SentenceTransformers for text embeddings
- **Memory**: SQLite for conversation checkpointing

## Configuration

The system can be configured through `config.py` and environment variables:

```python
# API Keys (set via environment variables)
GOOGLE_API_KEY = "your-google-api-key"

# Model configurations
GEMINI_MODEL = "gemini-2.5-flash-lite-preview-06-17"
LLAMA_MODEL = "llama3.2:3b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Data paths
VECTORSTORE_PATH = "./data/vectorstore_index"
UPLOAD_DIR = "./data/uploaded_docs"
CHECKPOINT_DB = "./data/checkpoints/checkpoint.db"
```

## Make Commands

| Command | Description |
|---------|-------------|
| `make all` | Setup and run complete application |
| `make setup` | Install all dependencies |
| `make install_deps` | Install Python dependencies only |
| `make install_ollama` | Install Ollama runtime |
| `make start_ollama` | Start Ollama service |
| `make pull_llama` | Download Llama model |
| `make run_llama` | Run Llama model in background |
| `make run-app` | Run Streamlit application |
| `make pull_qwen` | Download Qwen model (alternative) |

## Available Tools

### Calculator Tool

- **Function**: Mathematical calculations using numexpr
- **Usage**: Automatic for math questions
- **Example**: "Calculate 37593 times 67"

### Weather Tool

- **Function**: Current weather information
- **Usage**: Location-based weather queries
- **Example**: "What's the weather in Cairo?"

### Document Search Tool

- **Function**: Search uploaded documents
- **Usage**: Automatic for document-related queries
- **Example**: "Find information about machine learning"

### Wikipedia Tool

- **Function**: Wikipedia knowledge retrieval
- **Usage**: General knowledge questions
- **Example**: "Tell me about the Eiffel Tower"

## Database Schema

### Checkpoint Database

- **Purpose**: Store conversation history and agent states
- **Location**: `data/checkpoints/checkpoint.db`
- **Tables**: Automatically managed by LangGraph SQLiteSaver

## OCR Capabilities

### Supported Languages

- English (`en`)
- Arabic (`ar`)
- Extensible to other languages

### Image Processing

- **Formats**: PNG, JPG, JPEG
- **Text Extraction**: Multi-line text recognition
- **Integration**: Automatic context addition to queries

## Troubleshooting

### Common Issues

1. **Gemini API Errors**: Verify your Google API key is valid and has Gemini access
2. **Ollama Connection Issues**: Ensure Ollama service is running (`ollama serve`)
3. **Vector Store Errors**: Use reset function to clear corrupted vector stores
4. **Memory Issues**: For large documents, consider increasing system RAM

### System Requirements

- **Memory**: 4GB+ RAM recommended (8GB for Llama)
- **Storage**: 10GB+ for models and data
- **Network**: Required for Gemini, optional for Llama (local)

## Security Considerations

- API keys are stored in environment variables
- Documents processed locally; no external data transmission for Llama
- Consider secure storage for sensitive documents
- Authentication system is placeholder; implement proper auth for production

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with both model backends
5. Submit a pull request

For bug reports and feature requests, please use the issue tracker.

---

**Note**: This AI assistant is designed for educational and development purposes. For production deployment, consider implementing proper authentication, rate limiting, and security measures.
