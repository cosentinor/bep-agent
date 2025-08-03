"""
Interactive outline refiner module for document outline learning.
Streamlit app for refining and editing hierarchical outlines with drag-and-drop functionality.
"""

import os
import sys
import json
import streamlit as st
from typing import Dict, List, Optional
import uuid


class OutlineRefiner:
    """Interactive outline refiner using Streamlit."""
    
    def __init__(self):
        """Initialize the outline refiner."""
        self.outline = None
        self.modified = False
    
    def load_outline(self, outline_path: str) -> bool:
        """
        Load outline from JSON file.
        
        Args:
            outline_path: Path to outline JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(outline_path, 'r', encoding='utf-8') as f:
                self.outline = json.load(f)
            return True
        except Exception as e:
            st.error(f"Error loading outline: {str(e)}")
            return False
    
    def save_outline(self, output_path: str) -> bool:
        """
        Save refined outline to JSON file.
        
        Args:
            output_path: Path to save the refined outline
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.outline, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            st.error(f"Error saving outline: {str(e)}")
            return False
    
    def render_outline_editor(self):
        """Render the interactive outline editor."""
        if not self.outline:
            st.error("No outline loaded")
            return
        
        st.title("📝 Interactive Outline Refiner")
        
        # Display outline metadata
        if 'metadata' in self.outline:
            with st.expander("📊 Outline Metadata"):
                metadata = self.outline['metadata']
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Source Documents", len(metadata.get('source_documents', [])))
                    st.metric("Total Nodes", metadata.get('total_nodes_considered', 0))
                
                with col2:
                    st.text(f"Generation Method: {metadata.get('generation_method', 'unknown')}")
                    if metadata.get('source_documents'):
                        st.text("Source Documents:")
                        for doc in metadata['source_documents']:
                            st.text(f"  • {doc}")
        
        # Outline title editor
        st.subheader("📋 Outline Title")
        new_title = st.text_input(
            "Title", 
            value=self.outline.get('title', 'Project Outline'),
            key="outline_title"
        )
        
        if new_title != self.outline.get('title'):
            self.outline['title'] = new_title
            self.modified = True
        
        # Sections editor
        st.subheader("📑 Sections")
        
        # Add new section button
        if st.button("➕ Add New Section"):
            self._add_new_section()
            self.modified = True
            st.rerun()
        
        # Render existing sections
        if 'sections' in self.outline:
            self._render_sections_editor()
        
        # Save/Export controls
        st.divider()
        self._render_save_controls()
    
    def _render_sections_editor(self):
        """Render the sections editor with drag-and-drop simulation."""
        sections = self.outline.get('sections', [])
        
        for i, section in enumerate(sections):
            with st.container():
                col1, col2, col3, col4 = st.columns([0.1, 0.6, 0.2, 0.1])
                
                with col1:
                    # Move up/down buttons
                    if st.button("⬆️", key=f"up_{i}", disabled=(i == 0)):
                        self._move_section(i, i - 1)
                        self.modified = True
                        st.rerun()
                    
                    if st.button("⬇️", key=f"down_{i}", disabled=(i == len(sections) - 1)):
                        self._move_section(i, i + 1)
                        self.modified = True
                        st.rerun()
                
                with col2:
                    # Section title editor
                    new_title = st.text_input(
                        f"Section {i + 1}",
                        value=section.get('title', ''),
                        key=f"section_title_{i}"
                    )
                    
                    if new_title != section.get('title'):
                        section['title'] = new_title
                        self.modified = True
                
                with col3:
                    # Level selector
                    current_level = section.get('level', 1)
                    new_level = st.selectbox(
                        "Level",
                        options=[1, 2, 3],
                        index=current_level - 1,
                        key=f"section_level_{i}"
                    )
                    
                    if new_level != current_level:
                        section['level'] = new_level
                        self.modified = True
                
                with col4:
                    # Delete button
                    if st.button("🗑️", key=f"delete_{i}"):
                        self._delete_section(i)
                        self.modified = True
                        st.rerun()
                
                # Subsections editor
                if section.get('subsections'):
                    with st.expander(f"📂 Subsections for '{section['title']}'"):
                        self._render_subsections_editor(section, i)
                
                # Add subsection button
                if st.button(f"➕ Add Subsection to '{section['title']}'", key=f"add_sub_{i}"):
                    self._add_subsection(section)
                    self.modified = True
                    st.rerun()
                
                st.divider()
    
    def _render_subsections_editor(self, parent_section: Dict, parent_index: int):
        """Render subsections editor."""
        subsections = parent_section.get('subsections', [])
        
        for j, subsection in enumerate(subsections):
            col1, col2, col3, col4 = st.columns([0.1, 0.6, 0.2, 0.1])
            
            with col1:
                # Move subsection up/down
                if st.button("⬆️", key=f"sub_up_{parent_index}_{j}", disabled=(j == 0)):
                    self._move_subsection(parent_section, j, j - 1)
                    self.modified = True
                    st.rerun()
                
                if st.button("⬇️", key=f"sub_down_{parent_index}_{j}", disabled=(j == len(subsections) - 1)):
                    self._move_subsection(parent_section, j, j + 1)
                    self.modified = True
                    st.rerun()
            
            with col2:
                # Subsection title
                new_title = st.text_input(
                    f"Subsection {j + 1}",
                    value=subsection.get('title', ''),
                    key=f"subsection_title_{parent_index}_{j}"
                )
                
                if new_title != subsection.get('title'):
                    subsection['title'] = new_title
                    self.modified = True
            
            with col3:
                # Subsection level
                current_level = subsection.get('level', 2)
                new_level = st.selectbox(
                    "Level",
                    options=[2, 3, 4],
                    index=min(current_level - 2, 2),
                    key=f"subsection_level_{parent_index}_{j}"
                )
                
                if new_level != current_level:
                    subsection['level'] = new_level
                    self.modified = True
            
            with col4:
                # Delete subsection
                if st.button("🗑️", key=f"delete_sub_{parent_index}_{j}"):
                    self._delete_subsection(parent_section, j)
                    self.modified = True
                    st.rerun()
    
    def _add_new_section(self):
        """Add a new section to the outline."""
        new_section = {
            'title': 'New Section',
            'level': 1,
            'source_similarity': 0.0,
            'frequency': 1,
            'subsections': []
        }
        
        if 'sections' not in self.outline:
            self.outline['sections'] = []
        
        self.outline['sections'].append(new_section)
    
    def _add_subsection(self, parent_section: Dict):
        """Add a new subsection to a parent section."""
        new_subsection = {
            'title': 'New Subsection',
            'level': 2,
            'source_similarity': 0.0,
            'frequency': 1
        }
        
        if 'subsections' not in parent_section:
            parent_section['subsections'] = []
        
        parent_section['subsections'].append(new_subsection)
    
    def _move_section(self, from_index: int, to_index: int):
        """Move a section to a different position."""
        sections = self.outline['sections']
        section = sections.pop(from_index)
        sections.insert(to_index, section)
    
    def _move_subsection(self, parent_section: Dict, from_index: int, to_index: int):
        """Move a subsection to a different position."""
        subsections = parent_section['subsections']
        subsection = subsections.pop(from_index)
        subsections.insert(to_index, subsection)
    
    def _delete_section(self, index: int):
        """Delete a section from the outline."""
        del self.outline['sections'][index]
    
    def _delete_subsection(self, parent_section: Dict, index: int):
        """Delete a subsection from a parent section."""
        del parent_section['subsections'][index]
    
    def _render_save_controls(self):
        """Render save and export controls."""
        st.subheader("💾 Save & Export")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save as Draft", type="secondary"):
                if self.save_outline("outline_draft.json"):
                    st.success("Draft saved successfully!")
                    self.modified = False
        
        with col2:
            if st.button("✅ Confirm Final", type="primary"):
                if self.save_outline("outline_final.json"):
                    st.success("Final outline saved successfully!")
                    st.balloons()
                    self.modified = False
        
        with col3:
            # Download button
            if self.outline:
                outline_json = json.dumps(self.outline, indent=2, ensure_ascii=False)
                st.download_button(
                    label="📥 Download JSON",
                    data=outline_json,
                    file_name="refined_outline.json",
                    mime="application/json"
                )
        
        # Show modification status
        if self.modified:
            st.warning("⚠️ You have unsaved changes")
        else:
            st.info("✅ All changes saved")


