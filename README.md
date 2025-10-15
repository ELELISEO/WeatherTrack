# Proyecto 2: Gestor de Tareas al Aire Libre con Clima

Aplicación web para gestionar tareas al aire libre, que te sugiere cambiar la hora o el día de la tarea si el clima es adverso (temperatura alta o lluvia) usando Flask y la API de OpenWeatherMap.

## Características

- Agrega tareas con fecha y hora.
- Consulta el pronóstico del clima para la hora de la tarea.
- Si el clima es adverso (lluvia o temperatura mayor a 28°C), se muestra un aviso y puedes modificar la hora o el día.
- Interfaz con Tailwind CSS.
- Modal para sugerir cambios en tareas con mal clima.

## Instalación

1. **Clona el repositorio**
   ```sh
   git clone <URL_DEL_REPOSITORIO>
   ```

2. **Abre PowerShell o CMD como administrador**

3. **Navega a la carpeta del proyecto**
   ```sh
   cd c:\exmaple\example\myproject
   ```

4. **Crea y activa un entorno virtual**
   ```sh
   python -m venv venv
   .\venv\Scripts\activate
   ```

5. **Instala las dependencias**
   ```sh
   pip install flask requests
   ```

6. **Configura la variable de entorno para Flask**
   - En CMD:
     ```sh
     set FLASK_APP=flaskr:create_app
     ```
   - En PowerShell:
     ```sh
     $env:FLASK_APP="flaskr:create_app"
     ```

7. **Inicia la aplicación**
   ```sh
   flask run
   ```
8. **Inicia Tailwind CSS**
    ```sh
   npx @tailwindcss/cli -i ./src/input.css -o ./flaskr/static/css/output.css --watch
   ```

8. **Abre tu navegador en**
   ```
   http://127.0.0.1:5000/
   ```

## Uso

- Agrega una tarea con fecha y hora.
- Si el clima es adverso para esa hora, aparecerá un aviso y podrás cambiar la hora o el día.
- Consulta todas tus tareas y sugiere cambios si el clima lo requiere.

## Estructura del Proyecto

```
myproject/
│
├── flaskr/
│   ├── __init__.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── tareas.html
│   │   └── componentes/
│   │       └── card.html
│   └── static/
│       └── css/
│           └── output.css
├── instance/
│   └── flaskr.sqlite
└── readme.md
```

## Créditos

- [Flask](https://flask.palletsprojects.com/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Tailwind CSS](https://tailwindcss.com/)

---
