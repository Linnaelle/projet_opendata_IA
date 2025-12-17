# Sujets de Projet — Module Open Data & IA

## Informations générales

| | |
|---|---|
| **Durée** | J3 après-midi (briefing) + J4 complet |
| **Format** | Travail en groupe (3-4 personnes) |
| **Livrable** | Application + Repository GitHub + Présentation |
| **Présentation** | 15-20 min + 5 min questions |

---

## Critères d'évaluation communs

| Critère | Points | Description |
|---------|--------|-------------|
| **Qualité technique** | /5 | Code propre, architecture, bonnes pratiques (uv, .env, etc.) |
| **Utilisation Open Data** | /4 | Pertinence et richesse des sources de données |
| **Intégration IA** | /4 | Usage créatif et pertinent des LLMs via LiteLLM |
| **Interface utilisateur** | /3 | Ergonomie, fonctionnalités, expérience utilisateur |
| **Présentation orale** | /4 | Clarté, démo live, réponses aux questions |
| **Total** | /20 | |

---

## Contraintes techniques obligatoires

Chaque projet **DOIT** inclure :

1. ✅ **Gestion de projet avec `uv`** (pyproject.toml, dépendances gérées)
2. ✅ **Au moins une source Open Data** (API ou fichier)
3. ✅ **Intégration LiteLLM** avec au moins 2 modèles différents disponibles
4. ✅ **Interface utilisateur** (Streamlit ou Gradio)
5. ✅ **Au moins 3 visualisations** interactives
6. ✅ **Repository GitHub** avec README complet

---

# SUJET 1 : NutriScan — L'assistant nutrition intelligent

## 📋 Contexte

Les consommateurs sont de plus en plus soucieux de leur alimentation, mais les informations nutritionnelles restent difficiles à interpréter. Vous développez **NutriScan**, une application qui aide les utilisateurs à comprendre et améliorer leurs choix alimentaires.

## 🎯 Objectifs

1. **Analyse nutritionnelle automatisée** : Scanner un produit (code-barres ou recherche) et obtenir une analyse détaillée générée par IA
2. **Recommandation de substituts** : Proposer des alternatives plus saines basées sur les préférences
3. **Comparateur de produits** : Comparer plusieurs produits côte à côte
4. **Chatbot nutrition** : Répondre aux questions sur les ingrédients, additifs, allergènes

## 📊 Sources de données

- **OpenFoodFacts API** : Base de produits alimentaires
  - https://openfoodfacts.github.io/openfoodfacts-server/api/
- **Tables de composition nutritionnelle** (ANSES) : Données de référence
  - https://www.data.gouv.fr/fr/datasets/table-de-composition-nutritionnelle-des-aliments-ciqual/

## 🤖 Intégrations IA attendues

| Fonctionnalité | Rôle de l'IA |
|----------------|--------------|
| Analyse produit | Interpréter le Nutri-Score, NOVA, additifs en langage clair |
| Recommandation | Suggérer des alternatives basées sur le profil utilisateur |
| Chatbot | Répondre aux questions nutritionnelles |
| Génération | Créer des résumés personnalisés |

## 💡 Fonctionnalités suggérées

- Barre de recherche avec autocomplétion
- Fiche produit détaillée avec visualisations
- Comparateur multi-produits
- Historique des produits consultés
- Filtres par allergènes, régimes (végan, sans gluten, etc.)

## 📐 Maquette suggérée

```
┌─────────────────────────────────────────────────────────────┐
│  🥗 NutriScan                              [Rechercher...]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────────────────────────────┐   │
│  │   [Image]   │  │ Nutella - Ferrero                   │   │
│  │             │  │ ────────────────────────            │   │
│  │  Nutri: E   │  │ 🤖 Analyse IA :                     │   │
│  │  NOVA: 4    │  │ "Ce produit est ultra-transformé    │   │
│  └─────────────┘  │  avec une teneur élevée en sucre..."│   │
│                   └─────────────────────────────────────┘   │
│                                                             │
│  📊 Composition          🔄 Alternatives recommandées       │
│  ┌─────────────────┐    ┌────────────────────────────┐     │
│  │ [Pie Chart]     │    │ • Nocciolata (Score B)     │     │
│  │ Sucres: 57%     │    │ • Pâte noisette bio (A)    │     │
│  └─────────────────┘    └────────────────────────────┘     │
│                                                             │
│  💬 Posez une question : [________________________] [Envoyer]│
└─────────────────────────────────────────────────────────────┘
```

---

# SUJET 2 : SafeCity — Tableau de bord sécurité urbaine

## 📋 Contexte

Vous êtes mandatés par une collectivité locale pour développer un outil d'analyse de la criminalité. L'objectif : aider les décideurs à comprendre les tendances et orienter les politiques de prévention.

## 🎯 Objectifs

1. **Cartographie interactive** : Visualiser les crimes/délits par zone géographique
2. **Analyse temporelle** : Identifier les tendances et saisonnalités
3. **Comparateur territorial** : Comparer les départements/communes
4. **Assistant analyse** : Générer des rapports automatiques avec l'IA

