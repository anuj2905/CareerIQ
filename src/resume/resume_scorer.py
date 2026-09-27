import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# 1. Load dataset
# ==========================================

df = pd.read_csv(
    "data/resumes/resume_data_for_ranking.csv"
)

print("Dataset shape:", df.shape)
print("Columns:")
print(df.columns.tolist())


# ==========================================
# 2. Keep required columns
# ==========================================

df = df[
    [
        "skills",
        "degree_names",
        "major_field_of_studies",
        "positions",
        "responsibilities",
        "skills_required",
        "matched_score"
    ]
]


# ==========================================
# 3. Handle missing values
# ==========================================

text_columns = [
    "skills",
    "degree_names",
    "major_field_of_studies",
    "positions",
    "responsibilities",
    "skills_required"
]

for column in text_columns:
    df[column] = df[column].fillna("").astype(str)


# Check missing values
print("\nMissing values:")
print(df.isnull().sum())


# ==========================================
# 4. Create one combined text feature
# ==========================================

df["combined_text"] = (
    df["skills"] + " " +
    df["degree_names"] + " " +
    df["major_field_of_studies"] + " " +
    df["positions"] + " " +
    df["responsibilities"] + " " +
    df["skills_required"]
)


# ==========================================
# 5. X and Y
# ==========================================

X = df["combined_text"]

# Keep target between 0 and 1 during training
y = df["matched_score"]


# ==========================================
# 6. Train/Test split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ==========================================
# 7. Convert text → numerical features
# ==========================================

vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)

X_test_tfidf = vectorizer.transform(X_test)


print("\nTF-IDF training shape:", X_train_tfidf.shape)
print("TF-IDF testing shape:", X_test_tfidf.shape)


# ==========================================
# 8. Random Forest model
# ==========================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# ==========================================
# 9. Train model
# ==========================================

model.fit(
    X_train_tfidf,
    y_train
)

print("\nModel training completed!")


# ==========================================
# 10. Make predictions
# ==========================================

y_pred = model.predict(X_test_tfidf)


# ==========================================
# 11. Evaluate model
# ==========================================

mae = mean_absolute_error(y_test, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_test, y_pred)
)

r2 = r2_score(y_test, y_pred)


print("\n========== MODEL PERFORMANCE ==========")

print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")


# ==========================================
# 12. Convert predictions to percentage
# ==========================================

y_pred_percentage = y_pred * 100
y_test_percentage = y_test.to_numpy() * 100


print("\n========== SAMPLE PREDICTIONS ==========")

for actual, predicted in zip(
    y_test_percentage[:10],
    y_pred_percentage[:10]
):
    print(
        f"Actual: {actual:.2f}%  |  "
        f"Predicted: {predicted:.2f}%"
    )


print(df["skills"].head(5).to_list())
print(df["skills_required"].head(5).to_list())