import sqlite3
import pandas as pd
import streamlit as st

# Title
st.set_page_config(page_title="📊 Patient Database", layout="centered")
st.title("📋 Stored Patient Records")
st.markdown("This dashboard shows all stored patient data and age-wise analytics.")

# ✅ Step 1: Function to create table (runs only if it doesn't already exist)
def create_table():
    conn = sqlite3.connect("patients.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS patients (
                    name TEXT,
                    phone TEXT,
                    age INTEGER,
                    symptoms TEXT,
                    risk TEXT,
                    language TEXT
                )''')
    conn.commit()
    conn.close()

# ✅ Step 2: Fetch patient data
def fetch_data():
    conn = sqlite3.connect("patients.db")
    df = pd.read_sql_query("SELECT * FROM patients", conn)
    conn.close()
    return df

# ✅ Step 3: Display patient data and analytics
def display_patient_data():
    create_table()  # 🔁 Call this first to ensure the table exists

    df = fetch_data()

    if df.empty:
        st.warning("⚠ No patient records found.")
    else:
        st.success(f"✅ {len(df)} patient records found.")
        st.dataframe(df)

        # Age distribution chart
        st.markdown("### 📈 Age-wise Distribution")
        age_counts = df['age'].value_counts().sort_index()
        st.bar_chart(age_counts)

        # Risk level summary chart
        st.markdown("### 🧪 Risk Level Summary")
        risk_counts = df['risk'].value_counts()
        st.bar_chart(risk_counts)

# ✅ Step 4: Run the main function
if __name__ == "__main__":
    display_patient_data()