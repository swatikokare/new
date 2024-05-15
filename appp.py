import pickle
import streamlit as st
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st

# Authenticate with Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id='93bc85565d224b3e94d22fbe7314c8f0', client_secret='3495495ef0984e5ca13893544733f75a')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

mood_valence = {
    "happy": 0.8,
    "sad": 0.2,
    "energetic": 0.7,
    "chill": 0.5
}


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

st.set_page_config(layout="wide")

st.title("Movies and Music Recommendation System")

try:
    # Load movie list from pickle file
    movies = pickle.load(open('D:\\Desktop\\6th sem\\CAD\\movie\\artifacts\\movie_list.pkl', 'rb'))
    similarity = pickle.load(open('D:\\Desktop\\6th sem\\CAD\\movie\\artifacts\\similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error: Pickle file not found.")
    st.stop()

# Movie Recommendation Section
st.header("Movie Recommendations")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie to get a recommendation',
    movie_list
)

if st.button('Show movie recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie, movies, similarity)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i, (name, poster) in enumerate(zip(recommended_movies_name, recommended_movies_poster)):
        with locals()[f"col{i+1}"]:
            st.text(name)
            st.image(poster, use_column_width=True)

# Music Recommendation Section
st.header("Music Recommendations")


# Set sidebar to be fixed
st.sidebar.set_option('decoration_style', 'accordion')


# Sidebar for music filters
st.sidebar.header("Music Filters")
genre = st.sidebar.selectbox("Select Genre", ["pop", "rock", "jazz", "hiphop"])
mood = st.sidebar.selectbox("Select Mood", ["happy", "sad", "energetic", "chill"])
year = st.sidebar.slider("Select Release Year", 1970, 2022, (1990, 2022))






# Main content for music recommendation
st.write(f"**Genre:** {genre}, **Mood:** {mood}, **Year Range:** {year[0]} - {year[1]}")
st.subheader("Recommended Songs")

# Fetch recommendations from Spotify API
results = sp.recommendations(seed_genres=[genre], target_valence=mood_valence[mood], min_year=year[0], max_year=year[1], limit=5)

# Display recommended songs
for idx, track in enumerate(results['tracks']):
    st.write(f"{idx+1}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
    st.image(track['album']['images'][0]['url'], width=200)
# Here you can fetch and display recommended songs based on selected filters.
# You can use APIs like Spotify API to fetch song recommendations based on genre, mood, and year.
# Display them using st.write or st.dataframe
