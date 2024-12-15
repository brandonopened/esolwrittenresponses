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

def load_data():
    try:
        df = pd.read_csv("student_engagement_responses.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    # Title
    st.title("Special Education Response Analysis")

    # Load data
    df = load_data()
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

        st.header("Student Response")
        
        # Get student responses
        if selected_student:
            if selected_student == 'All Students':
                # Combine all student responses
                all_responses = []
                for _, student_data in df.iterrows():
                    response = f"""
                    Student: {student_data['Student']}
                    Response:
                    {student_data['What student information do you need to plan the lesson?']}
                    """
                    all_responses.append(response)
                response_text = "\n\n".join(all_responses)
            else:
                # Single student response
                student_data = df[df['Student'] == selected_student].iloc[0]
                response_text = f"""
                "{selected_student}, 5th Grade Teacher"

                Responses:
                What student information do you need to plan the lesson?
                {student_data['What student information do you need to plan the lesson?']}
                """
            
            st.text_area("", value=response_text, height=300, disabled=True)
            
            if st.button("Analyze Responses", type="primary"):
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

if __name__ == "__main__":
    main()