import csv
import re
import threading
import webbrowser

import requests
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secret-key"

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Semantic model (loaded lazily to avoid startup crashes on Windows)
model = None

# RapidAPI credentials
RAPID_API_KEY = "993fba48e9mshbde4683173e2b8cp1826c9jsn4b4926fea284"
RAPID_API_HOST = "jsearch.p.rapidapi.com"

# Job API fetch
def fetch_jobs_from_api(description, industry, experience):
    query = description
    if industry:
        query += f" {industry}"
    if experience:
        query += f" {experience} level"

    url = f"https://{RAPID_API_HOST}/search"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }
    querystring = {
        "query": query,
        "page": "1",
        "num_pages": "1",
        "date_posted": "all",
        "country": "in",
        "language": "en"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print("Error fetching data:", response.text)
        return []

def _keyword_similarity(user_input, title):
    tokens = set(re.findall(r"[a-z0-9]+", user_input.lower()))
    title_tokens = set(re.findall(r"[a-z0-9]+", title.lower()))
    if not tokens:
        return 0.0
    overlap = len(tokens & title_tokens)
    return overlap / max(1, len(tokens))

# Semantic matching
def match_jobs_semantic(user_input, jobs, title_key="job_title"):
    if not jobs:
        return []

    global model
    try:
        if model is None:
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity
            model = SentenceTransformer("all-MiniLM-L12-v2")

        titles = [job.get(title_key, "") for job in jobs]
        user_emb = model.encode([user_input])
        job_embs = model.encode(titles)
        scores = cosine_similarity(user_emb, job_embs)[0]
        for i, job in enumerate(jobs):
            job["match_score"] = round(float(scores[i]) * 100, 2)
    except Exception as exc:
        print("Falling back to keyword matching:", exc)
        for job in jobs:
            title = job.get(title_key, "")
            job["match_score"] = round(_keyword_similarity(user_input, title) * 100, 2)

    jobs.sort(key=lambda x: x["match_score"], reverse=True)
    return jobs

# NCO data fetch
def fetch_nco_data(description):
    with open("nco_2015_occupations.csv", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        nco_jobs = list(reader)
    for job in nco_jobs:
        job["job_title"] = job.get("Occupation_Title", "")
        job["employer_name"] = "NCO"
        job["job_city"] = job.get("Industry", "")
        job["job_publisher"] = "NCO Database"
        job["job_apply_link"] = ""
    return nco_jobs

# Save results to CSV
def save_to_csv(jobs):
    filename = "job_results.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Source", "Match Score", "Link"])
        for job in jobs:
            writer.writerow([
                job.get("job_title", ""),
                job.get("employer_name", ""),
                job.get("job_city", ""),
                job.get("job_publisher", ""),
                job.get("match_score", ""),
                job.get("job_apply_link", "")
            ])
    return filename

# Translation endpoint: auto-detect source, return English
@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400
    try:
        from deep_translator import GoogleTranslator
        translated_text = GoogleTranslator(source="auto", target="en").translate(text)
        return jsonify({"text": translated_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Routes
@app.route("/")
def home():
    return render_template('home.html')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@login_required
def index():
    return render_template("index.html", username=current_user.username)

@app.route("/search", methods=["POST"])
@login_required
def search():
    description = request.form.get("description", "").strip()
    career_goal = request.form.get("career_goal", "")
    industry = request.form.get("industry", "").strip()
    experience = request.form.get("experience", "")

    if not description:
        flash(("danger", "Please enter a job description or skills."))
        return render_template("index.html")

    jobs_api = fetch_jobs_from_api(description, industry, experience)
    matched_jobs_api = match_jobs_semantic(description, jobs_api, title_key="job_title")
    for job in matched_jobs_api:
        job["source"] = "API"

    nco_jobs = fetch_nco_data(description)
    matched_nco_jobs = match_jobs_semantic(description, nco_jobs, title_key="job_title")
    for job in matched_nco_jobs:
        job["source"] = "NCO"

    # Combine and sort all jobs by match_score, then take top 5
    combined_jobs = matched_jobs_api + matched_nco_jobs
    combined_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    top_jobs = combined_jobs[:5]
    save_to_csv(top_jobs)

    return render_template(
        "results.html",
        jobs=top_jobs,
        career_goal=career_goal,
        description=description,
        username=current_user.username
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("index"))  # ✅ Redirects to index after login
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode("utf-8")
        confirm = request.form["confirm"]
        mobile = request.form["mobile"]
        # otp = request.form["otp"]

        if request.form["password"] != confirm:
            flash("Passwords do not match", "danger")
            return redirect(url_for("register"))

        # if otp != "123456":
        #     flash("Invalid OTP", "danger")
        #     return redirect(url_for("register"))

        user = User(username=username, email=email, password=password, mobile=mobile)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))

# ✅ Fix for RuntimeError
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True)
