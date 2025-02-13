
import os
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
import base64
import datetime
import io
import pandas as pd
import plotly.express as px

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets,  suppress_callback_exceptions=True)

# Variable global para almacenar los datos subidos
uploaded_data = None

loading_spinner = dcc.Loading(
    id="loading-spinner",
    type="cube",  # Puedes cambiar el tipo: "circle", "dot", "cube", etc.
    children=[
        html.Div(id="output-data-upload")  # Aquí se mostrará la tabla después de cargar los datos
    ]
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Acerca de", href="/acerca")),
    ],
    brand="Business Intelligence",
    brand_href="/",
    color="dark",
    dark=True,
)

app.layout = html.Div([
    navbar,
    dcc.Location(id='url', refresh=False),  # Rastrear la URL para navegación
    html.H1("SUPERMERCADO", style={
        'textAlign': 'center',
        'color': 'white',
        'fontFamily': 'Arial, sans-serif',
        'fontWeight': 'bold',
        'textTransform': 'uppercase',
        'letterSpacing': '1.5px',
        'textShadow': '1px 1px 2px #aaa',
        'margin-top': '120px'
    }),
    html.Div(id='page-content'),  # Placeholder para el contenido de la página

    # Enlaces de navegación
    html.Div([
       
        dcc.Link('Cargar datos', href='/', className='custom-button', style={'margin': '5px'}),
        dcc.Link('ver Datos', href='/view-data', className='custom-button custom-button-secondary', style={'margin': '5px'}),
        dcc.Link('Dashboard', href='/view-graphs', className='custom-button custom-button-success', style={'margin': '5px'}),
    ],style ={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
],
style={
    'background': 'linear-gradient(to bottom, rgba(0,0,139,0.7), rgba(64,224,208,0.7)), url("https://www.example.com/background.jpg")',
    'minHeight': '100vh',
   # 'background': 'linear-gradient(to bottom, rgba(0,123,255,0.7), rgba(135,206,235,0.7)), url("https://www.example.com/background.jpg")',
})

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')
               ])
def display_page(pathname):
    if pathname == '/view-data':
        return display_data_page()
    elif pathname == '/view-graphs':
        return display_graphs_page()
    else:
        return display_upload_page()

def display_upload_page():
    return html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Arrastrar o  ',
                html.A('Selecciona el archivo')
            ],style={'color': 'blue'}),
               style={
            'width': '60%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            'margin': '20px auto',  # Centrando el div
            'backgroundColor': '#F0F0F0'
        },
            multiple=True
        ),
        loading_spinner,

      #  html.Div(id='output-data-upload')  # Colocar la salida aquí
    ])

def display_data_page():
    global uploaded_data
    if uploaded_data is None:
        return html.Div([
            'No hay datos, cargue nuevos datos'
        ], style ={'display': 'flex', 
                   'justify-content': 'center', 
                   'align-items': 'center',
                   'color':'red', 'fontFamily': 
                   'Arial, sans-serif',
                   'fontWeight': 'bold'})

    return html.Div([
        html.H5("Datos cargados"),
        dash_table.DataTable(
            uploaded_data.to_dict('records'),
            [{'name': i, 'id': i} for i in uploaded_data.columns],
            page_size=20,
            style_table={'overflowX': 'auto'},
        ),
        dcc.Link('Go to Graphs', href='/view-graphs'),  # Enlace para ver gráficos
    ])

# def display_graphs_page():
#     global uploaded_data
#     if uploaded_data is None:
#         return html.Div([
#             'No data uploaded. Please upload a file first.'
#         ])

#     uploaded_data['Fecha'] = pd.to_datetime(uploaded_data['Fecha'])
#     uploaded_data['Mes'] = uploaded_data['Fecha'].dt.strftime('%B')

#     # Filtrar los datos según los meses seleccionados
#     #filtered_data = uploaded_data[uploaded_data['Mes'].isin(selected_months)] if selected_months else uploaded_data
#     total_ventas = calcular_total_ventas(uploaded_data)  # Llama a la función para obtener el total
#     total_costo = total_cost(uploaded_data)
#     total_ingreso = total_ingr(uploaded_data)

