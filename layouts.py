from dash import dcc, html
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
        dbc.NavItem(dbc.NavLink("Acerca de", href="#")),
        dbc.NavItem(dbc.NavLink("Contacto", href="#")),
    ],
    brand="Bussiness Intellingence",
    brand_href="#",
    color="primary",
    dark=True,
)

# Layout para cargar archivo
upload_layout = html.Div([
    navbar,  # Navbar en la parte superior
    html.H1("INGRESE LA FUENTE DE DATOS", style={
        'textAlign': 'center',
        'color': 'white', 
        'fontFamily': 'Arial, sans-serif',
        'fontWeight': 'bold', 
        'textTransform': 'uppercase',
        'letterSpacing': '1.5px', 
        'textShadow': '1px 1px 2px #aaa',
        'margin-top': '120px'}),
    
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Arrastra y suelta o ',
            html.A('Selecciona un archivo Excel', style={'color': '#FF4136'})
        ]),
        style={
            'width': '60%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            'margin': '20px auto',
            'backgroundColor': '#F0F0F0'
        },
        multiple=False
    ),
    
    html.Div(id='output-data-upload', style={'textAlign': 'center', 'margin': '20px', 'color': '#3D9970'}),
    html.A(html.Button("Ver contenido del archivo", id='show-dataframe-btn', 
        style={'display': 'none'}), href="/dataframe", id='dataframe-link'),

    dcc.Store(id='stored-file'),  # Componente para almacenar el archivo cargado temporalmente
],
 style={
    'background': 'linear-gradient(to bottom, rgba(0,123,255,0.7), rgba(135,206,235,0.7)), url("https://www.example.com/background.jpg")',
    'minHeight': '100vh',  # Para que el fondo cubra toda la altura de la página
})

# Layout para mostrar el DataFrame
dataframe_layout = html.Div([
    navbar,  # Navbar
    html.H1("Contenido del archivo cargado", style={'textAlign': 'center', 'color': '#0074D9'}),
    html.Div(id='dataframe-content', style={'textAlign': 'center', 'marginTop': '20px'}),
    dcc.Link('Volver a cargar archivo', href='/')
])