import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ==== LOAD DATA ====
data = pd.read_csv("sign_data.csv")
print("Columns:", data.columns.tolist())  # debug

# Try to find the label column
if "label" in data.columns:
    label_col = "label"
elif "Label" in data.columns:
    label_col = "Label"
else:
    # assume first column is label
    label_col = data.columns[0]

print(f"Using '{label_col}' as label column")

X = data.drop(label_col, axis=1)
y = data[label_col]

# ==== SPLIT ====
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ==== TRAIN ====
clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train, y_train)

# ==== EVALUATE ====
y_pred = clf.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ==== SAVE ====
joblib.dump(clf, "sign_rf_model.pkl")
print("🎉 Model saved as sign_rf_model.pkl")
