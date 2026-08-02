# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
VibePulse
---

## 2. Intended Use  

This recommender is designed to generate personalized song recommendations from a small catalog for a listener based on simple content features such as genre, mood, and energy, and it is mainly for students and instructors exploring how recommendation systems work in practice. It generates top-ranked song suggestions by comparing song attributes to a user preference profile, and it assumes the user has stable preferences that can be represented with clear labels and a target energy level (for example, favorite genre, favorite mood, and desired intensity). This project is intended for classroom exploration and learning, not for real production users, so its goal is transparency and experimentation rather than large-scale commercial accuracy.

---

## 3. How the Model Works  

This model is a simple content-based recommender that compares each song in the catalog to a listener profile and gives every song a score. The profile includes a favorite genre, favorite mood, and target energy level. A song gets a strong boost if its genre matches the listener, a smaller boost if its mood matches, and then receives additional points based on how close its energy level is to the listener's target energy. After all songs are scored, the system sorts them from highest to lowest and returns the top recommendations with short reason labels (for example, genre match or energy similarity) so the ranking is easy to understand.

Because this model uses only song attributes and a manually defined user profile, it is easy to explain and test, but it is also limited. It does not learn from listening history or other users, and it currently emphasizes exact category matches and energy closeness more than broader musical context. This makes it a good educational example of how recommendation rules turn input features into ranked predictions.

---

## 4. Data  

This project uses a small hand-curated catalog of 20 songs from data/songs.csv. Each song includes structured attributes that the recommender can score directly: title, artist, genre, mood, energy, tempo (BPM), valence, danceability, and acousticness. The catalog covers a broad but limited mix of genres, including pop, lofi, rock, electronic, ambient, jazz, folk, indie pop, indie folk, hip hop, house, synthwave, latin, classical, country, and rnb, and it includes moods such as happy, chill, intense, calm, focused, relaxed, energetic, romantic, hopeful, playful, reflective, nostalgic, and serene. I did not add or remove any rows from the provided starter dataset during this assignment, so all experiments were run on the same fixed catalog. Important parts of musical taste are still missing, including lyrics, language preference, cultural context, artist familiarity, listening history, skip behavior, time-of-day context, and evolving preferences over time, which means the model can only represent a simplified view of user taste.

---

## 5. Strengths  

This recommender works best for users with clear, consistent preferences for one genre and one mood, especially when their target energy is not extreme. In the evaluation, it produced intuitive top results for profiles like High-Energy Pop, Chill Lofi, and Deep Intense Rock, where the highest-ranked songs had expected genre or mood matches and close energy values. The scoring pattern it captures well is straightforward similarity: songs with exact genre and mood alignment plus nearby energy tend to rise to the top, and the generated reasons make this behavior transparent. This made the recommendations easy to interpret and generally consistent with what I expected from the weighted rules.

---

## 6. Limitations and Biases

This system has important limitations because the catalog is small (20 songs) and only represents a limited number of genres, moods, and artists from `data/songs.csv`. It uses weighted rules with strong fixed bonuses for exact genre and mood matches, so those category matches can be over-prioritized compared to more subtle musical similarity. In practice, this can create filter-bubble behavior where similar songs repeatedly surface and music discovery gets narrower.

The model is also dependent on manually assigned song attributes, which can be incomplete or subjective. If a genre or mood label is too broad or inconsistent, the ranking can reflect labeling choices more than a listener's full intent. This system does not use listening history, skips, likes, replay behavior, changing preferences, lyrics, language, or cultural context, so it represents only a simplified snapshot of taste rather than a full listening profile.

The OpenAI-assisted explanation path is also limited by what is retrieved from the local song records. Even when an AI explanation is available, it should be treated as a contextual summary of available metadata, not as an objective judgment of what music is "best."

### 6.1 Potential Misuse and Prevention

One realistic misuse is presenting recommendations as if they are universally correct or neutral, when they are actually produced by explicit weighting choices and a small catalog. Another risk is using unbalanced or biased catalog data and then interpreting those outputs as fair personalization. There is also operational risk if an API key is exposed, and content risk if generated explanations add unsupported details that are not grounded in retrieved song records. Finally, if personal listening data were added in future versions, over-aggressive user profiling could harm privacy and user trust.

To reduce those risks, I ground explanations in retrieved song records and keep a deterministic fallback path so the app still provides transparent explanations without external generation. I also rely on basic validation in the app flow and tests to check core ranking and explanation behavior. For operational safety, API keys are kept in environment variables or ignored local secrets files (for example `.streamlit/secrets.toml` and `.env`) rather than hardcoded values. I avoid storing unnecessary personal user data in this project, document limitations clearly in this model card, and treat this as an educational system that would require stronger evaluation and human review before any production use.