def main():
    """Main Streamlit app entry point."""
    st.set_page_config(
        page_title="Interactive Outline Refiner",
        page_icon="📝",
        layout="wide"
    )
    
    # Initialize session state
    if 'refiner' not in st.session_state:
        st.session_state.refiner = OutlineRefiner()
    
    refiner = st.session_state.refiner
    
    # Sidebar for file operations
    with st.sidebar:
        st.title("📁 File Operations")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Outline JSON",
            type=['json'],
            help="Upload a draft outline JSON file to edit"
        )
        
        if uploaded_file is not None:
            try:
                outline_data = json.load(uploaded_file)
                refiner.outline = outline_data
                refiner.modified = False
                st.success("Outline loaded successfully!")
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
        
        # Command line argument handling
        if len(sys.argv) > 1:
            outline_path = sys.argv[1]
            if os.path.exists(outline_path):
                if refiner.load_outline(outline_path):
                    st.success(f"Loaded outline from: {outline_path}")
            else:
                st.error(f"File not found: {outline_path}")
        
        # Instructions
        st.markdown("""
        ### 📖 Instructions
        
        1. **Upload** or load an outline JSON file
        2. **Edit** section titles and levels
        3. **Reorder** sections using ⬆️⬇️ buttons
        4. **Add/Delete** sections and subsections
        5. **Save** your changes when done
        
        ### 🎯 Tips
        - Use Level 1 for main sections
        - Use Level 2-3 for subsections
        - Drag sections to reorder them
        - Save frequently to avoid losing changes
        """)
    
    # Main content area
    if refiner.outline:
        refiner.render_outline_editor()
    else:
        st.title("📝 Interactive Outline Refiner")
        st.info("👈 Please upload an outline JSON file using the sidebar to get started.")
        
        # Show example outline structure
        with st.expander("📋 Example Outline Structure"):
            example = {
                "title": "Example Project Outline",
                "sections": [
                    {
                        "title": "Executive Summary",
                        "level": 1,
                        "subsections": [
                            {"title": "Project Overview", "level": 2},
                            {"title": "Key Objectives", "level": 2}
                        ]
                    },
                    {
                        "title": "Implementation Plan",
                        "level": 1,
                        "subsections": []
                    }
                ]
            }
            st.json(example)


if __name__ == "__main__":
    main()
