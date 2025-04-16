Andrew Goodling<br>
CIS 655 01<br>
4/16/2025<br>
ReadMe File<br>
This application scrapes research articles from PubMed based on user-supplied keywords and emails daily summaries back to the users. It runs on Google Cloud using fully managed services.<br><br>

Project Goals:<br>
•	Allow users to subscribe with an email + topic <br>
•	Scrape PubMed for articles matching the topic<br>
•	Send queried emails every day at 11 AM<br>
•	Automatically trigger using Cloud Scheduler<br><br>

Technologies used:<br>
Tool/Service	Purpose<br>
Flask	Backend web framework <br>
FireStore	Store subscriptions and articles<br>
Cloud Run	Host the Flask application <br>
Cloud Build	Containerize the application<br>
Cloud Scheduler	Trigger daily tasks<br>
Docker	Package and ship Flask application<br>
Gmail SMTP	Send formatted emails<br>
BeautifulSoup/requests	Scrape PubMed for queries<br><br>

Prerequisites:
1.	A Google Cloud Account
2.	Python 3.11 +
3.	Gmail account with App password enabled (need to have MFA enabled on gmail)
4.	Google Cloud CLI installed
5.	Understanding of Python, Flask, HTML<br><br>

Step by Step:
1.	Create a Google Cloud Project and enable the following API’s
    a.	Cloud Build
    b.	Firestore
    c.	Cloud Scheduler
2.	Set up the Firestore<br>
    a.	To set up the Firestore search “Firestore” in the search bar <br>
   b.	Click create databasechose ‘native mode’ Select region to host<br>
3.	 Open the Cloud shell and make a directory for the project<br>
    a.	Add in the Files that will be needed for deployment<br>
        i.	Main.py<br>
        ii.	Index.html <br>
        iii.	Requirements.txt<br>
        iv.	Dockerfile<br>
        v.	.env<br>
    b.	Populate these files with the code needed to build the application.<br>
        i.	These can be seen in the Github repo found here
4.	Build and Deploy the application to Cloud Run
    a.	gcloud builds submit --tag gcr.io/[PROJECT-ID]/[API Endpoint]
        gcloud run deploy research-scraper \
       --image gcr.io/[PROJECT-ID]/[API Endpoint] \
       --platform managed \
       --region us-central1 \
       --allow-unauthenticated
5.	Set up Cloud Scheduler to hit the API endpoint at a specified time <br>
    a.	I set mine for 11am everyday using (0 11 ***)






