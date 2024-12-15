import streamlit as st

def apply_styles():
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Main container */
        .main {
            padding: 2rem;
        }
        
        /* Headers */
        h1 {
            color: #1E3A8A;
            font-size: 2.2rem;
            margin-bottom: 2rem;
        }
        
        h2 {
            color: #2563EB;
            font-size: 1.8rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        
        h3 {
            color: #3B82F6;
            font-size: 1.5rem;
            margin-top: 1rem;
            margin-bottom: 0.75rem;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-size: 1.1rem;
            color: #1E3A8A;
            background-color: #F3F4F6;
            border-radius: 4px;
            padding: 0.75rem;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #4B79F6;
            color: white;
            padding: 0.5rem 2rem;
            font-size: 1.1rem;
            border-radius: 4px;
            border: none;
            transition: background-color 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #3B82F6;
        }
        
        /* Text area styling */
        .stTextArea>div>div>textarea {
            background-color: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 4px;
            padding: 0.75rem;
            font-size: 1rem;
        }
        
        /* Select box styling */
        .stSelectbox>div>div {
            background-color: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)
