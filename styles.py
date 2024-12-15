import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        /* Main container */
        .main {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
            background-color: #f8fafc;
        }
        
        /* Headers */
        h1 {
            color: #1e293b;
            font-size: 2.25rem;
            margin-bottom: 2rem;
            font-weight: 700;
            letter-spacing: -0.025em;
        }
        
        h2 {
            color: #334155;
            font-size: 1.5rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        h3 {
            color: #475569;
            font-size: 1.25rem;
            margin-top: 1rem;
            margin-bottom: 0.75rem;
            font-weight: 500;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            font-size: 1rem;
            color: #4B79F6;
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 0.75rem 1rem;
            font-weight: 500;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
            transition: all 0.2s;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #f8fafc;
            border-color: #4B79F6;
        }
        
        .streamlit-expanderContent {
            padding: 1rem;
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #4B79F6;
            color: white;
            padding: 0.75rem 2rem;
            font-size: 1rem;
            font-weight: 500;
            border-radius: 0.5rem;
            border: none;
            transition: all 0.2s;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .stButton>button:hover {
            background-color: #3B82F6;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Text area styling */
        .stTextArea>div>div>textarea {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            padding: 1rem;
            font-size: 1rem;
            min-height: 200px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s;
        }
        
        .stTextArea>div>div>textarea:focus {
            border-color: #4B79F6;
            box-shadow: 0 0 0 3px rgba(75,121,246,0.1);
        }
        
        /* Select box styling */
        .stSelectbox>div>div {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            padding: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .stSelectbox>div>div:hover {
            border-color: #4B79F6;
        }

        /* Expand/Collapse link styling */
        .css-1aumxhk {
            color: #4B79F6 !important;
            font-size: 0.9rem;
            font-weight: 500;
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .css-1aumxhk:hover {
            color: #3B82F6 !important;
        }

        /* Custom styling for code categories */
        .code-category {
            margin-bottom: 1.5rem;
            border-radius: 0.5rem;
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        
        .code-category h3 {
            margin-bottom: 0.75rem;
            color: #334155;
            font-weight: 600;
        }

        /* Improve padding and spacing */
        .block-container {
            padding: 3rem 2rem;
            max-width: 1400px;
        }

        /* Custom container for response text */
        .response-container {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        /* Add spacing between sections */
        .stMarkdown {
            margin-bottom: 1.5rem;
        }
        
        /* Style the analysis results */
        .element-container {
            margin-bottom: 1.5rem;
        }
        </style>
        </style>
    """, unsafe_allow_html=True)
