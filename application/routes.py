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

from application import functions

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
        # Inicializa el dashboard con los datos del archivo
        dashboard_data = functions.init_dashboard(request)

        # Renderiza el template del dashboard y pasa los datos
        return render_template('dashboard.html', **dashboard_data)
    
    # Si es una solicitud GET, puede devolver la página de subida de archivo o un error
    return render_template('upload_file.html')

@app.route('/filtrar',  methods=['GET', 'POST'])
def filtrar():    
    # Obtener los meses seleccionados del formulario
    months_seleted = request.form.getlist('meses')

    # Verificar si se seleccionaron meses
    if not months_seleted:
        return redirect(url_for('upload_file'))

    dashboard_filter= functions.filter_by_time(months_seleted,'datos.csv')
    return render_template('dashboard.html', **dashboard_filter)
    # Filtrar el DataFrame por los meses seleccionados
    # df = pd.read_csv(os.path.join(UPLOAD_FOLDER, 'datos.csv'))  # Reemplaza con el nombre de tu archivo CSV guardado
    # df['Fecha'] = pd.to_datetime(df['Fecha'])
    
    # # Diccionario de nombres de meses en español
    # nombres_meses = {
    #     1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 
    #     6: 'Junio', 7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 
    #     10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    # }
    
    # # Añadir la columna de nombre del mes
    # df['Mes'] = df['Fecha'].dt.month.map(nombres_meses)
    
    # # Filtrar el DataFrame por los meses seleccionados
    # df_filtrado = df[df['Mes'].isin(meses_seleccionados)]

    # # Actualizar los gráficos con los datos filtrados
    # graph_html_total_ventas = totalVentas(df_filtrado)
    # graph_html_total_costos = total_costo(df_filtrado)
    # graph_html_total_ingreso = total_ingreso(df_filtrado)
    # grafico_categ = grafico_categoria(df_filtrado)    
    # cant_sucursales = cantidad_sucursales(df)
    # grafico_suc = grafico_sucursales(df_filtrado)
    # grafico_pago = grafico_tipo_pago(df_filtrado)
    # grafico_hora = grafico_ventas_hora(df_filtrado)
    # meses_ventas = meses(df)


    # return render_template('dashboard.html',
    #                        graph_html_total_ventas=graph_html_total_ventas,
    #                        graph_html_total_costos=graph_html_total_costos,
    #                        graph_html_total_ingreso=graph_html_total_ingreso,
    #                        grafico_categ=grafico_categ,
    #                        grafico_suc=grafico_suc,
    #                        grafico_pago=grafico_pago,
    #                        grafico_hora=grafico_hora,
    #                        cant_sucursales=cant_sucursales,
    #                        meses_ventas=meses_ventas)


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
