import base64

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from wordcloud import WordCloud


IRREGULAR_NUM = -99


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
            'nperps', 'attacktype1_txt', 'summary', 'region_txt'
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
    df['marker_size'] = 10*df['nkillwound'].pow(1./2)
    # df['ransomamt'] = df['ransomamt'].replace(IRREGULAR_NUM, 0)
    # df['ransompaid'] = df['ransompaid'].replace(IRREGULAR_NUM, 0)
    df = df.reset_index()

    return df

def get_map_fig(df, component_theme):
    # top10 = df['gname'].value_counts()[: 10]
    # top10 = pd.DataFrame(
    #     data=[[group, count] for group, count in zip(top10.index, top10.values)], columns=['Group', 'Count'])
    fig = px.scatter_geo(
        df, 
        lat=df['latitude'], 
        lon=df['longitude'],
        color=df['gname'],
        size=df['marker_size'],
        hover_name="gname",
        hover_data={
            'latitude': False,
            'longitude': False,
            'gname': False,
            'marker_size': False,
            'nkillwound': True,
            'country_txt': True,
            'weaptype1_txt': True,
            'attacktype1_txt': True,
        },
        labels={
            "gname": "Group Name",
            "nkillwound": "Casualities",
            "country_txt": "Country",
            "weaptype1_txt": "Weapon",
            "attacktype1_txt": "Attack Type",
        },
        custom_data=[
            "summary",
            "region_txt"
        ],
        scope="world",
        height=500,
        title=None
    )
    fig.update_layout(
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        plot_bgcolor=component_theme['bg_color'],
        paper_bgcolor=component_theme['bg_color'],
        font={ "color": component_theme["text_color"] },
        hoverlabel={
            'bgcolor': component_theme['bg_color']
        },
        legend={
            'title': "",
            'bgcolor': component_theme['legend_bg_color_half'],
            'traceorder': "normal",    
            'yanchor': "top",
            'y': 0.99,
            'xanchor': "left",
            'x': 0.01
        },
        geo={
            "showocean": True,
            "showcountries": True,
            "landcolor": 'rgb(128, 128, 128)',
            "oceancolor": 'rgb(0, 12, 51)',
            "countrycolor": "rgb(192, 192, 192)",
            "fitbounds": "locations"
        }
    )

    return fig

def get_trending_line(df, y_label, component_theme, **kwargs):
    fig = px.line(
        df,
        x='iyear',
        y='total', 
        color=df['gname'], 
        labels={
            'gname': 'Group',
            'iyear': 'Year',
            'total': y_label
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
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        plot_bgcolor=component_theme["legend_bg_color"],
        paper_bgcolor=component_theme["legend_bg_color"],
        font={"color": component_theme["text_color"]},
        showlegend=True,  
        hovermode="x",
        hoverlabel={'font_size': 12},
        legend={
            'title': "",
            'bgcolor': component_theme['legend_bg_color'],
            'yanchor': "top",
            'y': 0.99,
            'xanchor': "left",
            'x': 0.01
        }
    )

    if "selection_record" in kwargs.keys():
        group_list = kwargs["top_group_list"]
        hidden_group = []
        for idx, selection in enumerate(kwargs["selection_record"]):
            if selection == "legendonly":
                hidden_group.append(group_list[idx])
                
        fig.for_each_trace(
            lambda trace: trace.update(visible="legendonly") if trace.name in hidden_group else ()
        )

    return fig

def get_horizontal_bar(df, component_theme, **kwargs):
    fig = px.bar(
        df, 
        x=['nkill', 'nwound'], 
        y='gname',
        color=df['gname'],    # it will effect the order of bars, so I keep it.
        color_discrete_sequence=component_theme['bar']['colors'],    # Real colors for bars
        orientation='h', 
        height=200
    )
    fig.update_traces(hovertemplate='%{x}<extra></extra>')
    fig.update_xaxes(
        matches=None, 
        showgrid=False, 
        showticklabels=False, 
        visible=True, 
        title="K / W")
    fig.update_yaxes(matches=None, showticklabels=False, visible=False)
    fig.update_layout(
        margin={'l': 10, 'r': 0, 't': 0, 'b': 52},
        bargap=0.1,
        bargroupgap=0.1,
        plot_bgcolor=component_theme["bg_color"],
        paper_bgcolor=component_theme["bg_color"],
        font={
            "size": 12,
            "color": component_theme["text_color"]
        },
        showlegend=False
    )

    if "selection_record" in kwargs.keys():
        group_list = df['gname']
        hidden_group = []
        for idx, selection in enumerate(kwargs["selection_record"]):
            if selection == "legendonly":
                hidden_group.append(group_list[idx])
                
        fig.for_each_trace(
            lambda trace: trace.update(visible="legendonly") if trace.name in hidden_group else ()
        )

    return fig

def selected_attacks_bar(df, component_theme):
    fig = px.bar(
        df, 
        x="region_txt", 
        y="attack_count",
        color="region_txt",
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        log_y=True,
        barmode='overlay',
        height=253
    )
    # fig.add_trace(
    #     px.bar(
    #         df, 
    #         x="region_txt", 
    #         y="selected_attack_count",
    #         color="region_txt",
    #         color_discrete_sequence=px.colors.qualitative.Set1,
    #         barmode='overlay',
    #         width=11
    #     ).data[0]
    # )
    fig.add_bar(
        x=df["region_txt"],
        y=df["selected_attack_count"],
        base='overlay',
        hovertext="",
        # color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig.update_traces(
        # selectedpoints=selectedpoints, 
        # mode='markers',
        # marker={ 'color': '#0066ff' },
        hovertemplate='%{y}<extra></extra>',
    )
    fig.update_xaxes(
        title="", 
        zeroline=False,
        # tickangle=-45,
        # tickfont={
        #     "size": 10
        # },
        showticklabels=False, 
        showgrid=False,
        showline=True,
        linewidth=1, 
        linecolor='white',
        visible=True, 
        matches=None
    )
    fig.update_yaxes(
        title="Number of Attacks (log)", 
        zeroline=False,
        showticklabels=False,  
        showgrid=False,
        showline=True,
        linewidth=1, 
        linecolor='white',
        visible=True, 
    )
    fig.update_layout(
        margin={'l': 0, 'r': 30, 't': 20, 'b': 40},
        plot_bgcolor=component_theme["bg_color"],
        paper_bgcolor=component_theme["bg_color"],
        font={"color": component_theme["text_color"]},
        hovermode="x",
        # hoverlabel={'font_size': 6},
        showlegend=False,  
    )

    return fig

def make_word_cloud_image(text):
    word_list = text.split()

    word_freq = []
    for w in word_list:
        word_freq.append(word_list.count(w))
    data = {word: times for word, times in zip(word_list, word_freq)}
    wc = WordCloud(background_color='black', width=268, height=268)
    wc.fit_words(data)

    return wc.to_image()