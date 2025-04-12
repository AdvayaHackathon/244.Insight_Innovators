import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Health Report", layout="centered")

# Title and GenAI intro
st.markdown("## 📋 Patient Health Summary")
st.markdown(
    """
    #### 🤖 Auto-Generated Medical Reports using GenAI  
    """
)

# Function to generate GenAI-style health report summary
def generate_ai_summary(data):
    name = data["Name"]
    risk_text = data["Risk Level"]
    risk = "High" if "High" in risk_text else "Low"
    age = data["Age"]
    symptoms = data.get("Symptoms", "N/A")

    if risk == "High":
        advice = (
            f"Hi {name}, based on the symptoms you've provided and your age of {age}, "
            "there are strong indicators of a potential diabetes risk. "
            f"Symptoms like {symptoms} can be critical warning signs. "
            "We highly recommend visiting a nearby healthcare provider for further consultation as early as possible. "
            "Taking proactive steps now can help manage or even prevent complications."
        )
    else:
        advice = (
            f"Hi {name}, based on your inputs and your age of {age}, "
            "you currently show a low risk for diabetes. "
            f"Your symptoms ({symptoms}) don’t appear to be serious at the moment. "
            "To stay healthy, continue maintaining a balanced diet, regular exercise, and schedule routine health checkups. "
            "Stay alert to any changes in your health."
        )
    return advice

# 🆕 Function to generate GenAI-style precautions
def generate_ai_precautions(data):
    risk_text = data["Risk Level"]
    risk = "High" if "High" in risk_text else "Low"
    if risk == "High":
        return [
            "Avoid sugary foods and drinks.",
            "Monitor blood sugar levels regularly.",
            "Exercise at least 30 minutes a day.",
            "Limit carbohydrate intake.",
            "Visit a nearby healthcare provider for diagnosis."
        ]
    else:
        return [
            "Maintain a balanced diet rich in fiber.",
            "Stay physically active with daily walks or yoga.",
            "Drink plenty of water throughout the day.",
            "Avoid skipping meals.",
            "Schedule annual health checkups."
        ]

# Updated PDF generation function
def generate_pdf(data_dict, summary):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, height - 50, "Patient Health Report")

    c.setFont("Helvetica", 12)
    y = height - 100
    for key, value in data_dict.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "🤖 AI-Based Health Summary")
    y -= 20

    c.setFont("Helvetica", 11)
    for line in summary.split('. '):
        if line.strip():
            c.drawString(50, y, line.strip() + '.')
            y -= 18

    # 🆕 Add precautions
    y -= 30
    precautions = generate_ai_precautions(data_dict)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "🛡️ Precautions Suggested by GenAI")
    y -= 20

    c.setFont("Helvetica", 11)
    for precaution in precautions:
        c.drawString(60, y, f"• {precaution}")
        y -= 18

    c.save()
    buffer.seek(0)
    return buffer

# Display Report
if "patient_data" in st.session_state:
    data = st.session_state.patient_data
    df = pd.DataFrame([data])
    st.table(df.T.rename(columns={0: "Value"}))

    summary = generate_ai_summary(data)
    precautions = generate_ai_precautions(data)

    if "High" in data["Risk Level"]:
        st.error("🔴 High Risk: Please consult a nearby health center.")
    else:
        st.success("🟢 Low Risk: You’re doing well! Stay healthy.")

    # Show summary
    st.markdown(f"### 📄 AI Summary\n{summary}")

    # Show precautions
    st.markdown("### 🛡️ Precautions Suggested by GenAI")
    for p in precautions:
        st.markdown(f"- {p}")

    # PDF download
    pdf_buffer = generate_pdf(data, summary)

    st.download_button(
        label="📄 Download Report as PDF",
        data=pdf_buffer,
        file_name="health_report.pdf",
        mime="application/pdf",
        key="download-pdf"
    )

    # Auto-download trigger
    streamlit_js_eval(js_expressions="parent.document.querySelector('button[kind=download-pdf]').click();")

else:
    st.warning("⚠ No patient data found. Please go to the previous page and enter details.")
