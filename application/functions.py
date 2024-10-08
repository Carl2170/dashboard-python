from application import app
from flask import render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt

import plotly.express as px
import plotly.graph_objs as go
import plotly.io as pio
import os

# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField

#Direccion de directorio donde se guardarán los archivos subidos
UPLOAD_FOLDER = 'application/uploads'

def process_file(request):
    """
    Función para el proceso del archivo (Excel, csv)

    Parámetros:
    request : flask.Request
    Retorna:
        Retorna el contenido del archivo Excel o CSV en un DataFrame para su posterior uso.

    """
    if request.method == 'POST':
        file = request.files['file']
        csv_name = request.form['csv_name']
        csv_path = os.path.join(UPLOAD_FOLDER, f"{csv_name}.csv")

        if verif_file_xlsx(file):
            df = pd.read_excel(file)
            df.to_csv(csv_path, index=False) 
        else:
            df = pd.read_csv(file)
    return df                  

def verif_file_xlsx(file):    
    return file and file.filename.endswith('.xlsx') 


def init_dashboard(request):
    """
    Esta función procesa un archivo subido a través de la solicitud HTTP y genera un conjunto de datos 
    clave y gráficos que serán utilizados para mostrar un dashboard interactivo.

    Parámetros:
    request : flask.Request
        El objeto `request` que contiene el archivo cargado por el usuario. Se asume que el archivo  
        contiene datos del supermercado, como ventas, costos, categorías, sucursales, etc.
    
    Retorna:
        Un diccionario que contiene los siguientes datos clave y gráficos:
        
        - 'sales_total': float
            El total de las ventas calculado a partir del archivo CSV.
        
        - 'cost_total': float
            El costo total de las operaciones del supermercado calculado a partir del archivo CSV.
        
        - 'utility': float
            El ingreso bruto (o utilidad) calculado como la diferencia entre las ventas totales y los 
            costos totales.
        
        - 'number_branch': int
            El número total de sucursales del supermercado presentes en el archivo CSV.
        
        - 'number_months': list[str]
            Una lista de los nombres de los meses que aparecen en el archivo CSV para las ventas. Estos 
            meses se utilizarán para filtrados y gráficos por tiempo.
        
        - 'cate_graph': str (HTML gráfico)
            Un gráfico HTML que muestra la distribución de las ventas por categoría de productos.
        
        - 'branch_graph': str (HTML gráfico)
            Un gráfico HTML que muestra las ventas por cada sucursal.
        
        - 'type_payment_graph': str (HTML gráfico)
            Un gráfico HTML que muestra el desglose de las ventas por tipo de pago (efectivo, tarjeta, etc.).
        
        - 'hour_graph': str (HTML gráfico)
            Un gráfico HTML que muestra las horas más concurridas para las ventas del supermercado.
    """
  
    df=process_file(request)
    sales_total= total_sales(df)
    cost_total= total_cost(df)
    utility= total_ingr(df)
    number_branch= number_branches(df)
    number_months= list_months(df)

    #graficos
    cate_graph= graph_categories(df)
    branch_graph= graph_branches(df)
    type_payment_graph= graph_type_payment(df)
    hour_graph= graph_sales_hours(df)

    # Devuelve los datos para ser usados en la plantilla
    return {
        'sales_total': sales_total,
        'cost_total': cost_total,
        'utility': utility,
        'number_branch': number_branch,
        'number_months': number_months,
        'cate_graph': cate_graph,
        'branch_graph': branch_graph,
        'type_payment_graph': type_payment_graph,
        'hour_graph': hour_graph
    }
  
def filter_by_time(months, name_document):
    """
    Realiza un filtro de datos a traves de meses seleccionados en el dashboard.

    Parámetros:
    value (months): Conjunto de meses seleccionados.
    Retorna:
     Un diccionario basado en un Dataframe filtrado, que contiene los siguientes datos clave y gráficos:
        
        - 'sales_total': float
            El total de las ventas calculado a partir del archivo CSV.
        
        - 'cost_total': float
            El costo total de las operaciones del supermercado calculado a partir del archivo CSV.
        
        - 'utility': float
            El ingreso bruto (o utilidad) calculado como la diferencia entre las ventas totales y los 
            costos totales.
        
        - 'number_branch': int
            El número total de sucursales del supermercado presentes en el archivo CSV.
        
        - 'number_months': list[str]
            Una lista de los nombres de los meses que aparecen en el archivo CSV para las ventas. Estos 
            meses se utilizarán para filtrados y gráficos por tiempo.
        
        - 'cate_graph': str (HTML gráfico)
            Un gráfico HTML que muestra la distribución de las ventas por categoría de productos.
        
        - 'branch_graph': str (HTML gráfico)
            Un gráfico HTML que muestra las ventas por cada sucursal.
        
        - 'type_payment_graph': str (HTML gráfico)
            Un gráfico HTML que muestra el desglose de las ventas por tipo de pago (efectivo, tarjeta, etc.).
        
        - 'hour_graph': str (HTML gráfico)
            Un gráfico HTML que muestra las horas más concurridas para las ventas del supermercado.
    
    """
    # Reemplaza con el nombre de tu archivo CSV guardado
    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, 'datos.csv'))  
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    name_months = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 
        6: 'Junio', 7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 
        10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    # Añadir la columna de nombre del mes
    df['Mes'] = df['Fecha'].dt.month.map(name_months)
    df_filter = df[df['Mes'].isin(months)]

    sales_total= total_sales(df_filter)
    cost_total= total_cost(df_filter)
    utility= total_ingr(df_filter)
    number_branch= number_branches(df)
    number_months= list_months(df)

    #graficos
    cate_graph= graph_categories(df_filter)
    branch_graph= graph_branches(df_filter)
    type_payment_graph= graph_type_payment(df_filter)
    hour_graph= graph_sales_hours(df_filter)

    # Devuelve los datos para ser usados en la plantilla
    return {
        'sales_total': sales_total,
        'cost_total': cost_total,
        'utility': utility,
        'number_branch': number_branch,
        'number_months': number_months,
        'cate_graph': cate_graph,
        'branch_graph': branch_graph,
        'type_payment_graph': type_payment_graph,
        'hour_graph': hour_graph
    }
    
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

