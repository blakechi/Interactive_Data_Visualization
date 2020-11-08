import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def get_cleaned_dataset():
    df = pd.read_csv(
        "data/globalterrorismdb_0718dist.csv", 
        encoding='ISO-8859-1', 
        low_memory=False
    )
    df = df[
        [
            'iyear', 'country_txt', 'gname', 'longitude', 'latitude', 
            'nkill', 'nwound', 'success', 'weaptype1_txt', 
            'nhostkid', 'nreleased', 'ransomamt', 'ransompaid', 
            'nperps'
        ]
    ]
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
        df, 
        lat=df['latitude'], 
        lon=df['longitude'],
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
            "weaptype1_txt": "Weapon"
        },
        projection="natural earth",
        scope="world",
        title=None
    )
    fig.update_layout(
        hoverlabel={
            'bgcolor': 'rgba(0, 0, 0, 0)'
        },
        legend={
            'bgcolor': 'rgba(0, 0, 0, 0)',
            'traceorder': "normal",    
            'yanchor': "top",
            'y': 0.99,
            'xanchor': "left",
            'x': 0.01
        }
    )

    return fig

def get_trending_line(df, bg_color, text_color):
    fig = px.line(
        df, x='iyear', y='total', 
        color='gname', 
        labels={
            'gname': 'Group',
            'iyear': 'Year',
            'total': 'Kills + Wounds'
        },
        hover_data={
            'iyear': False
        },
        height=200
    )
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_xaxes(
        title="", 
        range=[df['iyear'].min(), df['iyear'].max()],
        showticklabels=True, 
        showgrid=False,
        visible=True, 
        matches=None
    )
    fig.update_yaxes(
        showgrid=False,
    )
    fig.update_layout(
        margin={'l': 0, 'r': 20, 't': 0, 'b': 0},
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font={"color": text_color},
        showlegend=True,  
        hovermode="x",
        hoverlabel={'font_size': 12},
        legend={
            'title': "",
            'yanchor': "top",
            'y': 0.99,
            'xanchor': "left",
            'x': 0.01
        }
    )

    return fig

def get_horizontal_bar(df, bg_color, text_color):
    fig = px.bar(
        df, 
        x=df['total'], 
        y=df['gname'],
        color=df['gname'], 
        hover_data={
            'gname': False
        },
        labels={
            'total': 'Total',
        },
        orientation='h', 
        height=200
    )
    fig.update_traces(hovertemplate='%{x}<extra></extra>')
    fig.update_xaxes(matches=None, showticklabels=False, visible=False)
    fig.update_yaxes(matches=None, showticklabels=False, visible=False)
    fig.update_layout(
        margin={'l': 0, 'r': 0, 't': 0, 'b': 55},
        bargap=0.1,
        bargroupgap=0.1,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font={"color": text_color},
        showlegend=False
    )

    return fig