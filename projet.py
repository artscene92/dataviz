import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt


df = pd.read_csv(r'https://opendata.reseaux-energies.fr/explore/dataset/evolution-des-prix-domestiques-du-gaz-et-de-lelectricite/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false', sep=';')

st.title("Consommation d'énergie en France")


with st.sidebar:
    st.subheader("INFOS")
    st.write("PONSIN Arsène")
    st.write("#DATAVIZ2023")
    st.write("LinkedIn : https://www.linkedin.com/in/ars%C3%A8ne-ponsin-2a72591b8/")
    
 



columns_to_average = ["u_e_gaz_naturel", "u_e_electricite", "france_electricite", "france_gaz_naturel"]
df_per_year = df.groupby('annee')[columns_to_average].mean().reset_index()

col1, col2 = st.columns(2)

# Graphique 1 : Prix du gaz naturel en fonction de l'année
with col1:
    st.title("Graphique du prix du gaz naturel en France en fonction de l'année")
    st.bar_chart(df_per_year.set_index('annee')['france_gaz_naturel'])

# Graphique 2 : Prix de l'électricité en fonction de l'année
with col2:
    st.title("Graphique du prix de l'éléc en France en fonction de l'année")
    st.bar_chart(df_per_year.set_index('annee')['france_electricite'])




fig = px.line(df_per_year, x="annee", y=["u_e_gaz_naturel", "u_e_electricite", "france_electricite", "france_gaz_naturel"],
              title="Graphique du prix de l'énergie en €/MWh en fonction de l'année")

# Set line styles
fig.update_traces(line=dict(dash="dash"), selector=dict(name="u_e_gaz_naturel"))
fig.update_traces(line=dict(dash="dash"), selector=dict(name="u_e_electricite"))
fig.update_traces(line=dict(dash="solid"), selector=dict(name="france_electricite"))
fig.update_traces(line=dict(dash="solid"), selector=dict(name="france_gaz_naturel"))

st.plotly_chart(fig)


data_conso = pd.read_csv("https://opendata.agenceore.fr/explore/dataset/conso-elec-gaz-annuelle-par-naf-agregee-region/download?format=csv&timezone=Europe/Berlin&use_labels_for_header=false", encoding="utf-8", delimiter=";", thousands=".", decimal=".")

# je garde uniquement les lignes qui ont la colonne "code_categorie_consommation" =="RES"

data_conso_res = data_conso[data_conso["code_categorie_consommation"] == "RES"]

data_conso = data_conso.drop(["operateur", "code_categorie_consommation","libelle_categorie_consommation", "code_grand_secteur", "code_naf", "pdl", "indqual", "nombre_mailles_secretisees"], axis=1)


# on drop les colonnes suivantes : "opérateur","code_categorie_consommation", "code_grand_secteur", "code_naf", "pdl", "indqual", "nombre_mailles_secretisees"

data_conso_res = data_conso_res.drop(["operateur", "code_categorie_consommation", "code_grand_secteur", "code_naf", "pdl", "indqual", "nombre_mailles_secretisees"], axis=1)



# on va créer un nouveau dataframe, où on va additionner "conso" par "annee" en fonction de "code_region"
data_conso_res_region = data_conso_res.groupby(["annee","filiere","libelle_region"])["conso"].sum().reset_index()

electricite_data = data_conso_res_region[data_conso_res_region['filiere'] == 'Electricité']
gaz_data = data_conso_res_region[data_conso_res_region['filiere'] == 'Gaz']

st.title("Évolution de la consommation d'électricité et de gaz par région du secteur résidentiel")

# Filtrer les données pour l'électricité et le gaz
electricite_data = data_conso_res_region[data_conso_res_region['filiere'] == 'Electricité']
gaz_data = data_conso_res_region[data_conso_res_region['filiere'] == 'Gaz']

# Sélection de la filière
filiere_selection = st.selectbox("Sélectionnez la filière", ['Électricité', 'Gaz', 'Les deux'])

# Créer un graphique en ligne
if filiere_selection == 'Électricité':
    chart_data = electricite_data
    chart_title = 'Consommation d\'électricité par région'
elif filiere_selection == 'Gaz':
    chart_data = gaz_data
    chart_title = 'Consommation de gaz par région'
else:
    chart_data = data_conso_res_region
    chart_title = 'Consommation d\'électricité et de gaz par région'

st.subheader(chart_title)

# Créer le graphique en ligne avec Altair
chart = alt.Chart(chart_data).mark_line().encode(
    x=alt.X('annee:O', title='Année'),
    y='conso',
    color='libelle_region'
).properties(
    width=800,
    height=500
)

st.altair_chart(chart)



# Grouper les données par "annee", "filiere" et sommer la consommation
somme_conso = data_conso_res_region.groupby(['annee', 'filiere'])['conso'].sum().reset_index()

# Filtrer les données pour ne conserver que "Electricité" et "Gaz"
somme_conso = somme_conso[somme_conso['filiere'].isin(['Electricité', 'Gaz'])]

