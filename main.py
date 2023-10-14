# Import necessary modules
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
import logging, requests, sys
from html import unescape
from flask import Flask, render_template, request

# Create a Flask application
app = Flask(__name__, template_folder='templat')

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)
logs = []

# Set up Google Analytics credentials
credentials = service_account.Credentials.from_service_account_file(
    'Credentials.json', scopes=['https://www.googleapis.com/auth/analytics.readonly']
)

# Function to run a report using Google Analytics Data API
def sample_run_report():
    """Runs a simple report on a Google Analytics 4 property."""
    user_count = 0
    property_id = "407490614"
    client = BetaAnalyticsDataClient(credentials=credentials)

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="country")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="2023-03-31", end_date="today")],
    )
    response = client.run_report(request)

    for row in response.rows:
        user_count += int(row.metric_values[0].value)

    return user_count

# Define a route for the root URL
@app.route('/')
def root():
    return render_template("index.html")

# Define a route for the logger page
@app.route('/logger', methods=['GET', 'POST'])
def logger_page():
    log_message = 'This a log message'
    logger.info('This is a log message!')
    response_message = "This is a response"
    user_count = sample_run_report()
    
    # Handle POST requests
    if request.method == 'POST':
        if 'log_message' in request.form:
            log_message = request.form.get('log_message')
            logger.info(log_message)
        elif request.form.get('action') == 'Google':
            response = requests.get("https://www.google.com")
            if response.status_code == 200:
                response_message = response.cookies.get_dict()
            else:
                response_message = "Request to Google failed."
        elif request.form.get('action') == 'ganalytics':
            response = requests.get("https://analytics.google.com/analytics/web/#/p407490614/reports/intelligenthome")
            if response.status_code == 200:
                response_message = response.text
            else:
                response_message = "Request to Google failed."

    return render_template("logger.html", logs=log_message, response_message=response_message, user_count=user_count)

# Run the Flask application if this script is the main program
if __name__ == '__main__':
    app.run(debug=True)