---

## 7. Evaluation  

I checked whether the recommender behaved as expected by running it against four distinct user profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and a conflicting edge-case profile. I looked for whether the highest-ranked tracks matched the intended mood and energy preferences and whether the explanations reflected the scoring logic in a way that felt understandable.

The tested profiles represent different listening styles: High-Energy Pop (upbeat pop with high energy), Chill Lofi (calmer low-energy lofi/chill), Deep Intense Rock (high-energy intense rock), and a Conflicting Edge Case (pop and happy preferences but very low target energy). What may be surprising is that the conflicting profile still ranked pop/happy songs highly, even when their energy was not close to the target, because fixed genre and mood bonuses are strong enough to offset weaker energy similarity.

```text
Profile: High-Energy Pop
----------------------------------------
1. Sunrise City
   Score: 3.92
   Reasons:
     - Genre match (+2.0)
     - Mood match (+1.0)
     - Energy similarity (+0.92)

2. Gym Hero
   Score: 2.97
   Reasons:
     - Genre match (+2.0)
     - Energy similarity (+0.97)

3. Rooftop Lights
   Score: 1.86
   Reasons:
     - Mood match (+1.0)
     - Energy similarity (+0.86)

4. Storm Runner
   Score: 0.99
   Reasons:
     - Energy similarity (+0.99)

5. Backstreet Sparks
   Score: 0.98
   Reasons:
     - Energy similarity (+0.98)
```

```text
Profile: Chill Lofi
----------------------------------------
1. Library Rain
   Score: 4.00
   Reasons:
     - Genre match (+2.0)
     - Mood match (+1.0)
     - Energy similarity (+1.00)

2. Midnight Coding
   Score: 3.93
   Reasons:
     - Genre match (+2.0)
     - Mood match (+1.0)
     - Energy similarity (+0.93)

3. Focus Flow
   Score: 2.95
   Reasons:
     - Genre match (+2.0)
     - Energy similarity (+0.95)

4. Spacewalk Thoughts
   Score: 1.93
   Reasons:
     - Mood match (+1.0)
     - Energy similarity (+0.93)

5. Coffee Shop Stories
   Score: 0.98
   Reasons:
     - Energy similarity (+0.98)
```

```text
Profile: Deep Intense Rock
----------------------------------------
1. Storm Runner
   Score: 3.96
   Reasons:
     - Genre match (+2.0)
     - Mood match (+1.0)
     - Energy similarity (+0.96)

2. Gym Hero
   Score: 1.98
   Reasons:
     - Mood match (+1.0)
     - Energy similarity (+0.98)

3. Backstreet Sparks
   Score: 0.93
   Reasons:
     - Energy similarity (+0.93)

4. Sunrise City
   Score: 0.87
   Reasons:
     - Energy similarity (+0.87)

5. Neon Skyline
   Score: 0.86
   Reasons:
     - Energy similarity (+0.86)
```

```text
Profile: Conflicting Edge Case
----------------------------------------
1. Sunrise City
   Score: 3.38
   Reasons:
     - Genre match (+2.0)
     - Mood match (+1.0)
     - Energy similarity (+0.38)

2. Gym Hero
   Score: 2.27
   Reasons:
     - Genre match (+2.0)
     - Energy similarity (+0.27)

3. Rooftop Lights
   Score: 1.44
   Reasons:
     - Mood match (+1.0)
     - Energy similarity (+0.44)

4. Paper Skyline
   Score: 1.00
   Reasons:
     - Energy similarity (+1.00)

5. Spacewalk Thoughts
   Score: 0.92
   Reasons:
     - Energy similarity (+0.92)
```

Pairwise profile comparisons:

