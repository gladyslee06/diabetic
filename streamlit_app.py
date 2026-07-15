import streamlit as st
import pandas as pd
import pickle
import random
import os
import base64
from PIL import Image
import requests
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Card-like containers */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .css-1r6slb0 {
        background-color: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Title styling */
    .title-text {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem;
    }
    
    .subtitle-text {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Input field styling - CONSISTENT HEIGHT */
    .stNumberInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem;
        transition: all 0.3s ease;
        height: 38px !important;
        min-height: 38px !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Fix for number input container to maintain consistent height */
    .stNumberInput > div {
        margin-bottom: 0 !important;
    }
    
    .stNumberInput > div > div {
        height: 38px !important;
        min-height: 38px !important;
    }
    
    /* Validation message container - FIXED HEIGHT to prevent shifting */
    .validation-message {
        min-height: 24px;
        height: 24px;
        margin-top: 2px;
        margin-bottom: 8px;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        padding: 0 8px;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    
    .validation-message-empty {
        min-height: 24px;
        height: 24px;
        margin-top: 2px;
        margin-bottom: 8px;
        visibility: hidden;
    }
    
    .validation-error {
        color: #f5576c;
        background-color: #fff0f0;
        border-left: 3px solid #f5576c;
    }
    
    .validation-success {
        color: #28a745;
        background-color: #f0fff0;
        border-left: 3px solid #28a745;
    }
    
    .validation-warning {
        color: #856404;
        background-color: #fff3cd;
        border-left: 3px solid #ffc107;
    }
    
    /* Fix spacing for input containers */
    .stNumberInput > label {
        margin-bottom: 0.2rem !important;
        font-weight: 500;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 1.2rem;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Mode toggle button styling */
    .mode-toggle-button > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
        font-size: 1rem;
        padding: 0.5rem 1.5rem;
    }
    
    .mode-toggle-button > button:hover {
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
    }
    
    /* Reset button styling */
    .reset-button > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
    }
    
    .reset-button > button:hover {
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.6);
    }
    
    /* BMI Category Cards */
    .bmi-underweight {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .bmi-normal {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .bmi-overweight {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .bmi-obese {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .bmi-value {
        font-size: 3rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .bmi-category {
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
    }
    
    .bmi-description {
        font-size: 1rem;
        color: rgba(0,0,0,0.7);
        margin-top: 0.5rem;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        padding: 0;
        border-bottom: 2px solid #e0e0e0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0;
        color: #666;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #333;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1a237e;
        font-weight: 600;
        background-color: transparent;
        border-bottom: 3px solid #1a237e;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        display: none;
    }
    
    /* BMI Chart */
    .bmi-chart {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    
    /* Info box styling */
    .info-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    /* Result container styling */
    .result-container {
        border-radius: 30px;
        padding: 40px 30px;
        min-height: 420px;
        height: 420px;
        max-height: 420px;
        border: 3px solid #333;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        animation: fadeIn 0.5s ease;
    }
    
    .result-container-high {
        border-color: #dc3545;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
    }
    
    .result-container-low {
        border-color: #28a745;
        background: linear-gradient(135deg, #f0fff4 0%, #e8f5e9 100%);
    }
    
    /* Meme container styling */
    .meme-container {
        border-radius: 30px;
        padding: 20px;
        min-height: 420px;
        height: 420px;
        max-height: 420px;
        border: 3px solid #333;
        text-align: center;
        animation: fadeIn 0.5s ease;
        background: white;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
    }
    
    .meme-container img {
        max-height: 250px;
        object-fit: contain;
        width: 100%;
        border-radius: 15px;
        margin: 10px 0;
        flex-shrink: 0;
    }
    
    /* Section header */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }
    
    /* Validation error box */
    .validation-error-box {
        background: #fff0f0;
        border-left: 4px solid #f5576c;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .validation-error-box li {
        color: #dc3545;
        margin: 0.3rem 0;
    }
    
    /* Fix for file uploader */
    .stFileUploader {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== Validation Functions ====================
def validate_pregnancies(value):
    """Validate pregnancies input"""
    if value < 0:
        return False, "Pregnancies cannot be negative."
    elif value > 20:
        return False, "Pregnancies should be 20 or less."
    return True, "✅ Valid"

def validate_glucose(value):
    """Validate glucose input"""
    if value < 40:
        return False, "Glucose level must be between 40 and 300 mg/dL."
    elif value > 300:
        return False, "Glucose level must be between 40 and 300 mg/dL."
    elif value == 0:
        return False, "Glucose level must be greater than 0."
    return True, "✅ Valid"

def validate_blood_pressure(value):
    """Validate blood pressure input"""
    if value < 40:
        return False, "Blood pressure must be between 40 and 180 mm Hg."
    elif value > 180:
        return False, "Blood pressure must be between 40 and 180 mm Hg."
    elif value == 0:
        return False, "Blood pressure must be greater than 0."
    return True, "✅ Valid"

def validate_skin_thickness(value):
    """Validate skin thickness input"""
    if value < 7:
        return False, "Skin thickness must be between 7 and 99 mm."
    elif value > 99:
        return False, "Skin thickness must be between 7 and 99 mm."
    elif value == 0:
        return False, "Skin thickness must be greater than 0."
    return True, "✅ Valid"

def validate_insulin(value):
    """Validate insulin input"""
    if value < 15:
        return False, "Insulin level must be between 15 and 900 mu U/ml."
    elif value > 900:
        return False, "Insulin level must be between 15 and 900 mu U/ml."
    elif value == 0:
        return False, "Insulin level must be greater than 0."
    return True, "✅ Valid"

def validate_bmi(value):
    """Validate BMI input"""
    if value < 10.0:
        return False, "BMI must be between 10.0 and 70.0."
    elif value > 70.0:
        return False, "BMI must be between 10.0 and 70.0."
    elif value == 0:
        return False, "BMI must be greater than 0."
    return True, "✅ Valid"

def validate_diabetes_pedigree(value):
    """Validate diabetes pedigree function"""
    if value < 0.078:
        return False, "Diabetes pedigree must be between 0.078 and 2.5."
    elif value > 2.5:
        return False, "Diabetes pedigree must be between 0.078 and 2.5."
    elif value == 0:
        return False, "Diabetes pedigree must be greater than 0."
    return True, "✅ Valid"

def validate_age(value):
    """Validate age input"""
    if value < 21:
        return False, "Age must be between 21 and 100 years."
    elif value > 100:
        return False, "Age must be between 21 and 100 years."
    return True, "✅ Valid"

# ==================== Load GIF Memes ====================
@st.cache_data
def load_memes():
    """Load meme files from the memes directory"""
    high_risk_gifs = []
    low_risk_gifs = []
    
    # Default fallback memes (URLs that work)
    default_high_risk = [
        "https://media1.tenor.com/m/1RjqsCqf6rYAAAAC/sad-cry.gif",
        "https://media1.tenor.com/m/NgUihdSSB2kAAAAC/sad-crying.gif",
        "https://media1.tenor.com/m/DtK5C88erWEAAAAC/oh-no-what.gif"
    ]
    
    default_low_risk = [
        "https://media1.tenor.com/m/71M3T1rP2mYAAAAC/happy-dance-happy.gif",
        "https://media1.tenor.com/m/pwR6WJ5ZLysAAAAC/celebration-dance.gif",
        "https://media1.tenor.com/m/n3THjO3Fw4YAAAAC/moonwalk-dance.gif"
    ]
    
    # Check if memes directory exists
    if os.path.exists("memes"):
        # Get all image files from memes directory
        image_extensions = ['.gif', '.jpg', '.jpeg', '.png', '.webp']
        all_images = []
        
        for file in os.listdir("memes"):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                all_images.append(os.path.join("memes", file))
        
        # Sort files and split into high and low risk
        if all_images:
            high_risk_gifs = [img for img in all_images if any(keyword in img.lower() for keyword in ['high', 'bad', 'sad', 'negative', 'risk'])]
            low_risk_gifs = [img for img in all_images if any(keyword in img.lower() for keyword in ['low', 'good', 'happy', 'positive', 'safe'])]
            
            # If no specific files found, split them alternately
            if not high_risk_gifs and not low_risk_gifs and all_images:
                mid = len(all_images) // 2
                low_risk_gifs = all_images[:mid]
                high_risk_gifs = all_images[mid:]
    
    # Use defaults if no images found
    if not high_risk_gifs:
        high_risk_gifs = default_high_risk
    
    if not low_risk_gifs:
        low_risk_gifs = default_low_risk
    
    return high_risk_gifs, low_risk_gifs

# Load memes
high_risk_gifs, low_risk_gifs = load_memes()

# ==================== Meme HTML Helper ====================
@st.cache_data(show_spinner=False)
def get_meme_img_html(selected_meme):
    """
    Build an <img> tag string for the meme so it can be embedded
    INSIDE the same st.markdown() call as the meme-container div.
    """
    if not selected_meme:
        return '<p style="color:#999;">🎭 No meme available</p>'
    try:
        if selected_meme.startswith("http"):
            response = requests.get(selected_meme, timeout=10)
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "image/gif")
                b64 = base64.b64encode(response.content).decode()
                return f'<img src="data:{content_type};base64,{b64}" alt="meme">'
            else:
                return '<p style="color:#999;">🎭 Meme could not be loaded</p>'
        else:
            if os.path.exists(selected_meme):
                ext = selected_meme.split(".")[-1].lower()
                mime = "image/gif" if ext == "gif" else f"image/{ext}"
                with open(selected_meme, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                return f'<img src="data:{mime};base64,{b64}" alt="meme">'
            else:
                return '<p style="color:#999;">🎭 Meme file not found</p>'
    except Exception:
        return '<p style="color:#999;">🎭 Meme could not be loaded</p>'

# ==================== Load Models ====================
@st.cache_resource
def load_models():
    """Load the trained model and scaler"""
    try:
        if os.path.exists("diabetes_model.pkl") and os.path.exists("scaler.pkl"):
            model = pickle.load(open("diabetes_model.pkl", "rb"))
            scaler = pickle.load(open("scaler.pkl", "rb"))
            return model, scaler
        else:
            st.warning("⚠️ Model files not found. Using a placeholder model for demonstration.")
            
            from sklearn.linear_model import LogisticRegression
            import numpy as np
            
            model = LogisticRegression()
            X_dummy = np.random.randn(100, 8)
            y_dummy = np.random.randint(0, 2, 100)
            model.fit(X_dummy, y_dummy)
            
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            scaler.fit(X_dummy)
            
            return model, scaler
    except Exception as e:
        st.error(f"⚠️ Error loading models: {str(e)}")
        return None, None

model, scaler = load_models()

# Initialize session state variables
if 'show_validation' not in st.session_state:
    st.session_state.show_validation = False

if 'show_result' not in st.session_state:
    st.session_state.show_result = False

if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

if 'selected_meme' not in st.session_state:
    st.session_state.selected_meme = None

# Input mode
if 'input_mode' not in st.session_state:
    st.session_state.input_mode = "Manual Input"

# Reset counter for forcing widget reinitialization
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def reset_app():
    """Reset all session state variables"""
    st.session_state.show_validation = False
    st.session_state.show_result = False
    st.session_state.prediction_result = None
    st.session_state.selected_meme = None
    # Increment reset counter to force widget reinitialization
    st.session_state.reset_counter += 1

def process_uploaded_file(uploaded_file):
    """Process uploaded CSV or Excel file and return the first row as values"""
    try:
        # Get file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # Read the file based on type
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            try:
                # Try with openpyxl engine first (for .xlsx)
                if file_extension == 'xlsx':
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                else:
                    # Try with xlrd for .xls
                    df = pd.read_excel(uploaded_file, engine='xlrd')
            except ImportError as e:
                if 'openpyxl' in str(e).lower():
                    return None, "openpyxl is not installed. Please run: pip install openpyxl"
                elif 'xlrd' in str(e).lower():
                    return None, "xlrd is not installed. Please run: pip install xlrd"
                else:
                    return None, f"Error reading Excel file: {str(e)}"
            except Exception as e:
                return None, f"Error reading Excel file: {str(e)}"
        else:
            return None, f"Unsupported file format: {file_extension}. Please upload CSV or Excel files."
        
        # Check if DataFrame is empty
        if df.empty:
            return None, "The uploaded file is empty."
        
        # Clean column names
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(' ', '')
        
        # Required columns
        required_columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                           'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        
        # Check for missing columns
        missing_cols = []
        for col in required_columns:
            if col not in df.columns:
                # Try case-insensitive match
                found = False
                for df_col in df.columns:
                    if df_col.lower() == col.lower():
                        df.rename(columns={df_col: col}, inplace=True)
                        found = True
                        break
                if not found:
                    missing_cols.append(col)
        
        if missing_cols:
            return None, f"Missing columns: {', '.join(missing_cols)}. Required columns: {', '.join(required_columns)}"
        
        # Get first row of data
        first_row = df.iloc[0]
        
        # Extract data with proper type conversion
        data = {
            'Pregnancies': int(first_row['Pregnancies']) if pd.notna(first_row['Pregnancies']) else 0,
            'Glucose': int(first_row['Glucose']) if pd.notna(first_row['Glucose']) else 0,
            'BloodPressure': int(first_row['BloodPressure']) if pd.notna(first_row['BloodPressure']) else 0,
            'SkinThickness': int(first_row['SkinThickness']) if pd.notna(first_row['SkinThickness']) else 0,
            'Insulin': int(first_row['Insulin']) if pd.notna(first_row['Insulin']) else 0,
            'BMI': float(first_row['BMI']) if pd.notna(first_row['BMI']) else 0.0,
            'DiabetesPedigreeFunction': float(first_row['DiabetesPedigreeFunction']) if pd.notna(first_row['DiabetesPedigreeFunction']) else 0.0,
            'Age': int(first_row['Age']) if pd.notna(first_row['Age']) else 0
        }
        
        return data, None
    except Exception as e:
        return None, f"Error processing file: {str(e)}"

# Create tabs
tab1, tab2 = st.tabs(["🩺 Diabetes Prediction", "⚖️ BMI Calculator"])

# ==================== TAB 1: Diabetes Prediction ====================
with tab1:
    # Header
    st.markdown('<div class="title-text">🩺 Diabetes Prediction System</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Early detection can save lives. Enter patient details below for risk assessment.</div>', unsafe_allow_html=True)

    # Input mode selection with buttons
    st.markdown("### 📝 Select Input Method")
    col_mode1, col_mode2, col_mode3, col_mode4 = st.columns([1, 1, 1, 1])
    
    with col_mode1:
        if st.button("✍️ Manual Input", use_container_width=True, key="btn_manual"):
            if st.session_state.input_mode != "Manual Input":
                st.session_state.input_mode = "Manual Input"
                reset_app()
                st.rerun()
    
    with col_mode2:
        if st.button("📤 Upload File", use_container_width=True, key="btn_upload"):
            if st.session_state.input_mode != "File Upload":
                st.session_state.input_mode = "File Upload"
                reset_app()
                st.rerun()
    
    # Show current mode indicator
    if st.session_state.input_mode == "Manual Input":
        st.info("✅ Currently in **Manual Input** mode")
    else:
        st.info("✅ Currently in **File Upload** mode")

    st.markdown("---")

    # ==================== MANUAL INPUT MODE ====================
    if st.session_state.input_mode == "Manual Input":
        # Create two columns for layout
        col1, col2 = st.columns([2, 1])

        with col1:
            # Create two columns for input fields
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown('<div class="section-header">📊 Personal Information</div>', unsafe_allow_html=True)
                
                # Pregnancies - Range: 0 to 20
                Pregnancies = st.number_input(
                    "🤰 Pregnancies",
                    min_value=0,
                    max_value=20,
                    value=0,
                    step=1,
                    help="Number of times pregnant (0-20)",
                    key=f"preg_{st.session_state.reset_counter}"
                )
                if st.session_state.show_validation:
                    preg_valid, preg_msg = validate_pregnancies(Pregnancies)
                    if preg_valid:
                        st.markdown(f'<div class="validation-message validation-success">{preg_msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="validation-message validation-error">❌ {preg_msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                
                # Glucose - Range: 40 to 300
                Glucose = st.number_input(
                    "🍬 Glucose Level",
                    min_value=0,
                    max_value=300,
                    value=0,
                    step=1,
                    help="Plasma glucose concentration (mg/dL) - Range: 40-300",
                    key=f"gluc_{st.session_state.reset_counter}"
                )
                if st.session_state.show_validation:
                    gluc_valid, gluc_msg = validate_glucose(Glucose)
                    if not gluc_valid:
                        st.markdown(f'<div class="validation-message validation-error">❌ {gluc_msg}</div>', unsafe_allow_html=True)
                    elif Glucose > 0:
                        st.markdown(f'<div class="validation-message validation-success">{gluc_msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                
                # Blood Pressure - Range: 40 to 180
                BloodPressure = st.number_input(
                    "❤️ Blood Pressure",
                    min_value=0,
                    max_value=180,
                    value=0,
                    step=1,
                    help="Diastolic blood pressure (mm Hg) - Range: 40-180",
                    key=f"bp_{st.session_state.reset_counter}"
                )
                if st.session_state.show_validation:
                    bp_valid, bp_msg = validate_blood_pressure(BloodPressure)
                    if not bp_valid:
                        st.markdown(f'<div class="validation-message validation-error">❌ {bp_msg}</div>', unsafe_allow_html=True)
                    elif BloodPressure > 0:
                        st.markdown(f'<div class="validation-message validation-success">{bp_msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                
                # Skin Thickness - Range: 7 to 99
                SkinThickness = st.number_input(
                    "📏 Skin Thickness",
                    min_value=0,
                    max_value=99,
                    value=0,
                    step=1,
                    help="Triceps skin fold thickness (mm) - Range: 7-99",
                    key=f"skin_{st.session_state.reset_counter}"
                )
                if st.session_state.show_validation:
                    skin_valid, skin_msg = validate_skin_thickness(SkinThickness)
                    if not skin_valid:
                        st.markdown(f'<div class="validation-message validation-error">❌ {skin_msg}</div>', unsafe_allow_html=True)
                    elif SkinThickness > 0:
                        st.markdown(f'<div class="validation-message validation-success">{skin_msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
            
            with col_right:
                st.markdown('<div class="section-header">🏥 Health Metrics</div>', unsafe_allow_html=True)
                
                # Insulin - Range: 15 to 900
                Insulin = st.number_input(
                    "💉 Insulin",
                    min_value=0,
                    max_value=900,
                    value=0,
                    step=1,
                    help="2-Hour serum insulin (mu U/ml) - Range: 15-900",
                    key=f"ins_{st.session_state.reset_counter}"
                )
                if st.session_state.show_validation:
                    ins_valid, ins_msg = validate_insulin(Insulin)
                    if not ins_valid:
                        st.markdown(f'<div class="validation-message validation-error">❌ {ins_msg}</div>', unsafe_allow_html=True)
                    elif Insulin > 0:
                        st.markdown(f'<div class="validation-message validation-success">{ins_msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                
                # BMI - Range: 10.0 to 70.0
                BMI = st.number_input(
                    "⚖️ BMI",
                    min_value=0.0,
                    max_value=70.0,
                    value=0.0,
                    step=0.1,
                    format="%.1f",
                    help="Body Mass Index - Range: 10.0-70.0",
                    key=f"bmi_{st.session_state.reset_counter}"
                )
                if st.session_state.show_validation:
                    bmi_valid, bmi_msg = validate_bmi(BMI)
                    if not bmi_valid:
                        st.markdown(f'<div class="validation-message validation-error">❌ {bmi_msg}</div>', unsafe_allow_html=True)
                    elif BMI > 0:
                        st.markdown(f'<div class="validation-message validation-success">{bmi_msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                
                # Diabetes Pedigree - Range: 0.078 to 2.5
                DiabetesPedigreeFunction = st.number_input(
                    "🧬 Diabetes Pedigree",
                    min_value=0.0,
                    max_value=2.5,
                    value=0.0,
                    step=0.001,
                    format="%.3f",
                    help="Diabetes pedigree function - Range: 0.078-2.5",
                    key=f"dpf_{st.session_state.reset_counter}"
                )
                if st.session_state.show_validation:
                    dpf_valid, dpf_msg = validate_diabetes_pedigree(DiabetesPedigreeFunction)
                    if not dpf_valid:
                        st.markdown(f'<div class="validation-message validation-error">❌ {dpf_msg}</div>', unsafe_allow_html=True)
                    elif DiabetesPedigreeFunction > 0:
                        st.markdown(f'<div class="validation-message validation-success">{dpf_msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                
                # Age - Range: 21 to 100
                Age = st.number_input(
                    "🎂 Age",
                    min_value=0,
                    max_value=100,
                    value=0,
                    step=1,
                    help="Age in years - Range: 21-100",
                    key=f"age_{st.session_state.reset_counter}"
                )
                if st.session_state.show_validation:
                    age_valid, age_msg = validate_age(Age)
                    if not age_valid:
                        st.markdown(f'<div class="validation-message validation-error">❌ {age_msg}</div>', unsafe_allow_html=True)
                    elif Age > 0:
                        st.markdown(f'<div class="validation-message validation-success">{age_msg}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="validation-message-empty"></div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="section-header">📋 Quick Stats</div>', unsafe_allow_html=True)
            
            # Display some statistics or information
            st.markdown("""
            <div class="info-box">
                <p style="margin:0;"><strong>🔍 About Diabetes</strong></p>
                <p style="margin:0; font-size:0.9rem; color:#666;">
                    Diabetes is a chronic condition affecting how your body turns food into energy. 
                    Early detection and proper management are crucial for preventing complications.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="info-box">
                <p style="margin:0;"><strong>📊 Risk Factors</strong></p>
                <ul style="font-size:0.9rem; color:#666; margin:0.5rem 0;">
                    <li>High glucose levels (> 140 mg/dL)</li>
                    <li>Elevated BMI (> 25)</li>
                    <li>Family history</li>
                    <li>Age over 45</li>
                    <li>High blood pressure</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Prediction button
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            predict_button = st.button("🔮 Predict Diabetes Risk", use_container_width=True, key="predict")

    # ==================== UPLOAD FILE MODE ====================
    else:
        st.markdown('<div class="section-header">📤 Upload Patient Data</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <p style="color: #666; margin-bottom: 1rem;">
            Upload a CSV or Excel file containing patient data. The first row will be used for prediction.
        </p>
        """, unsafe_allow_html=True)
        
        # Simple functional file uploader
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload a file containing patient data. The first row will be used for prediction.",
            key=f"uploader_{st.session_state.reset_counter}",
            accept_multiple_files=False
        )
        
        if uploaded_file is not None:
            # Process the uploaded file
            data, error = process_uploaded_file(uploaded_file)
            
            if error:
                st.error(f"❌ {error}")
            elif data is not None:
                st.success(f"✅ File '{uploaded_file.name}' processed successfully!")
                
                # Create a DataFrame for preview
                df_preview = pd.DataFrame([data])
                
                # Display data preview
                st.markdown("**📊 Data Preview (First Row):**")
                st.dataframe(df_preview, use_container_width=True)
                
                # Validate each field and show ONLY invalid validation messages
                st.markdown("**⚠️ Validation Errors (if any):**")
                
                validations = {
                    'Pregnancies': validate_pregnancies(data['Pregnancies']),
                    'Glucose': validate_glucose(data['Glucose']),
                    'BloodPressure': validate_blood_pressure(data['BloodPressure']),
                    'SkinThickness': validate_skin_thickness(data['SkinThickness']),
                    'Insulin': validate_insulin(data['Insulin']),
                    'BMI': validate_bmi(data['BMI']),
                    'DiabetesPedigreeFunction': validate_diabetes_pedigree(data['DiabetesPedigreeFunction']),
                    'Age': validate_age(data['Age'])
                }
                
                all_valid = True
                has_errors = False
                error_fields = []
                
                # Check for validation errors
                for field, (is_valid, message) in validations.items():
                    if not is_valid:
                        st.markdown(f'<div class="validation-message validation-error">❌ {field}: {message}</div>', unsafe_allow_html=True)
                        has_errors = True
                        all_valid = False
                        error_fields.append(field)
                
                # Check if all values are > 0 (except Pregnancies which can be 0)
                zero_values = []
                if data['Glucose'] == 0:
                    zero_values.append("Glucose")
                    error_fields.append("Glucose")
                if data['BloodPressure'] == 0:
                    zero_values.append("BloodPressure")
                    error_fields.append("BloodPressure")
                if data['SkinThickness'] == 0:
                    zero_values.append("SkinThickness")
                    error_fields.append("SkinThickness")
                if data['Insulin'] == 0:
                    zero_values.append("Insulin")
                    error_fields.append("Insulin")
                if data['BMI'] == 0:
                    zero_values.append("BMI")
                    error_fields.append("BMI")
                if data['DiabetesPedigreeFunction'] == 0:
                    zero_values.append("DiabetesPedigreeFunction")
                    error_fields.append("DiabetesPedigreeFunction")
                if data['Age'] == 0:
                    zero_values.append("Age")
                    error_fields.append("Age")
                
                if zero_values:
                    st.markdown(f'<div class="validation-message validation-error">⚠️ The following fields have zero values: {", ".join(zero_values)}</div>', unsafe_allow_html=True)
                    all_valid = False
                    has_errors = True
                
                # Show success message if no errors
                if not has_errors:
                    st.markdown('<div class="validation-message validation-success">✅ All fields are valid!</div>', unsafe_allow_html=True)
                
                # If there are errors, show reset options
                if has_errors:
                    st.warning("⚠️ Please fix the validation errors above. You can upload a corrected file or switch to manual input mode.")
                    
                    st.markdown("---")
                    st.markdown("**💡 Options to fix:**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Reset upload - clear the uploaded file
                        if st.button("🔄 Upload New File", use_container_width=True, key="reset_upload"):
                            reset_app()
                            st.rerun()
                    
                    with col2:
                        # Switch to manual mode
                        if st.button("✍️ Switch to Manual Input", use_container_width=True, key="switch_manual"):
                            st.session_state.input_mode = "Manual Input"
                            reset_app()
                            st.rerun()
                
                # Prediction button for uploaded data (only if valid)
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    predict_upload_button = st.button(
                        "🔮 Predict Risk from Uploaded Data", 
                        use_container_width=True, 
                        key="predict_upload", 
                        disabled=not all_valid
                    )
                
                if predict_upload_button and all_valid:
                    # Set the values from uploaded data
                    Pregnancies = data['Pregnancies']
                    Glucose = data['Glucose']
                    BloodPressure = data['BloodPressure']
                    SkinThickness = data['SkinThickness']
                    Insulin = data['Insulin']
                    BMI = data['BMI']
                    DiabetesPedigreeFunction = data['DiabetesPedigreeFunction']
                    Age = data['Age']
                    
                    if model is None or scaler is None:
                        st.error("⚠️ Model not loaded. Please check the model files.")
                    else:
                        try:
                            input_data = pd.DataFrame(
                                [[
                                    Pregnancies,
                                    Glucose,
                                    BloodPressure,
                                    SkinThickness,
                                    Insulin,
                                    BMI,
                                    DiabetesPedigreeFunction,
                                    Age
                                ]],
                                columns=[
                                    "Pregnancies",
                                    "Glucose",
                                    "BloodPressure",
                                    "SkinThickness",
                                    "Insulin",
                                    "BMI",
                                    "DiabetesPedigreeFunction",
                                    "Age"
                                ]
                            )

                            # Scale input
                            input_scaled = scaler.transform(input_data)

                            # Prediction
                            result = model.predict(input_scaled)
                            probability = model.predict_proba(input_scaled)

                            # Store result in session state
                            st.session_state.prediction_result = {
                                "result": result[0],
                                "probability": probability[0]
                            }
                            
                            # Select random meme based on result
                            if result[0] == 1:
                                st.session_state.selected_meme = random.choice(high_risk_gifs)
                            else:
                                st.session_state.selected_meme = random.choice(low_risk_gifs)
                            
                            st.session_state.show_result = True
                            st.rerun()
                                    
                        except Exception as e:
                            st.error(f"⚠️ An error occurred during prediction: {str(e)}")

    # ==================== DISPLAY RESULTS (Common for both modes) ====================
    if st.session_state.show_result and st.session_state.prediction_result is not None:
        
        result_data = st.session_state.prediction_result
        selected_meme = st.session_state.selected_meme
        
        # Create two columns for side by side display with equal heights
        left_col, right_col = st.columns(2, gap="large")
        
        # ================= LEFT COLUMN - Result =================
        with left_col:
            if result_data["result"] == 1:
                st.markdown(f"""
                <div class="result-container result-container-high">
                    <h2 style="color: #dc3545;">⚠️ High Risk of Diabetes</h2>
                    <div style="font-size: 2.5rem; font-weight: 700; margin: 1rem 0; color: #dc3545;">
                        {result_data['probability'][1]:.1%}
                    </div>
                    <p style="font-size: 1.1rem; color: #666;">
                        Please consult a healthcare professional for proper diagnosis and management.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-container result-container-low">
                    <h2 style="color: #28a745;">✅ Low Risk of Diabetes</h2>
                    <div style="font-size: 2.5rem; font-weight: 700; margin: 1rem 0; color: #28a745;">
                        {result_data['probability'][0]:.1%}
                    </div>
                    <p style="font-size: 1.1rem; color: #666;">
                        Continue maintaining a healthy lifestyle!
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # ================= RIGHT COLUMN - Meme =================
        with right_col:
            img_html = get_meme_img_html(selected_meme)
            
            if result_data["result"] == 1:
                caption = "😢 Don't worry! Early detection is important."
            else:
                caption = "🎉 Keep up the healthy lifestyle!"
            
            st.markdown(f"""
            <div class="meme-container">
                <h4 style="margin-bottom: 15px; color: #333;">🎭 Today's Meme</h4>
                {img_html}
                <hr style="width:100%; border: none; border-top: 1px solid #eee; margin: 15px 0;">
                <p style="color:#666; font-size:0.9rem; margin:0;">{caption}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # ================= RESET BUTTON UNDER BOTH BOXES =================
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="reset-button">', unsafe_allow_html=True)
            if st.button("🔄 Reset Prediction", use_container_width=True, key="reset_prediction"):
                reset_app()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ==================== TAB 2: BMI Calculator ====================
with tab2:
    st.markdown('<div class="title-text">⚖️ BMI Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-text">Calculate your Body Mass Index and understand your health status</div>', unsafe_allow_html=True)
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">📏 Enter Your Measurements</div>', unsafe_allow_html=True)
        
        # Unit selection
        unit_system = st.radio(
            "Select Unit System",
            ["Metric (kg/cm)", "Imperial (lbs/in)"],
            horizontal=True,
            key="unit_system"
        )
        
        st.markdown("---")
        
        if unit_system == "Metric (kg/cm)":
            weight = st.number_input(
                "⚖️ Weight (kg)",
                min_value=1.0,
                max_value=300.0,
                value=70.0,
                step=0.5,
                format="%.1f",
                key="weight_metric"
            )
            
            height_cm = st.number_input(
                "📏 Height (cm)",
                min_value=50.0,
                max_value=300.0,
                value=170.0,
                step=0.5,
                format="%.1f",
                key="height_metric"
            )
            
            # Calculate BMI
            if height_cm > 0:
                height_m = height_cm / 100
                bmi = weight / (height_m ** 2)
            else:
                bmi = 0
                
        else:  # Imperial
            weight = st.number_input(
                "⚖️ Weight (lbs)",
                min_value=1.0,
                max_value=660.0,
                value=154.0,
                step=0.5,
                format="%.1f",
                key="weight_imperial"
            )
            
            height_in = st.number_input(
                "📏 Height (inches)",
                min_value=20.0,
                max_value=120.0,
                value=67.0,
                step=0.5,
                format="%.1f",
                key="height_imperial"
            )
            
            # Calculate BMI
            if height_in > 0:
                bmi = (weight / (height_in ** 2)) * 703
            else:
                bmi = 0
        
        # Calculate button
        st.markdown("<br>", unsafe_allow_html=True)
        calculate_bmi = st.button("📊 Calculate BMI", use_container_width=True, key="calc_bmi")
    
    with col2:
        st.markdown('<div class="section-header">📊 BMI Result</div>', unsafe_allow_html=True)
        
        if calculate_bmi and weight > 0 and (height_cm > 0 or height_in > 0):
            # Determine BMI category
            if bmi < 18.5:
                category = "Underweight"
                color_class = "bmi-underweight"
                emoji = "⚠️"
                description = "You may need to gain weight. Consult a healthcare professional for guidance."
                icon = "🍽️"
            elif 18.5 <= bmi < 25:
                category = "Normal Weight"
                color_class = "bmi-normal"
                emoji = "✅"
                description = "Great job! Maintain your healthy lifestyle."
                icon = "💪"
            elif 25 <= bmi < 30:
                category = "Overweight"
                color_class = "bmi-overweight"
                emoji = "⚠️"
                description = "Consider adopting a healthier diet and increasing physical activity."
                icon = "🏃"
            else:
                category = "Obese"
                color_class = "bmi-obese"
                emoji = "🚨"
                description = "Please consult a healthcare professional for a comprehensive health plan."
                icon = "🩺"
            
            # Display BMI result
            st.markdown(f"""
            <div class="{color_class}">
                <div class="bmi-category">{emoji} {category}</div>
                <div class="bmi-value">{bmi:.1f}</div>
                <div class="bmi-description">{icon} {description}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display BMI chart
            st.markdown('<div class="section-header" style="margin-top:1rem;">📈 BMI Scale</div>', unsafe_allow_html=True)
            
            # Create progress bar style visualization
            bmi_display = min(bmi, 40)
            bmi_percentage = (bmi_display / 40) * 100
            
            st.markdown(f"""
            <div class="bmi-chart">
                <div style="position: relative; height: 30px; background: #f0f0f0; border-radius: 15px; overflow: hidden;">
                    <div style="position: absolute; left: 0; top: 0; height: 100%; width: {min(bmi_percentage, 100)}%; 
                         background: linear-gradient(90deg, #fcb69f, #a8edea, #ffd93d, #f5576c); 
                         border-radius: 15px; transition: width 0.8s ease;">
                    </div>
                    <div style="position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); 
                         font-weight: 600; font-size: 0.8rem; color: #333; text-shadow: 0 0 10px rgba(255,255,255,0.8);">
                        {bmi:.1f}
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.7rem; color: #666;">
                    <span>Underweight</span>
                    <span>Normal</span>
                    <span>Overweight</span>
                    <span>Obese</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display detailed BMI information
            with st.expander("📋 Detailed BMI Information", expanded=True):
                st.markdown(f"""
                **Your BMI:** {bmi:.1f}
                
                **Category:** {category}
                
                **Health Implications:**
                - Underweight (< 18.5): May indicate malnutrition, eating disorders, or other health issues
                - Normal (18.5 - 24.9): Healthy weight range for most adults
                - Overweight (25 - 29.9): Increased risk of health problems
                - Obese (≥ 30): High risk of health problems including diabetes, heart disease, and more
                
                **Note:** BMI is a screening tool and doesn't account for muscle mass, bone density, or overall body composition.
                """)
                
                # Health recommendations based on BMI
                if bmi < 18.5:
                    st.info("""
                    **Recommendations for Underweight:**
                    - 🥗 Eat nutrient-rich foods more frequently
                    - 💪 Strength training to build muscle mass
                    - 🩺 Consult a healthcare professional
                    - 🥑 Include healthy fats in your diet
                    - 🍚 Increase calorie intake with healthy options
                    """)
                elif 18.5 <= bmi < 25:
                    st.success("""
                    **Maintain Your Healthy Weight:**
                    - 🥦 Continue balanced nutrition
                    - 🏃‍♂️ Regular physical activity (150 min/week)
                    - 😴 Adequate sleep (7-9 hours)
                    - 🧘 Stress management
                    - 💧 Stay hydrated
                    """)
                elif 25 <= bmi < 30:
                    st.warning("""
                    **Tips for Weight Management:**
                    - 🥗 Reduce calorie intake gradually
                    - 🏃‍♂️ Increase physical activity
                    - 🍎 Choose whole foods over processed
                    - 💧 Stay hydrated
                    - 📊 Monitor portion sizes
                    - 🩺 Regular health checkups
                    """)
                else:
                    st.error("""
                    **Important Actions to Take:**
                    - 🩺 Schedule a comprehensive health checkup
                    - 🥗 Consult a nutritionist for a personalized diet plan
                    - 🏃‍♂️ Start with moderate exercise (consult your doctor first)
                    - 🩸 Monitor blood pressure and blood sugar levels
                    - 💊 Follow medical advice and prescribed treatments
                    - 🧘 Consider stress management techniques
                    """)
        else:
            st.info("👆 Enter your weight and height, then click 'Calculate BMI' to see your results.")
            
            # Show BMI reference chart
            st.markdown('<div class="section-header" style="margin-top:1rem;">📊 BMI Reference Chart</div>', unsafe_allow_html=True)
            
            bmi_data = {
                "Category": ["Underweight", "Normal", "Overweight", "Obese"],
                "BMI Range": ["< 18.5", "18.5 - 24.9", "25 - 29.9", "≥ 30"],
                "Status": ["⚠️ Needs Attention", "✅ Healthy", "⚠️ Caution", "🚨 High Risk"]
            }
            
            df_bmi = pd.DataFrame(bmi_data)
            st.table(df_bmi.style.hide(axis='index'))

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.8rem; padding: 1rem;">
    ⚕️ This tool is for educational purposes only. Always consult with a healthcare professional for medical advice.<br>
    🎭 Memes are for entertainment purposes and should not affect medical decisions.
</div>
""", unsafe_allow_html=True)
