import dash
from dash import html
from dash import dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import researchpy as rp

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

card_country = dbc.Card(
    [
        dbc.CardHeader('Country of Survey  : '),
        dbc.CardBody(
            [
                html.P('USA')
            ]
        )
    ], color='#DEDEDE',
)

card_population = dbc.Card(
    [
        dbc.CardHeader('Total Population  : '),
        dbc.CardBody(
            [
                html.P('328.2 Million')
            ]
        )
    ], color='#DEDEDE',
)

card_percentage = dbc.Card(
    [
        dbc.CardHeader('Anti-Vaxxers percentage: '),
        dbc.CardBody(
            [
                html.P('18.9 %')
            ]
        )
    ], color='#DEDEDE',
)

card_infections= dbc.Card(
    [
        dbc.CardHeader('Tot Infections : '),
        dbc.CardBody(
            [
                html.P('43.2 M')
            ]
        )
    ], color='#DEDEDE',
)

card_deaths = dbc.Card(
    [
        dbc.CardHeader('Tot Deaths : '),
        dbc.CardBody(
            [
                html.P('693 K')
            ]
        )
    ], color='#DEDEDE',
)

card_states = dbc.Card(
    [
        dbc.CardHeader('Tot States  : '),
        dbc.CardBody(
            [
                html.P('41 States')
            ]
        )
    ], color='#DEDEDE',
)



info_cards = dbc.CardDeck(
    [
        dbc.Col(card_country, width='auto'),
        dbc.Col(card_population, width='auto'),
        dbc.Col(card_infections, width='auto'),
        dbc.Col(card_deaths, width='auto'),
        dbc.Col(card_states, width='auto'),
        dbc.Col(card_percentage, width='auto')
    ],
)
# working with the data
df = pd.read_csv('/Users/RyanMburu/Documents/DS-Projects/Module-I/Group Project/THE-FACTORS-DETERMINING-COVID-19-VACCINE-ACCEPTANCE/datasets/covid_main.csv')

demographic_list = list(df)

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label('Which demographic of Americans do you want to see?'),
                dcc.Dropdown(
                    id='demographic_dropdown',
                    #set the options after loading dataframe
                    options=[{'label':i, 'value':i} for i in demographic_list],
                    value='Gender',
                ),
            ]
        )
    ], body=True
)

piechart_dropdown = dbc.Card(
    [
        html.Div(
            [
                dbc.Label('What Demographic of Anti-Vaxxers would you like to see ? : '),
                dcc.Dropdown(
                    id='antivax_piechart',
                    options=[{'label':i, 'value':i} for i in demographic_list],
                    value='Age',
                ),
            ]
        )
    ], body=True
)

app.layout = dbc.Container(
    [
        html.H1('COVID ACCEPTANCE IN THE US'),
        html.Hr(),
        dbc.Row(
            [
                html.Div([info_cards])

            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=3, width='auto'),
                dbc.Col(dcc.Graph(id='bar graphs of demographics'), width='auto'),
                html.Hr(),         
            ], 
            align='Center',
        ),
        html.Hr(),
        dbc.Row([
            dbc.Col(dcc.Graph(id='antivax_piechart'), width=5),
            dbc.Col(dcc.Graph(id='vaxxers_piechart'), md=5),
            ])  
    ],
    fluid=True
)

@app.callback(
    Output('bar graphs of demographics', 'figure'),
    Input('demographic_dropdown', 'value')
)

def bar_percentage(column):
    df_one = df.groupby([column, 'Willingness to take vaccine']).size().reset_index()
    df_one['Percentage']=df.groupby([column, 'Willingness to take vaccine']).size().groupby(level=0).apply(lambda x:100 * x/float(x.sum())).values
    df_one = df_one.drop(0, axis=1)
    plot = px.bar(df_one, x=column, y='Percentage', color='Willingness to take vaccine', barmode='stack')
    return plot


@app.callback(
    Output('antivax_piechart', 'figure'),
    Input('demographic_dropdown', 'value')
)

def bar_pie(column):
    df_two = df.groupby([column, 'Willingness to take vaccine']).size().reset_index()
    df_two['Percentage']=df.groupby([column, 'Willingness to take vaccine']).size().groupby(level=0).apply(lambda x:100 * x/float(x.sum())).values
    df_two = df_two.drop(0, axis=1)
    df_antivax = df_two[df_two['Willingness to take vaccine'] == 'no']
    plot = px.pie(df_antivax, values='Percentage', names=column, labels=column, title=f'Percentages of Antivaxxers per {column} ')
    return plot


@app.callback(
    Output('vaxxers_piechart', 'figure'),
    Input('demographic_dropdown', 'value')
)

def bar_pie(column):
    df_two = df.groupby([column, 'Willingness to take vaccine']).size().reset_index()
    df_two['Percentage']=df.groupby([column, 'Willingness to take vaccine']).size().groupby(level=0).apply(lambda x:100 * x/float(x.sum())).values
    df_two = df_two.drop(0, axis=1)
    df_antivax = df_two[df_two['Willingness to take vaccine'] == 'yes']
    plot = px.pie(df_antivax, values='Percentage', names=column, labels=column, title=f'Percentages of Pro-Vaxxers per {column} ')
    return plot



if __name__ == '__main__':
    app.run_server(debug=True)



