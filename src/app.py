import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

import components
import utils


df = utils.get_cleaned_dataset()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[external_stylesheets])
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets])
app.layout = html.Div([
    # dbc.NavbarSimple(
    #     children=[
    #         dbc.NavItem(dbc.NavLink("Page 1", href="#")),
    #         dbc.DropdownMenu(
    #             children=[
    #                 dbc.DropdownMenuItem("More pages", header=True),
    #                 dbc.DropdownMenuItem("Page 2", href="#"),
    #                 dbc.DropdownMenuItem("Page 3", href="#"),
    #             ],
    #             nav=True,
    #             in_navbar=True,
    #             label="More",
    #         ),
    #     ],
    #     brand="NavbarSimple",
    #     brand_href="#",
    #     color="primary",
    #     dark=True,
    #     style={'left': 0, 'top': 0, "bottom": 0}
    # ),
    
    # html.Div([
    #     html.Div([
    #         dcc.Dropdown(
    #             id='crossfilter-xaxis-column',
    #             options=[{'label': i, 'value': i} for i in available_indicators],
    #             value='Fertility rate, total (births per woman)'
    #         ),
    #         dcc.RadioItems(
    #             id='crossfilter-xaxis-type',
    #             options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
    #             value='Linear',
    #             labelStyle={'display': 'inline-block'}
    #         )
    #     ],
    #     style={'width': '49%', 'display': 'inline-block'}),

    #     html.Div([
    #         dcc.Dropdown(
    #             id='crossfilter-yaxis-column',
    #             options=[{'label': i, 'value': i} for i in available_indicators],
    #             value='Life expectancy at birth, total (years)'
    #         ),
    #         dcc.RadioItems(
    #             id='crossfilter-yaxis-type',
    #             options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
    #             value='Linear',
    #             labelStyle={'display': 'inline-block'}
    #         )
    #     ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    # ], style={
    #     'borderBottom': 'thin lightgrey solid',
    #     'backgroundColor': 'rgb(250, 250, 250)',
    #     'padding': '10px 5px'
    # }),

    # html.Div([
    #     dcc.Graph(
    #         id='crossfilter-indicator-scatter',
    #         hoverData={'points': [{'customdata': 'Japan'}]}
    #     )
    # ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    # html.Div([
    #     dcc.Graph(id='x-time-series'),
    #     dcc.Graph(id='y-time-series'),
    # ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(
        dcc.Graph(id='global-map'),
        style={'width': '79%', 'display': 'inline-block', 'padding': '0 0 0 0'}),
    html.Div(
        components.range_slider('year-slider', df['iyear']),
        style={'width': '79%', 'padding': '0 0 0 0'}),
    html.Div([
        dcc.Graph(id='trending-line'),
        # dcc.Graph(id='horizontal_bar'),
    ], style={'display': 'inline-block', 'width': '59%', 'height': '15%', 'padding': '0, 0, 0, 0'}),
    # html.Div([
    #     dcc.Graph(id='horizontal_bar'),
    # ], style={'display': 'inline-block', 'width': '39%'}),
    html.Div(id='state-top_10_df', style={'display': 'none'}),
    html.Div(id='state-top_10', style={'display': 'none'})
])


# @app.callback(
#     dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
#     [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
#      dash.dependencies.Input('crossfilter-year--slider', 'value')])
# def update_graph(xaxis_column_name, yaxis_column_name,
#                  xaxis_type, yaxis_type,
#                  year_value):
#     dff = df[df['Year'] == year_value]

#     fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
#             y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
#             hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name']
#             )

#     fig.update_traces(customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

#     fig.update_xaxes(title=xaxis_column_name, type='linear' if xaxis_type == 'Linear' else 'log')

#     fig.update_yaxes(title=yaxis_column_name, type='linear' if yaxis_type == 'Linear' else 'log')

#     fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

#     return fig


# def create_time_series(dff, axis_type, title):

#     fig = px.scatter(dff, x='Year', y='Value')

#     fig.update_traces(mode='lines+markers')

#     fig.update_xaxes(showgrid=False)

#     fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

#     fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
#                        xref='paper', yref='paper', showarrow=False, align='left',
#                        bgcolor='rgba(255, 255, 255, 0.5)', text=title)

#     fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

#     return fig


# @app.callback(
#     dash.dependencies.Output('x-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
#      dash.dependencies.Input('crossfilter-year--slider', 'value')])
# def update_y_timeseries(hoverData, xaxis_column_name, axis_type, year_value):
#     dff = df[df['Year'] <= year_value]
#     country_name = hoverData['points'][0]['customdata']
#     dff = dff[dff['Country Name'] == country_name]
#     dff = dff[dff['Indicator Name'] == xaxis_column_name]
#     title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
#     return create_time_series(dff, axis_type, title)


# @app.callback(
#     dash.dependencies.Output('y-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
#      dash.dependencies.Input('crossfilter-year--slider', 'value')])
# def update_x_timeseries(hoverData, yaxis_column_name, axis_type, year_value):
#     dff = df[df['Year'] <= year_value]
#     dff = dff[dff['Country Name'] == hoverData['points'][0]['customdata']]
#     dff = dff[dff['Indicator Name'] == yaxis_column_name]
#     return create_time_series(dff, axis_type, yaxis_column_name)

@app.callback(
    [Output('state-top_10_df', 'children'),
     Output('state-top_10', 'children')],
    [Input('year-slider', 'value')])
def update_state(year):
    df_ = df.loc[year[0] <= df['iyear']]
    df_ = df_.loc[df_['iyear'] <= year[1]]
    top_10 = df_['gname'].value_counts()[: 4]
    df_ = df_[df_['gname'].isin(top_10.index)]

    return [
        df_.to_json(date_format='iso', orient='split'), 
        top_10.to_json(date_format='iso', orient='index')]

@app.callback(
    Output('global-map', 'figure'),
    [Input('state-top_10_df', 'children')])
def update_global_map(json_df):
    df = pd.read_json(json_df, orient='split')

    return utils.get_map_fig(df)

@app.callback(
    Output('trending-line', 'figure'),
    [Input('state-top_10_df', 'children'),
     Input('state-top_10', 'children')])
def update_trending_line(json_df, json_top_10):
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
    return utils.get_trending_line(year_sum_df)

# @app.callback(
#     Output('global-map', 'figure'),
#     [State('state-top_10_total', 'children')])
# def update_horizontal_bar(top_10):
#     return utils.get_horizontal_bar(top_10)


if __name__ == '__main__':
    app.run_server(debug=True)