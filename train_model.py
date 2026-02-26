import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

def train_and_save_model():
    print("Loading training data...")
    
    # 1. Load the CSV we just created
    try:
        df = pd.read_csv("training_data.csv")
    except FileNotFoundError:
        print("Error: Could not find 'training_data.csv'. Make sure it is in the same folder.")
        return

    print("Training the classification model...")

    # 2. Convert text descriptions into numerical vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['Description'])
    y = df['Category']

    # 3. Train the Naive Bayes Classifier
    model = MultinomialNB()
    model.fit(X, y)

    # 4. Save the trained model and vectorizer to disk
    joblib.dump(model, 'expense_model.pkl')
    joblib.dump(vectorizer, 'expense_vectorizer.pkl')

    print("Success! The AI brain has been trained and saved.")

if __name__ == "__main__":
    train_and_save_model()