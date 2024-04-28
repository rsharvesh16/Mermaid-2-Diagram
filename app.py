import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
import base64

# Configure Google API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-pro")

# def convert_to_mermaid(text):
#     # Start the Mermaid diagram definition
#     mermaid_code = "graph TD;\n"

#     # Split the text into sections (Actors and Use Cases)
#     sections = text.split("**")

#     # Process Actors and Use Cases sections
#     for section in sections:
#         lines = section.strip().split("\n")

#         if len(lines) > 1:
#             # Actor or Use Case section found
#             title = lines[0].strip()

#             # Add the actor or use case as a node
#             mermaid_code += f"    {title}\n"

#             # Add connections for each item under the actor or use case
#             for item in lines[1:]:
#                 if item.strip():
#                     # Remove triple backticks from each line
#                     clean_item = item.strip().replace("`", "")
#                     mermaid_code += f"    {title} --> {clean_item}\n"
#     return mermaid_code

import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import base64

load_dotenv()

# Configure Google API
genai.configure(api_key="AIzaSyBNNgDh-dr08FahrDZSZe1tpASuQFhZDog")
# model = genai.GenerativeModel("gemini-pro")

def mm(graph):
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    return "https://mermaid.ink/img/" + base64_string

def generate_mermaid_link(prompt):
    # Input prompt for expert
    input_prompt = """You are an expert in understanding The UML (Unified Modeling Language) diagrams, including:

        - Class Diagrams
        - Use Case Diagrams
        - Sequence Diagrams
        - Activity Diagrams
        - Component Diagrams
        - Flowchart

        When a user provides a prompt, you can generate Mermaid code for any of these diagrams based on their request and give it in the correct format for printing in streamlit using st.image()"""

    # Call Google Gemini Pro API to generate response
    response = generate_response(prompt, input_prompt)
    gemini_text = response
    cleaned_code = gemini_text.replace("mermaid", "").replace("", "").replace("```", "")

    mermaid_link = mm(f"""
                      {cleaned_code}
                    """)

    return mermaid_link 

def generate_response(input_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([input_text, "", prompt])
    return response.text

def main():
    st.title('UML Diagram Generator')

    prompt = st.text_area("Enter prompt:", "")

    if st.button("Generate UML Diagram"):
        mermaid_link = generate_mermaid_link(prompt)
        print(mermaid_link)
        st.image(mermaid_link)

if __name__ == '__main__':
    main()
