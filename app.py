import streamlit as st
import re
import PyPDF2
import urllib.parse

# --------- Streamlit UI ---------
st.set_page_config(page_title="AI Resume Job Recommender", layout="wide")
st.title("📄 AI Resume Job Recommender")

st.write("Upload your resume and select your city to get suggested job roles. Then click on the button to view real jobs on LinkedIn near you.")

# File uploader
uploaded_file = st.file_uploader("Upload your Resume (.pdf/.txt)", type=["pdf", "txt"])

# City dropdown
cities = ["Delhi", "Mumbai", "Bangalore", "Pune", "Hyderabad", "Chennai"]
city = st.selectbox("Select Your City", cities)

if st.button("Get Suggested Role"):
    if uploaded_file is not None:
        # Extract text from resume
        resume_text = ""
        if uploaded_file.name.endswith(".txt"):
            resume_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
        else:
            st.error("Only PDF and TXT supported!")

        resume_text = resume_text.lower()

        # Skill Keywords
        skill_keywords = {
            "python","machine","learning","sql","html","css","javascript","data","java","excel",
            "accounting","finance","commerce","tally","audit","taxation",
            "marketing","seo","sales","digital","management","analytics","content","research",
            "graphic","design","creative","photoshop","illustrator",
            "hr","recruitment","operations",
            "science","lab","biology","chemistry","physics","research"
        }

        words = re.findall(r"[a-zA-Z]+", resume_text)
        detected_skills = [w for w in words if w in skill_keywords]
        detected_skills = list(set(detected_skills))

        # Suggest Role
        def suggest_role(skills):
            s = set(skills)
            if {"python","sql","machine","learning","html","css","javascript","data","java"}.intersection(s):
                return "Data Analyst"
            if {"accounting","finance","audit","tally","taxation","commerce"}.intersection(s):
                return "Finance Intern"
            if {"marketing","seo","sales","digital","content","research","management"}.intersection(s):
                return "Marketing Intern"
            if {"graphic","design","creative","photoshop","illustrator"}.intersection(s):
                return "Graphic Designer"
            if {"hr","recruitment","operations"}.intersection(s):
                return "HR Intern"
            if {"science","lab","biology","chemistry","physics","research"}.intersection(s):
                return "Research Intern"
            return "General Internship"

        suggested_role = suggest_role(detected_skills)

        st.subheader("🔎 Detected Skills")
        st.write(detected_skills)
        st.subheader("✅ Suggested Job Role")
        st.write(suggested_role)

        # LinkedIn URL creation
        role_param = urllib.parse.quote_plus(suggested_role)
        city_param = urllib.parse.quote_plus(city)
        linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={role_param}&location={city_param}"

        st.subheader("🔗 Real Jobs")
        st.markdown(
            f'<a href="{linkedin_url}" target="_blank"><button style="padding:10px 20px;">Open LinkedIn Jobs Page</button></a>',
            unsafe_allow_html=True
        )
    else:
        st.error("Please upload your resume first!")
