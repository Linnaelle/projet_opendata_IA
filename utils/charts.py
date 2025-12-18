import plotly.graph_objects as go
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

# ✅ Mapping centralisé et cohérent
NUTRISCORE_MAP = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
    "E": 1,
    "N/A": 0
}

NUTRISCORE_COLORS = {
    'A': '#22C55E',
    'B': '#84CC16',
    'C': '#FCD34D',
    'D': '#F59E0B',
    'E': '#EF4444',
    'N/A': '#6B7280'
}

def create_nutriscore_gauge(score: str) -> go.Figure:
    """Crée une jauge Nutri-Score avec thème sombre"""
    value = NUTRISCORE_MAP.get(score, 0)

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
                'range': [0, 5],
                'tickvals': [1, 2, 3, 4, 5],
                'ticktext': ['E', 'D', 'C', 'B', 'A'],
                'tickfont': {'color': COLORS['text_secondary']}
            },
            'bar': {'color': COLORS['primary_green']},
            'steps': [
                {'range': [0, 1], 'color': '#6B7280'},
                {'range': [1, 2], 'color': '#EF4444'},
                {'range': [2, 3], 'color': '#F59E0B'},
                {'range': [3, 4], 'color': '#FCD34D'},
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
    nutrients = {
        "Protéines": nutriments.get("proteins_100g", 0),
        "Glucides": nutriments.get("carbohydrates_100g", 0),
        "Lipides": nutriments.get("fat_100g", 0),
        "Fibres": nutriments.get("fiber_100g", 0),
    }

    colors_map = {
        "Protéines": '#22C55E',
        "Glucides": '#F59E0B',
        "Lipides": '#EF4444',
        "Fibres": '#38BDF8',
    }

    labels, values, pie_colors = [], [], []

    for label, value in nutrients.items():
        if value > 0:
            labels.append(label)
            values.append(value)
            pie_colors.append(colors_map.get(label))

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=pie_colors, line=dict(color=COLORS['primary_bg'], width=2)),
        textfont=dict(color=COLORS['text_primary'], size=14),
        hovertemplate='<b>%{label}</b><br>%{value}g (%{percent})<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text='<b>Composition nutritionnelle</b><br>(pour 100g)',
            x=0.5,
            xanchor='center',
            font=dict(color=COLORS['text_primary'], size=18)
        ),
        paper_bgcolor=COLORS['elevated'],
        plot_bgcolor=COLORS['elevated'],
        font=dict(color=COLORS['text_primary']),
        height=350,
        margin=dict(l=20, r=20, t=80, b=20)
    )
    return fig

def create_comparison_chart(products: list) -> go.Figure:
    """Compare plusieurs produits avec thème sombre"""
    names = [p["name"][:30] for p in products]
    nutriscores = [p["nutriscore"] for p in products]
    scores = [NUTRISCORE_MAP.get(score, 0) for score in nutriscores]
    colors = [NUTRISCORE_COLORS.get(score, COLORS['text_secondary']) for score in nutriscores]

    fig = go.Figure(go.Bar(
        x=names,
        y=scores,
        marker=dict(
            color=colors,
            line=dict(color=COLORS['primary_bg'], width=1.5)
        ),
        text=nutriscores,
        textposition='outside',
        textfont=dict(color=COLORS['text_primary'], size=14),
        hovertemplate='<b>%{x}</b><br>Nutri-Score: %{text}<extra></extra>',
        cliponaxis=False
    ))

    fig.update_layout(
        title=dict(
            text='<b>Comparaison Nutri-Score</b>',
            x=0.5,
            xanchor='center',
            font=dict(color=COLORS['text_primary'], size=20)
        ),
        yaxis=dict(
            title=dict(
                text='Qualité nutritionnelle (A meilleur → E moins bon)',
                font=dict(color=COLORS['text_secondary'])
            ),
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['E', 'D', 'C', 'B', 'A'],
            range=[0, 5.5],
            gridcolor=COLORS['secondary_bg'],
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        xaxis=dict(
            title=dict(
                text='Produits',
                font=dict(color=COLORS['text_secondary'])
            ),
            tickangle=-45,
            tickfont=dict(color=COLORS['text_primary'])
        ),
        paper_bgcolor=COLORS['elevated'],
        plot_bgcolor=COLORS['elevated'],
        height=400,
        margin=dict(l=60, r=40, t=80, b=120),
        showlegend=False
    )

    return fig
