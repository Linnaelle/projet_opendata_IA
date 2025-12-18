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

# Charger les variables d'environnement (.env)
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="🥗 NutriScan",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS avec la palette de couleurs moderne nutrition
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main content area */
    .main {
        background-color: #0F172A !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Sidebar styling - WIDER & MORE PROMINENT */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16213A 0%, #0F172A 100%) !important;
        min-width: 400px !important;
        max-width: 400px !important;
        border-right: 2px solid #243244 !important;
        box-shadow: 4px 0 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #16213A 0%, #0F172A 100%) !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] label {
        color: #E5E7EB !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.5rem !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label {
        color: #9CA3AF !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
    }
    
    /* Headers with gradient accent */
    h1 {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }
    
    h2, h3 {
        color: #E5E7EB !important;
        font-weight: 700 !important;
    }
    
    h2 {
        font-size: 1.75rem !important;
        margin-top: 2rem !important;
    }
    
    /* Card-like containers with elevated design */
    [data-testid="stExpander"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        border: 2px solid #243244 !important;
        border-radius: 16px !important;
        margin-bottom: 1.25rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stExpander"]:hover {
        border-color: #22C55E40 !important;
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    [data-testid="stExpander"] summary {
        color: #E5E7EB !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 0.5rem 0 !important;
    }
    
    /* Metric cards with enhanced styling */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        padding: 1.25rem !important;
        border-radius: 12px !important;
        border: 2px solid #243244 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: #22C55E40 !important;
        transform: translateY(-2px) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #22C55E !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 8px rgba(34, 197, 94, 0.3) !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #9CA3AF !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.1em !important;
    }
    
    /* Buttons with modern design */
    .stButton > button {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%) !important;
        color: #0F172A !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(34, 197, 94, 0.4) !important;
        background: linear-gradient(135deg, #16A34A 0%, #22C55E 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3) !important;
    }
    
    /* Primary button specific */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%) !important;
    }
    
    /* Secondary buttons */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        color: #E5E7EB !important;
        border: 2px solid #243244 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        border-color: #22C55E !important;
        box-shadow: 0 6px 16px rgba(34, 197, 94, 0.2) !important;
    }
    
    /* Text input with enhanced focus */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        border: 2px solid #243244 !important;
        border-radius: 12px !important;
        color: #E5E7EB !important;
        padding: 1rem 1.25rem !important;
        font-size: 1.05rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #22C55E !important;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15), 0 4px 12px rgba(34, 197, 94, 0.2) !important;
        background: #1E293B !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #6B7280 !important;
        font-style: italic !important;
    }
    
    /* Select boxes with modern styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        border: 2px solid #243244 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    /* Main select control - proper alignment */
    .stSelectbox [data-baseweb="select"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        border: 2px solid #243244 !important;
        border-radius: 12px !important;
    }
    
    /* Control wrapper - THE MAIN CONTAINER */
    .stSelectbox [data-baseweb="select"] > div:first-child {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        min-height: auto !important;
        height: auto !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        color: #E5E7EB !important;
    }
    
    /* Selectbox value container - proper alignment with padding */
    .stSelectbox [data-baseweb="select"] div[class*="ValueContainer"] {
        display: flex !important;
        align-items: center !important;
        color: #E5E7EB !important;
        flex: 1 !important;
    }
    
    /* Selected value text - centered within container */
    .stSelectbox [data-baseweb="select"] div[class*="SingleValue"],
    .stSelectbox [data-baseweb="select"] div[class*="singleValue"] {
        color: #E5E7EB !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        margin: 0 !important;
        padding: 0 !important;
        position: relative !important;
        top: 0 !important;
    }
    
    /* Input container alignment */
    .stSelectbox [data-baseweb="select"] div[class*="Input"] {
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        position: relative !important;
        top: 0 !important;
    }
    
    .stSelectbox [data-baseweb="select"] input {
        color: #E5E7EB !important;
        margin: 0 !important;
        padding: 0 !important; 
        position: relative !important;
        top: 0 !important;
    }
    
    /* Indicators container (arrow) - centered with padding */
    .stSelectbox [data-baseweb="select"] div[class*="IndicatorsContainer"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0.85rem 1rem 0.85rem 0.5rem !important;
    }
    
    /* Individual indicator (arrow icon) */
    .stSelectbox [data-baseweb="select"] div[class*="IndicatorsContainer"] > div {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 !important;
        margin: 0 !important;
        position: relative !important;
        top: 0 !important;
    }
    
    /* Force text color on all selectbox internal elements */
    .stSelectbox * {
        color: #E5E7EB !important;
    }
    
    /* Target Streamlit's specific selectbox value container */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child {
        color: #E5E7EB !important;
    }
    
    /* Target the actual text div inside select */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div > div > div {
        color: #E5E7EB !important;
    }
    
    /* Ensure placeholder and selected value are visible */
    [data-testid="stSelectbox"] input {
        color: #E5E7EB !important;
    }
    
    /* Sidebar selectbox specific - very aggressive */
    [data-testid="stSidebar"] .stSelectbox * {
        color: #E5E7EB !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] {
        color: #E5E7EB !important;
    }
    
    /* Target the inner value display */
    [data-testid="stSidebar"] [data-baseweb="select"] div[class*="singleValue"] {
        color: #E5E7EB !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] div[class*="placeholder"] {
        color: #9CA3AF !important;
    }
    
    /* Prevent text clipping */
    .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] > div {
        overflow: visible !important;
    }
    
    .stSelectbox [data-baseweb="select"] div[class*="ValueContainer"] {
        overflow: visible !important;
        flex-wrap: nowrap !important;
    }
    
    /* Text content styling */
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div[class*="singleValue"] {
        white-space: nowrap !important;
        opacity: 1 !important;
        visibility: visible !important;
        color: #E5E7EB !important;
        margin: 0 !important;
        padding: 0 !important;
        position: relative !important;
        top: 0 !important;
        transform: none !important;
    }
    
    /* Let inner text elements flow naturally */
    .stSelectbox [data-baseweb="select"] div[class*="ValueContainer"] > div {
        display: flex !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0 !important;
        position: relative !important;
        top: 0 !important;
    }
    
    /* Ensure the control wrapper has the right structure */
    .stSelectbox [data-baseweb="select"] > div:first-child {
        display: flex !important;
        flex-direction: row !important;
        align-items: stretch !important;
        justify-content: space-between !important;
    }
    
    /* Selectbox dropdown arrow - properly sized and centered */
    .stSelectbox [data-baseweb="select"] svg {
        fill: #E5E7EB !important;
        width: 30px !important;
        height: 30px !important;
        display: block !important;
        vertical-align: middle !important;
        margin: 0 !important;
        position: relative !important;
        top: 0 !important;
        transform: none !important;
    }
    
    .stSelectbox [data-baseweb="select"]:hover > div {
        border-color: #22C55E !important;
        box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1) !important;
    }
    
    .stSelectbox [data-baseweb="select"]:focus-within > div {
        border-color: #22C55E !important;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15) !important;
    }
    
    /* Selectbox dropdown menu */
    [data-baseweb="popover"] {
        background: #1E293B !important;
        border: 2px solid #243244 !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Selectbox dropdown options */
    [data-baseweb="menu"] {
        background: #1E293B !important;
    }
    
    [role="option"] {
        background: #1E293B !important;
        color: #E5E7EB !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    [role="option"]:hover {
        background: linear-gradient(135deg, #243244 0%, #1E293B 100%) !important;
        color: #22C55E !important;
    }
    
    [role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, #1E293B 100%) !important;
        color: #22C55E !important;
        font-weight: 600 !important;
    }
    
    /* Info/Success/Warning/Error boxes */
    .stAlert {
        border-radius: 12px !important;
        border-left-width: 4px !important;
    }
    
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1) !important;
        border-left-color: #22C55E !important;
        color: #22C55E !important;
    }
    
    .stInfo {
        background-color: rgba(56, 189, 248, 0.1) !important;
        border-left-color: #38BDF8 !important;
        color: #38BDF8 !important;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1) !important;
        border-left-color: #F59E0B !important;
        color: #F59E0B !important;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border-left-color: #EF4444 !important;
        color: #EF4444 !important;
    }
    
    /* Chat messages with modern design */
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        border-radius: 16px !important;
        padding: 1.25rem !important;
        margin-bottom: 1rem !important;
        border: 2px solid #243244 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatMessage"]:hover {
        transform: translateX(4px) !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #1E293B 0%, #243244 100%) !important;
        border-left: 4px solid #F59E0B !important;
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.08) 0%, #1E293B 100%) !important;
        border-left: 4px solid #22C55E !important;
    }
    
    /* Chat input with nutrition theme */
    .stChatInput > div > div > div > div > input {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        border: 2px solid #243244 !important;
        border-radius: 24px !important;
        color: #E5E7EB !important;
        padding: 1rem 1.5rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stChatInput > div > div > div > div > input:focus {
        border-color: #22C55E !important;
        box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.15), 0 4px 16px rgba(34, 197, 94, 0.2) !important;
    }
    
    .stChatInput > div > div > div > div > input::placeholder {
        color: #6B7280 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #22C55E !important;
    }
    
    /* Divider */
    hr {
        border-color: #243244 !important;
    }
    
    /* Secondary text */
    .css-10trblm {
        color: #9CA3AF !important;
    }
    
    /* Plotly charts with elevated design */
    .js-plotly-plot {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        border-radius: 16px !important;
        border: 2px solid #243244 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        padding: 0.5rem !important;
    }
    
    /* Images with nutrition theme border */
    img {
        border-radius: 16px !important;
        border: 3px solid #243244 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    img:hover {
        border-color: #22C55E40 !important;
        box-shadow: 0 6px 20px rgba(34, 197, 94, 0.2) !important;
        transform: scale(1.02) !important;
    }
    
    /* Nutrition badge styling - enhanced */
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
    
    /* App header styling - hero section */
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
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar styling */
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
    
    /* Column styling */
    [data-testid="column"] {
        padding: 0.5rem !important;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        border-radius: 16px !important;
        border: 2px solid #243244 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Progress bars */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #22C55E 0%, #16A34A 100%) !important;
    }
    
    /* Tabs styling */
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
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%) !important;
        color: #0F172A !important;
        border-color: #22C55E !important;
    }
    
    /* Toast notifications */
    .stToast {
        background: linear-gradient(135deg, #1E293B 0%, #16213A 100%) !important;
        border: 2px solid #243244 !important;
        border-radius: 12px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
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
    
    if search_button and search_query:
        with st.spinner("Recherche en cours..."):
            # Recherche par code-barres ou nom
            if search_query.isdigit() and len(search_query) >= 8:
                product = api.get_product(search_query)
                products = [product] if product else []
            else:
                products = api.search_products(search_query, page_size=10)
        
        if products:
            st.success(f"✅ {len(products)} produit(s) trouvé(s)")
            
            # Sélection du produit
            product_names = [
                f"{p.get('product_name', 'Sans nom')} - {p.get('brands', 'Sans marque')}"
                for p in products
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
                        st.write("**Ingrédients:**", product_info["ingredients"][:500] + "...")
                
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
                    st.plotly_chart(fig_gauge, use_container_width=True)
                
                with col2:
                    if product_info["nutriments"]:
                        fig_pie = create_nutriments_pie(product_info["nutriments"])
                        st.plotly_chart(fig_pie, use_container_width=True)
                
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
                
                if st.button(f"🗑️ Retirer", key=f"remove_{idx}", use_container_width=True):
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
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse comparative IA
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🤖 Analyse comparative IA", type="primary", use_container_width=True):
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
            if st.button("🗑️ Vider le comparateur", use_container_width=True):
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
        if st.sidebar.button(f"{emoji} {suggestion}", use_container_width=True):
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