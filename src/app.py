import json
import base64
from io import BytesIO

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

import components
import utils


NUMTOPGROUP = 5
NUMCASUALITIES = 30
MEANLESSLIST = [
    "is ", "are", "was", "were", "a ", "an ", "the",
    "Is ", "Are", "Was", "Were", "A ", "An ", "The",
    "in ", "at ", "on ", "of ", "for ", "to ",
    "In ", "At ", "On ", "Of ", "For ", "To ",
    ":", ","
]

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
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 

main_col_1_layout = [
    html.Div(
        children=[
            dcc.Graph(id='global_map'),
            # components.markdown("summary", "test", component_theme)
        ]
    ),
    components.range_slider('year_slider', df['iyear'], component_theme),
    html.Div(
        id='buttom_row',
        style={
            'margin-top': 20,
            "position": "relative",
        },
        children=[
            html.Div(
                id='trending_line_container',
                children=[
                    dcc.Graph(
                        id='trending_line',
                        config={ 'displayModeBar': False }
                    )
                ],
                style={
                    'display': 'inline-block', 
                    'width': '91%',
                    'background-color': component_theme['bg_color'],

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
                style={
                    'display': 'inline-block', 
                    'width': '9%',
                },
            ),
            dcc.RadioItems(
                id='trending_line_radio',
                options=[
                    {'label': 'Attacks', 'value': ''},
                    {'label': 'Casualties', 'value': 'Casualties'},
                ],
                value='',
                labelStyle={'display': 'inline-block'},
                style={
                    # 'display': 'inline_block',
                    "position": "absolute",
                    "left": "0px",
                    "top": "180px",
                    "width": "100%",
                    'background-color': component_theme['bg_color'], 
                    'color': component_theme['text_color'],
                }
            ),
        ]
    )
]

main_col_2_layout = [
    html.Div(
        id='summary_container',
        children=[
            components.summary_window("summary", "test", component_theme),
            components.word_cloud("word_cloud_image", component_theme),
        ],
    ),
    html.Div(
        id='selected_attacks_bar_container',
        children=dcc.Graph(
            id='selected_attacks_bar',
            config={ 'displayModeBar': False }
        ),
        style={
            "margin-top": "20px",    # ?????
        }
    ),
]

app.layout = html.Div(
    id="app",
    style={
        'background-color': 'black',
        'color': 'white',
    },
    children=[
        html.Div(
            className="row",
            style={
                "height": "100%",
            },
            children=[
                html.Div(
                    id="main_col_1",
                    className="nine columns",
                    children=main_col_1_layout,
                    style={
                        'display': 'inline-block',
                        'margin-top': 10,
                        'margin-right': 10,
                        'margin-buttom': 10,
                        'margin-left': 10,
                    }
                ),
                html.Div(
                    id="main_col_2",
                    className="three columns",
                    children=main_col_2_layout,
                    style={
                        "height": "100%",
                        'display': 'inline-block', 
                        'margin-top': 4,
                        'margin-right': 10,
                        'margin-buttom': 10,
                        'margin-left': 10,
                    }
                ),
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
        ),
        html.Div(
            id='state_selection_record', 
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
        Input('state_top_group', 'children'),
        Input('state_selection_record', 'children'),
        Input('trending_line_radio', 'value'),
    ],
)
def update_trending_line(json_df, json_top_group, json_selection_record, isCasualty):
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

    year_sum_df = year_sum_df.reset_index()

    if isCasualty:
        y_label = "Casualities"
    else:
        y_label = "Number of Attacks"

    if json_selection_record is None:
        return utils.get_trending_line(year_sum_df, y_label, component_theme)
    else:
        selection_record = json.loads(json_selection_record)["record"]
        return utils.get_trending_line(
            year_sum_df, 
            y_label, 
            component_theme,
            selection_record=selection_record,
            top_group_list=top_group['gname'] 
        )

@app.callback(
    Output('horizontal_bar', 'figure'),
    [
        Input('state_top_group', 'children'),
        Input('state_selection_record', 'children')
    ],
)
def update_horizontal_bar(json_top_group, json_selection_record):
    top_group = pd.read_json(json_top_group, orient='split')

    if json_selection_record is None:
        return utils.get_horizontal_bar(top_group, component_theme)
    else:
        selection_record = json.loads(json_selection_record)["record"]
        return utils.get_horizontal_bar(
            top_group,
            component_theme,
            selection_record=selection_record,
        )

@app.callback(
    Output('group_summary', 'children'),
    [
        Input('global_map', 'hoverData'),
    ]
)
def show_summary(hover_data):
    if hover_data:
        group_name = hover_data['points'][0]["hovertext"] + ":\n\n"
        summary = hover_data['points'][0]['customdata'][0]
        summary = summary.replace(": ", ":\n")
        summary = summary.replace(". ", ".\n")
        return [group_name, summary]
    else:
        return ""

@app.callback(
    Output('state_selection_record', 'children'),
    [
        Input('global_map', 'restyleData'),
    ],
    State('state_selection_record', 'children'),
)
def update_seleted_groups_in_legend(selected_group, json_selection_record):
    if selected_group is None:
        return
    if json_selection_record:
        selection_record = json.loads(json_selection_record)["record"]
    else:
        selection_record = [True]*NUMTOPGROUP
    selection_record[selected_group[1][0]] = selected_group[0]['visible'][0]

    return json.dumps({ "record": selection_record })

@app.callback(
    Output('selected_attacks_bar', 'figure'),
    [
        Input('state_top_group_df', 'children'),
        Input('global_map', 'clickData'),
        Input('global_map', 'selectedData'),
    ],
)
def update_seleted_attacks_bar(json_df, click_data, selected_data):
    # blank df
    df_selected = pd.DataFrame(
        { "region_txt": [""], "nkillwound": [0] }
    )
    point_data = [[], []]

    for points in [click_data, selected_data]:
        if points and points['points']:
            for point in points['points']:
                point_data[0].append(point['customdata'][1])
                point_data[1].append(point['customdata'][2])

            df_selected = df_selected.append(
                pd.DataFrame(
                    {
                        "region_txt": point_data[0],
                        "nkillwound": point_data[1],
                    }
                ),
                ignore_index=True
            )
            point_data = [[], []]

    df_selected = df_selected.groupby(['region_txt']).count()
    df_selected["region_txt"] = df_selected.index
    df_selected = df_selected.rename(columns={"nkillwound": "attack_count"})

    df = pd.read_json(json_df, orient='split')
    df = df[['region_txt', 'nkillwound']].groupby(['region_txt']).count()
    df["region_txt"] = df.index
    df = df.rename(columns={"nkillwound": "attack_count"})

    df["selected_attack_count"] = [0]*df.index.shape[0]
    for idx in range(df_selected.index.shape[0]):
        count, region = df_selected.iloc[idx, :]
        df.iloc[(df.index == region), -1] = count

    return utils.selected_attacks_bar(
        df,
        component_theme, 
    )

@app.callback(
    Output('word_cloud_image', 'src'),
    [
        Input('word_cloud_image', 'id'),
        Input('global_map', 'hoverData'),
    ]
)
def update_word_cloud(id, hover_data):
    # https://stackoverflow.com/questions/58907867/how-to-show-wordcloud-image-on-dash-web-application
    img = BytesIO()

    if hover_data:
        summary = hover_data['points'][0]['customdata'][0]

        for meanless in MEANLESSLIST:
            summary = summary.replace(meanless, "")
    else:
        summary = "Please-Hover-on-Map"

    utils.make_word_cloud_image(summary).save(img, format='PNG')
    
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


if __name__ == '__main__':
    app.run_server(debug=True)