import streamlit as st
import pandas as pd
from analysis import analyze_response
import styles
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import hashlib
import hmac

# Page configuration
st.set_page_config(
    page_title="Special Education Response Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Login management
def check_password(password):
    """Check if the password matches the stored hash."""
    # In a real application, use a secure password hash from the database
    # For this demo, we'll use a simple hash comparison
    correct_password = "Tessagirl"
    return hmac.compare_digest(password, correct_password)

def login():
    """Returns True if the user is logged in."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True

    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username.lower() == "admin" and check_password(password):
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password")
            return False
            
    return False

def logout():
    """Logs out the user."""
    st.session_state.logged_in = False
    st.rerun()
# Apply custom styles
styles.apply_styles()

def load_data(uploaded_file=None):
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_csv("Varied_PhD-Level_Responses.csv")
        
        # Remove any completely empty rows
        df = df.dropna(how='all')
        
        # Ensure all required columns exist
        required_columns = [
            'Student',
            'What student information do you need to plan the lesson?',
            'What information would you ask of the other fifth-grade teachers?',
            'How would you ensure all students are engaged in the lesson?',
            'How would you assess the assignment?',
            "How would you assess students' understanding of each of the objectives?"
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"Missing required columns: {', '.join(missing_columns)}")
            return None
            
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.error("Please ensure your CSV file has all required columns and valid data.")
        return None

def generate_heatmap(df):
    # Define the questions for analysis
    questions = [
        'What student information do you need to plan the lesson?',
        'What information would you ask of the other fifth-grade teachers?',
        'How would you ensure all students are engaged in the lesson?',
        'How would you assess the assignment?',
        "How would you assess students' understanding of each of the objectives?"
    ]
    
    # Initialize a matrix to store response lengths
    students = df['Student'].unique()
    matrix = np.zeros((len(students), len(questions)))
    
    # Fill the matrix with response lengths
    for i, student in enumerate(students):
        student_data = df[df['Student'] == student]
        for j, question in enumerate(questions):
            response = student_data[question].iloc[0]
            # Calculate complexity score based on response length
            words = str(response).split()
            matrix[i, j] = len(words)
    
    # Create the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(
        matrix,
        xticklabels=['Student Info', 'Teacher Input', 'Engagement', 'Assessment', 'Objectives'],
        yticklabels=students,
        cmap='YlOrRd',
        annot=True,
        fmt='.0f',
        cbar_kws={'label': 'Response Length (words)'}
    )
    plt.title('Response Analysis Heatmap')
    plt.tight_layout()
    
    return plt

def main():
    # Initialize session state for historical tracking
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = {}
        
    # Check login status
    if not login():
        return
        
    # Add logout button in sidebar
    with st.sidebar:
        if st.button("Logout"):
            logout()
    
    # Title
    st.title("Special Education Response Analysis")

    # Sidebar
    with st.sidebar:
        st.header("Data Options")
        
        # File uploader
        uploaded_file = st.file_uploader(
            "Upload custom response data (CSV)",
            type="csv",
            help="Upload your own CSV file with student responses"
        )
        
        if uploaded_file is not None:
            st.success("Custom data loaded successfully!")
            
        # Historical Analysis Section
        st.header("Analysis History")
        if st.session_state.analysis_history:
            selected_history = st.selectbox(
                "View Previous Analyses",
                options=list(st.session_state.analysis_history.keys()),
                format_func=lambda x: f"{x.split('_')[0]} - {x.split('_')[1]}"
            )
            if st.button("Load Selected Analysis"):
                st.session_state.analysis_results = st.session_state.analysis_history[selected_history]
                st.session_state.show_analysis = True

    # Load data
    df = load_data(uploaded_file)
    if df is None:
        return

    # Create tabs for different views
    analysis_tab, heatmap_tab = st.tabs(["Response Analysis", "Heatmap Analysis"])
    
    # Analysis tab content
    with analysis_tab:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.header("Select Student")
            
            # Get unique students from the DataFrame and add "All Students" option
            students = df['Student'].dropna().unique().tolist()
            students = ['All Students'] + students
            selected_student = st.selectbox("", students)

            # Analyze button placed above response section
            analyze_button = st.button("Analyze Responses")
            
            st.header("Student Response")
            
            # Get student responses
            if selected_student:
                if selected_student == 'All Students':
                    # Combine all student responses
                    all_responses = []
                    for _, student_data in df.iterrows():
                        response = f"""
                        Student: {student_data['Student']}
                        
                        Student Information Needed:
                        {student_data['What student information do you need to plan the lesson?']}
                        
                        Information from Other Teachers:
                        {student_data['What information would you ask of the other fifth-grade teachers?']}
                        
                        Student Engagement:
                        {student_data['How would you ensure all students are engaged in the lesson?']}
                        
                        Assessment Approach:
                        {student_data['How would you assess the assignment?']}
                        
                        Objectives Assessment:
                        {student_data["How would you assess students' understanding of each of the objectives?"]}
                        """
                        all_responses.append(response)
                    response_text = "\n\n".join(all_responses)
                else:
                    # Single student response
                    student_data = df[df['Student'] == selected_student].iloc[0]
                    response_text = f"""
                    "{selected_student}, 5th Grade Teacher"

                    Student Information:
                    {student_data['What student information do you need to plan the lesson?']}

                    Information from Other Teachers:
                    {student_data['What information would you ask of the other fifth-grade teachers?']}

                    Student Engagement:
                    {student_data['How would you ensure all students are engaged in the lesson?']}

                    Assessment Approach:
                    {student_data['How would you assess the assignment?']}

                    Objectives Assessment:
                    {student_data["How would you assess students' understanding of each of the objectives?"]}
                    """
                
                # Add a container with custom styling for the response text
                st.markdown(f"""
                    <div class="response-container">
                        <pre style="white-space: pre-wrap; font-family: sans-serif; margin: 0;">{response_text}</pre>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Handle analysis when button is clicked
                if analyze_button:
                    analysis_results = analyze_response(response_text)
                    st.session_state['analysis_results'] = analysis_results
                    st.session_state['show_analysis'] = True
                    
                    # Add to history with timestamp
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    history_key = f"{selected_student}_{timestamp}"
                    st.session_state.analysis_history[history_key] = analysis_results
                    st.success("Analysis completed and saved to history!")

        with col2:
            st.header("Analysis Results")
            
            if 'show_analysis' in st.session_state and st.session_state['show_analysis']:
                results = st.session_state['analysis_results']
                
                st.subheader("Predetermined Codes")
                codes = [
                    "Academic Language Support",
                    "Grammar Support",
                    "Content Knowledge Support",
                    "Collaboration with Teachers",
                    "Student Engagement",
                    "Assessment of Language Proficiency"
                ]
                
                for code in codes:
                    with st.expander(f"{code}", expanded=False):
                        quotes = results['predetermined_codes'].get(code, ["No direct quote found"])
                        for quote in quotes:
                            st.markdown(f"- {quote}")
                
                st.subheader("Emergent Codes")
                emergent_codes = [
                    "Perceptions of Language Acquisition",
                    "Perceived Challenges",
                    "Innovative Practices",
                    "Perceptions of Error"
                ]
                
                for code in emergent_codes:
                    with st.expander(f"{code}", expanded=False):
                        quotes = results['emergent_codes'].get(code, ["No direct quote found"])
                        for quote in quotes:
                            st.markdown(f"- {quote}")
                
                st.markdown("---")
                st.subheader("Export Analysis")
                
                if st.button("Export Analysis Results"):
                    # Get student name for export
                    student_identifier = "all_students" if selected_student == "All Students" else selected_student
                    
                    # Create DataFrame for predetermined codes
                    predetermined_df = pd.DataFrame([
                        {"Student": student_identifier, "Category": code, "Analysis": results['predetermined_codes'].get(code, "")}
                        for code in codes
                    ])
                    
                    # Create DataFrame for emergent codes
                    emergent_df = pd.DataFrame([
                        {"Student": student_identifier, "Category": code, "Analysis": results['emergent_codes'].get(code, "")}
                        for code in emergent_codes
                    ])
                    
                    # Combine both DataFrames
                    export_df = pd.concat([
                        predetermined_df.assign(Type="Predetermined"),
                        emergent_df.assign(Type="Emergent")
                    ])
                    
                    # Convert DataFrame to CSV for download
                    csv = export_df.to_csv(index=False)
                    filename = f"response_analysis_{student_identifier.lower().replace(' ', '_')}.csv"
                    st.download_button(
                        label="Download Analysis CSV",
                        data=csv,
                        file_name=filename,
                        mime="text/csv"
                    )

    # Heatmap tab content
    with heatmap_tab:
        st.header("Response Analysis Heatmap")
        st.write("This heatmap shows the depth of responses across different questions for each student.")
        
        if st.button("Generate Heatmap"):
            fig = generate_heatmap(df)
            st.pyplot(fig)
            plt.close()

            st.markdown("""
            ### Understanding the Heatmap
            - Each row represents a student
            - Each column represents a question category
            - The color intensity indicates the response length (number of words)
            - Darker colors represent longer, more detailed responses
            - Numbers show the exact word count for each response
            """)

if __name__ == "__main__":
    main()
