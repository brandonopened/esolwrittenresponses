import streamlit as st
import pandas as pd
from analysis import analyze_response
import styles

# Page configuration
st.set_page_config(
    page_title="Special Education Response Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
styles.apply_styles()

def load_data(uploaded_file=None):
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_csv("Varied_PhD-Level_Responses.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
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

    # Load data
    df = load_data(uploaded_file)
    if df is None:
        return

    # Create two columns for layout
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
                    st.write(results['predetermined_codes'].get(code, "No relevant content found"))
            
            st.subheader("Emergent Codes")
            emergent_codes = [
                "Perceptions of Language Acquisition",
                "Perceived Challenges",
                "Innovative Practices",
                "Perceptions of Error"
            ]
            
            for code in emergent_codes:
                with st.expander(f"{code}", expanded=False):
                    st.write(results['emergent_codes'].get(code, "No relevant content found"))
            
            # Export functionality
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

if __name__ == "__main__":
    main()