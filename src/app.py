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


NUMTOPGROUP = 5
NUMCASUALITIES = 30

df = utils.get_cleaned_dataset()

component_theme = {
    "bg_color": "rgba(64, 64, 64, 255)",
    "legend_bg_color": "rgba(64, 64, 64, 0)",
    "text_color": "white",
    "bar": {
        "colors": [
            ['#636EFA', '#b5bafd'],
            ['#EF553B', '#f9c2b8'],
            ['#00CC96', '#b3ffeb'],
            ['#AB63FA', '#d8b5fd'],
            ['#FFA15A', '#ffd4b3']
        ]
    }
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__, 
    external_stylesheets=[external_stylesheets],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets])

main_col_1_layout = [
    html.Div(
        dcc.Graph(id='global_map'),
        style={
            'width': '79%', 
            'display': 'inline-block', 
            'padding': '10px 10px 6px 10px',
        }
    ),
    components.range_slider('year_slider', df['iyear'], component_theme),
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
                    'padding': "10px 0px 10px 10px",
                    'width': '74%', 
                    'height': '10%', 
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
                    'padding': "10px 10px 10px 0px",
                    'width': '5%', 
                    'height': '10%', 
                },
            ),
        ],
        id='buttom_row',
        className='row'
    )
]

main_col_2_layout = [
    components.markdown("summary", "", component_theme),
]

app.layout = html.Div(
    id="app",
    style={
        'background-color': 'black',
        'color': 'white',
        'padding': '0px'},
    children=[
        html.Div(
            id="main_row",
            className="row",
            children=[
                html.Div(
                    id="main_col_1",
                    className="column",
                    children=main_col_1_layout
                ),
                html.Div(
                    id="main_col_2",
                    className="column",
                    children=main_col_2_layout
                )
            ]
        ),
        html.Br(),
        html.Div(
            id='state_top_group_df', 
            style={ 'display': 'none' }
        ),
        html.Div(
            id='state_top_group_list', 
            style={ 'display': 'none' }
        ),
        html.Div(
            id='state_top_group', 
            style={ 'display': 'none' }
        )
    ]
)

@app.callback(
    [
        Output('state_top_group_df', 'children'),
        Output('state_top_group_list', 'children'),
        Output('state_top_group', 'children')
    ],
    [
        Input('year_slider', 'value')
    ]
)
def update_state(year):
    df_ = df.loc[(year[0] <= df['iyear'])]
    df_ = df_.loc[(df_['iyear'] <= year[1])]
    top_group = df_[['gname', 'nkillwound']].groupby(by='gname').sum().sort_values(by=['nkillwound'], ascending=False)[: NUMTOPGROUP]
    top_group_list = top_group.index
    df_ = df_[df_['gname'].isin(top_group_list)]
    sortIdx = dict(zip(top_group_list, range(len(top_group_list))))
    df_['top_group_idx'] = df_['gname'].map(sortIdx)
    top_group = pd.DataFrame(
        data={
            "gname": top_group_list,
            "total": top_group['nkillwound'],
        }
    )

    nkill = []
    nwound = []
    for i in range(NUMTOPGROUP):
        group_data = df_.loc[df_['gname'] == top_group_list[i]]
        nkill.append(group_data['nkill'].sum())
        nwound.append(group_data['nwound'].sum())

    top_group['nkill'] = nkill
    top_group['nwound'] = nwound

    return [
        df_.to_json(date_format='iso', orient='split'), 
        json.dumps({ 'top_gname': list(top_group_list) }, indent=4),
        top_group.to_json(date_format='iso', orient='split')
    ]

@app.callback(
    Output('global_map', 'figure'),
    [Input('state_top_group_df', 'children')])
def update_global_map(json_df):
    df = pd.read_json(json_df, orient='split')
    df = df[df['nkillwound'] > NUMCASUALITIES]
    df = df.sort_values(by = 'top_group_idx') 

    return utils.get_map_fig(df, component_theme)

@app.callback(
    Output('trending_line', 'figure'),
    [
        Input('state_top_group_df', 'children'),
        Input('state_top_group', 'children')
    ]
)
def update_trending_line(json_df, json_top_group, isCasualty=True):
    df = pd.read_json(json_df, orient='split')
    top_group = pd.read_json(json_top_group, orient='split')

    year_sum_df = pd.DataFrame([])
    year_min = df['iyear'].min()
    year_max = df['iyear'].max()
    x_axis = [year for year in range(year_min, year_max + 1)]
    for group in top_group['gname']:
        group_data = df[df['gname'] == group]
        if isCasualty:
            year_count = group_data[['iyear', 'nkillwound']].groupby(['iyear']).sum()
            year_count = pd.Series(year_count['nkillwound'], index=year_count.index)
        else:    # Number of Attacks
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

    if isCasualty:
        y_label = "Casualities"
    else:
        y_label = "Number of Attacks"

    return utils.get_trending_line(year_sum_df, y_label, component_theme)

@app.callback(
    Output('horizontal_bar', 'figure'),
    [
        Input('state_top_group', 'children')
    ]
)
def update_horizontal_bar(json_top_group):
    top_group = pd.read_json(json_top_group, orient='split')

    return utils.get_horizontal_bar(top_group, component_theme)

if __name__ == '__main__':
    app.run_server(debug=True)