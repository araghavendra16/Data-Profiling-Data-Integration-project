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

