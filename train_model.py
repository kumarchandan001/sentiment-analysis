# train_model.py

# 1. Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib # Used to save our model

print("Starting the model training process... 🚀")

# 2. Load the Dataset
try:
    df = pd.read_csv('IMDB Dataset.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("Error: 'IMDB Dataset.csv' not found. Make sure it's in the 'sentiment-app' folder.")
    exit()

# 3. Prepare the Data
df['sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})
X = df['review']
y = df['sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data prepared and split.")

# 4. Create and Train the Model using a Pipeline
model_pipeline = Pipeline([
    ('vectorizer', CountVectorizer(stop_words='english')),
    ('classifier', MultinomialNB())
])
model_pipeline.fit(X_train, y_train)
print("Model training complete.")

# 5. Save the Trained Model 🧠
joblib.dump(model_pipeline, 'sentiment_model.joblib')
print("Model has been saved as 'sentiment_model.joblib'. ✅")