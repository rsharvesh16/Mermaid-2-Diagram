import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-pro")

def convert_to_mermaid(text):
    # Start the Mermaid diagram definition
    mermaid_code = "graph TD;\n"

    # Split the text into sections (Actors and Use Cases)
    sections = text.split("**")

    # Process Actors and Use Cases sections
    for section in sections:
        lines = section.strip().split("\n")

        if len(lines) > 1:
            # Actor or Use Case section found
            title = lines[0].strip()

            # Add the actor or use case as a node
            mermaid_code += f"    {title}\n"

            # Add connections for each item under the actor or use case
            for item in lines[1:]:
                if item.strip():
                    # Remove triple backticks from each line
                    clean_item = item.strip().replace("`", "")
                    mermaid_code += f"    {title} --> {clean_item}\n"
    return mermaid_code

def generate_response(input_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([input_text, "", prompt])
    return response.text

def main():
    st.title('UML Diagram Generator')

    prompt = st.text_area("Enter prompt:", "")

    if st.button("Generate UML Diagram"):
        # Input prompt for expert
        input_prompt = """You are an expert in understanding The UML(Unified Modeling Language) Diagrams, Flowcharts, Class Diagrams,
        and All types of Diagrams required for making reports, flowcharts etc. When a User gives a prompt, Give the output
        to the requested UML Diagram"""
        
        # Call Google Gemini Pro API to generate response
        response = generate_response(prompt, input_prompt)
        gemini_text = response

        # Convert Gemini response to Mermaid.js code
        mermaid_code = convert_to_mermaid(gemini_text)

        # Display the Mermaid.js code
        st.text_area("Generated Mermaid.js Code:", mermaid_code, height=200)

if __name__ == '__main__':
    main()