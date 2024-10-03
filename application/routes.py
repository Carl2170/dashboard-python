from application import app
from flask import render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

import json
import plotly
import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import os

UPLOAD_FOLDER = 'application/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#VARIABLE GLOBAL DEL DATAFRAME
nombre_archivo =None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload-file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Obtener el archivo de la solicitud
        file = request.files['file']
        csv_name = request.form['csv_name']

        # Verificar que se haya seleccionado un archivo
        if file and file.filename.endswith('.xlsx'):

            # Cargar el archivo Excel en un DataFrame
            df = pd.read_excel(file)
            dfO = df
            # Guardar el DataFrame como CSV
            csv_path = os.path.join(UPLOAD_FOLDER, f"{csv_name}.csv")
            nombre_archivo =f"{csv_name}.csv" 
            df.to_csv(csv_path, index=False)

    #TOTAL VENTAS
    graph_html_total_ventas= totalVentas(df)

    #TOTAL COSTO
    graph_html_total_costos = total_costo(df)

    #TOTAL INGRESO
    graph_html_total_ingreso = total_ingreso(df)

    #CANT SUCURSALES
    cant_sucursales = cantidad_sucursales(df)
    
    #MESES
    meses_ventas = meses(df)

    #GRAFICO VENTAS POR CATEGORIA
    grafico_categ = grafico_categoria(df)
    #GRAFICO VENTAS POR SUCURSAL
    grafico_suc = grafico_sucursales(df)
    #GRAFICO VENTAS POR TIPO PAGO
    grafico_pago = grafico_tipo_pago(df)
    #GRAFICO VENTAS POR HORA
    grafico_hora = grafico_ventas_hora(df)

    return render_template('dashboard.html',
                           graph_html_total_ventas=graph_html_total_ventas,
                           graph_html_total_costos=graph_html_total_costos,
                           graph_html_total_ingreso=graph_html_total_ingreso,
                           cant_sucursales=cant_sucursales,
                           meses_ventas=meses_ventas,
                           grafico_categ=grafico_categ,
                           grafico_suc=grafico_suc,
                           grafico_pago=grafico_pago,
                           grafico_hora=grafico_hora)


@app.route('/filtrar',  methods=['GET', 'POST'])
def filtrar():    
    # Obtener los meses seleccionados del formulario
    meses_seleccionados = request.form.getlist('meses')

    # Verificar si se seleccionaron meses
    if not meses_seleccionados:
        return redirect(url_for('upload_file'))

    # Filtrar el DataFrame por los meses seleccionados
    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, 'datos.csv'))  # Reemplaza con el nombre de tu archivo CSV guardado
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    # Diccionario de nombres de meses en español
    nombres_meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 
        6: 'Junio', 7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 
        10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    
    # Añadir la columna de nombre del mes
    df['Mes'] = df['Fecha'].dt.month.map(nombres_meses)
    
    # Filtrar el DataFrame por los meses seleccionados
    df_filtrado = df[df['Mes'].isin(meses_seleccionados)]

    # Actualizar los gráficos con los datos filtrados
    graph_html_total_ventas = totalVentas(df_filtrado)
    graph_html_total_costos = total_costo(df_filtrado)
    graph_html_total_ingreso = total_ingreso(df_filtrado)
    grafico_categ = grafico_categoria(df_filtrado)    
    cant_sucursales = cantidad_sucursales(df)
    grafico_suc = grafico_sucursales(df_filtrado)
    grafico_pago = grafico_tipo_pago(df_filtrado)
    grafico_hora = grafico_ventas_hora(df_filtrado)
    meses_ventas = meses(df)


    return render_template('dashboard.html',
                           graph_html_total_ventas=graph_html_total_ventas,
                           graph_html_total_costos=graph_html_total_costos,
                           graph_html_total_ingreso=graph_html_total_ingreso,
                           grafico_categ=grafico_categ,
                           grafico_suc=grafico_suc,
                           grafico_pago=grafico_pago,
                           grafico_hora=grafico_hora,
                           cant_sucursales=cant_sucursales,
                           meses_ventas=meses_ventas)

@app.route('/redireccionar')
def redireccion():
    return redirect('dashboard')

def totalVentas(df):
    total_ventas = df['Total'].sum()
#total_ventas_formateado = f"${total_ventas:,.2f}"
    total_ventas_formateado = format_currency(total_ventas)
    return total_ventas_formateado

def total_costo(df):
    total_costo = df['Costo de Bienes Vendidos'].sum()
    #total_ventas_formateado = f"${total_ventas:,.2f}"
    total_costo_formateado = format_currency(total_costo)
    return total_costo_formateado  

