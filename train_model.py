import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import glob

def train_and_save_model():
    print("Loading all training data CSV files...")
    
    all_data = []
    
    # Find active training data CSV files
    csv_files = glob.glob("training_data*.csv")
    
    if not csv_files:
        print("Error: Could not find any 'training_data*.csv' files.")
        return
        
    for file in csv_files:
        try:
            # Load CSV, skipping malformed lines
            temp_df = pd.read_csv(file, on_bad_lines='skip')
            # Normalize column names
            if 'Transaction_Text' in temp_df.columns and 'Label' in temp_df.columns:
                temp_df.rename(columns={'Transaction_Text': 'Description', 'Label': 'Category'}, inplace=True)
                
            if 'Description' in temp_df.columns and 'Category' in temp_df.columns:
                # Merge variations into standard categories
                temp_df['Category'] = temp_df['Category'].replace({'Investments': 'Investment'})
                all_data.append(temp_df[['Description', 'Category']])
                print(f"Loaded {len(temp_df)} records from {file}")
            else:
                print(f"Warning: {file} is missing required columns. Skipping.")
        except Exception as e:
            print(f"Error loading {file}: {e}")
            
    if not all_data:
        print("Error: No valid training data found inside the CSVs.")
        return
        
    df = pd.concat(all_data, ignore_index=True)
    df = df.dropna(subset=['Description', 'Category'])
    print(f"Total training size: {len(df)} records")

    print("Evaluating the classification model...")

    # Split dataset into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(df['Description'], df['Category'], test_size=0.2, random_state=42)

    # Vectorize text descriptions
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Train Naive Bayes model on training subset
    test_model = MultinomialNB()
    test_model.fit(X_train_vec, y_train)
    
    # Evaluate model accuracy
    y_pred = test_model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n====================================")
    print(f"MODEL ACCURACY: {acc * 100:.2f}%")
    print(f"====================================\n")
    
    print("Detailed Classification Report (where the model struggles):")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    print("\nRetraining model using 100% of the dataset for final deployment...")
    X_full = vectorizer.fit_transform(df['Description'])
    y_full = df['Category']
    final_model = MultinomialNB()
    final_model.fit(X_full, y_full)

    # Persist the final model and vectorizer
    joblib.dump(final_model, 'expense_model.pkl')
    joblib.dump(vectorizer, 'expense_vectorizer.pkl')

    print("Success! The highly accurate final model has been saved.")

if __name__ == "__main__":
    train_and_save_model()