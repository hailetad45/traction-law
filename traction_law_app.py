# ============================================================================
# TRACTION LAW CONTRACT ANALYZER
# Enterprise Edition v2.0
# ============================================================================

import streamlit as st
from openai import OpenAI
import tempfile
import os
from datetime import datetime
import PyPDF2
import docx
import hashlib
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
import time

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="TRACTION LAW - Contract Intelligence Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.tractionlaw.com/support',
        'Report a bug': 'https://www.tractionlaw.com/bug',
        'About': '# Traction Law Contract Analyzer\nProfessional Construction Contract Intelligence Platform v2.0'
    }
)

# ============================================================================
# CUSTOM CSS - PROFESSIONAL BRANDING
# ============================================================================

st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles - softer background for better contrast */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecf5 100%);
    }
    
    /* Main container - improved contrast */
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        margin: 1rem;
        color: #1a2639;
    }
    
    /* Header styles - keep vibrant but ensure white text */
    .traction-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white !important;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .traction-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        color: white !important;
    }
    
    .traction-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 300;
        color: white !important;
    }
    
    /* Feature badges - improved readability */
    .feature-badge {
        background: rgba(255,255,255,0.15);
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 500;
        display: inline-block;
        margin: 0.25rem;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Metric cards - improved text contrast */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.3s ease;
        border: 1px solid #e0e0e0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3c72 !important;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #2d3748 !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Contract cards - better text contrast */
    .contract-card {
        background: #ffffff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
        color: #1a2639 !important;
    }
    
    .contract-card:hover {
        background: #f8faff;
        border-left-width: 6px;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.15);
    }
    
    .contract-card b, .contract-card strong {
        color: #1e3c72 !important;
    }
    
    /* Alert styles - improved contrast */
    .success-alert {
        background: #d4edda;
        color: #155724 !important;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .warning-alert {
        background: #fff3cd;
        color: #856404 !important;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Button styles - keep vibrant */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        color: white !important;
    }
    
    /* Tab styling - improved text contrast */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: white;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: #2d3748 !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #667eea !important;
        border-bottom: 3px solid #667eea !important;
    }
    
    /* Footer - keep dark but ensure readability */
    .footer {
        background: #1a1a2e;
        color: rgba(255,255,255,0.9) !important;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
    }
    
    .footer a {
        color: #a0c0ff !important;
        text-decoration: none;
        font-weight: 500;
    }
    
    .footer a:hover {
        text-decoration: underline;
        color: white !important;
    }
    
    .footer div {
        color: rgba(255,255,255,0.9) !important;
    }
    
    /* Ensure all text has good contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #1a2639 !important;
    }
    
    p, li, span:not(.feature-badge) {
        color: #2d3748 !important;
    }
    
    .stMarkdown {
        color: #2d3748 !important;
    }
    
    /* Form elements - better visibility */
    .stTextInput label, .stSelectbox label, .stCheckbox label {
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
    
    /* DataFrame text */
    .stDataFrame {
        color: #2d3748 !important;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader {
        color: #1e3c72 !important;
        font-weight: 600 !important;
        background: #f8f9fa;
        border-radius: 5px;
    }
    
    /* Success/Info/Warning/Error messages - ensure contrast */
    .stSuccess {
        background: #d4edda !important;
        color: #155724 !important;
        font-weight: 500 !important;
    }
    
    .stInfo {
        background: #d1ecf1 !important;
        color: #0c5460 !important;
        font-weight: 500 !important;
    }
    
    .stWarning {
        background: #fff3cd !important;
        color: #856404 !important;
        font-weight: 500 !important;
    }
    
    .stError {
        background: #f8d7da !important;
        color: #721c24 !important;
        font-weight: 500 !important;
    }
    
    /* Keep header text white */
    .traction-header h1,
    .traction-header h2,
    .traction-header h3,
    .traction-header p,
    .traction-header span {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)
# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.uploaded_contracts = []
    st.session_state.analyses = []
    st.session_state.synthesis_history = []
    st.session_state.risk_scores = {}
    st.session_state.comparison_matrix = pd.DataFrame()
    st.session_state.user_preferences = {
        'jurisdiction': 'Ontario, Canada',
        'analysis_depth': 'Comprehensive',
        'include_case_law': True,
        'output_format': 'Legal Professional',
        'dark_mode': False
    }
    st.session_state.activity_log = []
    st.session_state.current_project = "Untitled Project"
    st.session_state.saved_projects = {}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def log_activity(activity):
    """Log user activity with timestamp"""
    st.session_state.activity_log.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'activity': activity
    })

