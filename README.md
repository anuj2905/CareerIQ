# CareerIQ

### AI-Powered Career Intelligence & Job Matching Platform

CareerIQ is an AI/ML-powered career intelligence and job-matching platform designed to help students, fresh graduates, job seekers, and recruiters make better use of resume and job-related information.

The system analyzes candidate resumes, extracts structured profile information, evaluates job compatibility, identifies skill gaps, predicts suitable career roles, provides salary predictions, and offers personalized career guidance through AI-powered features.

---

## 🌐 Live Demo

[🚀 Try CareerIQ Live](https://careeriq-anuj-patil.streamlit.app/)

---

## 📌 Overview

Finding suitable career opportunities can be challenging for students and job seekers because they often need to manually analyze their resumes, understand job requirements, identify missing skills, search for suitable opportunities, and estimate their career readiness.

CareerIQ addresses these challenges by providing an integrated platform for resume analysis, job matching, career insights, skill-gap analysis, salary prediction, job discovery, and AI-powered career assistance.

The system processes information such as:

- 👤 Name
- 🎓 Education
- 💻 Technical Skills
- 📂 Projects
- 💼 Experience
- 📜 Certifications

The extracted information is converted into a structured candidate profile and reused across multiple modules of the application.

---

## 🎯 Objectives

The main objectives of CareerIQ are:

- To automatically analyze candidate resumes.
- To extract structured information from unstructured resume documents.
- To identify career roles that match a candidate's profile.
- To compare candidate profiles with job requirements.
- To calculate skill, education, and experience matching scores.
- To identify missing skills for a selected career role.
- To provide personalized career recommendations.
- To provide AI-powered career assistance.
- To help users discover relevant job opportunities.
- To provide salary prediction using machine learning.
- To provide a centralized career dashboard.
- To help users plan their career development.

---

# 🚀 Features

## 📄 1. Resume Analysis

Users can upload their resumes and automatically extract important information.

The system extracts:

- Name
- Education
- Skills
- Projects
- Experience
- Certifications

The extracted information is converted into a structured candidate profile that can be reused across other modules.

The system supports PDF text extraction and can use OCR for scanned or image-based documents.

---

## 🎯 2. Job Matching

The Job Matching module compares a candidate's profile with specific job requirements.

The system evaluates:

- 💻 Skill Match
- 🎓 Education Match
- 💼 Experience Match
- 🏆 Overall Job Match

The results are presented using visual indicators to make the matching information easier to understand.

The matching process can consider both direct skill matching and semantic relevance between candidate experience and job requirements.

---

## 🧠 3. Career Insights

Career Insights analyzes the candidate's profile and provides career-related information based on their skills, education, projects, experience, and certifications.

The module can help users understand:

- Suitable career roles
- Existing strengths
- Areas that require improvement
- Relevant technical skills
- Career development requirements

---

## 📊 4. Skill Gap Analysis

The Skill Gap Analysis module compares the user's existing skills with the skills required for a selected career role.

It provides:

- ✅ Matched Skills
- ❌ Missing Skills
- ➕ Additional Skills
- 📈 Skill Gap Score
- 📚 Learning Recommendations

This helps users understand which technical skills they should focus on developing for their target career.

---

## 🤖 5. AI Career Assistant

CareerIQ includes an AI-powered career assistant that can help users with career-related questions.

Users can ask about:

- Career paths
- Technical skills
- Learning strategies
- Projects
- Interview preparation
- Job preparation
- Career development

The assistant uses AI to generate contextual career guidance.

---

## 🔎 6. Job Discovery

The Job Discovery module helps users find relevant job opportunities based on their career profile and requirements.

The module is designed to reduce the manual effort involved in searching for suitable job opportunities.

---

## 📈 7. Career Dashboard

The Career Dashboard provides a centralized view of important career-related information.

Users can access information related to:

- Candidate profile
- Career insights
- Job matching
- Skill gaps
- Career analysis
- Other relevant career results

---

## 🗺️ 8. Career Roadmap

The Career Roadmap feature provides structured guidance for users who want to work toward a specific career role.

The roadmap can help users understand:

- Skills to develop
- Areas to improve
- Projects to build
- Career preparation requirements

---

## 💰 9. Salary Prediction

CareerIQ includes a machine-learning-based salary prediction module.

The system processes relevant job and market information to estimate salary values.

This feature is intended to provide users with an approximate understanding of salary expectations associated with relevant job profiles.

---

# 🏢 Company Features

CareerIQ also includes functionality designed for the company/recruiter side.

## 🏢 Company Dashboard

The Company Dashboard provides an interface for organizations to manage job-related information.

## 💼 Job Management

Companies can manage job postings and define relevant job requirements.

This functionality provides the foundation for future candidate-job matching and recruitment intelligence.

---

# 🏗️ System Architecture

```text
                           ┌───────────────────────┐
                           │       CareerIQ         │
                           │  Career Intelligence  │
                           └───────────┬───────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    │                                     │
             ┌──────▼──────┐                       ┌──────▼──────┐
             │   Student   │                       │   Company   │
             │    Portal   │                       │    Portal   │
             └──────┬──────┘                       └──────┬──────┘
                    │                                     │
       ┌────────────┼────────────┐              ┌──────────┴─────────┐
       │            │            │              │                    │
       ▼            ▼            ▼              ▼                    ▼
   Resume       Job Matching   Career       Company             Manage
   Analysis                    Insights     Dashboard              Jobs
       │            │            │
       └────────────┼────────────┘
                    │
                    ▼
          ┌──────────────────────┐
          │   AI / ML Engine     │
          └──────────┬───────────┘
                     │
       ┌─────────────┼──────────────┐
       │             │              │
       ▼             ▼              ▼
  Skill Gap      Salary         Career
  Analysis      Prediction      Guidance
       │
       ▼
  Learning & Career
   Recommendations



🛠️ Tech Stack
Programming Language
Python
Frontend / Web Application
Streamlit
AI / Machine Learning
OpenAI API
Scikit-learn
Natural Language Processing
Semantic Similarity
Machine Learning
Data Processing
Pandas
NumPy
Resume Processing
PyMuPDF
Tesseract OCR
Python-docx
Database
SQLite / project database
Development Tools
Git
GitHub
VS Code
Virtual Environment



📂 Project Structure

Job-Intelligent-System/
│
├── app.py
├── requirements.txt
├── .env
│
├── config/
│   ├── settings.py
│   └── prompts.py
│
├── src/
│   ├── ui/
│   │   ├── home.py
│   │   ├── resume.py
│   │   └── assistant.py
│   │
│   ├── resume/
│   │   ├── parser.py
│   │   ├── skill_extractor.py
│   │   ├── experience_analyzer.py
│   │   └── resume_scorer.py
│   │
│   ├── matching/
│   │   └── job_matcher/
│   │       ├── skill_matcher.py
│   │       ├── education_matcher.py
│   │       ├── experience_matcher.py
│   │       ├── experience_semantic_matcher.py
│   │       └── calculate_experience.py
│   │
│   ├── career/
│   │   ├── career_recommender.py
│   │   ├── role_predictor.py
│   │   ├── skill_gap_analyzer.py
│   │   └── career_roadmap.py
│   │
│   ├── rag/
│   ├── agents/
│   ├── llm/
│   ├── database/
│   └── job_discovery/
│
└── data/


⚙️ How It Works
Step 1 — Upload Resume
The user uploads a resume through the Streamlit interface.

Step 2 — Extract Resume Text
The system first uses PyMuPDF to extract text.
For scanned/image-based resumes, Tesseract OCR is used as a fallback.

Step 3 — Generate Candidate Profile
The extracted text is analyzed using an AI model to generate a structured profile containing:
Name
Education
Skills
Projects
Experience
Certifications

Step 4 — Career Analysis
The profile is analyzed to determine suitable career roles and career insights.

Step 5 — Job Matching
The candidate profile is compared with job requirements.

Skill Match
     +
Education Match
     +
Experience Match
     ↓
Overall Job Match
Step 6 — Skill Gap Analysis

The system compares the candidate's current skills with the required skills for the selected career role.

Current Skills
       ↓
Required Skills
       ↓
Skill Comparison
       ↓
Matched + Missing Skills
       ↓
Learning Recommendations
Step 7 — Career Guidance

The AI Career Assistant and Career Roadmap provide personalized guidance based on the user's profile.

📊 Machine Learning

The project can use machine-learning techniques for job matching and candidate analysis.

A job-matching model can use features such as:

Skill Match
Education Match
Experience Match
Semantic Similarity
        ↓
Machine Learning Model
        ↓
Matched Score

The matching score can then be converted into a percentage for user-friendly display.

🎯 Target Users
🎓 Students
👨‍💻 Fresh Graduates
💼 Job Seekers
🧑‍💼 Recruiters
🏢 Companies
🎓 Educational Institutions
🔮 Future Scope

Future versions of the Job Intelligent System can include:

Advanced career-role prediction
Transformer-based semantic job matching
RAG-based career assistant
AI career agents
Automated job discovery
Company recruitment portal
Candidate ranking
Salary prediction
Job-market trend analysis
Authentication and role-based access
Career progress tracking
Mobile application


## 📸 Screenshots

### 🏠 Home
![Home](screenshots/home.png)

### 📄 Resume Analysis
![Resume Analysis](screenshots/resume-analysis.png)

### 🏢 Company Dashboard
![Company Dashboard](screenshots/company_dashboard.png)

### 💼 Manage Jobs
![Manage Jobs](screenshots/manage_jobs.png)

### 💰 Salary Prediction
![Salary Prediction](screenshots/salary_prediction.png)

🌐 Live Demo

Try the deployed application:

https://careeriq-anuj-patil.streamlit.app/

⚠️ Note

The application may require access to AI services for some features. Results generated by AI should be treated as career guidance, not as a guaranteed assessment of employment suitability.

👨‍💻 Author

Anuj Patil

B.E. Computer Engineering
Atharva College of Engineering, Mumbai
