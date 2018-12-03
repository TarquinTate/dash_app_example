
# coding: utf-8

# In[ ]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd

# read values
dfo = pd.read_csv('nama_10_gdp_1_Data.csv', engine = 'python')
dfo.columns = ['Time', 'Geo', 'Unit', 'NA_item', 'Value', 'Flag_and_footnotes']

# clean data
# clear the lines with 'Euro', which are not european countries and set the measure to be Current prices, million euro
dfn = dfo[~dfo['Geo'].str.contains('Euro')]
df = dfn[dfn['Unit'].str.contains('Current prices, million euro')]

# get the indicators
available_indicators_n = df['NA_item'].unique()
# get the indicators
available_indicators_g = df['Geo'].unique()

# first paragraph
# design layout
app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators_n],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                value='Linear',
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators_n],
                value='Gross domestic product at market prices'
            ),
            dcc.RadioItems(
                id='yaxis-type',
                value='Linear',
            )
        ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'), # graph component

    dcc.Slider( # slider component
        id='year--slider',
        min=df['Time'].min(),
        max=df['Time'].max(),
        value=df['Time'].max(),
        step=None,
        marks={str(year): str(year) for year in df['Time'].unique()}
    ),
    
    html.Div([
        
        html.Div([
            dcc.Dropdown(
                id='Countries',
                options=[{'label': i, 'value': i} for i in available_indicators_g],
                value='France'
            ),
            
            dcc.RadioItems(id='Countries-type')
        
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='Indicators',
                options=[{'label': i, 'value': i} for i in available_indicators_n],
                value='Gross domestic product at market prices'
            ),
            
            dcc.RadioItems(id='Indicators-type')
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='Graphic') # graph component
])

@app.callback( #call back function to update
    dash.dependencies.Output('indicator-graphic', 'figure'), #diff output, diff callbacks
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('xaxis-type', 'value'),
     dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df[df['Time'] == year_value] # filter the data for the year
    
    return {  #still in call back function
        'data': [go.Scatter(
            x=dff[dff['NA_item'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_item'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_item'] == yaxis_column_name]['Geo'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'color' : ('rgb(10, 186, 181)'),
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('Graphic', 'figure'),
    [dash.dependencies.Input('Countries', 'value'),
     dash.dependencies.Input('Indicators', 'value'),
     dash.dependencies.Input('Countries-type', 'value'),
     dash.dependencies.Input('Indicators-type', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type):

    
    return {  #still in call back function
        'data': [go.Scatter(
            x=df['Time'].unique(),
            y=df[(df['Geo'] == xaxis_column_name) & (df['NA_item'] == yaxis_column_name)]['Value'],
            text=xaxis_column_name,
            mode='lines',
            line = {
                'color' : ('rgb(10, 186, 181)'),
                'shape':'spline'
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 60, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
            
        )
    }

if __name__ == '__main__':
    app.run_server()

