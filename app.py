from dash import Dash
import dash_bootstrap_components as dbc
from dash import dcc, html  
from layouts import upload_layout, dataframe_layout
from dash.dependencies import Input, Output

# Inicializar la aplicación Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True 

server = app.server 

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Para manejar las rutas
    html.Div(id='page-content')             # Para cargar el layout de la página
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dataframe':
        return dataframe_layout
    else:
        return upload_layout

if __name__ == '__main__':
    app.run_server(debug=True)
