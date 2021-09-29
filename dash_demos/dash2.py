import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
import numpy as np

app = dash.Dash(__name__)

df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig1 = px.scatter(df, x='gdp per capita', y='life expectancy', size='population', color='continent', hover_name='country', log_x=True, size_max=70)

app.layout = html.Div(children=[
    html.Div(classname='row', 
    children=[
        html.Div(
            className='four columns for user controls'),
            
        html.Div(
            className='eight columns for viz'
        )

    ])
]
)

# For auto reload
if __name__ == '__main__':
    app.run_server(debug=True)