def total_ingreso(df):
    total_ingreso = df['Ingreso Bruto'].sum()
    total_ingreso_formateado=format_currency(total_ingreso)
    return total_ingreso_formateado

def grafico_ventas_hora(df):
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce', format='%H:%M')
    df['Hora Dia'] = df['Hora'].dt.hour
    compras_por_hora = df['Hora Dia'].value_counts().sort_index()


    fig = px.bar(compras_por_hora, 
             x=compras_por_hora.index, 
             y=compras_por_hora.values, 
             labels={'x': 'Hora del Día', 'y': 'Número de Compras'})

    fig.update_layout(
        width=255,
        height=250,
        plot_bgcolor='black',  # Fondo del área del gráfico
        paper_bgcolor='black',  # Fondo del gráfico completo
        font=dict(color='white')  # Cambiar el color de las fuentes a blanco para que sean visibles
    )

    fig.update_layout(xaxis=dict(showticklabels=False))
    grafico = fig.to_html(full_html=False)
    return grafico

def grafico_categoria(df):
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    ventas_por_categoria = df.groupby('Categoria')['Total'].sum().reset_index()
    fig = px.bar(
        ventas_por_categoria,
        x='Categoria',
        y='Total',
        labels={'Categoría': 'Categoría', 'Total': 'Total de Ventas'},
        color='Categoria',
        color_discrete_sequence=px.colors.qualitative.Prism ,
        height=400 # Puedes cambiar la paleta de colores

    )

    fig.update_layout(
        height=380,
        plot_bgcolor='black',  # Fondo del área del gráfico
        paper_bgcolor='black',  # Fondo del gráfico completo
        font=dict(color='white')  # Cambiar el color de las fuentes a blanco para que sean visibles
    )

    fig.update_layout(xaxis=dict(showticklabels=False))


    grafico = fig.to_html(full_html=False)
    return grafico

def grafico_sucursales(df):
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

    ventas_por_sucursal = df.groupby('Sucursal')['Total'].sum().reset_index()

    # Crear gráfico de torta con Plotly
    fig = px.pie(
        ventas_por_sucursal, 
        names='Sucursal',       
        values='Total',        
        labels={'Sucursal': 'Sucursal', 'Total': 'Total de Ventas'},
        color_discrete_sequence=px.colors.sequential.RdBu  # Esquema de color
    )

    # Añadir más configuraciones para controlar la posición del texto
    fig.update_traces(
        textposition='outside',    # Poner las etiquetas fuera del gráfico
        textinfo='label+percent'   # Mostrar nombre de la sucursal y porcentaje
    )

    # Configuración del layout
    fig.update_layout(
        height=200,
        showlegend=False,  # Mostrar leyenda con las sucursales
        # legend_title="Sucursales",  # Título de la leyenda
        # legend=dict(
        #     orientation="h",      # Leyenda horizontal debajo del gráfico
        #     yanchor="bottom",
        #     y=-0.3,
        #     xanchor="center",
        #     x=0.5
        #),
        margin=dict(t=0, b=0, l=0, r=0),  # Ajustar márgenes: reducir espacio superior e inferior
        title_y=0.55
    )

    fig.update_layout(
        plot_bgcolor='black',  # Fondo del área del gráfico
        paper_bgcolor='black',  # Fondo del gráfico completo
        font=dict(color='white')  # Cambiar el color de las fuentes a blanco para que sean visibles
    )

    fig.update_layout(xaxis=dict(showticklabels=False))

    grafico_torta_html = fig.to_html(full_html=False)
    return grafico_torta_html

