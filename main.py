import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from styles import apply_styles
from analysis import analyze_response

# Page configuration
st.set_page_config(
    page_title="Special Education Response Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Login management
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "Tessagirl" and st.session_state["username"].lower() == "admin":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
            del st.session_state["username"]  # Don't store the username
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct
        return True

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
    # Define the analysis codes
    codes = [
        'Academic Language Support',
        'Grammar Support',
        'Content Knowledge Support',
        'Collaboration with Teachers',
        'Student Engagement',
        'Assessment of Language Proficiency',
        'Perceptions of Language Acquisition',
        'Perceived Challenges',
        'Innovative Practices',
        'Perceptions of Error'
    ]
    
    # Initialize a matrix to store code frequencies
    students = df['Student'].unique()
    matrix = np.zeros((len(students), len(codes)))
    
    # Fill the matrix with code frequencies
    for i, student in enumerate(students):
        student_data = df[df['Student'] == student]
        
        # Combine all responses for the student
        response_text = f"""
        Student: {student}
        
        Student Information Needed:
        {student_data['What student information do you need to plan the lesson?'].iloc[0]}
        
        Information from Other Teachers:
        {student_data['What information would you ask of the other fifth-grade teachers?'].iloc[0]}
        
        Student Engagement:
        {student_data['How would you ensure all students are engaged in the lesson?'].iloc[0]}
        
        Assessment Approach:
        {student_data['How would you assess the assignment?'].iloc[0]}
        
        Objectives Assessment:
        {student_data["How would you assess students' understanding of each of the objectives?"].iloc[0]}
        """
        
        # Analyze the response
        analysis_results = analyze_response(response_text)
        
        # Count code frequencies
        for j, code in enumerate(codes):
            if j < 6:  # Predetermined codes
                quotes = analysis_results['predetermined_codes'].get(code, ["No direct quote found"])
            else:  # Emergent codes
                quotes = analysis_results['emergent_codes'].get(code, ["No direct quote found"])
            
            # Count non-empty quotes
            valid_quotes = [q for q in quotes if q != "No direct quote found"]
            matrix[i, j] = len(valid_quotes)
    
    # Create the heatmap
    plt.figure(figsize=(15, 8))
    sns.heatmap(
        matrix,
        xticklabels=[code.replace(' Support', '').replace('Perceptions of ', '') for code in codes],
        yticklabels=students,
        cmap='YlOrRd',
        annot=True,
        fmt='.0f',
        cbar_kws={'label': 'Number of Relevant Quotes'}
    )
    plt.title('Response Analysis Code Frequency Heatmap')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return plt

def main():
    # Initialize session state for historical tracking
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = {}
        
    # Check authentication
    if not check_password():
        return
        
    # Add logout button in sidebar
    with st.sidebar:
        if st.button("Logout"):
            st.session_state["password_correct"] = False
            st.rerun()
    
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
    # Apply custom styles
    apply_styles()
    main()
