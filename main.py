import streamlit as st
st.set_page_config(layout="wide")

# Define a dictionary to map button labels to Python file names
page_files = {
    "Home": "index",
    "FP1": "fp1",
    "FP2": "fp2",
    "FP3": "fp3",
    "Q": "q",
    "Race": "race"
}

session_numbers = {
    "Bahrain": 1,
    "Saudi Arabia": 2,
    "Australia": 3,
    "Japan": 4,
    "China": 5,
    "Miami": 6,
    "Emilia Romagna": 7,
    "Monaco": 8,
    "Canada": 9,
    "Spain": 10,
    "Austria": 11,
    "Silverstone": 12,
    "Hungary": 13,
    "SPA": 14,
    "Netherlands": 15,
    "Monza": 16,
    "Azerbaijan": 17,
    "Singapore": 18
}

# Custom CSS for centering and responsive layout
st.markdown("""
    <style>
        .centered {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        .button-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap; /* Allow buttons to wrap on smaller screens */
            gap: 10px; /* Space between buttons */
        }
        .stButton > button {
            padding: 10px 20px;
            font-size: 16px;
            flex: 1; /* Allow buttons to grow equally */
            min-width: 120px; /* Minimum width for buttons */
        }
        @media (max-width: 600px) {
            .stButton > button {
                font-size: 14px; /* Smaller font size on mobile */
            }
        }
        .stButton > button.selected {
            background-color: #4CAF50;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Create a container for the title
st.markdown('<h1 class="centered">Formula 1 Stats</h1>', unsafe_allow_html=True)
st.markdown('<p class="centered">Welcome to my Formula 1 stats page! Here, you can check all the data related to '
            'your favorite driver and gain insights into the weekend.</p>', unsafe_allow_html=True)
st.markdown('<p class="centered">IMPORTANT!!! SPRINT WEEKENDS DONT HAVE DATA FOR THE SPRINT QUALI AND SPRINT RACE.</p>'
            , unsafe_allow_html=True)

session_number = st.selectbox("Select GP", session_numbers.keys())

# Store which page to show
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = 'Home'

# Create a horizontal layout for buttons
col_count = len(page_files)
cols = st.columns(col_count)

# Create a button container with responsive layout
st.markdown('<div class="button-container">', unsafe_allow_html=True)

for idx, page in enumerate(page_files.keys()):
    with cols[idx]:
        if st.button(page, key=page):
            st.session_state.selected_page = page
        # Highlight the selected button
        if st.session_state.selected_page == page:
            st.markdown('<style>.stButton > button { background-color: #4CAF50; color: white; }</style>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Dynamically import and execute the selected page's script
selected_page = st.session_state.selected_page
page_module = __import__(page_files[selected_page])
with st.spinner("Getting Information"):
    page_module.render_page(session_numbers[session_number])