def calculate_risk_score(analysis_text):
    """Calculate risk score based on analysis"""
    risk_keywords = {
        'high': ['dangerous', 'severe', 'critical', 'unacceptable', 'void'],
        'medium': ['caution', 'risk', 'exposure', 'concern', 'potential'],
        'low': ['standard', 'typical', 'acceptable', 'reasonable']
    }
    
    text_lower = analysis_text.lower()
    
    high_count = sum(1 for word in risk_keywords['high'] if word in text_lower)
    medium_count = sum(1 for word in risk_keywords['medium'] if word in text_lower)
    low_count = sum(1 for word in risk_keywords['low'] if word in text_lower)
    
    total = high_count + medium_count + low_count
    if total == 0:
        return 50
    
    score = (high_count * 100 + medium_count * 60 + low_count * 20) / total
    return min(100, max(0, score))

def save_project():
    """Save current session as a project"""
    project_data = {
        'contracts': st.session_state.uploaded_contracts,
        'analyses': st.session_state.analyses,
        'synthesis_history': st.session_state.synthesis_history,
        'preferences': st.session_state.user_preferences,
        'saved_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    project_name = st.session_state.current_project
    st.session_state.saved_projects[project_name] = project_data
    
    # Save to file
    with open(f'traction_law_project_{datetime.now().strftime("%Y%m%d")}.json', 'w') as f:
        json.dump(project_data, f, indent=2)
    
    return project_name

def load_project(project_name):
    """Load a saved project"""
    if project_name in st.session_state.saved_projects:
        project = st.session_state.saved_projects[project_name]
        st.session_state.uploaded_contracts = project['contracts']
        st.session_state.analyses = project['analyses']
        st.session_state.synthesis_history = project['synthesis_history']
        st.session_state.user_preferences = project['preferences']
        st.session_state.current_project = project_name
        return True
    return False

# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown("""
<div class="traction-header">
    <div class="traction-title">⚖️ TRACTION LAW</div>
    <div class="traction-subtitle">Contract Intelligence Platform | Enterprise Edition v2.0</div>
    <div style="margin-top: 1rem;">
        <span class="feature-badge">AI-Powered Analysis</span>
        <span class="feature-badge">Multi-Jurisdiction</span>
        <span class="feature-badge">Risk Scoring</span>
        <span class="feature-badge">Enterprise Security</span>
        <span class="feature-badge">Team Collaboration</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - PROFESSIONAL CONTROL PANEL
# ============================================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/contract.png", width=100)
    st.markdown("## **CONTROL PANEL**")
    st.markdown("---")
    
    # Project Management
    with st.expander("📁 **PROJECT MANAGEMENT**", expanded=True):
        st.text_input("Project Name:", value=st.session_state.current_project, key="project_name_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Project", use_container_width=True):
                saved = save_project()
                st.success(f"Saved: {saved}")
                log_activity(f"Saved project: {saved}")
        
        with col2:
            if st.button("📂 Load Project", use_container_width=True):
                projects = list(st.session_state.saved_projects.keys())
                if projects:
                    selected = st.selectbox("Select project:", projects)
                    if load_project(selected):
                        st.success(f"Loaded: {selected}")
                        log_activity(f"Loaded project: {selected}")
                        st.rerun()
    
    # ============================================================================
# API CONFIGURATION - FIXED & SECURE
# ============================================================================

with st.expander("🔑 **API CONFIGURATION**", expanded=True):
    
    # Try to get API key from secrets (safe) or environment
    api_key = None
    
    # Check secrets first (for deployment)
    try:
        if "DEEPSEEK_API_KEY" in st.secrets:
            api_key = st.secrets["DEEPSEEK_API_KEY"]
            st.success("✅ API key loaded from secrets!")
    except:
        pass  # No secrets file - that's fine
    
    # If no API key yet, ask user (for local development)
    if not api_key:
        api_key = st.text_input(
            "Enter your DeepSeek API Key:", 
            type="password",
            help="Your API key starts with 'sk-'. It will be kept private."
        )
        
        if not api_key:
            st.warning("⚠️ Please enter your API key to continue")
            st.stop()
        else:
            # Quick validation
            if not api_key.startswith('sk-'):
                st.error("❌ Invalid API key format - should start with 'sk-'")
                st.stop()
            st.success("✅ API key entered")
    
    # Test the connection
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        # Quick test
        test = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        st.success("✅ Connected to DeepSeek API")
    except Exception as e:
        st.error(f"❌ Connection failed: {e}")
        st.stop()
        
        # Connection status
        try:
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
            test = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            st.success("🟢 API Connected")
        except Exception as e:
            st.error("🔴 API Error")
            st.stop()
    
    # Jurisdiction & Settings
    with st.expander("🌍 **JURISDICTION & SETTINGS**", expanded=True):
        jurisdiction = st.selectbox(
            "Governing Law:",
            ["Ontario, Canada", "British Columbia, Canada", "Alberta, Canada", 
             "Quebec, Canada", "Federal (Canada)", "New York, USA", 
             "California, USA", "Texas, USA", "UK (England & Wales)", 
             "Australia (NSW)", "Singapore", "UAE (Dubai)", "International"],
            index=0
        )
        
        analysis_depth = st.select_slider(
            "Analysis Depth:",
            options=["Quick Scan", "Standard Review", "Deep Analysis", "Comprehensive"]
        )
        
        output_style = st.selectbox(
            "Output Style:",
            ["Legal Professional", "Business Executive", "Combined", "Plain Language"]
        )
        
        # Advanced settings
        with st.popover("⚙️ Advanced Settings"):
            include_case_law = st.checkbox("Include Case Law", value=True)
            include_risk_scores = st.checkbox("Calculate Risk Scores", value=True)
            include_comparison_matrix = st.checkbox("Generate Comparison Matrix", value=True)
            auto_save = st.checkbox("Auto-save Projects", value=True)
            dark_mode = st.checkbox("Dark Mode (Beta)", value=False)
    
    # Usage Statistics
    with st.expander("📊 **USAGE STATISTICS**"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Contracts", len(st.session_state.uploaded_contracts))
        with col2:
            st.metric("Analyses", len(st.session_state.analyses))
        st.metric("Syntheses", len(st.session_state.synthesis_history))
        st.metric("Risk Assessments", len(st.session_state.risk_scores))
    
    st.markdown("---")
    st.caption("© 2025 Traction Law Inc. All rights reserved.")
    st.caption("Enterprise License | Professional Use Only")

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">{}</div>
        <div class="metric-label">Contracts Loaded</div>
    </div>
    """.format(len(st.session_state.uploaded_contracts)), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">{}</div>
        <div class="metric-label">Clauses Analyzed</div>
    </div>
    """.format(sum(len(a.get('clauses', [])) for a in st.session_state.analyses)), unsafe_allow_html=True)

with col3:
    avg_risk = sum(st.session_state.risk_scores.values()) / len(st.session_state.risk_scores) if st.session_state.risk_scores else 0
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">{:.0f}</div>
        <div class="metric-label">Avg Risk Score</div>
    </div>
    """.format(avg_risk), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">{}</div>
        <div class="metric-label">Syntheses</div>
    </div>
    """.format(len(st.session_state.synthesis_history)), unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# MAIN TABS - PROFESSIONAL WORKSPACE
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📁 **CONTRACT HUB**",
    "🔍 **ANALYSIS STUDIO**",
    "✨ **SYNTHESIS ENGINE**",
    "📊 **RISK DASHBOARD**",
    "📚 **KNOWLEDGE BASE**",
    "👥 **TEAM WORKSPACE**"
])

