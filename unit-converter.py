import streamlit as st
import pint

# Set page title and icon
st.set_page_config(page_title="🚀 Unit Converter", page_icon="🔄", layout="centered")

# Pint library for unit conversion
ureg = pint.UnitRegistry()

# Define custom CSS for better UI
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            color: #ffffff;
            background: linear-gradient(90deg, #00b4db, #5b2cff);
            font-size: 36px;
            font-weight: 700;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .stButton>button {
            background: linear-gradient(90deg, #00b4db, #5b2cff);
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            padding: 12px;
            width: 100%;
            border: none;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            transition: all 0.2s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #5b2cff, #00b4db);
            transform: scale(1.03);
        }
        .stTextInput>div>div>input, .stSelectbox>div {
            border-radius: 10px;
            border: 2px solid #00b4db;
            padding: 10px;
            font-size: 16px;
        }
        .stMarkdown {
            color: #333333;
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Unit Categories
unit_categories = {
    "📏 Length": ["meter", "kilometer", "centimeter", "millimeter", "mile", "yard", "foot", "inch"],
    "🌡 Temperature": ["celsius", "fahrenheit", "kelvin"],
    "📐 Area": ["square_meter", "square_kilometer", "square_centimeter", "square_millimeter"],
    "🧊 Volume": ["liter", "milliliter", "cubic_meter", "cubic_centimeter", "gallon", "quart", "pint", "cup"],
    "⚖ Weight": ["gram", "kilogram", "milligram", "pound", "ounce"],
    "⏳ Time": ["second", "minute", "hour", "day", "week", "month", "year"]
}

# UI Section
st.markdown("<div class='title'>🔄 Unit Converter</div>", unsafe_allow_html=True)

st.subheader("Select Conversion Type")
category = st.selectbox("Category", list(unit_categories.keys()))

col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From Unit", unit_categories[category])
with col2:
    to_unit = st.selectbox("To Unit", unit_categories[category])

value = st.number_input("Enter Value:", format="%.6f", step=0.1)

# Temperature Conversion
def convert_temperature(value, from_unit, to_unit):
    conversions = {
        ("celsius", "fahrenheit"): lambda x: (x * 9/5) + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
        ("celsius", "kelvin"): lambda x: x + 273.15,
        ("kelvin", "celsius"): lambda x: x - 273.15,
        ("fahrenheit", "kelvin"): lambda x: (x - 32) * 5/9 + 273.15,
        ("kelvin", "fahrenheit"): lambda x: (x - 273.15) * 9/5 + 32
    }
    return conversions.get((from_unit, to_unit), lambda x: x)(value)

# Convert
if st.button("Convert 🔄"):
    try:
        if category == "🌡 Temperature":
            result = convert_temperature(value, from_unit, to_unit)
        else:
            result = (value * ureg(from_unit)).to(to_unit).magnitude

        st.success(f"✅ {value} {from_unit} = {round(result, 4)} {to_unit}")
        st.session_state.history.append(f"{value} {from_unit} → {round(result, 4)} {to_unit}")
    except Exception as e:
        st.error(f"⚠ Conversion error: {e}")

# History
st.subheader("📜 Conversion History")
if st.session_state.history:
    for entry in st.session_state.history[::-1]:
        st.markdown(f"✅ {entry}")
    if st.button("Clear History ❌"):
        st.session_state.history = []