#     meses = [
#         {'label': 'Enero', 'value': 'Enero'},
#         {'label': 'Febrero', 'value': 'Febrero'},
#         {'label': 'Marzo', 'value': 'Marzo'},
#         {'label': 'Abril', 'value': 'Abril'},
#         {'label': 'Mayo', 'value': 'Mayo'},
#         {'label': 'Junio', 'value': 'Junio'},
#         {'label': 'Julio', 'value': 'Julio'},
#         {'label': 'Agosto', 'value': 'Agosto'},
#         {'label': 'Septiembre', 'value': 'Septiembre'},
#         {'label': 'Octubre', 'value': 'Octubre'},
#         {'label': 'Noviembre', 'value': 'Noviembre'},
#         {'label': 'Diciembre', 'value': 'Diciembre'},
#     ]
#     return html.Div([

#         # Create a row for the three top cards with no content
#         dbc.Row([
#             dbc.Col(dbc.Card(dbc.CardBody([
#                 html.H4("Ventas", className='card-title'),
#                 html.H5(total_ventas, className='card-text'),
#             ])), width=4),
#             dbc.Col(dbc.Card(dbc.CardBody([
#                 html.H4("Costos", className='card-title'),
#                 html.H5(total_costo, className='card-text'),  # Muestra el total de costos
#             ])), width=4),
#             dbc.Col(dbc.Card(dbc.CardBody([
#                 html.H4("Ingresos", className='card-title'),
#                 html.H5(total_ingreso, className='card-text'),

#             ])), width=4),
#         ], justify='around'),

#         dbc.Row([
#              dbc.Col(
#                     dbc.Card(dbc.CardBody([
#                     html.H4("Seleccionar Mes(es)", className='card-title'),
#                     dcc.Checklist(
#                         id='mes-checklist',  # ID para el Checklist
#                         options=meses,
#                         value=[],  # Inicialmente vacío, sin meses seleccionados
#                         inline=True,  # Opciones en línea
#                         labelStyle={
#                             'display': 'block',
#                             'marginBottom': '10px',  # Espaciado entre los checkboxes
#                             'fontSize': '16px',  # Tamaño de la fuente
#                             'color': '#ffffff'  # Color del texto
#                         },
#                         style={'padding': '10px', 'backgroundColor': '#343a40', 'borderRadius': '5px'},  # Fondo de la checklist
#                         inputStyle={'marginRight': '10px'},  # Espaciado a la derecha del checkbox
#                         className='custom-checklist'  # Puedes añadir una clase CSS adicional para personalización
#                     ),
#                 ])), width=3
#             ),
#             dbc.Col(
#                 dbc.Card(dbc.CardBody([
#                     html.H4("Gráfico por Categoría", className='card-title'),
#                     dcc.Graph(figure=graph_categories(uploaded_data)),
#                 ])), width=9
#             ),
    
#         ], justify='around', className="mt-3"),  # Adding margin to separate rows

#         dbc.Row([
#             dbc.Col(
#                 dbc.Card(dbc.CardBody([
#                     html.H4("Gráfico por Tipo de Pago", className='card-title'),
#                     dcc.Graph(figure=graph_type_payment(uploaded_data)),
#                 ])), width=4
#             ),
#                     dbc.Col(
#                 dbc.Card(dbc.CardBody([
#                     html.H4("Gráfico por Sucursal", className='card-title'),
#                     dcc.Graph(figure=graph_branches(uploaded_data)),
#                 ])), width=4
#             ),
#             dbc.Col(
#                 dbc.Card(dbc.CardBody([
#                     html.H4("Gráfico de Ventas por Hora", className='card-title'),
#                     dcc.Graph(figure=graph_sales_hours(uploaded_data)),
#                 ])), width=4
#             ),
#         ], justify='around', className="mt-3"),
#     ])