def grafico_tipo_pago(df):
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    ventas_por_tipo_pago = df.groupby('Pago')['Total'].sum().reset_index()
    fig = px.pie(
        ventas_por_tipo_pago, 
        names='Pago',       
        values='Total',        
        labels={'Pago': 'Pago', 'Total': 'Total de Ventas'},
        color_discrete_sequence=px.colors.sequential.Agsunset  # Esquema de color
    )
    fig.update_layout(
        height=290,
        showlegend=True,
        legend=dict(
            orientation="h",      # Leyenda horizontal debajo del gráfico
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
    )
    fig.update_layout(
        plot_bgcolor='black',  # Fondo del área del gráfico
        paper_bgcolor='black',  # Fondo del gráfico completo
        font=dict(color='white')  # Cambiar el color de las fuentes a blanco para que sean visibles
    )

    fig.update_layout(xaxis=dict(showticklabels=False))
    grafico_torta_pago = fig.to_html(full_html=False)
    return grafico_torta_pago

def grafico_productos(df):
    ventas_por_producto = df.groupby('Producto')['Ventas'].sum()
    productos_ordenados = ventas_por_producto.sort_values(ascending=False)
    top_5_productos = productos_ordenados.head(5)
    

def venta_mes(array_mes, df):
        total_ventas = df['Total'].sum()

def format_currency(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:,.2f} millones"
    elif value >= 1_000:
        return f"{value / 1_000:,.2f} mil"
    else:
        return f"{value:,.2f}"
    
def cantidad_sucursales(df):
    return df['Sucursal'].nunique()

def meses(df):
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Mes'] = df['Fecha'].dt.month
    
    # Crear un diccionario con los nombres de los meses en español
    nombres_meses = {
        1: 'Enero', 
        2: 'Febrero', 
        3: 'Marzo', 
        4: 'Abril', 
        5: 'Mayo', 
        6: 'Junio', 
        7: 'Julio', 
        8: 'Agosto', 
        9: 'Septiembre', 
        10: 'Octubre', 
        11: 'Noviembre', 
        12: 'Diciembre'
    }
    
    df['Mes'] = df['Mes'].map(nombres_meses)
    meses_ventas = df['Mes'].unique()
    meses_ventas = sorted(meses_ventas, key=lambda x: list(nombres_meses.values()).index(x))
    return meses_ventas



@app.route('/graficos')
def upload_file1():
    if request.method == 'POST':
        # Obtener el archivo de la solicitud
        file = request.files['file']
        csv_name = request.form['csv_name']

        # Verificar que se haya seleccionado un archivo
        if file and file.filename.endswith('.xlsx'):

            # Cargar el archivo Excel en un DataFrame
            df = pd.read_excel(file)

            # Guardar el DataFrame como CSV
            csv_path = os.path.join(UPLOAD_FOLDER, f"datos.csv")
            df.to_csv(csv_path, index=False)
    
            # Calcular KPIs
            kpis = calculate_kpis(df)
            print(kpis)
            # return redirect(url_for('download_file', filename=f"{csv_name}.csv"))
            return render_template('kpis.html', kpis=kpis)


    return render_template('graficos.html')


def calculate_kpis(df):
  # Inicializa un diccionario para almacenar los KPIs
    kpis = {}

    # 1. Ventas Totales
    kpis['ventas_totales'] = df['Total'].sum()

    # 2. Ventas por Sucursal
    ventas_por_sucursal = df.groupby('Sucursal')['Total'].sum()
    kpis['ventas_por_sucursal'] = df.groupby('Sucursal')['Total'].sum()

    # 3. Promedio de Ventas por Transacción
    kpis['promedio_ventas'] = df['Total'].mean()

    # 4. Ventas por Tipo de Cliente
    ventas_por_cliente = df.groupby('Tipo Cliente')['Total'].sum()
    kpis['ventas_por_cliente'] = df.groupby('Tipo Cliente')['Total'].sum()

    # 5. Ventas por Género
    ventas_por_genero = df.groupby('Genero')['Total'].sum()
    kpis['ventas_por_genero'] = df.groupby('Genero')['Total'].sum()

    # 6. Ventas por mes
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    ventas_por_mes = df.groupby(df['Fecha'].dt.to_period('M'))['Total'].sum()
    kpis['ventas_por_mes'] = ventas_por_mes

    # 7. Ventas por categoria
    ventas_por_categoria = df.groupby('Categoria')['Total'].sum()
    kpis['ventas_por_categoria'] = ventas_por_categoria

    #crear graficos
    img_sucursal = create_bar_chart(ventas_por_sucursal, 'Ventas por Sucursal')
    img_cliente = create_bar_chart(ventas_por_cliente, 'Ventas por Tipo de Cliente')
    img_genero = create_bar_chart(ventas_por_genero, 'Ventas por Género')
    img_ventas = create_bar_chart(ventas_por_mes, 'Ventas por mes')
    img_categoria = create_bar_chart(ventas_por_categoria, 'Ventas por categoria')

    kpis['img_sucursal'] = img_sucursal
    kpis['img_cliente'] = img_cliente
    kpis['img_genero'] = img_genero
    kpis['img_ventas'] = img_ventas
    kpis['img_categoria'] = img_categoria

    return kpis
    
def create_bar_chart(data, title):
    plt.figure(figsize=(6,4))
    sns.barplot(x=data.index, y=data.values)
    ax = sns.barplot(x=data.index, y=data.values)
    plt.title(title)
    plt.ylabel('Total Ventas')
    plt.xticks(rotation=45)

    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', 
            (p.get_x() + p.get_width() / 2., p.get_height()), 
            ha = 'center', va = 'center', 
            xytext = (0, 10), 
            textcoords = 'offset points')

    # Guardar el gráfico en memoria en lugar de archivo físico
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    
    # Retornar la imagen codificada en base64
    return plot_url
