import plotly.express as px


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


def bar_chart(
    data, x, y, title="", color=None, barmode="group", color_discrete_sequence=None
):
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
