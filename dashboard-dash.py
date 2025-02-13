# import pandas as pd
# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import plotly.express as px

# # Cargar datos desde un archivo CSV
# df = pd.read_csv('supermercado.csv')

# # Crear la aplicación Dash
# app = dash.Dash(__name__)

# # Layout del dashboard
# app.layout = html.Div([
#     html.H1("Dashboard de Supermercado"),
    
#     # Filtros (Dropdown para la sucursal y el tipo de pago)
#     html.Div([
#         html.Label("Seleccionar Sucursal:"),
#         dcc.Dropdown(
#             id='sucursal-dropdown',
#             options=[{'label': sucursal, 'value': sucursal} for sucursal in df['Sucursal'].unique()],
#             value=df['Sucursal'].unique()[0]  # Valor por defecto
#         ),
#         html.Label("Seleccionar Tipo de Pago:"),
#         dcc.Dropdown(
#             id='tipo-pago-dropdown',
#             options=[{'label': pago, 'value': pago} for pago in df['Tipo de Pago'].unique()],
#             value=df['Tipo de Pago'].unique()[0]  # Valor por defecto
#         )
#     ]),
    
#     # Gráfico de ventas totales por categoría
#     dcc.Graph(id='ventas-categoria-graph'),
    
#     # Gráfico de ventas diarias
#     dcc.Graph(id='ventas-diarias-graph')
# ])

# # Callback para actualizar el gráfico de ventas por categoría
# @app.callback(
#     Output('ventas-categoria-graph', 'figure'),
#     [Input('sucursal-dropdown', 'value'), Input('tipo-pago-dropdown', 'value')]
# )
# def actualizar_grafico_categoria(sucursal_seleccionada, tipo_pago_seleccionado):
#     # Filtrar datos según la sucursal y tipo de pago seleccionados
#     df_filtrado = df[(df['Sucursal'] == sucursal_seleccionada) & (df['Tipo de Pago'] == tipo_pago_seleccionado)]
    
#     # Gráfico de ventas por categoría
#     fig = px.bar(df_filtrado, x='Categoria', y='Total de Venta', color='Categoria', title="Ventas por Categoría")
    
#     return fig

# # Callback para actualizar el gráfico de ventas diarias
# @app.callback(
#     Output('ventas-diarias-graph', 'figure'),
#     [Input('sucursal-dropdown', 'value'), Input('tipo-pago-dropdown', 'value')]
# )
# def actualizar_grafico_diario(sucursal_seleccionada, tipo_pago_seleccionado):
#     # Filtrar datos según la sucursal y tipo de pago seleccionados
#     df_filtrado = df[(df['Sucursal'] == sucursal_seleccionada) & (df['Tipo de Pago'] == tipo_pago_seleccionado)]
    
#     # Convertir la columna 'Fecha' en formato datetime
#     df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
    
#     # Agrupar por fecha y calcular las ventas totales por día
#     df_diario = df_filtrado.groupby('Fecha')['Total de Venta'].sum().reset_index()
    
#     # Gráfico de ventas diarias
#     fig = px.line(df_diario, x='Fecha', y='Total de Venta', title="Ventas Diarias")
    
#     return fig

# # Ejecutar la aplicación
# if __name__ == '__main__':
#     app.run_server(debug=True)



import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import base64
import io

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout del dashboard
app.layout = html.Div([
    html.H1("Dashboard de Supermercado"),

    # Componente para cargar archivos
    dcc.Upload(
        id='upload-data',
        children=html.Div(['Arrastra o selecciona un archivo XLS/XLSX']),
        style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
            'textAlign': 'center', 'margin': '10px'
        },
        multiple=False  # Permitir solo un archivo
    ),

    # Mensaje de estado del archivo cargado
    html.Div(id='output-data-upload'),


        html.H1("Ingresar fuente de datos", style={
        'textAlign': 'center',
        'color': 'white',  # Color de texto
        'fontFamily': 'Arial, sans-serif',
        'fontWeight': 'bold', 
        'textTransform': 'uppercase',
        'letterSpacing': '1.5px', 
        'textShadow': '1px 1px 2px #aaa',
        'margin-top': '120px'
    }),

    html.Div(style={
        'background': 'linear-gradient(to bottom, rgba(0,123,255,0.7), rgba(135,206,235,0.7)), url("https://www.example.com/background.jpg")',
        'minHeight': '100vh'
    }),

    # Dropdowns para filtrar
    html.Div([
        html.Label("Seleccionar Sucursal:"),
        dcc.Dropdown(id='sucursal-dropdown'),
        
        html.Label("Seleccionar Tipo de Pago:"),
        dcc.Dropdown(id='tipo-pago-dropdown')
    ]),
    
    # Gráfico de ventas totales por categoría
    dcc.Graph(id='ventas-categoria-graph'),
    
    # Gráfico de ventas diarias
    dcc.Graph(id='ventas-diarias-graph')
])

