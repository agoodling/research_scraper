from flask import Flask, request, jsonify, send_from_directory
from google.cloud import firestore
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
db = firestore.Client()

PUBMED_URL = "https://pubmed.ncbi.nlm.nih.gov/"

# Static frontend
@app.route("/", methods=["GET"])
def index():
    return send_from_directory('.', "index.html")

@app.route("/home", methods=["GET"])
def home():
    return send_from_directory('.', "index.html")

# PubMed scraper
def scrape_pubmed(query):
    search_url = f"{PUBMED_URL}?term={query.replace(' ', '+')}"
    response = requests.get(search_url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []

    for article in soup.select('.docsum-content'):
        title_elem = article.select_one('.docsum-title')
        title = title_elem.text.strip() if title_elem else "No title available"
        link = PUBMED_URL + title_elem["href"] if title_elem and title_elem.has_attr("href") else ""
        snippet_elem = article.select_one('.full-view-snippet')
        summary = snippet_elem.text.strip() if snippet_elem else "No summary available."

        articles.append({
            "title": title,
            "link": link,
            "summary": summary
        })

    return articles

# Subscribe endpoint
@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    user_email = data.get("email")
    query = data.get("query")

    if not user_email or not query:
        return jsonify({"error": "Email and query are required"}), 400

    db.collection("subscriptions").add({
        "email": user_email,
        "query": query
    })

    return jsonify({"message": "Subscription successful!"})

# Email sender
def send_email(recipient, query, articles):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    user_name = recipient.split("@")[0].replace(".", " ").title()
    logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Logo_TV_2021.svg/512px-Logo_TV_2021.svg.png"

    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .wrapper {{
                padding: 20px 0;
                background-color: #f4f4f4;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background-color: #fff;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }}
            .logo {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .logo img {{
                width: 120px;
            }}
            h2 {{
                color: #1a73e8;
                font-size: 20px;
            }}
            .article {{
                border-top: 1px solid #e0e0e0;
                padding: 15px 0;
            }}
            .article h4 {{
                margin: 0 0 5px;
                font-size: 16px;
                color: #222;
            }}
            .article p {{
                margin: 5px 0;
                color: #555;
            }}
            .article a {{
                display: inline-block;
                margin-top: 8px;
                color: #1a73e8;
                text-decoration: none;
                font-weight: bold;
            }}
            .footer {{
                text-align: center;
                font-size: 13px;
                color: #999;
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        <div class="wrapper">
            <div class="container">
                <div class="logo">
                    <img src="{logo_url}" alt="Logo" />
                </div>
                <h2>Hi {user_name},</h2>
                <p>Here are the latest research articles for: <strong>{query}</strong></p>
    """

    for article in articles:
        html += f"""
            <div class="article">
                <h4>{article['title']}</h4>
                <p>{article['summary']}</p>
                <a href="{article['link']}" target="_blank">Read Full Article →</a>
            </div>
        """

    html += f"""
                <div class="footer">
                    <p>You're receiving this because you subscribed to Research Scraper alerts.</p>
                    <p>© 2025 Research Scraper</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📬 Research Digest: {query}"
    msg["From"] = sender_email
    msg["To"] = recipient
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
            print(f"✅ Email sent to {recipient}")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient}: {e}")

# Email processor for all subscriptions
def send_to_all_subscribers():
    subscriptions_ref = db.collection("subscriptions")
    subscriptions = subscriptions_ref.stream()

    for sub in subscriptions:
        try:
            data = sub.to_dict()
            email = data.get("email")
            query = data.get("query")

            if email and query:
                articles = scrape_pubmed(query)
                send_email(email, query, articles)
                print(f"Sent email to {email} with query: {query}")
        except Exception as e:
            print(f"❌ Error processing subscriber: {e}")

# Route for scheduler to call
@app.route("/process_subscriptions", methods=["POST"])
def process_subscriptions_route():
    try:
        send_to_all_subscribers()
        return jsonify({"message": "Subscription processing job executed!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run locally if needed
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
