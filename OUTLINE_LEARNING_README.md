# Outline Learning Enhancement

This document describes the new outline learning capabilities added to the BEP Agent project. The enhancement includes four Python packages that work together to extract, index, suggest, and refine document outlines.

## Overview

The outline learning system consists of:

1. **Structure Extractor** - Extracts hierarchical structure from DOCX and PDF documents
2. **Structure Indexer** - Creates searchable FAISS index of document structures
3. **Outline Suggester** - Suggests outlines based on requirements and indexed structures
4. **Interactive Refiner** - Streamlit app for refining and editing outlines

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install with development dependencies:

```bash
pip install -e ".[dev]"
```

## CLI Tools

### 1. Structure Indexer

Creates a FAISS index of document structures for fast similarity search.

**Usage:**
```bash
python -m src.structure_indexer --in_dir samples/ --out index
```

**Parameters:**
- `--in_dir`: Directory containing documents to index (supports .docx and .pdf)
- `--out`: Output path for index files (without extension)
- `--api_key`: OpenAI API key (optional, uses OPENAI_API_KEY env var)

**Output Files:**
- `index.faiss` - FAISS vector index
- `index_metadata.json` - Metadata for indexed structures

**Example:**
```bash
# Index all documents in the samples directory
python -m src.structure_indexer --in_dir data/bep_samples --out data/structure_index

# Use custom API key
python -m src.structure_indexer --in_dir samples/ --out index --api_key your_api_key_here
```

### 2. Outline Suggester

Generates hierarchical outline suggestions based on requirements documents and indexed structures.

**Usage:**
```bash
python -m src.outline_suggester --faiss index.faiss --requirements rfp.pdf --top_k 5 --out draft_outline.json
```

**Parameters:**
- `--faiss`: Path to FAISS index file
- `--metadata`: Path to metadata JSON file (optional, auto-detected if not provided)
- `--requirements`: Path to requirements document (PDF or DOCX)
- `--top_k`: Number of top similar headings to consider (default: 5)
- `--out`: Output path for draft outline JSON
- `--api_key`: OpenAI API key (optional, uses OPENAI_API_KEY env var)

**Example:**
```bash
# Generate outline from requirements
python -m src.outline_suggester \
    --faiss data/structure_index.faiss \
    --requirements data/new_project/requirements.pdf \
    --top_k 10 \
    --out draft_outline.json

# Use custom metadata file
python -m src.outline_suggester \
    --faiss index.faiss \
    --metadata custom_metadata.json \
    --requirements requirements.docx \
    --out outline.json
```

### 3. Interactive Refiner

Streamlit web application for interactively refining and editing outlines.

**Usage:**
```bash
streamlit run src/interactive_refiner.py draft_outline.json
```

**Features:**
- Edit section titles and hierarchy levels
- Reorder sections with up/down buttons
- Add and delete sections and subsections
- Drag-and-drop functionality simulation
- Save as draft or final outline
- Download refined outline as JSON

**Example:**
```bash
# Launch refiner with draft outline
streamlit run src/interactive_refiner.py draft_outline.json

# Launch refiner without initial file (upload via UI)
streamlit run src/interactive_refiner.py
```

## Python API

### Structure Extractor

```python
from src.structure_extractor import StructureExtractor, extract

# Auto-detect document type
nodes = extract("document.pdf")

# Use specific parsers
extractor = StructureExtractor()
docx_nodes = extractor.parse_docx("document.docx")
pdf_nodes = extractor.parse_pdf("document.pdf")

# Node structure
for node in nodes:
    print(f"Level {node.level}: {node.title}")
    print(f"Content: {node.text_span[:100]}...")
```

### Structure Indexer

```python
from src.structure_indexer import StructureIndexer

# Create and build index
indexer = StructureIndexer(openai_api_key="your_key")
indexer.index_directory("samples/", "my_index")

# Load existing index and search
indexer.load_index("my_index.faiss")
results = indexer.search("project management", top_k=5)

for result in results:
    print(f"{result['title']} (similarity: {result['similarity_score']:.3f})")
```

### Outline Suggester

```python
from src.outline_suggester import OutlineSuggester

# Create suggester
suggester = OutlineSuggester("index.faiss", "metadata.json")

# Generate outline
outline = suggester.suggest_outline("requirements.pdf", top_k=10)

print(f"Generated outline: {outline['title']}")
for section in outline['sections']:
    print(f"- {section['title']} (Level {section['level']})")
```

## Workflow Example

Here's a complete workflow example:

```bash
# 1. Index existing BEP documents
python -m src.structure_indexer \
    --in_dir data/bep_samples \
    --out data/bep_structure_index

# 2. Generate outline from new project requirements
python -m src.outline_suggester \
    --faiss data/bep_structure_index.faiss \
    --requirements data/new_project/project_requirements.pdf \
    --top_k 8 \
    --out data/new_project/draft_outline.json

# 3. Refine outline interactively
streamlit run src/interactive_refiner.py data/new_project/draft_outline.json

# 4. Use final outline in main BEP generation process
python main.py  # Will use outline_final.json if available
```

## Configuration

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Or create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

## File Formats

### Input Documents
- **DOCX**: Extracts headings from paragraph styles and regex patterns
- **PDF**: Extracts from table of contents and text patterns

### Output Formats

**Structure Index Metadata:**
```json
[
  {
    "id": "doc1_h1_1",
    "level": 1,
    "title": "Executive Summary",
    "text_span": "This document provides...",
    "doc_id": "sample.docx",
    "vector_id": 0
  }
]
```

**Outline JSON:**
```json
{
  "title": "Project Outline",
  "sections": [
    {
      "title": "Executive Summary",
      "level": 1,
      "source_similarity": 0.85,
      "frequency": 3,
      "subsections": [
        {
          "title": "Project Overview",
          "level": 2,
          "source_similarity": 0.78,
          "frequency": 1
        }
      ]
    }
  ],
  "metadata": {
    "source_documents": ["doc1.docx", "doc2.docx"],
    "total_nodes_considered": 15,
    "generation_method": "frequency_semantic_dedup"
  }
}
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python -m pytest tests/test_structure_extractor.py
python -m pytest tests/test_outline_merger.py

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Troubleshooting

**Common Issues:**

1. **Missing OpenAI API Key**
   ```
   Error: OpenAI API key is required
   ```
   Solution: Set the `OPENAI_API_KEY` environment variable

2. **Document Parsing Errors**
   ```
   Error parsing DOCX/PDF file
   ```
   Solution: Ensure documents are not corrupted and are in supported formats

3. **FAISS Index Not Found**
   ```
   Index file not found
   ```
   Solution: Run structure indexer first to create the index

4. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'fitz'
   ```
   Solution: Install PyMuPDF: `pip install PyMuPDF`

## Performance Notes

- **Indexing**: Processing time depends on document size and number of documents
- **Embedding**: Uses OpenAI's text-embedding-3-small model (1536 dimensions)
- **Memory**: FAISS index size scales with number of indexed structures
- **API Costs**: Embedding generation incurs OpenAI API costs

## Integration with Existing BEP Agent

The outline learning modules integrate seamlessly with the existing BEP Agent:

1. **Document Loading**: Leverages existing `DocumentLoader` for text extraction
2. **Vector Store**: Compatible with existing `VectorStore` class
3. **Configuration**: Uses existing `Config` class for settings
4. **Streamlit UI**: Can be integrated into the main Streamlit application

The generated outlines can be used by the existing `OutlineGenerator` to create more targeted and relevant BEP documents.
