# Guía de ejecución de la API

## Introducción

Este documento proporciona instrucciones paso a paso para la configuración y ejecución de la API del nuestro sistema de información para nutrición saludable. La API está implementada en Python utilizando el framework FastAPI y se conecta a una base de datos MongoDB.

## Requisitos Previos

Antes de iniciar la API, asegúrate de tener instalados los siguientes componentes:

- Python 3.7 o superior
- pip (gestor de paquetes de Python)
- MongoDB
- uvicorn

## Instalación

1. **Clonar el repositorio**

   Clona el repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tu_usuario/foodDB.git
   cd foodDB/db-api
   ```

2. **Crear un entorno virtual**

   Es recomendable crear un entorno virtual para gestionar las dependencias:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. **Instalar las dependencias**

   Instala las dependencias necesarias para ejecutar la API:

   ```bash
   pip install -r requirements.txt
   ```

## Configuración

1. **Configurar la conexión a MongoDB**

   Exporta la URL de conexión a MongoDB en tu entorno. Asegúrate de tener MongoDB en ejecución y accesible en la URL especificada:

   ```bash
   export MONGODB_URL=mongodb://...
   ```

## Ejecución de la API

Para iniciar la API, ejecuta el siguiente comando en tu terminal:

```bash
uvicorn app:app --reload
```

Este comando iniciará el servidor de desarrollo de FastAPI con la recarga automática habilitada. La API estará disponible en `http://127.0.0.1:8000`.

## Verificación

Para verificar que la API está funcionando correctamente, puedes acceder a la documentación interactiva generada automáticamente por FastAPI en:

- Documentación Swagger: `http://127.0.0.1:8000/docs`
- Documentación Redoc: `http://127.0.0.1:8000/redoc`

## Notas Adicionales

- Puedes modificar la URL de conexión a MongoDB y otros parámetros de configuración según sea necesario en tu entorno de desarrollo.