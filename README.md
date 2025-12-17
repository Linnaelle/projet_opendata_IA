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

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API OpenAI/Anthropic
```

## Lancement
```bash
# Activer l'environnement et lancer l'app
uv run streamlit
uv run app.py
```

L'application sera accessible sur `http://localhost:8501`

## Sources de données

- [OpenFoodFacts API](https://openfoodfacts.github.io/openfoodfacts-server/api/) - Base de produits alimentaires
- [ANSES Ciqual](https://www.data.gouv.fr/fr/datasets/table-de-composition-nutritionnelle-des-aliments-ciqual/) - Tables nutritionnelles

## Technologies

- **Frontend**: Streamlit
- **Visualisations**: Plotly
- **IA**: LiteLLM (OpenAI GPT-4, Anthropic Claude)
- **Données**: OpenFoodFacts API, Pandas

## Équipe

- Perret Clément
- Sode Paul
- Araud Jules
- Le Goff Philippe

## 📄 Licence

MIT License