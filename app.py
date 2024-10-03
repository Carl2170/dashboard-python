
# from flask import Flask,render_template, request,redirect,url_for, send_from_directory
# import pandas as pd
# import os
# import matplotlib.pyplot as plt
# import seaborn as sns
# from io import BytesIO
# import base64

# from utils import hello

# app = Flask(__name__)

# # @app.route('/')
# # def hello():
# # 	return 'Hola mundo'

# # Ruta para guardar los archivos CSV
# UPLOAD_FOLDER = 'uploads'
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # Obtener el archivo de la solicitud
#         file = request.files['file']
#         csv_name = request.form['csv_name']

#         # Verificar que se haya seleccionado un archivo
#         if file and file.filename.endswith('.xlsx'):

#             # Cargar el archivo Excel en un DataFrame
#             df = pd.read_excel(file)

#             # Guardar el DataFrame como CSV
#             csv_path = os.path.join(UPLOAD_FOLDER, f"{csv_name}.csv")
#             df.to_csv(csv_path, index=False)
    
#             # Calcular KPIs
#             kpis = calculate_kpis(df)
#             print(kpis)
#             # return redirect(url_for('download_file', filename=f"{csv_name}.csv"))
#             return render_template('kpis.html', kpis=kpis)


#     return render_template('index.html')


# def calculate_kpis(df):
#   # Inicializa un diccionario para almacenar los KPIs
#     kpis = {}

#     # 1. Ventas Totales
#     kpis['ventas_totales'] = df['Total'].sum()

#     # 2. Ventas por Sucursal
#     ventas_por_sucursal = df.groupby('Sucursal')['Total'].sum()
#     kpis['ventas_por_sucursal'] = df.groupby('Sucursal')['Total'].sum()

#     # 3. Promedio de Ventas por Transacción
#     kpis['promedio_ventas'] = df['Total'].mean()

#     # 4. Ventas por Tipo de Cliente
#     ventas_por_cliente = df.groupby('Tipo Cliente')['Total'].sum()
#     kpis['ventas_por_cliente'] = df.groupby('Tipo Cliente')['Total'].sum()

#     # 5. Ventas por Género
#     ventas_por_genero = df.groupby('Genero')['Total'].sum()
#     kpis['ventas_por_genero'] = df.groupby('Genero')['Total'].sum()

#     # 6. Ventas por mes
#     df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

#     ventas_por_mes = df.groupby(df['Fecha'].dt.to_period('M'))['Total'].sum()
#     kpis['ventas_por_mes'] = ventas_por_mes

#     # 7. Ventas por categoria
#     ventas_por_categoria = df.groupby('Categoria')['Total'].sum()
#     kpis['ventas_por_categoria'] = ventas_por_categoria

#     #crear graficos
#     img_sucursal = create_bar_chart(ventas_por_sucursal, 'Ventas por Sucursal')
#     img_cliente = create_bar_chart(ventas_por_cliente, 'Ventas por Tipo de Cliente')
#     img_genero = create_bar_chart(ventas_por_genero, 'Ventas por Género')
#     img_ventas = create_bar_chart(ventas_por_mes, 'Ventas por mes')
#     img_categoria = create_bar_chart(ventas_por_categoria, 'Ventas por categoria')

#     kpis['img_sucursal'] = img_sucursal
#     kpis['img_cliente'] = img_cliente
#     kpis['img_genero'] = img_genero
#     kpis['img_ventas'] = img_ventas
#     kpis['img_categoria'] = img_categoria

#     return kpis
    
# def create_bar_chart(data, title):
#     plt.figure(figsize=(6,4))
#     sns.barplot(x=data.index, y=data.values)
#     ax = sns.barplot(x=data.index, y=data.values)
#     plt.title(title)
#     plt.ylabel('Total Ventas')
#     plt.xticks(rotation=45)

#     for p in ax.patches:
#         ax.annotate(f'{p.get_height():.2f}', 
#             (p.get_x() + p.get_width() / 2., p.get_height()), 
#             ha = 'center', va = 'center', 
#             xytext = (0, 10), 
#             textcoords = 'offset points')

#     # Guardar el gráfico en memoria en lugar de archivo físico
#     img = BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plot_url = base64.b64encode(img.getvalue()).decode('utf8')
#     plt.close()
    
#     # Retornar la imagen codificada en base64
#     return plot_url


# @app.route('/downloads/<filename>')
# def download_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