def display_graphs_page(selected_months=None):
    global uploaded_data
    if uploaded_data is None:
        return html.Div([
            'No hay datos cargados. Por favor, carga un archivo primero.'
        ])

    # Convertir la columna 'Fecha' a tipo datetime y extraer el mes
    uploaded_data['Fecha'] = pd.to_datetime(uploaded_data['Fecha'])
    uploaded_data['Mes'] = uploaded_data['Fecha'].dt.strftime('%B')

    # Filtrar datos según los meses seleccionados
    if selected_months:
        filtered_data = uploaded_data[uploaded_data['Mes'].isin(selected_months)]
    else:
        filtered_data = uploaded_data

    total_ventas = calcular_total_ventas(filtered_data)
    total_costo = total_cost(filtered_data)
    total_ingreso = total_ingr(filtered_data)

    meses = [
        {'label': 'Enero', 'value': 'Enero'},
        {'label': 'Febrero', 'value': 'Febrero'},
        {'label': 'Marzo', 'value': 'Marzo'},
        {'label': 'Abril', 'value': 'Abril'},
        {'label': 'Mayo', 'value': 'Mayo'},
        {'label': 'Junio', 'value': 'Junio'},
        {'label': 'Julio', 'value': 'Julio'},
        {'label': 'Agosto', 'value': 'Agosto'},
        {'label': 'Septiembre', 'value': 'Septiembre'},
        {'label': 'Octubre', 'value': 'Octubre'},
        {'label': 'Noviembre', 'value': 'Noviembre'},
        {'label': 'Diciembre', 'value': 'Diciembre'},
    ]
    
    return html.Div([

        # Tarjetas para mostrar Totales
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Ventas", className='card-title'),
                html.H5(total_ventas, className='card-text'),
            ])), width=4),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Costos", className='card-title'),
                html.H5(total_costo, className='card-text'),
            ])), width=4),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Ingresos", className='card-title'),
                html.H5(total_ingreso, className='card-text'),
            ])), width=4),
        ], justify='around'),

        # Sección para seleccionar meses y gráficos
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Seleccionar Mes(es)", className='card-title'),
                dcc.Checklist(
                    id='mes-checklist',
                    options=meses,
                    value=[],  # Inicialmente vacío
                    inline=True,
                    labelStyle={'display': 'block', 'marginBottom': '10px'},
                    style={'padding': '10px', 'backgroundColor': '#343a40', 'borderRadius': '5px'},
                    inputStyle={'marginRight': '10px'},
                ),
            ])), width=3),

            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Gráfico por Categoría", className='card-title'),
                dcc.Graph(id="grafico-categoria",figure=graph_categories(filtered_data)),
            ])), width=9),

        ], justify='around', className="mt-3"),

        # Gráficos adicionales
        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Gráfico por Tipo de Pago", className='card-title'),
                dcc.Graph(id="grafico-pago",figure=graph_type_payment(filtered_data)),
            ])), width=4),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Gráfico por margen de ganancia", className='card-title'),
                dcc.Graph(id='grafico-sucursal', figure=graph_profit_vs_price(filtered_data)),
            ])), width=4),
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Gráfico de Ventas por Hora", className='card-title'),
                dcc.Graph(id='grafico-hora',figure=graph_sales_hours(filtered_data)),
            ])), width=4),
        ], justify='around', className="mt-3"),


        dbc.Row([
            dbc.Col(dbc.Card(dbc.CardBody([
                html.H4("Gráfico ventas distribuidas" , className='card-title'),
                dcc.Graph(id="grafico-",figure=graph_sales_by_branch(filtered_data)),
            ])), width=8),
        ], justify='around', className="mt-3"),
    ])

@app.callback(
    #Output('graphs-output', 'children'),  # ID del contenedor donde se mostrarán los gráficos
   # Output('grafico-sucursal', 'figure'),  # ID del contenedor donde se mostrarán los gráficos
    [Input('mes-checklist', 'value')]
)
def update_graphs(selected_months):
    return graph_categories(uploaded_data[uploaded_data['Mes'].isin(selected_months)])  # De