# ============================================================================
# TAB 1: CONTRACT HUB
# ============================================================================

with tab1:
    st.markdown("## 📁 **Contract Management Hub**")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📤 **Document Import Center**")
        
        upload_method = st.radio(
            "Import Method:",
            ["📎 Upload Files", "✍️ Create Draft", "📋 Paste Text", "🔄 Import from Cloud"],
            horizontal=True
        )
        
        if upload_method == "📎 Upload Files":
            uploaded_files = st.file_uploader(
                "Drop files here or click to browse",
                type=['pdf', 'docx', 'txt'],
                accept_multiple_files=True,
                help="Upload PDF, DOCX, or TXT files (Max 25MB)"
            )
            
            if uploaded_files:
                with st.spinner("Processing documents..."):
                    for file in uploaded_files:
                        try:
                            if file.type == "application/pdf":
                                pdf_reader = PyPDF2.PdfReader(file)
                                text = ""
                                for page in pdf_reader.pages:
                                    text += page.extract_text()
                            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                                doc = docx.Document(file)
                                text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                            else:
                                text = file.getvalue().decode("utf-8")
                            
                            st.session_state.uploaded_contracts.append({
                                "id": hashlib.md5(f"{file.name}{datetime.now()}".encode()).hexdigest()[:8],
                                "name": file.name,
                                "text": text[:10000],
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "source": "upload",
                                "pages": len(text) // 2000 + 1,
                                "risk_score": None
                            })
                            log_activity(f"Uploaded contract: {file.name}")
                            st.success(f"✅ Processed: {file.name}")
                        except Exception as e:
                            st.error(f"Error: {file.name}")
        
        elif upload_method == "✍️ Create Draft":
            template_options = {
                "Blank Contract": "",
                "CCDC 2-2020 (Stipulated Price)": "THIS CONSTRUCTION CONTRACT is made on [DATE] between [OWNER] and [CONTRACTOR]...",
                "Owner-Friendly": "Owner retains right to withhold 15% holdback. No interest on late payments...",
                "Contractor-Friendly": "Payment due within 15 days, 2% monthly interest on late payments...",
                "FIDIC Red Book (Adapted)": "The Contractor shall execute the Works in accordance with the Contract..."
            }
            
            template = st.selectbox("Start from template:", list(template_options.keys()))
            contract_text = st.text_area("Contract editor:", value=template_options[template], height=300)
            contract_name = st.text_input("Contract name:", value=f"Draft_{datetime.now().strftime('%Y%m%d')}")
            
            if st.button("💾 Save Draft", type="primary"):
                st.session_state.uploaded_contracts.append({
                    "id": hashlib.md5(f"{contract_name}{datetime.now()}".encode()).hexdigest()[:8],
                    "name": contract_name,
                    "text": contract_text[:10000],
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "source": "draft",
                    "pages": len(contract_text) // 2000 + 1,
                    "risk_score": None
                })
                log_activity(f"Created draft: {contract_name}")
                st.success("✅ Draft saved!")
                st.balloons()
    
    with col2:
        st.markdown("### 📋 **Contract Library**")
        st.metric("Total Contracts", len(st.session_state.uploaded_contracts))
        
        if st.session_state.uploaded_contracts:
            st.markdown("**Recent Activity:**")
            for contract in st.session_state.uploaded_contracts[-3:]:
                st.markdown(f"• {contract['name'][:30]}...")
        
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.uploaded_contracts = []
            st.rerun()
    
    # Display contract library
    if st.session_state.uploaded_contracts:
        st.markdown("---")
        st.markdown("### 📚 **Contract Library**")
        
        # Search and filter
        search = st.text_input("🔍 Search contracts:", placeholder="Enter contract name...")
        
        filtered_contracts = [
            c for c in st.session_state.uploaded_contracts 
            if search.lower() in c['name'].lower()
        ] if search else st.session_state.uploaded_contracts
        
        for contract in filtered_contracts:
            with st.container():
                cols = st.columns([3, 1, 1, 1, 1])
                with cols[0]:
                    st.markdown(f"**{contract['name']}**")
                    st.caption(f"ID: {contract['id']} | Added: {contract['date']}")
                with cols[1]:
                    st.caption(f"📄 {contract['pages']} pages")
                with cols[2]:
                    if contract.get('risk_score'):
                        color = "🟢" if contract['risk_score'] < 30 else "🟡" if contract['risk_score'] < 70 else "🔴"
                        st.caption(f"{color} Risk: {contract['risk_score']:.0f}")
                with cols[3]:
                    if st.button("👁️ View", key=f"view_{contract['id']}"):
                        st.info(contract['text'][:1000] + "...")
                with cols[4]:
                    if st.button("🗑️", key=f"del_{contract['id']}"):
                        st.session_state.uploaded_contracts.remove(contract)
                        st.rerun()

