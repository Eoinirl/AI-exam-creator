
import streamlit as st
import json
import random
from fpdf import FPDF

# Load past paper questions
with open("past_papers.json") as f:
    past_questions = json.load(f)

st.title("AI Leaving Cert Exam Paper Generator")

# Select topics
topics = st.multiselect(
    "Select Topics", list(set([q['topic'] for q in past_questions]))
)

num_qs = st.number_input("Questions per topic", min_value=1, max_value=5, value=2)

if st.button("Generate Exam"):
    exam_questions = []

    for topic in topics:
        topic_qs = [q for q in past_questions if q["topic"] == topic]
        for _ in range(num_qs):
            q = random.choice(topic_qs)
            question_text = q["question"]
            marks = q["marks"]
            exam_questions.append(f"{question_text}\nMarking Scheme: {', '.join(marks)}")

    # Display questions
    for i, q in enumerate(exam_questions, 1):
        st.write(f"Q{i}:\n{q}\n")

    # Generate PDF
    if st.checkbox("Generate PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for i, q in enumerate(exam_questions, 1):
            pdf.multi_cell(0, 10, f"Q{i}:\n{q}\n")
        pdf_file = "AI_Exam_Paper.pdf"
        pdf.output(pdf_file)
        st.success(f"PDF generated: {pdf_file}")
        st.download_button("Download PDF", pdf_file, file_name=pdf_file)
