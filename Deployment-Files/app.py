import streamlit as st
import joblib
import pandas as pd

# Load the trained model pipeline (includes preprocessing)
model = joblib.load(r"C:\Users\user\OneDrive\Desktop\new\best_fit_model.pkl")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "ℹ️ Overview", "📊 Prediction"])

# ========
# HOME PAGE
# ========
if page == "🏠 Home":
    st.markdown(
        "<h1 style='color: #4CAF50; text-align: center;'>📱 Products Discount Data Analysis & Estimation</h1>",
        unsafe_allow_html=True
    )
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTfyBEp1ZKKov4PnnRkdkeXIVtsB6nf9H-6g&s",
        use_container_width=True
    )
    st.markdown("""
    ## Welcome to the Smartphone Discount Prediction
    This app helps you *predict the discount price* of smartphones
    based on their brand, RAM, storage, display size, battery, and camera details.

*💡 Why use this app?*
- 📊 Helps *e-commerce sellers* plan competitive discounts to attract more customers.
- 🛒 Assists *buyers* in estimating the best deal before making a purchase.
- 📈 Useful for *market analysis* and tracking *price trends* over time.
- 🧠 Supports *data-driven decision making* for better pricing strategies.
- ⏳ Saves *time* by predicting prices instantly without manual calculations.
- 🎯 Helps target *specific customer segments* with personalized discounts.
- 📦 Useful for *inventory clearance planning* by setting optimal discount rates.
- 🔍 Provides *insights into brand-wise pricing patterns* in the market.

Navigate to the *Prediction* tab from the sidebar to try it yourself!
    """)

# ========
# OVERVIEW PAGE
# ========
elif page == "ℹ️ Overview":
    st.title("📖 Project Overview")
    st.markdown("""
    ### 📌 Objective
    Predict the *Discount Price* of smartphones using machine learning.

    ### 📊 Dataset
    The model was trained on data scraped from:
    - *Amazon* 📦
    - *Flipkart* 🛒

    ### 📐 Features Used
    - *Brand* 🏷️
    - *RAM* (GB) 💾
    - *ROM* (GB) 📂
    - *Display Size* (inches) 📱
    - *Battery* (mAh) 🔋
    - *Front Camera (MP)* 🤳
    - *Back Camera (MP)* 📷

    ### ⚙️ How It Works
    1. Enter smartphone specifications.
    2. The app processes the input through the trained pipeline.
    3. The model predicts the *discount price*.

    ### 📈 Use Cases
    - Price strategy planning for e-commerce platforms.
    - Budget estimation for buyers.
    - Competitive market analysis.
    """)

# ========
# PREDICTION PAGE
# ========
elif page == "📊 Prediction":
    st.title("📊 Predict Smartphone Discount Price")
    input_features = {}

    # Brand dropdown
    brands = ['Samsung', 'Apple', 'Redmi', 'OnePlus', 'Realme', 'Vivo', 'Oppo', 'Motorola', 'Poco', 'Others']
    input_features['Brand'] = st.selectbox("Select Brand", brands)

    # Numeric inputs
    input_features['RAM'] = st.number_input("Enter RAM (GB)", min_value=0.0)
    input_features['ROM'] = st.number_input("Enter ROM (GB)", min_value=0.0)
    input_features['Display_Size'] = st.number_input("Enter Display Size (inches)", min_value=0.0)
    input_features['Battery'] = st.number_input("Enter Battery Capacity (mAh)", min_value=0.0)
    input_features['Front_Cam(MP)'] = st.number_input("Enter Front Camera (MP)", min_value=0.0)
    input_features['Back_Cam(MP)'] = st.number_input("Enter Back Camera (MP)", min_value=0.0)

    # Predict Button
    if st.button("🚀 Predict Discount Price"):
        df = pd.DataFrame([input_features])
        # Since we saved the preprocessing inside the pipeline in train.py,
        # we can directly pass the dataframe to model.predict()
        prediction = model.predict(df)[0]
        st.success(f"💰 Predicted Discount Price: ₹{prediction:,.2f}")