def generate_graphs(df):
    graphs = []

    graphs.append(dbc.Card(
        dbc.CardBody([
            html.H4("Gráfico por Categoría", className='card-title'),
            dcc.Graph(figure=graph_categories(df)),
        ])
    ))

    # Gráfico por Sucursal
    graphs.append(dbc.Card(
        dbc.CardBody([
            html.H4("Gráfico margen de ganancia", className='card-title'),
            dcc.Graph(figure =graph_profit_vs_price(df)),
        ])
    ))

    # Gráfico por Tipo de Pago
    graphs.append(dbc.Card(
        dbc.CardBody([
            html.H4("Gráfico por Tipo de Pago", className='card-title'),
            dcc.Graph(figure=graph_type_payment(df)),
        ])
    ))

    # Gráfico por Hora
    graphs.append(dbc.Card(
        dbc.CardBody([
            html.H4("Gráfico de Ventas por Hora", className='card-title'),
            dcc.Graph(figure=graph_sales_hours(df)),
        ])
    ))
   #  return html.Div(graphs)
    return dbc.Row(graphs, justify='around', style={"margin": "20px"})

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    global uploaded_data
    try:
        if 'csv' in filename:
            uploaded_data = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            uploaded_data = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'Error al procesar el archivo.'
        ])

    return html.Div([
        html.H5(filename,  style={
            'font-family': 'Arial, sans-serif',
            'color': '#4A90E2',  # Un color azul suave
            'background-color': '#F0F4F8',  # Fondo suave
            'padding': '10px 15px',
            'border-radius': '5px',  # Bordes redondeados
            'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',  # Sombra ligera
            'margin-top': '20px',  # Espaciado hacia arriba
            'text-align': 'center',  # Centrar el texto
            'width': '400px',
            'margin': '0 auto'  # Centrar horizontalmente el H5 Centrar el texto
        }),
        # html.Div('Archivo cargado correctamente.'),
        # html.Div(dcc.Link('Ver datos', href='/view-data')),  # Enlace para ver datos
        # html.Div(dcc.Link('Dashboard', href='/view-graphs')),  # Enlace para ver gráficos
    ],  style={
       'display': 'flex', 'justify-content': 'center', 'align-items': 'center'
    })