# Función para procesar el archivo subido
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    
    # Decodificar el archivo cargado
    decoded = base64.b64decode(content_string)
    
    # Verificar si el archivo es Excel (XLS o XLSX)
    if 'xls' in filename:
        # Leer el archivo Excel usando pandas
        df = pd.read_excel(io.BytesIO(decoded))
    else:
        return html.Div(['El archivo cargado no es un Excel.'])
    
    print(df.head()) 
    # Aquí puedes realizar cualquier transformación adicional si es necesario
    # Retornar el DataFrame
    return df

# Callback para procesar el archivo y actualizar el dashboard
@app.callback(
    [Output('sucursal-dropdown', 'options'),
     Output('sucursal-dropdown', 'value'),
     Output('tipo-pago-dropdown', 'options'),
     Output('tipo-pago-dropdown', 'value'),
     Output('output-data-upload', 'children')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def actualizar_dropdowns(contents, filename):
    if contents is None:
        return [[], None, [], None, 'No se ha cargado ningún archivo.']
    
    # Convertir el archivo subido a un DataFrame
    df = parse_contents(contents, filename)
    
    # Crear opciones para los dropdowns
    sucursal_options = [{'label': sucursal, 'value': sucursal} for sucursal in df['Sucursal'].unique()]
    tipo_pago_options = [{'label': pago, 'value': pago} for pago in df['Tipo de Pago'].unique()]
    
    # Texto de éxito para la carga del archivo
    mensaje_carga = f'Archivo "{filename}" cargado con éxito.'

    return sucursal_options, df['Sucursal'].unique()[0], tipo_pago_options, df['Tipo de Pago'].unique()[0], mensaje_carga

# Callback para actualizar el gráfico de ventas por categoría
@app.callback(
    Output('ventas-categoria-graph', 'figure'),
    [Input('sucursal-dropdown', 'value'), Input('tipo-pago-dropdown', 'value'), Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def actualizar_grafico_categoria(sucursal_seleccionada, tipo_pago_seleccionado, contents, filename):
    if contents is None:
        return {}
    
    # Convertir el archivo subido a un DataFrame
    df = parse_contents(contents, filename)
    
    # Filtrar datos según la sucursal y tipo de pago seleccionados
    df_filtrado = df[(df['Sucursal'] == sucursal_seleccionada) & (df['Tipo de Pago'] == tipo_pago_seleccionado)]
    
    # Gráfico de ventas por categoría
    fig = px.bar(df_filtrado, x='Categoria', y='Total de Venta', color='Categoria', title="Ventas por Categoría")
    
    return fig

# Callback para actualizar el gráfico de ventas diarias
@app.callback(
    Output('ventas-diarias-graph', 'figure'),
    [Input('sucursal-dropdown', 'value'), Input('tipo-pago-dropdown', 'value'), Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def actualizar_grafico_diario(sucursal_seleccionada, tipo_pago_seleccionado, contents, filename):
    if contents is None:
        return {}
    
    # Convertir el archivo subido a un DataFrame
    df = parse_contents(contents, filename)
    
    # Filtrar datos según la sucursal y tipo de pago seleccionados
    df_filtrado = df[(df['Sucursal'] == sucursal_seleccionada) & (df['Tipo de Pago'] == tipo_pago_seleccionado)]
    
    # Convertir la columna 'Fecha' en formato datetime
    df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
    
    # Agrupar por fecha y calcular las ventas totales por día
    df_diario = df_filtrado.groupby('Fecha')['Total de Venta'].sum().reset_index()
    
    # Gráfico de ventas diarias
    fig = px.line(df_diario, x='Fecha', y='Total de Venta', title="Ventas Diarias")
    
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)

