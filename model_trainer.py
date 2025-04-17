import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def train_and_save_model():
    df = pd.read_csv("Training.csv")

    X = df.drop(columns=['prognosis'])
    y = df['prognosis']

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Save models
    with open("model.pkl", "wb") as f:
        pickle.dump(clf, f)
    with open("symptom_list.pkl", "wb") as f:
        pickle.dump(list(X.columns), f)
    with open("label_encoder.pkl", "wb") as f:
        pickle.dump(label_encoder, f)

    # Evaluate
    y_pred = clf.predict(X_test)
    print("Model trained and saved!")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

if __name__ == "__main__":
    train_and_save_model()
  
