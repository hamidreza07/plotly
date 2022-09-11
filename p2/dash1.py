import dash  # use Dash version 1.16.0 or higher for this app to work
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px

df = px.data.gapminder()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(id='dpdn2', value=['Germany','Brazil'], multi=True,
                 options=[{'label': x, 'value': x} for x in
                          df.country.unique()]),
    html.Div([
        dcc.Graph(id='pie-graph', figure={}, className='six columns'),
        dcc.Graph(id='my-graph', figure={}, clickData=None, hoverData=None, # I assigned None for tutorial purposes. By defualt, these are None, unless you specify otherwise.
                  config={
                      'staticPlot': False,     # True, False toolpad hide if false
                      'scrollZoom': True,      # True, False
                      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                      'showTips': True,       # True, False
                      'displayModeBar': True,  # True, False, 'hover'
                      'watermark': True,
                    #   'modeBarButtonsToRemove': ['pan2d','select2d'],
                        },
                  className='six columns'
                  )
    ])
])


@app.callback(
    Output(component_id='my-graph', component_property='figure'),
    Input(component_id='dpdn2', component_property='value'),
)
def update_graph(Input):
    dff = df[df.country.isin(Input)]
    Output = px.line(data_frame=dff, x='year', y='gdpPercap', color='country',
                  custom_data=['country', 'continent', 'lifeExp', 'pop'])
    Output.update_traces(mode='lines+markers')
    return Output


# Dash version 1.16.0 or higher
@app.callback(
    Output(component_id='pie-graph', component_property='figure'),
    Input(component_id='my-graph', component_property='hoverData'),
    Input(component_id='my-graph', component_property='clickData'),
    Input(component_id='my-graph', component_property='selectedData'),
    Input(component_id='dpdn2', component_property='value')
)
def update_side_graph(hoverData, clk_data, slct_data, country_chosen):
    if clk_data is None:
        dff2 = df[(df.country.isin(country_chosen))&(df.year == 1952)]
        print(dff2)
        Output = px.pie(data_frame=dff2, values='pop', names='country',
                      title='Population for 1952')
        return Output
    else:
        print(f'hover data: {hoverData}')
        # print(hov_data['points'][0]['customdata'][0])
        print(f'click data: {clk_data}')
        print(f'selected data: {slct_data}')
        dff2 = df[df.country.isin(country_chosen)]
        hov_year = clk_data['points'][0]['x']
        dff2 = dff2[dff2.year == hov_year]
        Output = px.pie(data_frame=dff2, values='pop', names='country', title=f'Population for: {hov_year}')
        return Output


if __name__ == '__main__':
    app.run_server(debug=True)
    
    
# https://youtu.be/G8r2BB3GFVY