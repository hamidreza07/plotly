import pandas as pd     #(version 1.0.0)
import plotly           #(version 4.5.0)
import plotly.express as px

import dash             #(version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

#---------------------------------------------------------------

df = pd.read_csv(r"p6\DOHMH_New_York_City_Restaurant_Inspection_Results.csv")  # https://drive.google.com/file/d/1jyvSiRjaNIeOCP59dUFQuZ0_N_StiQOr/view?usp=sharing
df['INSPECTION DATE'] = pd.to_datetime(df['INSPECTION DATE'])
df = df.groupby(['INSPECTION DATE','CUISINE DESCRIPTION','CAMIS'], as_index=False)['SCORE'].mean()
df = df.set_index('INSPECTION DATE')
df = df.loc['2016-01-01':'2019-12-31']
df = df.groupby([pd.Grouper(freq="M"),'CUISINE DESCRIPTION'])['SCORE'].mean().reset_index()
# print (df[:5])

#---------------------------------------------------------------
app.layout = html.Div([

        html.Div([
        html.H1("CUISINE DESCRIPTION" ,style={ "align-items": "center","text-align": "center"}),
        html.Br(),
        html.Label(['Choose 3 Cuisines to Compare:'],style={'font-weight': 'bold', "text-align": "center"}),
        dcc.Dropdown(id='cuisine_one',
            options=[{'label':x, 'value':x} for x in df.sort_values('CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
            value='African',
            multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Cuisine...',
            className='form-dropdown',
            style={'width':"100%"},
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='cuisine_two',
            options=[{'label':x, 'value':x} for x in df.sort_values('CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
            value='Asian',
             multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Cuisine...',
            className='form-dropdown2',
            style={'width':"100%"},
            persistence='string',
            persistence_type='memory'),

        dcc.Dropdown(id='cuisine_three',
            options=[{'label':x, 'value':x} for x in df.sort_values('CUISINE DESCRIPTION')['CUISINE DESCRIPTION'].unique()],
            value='Donuts',
             multi=False,
            disabled=False,
            clearable=True,
            searchable=True,
            placeholder='Choose Cuisine...',
            className='form-dropdown3',
            style={'width':"100%"},
            persistence='string',
            persistence_type='memory'), #persistence_type (a value equal to: 'local', 'session' or 'memory'; default 'local'): Where persisted user changes will be stored: memory: only kept in memory, reset on page refresh. local: window.localStorage, data is kept after the browser quit. session: window.sessionStorage, data is cleared once the browser quit.



    ],className='three columns'),


html.Div(className='nine columns',style={'display':'flex'},children=[
        html.Div([
            dcc.Graph(id='linechart',figure={},style={'width':"100%","height":"100%"}),
        ],className='six columns'),

        html.Div([
            dcc.Graph(id='piechart',figure={},style={'width':"100%","height":"100%"}),
        ],className='six columns'),

    ])



])

#---------------------------------------------------------------

@app.callback(
    Output('linechart','figure'),
    Output('piechart','figure'),
    [Input('cuisine_one','value'),
     Input('cuisine_two','value'),
     Input('cuisine_three','value')]
)

def build_graph(first_cuisine, second_cuisine, third_cuisine):
    dff=df[(df['CUISINE DESCRIPTION']==first_cuisine)|
           (df['CUISINE DESCRIPTION']==second_cuisine)|
           (df['CUISINE DESCRIPTION']==third_cuisine)]
    print(dff[:5])

    fig = px.line(dff, x="INSPECTION DATE", y="SCORE", color='CUISINE DESCRIPTION')
    fig.update_layout(yaxis={'title':'NEGATIVE POINT'},
                      title={'text':'Restaurant Inspections in NYC',
                      'font':{'size':28},'x':0.5,'xanchor':'center'})


    pie_chart=px.pie(
            data_frame=dff,
            names="CUISINE DESCRIPTION",
            values='SCORE',
            hole=.3,
            labels={'CUISINE DESCRIPTION':'CUISINE'} #rename
            )
    return fig,pie_chart

#---------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)

    
    
# https://youtu.be/Kr94sFOWUMg