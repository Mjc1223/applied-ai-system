import os

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

from src.recommender import generate_explanation, load_songs, recommend_songs


def test_openai_connection(api_key: str) -> tuple[bool, str]:
    """Test whether the configured OpenAI key can successfully call the API."""
    if not api_key:
        return False, "OPENAI_API_KEY is not set."

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Connectivity check"},
                {"role": "user", "content": "Reply with OK"},
            ],
            max_tokens=5,
            temperature=0,
        )
        return True, "OpenAI connection successful."
    except Exception as error:
        return False, f"OpenAI connection failed: {type(error).__name__}"


st.set_page_config(page_title="Music Recommender", page_icon="🎵", layout="wide")

st.title("🎵 AI Music Recommender")

if not os.path.exists("data/songs.csv"):
    st.error("The songs dataset was not found. Make sure data/songs.csv exists.")
    st.stop()

songs = load_songs("data/songs.csv")
if not songs:
    st.error("The songs catalog is empty. Add songs to data/songs.csv before running the app.")
    st.stop()

genre_values = sorted({str(song.get("genre", "")).strip().lower() for song in songs if str(song.get("genre", "")).strip()})
mood_values = sorted({str(song.get("mood", "")).strip().lower() for song in songs if str(song.get("mood", "")).strip()})

if not genre_values or not mood_values:
    st.error("The song catalog must contain at least one genre and one mood value.")
    st.stop()

genre_options = [value.title() for value in genre_values]
mood_options = [value.title() for value in mood_values]

with st.sidebar:
    st.header("User Profile")
    favorite_genre_display = st.selectbox("Favorite genre", options=genre_options, index=0)
    st.caption("Genre choices come from the current song catalog.")
    favorite_mood_display = st.selectbox("Desired mood", options=mood_options, index=0)
    st.caption("Mood choices come from the current song catalog.")
    target_energy = st.slider("Target energy", 0.0, 1.0, 0.8, 0.01)
    likes_acoustic = st.checkbox("Likes acoustic songs", value=False)
    k = st.slider("Number of recommendations", 3, 10, 5, 1)

    st.caption("Set OPENAI_API_KEY to enable AI-generated explanations.")

    api_key = os.getenv("OPENAI_API_KEY", "")
    try:
        secret_key = st.secrets.get("OPENAI_API_KEY", "")
        if secret_key:
            api_key = secret_key
    except (FileNotFoundError, StreamlitSecretNotFoundError):
        pass
    if api_key:
        st.success("OpenAI key detected.")
    else:
        st.warning("OpenAI key not detected.")

    if st.button("Test OpenAI connection"):
        ok, message = test_openai_connection(api_key)
        if ok:
            st.success(message)
        else:
            st.error(message)
profile = {
    "favorite_genre": favorite_genre_display.lower() if favorite_genre_display else "",
    "favorite_mood": favorite_mood_display.lower() if favorite_mood_display else "",
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
            api_key=api_key,
        )
        st.write("Explanation:")
        st.info(explanation)
