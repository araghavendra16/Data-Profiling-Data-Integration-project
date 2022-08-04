
import streamlit as st
import numpy as np
from PIL import Image
from queries import *
import requests

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("Select your Municipalities and Communes")
    municipalities_choice = st.multiselect(
        'Municipalities',
        ['Avellino', 'Caserta', 'Salerno'],
        ['Avellino', 'Caserta', 'Salerno'])
    
st.title('Italian Municipalities')


fact_choice = st.selectbox('Statistics', ["Population", "Area", "Companies", "Schools", "Breakdowns","POI"])
st.pydeck_chart(get_fact_map(fact_choice, municipalities_choice))


st.title('Facts about Commune')
communes = []
for m in municipalities_choice:
    communes += get_communes(m)
communes_choice = st.selectbox("", sorted(communes))
facts = get_commune_facts(communes_choice)
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Population", facts["population"])
col2.metric("Area (KM)", facts["area"])
col3.metric("Companies", facts["companies"])
col4.metric("Schools", facts["schools"])
col5.metric("Breakdowns", facts["breakdowns"])
col6.metric("POI",facts["poi"])


st.title('Story')
story = get_story(communes_choice)
st.write(story)



st.title('Image')
image_url = get_image_url(communes_choice)
if image_url:
    img_data = requests.get(image_url).content
    with open('./images/image.jpg', 'wb') as handler:
        handler.write(img_data)
    
    image = Image.open('./images/image.jpg')
    st.image(image, caption='Image of %s Commune'%communes_choice)

else:

    image = Image.open('./images/no_image.png')
    st.image(image, caption='Image of %s Commune is not available'%communes_choice)

