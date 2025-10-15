import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import requests


def create_app(test_config=None):
    # Crear la app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Crear carpeta instance si no existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Lista global para guardar tareas
    tareas = []

    # Ruta de prueba
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Página principal con el formulario
    @app.route('/')
    def index():
        clima = obtener_clima()
        return render_template('index.html', clima=clima)

    # Ruta para guardar tarea
    @app.route('/guardar_tarea', methods=['POST'])
    def guardar_tarea():
        actividad = request.form.get('act')
        descripcion = request.form.get('descripcion')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')

        if not actividad or not fecha or not hora:
            return redirect(url_for('index'))

        pronostico = obtener_pronostico(fecha, hora)
        sugerir_cambio = False
        if pronostico:
            if pronostico['temperatura'] > 28 or pronostico['lluvia']:
                sugerir_cambio = True

        # Calcular el momento para mostrar el modal (una hora antes)
        dt_tarea = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
        mostrar_modal_desde = (dt_tarea - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")

        tarea = {
            'actividad': actividad,
            'descripcion': descripcion,
            'fecha': fecha,
            'hora': hora,
            'sugerir_cambio': sugerir_cambio,
            'pronostico': pronostico,
            'mostrar_modal_desde': mostrar_modal_desde
        }

        tareas.append(tarea)
        print(tareas)
        return redirect(url_for('mostrar_tareas'))

    # Ruta para mostrar tareas
    @app.route('/tareas')
    def mostrar_tareas():
        ahora = datetime.now()
        tareas_vigentes = []
        for tarea in tareas:
            if tarea['fecha'] and tarea['hora']:
                dt_tarea = datetime.strptime(tarea['fecha'] + " " + tarea['hora'], "%Y-%m-%d %H:%M")
                if dt_tarea >= ahora:
                    tareas_vigentes.append({
                        **tarea,
                        'dt_tarea': dt_tarea.strftime("%Y-%m-%d %H:%M")
                    })
        tareas[:] = tareas_vigentes

        clima = obtener_clima() or {'temperatura': 0, 'descripcion': '', 'icono': '01d'}

        return render_template('tareas.html', tareas=tareas, clima=clima, ahora=ahora.strftime("%Y-%m-%dT%H:%M"))


    def obtener_clima():
        api_key = '3b42af71dd4826a84dee8cfb65d4fe82'
        ciudad = 'Querétaro,MX'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            clima = {
                'descripcion': data['weather'][0]['description'],
                'temperatura': round(data['main']['temp']),
                'icono': data['weather'][0]['icon']
            }
            return clima
        else:
            return None

    def obtener_pronostico(fecha, hora):
        api_key = '3b42af71dd4826a84dee8cfb65d4fe82'
        ciudad = 'Querétaro,MX'
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={ciudad}&appid={api_key}&units=metric&lang=es'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            objetivo = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            pronostico_cercano = None
            min_diferencia = None
            for item in data['list']:
                dt_item = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
                diferencia = abs((dt_item - objetivo).total_seconds())
                if min_diferencia is None or diferencia < min_diferencia:
                    min_diferencia = diferencia
                    pronostico_cercano = item
            if pronostico_cercano:
                temp = pronostico_cercano['main']['temp']
                lluvia = 'rain' in pronostico_cercano and pronostico_cercano['rain'].get('3h', 0) > 0
                return {
                    'temperatura': temp,
                    'lluvia': lluvia,
                    'descripcion': pronostico_cercano['weather'][0]['description']
                }
            
    @app.route('/modificar_tarea/<int:idx>', methods=['POST'])
    def modificar_tarea(idx):
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        if 0 <= idx < len(tareas):
            tareas[idx]['fecha'] = fecha
            tareas[idx]['hora'] = hora
            # Recalcular pronóstico y sugerir_cambio
            pronostico = obtener_pronostico(fecha, hora)
            tareas[idx]['pronostico'] = pronostico
            tareas[idx]['sugerir_cambio'] = pronostico and (pronostico['temperatura'] > 28 or pronostico['lluvia'])
            # Recalcular mostrar_modal_desde si lo usas
            dt_tarea = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            tareas[idx]['mostrar_modal_desde'] = (dt_tarea - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M")
        return redirect(url_for('mostrar_tareas'))

    return app
    #return None


