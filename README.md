# 🏗️ BEP Agent - AI-Powered BIM Execution Plan Generator

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/openai-gpt--3.5--turbo-green.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A proof-of-concept application that helps users generate BIM Execution Plans (BEPs) by analyzing existing plans and new project requirements using AI.

![BEP Agent Demo](https://via.placeholder.com/800x400/1f77b4/ffffff?text=BEP+Agent+Demo)

> **Note**: This is a proof-of-concept implementation for demonstration purposes. For production use, additional security, scalability, and compliance considerations should be addressed.

## Features

- **Document Analysis**: Extracts text from existing BEP documents (.docx format)
- **Intelligent Matching**: Uses vector similarity to find the most relevant existing plans
- **AI-Powered Generation**: Leverages GPT to create tailored outlines and content
- **Web Interface**: User-friendly Streamlit interface for easy interaction
- **Multiple Export Formats**: Export generated BEPs as Markdown or JSON

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Or set `USE_LOCAL_EMBEDDINGS=true` to use local sentence transformers

4. **Add sample BEP documents**:
   - Place your existing BEP documents (.docx files) in `data/bep_samples/`
   - The system will analyze these to learn BEP structures and content
   - A sample document is included for testing

## Quick Start

### Option 1: Simple Demo (No API Key Required)
```bash
python demo_simple.py
```
This runs a basic demonstration of document loading and analysis without requiring external APIs.

### Option 2: Full Web Interface
```bash
streamlit run main.py
```
This launches the complete web interface with AI-powered features (requires OpenAI API key or local embeddings).

## Usage

1. **Start the application**:
   ```bash
   streamlit run main.py
   ```

2. **Initialize the system**:
   - Click "Initialize/Rebuild Vector Store" in the sidebar
   - This processes your sample documents and builds the vector index

3. **Generate a new BEP**:
   - **Project Input**: Describe your new project requirements
   - **Analysis**: Review similar existing plans and relevant content
   - **Outline**: Generate and customize the BEP outline
   - **Generate BEP**: Create full content and export

## Configuration

Edit the `.env` file to customize:

- `OPENAI_API_KEY`: Your OpenAI API key
- `USE_LOCAL_EMBEDDINGS`: Set to `true` to use local embeddings instead of OpenAI
- `CHUNK_SIZE`: Size of text chunks for processing (default: 1000)
- `TOP_K_CHUNKS`: Number of relevant chunks to retrieve (default: 5)

## Architecture

### Core Components

1. **DocumentLoader** (`document_loader.py`):
   - Extracts text from DOCX files using `python-docx`
   - Splits text into chunks using LangChain's RecursiveCharacterTextSplitter
   - Extracts headings and metadata

2. **VectorStore** (`vector_store.py`):
   - Creates embeddings using OpenAI API or sentence-transformers
   - Builds FAISS index for similarity search
   - Computes plan-level vectors for document matching

3. **OutlineGenerator** (`outline_generator.py`):
   - Analyzes existing BEP structures
   - Generates project-specific outlines using GPT
   - Creates detailed section content

4. **BEPProcessor** (`bep_processor.py`):
   - Orchestrates the entire workflow
   - Manages state and coordinates components
   - Handles export functionality

5. **Main Application** (`main.py`):
   - Streamlit web interface
   - User interaction and workflow management

### Data Flow

1. **Initialization**: Load sample BEPs → Extract text → Create chunks → Generate embeddings → Build FAISS index
2. **Analysis**: Project description → Find similar plans → Retrieve relevant chunks
3. **Generation**: Create outline → Generate section content → Export final BEP

## File Structure

```
BEP Agent DEV/
├── main.py                 # Streamlit web application
├── bep_processor.py        # Main orchestration logic
├── document_loader.py      # Document loading and text extraction
├── vector_store.py         # Vector embeddings and similarity search
├── outline_generator.py    # AI-powered outline and content generation
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
└── data/
    ├── bep_samples/      # Sample BEP documents (.docx)
    ├── new_project/      # Project requirements documents
    └── vector_store/     # Cached vector store data
```

## Dependencies

- **OpenAI**: GPT-based content generation and embeddings
- **FAISS**: Fast similarity search and clustering
- **LangChain**: Text processing and splitting
- **Sentence Transformers**: Local embedding generation (optional)
- **python-docx**: DOCX file processing
- **Streamlit**: Web interface
- **NumPy, Pandas, Scikit-learn**: Data processing

## Testing

Run the installation test to verify everything is working:
```bash
python test_installation.py
```

This will check dependencies, configuration, sample documents, and basic functionality.

## Troubleshooting

### Common Issues

1. **sentence-transformers import error**:
   - This is optional for local embeddings
   - Use OpenAI embeddings instead by setting `USE_LOCAL_EMBEDDINGS=false`
   - Or install missing dependencies: `pip install h5py tensorflow`

2. **OpenAI API errors**:
   - Ensure your API key is correctly set in `.env`
   - Check your OpenAI account has sufficient credits
   - Use local embeddings as fallback: `USE_LOCAL_EMBEDDINGS=true`

3. **No sample documents**:
   - Add .docx files to `data/bep_samples/`
   - A sample document is included for testing

## Limitations

- Currently supports only DOCX format for input documents
- Requires OpenAI API key for best performance (local embeddings available as alternative)
- Generated content quality depends on the quality of sample BEP documents
- Processing time scales with document size and number of sections

## Future Enhancements

- Support for additional document formats (PDF, Word templates)
- Integration with BIM software APIs
- Advanced template customization
- Collaborative editing features
- Version control for generated BEPs

## License

This is a proof-of-concept application for demonstration purposes.

## Support

For issues or questions, please check the configuration and ensure:
1. Sample BEP documents are placed in `data/bep_samples/`
2. OpenAI API key is correctly configured
3. All dependencies are installed
4. The vector store initializes successfully