def number_branches(df): 
    """
    Calcula la cantidad de sucursales únicas en un DataFrame.

    Parámetros:
    df (pandas.DataFrame): El DataFrame que contiene la información de las sucursales. 
                           Se espera que haya una columna llamada 'Sucursal'.

    Retorna:
    int: El número de sucursales únicas en el DataFrame.
    """
    return df['Sucursal'].nunique()

def list_months(df):
    """
    Extrae y devuelve los nombres de los meses presentes en un DataFrame, ordenados cronológicamente.

    Parámetros:
    df (pandas.DataFrame): El DataFrame que contiene una columna llamada 'Fecha' con valores de fecha.

    Retorna:
    list: Una lista de los nombres de los meses presentes en el DataFrame, en orden cronológico (de enero a diciembre).

    """
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df['Mes'] = df['Fecha'].dt.month
    
    # Crear un diccionario con los nombres de los meses en español
    name_month = {
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
    
    df['Mes'] = df['Mes'].map(name_month)
    sales_month = df['Mes'].unique()
    sales_month = sorted(sales_month, key=lambda x: list(name_month.values()).index(x))
    return sales_month

def total_sales(df):
    """
    Calcula el total de ventas y lo devuelve en un formato legible (miles o millones).

    Parámetros:
    df (pandas.DataFrame): El DataFrame que contiene una columna 'Total' con los valores de las ventas.

    Retorna:
    str: El total de ventas, formateado en miles o millones, dependiendo del valor.
    """
    total_sales = df['Total'].sum()
    total_sales_formatted = format_currency(total_sales )
    return total_sales_formatted

def total_cost(df):
    """
    Calcula el total de los costos y lo devuelve en un formato legible (miles o millones).

    Parámetros:
    df (pandas.DataFrame): El DataFrame que contiene una columna 'Costo de Bienes Vendidos' con los valores de las ventas.

    Retorna:
    str: El total de costos, formateado en miles o millones, dependiendo del valor.
    """
    total= df['Costo de Bienes Vendidos'].sum()
    #total_ventas_formateado = f"${total_ventas:,.2f}"
    total_cost_formatted = format_currency(total)
    return total_cost_formatted

def total_ingr(df):
    total_ingr = df['Ingreso Bruto'].sum()
    total_ingr_formatted=format_currency(total_ingr)
    return total_ingr_formatted

#Graficos

def graph_categories(df):
    """
    Genera un gráfico de barras de las ventas totales agrupadas por categoría.
    
    Parámetros:
    df (pd.DataFrame): Un DataFrame de pandas que contiene los datos de ventas, 
                       con una columna llamada 'Total' que representa el total de ventas
                       y una columna 'Categoria' que indica la categoría de las ventas.

    Retorna:
    str: Un gráfico de barras en formato HTML generado con plotly.                       

    """
    #Convierte la columna 'Total' a un tipo numérico para asegurarse de que los valores sean números.
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

    #Agrupa los datos por la columna 'Categoria' y suma los valores de la columna 'Total' para cada categoría.
    sales_by_category = df.groupby('Categoria')['Total'].sum().reset_index()

    # Generación del gráfico de barras
    fig = px.bar(
        sales_by_category,
        x='Categoria',
        y='Total',
        labels={'Categoría': 'Categoría', 'Total': 'Total de Ventas'},
        color='Categoria',
        color_discrete_sequence=px.colors.qualitative.Prism ,
        height=400 
    )

    # Configuración de diseño
    fig.update_layout(
        height=380,
        plot_bgcolor='black', 
        paper_bgcolor='black', 
        font=dict(color='white')  
    )

    # Ocultar etiquetas del eje X
    fig.update_layout(xaxis=dict(showticklabels=False))

    # Convertir el gráfico a HTML
    graph = fig.to_html(full_html=False)
    
    return graph

def graph_branches(df):
    """
    Genera un gráfico de torta de las ventas totales agrupadas por sucursales.
    
    Parámetros:
    df (pd.DataFrame): Un DataFrame de pandas que contiene los datos de ventas, 
                       con una columna llamada 'Total' que representa el total de ventas
                       y una columna 'Sucursal' que indica la sucursal de las ventas.

    Retorna:
    str: Un gráfico de torta en formato HTML generado con plotly.                       
    """
    #Convierte la columna 'Total' a un tipo numérico para asegurarse de que los valores sean números.
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

    #Agrupa los datos por la columna 'Sucursal' y suma los valores de la columna 'Total' para cada sucursal.
    sales_by_branches = df.groupby('Sucursal')['Total'].sum().reset_index()
    
    # Generación del gráfico de torta
    fig = px.pie(
        sales_by_branches, 
        names='Sucursal',       
        values='Total',        
        labels={'Sucursal': 'Sucursal', 'Total': 'Total de Ventas'},
        color_discrete_sequence=px.colors.sequential.RdBu  # Esquema de color
    )

    # Añadir más configuraciones para controlar la posición del texto
    fig.update_traces(
        textposition='outside',    
        textinfo='label+percent' 
    )

    # Configuración de diseño
    fig.update_layout(
        height=200,
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),  # Ajustar márgenes: reducir espacio superior e inferior
        title_y=0.55,
        plot_bgcolor='black', 
        paper_bgcolor='black',
        font=dict(color='white')
    )

    fig.update_layout(xaxis=dict(showticklabels=False))
    
    # Convertir el gráfico a HTML
    grafico_torta_html = fig.to_html(full_html=False)

    return grafico_torta_html

