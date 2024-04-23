# Scripts para la base de datos

Este repositorio contiene los scripts para la gestión de datos relacionados con ingredientes, compuestos, emisiones y recetas. Aquí se detalla el proceso para incluir la información de los diferentes datasets utilizando los scripts proporcionados.

La ejecución de los scripts se ha realizado con el comando **python ./script.py**.

## Ingredientes, compuestos químicos y emisiones

En la carpeta "scripts_ingredientes" se ubica todo lo necesario para almacenar la información de los *datasets* de ingredientes, además de los de compuestos y emisiones. Para ello, encontramos tanto los scripts como carpetas que contienen los archivos .csv con la información de cada *dataset*. El orden recomendado de ejecución de los scripts es el siguiente:

1. bedca.py: script para incluir el *dataset* de BEDCA en una colección llamada "bedca".
2. cofid.py: script para incluir el *dataset* de CoFID en una colección llamada "cofid".
3. fdc.py: script para incluir el *dataset* de Food Data Central en una colección llamada "fdc".
4. emissions.py: script para incluir el *dataset* de Environment Impact of Food Production en una colección llamada "emissions".
5. compounds.py: script para incluir el *dataset* del FlavorNetwork en una colección llamada "compounds".
6. compounds_ingredients.py: este script es el que se usa para relacionar la información de los compuestos (colección "compounds") con una colección de ingredientes. Para determinar cuál es la colección de ingredientes que se quiere actualizar para incluir la información sobre los compuestos químicos se puede cambiar el valor de la variable *ingredientes* en la línea 10 del script.

Cabe destacar que los nombres de las colecciones pueden personalizarse ajustando las variables correspondientes en cada uno de los scripts. En caso de desear combinar toda la información de ingredientes disponible, simplemente basta con utilizar el mismo nombre de colección al ejecutar los primeros tres scripts. De este modo, se creará una colección que contendrá la información de los tres datasets combinados. Posteriormente, esta colección puede ser procesada con el script número 6 para complementarla con información sobre compuestos químicos.

## Recetas

En la carpeta "scripts_recetas" encontramos todos los elementos necesarios para gestionar la información de los *datasets* de recetas, incluyendo tanto los scripts como las carpetas que contienen los archivos .csv o .json correspondientes a cada dataset. A continuación, se enumeran los scripts disponibles en el orden recomendado de ejecución:

1. abuela.py: script para incluir el *dataset* de Recetas de la Abuela en una colección llamada "abuela".
2. recipeQA.py: script para incluir el *dataset* de RecipeQA en una colección llamada "recipeQA".
3. recipe1m_originals.py: script diseñado para incorporar las recetas originales del conjunto de datos Recipe1M. Es importante destacar que estas recetas conservan el texto de los ingredientes en su estado original, lo que implica que incluyen cantidades y unidades dentro del propio texto. Esta información será necesaria para ejecutar el script 4.
4. recipe1m.py: script para incluir el *dataset* de Recipe1M en una colección llamada "recipe1m". Este script realiza una búsqueda en la colección "recipe1m_originals", por lo que es necesario haber ejeucutado recipe1m_originals.py previamente.
5. foodcom_interactions.py: script para incluir la información sobre interacciones de usuarios con recetas de Food.com en una colección llamada "food.com_inteactions". La inclusión de esta colección tiene como objetivo que sea más rápido añadir las interacciones a las recetas al ejecutar el script siguiente.
6. foodcom.py: script para incluir el *dataset* de Food.com en una colección llamada "food.com". Este script realiza una búsqueda en la colección "food.com_interactions", por lo que es necesario haber ejecutado el script 5 previamente.
7. mealREC.py: script para incluir el *dataset* de MealREC en una colección llamada "mealrec".
8. recipeNLG.py: script para incluir el *dataset* de RecipeNLG en una colección llamada "recipenlg".

---

En cada una de las carpetas, además de los scripts, se incluye un archivo .txt que describe el esquema al que se ajusta la información de los diferentes datasets. Estos archivos proporcionan una guía sobre la estructura de los datos, aunque pueden haber variaciones debido al tratamiento específico de cada conjunto de datos.
