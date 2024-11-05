# HEALTHY NUTRITION INFORMATION SYSTEM

## Final Degree Project - Bachelor’s Degree in Computer Engineering - University of Granada

**Student:** Mario López Quesada  
**Supervisors:** Maria José Martín Bautista and Andrea Morales Garzón

---

### Summary

This project presents the design and development of a multilingual information system aimed at managing and creating personalized healthy diets, with an additional focus on environmental emissions and food flavors. The growing public concern for healthy eating, the environmental impact of food production, and the lack of access to detailed and accurate nutritional information motivated the creation of this project: a system that integrates nutritional data from multiple sources, covering both recipes and ingredients, using advanced natural language processing (NLP) techniques for data mapping and standardization, which required intensive data processing efforts.

The developed platform allows users, ranging from ordinary individuals to nutrition professionals and researchers, to consult and manage diets efficiently and accurately. Through a simple and intuitive web interface, users can access a wide range of nutritional information, create and manage personalized diets, and evaluate the nutritional quality of foods according to indicators established by recognized institutions such as the World Health Organization (WHO).

The system also enables the comparison of foods and recipes in terms of their nutritional characteristics, environmental impact, and flavor, promoting healthier and more sustainable eating habits. The conclusions highlight the system’s capability to standardize diverse nutritional data and its potential for future expansions to include more nutrients and improve nutritional traffic lights.

---

### Repository Structure


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


#### Folder Descriptions

- **db-api:** Contains the system's API implementation. Due to copyright reasons, the necessary data for the `MONGODB_URL` environment variable is not included in the repository. Although you can run the Docker container with the MongoDB image, the database accessible from the provided URL will not contain the required information. You will need to obtain the data locally and set up your own MongoDB instance with this data. For more details on configuring and running the API, see this [README](/db-api/README.md).
- **db-scripts:** Contains scripts used for data loading and management in the system, categorized as follows:
  - **ingredient scripts:** Scripts related to ingredient collections.
  - **recipe scripts:** Scripts related to recipe collections.
  - **mappings:** Contains attribute mapping scripts between collections. These were the precursor to the mapping microservice implemented in the API.
- **fooddb-app:** Contains the system application code. You can view a demo of the application [here](https://drive.google.com/file/d/19o2rnG7faQAHBFGzdVJDY4vF_AghscpA/view?usp=sharing). For more details on installing and running the application, see this [README](/fooddb-app/README.md).

