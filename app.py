import pickle
import streamlit as st
import pandas as pd
import requests

API_KEY = "130ac9a5"  # OMDb API key

# -----------------------------
# Fetch movie info using OMDb
# -----------------------------
def fetch_movie_info(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get("Response") == "True":
        info = {
            "title": data.get("Title"),
            "year": data.get("Year"),
            "genre": data.get("Genre"),
            "rating": data.get("imdbRating"),
            "actors": data.get("Actors"),
            "plot": data.get("Plot"),
            "poster": data.get("Poster") if data.get("Poster") != "N/A" else None,
            "imdb_link": f"https://www.imdb.com/title/{data.get('imdbID')}/" if data.get("imdbID") else None
        }
        return info
    return None

# -----------------------------
# Load movies and similarity data
# -----------------------------
movies_dic = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dic)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Movie Recommender System")
selected_movie_name = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Recommend"):
    movie_index = movies[movies['title'] == selected_movie_name].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    st.subheader("Recommended Movies:")

    for i in movie_list:
        movie_title = movies.iloc[i[0]].title
        info = fetch_movie_info(movie_title)

        if info:
            # Movie title
            st.markdown(f"## *{info['title']} ({info['year']})")

            # Layout: Poster and details side by side
            col1, col2 = st.columns([1, 2])

            with col1:
                if info['poster']:
                    st.image(info['poster'], width=250)
                else:
                    st.info("Poster not available")

            with col2:
                st.markdown(f"**🎭 Genre:** {info['genre']}")
                st.markdown(f"**⭐ IMDb Rating:** {info['rating']}")
                st.markdown(f"**Actors:** {info['actors']}")
                st.markdown(f"**🗒️ Plot:** {info['plot']}")
                if info['imdb_link']:
                    st.markdown(f"[🔗 View on IMDb]({info['imdb_link']})")

            # Separator line
            st.markdown("---")
