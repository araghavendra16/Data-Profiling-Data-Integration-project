## Install PostgreSQL database

## Create the PostgreSQL database 
Run from Profiling folder the following script loading data one DB_v1.ipynb, making sure you cnage to your valid PostgreSQL credentials

## Install the libraries in requirement.txt
pip install -r requirements.txt

## Run the Ontop endpoint
./ontop endpoint --ontology=input/project.owl --mapping=input/project.obda --properties=input/project.properties

## Run the streamlit application
streamlit run ./app.py

## Voila, I hope it works :)


# What is the project about? 
 The main objective is to build a data integration system from scratch using Ontop (a Virtual Knowledge Graph application), PostgreSQL, SPARQL and Python (streamlit). The data provided was in CSV format. Data profiling tools such as pandas profiling was used, and various dependencies in data was detected using standard algorithms (SCDP, DUCC, TANE and NORMALIZE). Then, after cleaning the data and normalizing it, we designed a ER diagram and UML model for the database. We hand-designed the classes, object, and data property. The last part of the system is the mapping which is crucial to query ontology data sources. The mapping connect all classes, object and data properties with database. The data is queried using SPARQL queries and visualized using a streamlit application.

![image](https://user-images.githubusercontent.com/61226849/216811974-5b27f07b-28af-450b-9ff5-ffed9c6a2cd3.png)
![image](https://user-images.githubusercontent.com/61226849/216811984-0ed36e2e-a1eb-451f-adb5-c2869c8a91b4.png)
![image](https://user-images.githubusercontent.com/61226849/216812002-bed0a2b4-9ee8-43e6-a473-303d9b52f551.png)
![image](https://user-images.githubusercontent.com/61226849/216812023-1efadbe2-5a52-463e-be1f-847d8180b9d4.png)
![image](https://user-images.githubusercontent.com/61226849/216812036-f57ff521-044b-496c-91e4-56115a56eaed.png)
