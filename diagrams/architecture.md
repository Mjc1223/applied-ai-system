# Applied AI Music Recommendation System Architecture

```mermaid
flowchart TD
    A[Input: User opens Streamlit app] --> B[Enter profile preferences]
    B --> C[Validate input]
    C -->|Valid| D[Retriever: load songs from CSV]
    C -->|Invalid| X[Show helpful error message]

    D --> E[Process: score each song]
    E --> F[Weighted recommendation ranking]
    F --> G[Top K recommendations]

    G --> H[Retriever: explanation context]
    H --> I[Agent: generate explanation]
    I --> J{OpenAI API key available?}
    J -->|Yes| K[AI-generated explanation]
    J -->|No| L[Deterministic fallback explanation]

    K --> M[Output: display recommendations in Streamlit]
    L --> M

    M --> N[User reviews recommendations]

    O[Evaluator: evaluate_recommendations / validate_recommendations] --> P[Tester: tests/test_recommender.py]
    P --> Q[Precision and fallback checks]
    Q --> R[Feedback for reliability improvements]
```

## Workflow Summary

- Input starts in the Streamlit UI in `app.py`.
- The retriever loads the catalog from `data/songs.csv`.
- The recommender processes each song with weighted scoring and ranking.
- The explanation agent uses retrieved context and either calls OpenAI or falls back to deterministic text.
- The output is the ranked recommendations shown in Streamlit.
- The evaluator and tester live in `src/recommender.py` and `tests/test_recommender.py` to check precision and fallback behavior.