import dash_core_components as dcc
import dash_html_components as html
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
            'background-color': component_theme['bg_color'], 
            'color': component_theme['text_color']
        }
    )
    return 

def summary_window(id, text, component_theme):
    return html.Div(
        id=id,
        children=[
            html.H5(
                children=["Summary"],
                style={
                    "margin-left": "5px",
                }),
            html.Pre(
                id='group_summary', 
                style={
                    "height": "150px",
                    "border": f"5px solid {component_theme['bg_color']}",
                    'background-color': "black", 
                    'color': component_theme['text_color'],
                    'overflowX': 'auto',
                    'overflowY': 'scroll',
                }
            ),
        ],
        style={
            'background-color': component_theme['bg_color'], 
            'color': component_theme['text_color']
        }
    )

def word_cloud(id, component_theme):
    return html.Div(
        children=[
            html.Img(
                id=id,
                style={
                    'background-color': component_theme['bg_color'], 
                    'color': component_theme['text_color']
                }
            )
        ],
        style={
            "padding": "0",
            "border": f"5px solid {component_theme['bg_color']}",
            'background-color': component_theme['bg_color'], 
            'color': component_theme['text_color']
        }
    )