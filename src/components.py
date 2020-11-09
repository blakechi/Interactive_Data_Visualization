import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd


def range_slider(id, data, component_theme):
    return html.Div(
        id="year_slider_container",
        children=dcc.RangeSlider(
            id=id,
            min=data.min(),
            max=data.max(),
            value=[data.min(), data.max()],
            marks={ 
                str(year): {
                    "label": str(year), 
                    "style": {"color": component_theme['text_color']}
                } for year in data.unique()
            },
            step=None
        ),
        style={
            'width': '79%', 
            'padding': "0px 0px 0px 0px", 
            'margin-left': 10,
            'margin-right': 10,
            'background-color': component_theme['bg_color'], 
            'color': component_theme['text_color']
        }
    )
    return 

def markdown(id, text, component_theme):
    return dcc.Markdown(
        id=id,
        children=text,
        style={
            'display': 'inline-block', 
            'width': '29%', 
            'padding': "0px 0px 0px 0px", 
            'margin-left': 10,
            'margin-right': 10,
            'background-color': component_theme['bg_color'], 
            'color': component_theme['text_color']
        }
    )

