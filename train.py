# train.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

# ====================
# 1️⃣ Load the dataset
# ====================
# Replace with your dataset file
data = pd.read_csv(r"C:\Users\user\OneDrive\Desktop\new\data\Cleaned_ecommerce_data.csv")

# Example expected columns:
# Brand, RAM, ROM, Display_Size, Battery, Front_Cam(MP), Back_Cam(MP), Discount_Price

# ====================
# 2️⃣ Features & Target
# ====================
features = ['Brand', 'RAM', 'ROM', 'Display_Size', 'Battery', 'Front_Cam(MP)', 'Back_Cam(MP)']
target = 'Discount_Price'

X = data[features]
y = data[target]

# ====================
# 3️⃣ Split Data
# ====================
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ====================
# 4️⃣ Preprocessing + Model
# ====================
# OneHotEncode "Brand" column
categorical_features = ['Brand']
numeric_features = ['RAM', 'ROM', 'Display_Size', 'Battery', 'Front_Cam(MP)', 'Back_Cam(MP)']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
        ('num', 'passthrough', numeric_features)
    ]
)

# Example model - You can change to XGB, Linear Regression, etc.
model = RandomForestRegressor(n_estimators=200, random_state=42)

# Pipeline = Preprocessing + Model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', model)
])

# ====================
# 5️⃣ Train the model
# ====================
pipeline.fit(X_train, y_train)

# ====================
# 6️⃣ Evaluate
# ====================
y_pred = pipeline.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"✅ Model trained")
print(f"📉 Mean Squared Error: {mse:.2f}")
print(f"📈 R² Score: {r2:.2f}")

# ====================
# 7️⃣ Save the model
# ====================
joblib.dump(pipeline, "best_fit_model.pkl")
print("💾 Model saved as best_fit_model.pkl")
