# API para consulta en la base de datos de FoodDB

Esta API proporciona endpoints para consultar la base de datos de FoodDB.

## Instalación

1. Clona este repositorio:

2. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```

3. Configura la conexión a la base de datos MongoDB. Define la variable de entorno `MONGODB_URL` con la URL de conexión.

## Uso

La API proporciona los siguientes endpoints:

### Consultar ingredientes de BEDCA

- **GET /bedca/**

  Lista todos los ingredientes de BEDCA.

- **GET /bedca/{nombre}**

  Busca un ingrediente de BEDCA por su nombre en español o inglés.

### Consultar recetas de la abuela

- **GET /abuela/**

  Lista todas las recetas de la abuela.

- **GET /abuela/{titulo}**

  Busca una receta de la abuela por su título.

### Ejecutar la aplicación

Para ejecutar la aplicación, utiliza el siguiente comando:

```bash
uvicorn app:app --reload
