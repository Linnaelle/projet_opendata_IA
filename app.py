import os

import streamlit as st
from dotenv import load_dotenv

from utils.data import OpenFoodFactsAPI
from utils.charts import (
    create_comparison_chart,
    create_nutriscore_gauge,
    create_nutriments_pie,
)
from utils.chatbot import NutriChatbot

load_dotenv()

st.set_page_config(
    page_title="🥗 NutriScan",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #0F172A;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16213A 0%, #0F172A 100%);
        min-width: 400px;
        max-width: 400px;
        border-right: 2px solid #243244;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.4);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #16213A 0%, #0F172A 100%);
    }
    
    [data-testid="stSidebar"] label {
        color: #E5E7EB;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: #9CA3AF;
        font-size: 0.75rem;
        font-weight: 700;
    }
    
    h1 {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
    }
    
    h2, h3 {
        color: #E5E7EB;
        font-weight: 700;
    }
    
    h2 {
        font-size: 1.75rem;
        margin-top: 2rem;
    }
    
    [data-testid="stExpander"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        border: 2px solid #243244;
        border-radius: 16px;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stExpander"]:hover {
        border-color: #22C55E40;
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.15);
        transform: translateY(-2px);
    }
    
    [data-testid="stExpander"] summary {
        color: #E5E7EB;
        font-weight: 600;
        font-size: 1.05rem;
        padding: 0.5rem 0;
    }
    
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        padding: 1.25rem;
        border-radius: 12px;
        border: 2px solid #243244;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: #22C55E40;
        transform: translateY(-2px);
    }
    
    [data-testid="stMetricValue"] {
        color: #22C55E;
        font-size: 2.5rem;
        font-weight: 800;
        text-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
    }
    
    [data-testid="stMetricLabel"] {
        color: #9CA3AF;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.1em;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
        color: #0F172A;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(34, 197, 94, 0.4);
        background: linear-gradient(135deg, #16A34A 0%, #22C55E 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
    }
    
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        color: #E5E7EB;
        border: 2px solid #243244;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: #22C55E;
        box-shadow: 0 6px 16px rgba(34, 197, 94, 0.2);
    }
    
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        border: 2px solid #243244;
        border-radius: 12px;
        color: #E5E7EB;
        padding: 1rem 1.25rem;
        font-size: 1.05rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #22C55E;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15), 0 4px 12px rgba(34, 197, 94, 0.2);
        background: #1E293B;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6B7280;
        font-style: italic;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        border: 2px solid #243244;
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        border: 2px solid #243244;
        border-radius: 12px;
    }
    
    .stSelectbox [data-baseweb="select"] > div:first-child {
        background: transparent;
        border: none;
        padding: 0;
        min-height: auto;
        height: auto;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        color: #E5E7EB;
    }
    
    .stSelectbox [data-baseweb="select"] div[class*="ValueContainer"] {
        display: flex;
        align-items: center;
        color: #E5E7EB;
        flex: 1;
    }
    
    .stSelectbox [data-baseweb="select"] div[class*="SingleValue"],
    .stSelectbox [data-baseweb="select"] div[class*="singleValue"] {
        color: #E5E7EB;
        font-weight: 500;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
        padding: 0;
        position: relative;
        top: 0;
    }
    
    .stSelectbox [data-baseweb="select"] div[class*="Input"] {
        margin: 0;
        padding: 0;
        display: flex;
        align-items: center;
        position: relative;
        top: 0;
    }
    
    .stSelectbox [data-baseweb="select"] input {
        color: #E5E7EB;
        margin: 0;
        padding: 0; 
        position: relative;
        top: 0;
    }
    
    .stSelectbox [data-baseweb="select"] div[class*="IndicatorsContainer"] {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0.85rem 1rem 0.85rem 0.5rem;
    }
    
    .stSelectbox [data-baseweb="select"] div[class*="IndicatorsContainer"] > div {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 0;
        margin: 0;
        position: relative;
        top: 0;
    }
    
    .stSelectbox * {
        color: #E5E7EB;
    }
    
    [data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child {
        color: #E5E7EB;
    }
    
    [data-testid="stSelectbox"] [data-baseweb="select"] > div > div > div {
        color: #E5E7EB;
    }
    
    [data-testid="stSelectbox"] input {
        color: #E5E7EB;
    }
    
    [data-testid="stSidebar"] .stSelectbox * {
        color: #E5E7EB;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] {
        color: #E5E7EB;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] div[class*="singleValue"] {
        color: #E5E7EB;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] div[class*="placeholder"] {
        color: #9CA3AF;
    }
    
    .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] > div {
        overflow: visible;
    }
    
    .stSelectbox [data-baseweb="select"] div[class*="ValueContainer"] {
        overflow: visible;
        flex-wrap: nowrap;
    }
    
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div[class*="singleValue"] {
        white-space: nowrap;
        opacity: 1;
        visibility: visible;
        color: #E5E7EB;
        margin: 0;
        padding: 0;
        position: relative;
        top: 0;
        transform: none;
    }
    
    .stSelectbox [data-baseweb="select"] div[class*="ValueContainer"] > div {
        display: flex;
        align-items: center;
        margin: 0;
        padding: 0;
        position: relative;
        top: 0;
    }
    
    .stSelectbox [data-baseweb="select"] > div:first-child {
        display: flex;
        flex-direction: row;
        align-items: stretch;
        justify-content: space-between;
    }
    
    .stSelectbox [data-baseweb="select"] svg {
        fill: #E5E7EB;
        width: 30px;
        height: 30px;
        display: block;
        vertical-align: middle;
        margin: 0;
        position: relative;
        top: 0;
        transform: none;
    }
    
    .stSelectbox [data-baseweb="select"]:hover > div {
        border-color: #22C55E;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
    }
    
    .stSelectbox [data-baseweb="select"]:focus-within > div {
        border-color: #22C55E;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15);
    }
    
    [data-baseweb="popover"] {
        background: #1E293B;
        border: 2px solid #243244;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    
    [data-baseweb="menu"] {
        background: #1E293B;
    }
    
    [role="option"] {
        background: #1E293B;
        color: #E5E7EB;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
    }
    
    [role="option"]:hover {
        background: linear-gradient(135deg, #243244 0%, #1E293B 100%);
        color: #22C55E;
    }
    
    [role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, #1E293B 100%);
        color: #22C55E;
        font-weight: 600;
    }
    
    .stAlert {
        border-radius: 12px;
        border-left-width: 4px;
    }
    
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1);
        border-left-color: #22C55E;
        color: #22C55E;
    }
    
    .stInfo {
        background-color: rgba(56, 189, 248, 0.1);
        border-left-color: #38BDF8;
        color: #38BDF8;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border-left-color: #F59E0B;
        color: #F59E0B;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border-left-color: #EF4444;
        color: #EF4444;
    }
    
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 2px solid #243244;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatMessage"]:hover {
        transform: translateX(4px);
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #1E293B 0%, #243244 100%);
        border-left: 4px solid #F59E0B;
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.08) 0%, #1E293B 100%);
        border-left: 4px solid #22C55E;
    }
    
    .stChatInput > div > div > div > div > input {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        border: 2px solid #243244;
        border-radius: 24px;
        color: #E5E7EB;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stChatInput > div > div > div > div > input:focus {
        border-color: #22C55E;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15), 0 4px 16px rgba(34, 197, 94, 0.2);
    }
    
    .stChatInput > div > div > div > div > input::placeholder {
        color: #6B7280;
    }
    
    .stSpinner > div {
        border-top-color: #22C55E;
    }
    
    hr {
        border-color: #243244;
    }
    
    .css-10trblm {
        color: #9CA3AF;
    }
    
    .js-plotly-plot {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        border-radius: 16px;
        border: 2px solid #243244;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        padding: 0.5rem;
    }
    
    img {
        border-radius: 16px;
        border: 3px solid #243244;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    img:hover {
        border-color: #22C55E40;
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.2);
        transform: scale(1.02);
    }
    
    .nutrition-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 24px;
        font-weight: 700;
        font-size: 0.875rem;
        margin-right: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .nutrition-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .badge-success {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.25) 0%, rgba(34, 197, 94, 0.15) 100%);
        color: #22C55E;
        border: 2px solid #22C55E40;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.25) 0%, rgba(245, 158, 11, 0.15) 100%);
        color: #F59E0B;
        border: 2px solid #F59E0B40;
    }
    
    .badge-error {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.25) 0%, rgba(239, 68, 68, 0.15) 100%);
        color: #EF4444;
        border: 2px solid #EF444440;
    }
    
    .app-header {
        background: linear-gradient(135deg, #16213A 0%, #1E293B 50%, #16213A 100%);
        padding: 3rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        border: 2px solid #243244;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .app-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #22C55E 0%, #F59E0B 50%, #22C55E 100%);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0F172A;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #243244 0%, #1E293B 100%);
        border-radius: 6px;
        border: 2px solid #0F172A;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
    }
    
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    [data-testid="stDataFrame"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        border-radius: 16px;
        border: 2px solid #243244;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #22C55E 0%, #16A34A 100%);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #16213A;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1E293B;
        border-radius: 8px;
        color: #9CA3AF;
        border: 2px solid #243244;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #243244;
        color: #E5E7EB;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
        color: #0F172A;
        border-color: #22C55E;
    }
    
    .stToast {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%);
        border: 2px solid #243244;
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
</style>

<script>
// Ensure selectbox values remain visible after dynamic updates
(function() {
    function fixSelectboxes() {
        const selects = document.querySelectorAll('[data-testid="stSidebar"] [data-baseweb="select"]');
        selects.forEach(select => {
            const textDivs = select.querySelectorAll('div, span');
            textDivs.forEach(el => {
                if (el.textContent && el.textContent.trim() !== '') {
                    el.style.color = '#E5E7EB';
                    el.style.opacity = '1';
                    el.style.visibility = 'visible';
                }
            });
        });
    }
    
    fixSelectboxes();
    setTimeout(fixSelectboxes, 100);
    setTimeout(fixSelectboxes, 500);
    
    const observer = new MutationObserver(fixSelectboxes);
    observer.observe(document.body, { childList: true, subtree: true });
})();
</script>
""", unsafe_allow_html=True)

# Initialiser l'API
api = OpenFoodFactsAPI()

# Sidebar branding with enhanced nutrition theme
st.sidebar.markdown("""
<div style="text-align: center; padding: 2rem 1rem 1.5rem 1rem; background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, transparent 100%); border-radius: 16px; margin-bottom: 1rem; border: 2px solid #243244;">
    <div style="font-size: 3rem; margin-bottom: 0.5rem; filter: drop-shadow(0 4px 8px rgba(34, 197, 94, 0.3));">🥗</div>
    <h2 style="margin: 0; font-size: 2rem; background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-weight: 800; letter-spacing: -0.02em;">NutriScan</h2>
    <p style="margin: 0.75rem 0 0 0; color: #9CA3AF; font-size: 0.9rem; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase;">🍎 Nutrition Intelligente</p>
    <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(34, 197, 94, 0.1); border-radius: 8px; border: 1px solid #22C55E40;">
        <p style="margin: 0; color: #22C55E; font-size: 0.8rem; font-weight: 600;">✨ Alimentez votre santé</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar - Navigation with modern styling
st.sidebar.markdown("""
<div style="padding: 0.75rem 1rem; background: linear-gradient(135deg, #1E293B 0%, #16213A 100%); border-radius: 12px; margin-bottom: 1rem; border: 2px solid #243244;">
    <p style="margin: 0; color: #9CA3AF; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;">📋 Navigation</p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.selectbox(
    "Choisir une page",
    ["🔍 Recherche Produit", "⚖️ Comparateur", "💬 Chatbot Nutrition"]
)

st.sidebar.markdown("<div style='margin: 1.5rem 0; border-top: 2px solid #243244;'></div>", unsafe_allow_html=True)

# Choix du provider IA (sidebar) with enhanced design
st.sidebar.markdown("""
<div style="padding: 0.75rem 1rem; background: linear-gradient(135deg, #1E293B 0%, #16213A 100%); border-radius: 12px; margin-bottom: 1rem; border: 2px solid #243244;">
    <p style="margin: 0; color: #9CA3AF; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;">🤖 Modèle IA</p>
</div>
""", unsafe_allow_html=True)

default_provider = os.getenv("NUTRISCAN_PROVIDER", "openai").lower()
providers = ["openai", "gemini", "ollama"]
try:
    default_index = providers.index(default_provider)
except ValueError:
    default_index = 0

selected_provider = st.sidebar.selectbox(
    "Fournisseur de modèle",
    providers,
    index=default_index,
    format_func=lambda x: {"openai": "🧠 OpenAI GPT", "gemini": "✨ Google Gemini", "ollama": "🏠 Ollama (local)"}[x]
)

# Afficher le modèle actif avec design moderne
model_names = {
    "openai": "GPT-4o Mini",
    "gemini": "Gemini 2.0 Flash",
    "ollama": "Mistral (Local)"
}
st.sidebar.markdown(f"""
<div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%); padding: 1rem; border-radius: 12px; border: 2px solid #22C55E40; margin-top: 1rem; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(34, 197, 94, 0.1);">
    <p style="margin: 0; color: #9CA3AF; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;">⚡ MODÈLE ACTIF</p>
    <p style="margin: 0.5rem 0 0 0; color: #22C55E; font-weight: 700; font-size: 1.1rem;">{model_names.get(selected_provider, "Unknown")}</p>
    <div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid #243244;">
        <p style="margin: 0; color: #9CA3AF; font-size: 0.75rem;">🔋 Prêt à analyser vos produits</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialiser / mettre à jour le chatbot si besoin
if "chatbot" not in st.session_state or st.session_state.get("provider") != selected_provider:
    st.session_state.chatbot = NutriChatbot(provider=selected_provider)
    st.session_state.provider = selected_provider

if "comparison_products" not in st.session_state:
    st.session_state.comparison_products = []

# Styled Header - Hero Section
st.markdown("""
<div class="app-header">
    <div style="display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1rem;">
        <div style="font-size: 4rem; filter: drop-shadow(0 8px 16px rgba(34, 197, 94, 0.4));">🥗</div>
        <div style="flex: 1;">
            <h1 style="margin: 0; font-size: 3rem;">NutriScan</h1>
            <p style="margin: 0.5rem 0 0 0; color: #9CA3AF; font-size: 1.2rem; font-weight: 500;">
                🍎 Assistant Nutrition Intelligent
            </p>
        </div>
    </div>
    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); padding: 1.25rem; border-radius: 12px; border-left: 4px solid #22C55E;">
        <p style="margin: 0; color: #E5E7EB; font-size: 1rem; line-height: 1.6;">
            ✨ Analysez vos produits alimentaires avec l'IA • 📊 Comparez les valeurs nutritionnelles • 💬 Obtenez des conseils personnalisés
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

def clean_product_data(raw_product):
    raw_nutriments = raw_product.get("nutriments", {})
    nutriscore = raw_product.get("nutriscore", "")

    if isinstance(nutriscore, dict):
        data = nutriscore.get("2023") or nutriscore.get("2021") or {}
        nutriscore = data.get("grade", "").upper()
    else:
        nutriscore = str(nutriscore).upper()

    return {
        "code": raw_product.get("code"),
        "name": raw_product.get("product_name", "Inconnu"),
        "brands": raw_product.get("brands", "Inconnue"),
        "nutriscore": nutriscore,
        "nova_group": raw_product.get("nova_group"),
        "ingredients": raw_product.get("ingredients_text"),
        "allergens": raw_product.get("allergens", ""),
        "categories": raw_product.get("categories", ""),
        "image_url": raw_product.get("image_url"),
        "nutriments": {
            "calories": raw_nutriments.get("energy-kcal_100g"),
            "matg": raw_nutriments.get("fat_100g"),
            "satures": raw_nutriments.get("saturated-fat_100g"),
            "sucres": raw_nutriments.get("sugars_100g"),
            "sel": raw_nutriments.get("salt_100g"),
            "proteines": raw_nutriments.get("proteins_100g"),
            "glucides": raw_nutriments.get("carbohydrates_100g"),
            "fibres": raw_nutriments.get("fiber_100g"),
            "sodium": raw_nutriments.get("sodium_100g"),
        }
    }

# ===== PAGE 1: RECHERCHE PRODUIT =====
if page == "🔍 Recherche Produit":
    # Page header with modern design
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B 0%, #16213A 100%); padding: 1.5rem; border-radius: 16px; border: 2px solid #243244; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
        <h2 style="margin: 0; color: #E5E7EB; font-size: 2rem; font-weight: 700;">🔍 Rechercher un produit</h2>
        <p style="margin: 0.5rem 0 0 0; color: #9CA3AF; font-size: 1rem;">Trouvez et analysez les informations nutritionnelles de vos produits</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Nom du produit ou code-barres",
            placeholder="Ex: Nutella, 3017620422003 🍫"
        )
    
    with col2:
        search_button = st.button("🔍 Rechercher", type="primary")
    
    # --- RECHERCHE ---
    if search_button and search_query:
        with st.spinner("Recherche en cours..."):
            if search_query.isdigit() and len(search_query) >= 8:
                product = api.get_product(search_query)
                products = [product] if product else []
            else:
                products = api.search_products(search_query, page_size=15)

            clean_results = [clean_product_data(p) for p in products]
        
        if clean_results:
            st.success(f"✅ {len(products)} produit(s) trouvé(s)")
            
            # Sélection du produit
            product_names = [
                f"{p.get('name', 'Sans nom')} - {p.get('brands', 'Sans marque')}"
                for p in clean_results
            ]
            selected_idx = st.selectbox("Sélectionnez un produit:", range(len(product_names)), format_func=lambda x: product_names[x])
            
            if selected_idx is not None:
                selected_product = products[selected_idx]
                product_info = api.extract_product_info(selected_product)
                
                # Affichage des infos produit
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # Product image card
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #1E293B 0%, #16213A 100%); padding: 1.5rem; border-radius: 16px; border: 2px solid #243244; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); margin-bottom: 1rem;">
                    """, unsafe_allow_html=True)
                    
                    if product_info["image_url"]:
                        st.image(product_info["image_url"], width=250)
                    else:
                        st.markdown("""
                        <div style="width: 250px; height: 250px; background: linear-gradient(135deg, #243244 0%, #1E293B 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 4rem;">
                            🍽️
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Metrics in styled cards
                    st.metric("🏆 Nutri-Score", product_info["nutriscore"])
                    st.metric("🔬 NOVA Group", product_info["nova_group"])
                    
                    # CALLBACK pour ajouter au comparateur
                    def add_to_comparator():
                        """Callback exécuté AVANT le rerun"""
                        existing_codes = [p.get('code') for p in st.session_state.comparison_products]
                        
                        if product_info['code'] not in existing_codes:
                            st.session_state.comparison_products.append(product_info)
                            st.session_state.last_action = f"✅ {product_info['name'][:30]} ajouté !"
                        else:
                            st.session_state.last_action = "⚠️ Produit déjà dans le comparateur"
                    
                    # Bouton avec callback
                    st.button(
                        "➕ Ajouter au comparateur", 
                        key=f"add_{product_info['code']}",
                        on_click=add_to_comparator
                    )
                    
                    # Afficher le dernier message (persistera après rerun)
                    if "last_action" in st.session_state and st.session_state.last_action:
                        st.info(st.session_state.last_action)
                        # Optionnel : afficher des balloons
                        if "✅" in st.session_state.last_action:
                            st.balloons()
                
                with col2:
                    # Product title card
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #1E293B 0%, #16213A 100%); padding: 1.5rem; border-radius: 16px; border: 2px solid #243244; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); margin-bottom: 1.5rem;">
                        <h3 style="margin: 0 0 0.5rem 0; color: #E5E7EB; font-size: 1.5rem; font-weight: 700;">{product_info['name']}</h3>
                        <p style="margin: 0; color: #9CA3AF; font-size: 0.95rem;">🏷️ <strong>Marque:</strong> {product_info['brands']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Analyse IA
                    with st.expander("🤖 Analyse IA", expanded=True):
                        with st.spinner("Génération de l'analyse..."):
                            analysis = st.session_state.chatbot.analyze_product(product_info)
                            st.markdown(analysis)
                    
                    # Informations détaillées
                    with st.expander("📋 Informations détaillées"):
                        st.write("**Catégories:**", product_info["categories"])
                        st.write("**Allergènes:**", product_info["allergens"])
                        st.write("**Ingrédients:**", product_info["ingredients"])
                
                # Visualisations with styled header
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, transparent 100%); padding: 1rem 1.5rem; border-radius: 12px; border-left: 4px solid #22C55E; margin: 2rem 0 1.5rem 0;">
                    <h3 style="margin: 0; color: #E5E7EB; font-size: 1.5rem; font-weight: 700;">📊 Visualisations Nutritionnelles</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #9CA3AF; font-size: 0.9rem;">Analyse graphique des valeurs nutritionnelles</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_gauge = create_nutriscore_gauge(product_info["nutriscore"])
                    st.plotly_chart(fig_gauge, width='stretch')
                
                with col2:
                    if product_info["nutriments"]:
                        fig_pie = create_nutriments_pie(product_info["nutriments"])
                        st.plotly_chart(fig_pie, width='stretch')
                
                # Alternatives with styled header
                st.markdown("""
                <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, transparent 100%); padding: 1rem 1.5rem; border-radius: 12px; border-left: 4px solid #F59E0B; margin: 2rem 0 1.5rem 0;">
                    <h3 style="margin: 0; color: #E5E7EB; font-size: 1.5rem; font-weight: 700;">🔄 Alternatives Recommandées</h3>
                    <p style="margin: 0.5rem 0 0 0; color: #9CA3AF; font-size: 0.9rem;">Découvrez des options plus saines</p>
                </div>
                """, unsafe_allow_html=True)
                
                with st.spinner("🔍 Recherche d'alternatives..."):
                    # Rechercher des produits similaires
                    category = product_info["categories"].split(",")[0] if product_info["categories"] else product_info["name"].split()[0]
                    alternatives = api.search_products(category, page_size=5)
                    
                    # Filtrer pour garder que les meilleures
                    alternatives = [
                        api.extract_product_info(alt) for alt in alternatives
                        if alt.get("nutriscore_grade", "Z") < product_info["nutriscore"]
                    ][:3]
                    
                    if alternatives:
                        suggestion_text = st.session_state.chatbot.suggest_alternatives(
                            product_info, alternatives
                        )
                        st.info(suggestion_text)
                        
                        cols = st.columns(len(alternatives))
                        for idx, alt in enumerate(alternatives):
                            with cols[idx]:
                                st.image(alt["image_url"] if alt["image_url"] else "https://via.placeholder.com/150", width=150)
                                st.write(f"**{alt['name'][:30]}**")
                                st.write(f"Nutri-Score: **{alt['nutriscore']}**")
                    else:
                        st.warning("Aucune alternative trouvée avec un meilleur Nutri-Score")
        
        else:
            st.error("❌ Aucun produit trouvé")

# ===== PAGE 2: COMPARATEUR =====
elif page == "⚖️ Comparateur":
    # Page header with modern design
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B 0%, #16213A 100%); padding: 1.5rem; border-radius: 16px; border: 2px solid #243244; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
        <h2 style="margin: 0; color: #E5E7EB; font-size: 2rem; font-weight: 700;">⚖️ Comparateur de produits</h2>
        <p style="margin: 0.5rem 0 0 0; color: #9CA3AF; font-size: 1rem;">Comparez les valeurs nutritionnelles pour faire les meilleurs choix</p>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.comparison_products) == 0:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, transparent 100%); padding: 2rem; border-radius: 16px; border: 2px solid #38BDF8; text-align: center; margin-top: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📦</div>
            <h3 style="margin: 0; color: #38BDF8; font-size: 1.5rem;">Aucun produit à comparer</h3>
            <p style="margin: 1rem 0 0 0; color: #9CA3AF; font-size: 1rem;">👈 Ajoutez des produits depuis la page de recherche pour commencer</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Success banner
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%); padding: 1.25rem; border-radius: 12px; border: 2px solid #22C55E40; margin-bottom: 2rem; text-align: center;">
            <p style="margin: 0; color: #22C55E; font-size: 1.2rem; font-weight: 700;">📦 {len(st.session_state.comparison_products)} produit(s) dans le comparateur</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Affichage des produits avec design amélioré
        cols = st.columns(len(st.session_state.comparison_products))
        
        for idx, product in enumerate(st.session_state.comparison_products):
            with cols[idx]:
                # Product card
                st.markdown("""
                <div style="background: linear-gradient(135deg, #1E293B 0%, #16213A 100%); padding: 1.25rem; border-radius: 16px; border: 2px solid #243244; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); margin-bottom: 1rem;">
                """, unsafe_allow_html=True)
                
                if product["image_url"]:
                    st.image(product["image_url"], width=150)
                else:
                    st.markdown("""
                    <div style="width: 150px; height: 150px; background: linear-gradient(135deg, #243244 0%, #1E293B 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 3rem; margin: 0 auto;">
                        🍽️
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.markdown(f"**{product['name'][:30]}**")
                st.metric("🏆 Nutri-Score", product["nutriscore"])
                st.metric("🔬 NOVA", product["nova_group"])
                
                if st.button(f"🗑️ Retirer", key=f"remove_{idx}", width=True):
                    st.session_state.comparison_products.pop(idx)
                    st.rerun()
        
        # Graphique de comparaison avec header stylé
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, transparent 100%); padding: 1rem 1.5rem; border-radius: 12px; border-left: 4px solid #22C55E; margin: 2rem 0 1.5rem 0;">
            <h3 style="margin: 0; color: #E5E7EB; font-size: 1.5rem; font-weight: 700;">📊 Comparaison Visuelle</h3>
            <p style="margin: 0.5rem 0 0 0; color: #9CA3AF; font-size: 0.9rem;">Analyse comparative des produits</p>
        </div>
        """, unsafe_allow_html=True)
        
        fig = create_comparison_chart(st.session_state.comparison_products)
        st.plotly_chart(fig, width=True)
        
        # Analyse comparative IA
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🤖 Analyse comparative IA", type="primary", width=True):
                with st.spinner("🧠 Génération de l'analyse..."):
                    comparison_text = "\n".join([
                        f"- {p['name']} (Nutri-Score {p['nutriscore']}, NOVA {p['nova_group']})"
                        for p in st.session_state.comparison_products
                    ])
                    
                    prompt = f"Compare ces produits et dis lequel est le meilleur choix nutritionnel:\n{comparison_text}"
                    analysis = st.session_state.chatbot.chat(prompt)
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, #1E293B 100%); padding: 1.5rem; border-radius: 12px; border-left: 4px solid #22C55E; margin-top: 1rem;">
                        <p style="margin: 0; color: #E5E7EB; line-height: 1.6;">{analysis}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🗑️ Vider le comparateur", width=True):
                st.session_state.comparison_products = []
                st.rerun()

# ===== PAGE 3: CHATBOT =====
elif page == "💬 Chatbot Nutrition":
    # Page header with modern design
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B 0%, #16213A 100%); padding: 1.5rem; border-radius: 16px; border: 2px solid #243244; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
        <h2 style="margin: 0; color: #E5E7EB; font-size: 2rem; font-weight: 700;">💬 Assistant Nutrition</h2>
        <p style="margin: 0.5rem 0 0 0; color: #9CA3AF; font-size: 1rem;">🤖 Posez vos questions sur l'alimentation et la nutrition • Obtenez des réponses personnalisées</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Historique de conversation
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Zone de chat
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Input utilisateur
    user_input = st.chat_input("Posez votre question...")
    
    if user_input:
        # Afficher le message utilisateur
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Générer la réponse
        with st.chat_message("assistant"):
            with st.spinner("Réflexion..."):
                response = st.session_state.chatbot.chat(user_input)
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Suggestions de questions avec design amélioré
    st.sidebar.markdown("""
    <div style="padding: 0.75rem 1rem; background: linear-gradient(135deg, #1E293B 0%, #16213A 100%); border-radius: 12px; margin-bottom: 1rem; border: 2px solid #243244;">
        <p style="margin: 0; color: #9CA3AF; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;">💡 Questions suggérées</p>
    </div>
    """, unsafe_allow_html=True)
    
    suggestions = [
        ("🏆", "C'est quoi le Nutri-Score ?"),
        ("🍕", "Qu'est-ce que le groupe NOVA ?"),
        ("⚠️", "Pourquoi éviter les additifs ?"),
        ("📋", "Comment lire une étiquette nutritionnelle ?"),
        ("🍬", "Quels sont les sucres cachés ?")
    ]
    
    for emoji, suggestion in suggestions:
        if st.sidebar.button(f"{emoji} {suggestion}", width=True):
            st.session_state.chat_history.append({"role": "user", "content": suggestion})
            with st.spinner("Réflexion..."):
                response = st.session_state.chatbot.chat(suggestion)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

# Footer with enhanced nutrition theme
st.sidebar.markdown("<div style='margin: 2rem 0 1.5rem 0; border-top: 2px solid #243244;'></div>", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="padding: 1.25rem; background: linear-gradient(135deg, #1E293B 0%, #16213A 100%); border-radius: 16px; border: 2px solid #243244; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);">
    <div style="margin-bottom: 1rem;">
        <p style="margin: 0 0 0.75rem 0; color: #9CA3AF; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;">📚 Sources de données</p>
        <div style="background: rgba(34, 197, 94, 0.05); padding: 0.75rem; border-radius: 8px; border-left: 3px solid #22C55E; margin-bottom: 0.5rem;">
            <p style="margin: 0; color: #E5E7EB; font-size: 0.85rem; font-weight: 500;">🥗 OpenFoodFacts API</p>
        </div>
        <div style="background: rgba(245, 158, 11, 0.05); padding: 0.75rem; border-radius: 8px; border-left: 3px solid #F59E0B;">
            <p style="margin: 0; color: #E5E7EB; font-size: 0.85rem; font-weight: 500;">🔬 ANSES (Ciqual)</p>
        </div>
    </div>
    
    <div style="padding-top: 1rem; border-top: 1px solid #243244;">
        <p style="margin: 0 0 0.75rem 0; color: #9CA3AF; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;">🤖 Intelligence Artificielle</p>
        <div style="background: rgba(56, 189, 248, 0.05); padding: 0.75rem; border-radius: 8px; border-left: 3px solid #38BDF8;">
            <p style="margin: 0; color: #E5E7EB; font-size: 0.85rem; font-weight: 500;">⚡ Modèles via LiteLLM</p>
        </div>
    </div>
</div>

<div style="text-align: center; margin-top: 1.5rem; padding: 1rem; background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%); border-radius: 12px; border: 2px solid #243244;">
    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">💚</div>
    <p style="margin: 0; color: #22C55E; font-size: 0.85rem; font-weight: 700; letter-spacing: 0.05em;">Made with ♥ for health</p>
    <p style="margin: 0.5rem 0 0 0; color: #9CA3AF; font-size: 0.75rem; font-weight: 500;">🎓 IPSSI Open Data & IA</p>
</div>
""", unsafe_allow_html=True)