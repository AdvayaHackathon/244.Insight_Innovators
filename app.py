import streamlit as st
import re

st.set_page_config(page_title="Health Report Card", layout="centered")

# Language selection
lang = st.selectbox("🌐 Select Language / ಭಾಷೆ ಆಯ್ಕೆ / भाषा चुनें / భాషను ఎంచుకోండి", ["English", "Kannada", "Hindi", "Telugu"])

# Multilingual dictionary for static text
translations = {
    "English": {
        "enter_details": "👨‍⚕️ Enter Patient Details",
        "name": "Patient Name",
        "age": "Age",
        "phone": "Phone Number",
        "symptoms": "Select symptoms experienced:",
        "predict": "Predict Risk",
        "next": "Next",
        "success": "Prediction complete. Click 'Next' to view report.",
        "name_error": "❌ Name must contain only alphabets and spaces.",
        "phone_error": "❌ Phone number must contain only digits.",
    },
    "Kannada": {
        "enter_details": "👨‍⚕️ ರೋಗಿಯ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ",
        "name": "ರೋಗಿಯ ಹೆಸರು",
        "age": "ವಯಸ್ಸು",
        "phone": "ದೂರವಾಣಿ ಸಂಖ್ಯೆ",
        "symptoms": "ಅನುಭವಿಸಿದ ಲಕ್ಷಣಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "predict": "ಅಪಾಯವನ್ನು ಅಂದಾಜು ಮಾಡಿ",
        "next": "ಮುಂದೆ",
        "success": "ಅಂದಾಜು ಪೂರ್ಣವಾಗಿದೆ. ವರದಿಯನ್ನು ವೀಕ್ಷಿಸಲು 'ಮುಂದೆ' ಕ್ಲಿಕ್ ಮಾಡಿ.",
        "name_error": "❌ ಹೆಸರು ಅಕ್ಷರಗಳು ಮತ್ತು ಸ್ಪೇಸ್ ಮಾತ್ರ ಇರಬೇಕು.",
        "phone_error": "❌ ದೂರವಾಣಿ ಸಂಖ್ಯೆ ಸಂಖ್ಯೆಗಳಾಗಿರಬೇಕು.",
    },
    "Hindi": {
        "enter_details": "👨‍⚕️ रोगी का विवरण दर्ज करें",
        "name": "रोगी का नाम",
        "age": "उम्र",
        "phone": "फ़ोन नंबर",
        "symptoms": "अनुभव किए गए लक्षण चुनें:",
        "predict": "जोखिम की भविष्यवाणी करें",
        "next": "आगे",
        "success": "भविष्यवाणी पूरी हुई। रिपोर्ट देखने के लिए 'आगे' पर क्लिक करें।",
        "name_error": "❌ नाम में केवल अक्षर और स्पेस होने चाहिए।",
        "phone_error": "❌ फ़ोन नंबर में केवल नंबर होने चाहिए।",
    },
    "Telugu": {
        "enter_details": "👨‍⚕️ రోగి వివరాలను నమోదు చేయండి",
        "name": "రోగి పేరు",
        "age": "వయస్సు",
        "phone": "ఫోన్ నంబర్",
        "symptoms": "అనుభవించిన లక్షణాలను ఎంచుకోండి:",
        "predict": "ప్రమాదాన్ని అంచనా వేయండి",
        "next": "తర్వాత",
        "success": "అంచనా పూర్తైంది. నివేదికను చూడటానికి 'తర్వాత' క్లిక్ చేయండి.",
        "name_error": "❌ పేరు అక్షరాలు మరియు స్పేస్ మాత్రమే ఉండాలి.",
        "phone_error": "❌ ఫోన్ నంబర్ నంబర్లు మాత్రమే ఉండాలి.",
    },
}

# Symptoms translation
symptom_translations = {
    "English": {
        "Frequent urination": "Frequent urination",
        "Excessive thirst": "Excessive thirst",
        "Fatigue": "Fatigue",
        "Blurred vision": "Blurred vision",
        "Slow healing wounds": "Slow healing wounds",
        "Weight loss": "Weight loss",
        "None": "None"
    },
    "Kannada": {
        "Frequent urination": "ಅಭ್ಯಾಸವಾದ ಮೂತ್ರವಿಸರ್ಜನೆ",
        "Excessive thirst": "ಅತಿಯಾದ ಬಾಯಾರಿಕೆ",
        "Fatigue": "ದೌರ್ಬಲ್ಯ",
        "Blurred vision": "ಅಸ್ಪಷ್ಟ ದೃಷ್ಟಿ",
        "Slow healing wounds": "ಮಂದಗತಿಯ ಗಾಯದ ಗುಣಮುಖತೆ",
        "Weight loss": "ತೂಕ ಕಳೆವಿಕೆ",
        "None": "ಯಾವುದೂ ಅಲ್ಲ"
    },
    "Hindi": {
        "Frequent urination": "बार-बार पेशाब आना",
        "Excessive thirst": "अत्यधिक प्यास",
        "Fatigue": "थकान",
        "Blurred vision": "धुंधली दृष्टि",
        "Slow healing wounds": "घाव धीरे भरना",
        "Weight loss": "वज़न कम होना",
        "None": "कोई नहीं"
    },
    "Telugu": {
        "Frequent urination": "తరచుగా మూత్రవిసర్జన",
        "Excessive thirst": "తీవ్ర దాహం",
        "Fatigue": "దృఢత లేకపోవడం",
        "Blurred vision": "మసక దృష్టి",
        "Slow healing wounds": "నెమ్మదిగా మానే గాయాలు",
        "Weight loss": "బరువు తగ్గడం",
        "None": "ఏదీ లేదు"
    },
}

t = translations[lang]
symptom_map = symptom_translations[lang]
reverse_symptom_map = {v: k for k, v in symptom_map.items()}

# Define function to predict diabetes risk based on rules
def predict_diabetes_risk(age, selected_symptoms_translated):
    symptoms_english = [reverse_symptom_map[s] for s in selected_symptoms_translated]
    risk_score = 0

    if age >= 40:
        risk_score += 2
    elif age >= 30:
        risk_score += 1

    for symptom in symptoms_english:
        if symptom in [
            "Frequent urination",
            "Excessive thirst",
            "Fatigue",
            "Blurred vision",
            "Slow healing wounds",
        ]:
            risk_score += 1

    return 1 if risk_score >= 4 else 0

# User input
st.markdown(f"### {t['enter_details']}")
name = st.text_input(t["name"])
age = st.slider(t["age"], 1, 100, 30)
phone = st.text_input(t["phone"])

symptoms = st.multiselect(
    t["symptoms"],
    list(symptom_map.values())
)

# ✅ Validation flags
name_valid = bool(re.match("^[A-Za-z ]+$", name)) if name else True
phone_valid = phone.isdigit() if phone else True

if not name_valid:
    st.error(t["name_error"])

if not phone_valid:
    st.error(t["phone_error"])

# Proceed only if both inputs are valid
if st.button(t["predict"]) and name_valid and phone_valid:
    prediction = predict_diabetes_risk(age, symptoms)

    st.session_state["patient_data"] = {
        "Name": name,
        "Age": age,
        "Phone": phone,
        "Symptoms": ", ".join(symptoms),
        "Risk Level": "High Risk" if prediction == 1 else "Low Risk",
        "Language": lang
    }

    st.session_state["predicted"] = True
    st.success(t["success"])

if st.session_state.get("predicted") and st.button(t["next"]):
    st.switch_page("pages/report.py")