@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        
        children = [
            parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        
        return children  # Unpacking de children
    return [html.Div("No hay datos cargados.",style ={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}), None]
# Funciones de gráficos

def graph_categories(df):
    df['Total'] = pd.to_numeric(df['Total de Venta'], errors='coerce')
    sales_by_category = df.groupby('Categoría')['Total'].sum().reset_index()
    fig = px.bar(sales_by_category, x='Categoría', y='Total', labels={'Categoría': 'Categoría', 'Total': 'Total de Ventas'},
                 color='Categoría', color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(plot_bgcolor='rgba(50, 50, 50, 0.8)', paper_bgcolor='rgba(50, 50, 50, 0.8)', font=dict(color='white'))
    return fig

# def graph_branches(df):
#     # df['Total'] = pd.to_numeric(df['Total de Venta'], errors='coerce').fillna(0)
#     # sales_by_branches = df.groupby('Sucursal')['Total'].sum().reset_index()
#     # fig = px.pie(sales_by_branches, names='Sucursal', values='Total',
#     #              labels={'Sucursal': 'Sucursal', 'Total': 'Total de Ventas'},
#     #              color_discrete_sequence=px.colors.sequential.RdBu)
#     # fig.update_layout(plot_bgcolor='rgba(50, 50, 50, 0.8)', paper_bgcolor='rgba(50, 50, 50, 0.8)', font=dict(color='white'))

#     df['Total'] = pd.to_numeric(df['Total de Venta'], errors='coerce').fillna(0)
#     sales_by_month = df.groupby('Mes')['Total'].sum().reset_index()
#     fig = px.line(sales_by_month, x='Mes', y='Total', 
#                   labels={'Mes': 'Mes', 'Total': 'Total de Ventas'}, 
#                   markers=True, 
#                   color_discrete_sequence=['#FFA07A'])
#     fig.update_layout(plot_bgcolor='rgba(50, 50, 50, 0.8)', paper_bgcolor='rgba(50, 50, 50, 0.8)', font=dict(color='white'))

#     return fig

def graph_type_payment(df):
    df['Total'] = pd.to_numeric(df['Total de Venta'], errors='coerce')
    sales_by_type_payment = df.groupby('Tipo de Pago')['Total'].sum().reset_index()
    fig = px.pie(sales_by_type_payment, names='Tipo de Pago', values='Total',
                 labels={'Tipo de Pago': 'Tipo de Pago', 'Total': 'Total de Ventas'},
                 color_discrete_sequence=px.colors.sequential.Agsunset)
    fig.update_layout(plot_bgcolor='rgba(50, 50, 50, 0.8)', paper_bgcolor='rgba(50, 50, 50, 0.8)', font=dict(color='white'))
    return fig

def graph_sales_hours(df):
    df['Total'] = pd.to_numeric(df['Total de Venta'], errors='coerce')
    df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce', format='%H:%M')
    df['Hora Dia'] = df['Hora'].dt.hour
    sales_by_hour = df['Hora Dia'].value_counts().sort_index()
    fig = px.bar(sales_by_hour, x=sales_by_hour.index, y=sales_by_hour.values, 
                 labels={'x': 'Hora del Día', 'y': 'Número de Compras'})
    fig.update_layout(plot_bgcolor='rgba(50, 50, 50, 0.8)', paper_bgcolor='rgba(50, 50, 50, 0.8)', font=dict(color='white'))
    return fig

def calcular_total_ventas(df):
    # Asegúrate de que la columna que contiene los valores sea convertible a numérico
    df['Total'] = pd.to_numeric(df['Total de Venta'], errors='coerce')
    total_sales = df['Total'].sum()
    total_sales_formatted = format_currency(total_sales)
    return total_sales_formatted

def total_cost(df):
    """
    Calcula el total de los costos y lo devuelve en un formato legible (miles o millones).

    Parámetros:
    df (pandas.DataFrame): El DataFrame que contiene una columna 'Costo de Bienes Vendidos' con los valores de las ventas.

    Retorna:
    str: El total de costos, formateado en miles o millones, dependiendo del valor.
    """
    total= (df['Costo Unitario']*df['Cantidad Vendida']).sum() 
    #total_ventas_formateado = f"${total_ventas:,.2f}"
    total_cost_formatted = format_currency(total)
    return total_cost_formatted

def total_ingr(df):
    total_ingr = df['Margen de Ganancia'].sum()
    total_ingr_formatted=format_currency(total_ingr)
    return total_ingr_formatted

def format_currency(value):
    """
    Formatea un valor numérico a una cadena de texto representativa en términos de miles o millones, 
    dependiendo de su magnitud.

    Parámetros:
    value (float): El valor numérico a formatear.
    Retorna:
    str: El valor formateado como una cadena de texto. Si el valor es mayor o igual a un millón, 
         se expresa en millones con dos decimales. Si es mayor o igual a mil, se expresa en miles 
         con dos decimales. Si es menor a mil, se formatea simplemente con dos decimales.
    """
    if value >= 1_000_000:
        return f"{value / 1_000_000:,.2f} millones"
    elif value >= 1_000:
        return f"{value / 1_000:,.2f} mil"
    else:
        return f"{value:,.2f}"

def graph_profit_vs_price(df):
    df['Margen de Ganancia'] = pd.to_numeric(df['Margen de Ganancia'], errors='coerce').fillna(0)
    df['Precio de Venta Unitario'] = pd.to_numeric(df['Precio de Venta Unitario'], errors='coerce').fillna(0)
    fig = px.scatter(df, x='Precio de Venta Unitario', y='Margen de Ganancia', 
                     color='Categoría', 
                     labels={'Precio de Venta Unitario': 'Precio de Venta Unitario', 'Margen de Ganancia': 'Margen de Ganancia'}, 
                     color_discrete_sequence=px.colors.qualitative.T10)
    fig.update_layout(plot_bgcolor='rgba(50, 50, 50, 0.8)', paper_bgcolor='rgba(50, 50, 50, 0.8)', font=dict(color='white'))
    return fig

def graph_sales_by_branch(df):
    df['Total'] = pd.to_numeric(df['Total de Venta'], errors='coerce').fillna(0)
    sales_by_branch = df.groupby('Sucursal')['Total'].sum().reset_index()
    fig = px.pie(sales_by_branch, names='Sucursal', values='Total', 
                 labels={'Sucursal': 'Sucursal', 'Total': 'Total de Ventas'}, 
                 color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_layout(plot_bgcolor='rgba(50, 50, 50, 0.8)', paper_bgcolor='rgba(50, 50, 50, 0.8)', font=dict(color='white'))
    return fig



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
