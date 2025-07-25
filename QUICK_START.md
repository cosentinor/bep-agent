# BEP Agent - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Test the Installation
```bash
python demo_simple.py
```
This runs a basic demo without requiring any API keys.

### Step 3: Configure for Full Features (Optional)
Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

Or use local embeddings (no API key needed):
```
USE_LOCAL_EMBEDDINGS=true
```

### Step 4: Launch the Web Interface
```bash
streamlit run main.py
```

### Step 5: Generate Your First BEP

1. **Initialize**: Click "Initialize/Rebuild Vector Store" in the sidebar
2. **Project Input**: Describe your project (e.g., "10-story office building with MEP coordination")
3. **Analysis**: Review similar existing plans and relevant content
4. **Outline**: Generate and customize the BEP outline
5. **Generate**: Create full content and download as Markdown or JSON

## 📁 File Structure Overview

```
BEP Agent DEV/
├── main.py                 # 🌐 Web interface
├── demo_simple.py          # 🎯 Simple demo
├── bep_processor.py        # 🧠 Main logic
├── document_loader.py      # 📄 Document processing
├── vector_store.py         # 🔍 Similarity search
├── outline_generator.py    # ✍️ AI content generation
├── config.py              # ⚙️ Configuration
├── requirements.txt       # 📦 Dependencies
├── .env                   # 🔐 Environment variables
└── data/
    ├── bep_samples/       # 📚 Sample BEP documents
    ├── new_project/       # 📋 Project requirements
    └── vector_store/      # 💾 Cached data
```

## 🎯 Usage Examples

### Example 1: Office Building
**Input**: "New 15-story office building in downtown area requiring BIM coordination for architectural, structural, and MEP systems. LEED Gold certification required."

**Output**: Tailored BEP with sections for sustainability, high-rise coordination, and urban construction considerations.

### Example 2: Healthcare Facility
**Input**: "200-bed hospital with complex MEP systems, medical gas, and specialized equipment. Strict regulatory compliance required."

**Output**: BEP focused on healthcare-specific requirements, regulatory compliance, and specialized systems coordination.

### Example 3: Educational Building
**Input**: "University science building with laboratories, lecture halls, and research facilities. Phased construction during academic year."

**Output**: BEP emphasizing phased construction, specialized lab requirements, and academic schedule coordination.

## 🔧 Configuration Options

### Environment Variables (.env)
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_key_here

# Embedding Options
USE_LOCAL_EMBEDDINGS=false    # true for local, false for OpenAI

# Processing Parameters
CHUNK_SIZE=1000              # Text chunk size
CHUNK_OVERLAP=200            # Overlap between chunks
TOP_K_CHUNKS=5               # Relevant chunks to retrieve
TOP_K_PLANS=3                # Similar plans to consider
```

### Model Configuration (config.py)
- **GPT Model**: gpt-3.5-turbo (configurable)
- **Embedding Model**: text-embedding-ada-002 (OpenAI) or all-MiniLM-L6-v2 (local)
- **Temperature**: 0.7 (creativity level)
- **Max Tokens**: 2000 (response length)

## 📊 Understanding the Process

### 1. Document Analysis
- Loads existing BEP documents from `data/bep_samples/`
- Extracts text, headings, and structure
- Creates searchable chunks with metadata

### 2. Vector Similarity
- Converts text to numerical vectors (embeddings)
- Builds FAISS index for fast similarity search
- Computes document-level similarity scores

### 3. AI Generation
- Uses GPT to generate project-specific outlines
- Creates detailed section content based on context
- Maintains professional BEP language and structure

### 4. Export Options
- **Markdown**: Human-readable format for editing
- **JSON**: Structured data for integration with other tools

## 🛠️ Troubleshooting

### Common Issues

**"No sample documents found"**
- Add .docx files to `data/bep_samples/`
- A sample document is included for testing

**"OpenAI API key not configured"**
- Add your API key to `.env` file
- Or set `USE_LOCAL_EMBEDDINGS=true`

**"sentence-transformers import error"**
- This is optional for local embeddings
- Use OpenAI embeddings instead
- Or install: `pip install h5py tensorflow`

**"FAISS index not built"**
- Click "Initialize/Rebuild Vector Store" in the sidebar
- Ensure sample documents are available

### Performance Tips

- **Faster Processing**: Use OpenAI embeddings (requires API key)
- **No API Costs**: Use local embeddings (slower but free)
- **Better Results**: Add more diverse sample BEP documents
- **Faster Startup**: Vector store is cached after first build

## 📚 Adding Your Own BEP Documents

1. **Collect BEPs**: Gather existing BEP documents in DOCX format
2. **Anonymize**: Remove sensitive project information if needed
3. **Add to Samples**: Place files in `data/bep_samples/`
4. **Rebuild Index**: Click "Initialize/Rebuild Vector Store"
5. **Test**: Generate a new BEP to see improved results

### Best Sample Documents
- **Diverse Project Types**: Office, residential, industrial, healthcare
- **Various Sizes**: Small, medium, large projects
- **Different Phases**: Design, construction, operations
- **Complete Structure**: Well-organized with clear headings
- **Recent Standards**: Up-to-date BIM practices and standards

## 🎉 Success Indicators

You'll know the system is working well when:

- ✅ Multiple sample documents load successfully
- ✅ Vector store builds without errors
- ✅ Project analysis finds relevant similar plans
- ✅ Generated outlines are logical and comprehensive
- ✅ Section content is relevant and professional
- ✅ Export functions produce usable documents

## 📞 Getting Help

1. **Check the logs**: Look for error messages in the terminal
2. **Run tests**: Use `python test_installation.py`
3. **Try simple demo**: Use `python demo_simple.py`
4. **Review documentation**: Check README.md for detailed information
5. **Verify configuration**: Ensure .env file is properly set up

Happy BEP generating! 🏗️✨
