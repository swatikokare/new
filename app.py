import pickle
import streamlit as st
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=3596db3017cd271702c64fa2d34c6740&language=en-US".format(movie_id)
    data = requests.get(url)
    if data.status_code == 200:
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None

def recommend(movie, movies, similarity):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies_name.append(movies.iloc[i[0]]['title'])
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_poster.append(poster_url)

    return recommended_movies_name, recommended_movies_poster

st.header("Movies Recommendation System ")

try:
    # Load movie list from pickle file
    movies = pickle.load(open('D:\\Desktop\\6th sem\\CAD\\movie\\artifacts\\movie_list.pkl', 'rb'))
    similarity = pickle.load(open('D:\\Desktop\\6th sem\\CAD\\movie\\artifacts\\similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error: Pickle file not found.")
    st.stop()

# Continue with the rest of your script
movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get a recommendation',
    movie_list
)

if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie, movies, similarity)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])
    
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])

    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])    

    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])
    


    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])

   #streamlit run app.py