def graph_type_payment(df):
    """
    Genera un gráfico de torta de las ventas totales agrupadas por tipo de pago.
    
    Parámetros:
    df (pd.DataFrame): Un DataFrame de pandas que contiene los datos de ventas, 
                       con una columna llamada 'Total' que representa el total de ventas
                       y una columna 'Pago' que indica el tipo de pago de las ventas.

    Retorna:
    str: Un gráfico de torta en formato HTML generado con plotly.   
    """

    #Convierte la columna 'Total' a un tipo numérico para asegurarse de que los valores sean números.
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')

    #Agrupa los datos por la columna 'Pago' y suma los valores de la columna 'Total' para cada tipo de pago.
    ventas_por_tipo_pago = df.groupby('Pago')['Total'].sum().reset_index()
    
    # Generación del gráfico de torta
    fig = px.pie(
        ventas_por_tipo_pago, 
        names='Pago',       
        values='Total',        
        labels={'Pago': 'Pago', 'Total': 'Total de Ventas'},
        color_discrete_sequence=px.colors.sequential.Agsunset  # Esquema de color
    )

    # Configuración de diseño
    fig.update_layout(
        height=290,
        showlegend=True,
        legend=dict(
            orientation="h",  
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        plot_bgcolor='black',
        paper_bgcolor='black',  
        font=dict(color='white') 
    )

    fig.update_layout(xaxis=dict(showticklabels=False))

    # Convertir el gráfico a HTML
    grafico_torta_pago = fig.to_html(full_html=False)
    
    return grafico_torta_pago

def graph_sales_hours(df):
    """
    Genera un gráfico de barras que muestra la cantidad de compras agrupadas por hora del día.

    Parámetros:
    df (pd.DataFrame): Un DataFrame de pandas que contiene los datos de compras. 
                       Debe tener una columna 'Total' con los valores de las ventas y 
                       una columna 'Hora' con el formato de hora '%H:%M' (por ejemplo, '14:30').

    Retorna:
    str: Un gráfico de barras en formato HTML generado con plotly.
    """
    #Convierte la columna 'Total' a un tipo numérico para asegurarse de que los valores sean números.   
    df['Total'] = pd.to_numeric(df['Total'], errors='coerce')
    
    # Convertir la columna 'Hora' a tipo datetime (manejo de errores con NaN)
    df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce', format='%H:%M')

    # Extraer la hora del día de la columna 'Hora'
    df['Hora Dia'] = df['Hora'].dt.hour

    # Contar el número de compras por cada hora del día y ordenar por la hora
    sales_by_hour = df['Hora Dia'].value_counts().sort_index()

    # Crear gráfico de barras
    fig = px.bar(sales_by_hour, 
             x=sales_by_hour.index, 
             y=sales_by_hour.values, 
             labels={'x': 'Hora del Día', 'y': 'Número de Compras'})

    # Configurar el diseño del gráfico
    fig.update_layout(
        width=255,
        height=250,
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white') 
    )

    # Ocultar las etiquetas del eje X
    fig.update_layout(xaxis=dict(showticklabels=False))

    # Convertir el gráfico a HTML y retornarlo
    grafico = fig.to_html(full_html=False)
    
    return grafico

