import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit.components.v1 as components

TEMPLATE_PATH = "templates/GoogleDocTemplate.html"
OUTPUT_PATH = "templates/GoogleDocTemplate_modified.html"

st.title("AI HTML Agent: Edit with Natural Language")

# Load .env and API key

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("Please add your OpenAI API key to the .env file as OPENAI_API_KEY.")
    st.stop()
client = OpenAI(api_key=api_key)

# Load HTML into session state if not already loaded
if "edited_html" not in st.session_state:
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        st.session_state.edited_html = f.read()


# User instruction
instruction = st.text_area(
    "Describe what you want to change in the HTML (e.g., 'Move the test data section above the images, make all headings blue'):"
)

# Generate button to let AI modify HTML
if st.button("Generate (AI Modify HTML)") and instruction.strip():
    with st.spinner("AI is modifying your HTML..."):
        prompt = f"""
You are an expert /CSS editor. Given the following HTML document, modify it according to the user's instruction. Return the modified HTML and styling changes. Also make sure if user requests adding new data or sections these are added and formatted properly and concistently with the document. 
Do not send back any messages to the user about what is done, just the modified HTML.
User instruction: {instruction}

HTML:
{st.session_state.edited_html}
"""
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_html = response.choices[0].message.content.strip()
        st.session_state.edited_html = ai_html
        st.success("AI updated the HTML! Preview below.")

# Editable text area for the whole HTML (always shows latest)
# edited_html = st.text_area(
#     "Edit HTML Source (optional, you can also edit manually before saving)",
#     value=st.session_state.edited_html,
#     height=600,
#     key="html_editor"
# )

# Update session state if manual edit
# if edited_html != st.session_state.edited_html:
#     st.session_state.edited_html = edited_html

# Save changes
if st.button("Save Changes"):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(st.session_state.edited_html)
    st.success(f"Saved to {OUTPUT_PATH}")
    st.markdown(f"[Download modified HTML]({OUTPUT_PATH})")

# Preview the HTML directly in Streamlit (best possible in-app rendering)
# TODO update to render images and styles properly 
st.markdown("### Preview (in-app)")
components.html(
    st.session_state.edited_html,
    height=650,
    scrolling=True
)
