import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd


def range_slider(id, data, mark_color):
    return dcc.RangeSlider(
        id=id,
        min=data.min(),
        max=data.max(),
        value=[data.min(), data.max()],
        marks={ 
            str(year): {
                "label": str(year), 
                "style": {"color": mark_color}
            } for year in zip(data.unique(), [mark_color]*len(data.unique())) 
        },
        step=None
    )

