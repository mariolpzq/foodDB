# Guía de Ejecución de la API

## Introducción

Este documento proporciona instrucciones paso a paso para la configuración y ejecución de la API del sistema de información para la nutrición saludable. La API está implementada en Python utilizando el framework FastAPI y se conecta a una base de datos MongoDB.

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

   Por razones de derechos de autor, los datos necesarios para la variable de entorno `MONGODB_URL` no están incluidos en el repositorio. A pesar de que puedes ejecutar el contenedor Docker con la imagen de MongoDB, la base de datos accesible desde la URL proporcionada no contendrá la información necesaria. Deberás obtener los datos localmente y configurar tu propia instancia de MongoDB con estos datos.

   Exporta la URL de conexión a MongoDB en tu entorno:

   ```bash
   export MONGODB_URL=mongodb://mongoadmin:4qJp8wDxA7@localhost:27022/
   ```

   **Nota:** Debes configurar y cargar los datos en tu instancia local de MongoDB siguiendo las instrucciones de tu institución o proveedor de datos.

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

- Asegúrate de que el puerto `27022` en el que está ejecutándose MongoDB no esté bloqueado por un firewall u otro servicio.
- Puedes modificar la URL de conexión a MongoDB y otros parámetros de configuración según sea necesario en tu entorno de desarrollo.

## Conclusión

Siguiendo estos pasos, deberías tener la API del sistema de información para la nutrición saludable en funcionamiento en tu entorno local. Para cualquier problema o consulta, por favor revisa la documentación del proyecto o contacta al desarrollador del sistema.
