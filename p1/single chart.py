import pandas as pd
import random
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_excel("Farm - clustering or prediction.xlsx")

# you need to include __name__ in your Dash constructor if
# you plan to use a custom CSS or JavaScript in your Dash apps
app = dash.Dash(__name__)

#---------------------------------------------------------------
app.layout = html.Div([
    html.Div([
        html.Label(['NYC Calls for Animal Rescue']),
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                     {'label': 'mesurment of rainfall', 'value': 'rainfall'},
                     {'label': 'size of farme', 'value': 'farmsize'},
                     {'label': 'quality of land', 'value': 'landquality'},
                     {'label': 'income of farme', 'value': 'farmincome'},
                     {'label': 'claim value', 'value': 'claimvalue'},
                     
            ],
            value='farmsize',
            # defualt display
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
    ]),

    html.Div([
        dcc.Graph(id='the_graph',figure=[])
    ]),

])

#---------------------------------------------------------------
# callback : interactive 
@app.callback(
    Output(component_id='the_graph', component_property='figure'),# output refer to output of function bellow
    [Input(component_id='my_dropdown', component_property='value')]#input goes to input of function bellow
)
def update_graph(Input):
    # my_dropdown refer to input component_id
    dff = df

    Output=px.box(
            data_frame=dff,
            x=Input,
            y='claimvalue',
            # z= "farmincome",
            # symbol='landquality'
            )

    return (Output)


if __name__ == '__main__':
    app.run_server(debug=True)