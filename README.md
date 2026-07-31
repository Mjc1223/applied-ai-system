# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a content-based music recommendation system that generates personalized song recommendations using a weighted scoring algorithm. The recommender compares a listener's preferred genre, mood, and target energy level to songs in a catalog, ranks them by similarity, and explains why each recommendation was selected.

The goal of this project is to:

- Generate personalized song recommendations based on genre, mood, and target energy level
- Rank songs using a weighted scoring algorithm that compares listener preferences to song attributes
- Provide transparent explanations for why each song was recommended
- Demonstrate how content-based recommendation systems generate recommendations using structured song features
- Explore how feature weighting and algorithm design can influence recommendation results and introduce bias

---

## How The System Works

This project uses a simple content-based recommender. Each song is described by a set of features, and the system compares those features to a user’s taste profile.

- Each `Song` uses features such as:
  - `genre`: the broad style of the song
  - `mood`: the emotional feel, such as happy, chill, intense, or relaxed
  - `energy`: how active or intense the song feels
  - `tempo_bpm`: how fast the song is
  - `valence`: how positive or bright the song feels
  - `danceability` and `acousticness`: extra signals about rhythm and sound style

- Each `UserProfile` stores information about what the user seems to prefer:
  - `favorite_genre`: the style they like most
  - `favorite_mood`: the mood they usually enjoy
  - `target_energy`: the intensity level they tend to prefer
  - `likes_acoustic`: whether they often prefer acoustic or more electronic-sounding songs

- The `Recommender` computes a score for each song by comparing the song’s features to the user profile:
  - genre and mood matches receive a boost
  - numeric features such as energy, tempo, valence, danceability, and acousticness are compared to the user’s preferred values
  - songs that are closer to the user’s preferred values receive higher scores

- The recommendation process is:
  1. Input the user profile and the song catalog from `songs.csv`
  2. Compare each song to the user’s preferences
  3. Calculate a weighted similarity score for every song
  4. Rank the songs from highest score to lowest
  5. Output the top 5 recommended songs

- Final algorithm recipe:
  - Add **2.0 points** for an exact genre match
  - Add **1.0 point** for an exact mood match
  - Add up to **1.0 point** based on how close the song’s energy is to the user’s target energy
  - Add up to **1.0 point** for tempo similarity
  - Add up to **1.0 point** for valence similarity
  - Add up to **0.5 points** for danceability similarity
  - Add up to **0.5 points** for acousticness similarity
  - For numerical features, values closer to the user’s target receive more points
  - After every song is scored, the system sorts the songs from highest score to lowest and returns the top recommendations

Simple flow:

UserProfile -> Compare with each Song -> Score based on genre, mood, energy, tempo, valence, danceability, and acousticness -> Rank songs -> Show top recommendations

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
python -m pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Here is a representative sample of the recommender output from the terminal for the four evaluation profiles:

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

---

## Experiments You Tried

### Weight experiment: half genre weight, double energy weight

Experiment setup:

- Original scoring: genre match = +2.0, mood match = +1.0, energy similarity = up to +1.0
- Experimental scoring: genre match = +1.0, mood match = +1.0, energy similarity = up to +2.0

Baseline terminal output (original scoring weights):

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

Experimental terminal output (genre halved, energy doubled):

```text
Profile: High-Energy Pop
----------------------------------------
1. Sunrise City
   Score: 3.84
   Reasons:
     - Genre match (+1.0)
     - Mood match (+1.0)
     - Energy similarity (+1.84)

2. Gym Hero
   Score: 2.94
   Reasons:
     - Genre match (+1.0)
     - Energy similarity (+1.94)

3. Rooftop Lights
   Score: 2.72
   Reasons:
     - Mood match (+1.0)
     - Energy similarity (+1.72)

4. Storm Runner
   Score: 1.98
   Reasons:
     - Energy similarity (+1.98)

5. Backstreet Sparks
   Score: 1.96
   Reasons:
     - Energy similarity (+1.96)

Profile: Chill Lofi
----------------------------------------
1. Library Rain
   Score: 4.00
   Reasons:
     - Genre match (+1.0)
     - Mood match (+1.0)
     - Energy similarity (+2.00)

2. Midnight Coding
   Score: 3.86
   Reasons:
     - Genre match (+1.0)
     - Mood match (+1.0)
     - Energy similarity (+1.86)

3. Focus Flow
   Score: 2.90
   Reasons:
     - Genre match (+1.0)
     - Energy similarity (+1.90)

4. Spacewalk Thoughts
   Score: 2.86
   Reasons:
     - Mood match (+1.0)
     - Energy similarity (+1.86)

5. Coffee Shop Stories
   Score: 1.96
   Reasons:
     - Energy similarity (+1.96)

Profile: Deep Intense Rock
----------------------------------------
1. Storm Runner
   Score: 3.92
   Reasons:
     - Genre match (+1.0)
     - Mood match (+1.0)
     - Energy similarity (+1.92)

2. Gym Hero
   Score: 2.96
   Reasons:
     - Mood match (+1.0)
     - Energy similarity (+1.96)

3. Backstreet Sparks
   Score: 1.86
   Reasons:
     - Energy similarity (+1.86)

4. Sunrise City
   Score: 1.74
   Reasons:
     - Energy similarity (+1.74)

5. Neon Skyline
   Score: 1.72
   Reasons:
     - Energy similarity (+1.72)

Profile: Conflicting Edge Case
----------------------------------------
1. Sunrise City
   Score: 2.76
   Reasons:
     - Genre match (+1.0)
     - Mood match (+1.0)
     - Energy similarity (+0.76)

2. Paper Skyline
   Score: 2.00
   Reasons:
     - Energy similarity (+2.00)

3. Rooftop Lights
   Score: 1.88
   Reasons:
     - Mood match (+1.0)
     - Energy similarity (+0.88)

4. Spacewalk Thoughts
   Score: 1.84
   Reasons:
     - Energy similarity (+1.84)

5. Quiet Harbor
   Score: 1.78
   Reasons:
     - Energy similarity (+1.78)
```

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

Potential biases:

- This recommender may over-prioritize exact genre and mood matches because those features receive fixed bonus points. As a result, a song from a different genre that closely matches the user’s preferred energy, tempo, and emotional feel might rank lower than expected.
- The system also depends on manually assigned song features, so inaccurate labels or numerical values could affect the recommendations.
- Because the user profile contains specific target values, the recommender may favor songs that are very similar and provide less variety or discovery.


---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

This project helped me understand that recommender systems are shaped by the rules and weights we choose, not by an objective definition of what is "best." In this simulation, predictions came from comparing profile features (genre, mood, energy) against song attributes and adding weighted points. I learned that even small scoring decisions can strongly affect ranking outcomes, and that the recommendation list is really a reflection of design choices in the model.

One of the most interesting results came from testing the conflicting edge-case profile, where some songs still ranked highly even when one feature did not match well. That showed me how a few strong weighted factors can overpower other signals and create uneven outcomes. It also made me think more critically about real music apps: they can unintentionally reinforce familiar content, limit discovery, and introduce bias unless they include feedback loops, diversity mechanisms, and fairness checks.

Using AI tools helped me move faster when drafting explanations, comparing profile outputs, and organizing findings in both the README and model card. I still needed to double-check the AI output whenever specific numbers, score reasons, or ranking claims were involved, because those details had to match the real terminal runs from my code. If I extended this project next, I would add more user preference signals (like tempo and valence), use lightweight feedback updates from user actions (skip/like/replay), and test a diversity-aware re-ranking step so recommendations stay relevant while reducing filter-bubble behavior.



