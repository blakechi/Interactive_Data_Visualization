import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd


def range_slider(id, data: pd.Series):
    return dcc.RangeSlider(
        id=id,
        min=data.min(),
        max=data.max(),
        value=[data.min(), data.max()],
        marks={str(year): str(year) for year in data.unique()},
        step=None)

