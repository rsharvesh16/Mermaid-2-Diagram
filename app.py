import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import base64

load_dotenv()

# Configure Google API
genai.configure(api_key="YOUR_GOOGLE_API_KEY")

# Function to encode Mermaid graph into a base64 string
def mm(graph):
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    return "https://mermaid.ink/img/" + base64_string

# Function to generate Mermaid link from prompt
def generate_mermaid_link(prompt):
    # Input prompt for expert
    input_prompt = """You are an expert in understanding the prompts given by the user and convert it into mermaid code.
    you can achive this by writing mermaid code for the given user input. The user might ask you to make, flowcharts
    undertanding the generate the right mermaid code as per user needs!. use a proper syntax
    please avoid errors. write proper mermaid code for the flowchart and you have to only generate as per the instructions below

    Connect nodes with arrows to show relationships.
    Add styles and classes to nodes and arrows.
    Create subgraphs to group related nodes.
    Add comments using %% or <!-- -->.
    Use proper indentation for readability.

    Give it in the proper mermaid code format for showing in the st.image() in Streamlit.
    """

    # Call Google Gemini Pro API to generate response
    response = generate_response(prompt, input_prompt)
    gemini_text = response
    cleaned_code = gemini_text.replace("mermaid", "").replace("", "").replace("```", "")

    mermaid_link = mm(f"""
                      {cleaned_code}
                    """)

    return mermaid_link 

# Function to generate response using Gemini Pro API
def generate_response(input_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([input_text, "", prompt])
    return response.text

def star_rating(rating):
    """
    Generate a star rating HTML string based on the given rating.
    """
    # Define the maximum rating (number of stars)
    max_rating = 5
    # Limit rating to be within 0 to max_rating
    rating = min(max_rating, max(0, rating))
    
    # Create a string of filled stars based on the rating
    filled_stars = "★" * int(rating)
    # Create a string of empty stars for the remaining space
    empty_stars = "☆" * (max_rating - int(rating))
    
    # Combine filled and empty stars to form the star rating string
    star_rating_str = filled_stars + empty_stars
    
    return star_rating_str

# Main function
def main():
    
    st.write("""
<div style="background-color: #f0f0f0; padding: 20px; border-radius: 10px;">
    <h1 style="color: #333;">M2D - Flowchart Generator (Beta)</h1>
    <p style="color: #555;">Welcome to M2D Flowchart Generator! This tool allows you to generate flowchart diagrams based on your input prompts.</p>
</div>
""", unsafe_allow_html=True)
    # Dropdown button for choosing flowchart option
    option = st.selectbox("Choose Option", ["Flowchart"])

    if option == "Flowchart":
        prompt = st.text_area("Enter your prompt:", "")

        if st.button("Generate Flowchart"):
            mermaid_link = generate_mermaid_link(prompt)
            st.markdown('<h2 style="text-align: center;">Generated Flowchart</h2>', unsafe_allow_html=True)
            st.markdown(f'<img src="{mermaid_link}" alt="UML Diagram" style="display: block; margin-left: auto; margin-right: auto; max-width: 100%;" />', unsafe_allow_html=True)
            print(mermaid_link)
        
    rating = st.slider("Rate this app", min_value=0, max_value=5, step=1)
    # Display the star rating
    st.write(f"### Your Rating: {star_rating(rating)}")

if __name__ == '__main__':
    main()
