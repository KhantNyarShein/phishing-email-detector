from flask import Flask, render_template, request
import joblib
import re

# Load trained model and vectorizer
model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

app = Flask(__name__, template_folder="../templates")


# Extract URLs from email text
def extract_urls(text):
    url_pattern = r"https?://[^\s]+"
    urls = re.findall(url_pattern, text)
    return urls

import ipaddress

def detect_ip_urls(urls):

    ip_urls = []

    for url in urls:
        try:
            domain = url.split("/")[2]
            ipaddress.ip_address(domain)
            ip_urls.append(url)
        except:
            pass

    return ip_urls

# Detect suspicious URLs
def check_suspicious_urls(urls):

    suspicious_keywords = [
        "login",
        "verify",
        "update",
        "secure",
        "account",
        "bank",
        "password",
        "confirm"
    ]

    suspicious_found = []

    for url in urls:
        for keyword in suspicious_keywords:
            if keyword in url.lower():
                suspicious_found.append(url)

    return suspicious_found


# Detect suspicious words
def detect_suspicious_words(text):

    suspicious_words = [
        "verify",
        "password",
        "login",
        "account",
        "urgent",
        "bank",
        "confirm",
        "update",
        "security",
        "suspended"
    ]

    found_words = []

    words = text.lower().split()

    for word in suspicious_words:
        if word in words:
            found_words.append(word)

    return found_words


# Calculate risk score
def calculate_risk_score(prediction, suspicious_urls, suspicious_words):

    text_score = 80 if prediction == 1 else 20
    url_score = min(len(suspicious_urls) * 40, 100)
    keyword_score = min(len(suspicious_words) * 15, 100)

    final_score = int((text_score * 0.5) + (url_score * 0.3) + (keyword_score * 0.2))

    return text_score, url_score, keyword_score, final_score


@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    suspicious_urls = []
    suspicious_words = []
    text_score = 0
    url_score = 0
    keyword_score = 0
    final_score = 0
    risk_level = ""

    if request.method == "POST":

        email_text = request.form["email_text"]

        # Detect suspicious words
        suspicious_words = detect_suspicious_words(email_text)

        # Extract URLs
        urls = extract_urls(email_text)

        #ip address
        ip_urls = detect_ip_urls(urls)

        # Detect suspicious URLs
        suspicious_urls = check_suspicious_urls(urls)

        # ML prediction
        text_vector = vectorizer.transform([email_text])
        prediction = model.predict(text_vector)[0]

        probability = model.predict_proba(text_vector)[0][1]
        probability_percent = round(probability * 100, 2)

        # Calculate scores
        text_score, url_score, keyword_score, final_score = calculate_risk_score(
            prediction,
            suspicious_urls + ip_urls,
            suspicious_words
        )

        # Determine risk level
        if final_score >= 70:
            risk_level = "🔴 HIGH RISK"
        elif final_score >= 40:
            risk_level = "🟠 MEDIUM RISK"
        else:
            risk_level = "🟢 LOW RISK"

        # Final decision
        if prediction == 1 or suspicious_urls:
            result = f"⚠️ Possible Phishing Email ({probability_percent}% confidence)"
        else:
            result = f"✅ Email appears Safe ({100 - probability_percent}% confidence)"

    return render_template(
        "index.html",
        result=result,
        urls=suspicious_urls,
        ip_urls=ip_urls,
        words=suspicious_words,
        text_score=text_score,
        url_score=url_score,
        keyword_score=keyword_score,
        final_score=final_score,
        risk_level=risk_level
    )


if __name__ == "__main__":
    app.run()