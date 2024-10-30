from dash import html, dcc 
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
import io
import base64

# Función para procesar el archivo cargado
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    
    # Decodificar el contenido base64
    decoded = base64.b64decode(content_string)
    
    try:
        if 'xls' in filename or 'xlsx' in filename:  # Verificar formato de archivo
            df = pd.read_excel(io.BytesIO(decoded))
            return df.to_dict('records')  # Convertir DataFrame a formato JSON compatible
    except Exception as e:
        print(f'Error al procesar el archivo: {e}')
        return None

# Callback para procesar el archivo cargado y almacenarlo
@app.callback(
    [Output('output-data-upload', 'children'),
     Output('stored-file', 'data'),
     Output('show-dataframe-btn', 'style')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    if contents is None:
        return html.Div(['Por favor, carga un archivo Excel.']), None, {'display': 'none'}
    
    df_records = parse_contents(contents, filename)
    if df_records:
        return html.Div(['Archivo cargado exitosamente']), df_records, {'display': 'block'}
    else:
        return html.Div(['Error al procesar el archivo.']), None, {'display': 'none'}

# Callback para mostrar el DataFrame en la vista de DataFrame
@app.callback(
    Output('dataframe-content', 'children'),
    [Input('stored-file', 'data')]
)
def show_dataframe(data):
    if data is None:
        return html.Div(['No hay datos para mostrar.'])
    
    df = pd.DataFrame(data)
    return html.Div([
        html.H5("Vista del DataFrame:"),
        dcc.Graph(
            figure={
                'data': [{
                    'type': 'table',
                    'header': {'values': list(df.columns), 'align': 'center'},
                    'cells': {'values': [df[col] for col in df.columns], 'align': 'center'}
                }]
            }
        )
    ])
