# Phishing Email Detection Web Application

This project is a web-based phishing email detection system developed using Python and Flask.  
It analyzes email content and identifies whether the email is likely to be phishing or safe.

## Live Demo
You can test the system here:

https://phishing-email-detector-mvuo.onrender.com

## Features

- Machine Learning based email classification
- Suspicious URL detection
- Suspicious keyword detection
- Risk scoring dashboard
- Responsive web interface

## Technologies Used

- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- HTML / Bootstrap

## Project Structure

```
phishing-email-detector
│
├── app
│   └── app.py
│
├── datasets
│   └── phishing_email.csv
│
├── model
│   ├── phishing_model.pkl
│   └── vectorizer.pkl
│
├── templates
│   └── index.html
│
├── requirements.txt
├── start.sh
```

## How It Works

1. The user pastes an email message into the web interface.
2. The system analyzes the text using a machine learning model.
3. URLs inside the email are extracted and analyzed.
4. Suspicious keywords are detected.
5. A risk score is calculated and displayed.

## Disclaimer

This tool is for educational and research purposes only.  
The results may not always be 100% accurate.

## Author

Khant Nyar Shein (Kaleb)

Computer Science Student  
Cybersecurity Research Interest
