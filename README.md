Andrew Goodling
CIS 655 01
4/16/2025
ReadMe File
This application scrapes research articles from PubMed based on user-supplied keywords and emails daily summaries back to the users. It runs on Google Cloud using fully managed services.

Project Goals:
•	Allow users to subscribe with an email + topic
•	Scrape PubMed for articles matching the topic
•	Send queried emails every day at 11 AM
•	Automatically trigger using Cloud Scheduler

Technologies used:
Tool/Service	Purpose
Flask	Backend web framework 
FireStore	Store subscriptions and articles
Cloud Run	Host the Flask application 
Cloud Build	Containerize the application
Cloud Scheduler	Trigger daily tasks
Docker	Package and ship Flask application
Gmail SMTP	Send formatted emails
BeautifulSoup/requests	Scrape PubMed for queries

Prerequisites:
1.	A Google Cloud Account
2.	Python 3.11 +
3.	Gmail account with App password enabled (need to have MFA enabled on gmail)
4.	Google Cloud CLI installed
5.	Understanding of Python, Flask, HTML

Step by Step:
1.	Create a Google Cloud Project and enable the following API’s
a.	Cloud Build
b.	Firestore
c.	Cloud Scheduler
2.	Set up the Firestore
a.	To set up the Firestore search “Firestore” in the search bar 
b.	Click create databasechose ‘native mode’ Select region to host
3.	 Open the Cloud shell and make a directory for the project
a.	Add in the Files that will be needed for deployment
i.	Main.py
ii.	Index.html 
iii.	Requirements.txt
iv.	Dockerfile
v.	.env
b.	Populate these files with the code needed to build the application.
i.	These can be seen in the Github repo found here
4.	Build and Deploy the application to Cloud Run
a.	gcloud builds submit --tag gcr.io/[PROJECT-ID]/[API Endpoint]
gcloud run deploy research-scraper \
  --image gcr.io/[PROJECT-ID]/[API Endpoint] \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
5.	Set up Cloud Scheduler to hit the API endpoint at a specified time
a.	I set mine for 11am everyday using (0 11 ***)






