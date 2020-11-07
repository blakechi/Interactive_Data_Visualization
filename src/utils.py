import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def get_cleaned_dataset():
    df = pd.read_csv("data/globalterrorismdb_0718dist.csv", encoding='ISO-8859-1', low_memory=False)

    df = df[[
        'iyear', 'country_txt', 'gname', 'longitude', 'latitude', 
        'nkill', 'nwound', 'success', 'weaptype1_txt', 
        'nhostkid', 'nreleased', 'ransomamt', 'ransompaid', 
        'nperps']]
    df = df.loc[df['gname'] != "Unknown"]
    # consider evevts after 2000 only
    df = df.loc[df['iyear'] >= 2000]
    df = df.loc[~df['longitude'].isna()]
    df = df.loc[~df['latitude'].isna()]
    df = df.loc[~df['nkill'].isna()]
    df = df.loc[~df['nwound'].isna()]
    df['nkillwound'] = df['nkill'] + df['nwound']
    df = df.reset_index()

    return df

def get_map_fig(df):
    # top10 = df['gname'].value_counts()[: 10]
    # top10 = pd.DataFrame(
    #     data=[[group, count] for group, count in zip(top10.index, top10.values)], columns=['Group', 'Count'])
    fig = px.scatter_geo(
        df, lat=df['latitude'], lon=df['longitude'],
        color="gname",
        size=df["nkillwound"],
        hover_name="gname",
        hover_data={
            'latitude': False,
            'longitude': False,
            'gname': False,
            'weaptype1_txt': True
        },
        labels={
            "gname": "Group Name",
            "nkill": "Number of Kills",
            "nwound": "Number of Wounds",
            "size": "Number of Kills & Wounds",
            "weaptype1_txt": "Weapon"},
        projection="natural earth",
        scope="world",
        title=None)
    fig.update_layout(
        hoverlabel={
            'bgcolor': 'rgba(0, 0, 0, 0)'},
        legend={
            'bgcolor': 'rgba(0, 0, 0, 0)',
            'traceorder': "normal",    
            'yanchor': "top",
            'y': 0.99,
            'xanchor': "left",
            'x': 0.01})

    return fig

def get_trending_line(df):
    fig = px.line(
        df, x='iyear', y='total', 
        color='gname', 
        labels={
            'gname': 'Group Name',
            'iyear': 'Year',
            'total': 'Number of Kills & Wounds'},
        hover_data={
            'iyear': False},
        height=200)
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,  
        legend={
            'yanchor': "top",
            'y': 0.99,
            'xanchor': "left",
            'x': 0.01})

    return fig

def get_horizontal_bar(df):
    fig = go.Figure(
        go.Bar(
            x=df.values,
            y=df.index,
            color='lifeExp',
            orientation='h'))