import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

app = dash.Dash(__name__)

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig1 = px.scatter(df, x='gdp per capita', y='life expectancy', size='population', color='continent', hover_name='country', log_x=True, size_max=70)

individual_continents = df['continent'].unique()

markdown_text = '''
# First Scatter Plot

Trial on Dash and how to use a markdown on a dashboard.

Aight lets go!
'''

app.layout = html.Div([
    dcc.Markdown(children=markdown_text),
    html.Label('Continent'),
    dcc.Dropdown(
        id='continents_dropdown',
        options=[ {'label' : i, 'value' : i} for i in individual_continents],
        value='Africa'
    ),
    dcc.Graph(id = 'Life expectancy vs GDP')   
])

@app.callback(
    Output('Life expectancy vs GDP','figure'),
    Input('continents_dropdown','value'))

def new_graph(selected_continent):
    filtered_df = df[df['continent'] == selected_continent]
    fig2 = px.scatter(filtered_df, x='gdp per capita', y='life expectancy', size='population',color='country', hover_name='country', log_x=True, size_max=70)
    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)