1. High-Energy Pop vs Chill Lofi: High-Energy Pop prioritizes songs like Sunrise City and Gym Hero, while Chill Lofi puts Library Rain and Midnight Coding at the top. This makes sense because genre and mood bonuses differ (pop/happy vs lofi/chill), and the energy target shifts from high (0.90) to low (0.35).
2. High-Energy Pop vs Deep Intense Rock: Both profiles favor high-energy songs, but the top result changes from Sunrise City to Storm Runner. This is reasonable because Deep Intense Rock gets both genre and mood matches on Storm Runner, while High-Energy Pop gets those boosts on pop/happy tracks instead.
3. High-Energy Pop vs Conflicting Edge Case: Both profiles share pop/happy preferences, but the conflicting profile introduces a very low energy target (0.20), which lifts low-energy songs like Paper Skyline into the top five. This shows energy can influence rank, but genre and mood still strongly anchor the first positions.
4. Chill Lofi vs Deep Intense Rock: Chill Lofi recommendations cluster around low-energy calm tracks, while Deep Intense Rock surfaces intense, high-energy tracks. The difference matches the opposite targets in both category labels and energy direction.
5. Chill Lofi vs Conflicting Edge Case: Chill Lofi has coherent lofi/chill signals and therefore returns lofi-heavy results, but the conflicting profile mixes pop/happy labels with low energy and creates a more mixed top five. This makes sense because the conflicting profile pulls the scorer in two directions.
6. Deep Intense Rock vs Conflicting Edge Case: Deep Intense Rock consistently rewards intense, high-energy songs, while the conflicting profile introduces lower-energy options and fewer intense tracks. This contrast is expected because their target energies are far apart (0.95 vs 0.20), even though both still rely on the same fixed category bonus structure.

### 7.1 Reliability Testing Surprises

While testing, one thing that surprised me was how much ranking changed when I changed feature weights. Small shifts in the weight design made visible differences in top results, which reinforced how sensitive this kind of recommender is to modeling choices. Another important result was the conflicting profile behavior: genre and mood matches could still rank highly even when energy was a weaker match, because category bonuses stayed strong.

I also learned a reliability lesson from early development: my initial `Recommender` class draft returned songs in list order before ranking logic was fully implemented, which meant a simple test could appear to pass without proving the scoring behavior end to end. In the app layer, API key detection and Streamlit secrets handling also required careful testing because the app can still run through deterministic fallback explanations when no key is available. A recommendation list that "looks good" is not proof that the system is diverse, unbiased, or fully grounded, so I treat testing as ongoing rather than complete.

---

## 8. Future Work  

If I continue improving this recommender, I would add more user preference inputs beyond genre, mood, and energy, such as preferred tempo range, valence, danceability, acousticness, favorite artists, and a short recent listening history. I would also improve recommendation explanations by showing a clearer score breakdown per feature, adding a simple "why this was recommended" summary sentence, and displaying one contrast note like "this song ranked above X because of stronger mood alignment."

To improve diversity, I would add a re-ranking step so the top 5 are not all from the same genre or same mood, while still keeping overall relevance high. I would also test a novelty control that intentionally includes at least one "nearby but different" song to reduce filter-bubble effects and increase discovery.

To handle more complex user tastes, I would move from a single fixed profile to a blended preference model that supports multiple favorite genres or moods with different weights (for example, 60% chill lofi and 40% indie pop). I would also update preferences over time using user feedback signals (like skip, like, or replay) so the system can adapt when tastes change.

Additional recommendations to make this project stronger:

- Expand the catalog size and balance representation across genres/moods to reduce small-dataset bias.
- Add simple offline evaluation metrics (precision@k or hit-rate on a labeled validation set) to compare scoring versions more objectively.
- Run fairness and robustness checks across diverse profile types, especially edge-case and mixed-preference users.
- Keep an experiment log of weight changes and outcomes so model updates are reproducible and easy to compare.

---

## 9. Reflection and Ethics

### 9.1 Personal Reflection

I learned that recommender systems are heavily shaped by design choices, not neutral truth. In my own tests, the conflicting edge-case profile still pushed some genre/mood matches high in the ranking even when energy was less aligned, and that made me look at recommendation apps differently. It showed me how weighting can prioritize familiarity over discovery and why transparent scoring logic matters for responsible AI.

I also learned that integrating AI into an existing system is mostly about boundaries. In this project, the weighted recommender makes the core ranking decisions, while the AI layer adds optional explanation support. That split improved reliability and user trust because recommendations still work even when external AI services are unavailable.

### 9.2 Collaboration With AI

AI was useful for drafting code options, debugging steps, documentation structure, and architecture ideas, but I still had to verify behavior against real files, run the app, run tests, and correct inaccurate suggestions. One helpful AI suggestion was replacing free-text genre and mood input with dropdowns populated from the actual CSV catalog. That improved usability and reduced invalid input because users now choose values that are guaranteed to exist in the local dataset.

One flawed or incomplete AI direction early on was treating ordinary ranked CSV lookup as if it were automatically full RAG, or proposing broad architecture changes before checking the existing project structure and tests. I corrected that by reviewing the real repository first and by ensuring retrieved song records are actually used as explanation context in the implemented flow. This reminded me that human judgment is necessary to keep AI-assisted work accurate, safe, and aligned with responsible AI goals like transparency, reliability, and user trust.
