import plotly.graph_objects as go
import plotly.express as px
from typing import Dict

# Dark theme colors from palette
COLORS = {
    'primary_bg': '#0F172A',
    'secondary_bg': '#16213A',
    'elevated': '#1E293B',
    'primary_green': '#22C55E',
    'primary_green_dark': '#16A34A',
    'warm_accent': '#F59E0B',
    'text_primary': '#E5E7EB',
    'text_secondary': '#9CA3AF',
    'error': '#EF4444',
    'success': '#22C55E',
    'warning': '#F59E0B',
}

def create_nutriscore_gauge(score: str) -> go.Figure:
    """Crée une jauge Nutri-Score avec thème sombre"""
    score_map = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "N/A": 0}
    value = score_map.get(score, 0)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': f"<b>Nutri-Score: {score}</b>",
            'font': {'color': COLORS['text_primary'], 'size': 20}
        },
        number={'font': {'color': COLORS['primary_green'], 'size': 40}},
        gauge={
            'axis': {
                'range': [None, 5],
                'tickvals': [1, 2, 3, 4, 5],
                'ticktext': ['E', 'D', 'C', 'B', 'A'],
                'tickfont': {'color': COLORS['text_secondary']}
            },
            'bar': {'color': COLORS['primary_green']},
            'steps': [
                {'range': [0, 1], 'color': '#EF4444'},
                {'range': [1, 2], 'color': '#F59E0B'},
                {'range': [2, 3], 'color': '#FCD34D'},
                {'range': [3, 4], 'color': '#84CC16'},
                {'range': [4, 5], 'color': '#22C55E'}
            ],
            'threshold': {
                'line': {'color': COLORS['text_primary'], 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        paper_bgcolor=COLORS['elevated'],
        plot_bgcolor=COLORS['elevated'],
        font={'color': COLORS['text_primary']},
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def create_nutriments_pie(nutriments: Dict) -> go.Figure:
    """Crée un pie chart des nutriments avec thème sombre"""
    labels = []
    values = []
    
    nutrients = {
        "Protéines": nutriments.get("proteins_100g", 0),
        "Glucides": nutriments.get("carbohydrates_100g", 0),
        "Lipides": nutriments.get("fat_100g", 0),
        "Fibres": nutriments.get("fiber_100g", 0),
    }
    
    # Custom colors for each nutrient
    colors_map = {
        "Protéines": '#22C55E',  # Green
        "Glucides": '#F59E0B',   # Warm accent
        "Lipides": '#EF4444',    # Red
        "Fibres": '#38BDF8',     # Blue
    }
    
    pie_colors = []
    for label, value in nutrients.items():
        if value > 0:
            labels.append(label)
            values.append(value)
            pie_colors.append(colors_map.get(label, COLORS['text_secondary']))
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.4,
        marker=dict(colors=pie_colors, line=dict(color=COLORS['primary_bg'], width=2)),
        textfont=dict(color=COLORS['text_primary'], size=14),
        hovertemplate='<b>%{label}</b><br>%{value}g (%{percent})<extra></extra>'
    )])
    
    fig.update_layout(
        title={
            'text': '<b>Composition nutritionnelle</b><br>(pour 100g)',
            'font': {'color': COLORS['text_primary'], 'size': 18},
            'x': 0.5,
            'xanchor': 'center'
        },
        paper_bgcolor=COLORS['elevated'],
        plot_bgcolor=COLORS['elevated'],
        font={'color': COLORS['text_primary']},
        showlegend=True,
        legend=dict(
            font=dict(color=COLORS['text_primary']),
            bgcolor=COLORS['secondary_bg'],
            bordercolor=COLORS['text_secondary'],
            borderwidth=1
        ),
        height=350,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    return fig

def create_comparison_chart(products: list) -> go.Figure:
    """Compare plusieurs produits avec thème sombre"""
    names = [p["name"][:30] for p in products]
    nutriscores = [p["nutriscore"] for p in products]
    scores = [ord(p["nutriscore"]) - ord('A') if p["nutriscore"] != "N/A" else 5 for p in products]
    
    # Color mapping based on nutriscore
    color_map = {'A': '#22C55E', 'B': '#84CC16', 'C': '#FCD34D', 'D': '#F59E0B', 'E': '#EF4444', 'N/A': '#6B7280'}
    colors = [color_map.get(score, '#6B7280') for score in nutriscores]
    
    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=scores,
            marker=dict(
                color=colors,
                line=dict(color=COLORS['primary_bg'], width=1.5)
            ),
            text=nutriscores,
            textposition='outside',
            textfont=dict(color=COLORS['text_primary'], size=14, family='Inter'),
            hovertemplate='<b>%{x}</b><br>Nutri-Score: %{text}<br>Score: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': '<b>Comparaison Nutri-Score</b>',
            'font': {'color': COLORS['text_primary'], 'size': 20},
            'x': 0.5,
            'xanchor': 'center'
        },
        yaxis=dict(
            title='Score (A=0, E=4)',
            titlefont=dict(color=COLORS['text_secondary']),
            tickfont=dict(color=COLORS['text_secondary']),
            gridcolor=COLORS['secondary_bg'],
            range=[0, max(scores) + 1] if scores else [0, 5]
        ),
        xaxis=dict(
            title='Produits',
            titlefont=dict(color=COLORS['text_secondary']),
            tickfont=dict(color=COLORS['text_primary']),
            tickangle=-45
        ),
        paper_bgcolor=COLORS['elevated'],
        plot_bgcolor=COLORS['elevated'],
        font={'color': COLORS['text_primary']},
        height=400,
        margin=dict(l=60, r=40, t=80, b=120),
        showlegend=False
    )
    return fig