# ============================================================================
# TAB 2: ANALYSIS STUDIO
# ============================================================================

with tab2:
    st.markdown("## 🔍 **AI Analysis Studio**")
    
    if not st.session_state.uploaded_contracts:
        st.warning("⚠️ Please load contracts in the Contract Hub first")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📌 **Select Contracts**")
            selected_contracts = []
            for contract in st.session_state.uploaded_contracts:
                if st.checkbox(f"📄 {contract['name']}", key=f"analyze_{contract['id']}"):
                    selected_contracts.append(contract)
        
        with col2:
            st.markdown("### ⚖️ **Select Clauses**")
            
            clause_categories = {
                "Payment & Financial": ["Payment Terms", "Holdback", "Interest", "Progress Payments"],
                "Risk & Liability": ["Indemnification", "Limitation of Liability", "Insurance"],
                "Project Disruptions": ["Force Majeure", "Delay Damages", "Change Orders"],
                "Legal & Compliance": ["Dispute Resolution", "Lien Rights", "Governing Law"],
                "Performance": ["Warranties", "Defects", "Subcontracting"],
                "Termination": ["Termination Rights", "Suspension", "Survival"]
            }
            
            selected_clauses = []
            for category, clauses in clause_categories.items():
                with st.expander(category):
                    for clause in clauses:
                        if st.checkbox(clause, key=f"clause_{clause}"):
                            selected_clauses.append(clause)
        
        # Analysis button
        if st.button("🚀 **RUN COMPREHENSIVE ANALYSIS**", type="primary", use_container_width=True):
            if len(selected_contracts) < 2:
                st.error("Please select at least 2 contracts")
            elif not selected_clauses:
                st.error("Please select at least 1 clause")
            else:
                with st.spinner("🧠 Traction AI analyzing contracts..."):
                    analyses = []
                    progress_bar = st.progress(0)
                    
                    for idx, contract in enumerate(selected_contracts):
                        prompt = f"""You are a senior construction law expert practicing in {jurisdiction}.

CONTRACT: {contract['name']}
TEXT: {contract['text'][:8000]}

ANALYZE THESE CLAUSES: {', '.join(selected_clauses)}

For EACH clause provide:
1. **SUMMARY** (1 line)
2. **FAVORS** (Owner/Contractor/Balanced) with reasoning
3. **STRENGTHS** (3 bullet points)
4. **WEAKNESSES** (3 bullet points)
5. **{jurisdiction} COMPLIANCE** (specific legal issues)
{f'6. **CASE LAW** (relevant precedents)' if include_case_law else ''}
6. **RISK LEVEL** (High/Medium/Low)
7. **NEGOTIATION TIP** (practical advice)

Analysis Depth: {analysis_depth}
Output Style: {output_style}"""
                        
                        try:
                            response = client.chat.completions.create(
                                model="deepseek-chat",
                                messages=[{"role": "user", "content": prompt}],
                                max_tokens=2000,
                                temperature=0.3
                            )
                            
                            analysis_text = response.choices[0].message.content
                            
                            # Calculate risk score
                            risk_score = calculate_risk_score(analysis_text)
                            contract['risk_score'] = risk_score
                            st.session_state.risk_scores[contract['id']] = risk_score
                            
                            analyses.append({
                                "id": contract['id'],
                                "name": contract['name'],
                                "analysis": analysis_text,
                                "clauses": selected_clauses,
                                "risk_score": risk_score,
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            
                        except Exception as e:
                            st.error(f"Error analyzing {contract['name']}")
                        
                        progress_bar.progress((idx + 1) / len(selected_contracts))
                    
                    st.session_state.analyses = analyses
                    log_activity(f"Ran analysis on {len(selected_contracts)} contracts")
                    st.success("✅ Analysis complete!")
                    
                    # Display results
                    st.markdown("---")
                    st.markdown("### 📊 **Analysis Results**")
                    
                    # Risk scores visualization
                    if include_risk_scores:
                        risk_data = pd.DataFrame([
                            {"Contract": a['name'], "Risk Score": a['risk_score']}
                            for a in analyses
                        ])
                        
                        fig = px.bar(risk_data, x="Contract", y="Risk Score", 
                                   color="Risk Score", color_continuous_scale="RdYlGn_r",
                                   title="Contract Risk Assessment")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Detailed analyses
                    for a in analyses:
                        with st.expander(f"📄 **{a['name']}** - Risk Score: {a['risk_score']:.0f}"):
                            st.markdown(a['analysis'])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.download_button(
                                    label="📥 Download Analysis",
                                    data=a['analysis'],
                                    file_name=f"analysis_{a['name']}_{datetime.now().strftime('%Y%m%d')}.txt"
                                )
                            with col2:
                                st.caption(f"Analyzed: {a['timestamp']}")

# ============================================================================
# TAB 3: SYNTHESIS ENGINE
# ============================================================================

with tab3:
    st.markdown("## ✨ **AI Contract Synthesis Engine**")
    
    if len(st.session_state.analyses) < 2:
        st.info("📌 Please analyze at least 2 contracts in the Analysis Studio first")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 **Synthesis Strategy**")
            
            synthesis_goal = st.selectbox(
                "Primary Objective:",
                ["⚖️ Balanced - Fair to All Parties",
                 "🏢 Owner-Optimized - Protect Owner/Developer",
                 "🔨 Contractor-Optimized - Protect Builder",
                 "🛡️ Risk-Minimized - Reduce Exposure",
                 "💰 Lender-Optimized - Protect Financing",
                 "🎯 Custom Strategy"],
                key="synthesis_goal_select"
            )
            
            if synthesis_goal == "🎯 Custom Strategy":
                custom_goal = st.text_area("Describe your custom strategy:", key="custom_goal_input")
            else:
                custom_goal = synthesis_goal
            
            st.markdown("### 📝 **Contract Sections**")
            
            sections = {
                "Preamble": st.checkbox("Preamble/Recitals", value=True, key="sec_preamble"),
                "Definitions": st.checkbox("Definitions", value=True, key="sec_definitions"),
                "Payment": st.checkbox("Payment Terms", value=True, key="sec_payment"),
                "Indemnity": st.checkbox("Indemnification", value=True, key="sec_indemnity"),
                "Force Majeure": st.checkbox("Force Majeure", value=True, key="sec_force"),
                "Termination": st.checkbox("Termination", value=True, key="sec_termination"),
                "Dispute Resolution": st.checkbox("Dispute Resolution", value=True, key="sec_dispute"),
                "Insurance": st.checkbox("Insurance", value=True, key="sec_insurance"),
                "Warranties": st.checkbox("Warranties", value=True, key="sec_warranties"),
                "Change Orders": st.checkbox("Change Orders", value=True, key="sec_change"),
                "Delay Damages": st.checkbox("Delay Damages", value=True, key="sec_delay"),
                "Lien Rights": st.checkbox("Lien Rights", value=True, key="sec_lien"),
                "Miscellaneous": st.checkbox("Miscellaneous", value=True, key="sec_misc"),
                "Signatures": st.checkbox("Signature Blocks", value=True, key="sec_signatures")
            }
        
        with col2:
            st.markdown("### ⚙️ **Synthesis Settings**")
            
            tone = st.select_slider(
                "Contract Tone:",
                options=["Conservative", "Moderate", "Aggressive", "Balanced"],
                key="tone_slider"
            )
            
            detail_level = st.select_slider(
                "Detail Level:",
                options=["Concise", "Standard", "Detailed", "Comprehensive"],
                key="detail_slider"
            )
            
            include_explanations = st.checkbox("Include clause explanations", value=True, key="include_explanations")
            include_alternatives = st.checkbox("Include alternative clauses", value=False, key="include_alternatives")
            highlight_risks = st.checkbox("Highlight risk areas", value=True, key="highlight_risks")
            
            special_instructions = st.text_area(
                "Special Instructions:",
                placeholder="E.g., Include COVID-19 clause, Add sustainability requirements...",
                key="special_instructions"
            )
        
        if st.button("🚀 **GENERATE SYNTHESIZED CONTRACT**", type="primary", use_container_width=True):
            with st.spinner("🧠 Traction AI synthesizing optimal contract..."):
                # Build context
                context = "CONTRACT ANALYSES:\n\n"
                for a in st.session_state.analyses:
                    context += f"=== {a['name']} ===\n{a['analysis']}\n\n"
                
                # Build section list
                selected_sections = [k for k, v in sections.items() if v]
                
                prompt = f"""You are a senior construction law expert synthesizing an optimal contract for {jurisdiction}.

CONTEXT:
{context}

SYNTHESIS GOAL: {custom_goal}

SELECTED SECTIONS: {', '.join(selected_sections)}

TONE: {tone}
DETAIL LEVEL: {detail_level}
INCLUDE EXPLANATIONS: {include_explanations}
INCLUDE ALTERNATIVES: {include_alternatives}
HIGHLIGHT RISKS: {highlight_risks}
SPECIAL INSTRUCTIONS: {special_instructions if special_instructions else 'None'}

Create a PROFESSIONAL, ENFORCEABLE construction contract:

For EACH selected section:
1. Provide the actual contract clause (professionally drafted)
2. {'[EXPLAIN] the rationale and source influences' if include_explanations else ''}
3. {'[RISK] highlight any risk considerations' if highlight_risks else ''}
4. {'[ALTERNATIVE] provide an alternative version' if include_alternatives else ''}

The contract should be ready for legal review and use in actual construction projects."""
                
                try:
                    synthesis = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=4000,
                        temperature=0.4
                    )
                    
                    synthesized = synthesis.choices[0].message.content
                    
                    # Save to history
                    st.session_state.synthesis_history.append({
                        "id": hashlib.md5(f"{datetime.now()}".encode()).hexdigest()[:8],
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "goal": custom_goal,
                        "contract": synthesized,
                        "sections": selected_sections
                    })
                    
                    log_activity(f"Generated synthesis with goal: {custom_goal[:50]}...")
                    
                    # Display
                    st.markdown("---")
                    st.markdown("## 📄 **Synthesized Construction Contract**")
                    st.markdown("### Generated by Traction Law AI")
                    st.markdown(synthesized)
                    
                    # Download options - FIXED INDENTATION AND ADDED UNIQUE KEYS
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.download_button(
                            label="📄 TXT",
                            data=synthesized,
                            file_name=f"TractionLaw_Synthesis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            key=f"download_txt_{datetime.now().timestamp()}"
                        )
                    
                    with col2:
                        st.download_button(
                            label="📑 Markdown",
                            data=f"# Synthesized Construction Contract\n\n*Generated by Traction Law AI*\n\n{synthesized}",
                            file_name=f"TractionLaw_Synthesis_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                            key=f"download_md_{datetime.now().timestamp()}"
                        )
                    
                    with col3:
                        st.download_button(
                            label="📋 HTML",
                            data=f"<html><body><h1>Synthesized Contract</h1>{synthesized}</body></html>",
                            file_name=f"TractionLaw_Synthesis_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                            key=f"download_html_{datetime.now().timestamp()}"
                        )
                    
                    with col4:
                        st.success("✅ Ready for review")
                    
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"Synthesis error: {e}")
                    st.exception(e)  # This will show the full error for debugging

