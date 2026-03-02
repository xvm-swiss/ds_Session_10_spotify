import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st          
from wordcloud import WordCloud

st.set_page_config('Ahalysis Dashboard', ':bar_chart:', 'wide')

df = pd.read_csv('data/cleaned_data/cleaned_spotifiy_dataset.csv')



# Kpi

No_of_tracks = df.drop_duplicates(subset=["track_name"], keep='last').value_counts().sum()

No_of_artists = df.drop_duplicates(subset=['artists'], keep='first').value_counts().sum()

No_of_albums = df.drop_duplicates(subset=["album_name"], keep='last').value_counts().sum()

Avg_song_duration_is_minutes = round(df["duration_ms"].mean() / 1000/60, 2)


No_of_genres = df.drop_duplicates( subset=["track_genre"], keep="last").value_counts().sum()


# Columns

kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns(5)

kpi_1.markdown(f'<h6> No. of tracks:<br> {No_of_tracks}</h6>', unsafe_allow_html= True)
kpi_2.markdown(f'<h6> No. of artists:<br> {No_of_artists}</h6>', unsafe_allow_html=True)
kpi_3.markdown(f'<h6>No. of albums:<br> {No_of_albums}</h6>', unsafe_allow_html=True)
kpi_4.markdown(f'<h6>Avg song duration is:<br> {Avg_song_duration_is_minutes} minutes </h6>', unsafe_allow_html=True)
kpi_5.markdown(f'<h6> No. of genres:<br> {No_of_genres} </h6>', unsafe_allow_html=True)


# Chart Top_10_popularity
Top_10_popularity = df[ df["popularity"] >=91]
Best_Top_10_popularity = Top_10_popularity.drop_duplicates(subset=["popularity"], keep='last')

top_10 = px.histogram(Best_Top_10_popularity ,x= 'artists', y='popularity', color='popularity',
       title= '# Top 10 most popular tracks')

row_1_col_1,= st.columns(1)
row_1_col_1.plotly_chart(top_10)


#  Top 10 artists with most popular songs

New_colum_1, = st.columns(1)
my_top_10 = ['Sam Smith', 'Kim Petras','Bad Bunny', 'Chencho Corleone',
 'Manuel Turizo','Jhayco',  'Arctic Monkeys', 'The Neighbourhood']

st.subheader("Top 10 artists with most popular songs")
for artist in my_top_10:
    st.write(f"- {artist}")


# Top 7 most loud songs
Top_7_most_loud_songs = df[ df["loudness"] >= 1.7]

most_loud = px.bar(Top_7_most_loud_songs, x='artists', y='loudness', color= 'loudness',
                   title='Top 7 most loud songs')

row_1_col_1,= st.columns(1)
row_1_col_1.plotly_chart(most_loud)


# Top 7 artists with danceable overall songs

Top_7_artists_with_danceable_overall_songs = df[ df['danceability'] >=0.9800]

artists_with_danceable_overall = px.bar(Top_7_artists_with_danceable_overall_songs, x='artists', y='danceability', color='danceability',
                                        title='Top 7 artists with danceable overall songs')

row_1_col_1 , = st.columns(1)
row_1_col_1.plotly_chart(artists_with_danceable_overall)



## Overall relationship between columns :
correlation_matrix = df.select_dtypes(include=['number']).corr()

rel_a = correlation_matrix.loc['danceability', 'loudness']
rel_b = correlation_matrix.loc['valence', 'mode']

fig, ax = plt.subplots(figsize=(12, 8))

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
ax.set_title("Overall Relationship between Music Features")

col1 = st.columns(1)[0] # Liste entpacken
col1.pyplot(fig)