import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

import components
import utils


df = utils.get_cleaned_dataset()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[external_stylesheets])
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets])
app.layout = html.Div(
    id="app",
    style={'background-color': 'white', 'color': 'black'},
    children=[
        # html.Div(
        #     dcc.Graph(id='global_map'),
        #     style={'width': '79%', 'display': 'inline-block', 'padding': '0 0 0 0'}),
        html.Div(
            id="light_dark_mode",
            children=[
                daq.ToggleSwitch(
                    id='light_dark_toggle',
                    label=['Light', 'Dark'],
                    style={'width': '5%', 'margin': 'auto'}, 
                    value=False
                )
            ]
        ),
        html.Div(
            id="year_slider_container",
            children=components.range_slider('year_slider', df['iyear'], "black"),
            style={'width': '74%', 'padding': '0 0 0 0'}
        ),
        html.Div(
            children=[
                html.Div(
                    id='trending_line_container',
                    children=[
                        dcc.Graph(
                            id='trending_line',
                            config={ 'displayModeBar': False }
                        )
                    ],
                    className='column',
                    style={
                        'display': 'inline-block', 
                        'width': '74%', 
                        'height': '10%', 
                        'padding': '0, 0, 0, 0',
                        "background-color": "black",
                        "color": "white"
                    }
                ),
                html.Div(
                    id='bar_container',
                    children=[
                        dcc.Graph(
                            id='horizontal_bar',
                            config={ 'displayModeBar': False }
                        )
                    ], 
                    className='column',
                    style={
                        'display': 'inline-block', 
                        'width': '5%', 
                        'height': '10%', 
                        'padding': '0, 0, 0, 0',
                    },
                ),
            ],
            id='row_1',
            className='row',
        ),
        html.Div(
            id='state_top_10_df', 
            style={ 'display': 'none' }
        ),
        html.Div(
            id='state_top_10', 
            style={ 'display': 'none' }
        )
    ]
)

@app.callback(
    [
        Output('app', 'style'),
        Output('light_dark_mode', 'style'),
        Output('year_slider_container', 'style'),
        Output('year_slider', 'children'),
    ],
    [
        Input('light_dark_toggle', 'value')
    ]
)
def change_background(dark_theme):
    if(dark_theme):
        return [
            {'background-color': 'black', 'color': 'white'},
            {'background-color': 'black', 'color': 'white'},
            {'background-color': 'black', 'color': 'white', 'width': '74%', 'padding': '0 0 0 0'},
            components.range_slider('year_slider', df['iyear'], "white")
        ]
    else:
        return [
            {'background-color': 'white', 'color': 'black'},
            {'background-color': 'white', 'color': 'black'},
            {'background-color': 'white', 'color': 'black', 'width': '74%', 'padding': '0 0 0 0'},
            components.range_slider('year_slider', df['iyear'], "black")    
        ]

@app.callback(
    [Output('state_top_10_df', 'children'),
     Output('state_top_10', 'children')],
    [Input('year_slider', 'value')])
def update_state(year):
    df_ = df.loc[year[0] <= df['iyear']]
    df_ = df_.loc[df_['iyear'] <= year[1]]
    top_10 = df_['gname'].value_counts()[: 4]
    df_ = df_[df_['gname'].isin(top_10.index)]

    return [
        df_.to_json(date_format='iso', orient='split'), 
        top_10.to_json(date_format='iso', orient='index')]

# @app.callback(
#     Output('global_map', 'figure'),
#     [Input('state_top_10_df', 'children')])
# def update_global_map(json_df):
#     df = pd.read_json(json_df, orient='split')
    #   df = df[df['nkillwound'] > 0]
#     return utils.get_map_fig(df)

@app.callback(
    Output('trending_line', 'figure'),
    [Input('state_top_10_df', 'children'),
     Input('state_top_10', 'children'),
     Input('light_dark_toggle', 'value')])
def update_trending_line(json_df, json_top_10, dark_theme):
    df = pd.read_json(json_df, orient='split')
    top_10 = pd.read_json(json_top_10, orient='index')
    top_10 = top_10.rename(columns={0: "total"})

    year_sum_df = pd.DataFrame([])
    year_min = df['iyear'].min()
    year_max = df['iyear'].max()
    x_axis = [year for year in range(year_min, year_max + 1)]
    for group in top_10.index:
        group_data = df[df['gname'] == group]
        year_count = group_data['iyear'].value_counts()
        
        for year in x_axis:
            if not year in year_count.index:
                year_count = year_count.append(pd.Series([0], index=[year]))
        tmp = pd.DataFrame({
             'gname': [group for i in range(year_count.shape[0])], 
             'iyear': year_count.index, 
             'total': year_count.values})
        tmp = tmp.sort_values(by=['iyear'])
        year_sum_df = pd.concat([year_sum_df, tmp])

    if dark_theme:
        return utils.get_trending_line(year_sum_df, "black", "white")
    else:
        return utils.get_trending_line(year_sum_df, "white", "black")


@app.callback(
    Output('horizontal_bar', 'figure'),
    [Input('state_top_10', 'children'),
     Input('light_dark_toggle', 'value')])
def update_horizontal_bar(json_top_10, dark_theme):
    top_10 = pd.read_json(json_top_10, orient='index')
    top_10 = top_10.rename(columns={0: "total"})
    top_10['gname'] = top_10.index

    if dark_theme:
        return utils.get_horizontal_bar(top_10, "black", "white")
    else:
        return utils.get_horizontal_bar(top_10, "white", "black")


if __name__ == '__main__':
    app.run_server(debug=True)