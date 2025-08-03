"""
Main Streamlit application for BEP Agent.
Provides web interface for BIM Execution Plan generation.
"""

import streamlit as st
import os
import tempfile
from datetime import datetime
from bep_processor import BEPProcessor
from config import Config
from __version__ import __version__
from ui_styling import (
    load_atkinsrealis_styling,
    create_atkinsrealis_header,
    create_atkinsrealis_card,
    create_atkinsrealis_footer
)

# Page configuration
st.set_page_config(
    page_title="BEP Agent - Atkinsrealis BIM Execution Plan Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Atkinsrealis custom styling
load_atkinsrealis_styling()

# Initialize session state
if 'processor' not in st.session_state:
    st.session_state.processor = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'outline' not in st.session_state:
    st.session_state.outline = None
if 'bep_content' not in st.session_state:
    st.session_state.bep_content = None

def initialize_processor():
    """Initialize the BEP processor."""
    if st.session_state.processor is None:
        with st.spinner("Initializing BEP Agent..."):
            try:
                processor = BEPProcessor()
                success = processor.initialize()
                if success:
                    st.session_state.processor = processor
                    st.success("BEP Agent initialized successfully!")
                    return True
                else:
                    st.error("Failed to initialize BEP Agent. Please check your configuration and sample documents.")
                    return False
            except Exception as e:
                st.error(f"Error initializing BEP Agent: {str(e)}")
                return False
    return True

def main():
    """Main application function."""
    
    # Custom Atkinsrealis Header
    create_atkinsrealis_header(
        title="BEP Agent",
        subtitle="AI-Powered BIM Execution Plan Generator",
        version=__version__
    )
    
    # Sidebar for configuration and status
    with st.sidebar:
        st.header("Configuration")
        
        # Check if OpenAI API key is configured
        if not Config.OPENAI_API_KEY and not Config.USE_LOCAL_EMBEDDINGS:
            st.error("⚠️ OpenAI API key not configured!")
            st.info("Please set your OPENAI_API_KEY in the .env file or enable local embeddings.")
            return
        
        # Display configuration status
        st.success("✅ Configuration OK")
        
        if Config.USE_LOCAL_EMBEDDINGS:
            st.info("🔧 Using local embeddings")
        else:
            st.info("🌐 Using OpenAI embeddings")
        
        # Initialize processor
        if st.button("Initialize/Rebuild Vector Store", type="primary"):
            st.session_state.processor = None
            initialize_processor()
        
        # Show processor status
        if st.session_state.processor:
            stats = st.session_state.processor.get_processing_stats()
            st.success("✅ Processor Ready")
            st.metric("Documents Loaded", stats['documents_loaded'])
            st.metric("Text Chunks", stats['chunks_created'])
            st.metric("Vector Store Size", stats['vector_store_size'])
        else:
            st.warning("⏳ Processor not initialized")
    
    # Main content area
    if not st.session_state.processor:
        st.info("👈 Please initialize the BEP Agent using the sidebar.")
        
        # Show sample documents info
        st.subheader("📁 Sample Documents")
        if os.path.exists(Config.BEP_SAMPLES_DIR):
            sample_files = [f for f in os.listdir(Config.BEP_SAMPLES_DIR)
                           if f.endswith('.docx') or f.endswith('.pdf')]
            if sample_files:
                st.write(f"Found {len(sample_files)} sample BEP documents:")
                for file in sample_files:
                    file_type = "📄 PDF" if file.endswith('.pdf') else "📝 DOCX"
                    st.write(f"- {file_type} {file}")
            else:
                st.warning("No sample BEP documents found. Please add .docx or .pdf files to the data/bep_samples directory.")
        else:
            st.warning("Sample documents directory not found.")
        
        return
    
    # Tabs for different stages
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Project Input", "🔍 Analysis", "📋 Outline", "📄 Generate BEP"])
    
    with tab1:
        st.header("Project Requirements")
        
        # Project description input
        project_description = st.text_area(
            "Project Description",
            placeholder="Describe your project: type, size, complexity, special requirements, etc.",
            height=150,
            help="Provide a detailed description of your project to get the most relevant BEP recommendations."
        )
        
        # Project requirements - both text and file upload
        st.subheader("Project Requirements")

        # Multiple file upload for requirements
        uploaded_files = st.file_uploader(
            "Upload Requirements Documents (Optional)",
            type=['docx', 'pdf', 'txt'],
            accept_multiple_files=True,
            help="Upload RFP, EIR, or other requirements documents. You can upload multiple files."
        )

        # Additional BEP samples upload
        st.subheader("Additional BEP Samples (Optional)")
        uploaded_bep_samples = st.file_uploader(
            "Upload Additional BEP Documents",
            type=['docx', 'pdf'],
            accept_multiple_files=True,
            help="Upload additional BEP documents to improve analysis. These will be temporarily added to your sample library."
        )
        
        # Process requirements
        if st.button("Analyze Project Requirements", type="primary", disabled=not project_description.strip()):
            if project_description.strip():
                with st.spinner("Analyzing project requirements..."):
                    try:
                        # Handle uploaded files (multiple)
                        requirements_files = []
                        if uploaded_files:
                            for uploaded_file in uploaded_files:
                                # Save uploaded file temporarily
                                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                                    tmp_file.write(uploaded_file.getvalue())
                                    requirements_files.append(tmp_file.name)

                        # Handle additional BEP samples
                        additional_bep_files = []
                        if uploaded_bep_samples:
                            for bep_file in uploaded_bep_samples:
                                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{bep_file.name.split('.')[-1]}") as tmp_file:
                                    tmp_file.write(bep_file.getvalue())
                                    additional_bep_files.append(tmp_file.name)
                        
                        # Analyze requirements
                        analysis_results = st.session_state.processor.analyze_project_requirements(
                            project_description, requirements_files, additional_bep_files
                        )
                        st.session_state.analysis_results = analysis_results

                        # Clean up temporary files
                        for temp_file in requirements_files + additional_bep_files:
                            if temp_file and os.path.exists(temp_file):
                                os.unlink(temp_file)
                        
                        st.success("✅ Project requirements analyzed successfully!")
                        st.info("👉 Check the Analysis tab to see results.")
                        
                    except Exception as e:
                        st.error(f"Error analyzing requirements: {str(e)}")
    
    with tab2:
        st.header("Analysis Results")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results

            # Show uploaded files summary
            if results.get('requirements_count', 0) > 0 or results.get('additional_bep_count', 0) > 0:
                st.subheader("📁 Uploaded Files Summary")
                col1, col2 = st.columns(2)
                with col1:
                    if results.get('requirements_count', 0) > 0:
                        st.metric("Requirements Documents", results['requirements_count'])
                with col2:
                    if results.get('additional_bep_count', 0) > 0:
                        st.metric("Additional BEP Samples", results['additional_bep_count'])

                # Show additional BEP documents if any
                if results.get('additional_documents'):
                    with st.expander("📋 Additional BEP Documents Processed"):
                        for doc in results['additional_documents']:
                            file_type = "📄 PDF" if doc['file_type'] == 'pdf' else "📝 DOCX"
                            st.write(f"- {file_type} **{doc['filename']}** ({doc['word_count']} words, {len(doc['headings'])} headings)")

            # Similar plans
            st.subheader("🎯 Most Similar BEP Plans")
            similar_plans = results['similar_plans']
            
            if similar_plans:
                for i, (filename, similarity) in enumerate(similar_plans):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{i+1}. {filename}**")
                    with col2:
                        st.metric("Similarity", f"{similarity:.3f}")
            else:
                st.warning("No similar plans found.")
            
            # Relevant chunks
            st.subheader("📚 Most Relevant Content Sections")
            relevant_chunks = results['relevant_chunks']
            
            if relevant_chunks:
                for i, chunk in enumerate(relevant_chunks[:3]):  # Show top 3
                    with st.expander(f"Section {i+1}: {chunk.get('relevant_heading', 'General')} (Score: {chunk.get('similarity_score', 0):.3f})"):
                        st.write(f"**Source:** {chunk.get('source_file', 'Unknown')}")
                        st.write(f"**Content Preview:**")
                        st.write(chunk.get('text', '')[:500] + "..." if len(chunk.get('text', '')) > 500 else chunk.get('text', ''))
            
            # Generate outline button
            if st.button("Generate BEP Outline", type="primary"):
                with st.spinner("Generating BEP outline..."):
                    try:
                        outline = st.session_state.processor.generate_bep_outline(results)
                        st.session_state.outline = outline
                        st.success("✅ BEP outline generated successfully!")
                        st.info("👉 Check the Outline tab to review and customize.")
                    except Exception as e:
                        st.error(f"Error generating outline: {str(e)}")
        else:
            st.info("👈 Please analyze project requirements first.")
    
    with tab3:
        st.header("BEP Outline")
        
        if st.session_state.outline:
            st.subheader("📋 Generated Outline")
            
            # Display and allow editing of outline
            outline_text = "\n".join(st.session_state.outline)
            edited_outline = st.text_area(
                "Edit Outline (one heading per line)",
                value=outline_text,
                height=400,
                help="You can modify the outline by editing the text. Each line should be a section heading."
            )
            
            # Update outline if edited
            if edited_outline != outline_text:
                st.session_state.outline = [line.strip() for line in edited_outline.split('\n') if line.strip()]
            
            # Show outline preview
            st.subheader("📖 Outline Preview")
            for i, heading in enumerate(st.session_state.outline, 1):
                st.write(f"{i}. {heading}")
            
            # Generate content button
            if st.button("Generate BEP Content", type="primary"):
                with st.spinner("Generating BEP content... This may take a few minutes."):
                    try:
                        bep_content = st.session_state.processor.generate_bep_content(
                            st.session_state.analysis_results,
                            st.session_state.outline
                        )
                        st.session_state.bep_content = bep_content
                        st.success("✅ BEP content generated successfully!")
                        st.info("👉 Check the Generate BEP tab to review and download.")
                    except Exception as e:
                        st.error(f"Error generating content: {str(e)}")
        else:
            st.info("👈 Please generate an outline first.")
    
    with tab4:
        st.header("Generated BEP")
        
        if st.session_state.bep_content and st.session_state.outline:
            # Project name input
            project_name = st.text_input("Project Name", value="New BIM Project")
            
            # Display generated content
            st.subheader("📄 BEP Content Preview")
            
            # Show content in expandable sections
            for i, heading in enumerate(st.session_state.outline, 1):
                with st.expander(f"{i}. {heading}"):
                    content = st.session_state.bep_content.get(heading, "Content not generated.")
                    st.write(content)
            
            # Export options
            st.subheader("💾 Export Options")

            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Markdown export
                if st.button("📝 Export as Markdown"):
                    markdown_content = st.session_state.processor.export_bep_markdown(
                        st.session_state.outline,
                        st.session_state.bep_content,
                        project_name
                    )
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"BEP_{project_name.replace(' ', '_')}_{timestamp}.md"
                    
                    st.download_button(
                        label="📥 Download Markdown",
                        data=markdown_content,
                        file_name=filename,
                        mime="text/markdown"
                    )
            
            with col2:
                # JSON export
                if st.button("📊 Export as JSON"):
                    json_content = st.session_state.processor.export_bep_json(
                        st.session_state.outline,
                        st.session_state.bep_content,
                        st.session_state.analysis_results,
                        project_name
                    )

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"BEP_{project_name.replace(' ', '_')}_{timestamp}.json"

                    st.download_button(
                        label="📥 Download JSON",
                        data=json_content,
                        file_name=filename,
                        mime="application/json"
                    )

            with col3:
                # DOCX export
                if st.button("📄 Export as DOCX"):
                    try:
                        docx_path = st.session_state.processor.export_bep_docx(
                            st.session_state.outline,
                            st.session_state.bep_content,
                            st.session_state.analysis_results,
                            project_name
                        )

                        if docx_path and os.path.exists(docx_path):
                            with open(docx_path, 'rb') as f:
                                docx_data = f.read()

                            st.download_button(
                                label="📥 Download DOCX",
                                data=docx_data,
                                file_name=os.path.basename(docx_path),
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )

                            # Clean up temporary file
                            os.unlink(docx_path)
                            st.success("✅ DOCX file generated successfully!")
                        else:
                            st.error("❌ Failed to generate DOCX file")
                    except Exception as e:
                        st.error(f"❌ Error generating DOCX: {str(e)}")
        else:
            st.info("👈 Please generate BEP content first.")
    
    # Atkinsrealis Footer
    create_atkinsrealis_footer()
if __name__ == "__main__":
    # Auto-initialize on startup
    if st.session_state.processor is None:
        initialize_processor()
    
    main()
