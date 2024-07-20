import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

HIGHLIGHTS_FILE = 'highlights.txt'
EMAIL_RECIPIENT = os.environ.get('EMAIL_RECIPIENT')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

def load_highlights():
    if not os.path.exists(HIGHLIGHTS_FILE):
        return []
    with open(HIGHLIGHTS_FILE, 'r') as f:
        content = f.read()
    highlights = content.strip().split('\n\n')
    return [highlight.strip() for highlight in highlights]

def save_highlights(highlights):
    with open(HIGHLIGHTS_FILE, 'w') as f:
        f.write('\n\n'.join(highlights))

def select_random_highlights(highlights, count=5):
    return random.sample(highlights, min(count, len(highlights)))

def send_email(highlights):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT
    msg['Subject'] = 'Daily Highlights'

    body = '\n\n'.join(highlights)
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/')
def index():
    highlights = load_highlights()
    return render_template('index.html', highlights=highlights)

@app.route('/add', methods=['POST'])
def add():
    highlight = request.form['highlight']
    highlights = load_highlights()
    highlights.append(highlight)
    save_highlights(highlights)
    return redirect(url_for('index'))

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    highlights = load_highlights()
    if request.method == 'POST':
        highlights[index] = request.form['highlight']
        save_highlights(highlights)
        return redirect(url_for('index'))
    return render_template('edit.html', index=index, highlight=highlights[index])

@app.route('/send_daily_email')
def send_daily_email():
    highlights = load_highlights()
    selected_highlights = select_random_highlights(highlights, count=5)
    if selected_highlights:
        send_email(selected_highlights)
    return 'Daily email sent successfully!'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
