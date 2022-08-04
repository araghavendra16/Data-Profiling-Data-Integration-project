####Set of SparQL queries, wrapped around Pyhton, to retrieve the relevant data for the app

from SPARQLWrapper import SPARQLWrapper, JSON
from pandas.io.json import json_normalize
import pydeck as pdk

def get_communes(municipality):
    """Given the municipality choices find all the communes in it by queries the ontop endpoint """

    q = """
        PREFIX : <http://www.semanticweb.org/ontologies/2022/5/DI#>

        SELECT DISTINCT(?commune_name AS ?Commune) 
        {    
            ?m a :Municipality;
                :nome "%s"; 
                :hasCommune ?c.
            ?c :nome ?commune_name.
        }
    """%municipality


    sparql = SPARQLWrapper("http://localhost:8080/sparql")
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    df_result = json_normalize(results["results"]["bindings"])

    return list(df_result["Commune.value"].values)



def get_commune_feature(object_property, data_property, feature):
    """Given the feature, find all the communes with that feature"""
    
    q = """

    PREFIX : <http://www.semanticweb.org/ontologies/2022/5/DI#>

    SELECT (?municipality_name AS ?Municipality) (?commune_name AS ?Commune) ?lat ?long ?%s
    {    
        ?m a :Municipality.
        ?m :nome ?municipality_name.
        ?m :hasCommune ?c.
        ?c :nome ?commune_name.
        ?c :%s ?d.
        ?d :%s ?%s.
        ?c :hasGeography ?g.
        ?g :latitude ?lat.
        ?g :longitude ?long
    } """ %(feature, object_property, data_property, feature)

    sparql = SPARQLWrapper("http://localhost:8080/sparql")
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    df_result = json_normalize(results["results"]["bindings"])
    df = df_result[["Municipality.value","Commune.value","lat.value","long.value","%s.value"%feature]]

    df["lat"] = df["lat.value"].apply(lambda x: float(x))
    df["lon"] = df["long.value"].apply(lambda x: float(x))

    df["municipality"] = df["Municipality.value"]    
    df["name"] = df["Commune.value"]
    

    df["%s"%feature] = df["%s.value"%feature].apply(lambda x: float(x))
    df["%s_norm"%feature] = df["%s.value"%feature].apply(lambda x: float(x))
    feature_min = df["%s_norm"%feature].min()
    feature_max = df["%s_norm"%feature].max()
    df["%s_norm"%feature] = df["%s_norm"%feature].apply(lambda x: (x - feature_min)/(feature_max - feature_min))


    return df
def get_commune_facts(commune):
    
    q = """        
        PREFIX : <http://www.semanticweb.org/ontologies/2022/5/DI#>

        SELECT  ?municipality_name ?name ?population ?area ?companies ?schools ?breakdowns ?poi
        {    
            ?m a :Municipality.
            ?m :nome ?municipality_name.
            ?m :hasCommune ?c.
            ?c :nome ?name.
            ?c :nome "%s".
        OPTIONAL {  
                ?c :hasDemographic ?d.
                ?d :numero_di_abitanti ?population. 
        }
        OPTIONAL {  
                ?c :hasGeography ?g.
                ?g :superficie ?area.
        }
        OPTIONAL {
            ?c :hasDevelopment ?develop.
            ?develop :numero_di_aziende ?companies.
        }
        
        OPTIONAL {
            ?c :hasDevelopment ?develop.
            ?develop :numero_di_scuole ?schools.
        }
        OPTIONAL {
            ?c :hasItsOwn ?s.
            ?s :numero_di_punti_di_interesse ?poi.
        }
        OPTIONAL {
            ?c :hasItsOwn ?s.
            ?s :numero_di_frazioni ?breakdowns.
        }
        }      
    """%commune

    sparql = SPARQLWrapper("http://localhost:8080/sparql")
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    df_result = json_normalize(results["results"]["bindings"])

    result = {"population": "NA", "area": "NA", "companies": "NA", 
              "schools": "NA", "breakdowns":"NA","poi":"NA"}

    if "population.value" in df_result.columns:
        result["population"] = list(df_result["population.value"].values)[0]


    if "area.value" in df_result.columns:
        result["area"] = list(df_result["area.value"].values)[0]
        


    if "companies.value" in df_result.columns:
        result["companies"] = list(df_result["companies.value"].values)[0]
        


    if "schools.value" in df_result.columns:
        result["schools"] = list(df_result["schools.value"].values)[0]
        
        
    
    if "breakdowns.value" in df_result.columns:
        result["breakdowns"] = list(df_result["breakdowns.value"].values)[0]
        
    
    if "poi.value" in df_result.columns:
        result["poi"] = list(df_result["poi.value"].values)[0]
        
        
    #df = df_result[["name.value","population.value", "area.value", "companies.value","schools.value","breakdowns.value","poi.value"]]
    
    
    return result

    


