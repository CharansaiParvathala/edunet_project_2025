# main_app.py

import streamlit as st
from diagnosis_engine import predict_disease
from fpdf import FPDF
import datetime

# Title
st.set_page_config(page_title="AI Medical Diagnosis", layout="centered")
st.title("AI-Powered Medical Diagnosis System")
st.markdown("---")

# Sidebar Info
st.sidebar.title("Patient Info")
name = st.sidebar.text_input("Full Name")
age = st.sidebar.number_input("Age", min_value=1, max_value=120, step=1)
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
consult_date = st.sidebar.date_input("Consultation Date", datetime.date.today())

# Symptoms List (subset shown here; use full list in production)
all_symptoms = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", 
    "shivering", "chills", "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue",
    "muscle_wasting", "vomiting", "burning_micturition", "spotting_urination", "fatigue"
    # Load full symptom list from file if needed
]

selected_symptoms = st.multiselect("Select symptoms (up to 15)", all_symptoms, max_selections=15)

if st.button("Diagnose"):
    if not selected_symptoms or not name:
        st.warning("Please enter patient name and select at least one symptom.")
    else:
        with st.spinner("Analyzing symptoms..."):
            result = predict_disease(selected_symptoms)

        st.success("Diagnosis Complete!")
        top_result = result[0]
        
        # Display Top Prediction
        st.markdown(f"## Most Probable Diagnosis: **{top_result['disease']}**")
        st.markdown(f"**Confidence:** {top_result['confidence']}%")
        st.markdown("**Description:**")
        st.write(top_result['description'])

        st.markdown("**Precautions:**")
        for i, p in enumerate(top_result['precautions'], 1):
            st.write(f"{i}. {p}")

        st.markdown("**Treatment Suggestion:**")
        st.write(top_result['treatment'])

        # Show other possibilities
        with st.expander("Other Possible Conditions"):
            for r in result[1:]:
                st.markdown(f"**{r['disease']}** - {r['confidence']}%")
                st.write(r["description"])
                st.markdown("---")

        # PDF Export Button
        if st.button("Generate PDF Report"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="AI Medical Diagnosis Report", ln=True, align="C")

            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
            pdf.cell(200, 10, txt=f"Age: {age}    Gender: {gender}", ln=True)
            pdf.cell(200, 10, txt=f"Consultation Date: {consult_date}", ln=True)
            pdf.ln()

            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt="Symptoms Reported:", ln=True)
            pdf.set_font("Arial", size=12)
            for s in selected_symptoms:
                pdf.cell(200, 8, txt=f"- {s}", ln=True)

            pdf.ln()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt=f"Primary Diagnosis: {top_result['disease']}", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 8, txt=f"Confidence: {top_result['confidence']}%")
            pdf.multi_cell(0, 8, txt=f"Description: {top_result['description']}")
            pdf.ln()

            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt="Precautions:", ln=True)
            pdf.set_font("Arial", size=12)
            for p in top_result['precautions']:
                pdf.cell(200, 8, txt=f"- {p}", ln=True)

            pdf.ln()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, txt="Treatment Advice:", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 8, txt=top_result["treatment"])

            filename = f"{name.replace(' ', '_')}_diagnosis.pdf"
            pdf.output(filename)

            with open(filename, "rb") as file:
                btn = st.download_button(
                    label="Download Report",
                    data=file,
                    file_name=filename,
                    mime="application/pdf"
                )

        st.markdown("---")
        st.caption("Disclaimer: This is an AI-assist tool. Always consult a qualified doctor for confirmation.")

