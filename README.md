# NutriScan - Assistant Nutrition Intelligent

## Description

NutriScan est une application web qui aide les consommateurs à comprendre et améliorer leurs choix alimentaires grâce à l'intelligence artificielle.

## Fonctionnalités

- **Recherche de produits** : Scanner un produit par code-barres ou nom
- **Analyse IA** : Interprétation automatique du Nutri-Score et NOVA
- **Recommandations** : Suggestions d'alternatives plus saines
- **Comparateur** : Comparer plusieurs produits côte à côte
- **Chatbot nutrition** : Réponses aux questions nutritionnelles
- **Visualisations** : Graphiques interactifs (Nutri-Score, composition)

## Installation

### Prérequis
- Python 3.10+
- uv

### Étapes
```bash
# Cloner le repository
git clone https://github.com/votre-username/nutriscan.git
cd nutriscan

# Installer les dépendances avec uv
uv sync

# Configurer les variables d'environnement (optionnel mais recommandé)
cp .env.example .env
# Éditer .env avec vos clés API et préférences de modèle
# Exemple:
#   NUTRISCAN_PROVIDER=ollama        # openai | gemini | ollama
#   NUTRISCAN_MODEL_OPENAI=gpt-4o-mini
#   NUTRISCAN_MODEL_GEMINI=gemini/gemini-2.0-flash-exp
#   NUTRISCAN_MODEL_OLLAMA=ollama/mistral
#   OLLAMA_API_BASE=http://localhost:11434
```

## Lancement

### Option 1: Avec Ollama (local - recommandé)

**Terminal 1** - Démarrer Ollama:
```bash
ollama serve
ollama pull mistral  # première fois uniquement
```

**Terminal 2** - Lancer NutriScan:
```bash
cd projet_opendata_IA
export NUTRISCAN_PROVIDER=ollama  # optionnel si déjà dans .env
uv run streamlit run app.py
```

### Option 2: Avec Gemini ou OpenAI

```bash
# Créer votre .env
cp env.example.txt .env

# Éditer .env et ajouter votre clé
# GEMINI_API_KEY=votre_clé  (ou OPENAI_API_KEY)
# NUTRISCAN_PROVIDER=gemini  (ou openai)

# Lancer l'app
uv run streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

💡 **Dans l'app**, vous pouvez changer de modèle via la sidebar **🤖 Modèle IA**

## Sources de données

- [OpenFoodFacts API](https://openfoodfacts.github.io/openfoodfacts-server/api/) - Base de produits alimentaires
- [ANSES Ciqual](https://www.data.gouv.fr/fr/datasets/table-de-composition-nutritionnelle-des-aliments-ciqual/) - Tables nutritionnelles

## Technologies

- **Frontend**: Streamlit avec thème personnalisé (dark mode nutrition-focused)
- **Visualisations**: Plotly (charts interactifs avec palette cohérente)
- **IA**: LiteLLM multi-provider (OpenAI GPT, Google Gemini, Ollama local)
- **Données**: OpenFoodFacts API, DuckDB, Pandas
- **Gestion projet**: uv (gestionnaire Python moderne)

## Équipe

- Perret Clément
- Sode Paul
- Araud Jules
- Le Goff Philippe

## 📄 Licence

MIT License