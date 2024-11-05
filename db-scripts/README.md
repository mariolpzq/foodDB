# Database Scripts

This repository contains scripts for managing data related to ingredients, compounds, emissions, and recipes. Here, the process for including information from different datasets using the provided scripts is detailed.

Scripts are executed using the command **python ./script.py**.

## Ingredients, Chemical Compounds, and Emissions

In the "scripts_ingredientes" folder, you will find everything needed to store information from the ingredients datasets, as well as compounds and emissions datasets. Here, we have both the scripts and folders containing the .csv files with the information for each dataset. The recommended order for executing the scripts is as follows:

1. bedca.py: script to include the BEDCA dataset in a collection called "bedca".
2. cofid.py: script to include the CoFID dataset in a collection called "cofid".
3. fdc.py: script to include the Food Data Central dataset in a collection called "fdc".
4. emissions.py: script to include the Environmental Impact of Food Production dataset in a collection called "emissions".
5. compounds.py: script to include the FlavorNetwork dataset in a collection called "compounds".
6. compounds_ingredients.py: this script is used to relate the compounds information (collection "compounds") with an ingredient collection. To determine which ingredient collection you want to update to include the chemical compounds information, you can change the value of the *ingredientes* variable in line 10 of the script.

It should be noted that the collection names can be customized by adjusting the corresponding variables in each of the scripts. If you wish to combine all the available ingredient information, simply use the same collection name when running the first three scripts. This way, a collection will be created containing the combined information of all three datasets. Subsequently, this collection can be processed with script number 6 to complement it with information about chemical compounds.

## Recipes

In the "scripts_recetas" folder, you will find all the elements necessary for managing the recipe datasets, including the scripts and folders containing the .csv or .json files corresponding to each dataset. Below is a list of the available scripts in the recommended order of execution:

1. abuela.py: script to include the "Recetas de la Abuela" dataset in a collection called "abuela".
2. recipeQA.py: script to include the RecipeQA dataset in a collection called "recipeQA".
3. recipe1m_originals.py: script designed to incorporate the original recipes from the Recipe1M dataset. It is important to note that these recipes retain the ingredient text in its original state, which means they include quantities and units within the text itself. This information is necessary to execute script 4.
4. recipe1m.py: script to include the Recipe1M dataset in a collection called "recipe1m". This script performs a search in the "recipe1m_originals" collection, so you must have run recipe1m_originals.py beforehand.
5. foodcom_interactions.py: script to include user interaction data with recipes from Food.com in a collection called "food.com_interactions". The purpose of including this collection is to make it faster to add interactions to recipes when executing the following script.
6. foodcom.py: script to include the Food.com dataset in a collection called "food.com". This script performs a search in the "food.com_interactions" collection, so script 5 must be run beforehand.
7. mealREC.py: script to include the MealREC dataset in a collection called "mealrec".
8. recipeNLG.py: script to include the RecipeNLG dataset in a collection called "recipenlg".

---

In each of the folders, besides the scripts, there is a .txt file describing the schema to which the information from the different datasets adheres. These files provide a guide to the data structure, although there may be variations due to the specific treatment of each dataset.
