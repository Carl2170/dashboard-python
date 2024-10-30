from dash import dcc, html
from app import app
from layouts import upload_layout, dataframe_layout
from dash.dependencies import Input, Output

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
