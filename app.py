import streamlit as st
from dotenv import load_dotenv
import os
from utils.data import OpenFoodFactsAPI
from utils.charts import create_nutriscore_gauge, create_nutriments_pie, create_comparison_chart
from utils.chatbot import NutriChatbot

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="🥗 NutriScan",
    page_icon="🥗",
    layout="wide"
)

# Initialiser l'API et le chatbot
api = OpenFoodFactsAPI()

if "chatbot" not in st.session_state:
    st.session_state.chatbot = NutriChatbot(model="gpt-4o-mini")

if "comparison_products" not in st.session_state:
    st.session_state.comparison_products = []

# Header
st.title("🥗 NutriScan - Assistant Nutrition Intelligent")
st.markdown("*Analysez vos produits alimentaires avec l'IA*")

# Sidebar - Navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["🔍 Recherche Produit", "⚖️ Comparateur", "💬 Chatbot Nutrition"]
)

# ===== PAGE 1: RECHERCHE PRODUIT =====
if page == "🔍 Recherche Produit":
    st.header("Rechercher un produit")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Nom du produit ou code-barres",
            placeholder="Ex: Nutella, 3017620422003"
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
                    if product_info["image_url"]:
                        st.image(product_info["image_url"], width=250)
                    
                    st.metric("Nutri-Score", product_info["nutriscore"])
                    st.metric("NOVA Group", product_info["nova_group"])
                    
                    # Bouton ajout comparateur
                    if st.button("➕ Ajouter au comparateur"):
                        if product_info not in st.session_state.comparison_products:
                            st.session_state.comparison_products.append(product_info)
                            st.success("Produit ajouté !")
                
                with col2:
                    st.subheader(f"{product_info['name']}")
                    st.caption(f"Marque: {product_info['brands']}")
                    
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
                
                # Visualisations
                st.subheader("📊 Visualisations")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_gauge = create_nutriscore_gauge(product_info["nutriscore"])
                    st.plotly_chart(fig_gauge, use_container_width=True)
                
                with col2:
                    if product_info["nutriments"]:
                        fig_pie = create_nutriments_pie(product_info["nutriments"])
                        st.plotly_chart(fig_pie, use_container_width=True)
                
                # Alternatives
                st.subheader("🔄 Alternatives recommandées")
                with st.spinner("Recherche d'alternatives..."):
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
    st.header("Comparateur de produits")
    
    if len(st.session_state.comparison_products) == 0:
        st.info("👈 Ajoutez des produits depuis la page de recherche")
    else:
        st.success(f"📦 {len(st.session_state.comparison_products)} produit(s) dans le comparateur")
        
        # Affichage des produits
        cols = st.columns(len(st.session_state.comparison_products))
        
        for idx, product in enumerate(st.session_state.comparison_products):
            with cols[idx]:
                st.image(product["image_url"] if product["image_url"] else "https://via.placeholder.com/150", width=150)
                st.write(f"**{product['name'][:30]}**")
                st.metric("Nutri-Score", product["nutriscore"])
                st.metric("NOVA", product["nova_group"])
                
                if st.button(f"🗑️ Retirer", key=f"remove_{idx}"):
                    st.session_state.comparison_products.pop(idx)
                    st.rerun()
        
        # Graphique de comparaison
        st.subheader("📊 Comparaison visuelle")
        fig = create_comparison_chart(st.session_state.comparison_products)
        st.plotly_chart(fig, use_container_width=True)
        
        # Analyse comparative IA
        if st.button("🤖 Analyse comparative"):
            with st.spinner("Génération de l'analyse..."):
                comparison_text = "\n".join([
                    f"- {p['name']} (Nutri-Score {p['nutriscore']}, NOVA {p['nova_group']})"
                    for p in st.session_state.comparison_products
                ])
                
                prompt = f"Compare ces produits et dis lequel est le meilleur choix nutritionnel:\n{comparison_text}"
                analysis = st.session_state.chatbot.chat(prompt)
                st.info(analysis)
        
        if st.button("🗑️ Vider le comparateur"):
            st.session_state.comparison_products = []
            st.rerun()

# ===== PAGE 3: CHATBOT =====
elif page == "💬 Chatbot Nutrition":
    st.header("Assistant Nutrition")
    st.markdown("*Posez vos questions sur l'alimentation et la nutrition*")
    
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
    
    # Suggestions de questions
    st.sidebar.subheader("💡 Questions suggérées")
    suggestions = [
        "C'est quoi le Nutri-Score ?",
        "Qu'est-ce que le groupe NOVA ?",
        "Pourquoi éviter les additifs ?",
        "Comment lire une étiquette nutritionnelle ?",
        "Quels sont les sucres cachés ?"
    ]
    
    for suggestion in suggestions:
        if st.sidebar.button(suggestion):
            st.session_state.chat_history.append({"role": "user", "content": suggestion})
            with st.spinner("Réflexion..."):
                response = st.session_state.chatbot.chat(suggestion)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**📚 Sources de données**
- OpenFoodFacts API
- ANSES (tables nutritionnelles)

**🤖 IA**
- Modèles via LiteLLM
""")