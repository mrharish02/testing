import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np

movies_df = pickle.load(open('movies.pkl', 'rb'))
# movies_df = pd.DataFrame(movies_dict)

# Load similarity data as a generator function
def load_similarity_data():
    with open('similarity.pkl', 'rb') as file:
        while True:
            try:
                yield pickle.load(file)
            except EOFError:
                break

# Create a generator object for similarity data
similarity_generator = load_similarity_data()

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=dc35e67a529e6e6265a4d325eb09bdfa&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    # Get similarity values on-the-fly from the generator
    distances = next(similarity_generator)[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].movie_id
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Search MOVIES",
    movies_df['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
