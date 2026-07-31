import os

import streamlit as st

from src.recommender import generate_explanation, load_songs, recommend_songs


st.set_page_config(page_title="Music Recommender", page_icon="🎵", layout="wide")

st.title("🎵 Music Recommender with RAG-style Explanations")

with st.sidebar:
    st.header("User Profile")
    favorite_genre = st.text_input("Favorite genre", value="pop")
    favorite_mood = st.text_input("Favorite mood", value="happy")
    target_energy = st.slider("Target energy", 0.0, 1.0, 0.8, 0.01)
    likes_acoustic = st.checkbox("Likes acoustic songs", value=False)
    k = st.slider("Number of recommendations", 3, 10, 5, 1)

    st.caption("Set OPENAI_API_KEY to enable AI-generated explanations.")

if not os.path.exists("data/songs.csv"):
    st.error("The songs dataset was not found. Make sure data/songs.csv exists.")
    st.stop()

songs = load_songs("data/songs.csv")
profile = {
    "favorite_genre": favorite_genre,
    "favorite_mood": favorite_mood,
    "target_energy": target_energy,
    "likes_acoustic": likes_acoustic,
}

recommendations = recommend_songs(profile, songs, k=k)

st.subheader("Recommended songs")

for index, (song, score, _) in enumerate(recommendations, start=1):
    with st.expander(f"{index}. {song['title']} — Score: {score:.2f}", expanded=index == 1):
        st.write(f"Artist: {song['artist']}")
        st.write(f"Genre: {song['genre']}")
        st.write(f"Mood: {song['mood']}")
        st.write(f"Energy: {song['energy']:.2f}")
        explanation = generate_explanation(
            profile,
            song,
            songs,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        st.write("Explanation:")
        st.info(explanation)
