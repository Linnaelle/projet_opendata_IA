import plotly.graph_objects as go
import plotly.express as px
from typing import Dict

def create_nutriscore_gauge(score: str) -> go.Figure:
    """Crée une jauge Nutri-Score"""
    score_map = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "N/A": 0}
    value = score_map.get(score, 0)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Nutri-Score: {score}"},
        gauge={
            'axis': {'range': [None, 5], 'tickvals': [1, 2, 3, 4, 5], 
                     'ticktext': ['E', 'D', 'C', 'B', 'A']},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 1], 'color': "red"},
                {'range': [1, 2], 'color': "orange"},
                {'range': [2, 3], 'color': "yellow"},
                {'range': [3, 4], 'color': "lightgreen"},
                {'range': [4, 5], 'color': "green"}
            ],
        }
    ))
    
    fig.update_layout(height=300)
    return fig

def create_nutriments_pie(nutriments: Dict) -> go.Figure:
    """Crée un pie chart des nutriments"""
    labels = []
    values = []
    
    nutrients = {
        "Protéines": nutriments.get("proteins_100g", 0),
        "Glucides": nutriments.get("carbohydrates_100g", 0),
        "Lipides": nutriments.get("fat_100g", 0),
        "Fibres": nutriments.get("fiber_100g", 0),
    }
    
    for label, value in nutrients.items():
        if value > 0:
            labels.append(label)
            values.append(value)
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(title_text="Composition nutritionnelle (pour 100g)")
    return fig

def create_comparison_chart(products: list) -> go.Figure:
    """Compare plusieurs produits"""
    names = [p["name"][:30] for p in products]
    scores = [ord(p["nutriscore"]) - ord('A') if p["nutriscore"] != "N/A" else 5 for p in products]
    
    fig = go.Figure(data=[
        go.Bar(x=names, y=scores, marker_color=['green', 'lightgreen', 'yellow', 'orange', 'red'])
    ])
    
    fig.update_layout(
        title="Comparaison Nutri-Score",
        yaxis_title="Score (A=0, E=4)",
        xaxis_title="Produits"
    )
    return fig