### Set of helper functions for the app
def get_pydeck_all(df, feature):

    map_style = 'mapbox://styles/mapbox/light-v9'
    initial_view_state = pdk.ViewState( latitude=df["lat"].mean(), longitude=df["lon"].mean(), zoom=7.5, pitch=60)
    column_layer = pdk.Layer("ColumnLayer", data=df, get_position=["lon", "lat"], get_elevation=feature+"_norm", elevation_scale=50000,
        radius=800, get_fill_color=[200, "0", "0", 100], pickable=True, auto_highlight=True)

    visual = pdk.Deck( map_style = map_style, initial_view_state=initial_view_state , layers=[column_layer], tooltip={"text": "{name}\n{%s}"%feature})

    return visual


def get_image_url(commune):
    """get the image url if present"""

    q = """
    
    PREFIX : <http://www.semanticweb.org/ontologies/2022/5/DI#>
    SELECT  ?municipality_name ?name ?image_url
    {    
        ?m a :Municipality.
        ?m :nome ?municipality_name.
        ?m :hasCommune ?c.
        ?c :nome ?name.
        ?c :nome "%s".
    OPTIONAL {  
            ?c :hasImages ?i.
            ?i :image_url  ?image_url. 
    }
    }
    """%(commune)

    sparql = SPARQLWrapper("http://localhost:8080/sparql")
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    df_result = json_normalize(results["results"]["bindings"])

    if "image_url.value" in df_result.columns:
        return list(df_result["image_url.value"].values)[0]

    else:
        return None


def get_fact_map(fact_choice, municipalities_choice):

    if fact_choice == "Population":    
        df = get_commune_feature("hasDemographic", "numero_di_abitanti", "Population")
        df = df[df["municipality"].isin(municipalities_choice)]
        return get_pydeck_all(df, "Population")

    elif fact_choice == "Companies":
        df = get_commune_feature("hasDevelopment", "numero_di_aziende", "Companies")
        df = df[df["municipality"].isin(municipalities_choice)]
        return get_pydeck_all(df, "Companies")

    elif fact_choice == "Area":
        df = get_commune_feature("hasGeography", "superficie", "Area")
        df = df[df["municipality"].isin(municipalities_choice)]
        return get_pydeck_all(df, "Area")

    elif fact_choice == "Schools":
        df = get_commune_feature("hasDevelopment", "numero_di_scuole", "Schools")
        df = df[df["municipality"].isin(municipalities_choice)]
        return get_pydeck_all(df, "Schools")

    elif fact_choice == "Breakdowns":
        df = get_commune_feature("hasItsOwn", "numero_di_frazioni", "Breakdowns")
        df = df[df["municipality"].isin(municipalities_choice)]
        return get_pydeck_all(df, "Breakdowns")

    elif fact_choice == "POI":
        df = get_commune_feature("hasItsOwn", "numero_di_punti_di_interesse", "POI")
        df = df[df["municipality"].isin(municipalities_choice)]
        return get_pydeck_all(df, "POI")

    else:
        return None
        



def get_story(commune):
    """Get commune story"""

    q = """
        PREFIX : <http://www.semanticweb.org/ontologies/2022/5/DI#>

        SELECT (?municipality_name AS ?Municipality) (?commune_name AS ?Commune) ?story
        {    
            ?m a :Municipality.
            ?m :nome ?municipality_name.
            ?m :hasCommune ?c.
            ?c :nome "%s".
            ?c :hasHistory ?h.
            ?h :storia ?story.  
        }

    """%(commune)

    sparql = SPARQLWrapper("http://localhost:8080/sparql")
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    df_result = json_normalize(results["results"]["bindings"])

    if "story.value" in df_result.columns:
        return list(df_result["story.value"].values)[0]

    else:
        return None