# ============================================================================
# TAB 4: RISK DASHBOARD
# ============================================================================

with tab4:
    st.markdown("## 📊 **Risk Analytics Dashboard**")
    
    if not st.session_state.risk_scores:
        st.info("📌 Run some analyses to see risk metrics")
    else:
        # Create risk dataframe
        risk_df = pd.DataFrame([
            {"Contract": c['name'], "Risk Score": c.get('risk_score', 50)}
            for c in st.session_state.uploaded_contracts if c.get('risk_score')
        ])
        
        if not risk_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Gauge chart for average risk
                avg_risk = risk_df['Risk Score'].mean()
                
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=avg_risk,
                    title={'text': "Overall Portfolio Risk"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgreen"},
                            {'range': [30, 70], 'color': "yellow"},
                            {'range': [70, 100], 'color': "salmon"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': avg_risk
                        }
                    }
                ))
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Risk distribution
                risk_dist = pd.cut(risk_df['Risk Score'], 
                                  bins=[0, 30, 70, 100], 
                                  labels=['Low Risk', 'Medium Risk', 'High Risk'])
                dist_counts = risk_dist.value_counts()
                
                fig = px.pie(values=dist_counts.values, names=dist_counts.index,
                           title="Risk Distribution", color_discrete_sequence=['green', 'yellow', 'red'])
                st.plotly_chart(fig, use_container_width=True)
            
            # Risk by contract
            fig = px.bar(risk_df.sort_values('Risk Score', ascending=False),
                        x='Contract', y='Risk Score',
                        color='Risk Score', color_continuous_scale='RdYlGn_r',
                        title="Contract Risk Ranking")
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk heatmap
            st.markdown("### 🔥 **Risk Heat Map by Clause**")
            
            # Sample clause risk data (would come from actual analysis)
            clause_risk_data = pd.DataFrame({
                'Contract': risk_df['Contract'].tolist() * 5,
                'Clause': ['Payment'] * len(risk_df) + ['Indemnity'] * len(risk_df) + 
                          ['Force Majeure'] * len(risk_df) + ['Termination'] * len(risk_df) + 
                          ['Dispute'] * len(risk_df),
                'Risk': np.random.randint(20, 80, len(risk_df) * 5)
            })
            
            fig = px.density_heatmap(clause_risk_data, x='Clause', y='Contract', z='Risk',
                                   histfunc='avg', title="Risk Concentration Analysis")
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 5: KNOWLEDGE BASE
# ============================================================================

