from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    evaluate_recommendations,
    generate_explanation,
    retrieve_context,
    validate_recommendations,
)


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_retrieve_context_prioritizes_matching_genre_and_mood():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()

    context = retrieve_context(user, rec.songs, k=2)

    assert len(context) >= 1
    assert context[0].genre == "pop"
    assert context[0].mood == "happy"


def test_generate_explanation_falls_back_without_api_key():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    explanation = generate_explanation(user, rec.songs[0], rec.songs, api_key=None)

    assert isinstance(explanation, str)
    assert explanation.strip() != ""
    assert "genre" in explanation.lower() or "mood" in explanation.lower() or "energy" in explanation.lower()


def test_evaluate_recommendations_returns_precision_metrics():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    recommendations = rec.recommend(user, k=2)

    metrics = evaluate_recommendations(recommendations, relevant_ids=[1])

    assert metrics["precision_at_1"] == 1.0
    assert metrics["precision_at_2"] >= 0.5


def test_validate_recommendations_passes_for_strong_match():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    recommendations = rec.recommend(user, k=2)

    result = validate_recommendations(recommendations, relevant_ids=[1], minimum_precision=0.5)

    assert result["passed"] is True
    assert result["metrics"]["precision_at_1"] == 1.0
