import streamlit as st
import joblib
import pandas as pd
import os

# ---- ANIMATED & BRANDED BACKGROUND ----
st.markdown(r"""
    <style>
        body, .stApp {
            background: url('https://www.rhsmith.umd.edu/sites/default/files/research/featured/2025/04/online-marketplaces-beyond-the-number-of-buyers-and-sellers.jpg'), 
                        linear-gradient(120deg,#89f7fe 0%, #66a6ff 100%);
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Poppins', sans-serif;
        }
        .section {
            background-color: rgba(255,255,255,0.93);
            padding: 2em 2em 1.5em 2em;
            margin-bottom: 2em;
            border-radius: 15px;
            box-shadow: 1px 2px 24px #c9ddff;
            animation: fadeInBg 1.4s;
        }
        @keyframes fadeInBg {
            from {opacity: 0; transform: scale(0.98) translateY(28px);}
            to   {opacity: 1; transform: scale(1) translateY(0);}
        }
        .data-card {
            background-color: rgba(230,245,255,0.85);
            border-radius: 14px;
            box-shadow: 1px 2px 12px #e6ddff;
            padding: 0.6em 0.8em 0.4em 0.8em;
            margin-bottom: 2em;
        }
        .flipkart-logo {
            width: 110px;
            background: #fff;
            border-radius: 8px;
            box-shadow: 2px 3px 14px #aed6ff;
            margin-right: 12px;
            vertical-align:middle;
        }
        .amazon-logo {
            width: 110px;
            background: #fff;
            border-radius: 9px;
            box-shadow: 2px 3px 14px #eed6ff;
            vertical-align:middle;
        }
        /* Table header styling */
        .dataframe thead tr th {
            background: linear-gradient(90deg,#43cea2 10%,#185a9d 90%);
            color: #fff;
        }
    </style>
""", unsafe_allow_html=True)

# Model Loading
model = joblib.load(r"best_fit_model.pkl")

# Sidebar Navigation
st.sidebar.markdown(
    "<h2 style='color:#1abc9c; font-family:Space Mono;'>📌 Navigation</h2>",
    unsafe_allow_html=True
)
page = st.sidebar.radio("Go to", ["🏠 Home", "ℹ️ Overview", "📊 Prediction"])

# Divider Style
st.markdown(
    """<hr style="height:2px;border:none;color:#e6e6e6;background-color:#ededed;" /> """,
    unsafe_allow_html=True
)

# Data Loading
def load_data():
    try:
        df = pd.read_csv(r"Input.csv")
        return df
    except Exception as e:
        return None

# ---- HOME PAGE ----
if page == "🏠 Home":
    st.markdown(
        """
        <div style='display:flex; justify-content:center;align-items:center; margin-bottom:10px;'>
            <img src='https://www.citypng.com/public/uploads/preview/flipkart-logo-icon-hd-png-701751694706828v1habfry9b.png' class='flipkart-logo'/>
            <img src='https://i0.wp.com/magzoid.com/wp-content/uploads/2025/05/amazon-rebrand-2025_dezeen_2364_col_1-1.webp?resize=1200%2C675&ssl=1' class='amazon-logo'/>
        </div>
        <h1 style='
            background: linear-gradient(90deg, #43cea2 0%, #185a9d 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3.2rem;
            font-family: "Poppins", sans-serif;
            text-align: center;
            animation: fadeInBg 1.1s;
        '>📱 Products Discount Data Analysis & Estimation</h1>
        """, unsafe_allow_html=True
    )
    st.markdown("""
        <div class='section' style='animation:fadeInBg 1.5s;'>
            <div style='font-size:1.23rem; text-align:center;'>
                <b style="color:#2d3436;">Welcome to the <span style="color:#0984e3;">Smartphone Discount Prediction</span></b><br>
                This app helps you <span style="color:#26a69a;"><b>predict the discount price</b></span> of smartphones
                with real market data from <span style='color:#ffab00;'>Amazon</span> & <span style='color:#2874f0;'>Flipkart</span>!
            </div>
            <ul style="font-size: 1.11rem; color: #555;">
                <li>📊 <span style="color:#00b894;">Sellers</span>: Plan competitive discounts & strategies.</li>
                <li>🛒 <span style="color:#ff7675;">Buyers</span>: Estimate the best smartphone deals.</li>
                <li>📈 <span style="color:#6c5ce7;">Market Analysis</span>: Track discount trends.</li>
                <li>🧠 <span style="color:#00cec9;">Data-driven</span> pricing & deals.</li>
                <li>⏳ Predict prices <span style="color:#0984e3;">instantly</span>—no manual guesswork.</li>
                <li>🎯 <span style="color:#d35400;">Target</span> segments with smart offers.</li>
                <li>📦 <span style="color:#2d3436;">Clear inventory</span> with optimal discounts.</li>
                <li>🔍 <span style="color:#6ab04c;">Brand insights</span> for budget planning.</li>
            </ul>
            <div style="text-align:center; font-size:1.05rem; margin-top:1em;">
                Go to the <b>Prediction</b> tab to try for your specs!
            </div>
        </div>
    """, unsafe_allow_html=True)
    # Data Preview Block (animated)
    st.markdown(
        "<h3 style='color:#185a9d; font-family:Poppins;'>📊 Latest Smartphone Discount Data</h3>",
        unsafe_allow_html=True
    )
    df = load_data()
    if df is not None:
        st.markdown("<div class='data-card' style='animation:fadeInBg 1.4s;'>", unsafe_allow_html=True)
        with st.expander("Click to view smartphone data table ⬇", expanded=True):
            st.dataframe(df.head(20), use_container_width=True, height=420)
            if df.shape[0]>20:
                st.info(f"Showing 20 of {df.shape[0]:,} rows. Download the file for full data!")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Data file not found or format error. Please check file location. (Input.csv)")

