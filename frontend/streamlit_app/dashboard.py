import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

def risk_assessment_chart(risk_score: float, benchmarks: Dict[str, List[float]]) -> Any:
    """
    Create an interactive risk assessment radar chart
    """
    categories = ['Volatility', 'Liquidity', 'Concentration', 'Horizon', 'Capacity']
    
    fig = px.line_polar(
        r=benchmarks['conservative'],
        theta=categories,
        line_close=True,
        template="plotly_dark",
        color_discrete_sequence=["#1F77B4"]
    )
    
    # Add user profile trace
    fig.add_trace(px.line_polar(
        r=[v * risk_score/100 for v in benchmarks['conservative']],
        theta=categories,
        line_close=True
    ).data[0].update(
        fill='toself',
        opacity=0.5,
        line_color="#FF4B4B",
        name="Your Profile"
    ))
    
    # Add aggressive benchmark trace
    fig.add_trace(px.line_polar(
        r=benchmarks['aggressive'],
        theta=categories,
        line_close=True
    ).data[0].update(
        fill='toself',
        opacity=0.3,
        line_color="#2CA02C",
        name="Aggressive"
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        title="Risk Profile Analysis",
        font=dict(
            family="Arial",
            size=12,
            color="white"
        ),
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

def financial_health_meter(score: float) -> Any:
    """
    Create a financial health gauge chart
    """
    fig = px.indicators.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title="Financial Health Score",
        gauge={
            'axis': {'range': [None, 100]},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "green"}],
            'bar': {'color': "#4B78FF"},
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    )
    
    fig.update_layout(
        font=dict(color="white"),
        paper_bgcolor="#0E1117",
        margin=dict(t=50, b=10)
    )
    return fig

def cashflow_calendar_heatmap(transactions: pd.DataFrame) -> Any:
    """
    Create an interactive calendar heatmap of cashflow
    """
    transactions = transactions.copy()
    transactions['date'] = pd.to_datetime(transactions['date'])
    transactions['day'] = transactions['date'].dt.day_name()
    transactions['week'] = transactions['date'].dt.isocalendar().week
    transactions['month'] = transactions['date'].dt.month_name()
    
    # Order days of week properly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    transactions['day'] = pd.Categorical(
        transactions['day'],
        categories=day_order,
        ordered=True
    )
    
    daily_totals = transactions.groupby(
        ['month', 'week', 'day', 'date']
    )['amount'].sum().reset_index()
    
    fig = px.density_heatmap(
        daily_totals,
        x='day',
        y='week',
        z='amount',
        facet_col='month',
        facet_col_wrap=3,
        color_continuous_scale='Viridis',
        title="Daily Cashflow Patterns"
    )
    
    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white"),
        margin=dict(t=60, l=10, r=10, b=10)
    )
    
    return fig

def budget_sunburst(transactions: pd.DataFrame, budget: Dict[str, float]) -> Any:
    """
    Create an interactive sunburst chart of budget vs actual
    """
    category_totals = transactions.groupby('category')['amount'].sum().reset_index()
    category_totals['status'] = category_totals.apply(
        lambda x: 'Over' if x['amount'] > budget.get(x['category'], 0) else 'Under',
        axis=1
    )
    
    # Calculate percentage variance
    category_totals['variance'] = category_totals.apply(
        lambda x: (x['amount'] - budget.get(x['category'], 0)) / budget.get(x['category'], 1) * 100,
        axis=1
    )
    
    fig = px.sunburst(
        category_totals,
        path=['status', 'category'],
        values='amount',
        color='variance',
        color_continuous_scale='RdBu',
        color_continuous_midpoint=0,
        title="Budget Variance Analysis"
    )
    
    fig.update_layout(
        paper_bgcolor="#0E1117",
        font=dict(color="white"),
        margin=dict(t=40, b=10, l=10, r=10),
        coloraxis_colorbar=dict(
            title="Variance %",
            tickvals=[-100, 0, 100],
            ticktext=["Under", "On Budget", "Over"]
        )
    )
    
    return fig