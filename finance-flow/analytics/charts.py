import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def pie_chart(data, names, values, title="", color_discrete_sequence=None):
    fig = px.pie(
        data,
        names=names,
        values=values,
        title=title,
        color_discrete_sequence=color_discrete_sequence or px.colors.qualitative.Set3,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20))
    return fig


def bar_chart(data, x, y, title="", color=None, barmode="group", color_discrete_sequence=None):
    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        barmode=barmode,
        color_discrete_sequence=color_discrete_sequence or px.colors.qualitative.Set3,
    )
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20))
    return fig


def line_chart(data, x, y, title="", color=None):
    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        color=color,
        markers=True,
    )
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20))
    return fig


def comparison_chart(data, x, y_actual, y_budget, title=""):
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Actual", x=data[x], y=data[y_actual], marker_color="#4CAF50"))
    fig.add_trace(go.Bar(name="Budget", x=data[x], y=data[y_budget], marker_color="#FF9800"))
    fig.update_layout(
        title=title,
        barmode="group",
        margin=dict(t=40, b=20, l=20, r=20),
    )
    return fig


def progress_chart(percentage, category=""):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": f"{category} Budget Usage"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#4CAF50" if percentage < 80 else "#FF9800" if percentage < 100 else "#F44336"},
            "steps": [
                {"range": [0, 80], "color": "#E8F5E9"},
                {"range": [80, 100], "color": "#FFF3E0"},
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 100,
            },
        },
    ))
    fig.update_layout(margin=dict(t=40, b=20, l=20, r=20))
    return fig