# ---- OVERVIEW PAGE ----
elif page == "ℹ️ Overview":
    st.markdown("""
        <style>
            .animated-section {
                animation: fadeInBg 1.4s;
                opacity: 1;
                color: #18304b !important;
            }
        </style>
        <h2 style='color:#0984e3; font-size:2.4rem; font-family:Poppins;'>📖 Project Overview</h2>
        <div class='section animated-section'>
            <div style='font-size:1.2rem; margin-bottom:1.5em;'>
                <b>Objective:</b> Predict the <span style='color:#26a69a;font-weight:bold;'>Discount Price</span> of smartphones using ML.<br>
                <img src='https://mir-s3-cdn-cf.behance.net/project_modules/fs/0e206786775091.6090e06ac2a16.gif' class='flipkart-logo'/>
                <img src='https://cdn.dribbble.com/userupload/33976764/file/original-b0b9939526b22e903102754acf37c0dc.gif' class='amazon-logo'/>
            </div>
            <div style='margin-bottom:1em;'>
                <b>Dataset:</b><br>
                Data scrapped from e-commerce leaders:
                <ul>
                    <li>Amazon 📦</li>
                    <li>Flipkart 🛒</li>
                </ul>
            </div>
            <hr>
            <div style='margin-bottom:1em;'>
                <b>Features Used:</b>
                <ul>
                    <li>Brand 🏷️, Model, RAM (GB)</li>
                    <li>ROM (GB), Display Size (inches)</li>
                    <li>Battery (mAh), Front/Back Camera (MP)</li>
                </ul>
            </div>
            <div style='margin-bottom:1em;'>
                <b>How It Works:</b>
                <ol>
                    <li>Pick smartphone specs</li>
                    <li>Model processes and predicts</li>
                    <li>See your <span style='color:#27ae60;font-weight:bold;'>discount price</span> instantly</li>
                </ol>
            </div>
            <div>
                <b>Use Cases:</b>
                <ul>
                    <li>Seller discount planning & analysis</li>
                    <li>Buyer deal & budget estimator</li>
                    <li>Competitive intelligence</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif page == "📊 Prediction":
    st.markdown("""
        <style>
        .stApp section [data-testid="stMarkdownContainer"] h2, 
        .stApp section [data-testid="stMarkdownContainer"] h3, 
        .stApp section [data-testid="stMarkdownContainer"] h1,
        .stApp div.stButton button {
            color: #ffffff !important;  /* White font */
            text-shadow: 1.5px 1.5px 2.5px #000000a0; /* subtle black shadow */
        }
        </style>
    """, unsafe_allow_html=True)

    df = load_data()
    if df is None:
        st.error("Data file not found or format error. Please check file location. (Input.csv)")
    else:
        brands = sorted(df['Brand'].dropna().unique())
        selected_brand = st.selectbox("Select Brand", brands)

        filtered_models = df[df['Brand'] == selected_brand]['Brand_Model'].dropna().unique()
        selected_model = st.selectbox("Select Model", filtered_models)

        df_sub = df[(df['Brand'] == selected_brand) & (df['Brand_Model'] == selected_model)]

        available_rams = sorted(df_sub['RAM'].astype(int).unique())
        available_roms = sorted(df_sub['ROM'].astype(int).unique())

        ram = st.selectbox("Select RAM (GB)", available_rams)
        rom = st.selectbox("Select ROM (GB)", available_roms)

        # Select exact model details or fallback to first row
        specs = df_sub[(df_sub['RAM'].astype(int) == ram) & (df_sub['ROM'].astype(int) == rom)]
        if not specs.empty:
            model_details = specs.iloc[0]
        else:
            model_details = df_sub.iloc  # fallback to first available

        # Get min display size BEFORE using it
        min_display_size = df_sub['Display_Size'].min()

        display_size = st.number_input(
            "Display Size (inches)",
            min_value=0.0,
            value=float(model_details['Display_Size']),
            step=0.1,
            format="%.2f",
            help=f"Minimum display size available: {min_display_size:.2f} inches"
        )

        if display_size < min_display_size:
            st.warning(
                f"⚠️ Small display size ({display_size:.2f} inches) is not available for the selected model. Minimum available is {min_display_size:.2f} inches.")

        battery = st.number_input("Battery Capacity (mAh)", min_value=0, value=int(model_details['Battery']), step=100)
        front_cam = st.number_input("Front Camera (MP)", min_value=0, value=int(model_details['Front_Cam(MP)']), step=1)
        back_cam = st.number_input("Back Camera (MP)", min_value=0, value=int(model_details['Back_Cam(MP)']), step=1)

        input_features = {
            'Brand': selected_brand,
            'RAM': int(ram),
            'ROM': int(rom),
            'Display_Size': display_size,
            'Battery': battery,
            'Front_Cam(MP)': front_cam,
            'Back_Cam(MP)': back_cam
        }

        if st.button("🚀 Predict Discount Price", help="Get instant prediction based on selected specs!"):
            input_df = pd.DataFrame([input_features])
            prediction = model.predict(input_df)[0]
            st.success(f"💰 Predicted Discount Price: ₹{prediction:,.2f}", icon="✅")
            st.markdown(
                f"<span style='font-size:1.6rem;color:#27ae60;'>💰 Predicted: <b>₹{prediction:,.2f}</b></span>",
                unsafe_allow_html=True
            )
            st.balloons()
            st.markdown(
                "<div style='text-align:center;font-size:1.07rem;'>🎉 Find your best smartphone deal!<br>Results based on Amazon & Flipkart data.</div>",
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

