# 🚀 Semantica – AI-Powered Semantic Job Search Engine

> **Finding the right career through meaning, not just matching words.**

Semantica is an AI-powered job recommendation platform that leverages **Natural Language Processing (NLP)** and **semantic search** to connect users with relevant occupations and live job opportunities. By utilizing **Sentence Transformers**, **Cosine Similarity**, and the **NCO 2015 occupational classification**, the platform understands the meaning behind user skills rather than relying on exact keyword matches. It also supports **voice-based input**, **multilingual search**, and **real-time job retrieval** for a smarter and more accessible job search experience.

---

## 📌 Problem Statement

Most job portals rely on **keyword matching**, which often produces inaccurate or incomplete results because users and employers describe the same role differently.

For example:

| User Search | Job Listing |
|-------------|-------------|
| App Developer | Mobile Software Engineer |
| QA Engineer | Software Tester |
| Data Analyst | Business Intelligence Analyst |

Although these roles are semantically similar, traditional search engines frequently fail to recognize them.

### Existing Challenges

- Limited to exact keyword matching
- Unable to understand semantic meaning
- No integration between occupational standards and live job portals
- Poor multilingual support
- Lack of voice-based job search

---

# 💡 Our Solution

Semantica addresses these challenges through semantic understanding instead of simple text matching.

The platform:

- Converts user queries into semantic embeddings.
- Maps skills to **NCO 2015** occupational standards.
- Retrieves live job listings using the **JSearch API**.
- Supports multilingual and voice-based searches.
- Ranks recommendations using semantic similarity scores.

---

# ✨ Key Features

- 🔍 Semantic Search using Sentence Transformers
- 🤖 AI-powered Job Recommendations
- 📊 Cosine Similarity-based Ranking
- 📚 NCO 2015 Occupation Mapping
- 🌐 Real-time Job Listings (RapidAPI JSearch)
- 🎙 Voice-to-Text Job Search
- 🌍 Hindi ↔ English Translation
- 📈 Personalized Match Scores
- ⚡ Fast and User-Friendly Interface

---

# 🛠 Tech Stack

### Languages
- Python
- HTML
- CSS
- JavaScript

### Backend
- Flask

### Machine Learning & NLP
- Sentence Transformers
- Hugging Face
- Scikit-learn
- Cosine Similarity

### APIs
- RapidAPI JSearch API

### Data Processing
- Pandas
- NumPy

---

# ⚙️ Workflow

```text
User Query
      │
      ▼
Text / Voice Input
      │
      ▼
Speech-to-Text
      │
      ▼
Language Translation
      │
      ▼
Sentence Embedding Generation
      │
      ▼
Semantic Similarity Matching
      │
      ▼
NCO Occupation Mapping
      │
      ▼
Real-Time Job Retrieval
      │
      ▼
Ranked Job Recommendations
```

---

# 📂 Project Structure

```text
Semantica/
│
├── app.py
├── requirements.txt
├── static/
├── templates/
├── models/
├── dataset/
├── utils/
├── README.md
└── LICENSE
```

---

# 🚀 Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Semantica.git

# Move to project folder
cd Semantica

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

---

# 📸 Demo

<img width="1600" height="741" alt="Home" src="https://github.com/user-attachments/assets/874149e6-f7a5-49ca-9be4-f197d6311dec" />
<img width="1170" height="580" alt="Job Description" src="https://github.com/user-attachments/assets/273d1ca8-be05-4c62-beaf-e9cc13d2aca1" />
<img width="1170" height="571" alt="Job Matches results" src="https://github.com/user-attachments/assets/0b09ce11-0650-41dd-83a2-d37a1755d391" />



Example:

- Home Page
- Semantic Search
- Voice Search
- Job Recommendation Results

---

# 🎯 What Makes Semantica Different?

Unlike traditional job portals that depend on exact keyword matching, Semantica understands the **context and meaning** of user queries.

### Highlights

- Semantic search powered by Sentence Transformers
- Integration of occupational standards with live job listings
- Multilingual and voice-enabled search
- Personalized recommendations using similarity scores
- AI-driven career discovery instead of keyword search

---

# 📈 Future Enhancements

- Resume Parsing
- Skill Gap Analysis
- AI Career Assistant
- Course Recommendations
- Resume-Based Job Matching
- User Authentication
- Dashboard & Analytics
- Mobile Application

---

# 🎯 Use Cases

- Students seeking internships
- Fresh graduates
- Job seekers
- Career switchers
- Recruitment platforms
- Government employment services

---

## 📌 Project Status

This project is maintained solely by the author and is shared for portfolio and educational purposes.

---

## 📄 Copyright

© 2026 Rishu Kundu. All rights reserved.

This repository is intended for viewing and learning purposes only. Unauthorized copying, modification, redistribution, or commercial use of the source code is prohibited without prior permission.

---

# 👨‍💻 Author

**Rishu Kundu**

B.Tech – Computer Science Engineering

📧 Email: rishukundu5678@gmail.com

🔗 LinkedIn: www.linkedin.com/in/rishukundu

💻 GitHub: https://github.com/rishukundu5678-art

---

## ⭐ If you found this project useful, please consider giving it a Star!
