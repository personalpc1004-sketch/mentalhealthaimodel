import numpy as np
import pandas as pd


QUESTION_COLUMNS = [
    "question1",
    "question2",
    "question3",
    "question4",
    "question5",
    "question6",
    "question7",
    "question8",
    "question9",
]

TIME_COLUMNS = [
    "time1",
    "time2",
    "time3",
    "time4",
    "time5",
    "time6",
    "time7",
    "time8",
    "time9",
]


def create_features(data):
    """
    Convert API input into the exact 36-feature structure
    used by the trained XGBoost Model V1.
    """

    df = pd.DataFrame([data])

    # --------------------------------------------------
    # 1. Validate required columns
    # --------------------------------------------------

    required_columns = QUESTION_COLUMNS + TIME_COLUMNS

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required fields: {missing_columns}"
        )

    # --------------------------------------------------
    # 2. Extract response-time features
    # --------------------------------------------------

    times = df[TIME_COLUMNS].astype(float)

    behavioral_features = times.copy()

    # --------------------------------------------------
    # 3. Statistical behavioral features
    # --------------------------------------------------

    behavioral_features["time_mean"] = times.mean(axis=1)
    behavioral_features["time_median"] = times.median(axis=1)
    behavioral_features["time_std"] = times.std(axis=1)
    behavioral_features["time_min"] = times.min(axis=1)
    behavioral_features["time_max"] = times.max(axis=1)

    behavioral_features["time_range"] = (
        behavioral_features["time_max"]
        - behavioral_features["time_min"]
    )

    behavioral_features["time_total"] = times.sum(axis=1)

    # --------------------------------------------------
    # 4. Fast / slow response counts
    # --------------------------------------------------

    behavioral_features["fast_response_count"] = (
        (times < 2).sum(axis=1)
    )

    behavioral_features["slow_response_count"] = (
        (times > 60).sum(axis=1)
    )

    # --------------------------------------------------
    # 5. Log-transformed response times
    # --------------------------------------------------

    for column in TIME_COLUMNS:
        behavioral_features[f"log_{column}"] = np.log1p(
            times[column]
        )

    # --------------------------------------------------
    # 6. Combine PHQ-9 questions + behavioral features
    # --------------------------------------------------

    question_features = df[QUESTION_COLUMNS].astype(float)

    final_features = pd.concat(
        [
            question_features,
            behavioral_features,
        ],
        axis=1,
    )

    # --------------------------------------------------
    # 7. Safety check
    # --------------------------------------------------

    if final_features.shape[1] != 36:
        raise ValueError(
            f"Expected 36 features, "
            f"but generated {final_features.shape[1]}"
        )

    return final_features