## 📊 Sources de données

- **Crimes et délits** (Ministère de l'Intérieur)
  - https://www.data.gouv.fr/fr/datasets/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012/
- **Contours géographiques** (IGN)
  - https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/
- **Population INSEE**
  - https://www.insee.fr/fr/statistiques/1893198

## 🤖 Intégrations IA attendues

| Fonctionnalité | Rôle de l'IA |
|----------------|--------------|
| Analyse tendances | Interpréter les évolutions et anomalies |
| Génération rapport | Créer des synthèses textuelles automatiques |
| Comparaison | Contextualiser les chiffres (population, densité) |
| Chatbot | Répondre aux questions sur les statistiques |

## 💡 Fonctionnalités suggérées

- Carte choroplèthe interactive (Plotly/Folium)
- Graphiques d'évolution temporelle
- Filtres par type de délit, période, zone
- Export de rapports PDF
- Comparateur multi-territoires

## 📐 Maquette suggérée

```
┌─────────────────────────────────────────────────────────────┐
│  🏛️ SafeCity Dashboard                    [Période ▼]       │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────┐  ┌─────────────────────────┐ │
│  │                           │  │ 📊 Statistiques clés    │ │
│  │     [Carte de France]     │  │ ─────────────────────   │ │
│  │                           │  │ Total : 1.2M délits     │ │
│  │      🔴 Paris             │  │ Évolution : +3.2%       │ │
│  │      🟠 Lyon              │  │ Top : Vols (45%)        │ │
│  │      🟡 Marseille         │  └─────────────────────────┘ │
│  │                           │                              │
│  └───────────────────────────┘  ┌─────────────────────────┐ │
│                                  │ 🤖 Analyse IA           │ │
│  ┌───────────────────────────┐  │ "Les vols avec violence │ │
│  │ [Graphique évolution]     │  │  ont augmenté de 12%    │ │
│  │ ══════════════════════    │  │  en Île-de-France..."   │ │
│  └───────────────────────────┘  └─────────────────────────┘ │
│                                                             │
│  💬 Question : [Quel département a le plus progressé ?]     │
└─────────────────────────────────────────────────────────────┘
```

---

# SUJET 3 : EcoRoute — Calculateur d'impact carbone transport

## 📋 Contexte

Face à l'urgence climatique, les citoyens veulent connaître l'impact environnemental de leurs déplacements. Vous créez **EcoRoute**, une application qui calcule et compare l'empreinte carbone de différents modes de transport.

## 🎯 Objectifs

1. **Calcul d'empreinte** : Estimer les émissions CO2 d'un trajet
2. **Comparateur de modes** : Train vs Voiture vs Avion vs Vélo
3. **Suggestions d'optimisation** : Proposer des alternatives moins polluantes
4. **Assistant éco-mobilité** : Conseils personnalisés via chatbot

## 📊 Sources de données

- **Horaires et trajets SNCF** (SNCF Open Data)
  - https://ressources.data.sncf.com/
- **Facteurs d'émission** (ADEME)
  - https://www.data.gouv.fr/fr/datasets/base-carbone-r/
- **Qualité de l'air** (Atmo)
  - https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/

## 🤖 Intégrations IA attendues

| Fonctionnalité | Rôle de l'IA |
|----------------|--------------|
| Conseil trajet | Suggérer le mode optimal selon contexte |
| Comparaison | Expliquer les différences d'impact en termes concrets |
| Équivalences | Traduire en équivalences parlantes (km en voiture = X arbres) |
| Chatbot | Répondre aux questions sur l'éco-mobilité |

## 💡 Fonctionnalités suggérées

- Formulaire de trajet (départ, arrivée)
- Comparateur visuel des modes de transport
- Historique des trajets avec cumul CO2
- Objectifs de réduction personnalisés
- Badges/gamification

## 📐 Maquette suggérée

```
┌─────────────────────────────────────────────────────────────┐
│  🌱 EcoRoute                                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📍 De : [Paris________]    📍 À : [Lyon_________]          │
│                                      [Calculer 🔍]          │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │   🚗 Voiture     🚄 Train      ✈️ Avion      🚴 Vélo    ││
│  │   ────────────────────────────────────────────────────  ││
│  │   45 kg CO2      2.5 kg CO2   150 kg CO2   0 kg CO2    ││
│  │   ⬛⬛⬛⬛⬛⬛⬛⬛⬛  ⬛            ⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛  ✅        ││
│  │                                                         ││
│  │   🏆 Recommandé : Train (18x moins polluant que avion)  ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  🤖 "Prendre le train pour ce trajet équivaut à planter    │
│      2 arbres. En un an de trajets domicile-travail, vous  │
│      économiseriez 1.2 tonnes de CO2 vs la voiture."       │
│                                                             │
│  💬 Question : [Comment réduire mon bilan carbone ?]        │
└─────────────────────────────────────────────────────────────┘
```

---

# SUJET 4 : HealthMap — Déserts médicaux et accès aux soins

## 📋 Contexte

L'accès aux soins est un enjeu majeur de santé publique. Vous développez **HealthMap**, un outil qui cartographie les déserts médicaux et aide les citoyens à trouver des professionnels de santé.

## 🎯 Objectifs

1. **Cartographie des professionnels** : Visualiser la répartition des médecins, pharmacies, hôpitaux
2. **Détection des déserts** : Identifier les zones sous-dotées
3. **Recherche intelligente** : Trouver le professionnel le plus adapté
4. **Assistant santé** : Conseils d'orientation via chatbot

## 📊 Sources de données

- **Annuaire santé** (Ministère de la Santé)
  - https://annuaire.sante.fr/web/site-pro/extractions-publiques
- **Population par commune** (INSEE)
  - https://www.insee.fr/fr/statistiques/6011070
- **Contours géographiques**
  - https://www.data.gouv.fr/fr/datasets/contours-des-communes-de-france-simplifie-avec-regions-et-departement-doutre-mer-rapproches/

## 🤖 Intégrations IA attendues

| Fonctionnalité | Rôle de l'IA |
|----------------|--------------|
| Analyse zone | Évaluer le niveau d'accès aux soins |
| Recommandation | Suggérer des professionnels selon symptômes/besoins |
| Comparaison | Contextualiser vs moyennes nationales |
| Chatbot | Orienter vers le bon type de professionnel |

## 💡 Fonctionnalités suggérées

- Carte interactive avec filtres (spécialité, horaires)
- Indicateur de densité médicale par zone
- Recherche par symptômes/besoins
- Calcul du temps d'accès au professionnel le plus proche
- Comparateur de territoires

---

# SUJET 5 : Projet Libre

## 📋 Cadre

Vous avez carte blanche pour proposer un projet original, sous réserve de respecter les contraintes suivantes :

## ✅ Contraintes obligatoires

1. **Open Data** : Utiliser au moins 2 sources de données ouvertes
2. **IA intégrée** : Au moins 3 fonctionnalités utilisant LiteLLM
3. **Interface** : Application Streamlit ou Gradio fonctionnelle
4. **Visualisations** : Au moins 4 visualisations interactives différentes
5. **Chatbot** : Intégration d'un assistant conversationnel
6. **Innovation** : Proposer quelque chose d'original (pas de copie des sujets précédents)

## 💡 Idées de thématiques

- **Immobilier** : Analyse des prix avec DVF + prédiction
- **Sport** : Analyse des performances avec données fédérations
- **Culture** : Exploration des musées, monuments, événements
- **Éducation** : Carte des établissements, résultats, orientations
- **Énergie** : Consommation, production renouvelable, mix énergétique
- **Emploi** : Offres, salaires, tendances par secteur

## 📝 Validation

Avant de commencer, faites valider votre sujet par l'intervenant avec :
- Description en 3 phrases
- Sources de données identifiées
- Liste des fonctionnalités IA prévues

---

# Livrables attendus (tous sujets)

## 📁 Repository GitHub

```
projet-opendata/
├── .env.example        # Template des variables d'environnement
├── .gitignore
├── pyproject.toml      # Gestion uv
├── README.md           # Documentation complète
├── app.py              # Application principale
├── utils/
│   ├── __init__.py
│   ├── data.py
│   ├── charts.py
│   └── chatbot.py
├── data/
│   └── processed/
└── notebooks/          # Exploration (optionnel)
```

## 📝 README.md obligatoire

```markdown
# [Nom du projet]

## 📋 Description
[2-3 phrases décrivant le projet]

## 🎯 Fonctionnalités
- Feature 1
- Feature 2
- ...

## 🛠️ Installation

\`\`\`bash
# Cloner le repo
git clone [url]
cd [projet]

# Installer avec uv
uv sync

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API
\`\`\`

## 🚀 Lancement

\`\`\`bash
uv run streamlit run app.py
# ou
uv run python app.py  # pour Gradio
\`\`\`

## 📊 Sources de données
- [Source 1](url) - Description
- [Source 2](url) - Description

## 👥 Équipe
- Nom 1
- Nom 2
- ...

## 📄 Licence
MIT
```

## 🎤 Présentation orale

- **Durée** : 15-20 minutes + 5 min questions
- **Format** : Slides + Démo live
- **Contenu suggéré** :
  1. Contexte et problématique (2 min)
  2. Sources de données (2 min)
  3. Architecture technique (3 min)
  4. Démo live de l'application (8 min)
  5. Difficultés rencontrées et apprentissages (3 min)
  6. Questions (5 min)

---

## 📅 Planning

| Étape | Horaire |
|-------|---------|
| **J3 - 17h15** | Présentation des sujets, constitution des groupes |
| **J4 - 9h00** | Début du travail en groupe |
| **J4 - 13h00** | Point d'avancement (optionnel) |
| **J4 - 15h15** | Début des présentations |
| **J4 - 17h15** | Fin des présentations, debrief |

Bonne chance ! 🚀
