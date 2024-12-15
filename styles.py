import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* Main container */
        .main {
            padding: 1rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Headers */
        h1 {
            color: #262730;
            font-size: 2rem;
            margin-bottom: 1.5rem;
            font-weight: 600;
        }
        
        h2 {
            color: #262730;
            font-size: 1.2rem;
            margin-top: 1rem;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
        
        h3 {
            color: #262730;
            font-size: 1.1rem;
            margin-top: 0.75rem;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-size: 1rem;
            color: #262730;
            background-color: #ffffff;
            border: none;
            padding: 0.5rem;
            font-weight: normal;
        }
        
        .streamlit-expanderContent {
            padding: 0.75rem;
            background-color: #ffffff;
            border-radius: 0.25rem;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #4B79F6;
            color: white;
            padding: 0.5rem 1.5rem;
            font-size: 1rem;
            border-radius: 0.25rem;
            border: none;
            transition: all 0.2s;
        }
        
        .stButton>button:hover {
            background-color: #3B82F6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Text area styling */
        .stTextArea>div>div>textarea {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 0.25rem;
            padding: 0.75rem;
            font-size: 0.95rem;
            min-height: 200px;
        }
        
        /* Select box styling */
        .stSelectbox>div>div {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 0.25rem;
            padding: 0.25rem;
        }

        /* Expand/Collapse link styling */
        .css-1aumxhk {
            color: #4B79F6 !important;
            font-size: 0.9rem;
            text-decoration: none;
        }

        /* Custom styling for code categories */
        .code-category {
            margin-bottom: 1rem;
            border-radius: 0.25rem;
            background-color: #ffffff;
        }
        
        .code-category h3 {
            margin-bottom: 0.5rem;
            color: #262730;
            font-weight: 500;
        }

        /* Improve padding and spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Custom container for response text */
        .response-container {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 0.25rem;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
