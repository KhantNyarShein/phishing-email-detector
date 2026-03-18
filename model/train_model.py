import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load dataset
data = pd.read_csv("datasets/phishing_email.csv")

# Remove rows with empty email text
data = data.dropna(subset=["Email Text"])

# Convert labels to numbers
data["Email Type"] = data["Email Type"].map({
    "Safe Email": 0,
    "Phishing Email": 1
})

# Select correct columns
X = data["Email Text"]
y = data["Email Type"]

# Convert text to numbers
vectorizer = TfidfVectorizer(stop_words="english")
X_vectorized = vectorizer.fit_transform(X)

# Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "model/phishing_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("Model training complete")