"""
Custom UI styling for BEP Agent with Atkinsrealis branding.
"""

import streamlit as st

def load_atkinsrealis_styling():
    """Load Atkinsrealis custom styling and fonts."""
    
    # Atkinsrealis brand colors
    atkinsrealis_css = """
    <style>
    /* Import Atkinsrealis fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Atkinsrealis Color Palette */
    :root {
        --atkinsrealis-blue: #0066CC;
        --atkinsrealis-dark-blue: #003D7A;
        --atkinsrealis-light-blue: #4D94FF;
        --atkinsrealis-green: #00A651;
        --atkinsrealis-orange: #FF6B35;
        --atkinsrealis-gray: #6B7280;
        --atkinsrealis-light-gray: #F3F4F6;
        --atkinsrealis-white: #FFFFFF;
        --atkinsrealis-black: #1F2937;
    }
    
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Custom header styling */
    .atkinsrealis-header {
        background: linear-gradient(135deg, var(--atkinsrealis-blue) 0%, var(--atkinsrealis-dark-blue) 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .atkinsrealis-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: white !important;
    }
    
    .atkinsrealis-header h2 {
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
        color: #E5F3FF !important;
    }
    
    .atkinsrealis-header .version {
        font-family: 'Roboto', sans-serif;
        font-size: 0.9rem;
        color: #B3D9FF;
        font-weight: 300;
    }
    
    /* Custom fonts for all text */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--atkinsrealis-light-gray);
        border-right: 3px solid var(--atkinsrealis-blue);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--atkinsrealis-blue) 0%, var(--atkinsrealis-dark-blue) 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--atkinsrealis-dark-blue) 0%, var(--atkinsrealis-blue) 100%);
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.3);
        transform: translateY(-2px);
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--atkinsrealis-green) 0%, #008A43 100%);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #008A43 0%, var(--atkinsrealis-green) 100%);
        box-shadow: 0 4px 8px rgba(0, 166, 81, 0.3);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--atkinsrealis-light-gray);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: var(--atkinsrealis-gray);
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, var(--atkinsrealis-blue) 0%, var(--atkinsrealis-dark-blue) 100%);
        color: white !important;
        box-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
    }
    
    /* Metric styling */
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid var(--atkinsrealis-blue);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border: 2px dashed var(--atkinsrealis-blue);
        border-radius: 10px;
        background-color: #F8FAFF;
        padding: 2rem;
        text-align: center;
    }
    
    /* Success/Error message styling */
    .stSuccess {
        background-color: #F0FDF4;
        border-left: 4px solid var(--atkinsrealis-green);
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError {
        background-color: #FEF2F2;
        border-left: 4px solid var(--atkinsrealis-orange);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--atkinsrealis-light-gray);
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        color: var(--atkinsrealis-dark-blue);
    }
    
    /* Text area and input styling */
    .stTextArea > div > div > textarea {
        border: 2px solid var(--atkinsrealis-light-blue);
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input {
        border: 2px solid var(--atkinsrealis-light-blue);
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--atkinsrealis-blue) 0%, var(--atkinsrealis-green) 100%);
    }
    
    /* Custom card styling */
    .atkinsrealis-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #E5E7EB;
        margin: 1rem 0;
    }
    
    .atkinsrealis-card h3 {
        color: var(--atkinsrealis-dark-blue);
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Footer styling */
    .atkinsrealis-footer {
        background-color: var(--atkinsrealis-dark-blue);
        color: white;
        text-align: center;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 2rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom logo area */
    .atkinsrealis-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    .atkinsrealis-logo img {
        height: 60px;
        margin-right: 1rem;
    }
    </style>
    """
    
    st.markdown(atkinsrealis_css, unsafe_allow_html=True)

def create_atkinsrealis_header(title, subtitle, version):
    """Create a custom Atkinsrealis-branded header."""

    # Check for logo files in assets directory
    import os
    import base64

    logo_html = ""
    logo_files = [
        "assets/atkinsrealis-logo.png",
        "assets/atkinsrealis-logo.svg",
        "assets/atkinsrealis_logo.png",
        "assets/atkinsrealis_logo.svg",
        "assets/logo.png",
        "assets/logo.svg"
    ]

    logo_found = False
    for logo_path in logo_files:
        if os.path.exists(logo_path):
            try:
                if logo_path.endswith('.svg'):
                    # Handle SVG files
                    with open(logo_path, 'r', encoding='utf-8') as f:
                        svg_content = f.read()
                    logo_html = f'<div style="margin-right: 1rem; height: 60px;">{svg_content}</div>'
                else:
                    # Handle PNG/JPG files
                    with open(logo_path, 'rb') as f:
                        logo_data = f.read()
                    logo_base64 = base64.b64encode(logo_data).decode()
                    logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Atkinsrealis Logo" style="height: 60px; margin-right: 1rem;" />'
                logo_found = True
                break
            except Exception as e:
                print(f"Error loading logo {logo_path}: {e}")
                continue

    if not logo_found:
        # Fallback to Atkinsrealis text logo if no image found
        logo_html = '''
        <div style="margin-right: 1rem; display: flex; align-items: center;">
            <div style="
                background: linear-gradient(135deg, #FFFFFF 0%, #E5F3FF 100%);
                color: #003D7A;
                font-family: 'Inter', sans-serif;
                font-weight: 700;
                font-size: 1.2rem;
                padding: 8px 16px;
                border-radius: 8px;
                border: 2px solid #FFFFFF;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                ATKINSREALIS
            </div>
        </div>
        '''

    header_html = f"""
    <div class="atkinsrealis-header">
        <div class="atkinsrealis-logo">
            {logo_html}
        </div>
        <h1>{title}</h1>
        <h2>{subtitle}</h2>
        <div class="version">Version {version} | Powered by Atkinsrealis</div>
    </div>
    """

    st.markdown(header_html, unsafe_allow_html=True)

def create_atkinsrealis_card(title, content):
    """Create a custom Atkinsrealis-styled card."""
    
    card_html = f"""
    <div class="atkinsrealis-card">
        <h3>{title}</h3>
        <div>{content}</div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def create_atkinsrealis_footer():
    """Create a custom Atkinsrealis footer."""
    
    footer_html = """
    <div class="atkinsrealis-footer">
        <p>© 2025 Atkinsrealis | BIM Execution Plan Generator | Powered by AI</p>
        <p>Transforming Infrastructure Through Innovation</p>
    </div>
    """
    
    st.markdown(footer_html, unsafe_allow_html=True)
