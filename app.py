import streamlit as st
import pdfplumber
import re
import time

# -------------------------------
# ⚙️ PAGE CONFIG (FIRST LINE)
# -------------------------------
st.set_page_config(page_title="AI Job Matcher", layout="centered")

# -------------------------------
# 🎨 FORCE LIGHT THEME
# -------------------------------
st.markdown("""
<style>

/* FORCE LIGHT */
html, body, .stApp {
    background-color: #f8fafc !important;
    color: #0f172a !important;
}

/* Title */
h1 {
    text-align: center;
    color: #1e3a8a;
}

/* Card */
.section {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

/* Input */
textarea {
    background: white !important;
    color: black !important;
    border-radius: 10px;
}

/* File uploader */
.stFileUploader {
    background: white !important;
    border: 2px dashed #cbd5f5;
    padding: 10px;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg,#3b82f6,#6366f1);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
}

/* Score */
.score {
    font-size: 48px;
    text-align: center;
    color: #2563eb;
    font-weight: bold;
}

/* Loading animation */
@keyframes pulse {
  0% {opacity:0.4;}
  50% {opacity:1;}
  100% {opacity:0.4;}
}
.loading {
    text-align:center;
    font-weight:bold;
    color:#475569;
    animation: pulse 1.5s infinite;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# FUNCTIONS
# -------------------------------
def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

SKILLS_DB = [

    # 🔹 Programming
    "python", "r", "sql",

    # 🔹 Libraries (Core DS)
    "pandas", "numpy", "scikit-learn", "sklearn",

    # 🔹 Visualization
    "matplotlib", "seaborn", "plotly",

    # 🔹 Machine Learning
    "machine learning", "supervised learning", "unsupervised learning",
    "regression", "classification", "clustering",

    # 🔹 Models
    "linear regression", "logistic regression",
    "decision tree", "random forest", "knn", "k-means",

    # 🔹 Data Processing
    "data analysis", "data cleaning", "data preprocessing",
    "feature engineering", "feature selection",

    # 🔹 EDA
    "exploratory data analysis", "eda",

    # 🔹 Model Evaluation
    "model evaluation", "accuracy", "precision", "recall", "f1 score",

    # 🔹 Tools
    "jupyter", "google colab", "excel",

    # 🔹 Databases
    "mysql", "mongodb", "postgresql",

    # 🔹 Big Data (bonus)
    "hadoop", "spark",

    # 🔹 Deep Learning (optional)
    "tensorflow", "keras", "pytorch"
]

def extract_skills(text):
    return list(set([s for s in SKILLS_DB if s in text]))

def match_score(resume_skills, job_skills):
    if not job_skills:
        return 0
    return round(len(set(resume_skills)&set(job_skills))/len(job_skills)*100,2)

def recommendation(score):
    if score >= 80:
        return "Strong Match 🚀"
    elif score >= 50:
        return "Moderate Match ⚡"
    else:
        return "Low Match ❌"

# -------------------------------
# UI
# -------------------------------
st.title("AI Job Matching System")
st.caption("Clean • Smart • Fast Resume Analyzer")

# Upload
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📄 Upload Resume")
uploaded_file = st.file_uploader("", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)

# Job
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("💼 Job Description")
job_text = st.text_area("", height=150)
st.markdown('</div>', unsafe_allow_html=True)

# Button
if st.button("🚀 Analyze Match"):

    if uploaded_file and job_text:

        progress = st.progress(0)
        loading = st.empty()

        # Animation
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i+1)
            loading.markdown('<div class="loading">Analyzing...</div>', unsafe_allow_html=True)

        # Logic
        resume_text = read_pdf(uploaded_file)
        resume_clean = clean_text(resume_text)
        resume_skills = extract_skills(resume_clean)

        job_clean = clean_text(job_text)
        job_skills = extract_skills(job_clean)

        score = match_score(resume_skills, job_skills)

        matched = set(resume_skills) & set(job_skills)
        missing = set(job_skills) - set(resume_skills)

        loading.empty()

        # Result
        st.markdown('<div class="section">', unsafe_allow_html=True)

        st.markdown(f"<div class='score'>{score}%</div>", unsafe_allow_html=True)
        st.progress(int(score))

        st.info(recommendation(score))

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Skills")
            st.write(", ".join(matched) if matched else "None")

        with col2:
            st.subheader("❌ Missing Skills")
            st.write(", ".join(missing) if missing else "None 🎉")

        st.subheader("🧠 Your Skills")
        st.write(", ".join(resume_skills))

        st.subheader("📌 Job Skills")
        st.write(", ".join(job_skills))

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Upload resume and enter job description")