with tab5:
    st.markdown("## 📚 **Traction Law Knowledge Base**")
    
    kb_tabs = st.tabs(["📖 Library", "🎓 Training", "⚖️ Case Law", "📋 Checklists", "🔧 Tools"])
    
    with kb_tabs[0]:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### **Construction Law Library**")
            
            topics = {
                "Canadian Construction Law": {
                    "Construction Lien Act Guide": "Comprehensive guide to lien rights...",
                    "CCDC Contract Series": "Overview of CCDC 2, 5A, 14...",
                    "Prompt Payment Legislation": "Provincial requirements..."
                },
                "US Construction Law": {
                    "Mechanic's Liens by State": "50-state comparison...",
                    "AIA Contract Family": "Guide to AIA documents...",
                    "Miller Act Overview": "Federal project requirements..."
                },
                "International": {
                    "FIDIC Rainbow Suite": "Red, Yellow, Silver Books...",
                    "NEC4 Contracts": "Engineering and construction...",
                    "Common Law vs Civil Law": "Key differences..."
                }
            }
            
            for category, subtopics in topics.items():
                with st.expander(f"📘 {category}"):
                    for topic, description in subtopics.items():
                        st.markdown(f"**{topic}**")
                        st.caption(description)
                        if st.button(f"Read More", key=f"read_{topic}"):
                            st.info(f"Full article on {topic} - Coming soon!")
        
        with col2:
            st.markdown("### **Quick Reference**")
            st.info("**Top 10 Contract Clauses**\n1. Payment Terms\n2. Indemnity\n3. Force Majeure\n4. Termination\n5. Dispute Resolution\n6. Insurance\n7. Warranties\n8. Change Orders\n9. Delay Damages\n10. Lien Rights")
            
            st.warning("**Jurisdiction Alert**\nOntario's Construction Lien Act requires 10% holdback on all contracts over $100,000.")
            
            st.success("**Best Practice**\nAlways include a dispute resolution clause specifying arbitration under the applicable arbitration act.")
    
    with kb_tabs[1]:
        st.markdown("### **Training Modules**")
        
        modules = [
            "Contract Drafting Fundamentals",
            "Risk Allocation Strategies",
            "Negotiation Techniques",
            "Lien Law Masterclass",
            "Force Majeure After COVID",
            "Dispute Resolution Workshop"
        ]
        
        for module in modules:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{module}**")
                st.caption("2 hours • Certificate upon completion")
            with col2:
                st.button("Start", key=f"train_{module}")

