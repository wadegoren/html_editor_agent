import streamlit as st
from utils import fill_template
import pdfkit
import os

TEMPLATE_PATH = "templates/blank_alta_template.html"
OUTPUT_HTML = "filled_template.html"
OUTPUT_PDF = "filled_template.pdf"

st.title("One-Pager Generator")

# Example fields - you can add more as needed
name = st.text_input("Name")
date = st.date_input("Date")
description = st.text_area("Description")

if st.button("Generate One-Pager"):
    # Read the HTML template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    # Fill the template
    filled_html = fill_template(html, {"name": name, "date": date, "description": description})
    # Save filled HTML
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(filled_html)
    st.success("HTML generated!")
    st.markdown(f"[Download HTML]({OUTPUT_HTML})")
    # Convert to PDF
    pdfkit.from_file(OUTPUT_HTML, OUTPUT_PDF)
    st.markdown(f"[Download PDF]({OUTPUT_PDF})")
    st.markdown("---")
    st.markdown(filled_html, unsafe_allow_html=True)
