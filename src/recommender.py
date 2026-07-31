import csv
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Song:
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs = []
        for song in self.songs:
            score, _ = score_song(user, song)
            scored_songs.append((score, song))

        scored_songs.sort(key=lambda item: item[0], reverse=True)
        return [song for _, song in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return generate_explanation(user, song, self.songs, api_key=None)


def _get_value(source: Any, field_name: str, default: Any = None) -> Any:
    if isinstance(source, dict):
        return source.get(field_name, default)
    return getattr(source, field_name, default)


def _coerce_user_prefs(user_prefs: Any) -> Dict[str, Any]:
    if isinstance(user_prefs, dict):
        return user_prefs

    return {
        "favorite_genre": _get_value(user_prefs, "favorite_genre"),
        "favorite_mood": _get_value(user_prefs, "favorite_mood"),
        "target_energy": _get_value(user_prefs, "target_energy"),
        "likes_acoustic": _get_value(user_prefs, "likes_acoustic"),
    }


def _coerce_song(song: Any) -> Dict[str, Any]:
    if isinstance(song, dict):
        return song

    return {
        "id": _get_value(song, "id"),
        "title": _get_value(song, "title"),
        "artist": _get_value(song, "artist"),
        "genre": _get_value(song, "genre"),
        "mood": _get_value(song, "mood"),
        "energy": _get_value(song, "energy"),
        "tempo_bpm": _get_value(song, "tempo_bpm"),
        "valence": _get_value(song, "valence"),
        "danceability": _get_value(song, "danceability"),
        "acousticness": _get_value(song, "acousticness"),
    }


def load_songs(csv_path: str) -> List[Dict]:
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    return songs


def score_song(user_prefs: Any, song: Any) -> Tuple[float, List[str]]:
    prefs = _coerce_user_prefs(user_prefs)
    song_data = _coerce_song(song)

    score = 0.0
    reasons: List[str] = []

    preferred_genre = prefs.get("favorite_genre")
    song_genre = song_data.get("genre")
    if preferred_genre is not None and song_genre is not None:
        if str(preferred_genre).lower() == str(song_genre).lower():
            score += 2.0
            reasons.append("Genre match (+2.0)")

    preferred_mood = prefs.get("favorite_mood")
    song_mood = song_data.get("mood")
    if preferred_mood is not None and song_mood is not None:
        if str(preferred_mood).lower() == str(song_mood).lower():
            score += 1.0
            reasons.append("Mood match (+1.0)")

    target_energy = prefs.get("target_energy")
    song_energy = song_data.get("energy")
    if target_energy is not None and song_energy is not None:
        try:
            target_energy_value = float(target_energy)
            song_energy_value = float(song_energy)
            energy_similarity = max(0.0, 1.0 - abs(song_energy_value - target_energy_value))
            score += energy_similarity
            reasons.append(f"Energy similarity (+{energy_similarity:.2f})")
        except (TypeError, ValueError):
            reasons.append("Energy similarity skipped (invalid values)")
    else:
        reasons.append("Energy similarity skipped (missing values)")

    likes_acoustic = prefs.get("likes_acoustic")
    acousticness = song_data.get("acousticness")
    if likes_acoustic is not None and acousticness is not None:
        try:
            acousticness_value = float(acousticness)
            if bool(likes_acoustic) and acousticness_value >= 0.6:
                score += 0.5
                reasons.append("Acoustic preference match (+0.50)")
            elif not bool(likes_acoustic) and acousticness_value < 0.6:
                score += 0.5
                reasons.append("Non-acoustic preference match (+0.50)")
            else:
                reasons.append("Acoustic preference neutral")
        except (TypeError, ValueError):
            reasons.append("Acoustic preference skipped (invalid values)")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Any, songs: List[Any], k: int = 5) -> List[Tuple[Any, float, str]]:
    scored_recommendations: List[Tuple[Any, float, str]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored_recommendations.append((song, score, explanation))

    ranked_recommendations = sorted(
        scored_recommendations,
        key=lambda item: item[1],
        reverse=True,
    )

    return ranked_recommendations[:k]


def retrieve_context(user_prefs: Any, songs: List[Any], k: int = 5) -> List[Any]:
    prefs = _coerce_user_prefs(user_prefs)

    def rank_key(song: Any) -> Tuple[float, float, float]:
        song_data = _coerce_song(song)
        genre_match = 1.0 if str(prefs.get("favorite_genre", "")).lower() == str(song_data.get("genre", "")).lower() else 0.0
        mood_match = 1.0 if str(prefs.get("favorite_mood", "")).lower() == str(song_data.get("mood", "")).lower() else 0.0
        energy_diff = abs(float(song_data.get("energy", 0.0)) - float(prefs.get("target_energy", 0.0)))
        acoustic_bonus = 0.0
        if prefs.get("likes_acoustic") is not None:
            acousticness = float(song_data.get("acousticness", 0.0))
            if bool(prefs.get("likes_acoustic")) and acousticness >= 0.6:
                acoustic_bonus = 1.0
            elif not bool(prefs.get("likes_acoustic")) and acousticness < 0.6:
                acoustic_bonus = 1.0
        return (genre_match, mood_match, -energy_diff + acoustic_bonus)

    ranked = sorted(songs, key=rank_key, reverse=True)
    return ranked[:k]


def generate_explanation(user_prefs: Any, song: Any, songs: Optional[List[Any]] = None, api_key: Optional[str] = None) -> str:
    prefs = _coerce_user_prefs(user_prefs)
    song_data = _coerce_song(song)

    song_title = song_data.get("title") or "this song"
    reasons: List[str] = []

    if str(prefs.get("favorite_genre", "")).lower() == str(song_data.get("genre", "")).lower():
        reasons.append("it matches the user's favorite genre")

    if str(prefs.get("favorite_mood", "")).lower() == str(song_data.get("mood", "")).lower():
        reasons.append("it matches the user's preferred mood")

    try:
        if abs(float(song_data.get("energy", 0.0)) - float(prefs.get("target_energy", 0.0))) < 0.2:
            reasons.append("its energy level closely fits the target")
    except (TypeError, ValueError):
        pass

    fallback = (
        f"{song_title} is a strong fit because " + ", ".join(reasons)
        if reasons
        else f"{song_title} is a strong fit based on the available musical features."
    )

    if not api_key:
        return fallback

    try:
        from openai import OpenAI
    except Exception:
        return fallback

    try:
        client = OpenAI(api_key=api_key)
        context = retrieve_context(user_prefs, songs or [], k=5)

        prompt = (
            "You are a concise music recommendation assistant. "
            f"Explain why {song_title} should be recommended to a listener with "
            f"genre={prefs.get('favorite_genre')}, mood={prefs.get('favorite_mood')}, "
            f"and target energy={prefs.get('target_energy')}. "
            f"Use this context: {', '.join([str(_coerce_song(item).get('title', '')) for item in context])}"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a concise music recommendation assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=80,
        )

        ai_text = None
        if response and getattr(response, "choices", None):
            message = response.choices[0].message
            ai_text = getattr(message, "content", None)

        if isinstance(ai_text, str) and ai_text.strip():
            return ai_text.strip()
    except Exception:
        pass

    return fallback


def evaluate_recommendations(recommendations: List[Any], relevant_ids: Optional[List[int]] = None) -> Dict[str, float]:
    relevant = set(relevant_ids or [])

    def extract_id(item: Any) -> Optional[int]:
        if isinstance(item, tuple):
            item = item[0]
        if isinstance(item, dict):
            return item.get("id")
        if hasattr(item, "id"):
            return getattr(item, "id")
        return None

    ranked_ids = [extract_id(item) for item in recommendations]
    precision_at_1 = 1.0 if ranked_ids[:1] and ranked_ids[0] in relevant else 0.0
    precision_at_2 = sum(1 for item in ranked_ids[:2] if item in relevant) / 2.0 if ranked_ids[:2] else 0.0

    return {
        "precision_at_1": precision_at_1,
        "precision_at_2": precision_at_2,
    }


def validate_recommendations(
    recommendations: List[Any],
    relevant_ids: Optional[List[int]] = None,
    minimum_precision: float = 0.5,
) -> Dict[str, Any]:
    metrics = evaluate_recommendations(recommendations, relevant_ids=relevant_ids)
    passed = metrics["precision_at_1"] >= minimum_precision
    return {
        "passed": passed,
        "minimum_precision": minimum_precision,
        "metrics": metrics,
    }