# ============================================================================
# TAB 6: TEAM WORKSPACE
# ============================================================================

with tab6:
    st.markdown("## 👥 **Team Collaboration Workspace**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### **Team Members**")
        
        team_members = [
            {"name": "You (Admin)", "role": "Legal Counsel", "status": "🟢 Active"},
            {"name": "Sarah Chen", "role": "Contract Manager", "status": "🟢 Active"},
            {"name": "Mike Ross", "role": "Associate", "status": "🟡 Away"},
            {"name": "Rachel Zane", "role": "Paralegal", "status": "🟢 Active"}
        ]
        
        for member in team_members:
            st.markdown(f"""
            <div class="contract-card">
                <b>{member['name']}</b><br>
                {member['role']} | {member['status']}
            </div>
            """, unsafe_allow_html=True)
        
        st.button("➕ Invite Team Member")
    
    with col2:
        st.markdown("### **Activity Feed**")
        
        for activity in st.session_state.activity_log[-10:]:
            st.markdown(f"""
            <div class="contract-card">
                <b>{activity['activity']}</b><br>
                <small>{activity['timestamp']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### **Shared Projects**")
    
    shared_projects = [
        {"name": "Maple Tower Development", "owner": "You", "updated": "2h ago"},
        {"name": "Bridgeport Condos", "owner": "Sarah Chen", "updated": "1d ago"},
        {"name": "Riverside Infrastructure", "owner": "Mike Ross", "updated": "3d ago"}
    ]
    
    for project in shared_projects:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{project['name']}**")
        with col2:
            st.caption(f"Owner: {project['owner']}")
        with col3:
            st.caption(f"🕒 {project['updated']}")

# ============================================================================
# CELEBRATION BANNER - FIXED VERSION (NO EMOJI ERRORS)
# ============================================================================

st.markdown("---")

# Celebration button in sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🎉 CELEBRATE! 🎉", use_container_width=True):
        st.session_state.celebrate = True

# Celebration banner
if 'celebrate' not in st.session_state:
    st.session_state.celebrate = False

if st.session_state.celebrate:
    st.balloons()
    st.snow()
    
    # Using HTML entities instead of raw emojis
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 2rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">&#127881; TRACTION LAW &#127881;</h1>
        <h2 style="color: white; font-size: 2rem; margin-bottom: 1rem;">Contract Intelligence Platform</h2>
        <p style="color: white; font-size: 1.2rem; margin-bottom: 2rem;">Making construction contracts smarter, faster, and more accessible</p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 2rem;">
            <span style="color: white; font-size: 2rem;">&#9874;</span>
            <span style="color: white; font-size: 2rem;">&#127969;</span>
            <span style="color: white; font-size: 2rem;">&#128211;</span>
            <span style="color: white; font-size: 2rem;">&#10024;</span>
            <span style="color: white; font-size: 2rem;">&#128640;</span>
        </div>
        <p style="color: white; font-size: 1rem; opacity: 0.9;">Built with &#10084;&#65039; by Traction Law Team</p>
        <p style="color: white; font-size: 0.9rem; margin-top: 1rem; opacity: 0.7;">Version 2.0 | Enterprise Edition</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dismiss button
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("✨ Awesome! ✨"):
            st.session_state.celebrate = False
            st.rerun()
# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div class="footer">
    <div style="font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">⚖️ TRACTION LAW</div>
    <div style="margin-bottom: 1rem;">
        <a href="#">Privacy Policy</a> • 
        <a href="#">Terms of Service</a> • 
        <a href="#">Security</a> • 
        <a href="#">Support</a>
    </div>
    <div style="opacity: 0.7; font-size: 0.9rem;">
        © 2025 Traction Law Inc. All rights reserved. | Enterprise Contract Intelligence Platform
    </div>
    <div style="margin-top: 1rem; font-size: 0.8rem; opacity: 0.5;">
        Version 2.0.0 | Build 2025.03 | Certified for Enterprise Use
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# AUTO-SAVE FUNCTIONALITY
# ============================================================================

if auto_save and len(st.session_state.uploaded_contracts) > 0:
    if 'last_save' not in st.session_state:
        st.session_state.last_save = datetime.now()
    
    if datetime.now() - st.session_state.last_save > timedelta(minutes=5):
        save_project()
        st.session_state.last_save = datetime.now()

        st.toast("💾 Project auto-saved", icon="✅")


