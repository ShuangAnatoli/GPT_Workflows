import streamlit as st
from main import process_query

# Streamlit App
st.title("How-To Flowchart Generator")
st.write("Enter a 'How-To' question, and this app will generate a step-by-step flowchart for you.")

# User input
user_query = st.text_input("Enter your 'How-To' question:")

# Generate button
if st.button("Generate Flowchart"):
    if not user_query.strip():
        st.error("Please enter a valid question.")
    else:
        with st.spinner("Generating steps and flowchart..."):
            try:
                flowchart_path = process_query(user_query, output_path="generated_flowchart")
                st.image(flowchart_path, caption="Your Flowchart")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
