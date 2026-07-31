"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.
"""

import os
from typing import Dict, List, Tuple

from .recommender import generate_explanation, load_songs, recommend_songs


def build_profiles() -> List[Tuple[str, Dict[str, object]]]:
    """Create a set of user profiles to evaluate the recommender."""
    return [
        (
            "High-Energy Pop",
            {
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.90,
                "likes_acoustic": False,
            },
        ),
        (
            "Chill Lofi",
            {
                "favorite_genre": "lofi",
                "favorite_mood": "chill",
                "target_energy": 0.35,
                "likes_acoustic": True,
            },
        ),
        (
            "Deep Intense Rock",
            {
                "favorite_genre": "rock",
                "favorite_mood": "intense",
                "target_energy": 0.95,
                "likes_acoustic": False,
            },
        ),
        (
            "Conflicting Edge Case",
            {
                "favorite_genre": "pop",
                "favorite_mood": "happy",
                "target_energy": 0.20,
                "likes_acoustic": False,
            },
        ),
    ]


def main() -> None:
    songs = load_songs("data/songs.csv")
    profiles = build_profiles()

    for profile_name, profile in profiles:
        recommendations = recommend_songs(profile, songs, k=5)

        print(f"Profile: {profile_name}")
        print("-" * 40)
        for index, (song, score, _) in enumerate(recommendations, start=1):
            explanation = generate_explanation(profile, song, songs, api_key=os.getenv("OPENAI_API_KEY"))
            print(f"{index}. {song['title']}")
            print(f"   Score: {score:.2f}")
            print(f"   Explanation: {explanation}")
            print()


if __name__ == "__main__":
    main()