#créer graphique avec somme_conso
chart = alt.Chart(somme_conso).mark_line().encode(
    x=alt.X('annee:O', title='Année'),
    y='conso',
    color='filiere'
).properties(
    width=800,
    height=500
)

st.title("Consommation d'électricité et de gaz en France au fil des années pour les particuliers")
st.altair_chart(chart)


# Pivoter la table pour avoir l'électricité et le gaz dans des colonnes distinctes
somme_conso_pivot = somme_conso.pivot(index='annee', columns='filiere', values='conso').reset_index()


somme_conso = data_conso_res_region.groupby(['annee', 'filiere'])['conso'].sum().reset_index()

# Filtrer les données pour ne conserver que "Electricité" et "Gaz"
somme_conso = somme_conso[somme_conso['filiere'].isin(['Electricité', 'Gaz'])]



# Recommencons à partir de la ligne 1




# Filtrer les données pour ne conserver que "Electricité" et "Gaz"
# Filtrer les données pour ne conserver que les années à partir de 2018
data_conso = data_conso[data_conso['annee'] >= 2018]

# Filtrer les données pour ne conserver que "Electricité" et "Gaz"
electricite_data = data_conso[data_conso['filiere'] == 'Electricité']
gaz_data = data_conso[data_conso['filiere'] == 'Gaz']

# Grouper les données par "annee", "libelle_region" et sommer la consommation
electricite_grouped = electricite_data.groupby(['annee', 'libelle_region'])['conso'].sum().reset_index()
gaz_grouped = gaz_data.groupby(['annee', 'libelle_region'])['conso'].sum().reset_index()

# Créer le graphique avec Altair pour l'électricité
chart_electricite = alt.Chart(electricite_grouped).mark_line().encode(
    x=alt.X('annee:O', title='Année'),
    y=alt.Y('conso:Q', title='Consommation'),
    color='libelle_region:N'
).properties(
    width=800,
    height=500
)

st.title("Évolution de la consommation d'électricité par région à partir de 2018 tout secteur confondu")
st.altair_chart(chart_electricite)

# Créer le graphique avec Altair pour le gaz
chart_gaz = alt.Chart(gaz_grouped).mark_line().encode(
    x=alt.X('annee:O', title='Année'),
    y=alt.Y('conso:Q', title='Consommation'),
    color='libelle_region:N'
).properties(
    width=800,
    height=500
)

st.title("Évolution de la consommation de gaz par région à partir de 2018 tout secteur confondu")
st.altair_chart(chart_gaz)

# Filtrer les données pour l'année 2018 et la filière "Electricité"
electricite_2018 = data_conso[(data_conso['annee'] == 2018) & (data_conso['filiere'] == 'Electricité')]

# Grouper les données par "libelle_grand_secteur" et sommer la consommation
grouped = electricite_2018.groupby('libelle_grand_secteur')['conso'].sum().reset_index()


# Créer un slider pour sélectionner l'année avec une clé unique
selected_year = st.slider('Sélectionnez une année', key="year_selector", min_value=data_conso['annee'].min(), max_value=data_conso['annee'].max(), value=2018)

# Créer un bouton radio pour choisir la filière
selected_filiere = st.radio('Sélectionnez une filière', ['Electricité', 'Gaz'])

# Filtrer les données en fonction de l'année sélectionnée et de la filière choisie
filtered_data = data_conso[(data_conso['annee'] == selected_year) & (data_conso['filiere'] == selected_filiere)]

# Grouper les données par "libelle_grand_secteur" et sommer la consommation
grouped = filtered_data.groupby('libelle_grand_secteur')['conso'].sum().reset_index()

# Créer le graphique en camembert avec Plotly Express
fig = px.pie(grouped, names='libelle_grand_secteur', values='conso', title=f'Part des catégories dans la consommation de {selected_filiere} en France en {selected_year}')

# Afficher le graphique dans Streamlit
st.plotly_chart(fig)


categories = data_conso['libelle_grand_secteur'].unique()

# Sélectionner un libellé via la selectbox
selected_category = st.selectbox('Sélectionnez une catégorie', categories)

# Utiliser un widget radio pour sélectionner la filière
selected_filiere = st.radio('Sélectionnez une filière', ['Electricité', 'Gaz'], key="filiere_selector")

# Filtrer les données en fonction du libelle_grand_secteur sélectionné et de la filière sélectionnée
category_data = data_conso[(data_conso['libelle_grand_secteur'] == selected_category) & (data_conso['filiere'] == selected_filiere)]

# Grouper les données par "annee" et sommer la consommation
grouped = category_data.groupby(['annee', 'filiere'])['conso'].sum().reset_index()

# Créer le graphique en barres avec Plotly Express
fig = px.bar(grouped, x='annee', y='conso', title=f'Consommation de la catégorie "{selected_category}" en "{selected_filiere}" au fil des années')

# Afficher le graphique dans Streamlit
st.plotly_chart(fig)


