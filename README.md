# SISTEMA DE INFORMACIÓN PARA NUTRICIÓN SALUDABLE

## Trabajo de Fin de Grado - Grado en Ingeniería Informática - Universidad de Granada

**Alumno:** Mario López Quesada  
**Directoras:** Maria José Martín Bautista y Andrea Morales Garzón

---

### Resumen

Este trabajo presenta el diseño y desarrollo de un sistema de información multilingüe orientado a la gestión y elaboración de dietas saludables personalizadas, con un enfoque adicional en las emisiones ambientales y los sabores de los alimentos. La creciente preocupación de la población por llevar una alimentación saludable, el impacto ambiental de la producción alimentaria, y la falta de acceso a información nutricional detallada y precisa motivaron la creación de este proyecto: un sistema que integra datos nutricionales de múltiples fuentes, tanto de recetas como de ingredientes, utilizando técnicas avanzadas de procesamiento del lenguaje natural (NLP) para el mapeo y la homogeneización de datos, y cuya consecución ha requerido una labor intensiva de tratamiento de datos.

La plataforma desarrollada permite a los usuarios, desde individuos comunes hasta profesionales de la nutrición e investigadores, consultar y gestionar dietas de manera eficiente y precisa. A través de una interfaz web sencilla e intuitiva, los usuarios pueden acceder a una amplia variedad de información nutricional, crear y gestionar dietas personalizadas, y evaluar la calidad nutricional de los alimentos según los indicadores establecidos por instituciones reconocidas como la Organización Mundial de la Salud (OMS).

El sistema también facilita la comparación de alimentos y recetas en términos de sus características nutricionales, su impacto ambiental y su sabor, fomentando una alimentación más saludable y sostenible. Las conclusiones destacan la capacidad del sistema para homogeneizar datos nutricionales diversos y su potencial para futuras ampliaciones que incluyan más nutrientes y mejoren los semáforos nutricionales.

---

### Estructura del repositorio

```
foodDB/
├── db-api/
│   ├── app.py
│   ├── auth.py
│   ├── models.py
│   └── ...
│
├── db-scripts/
│   ├── scripts ingredientes/
│   ├── scripts recetas/
│   └── mapeos/
│
└── fooddb-app/
    ├── node_modules/
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── App.js
    │   ├── App.css
    │   ├── Auth.js
    │   ├── index.js
    │   └── ...
    ├── .gitignore
    ├── README.md
    ├── package.json
    └── package-lock.json
```

#### Descripción de las carpetas

- **db-api:** Contiene la implementación de la API del sistema. Por razones de derechos de autor, los datos necesarios para la variable de entorno `MONGODB_URL` no están incluidos en el repositorio. A pesar de que puedes ejecutar el contenedor Docker con la imagen de MongoDB, la base de datos accesible desde la URL proporcionada no contendrá la información necesaria. Deberás obtener los datos localmente y configurar tu propia instancia de MongoDB con estos datos. Para más detalles sobre la configuración y ejecución de la API, consulta este [README](/db-api/README.md).
- **db-scripts:** Contiene los scripts utilizados para la carga y gestión de datos del sistema, categorizados en:
  - **scripts ingredientes:** Scripts relacionados con las colecciones de ingredientes.
  - **scripts recetas:** Scripts relacionados con las colecciones de recetas.
  - **mapeos:** Contiene los scripts de mapeo de atributos entre colecciones. Supusieron la antesala al microservicio de mapeos implementado en la API.
- **fooddb-app:** Contiene el código de la aplicación del sistema. Para más detalles sobre la instalación y ejecución de la aplicación, consulta este [README](/fooddb-app/README.md).

