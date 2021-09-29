import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

card_country = dbc.Card(
    [
        dbc.CardHeader('Country of Survey  : '),
        dbc.CardBody(
            [
                html.P('USA')
            ]
        )
    ]
)

card_population = dbc.Card(
    [
        dbc.CardHeader('Total Population  : '),
        dbc.CardBody(
            [
                html.P('328.2 Million')
            ]
        )
    ]
)

card_percentage = dbc.Card(
    [
        dbc.CardHeader('Pro-Vaxxers percentage: '),
        dbc.CardBody(
            [
                html.P('81.9 %')
            ]
        )
    ]
)

card_infections= dbc.Card(
    [
        dbc.CardHeader('Tot Infections : '),
        dbc.CardBody(
            [
                html.P('43.2 M')
            ]
        )
    ]
)

card_deaths = dbc.Card(
    [
        dbc.CardHeader('Tot Deaths : '),
        dbc.CardBody(
            [
                html.P('693 K')
            ]
        )
    ]
)

card_states = dbc.Card(
    [
        dbc.CardHeader('Tot States  : '),
        dbc.CardBody(
            [
                html.P('41 States')
            ]
        )
    ]
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
                dbc.Col(dcc.Graph(id='bar graphs of demographics'), width='auto')
            ], 
            align='Center',
        ),
    ],
    fluid=True
)

@app.callback(
    Output('bar graphs of demographics', 'figure'),
    Input('demographic_dropdown', 'value')
)

def demographic_plot(column):
    df1 = df[['Willingness to take vaccine', column]].value_counts().reset_index()
    df1.rename(columns={0:'Number of Respondents'}, inplace=True)
    plot = px.bar(df1, x=column, y='Number of Respondents', color='Willingness to take vaccine', barmode='group')
    return plot

if __name__ == '__main__':
    app.run_server(debug=True)

