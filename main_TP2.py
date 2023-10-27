import json
from flask import Flask, request, render_template
import sys
import logging
import requests
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
from google.oauth2 import service_account
from logging.config import dictConfig
from pytrends.request import TrendReq

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


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


# Google request
@app.route('/google-request', methods=['GET'])
def google_request():
    # Question
    google_url = "https://www.google.com/"
    
    try:
        response = requests.get(google_url)
        response.raise_for_status()  
        return response.text
    # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        return f"Error making Google request: {str(e)}"
    
# Google analytics request
@app.route('/google-analytics-request', methods=['GET'])
def google_analytics_request():
    # Question
    google_analytics_url = "https://analytics.google.com/analytics/web/?authuser=6#/report-home/a286538006w411474576p296626512"
    
    try:
        response = requests.get(google_analytics_url)
        response.raise_for_status() # Raise an exception for HTTP errors
        # Return response from get request
        return response.text
   
    except requests.exceptions.RequestException as e:
        return f"Error making Google Analytics request: {str(e)}"

# Google cookies request
@app.route('/google-cookies-request', methods=['GET'])
def google_cookies_request():

    google_analytics_url = "https://analytics.google.com/analytics/web/?authuser=6#/report-home/a286538006w411474576p296626512"
    
    try:
        response = requests.get(google_analytics_url)
        response.raise_for_status() # Raise an exception for HTTP errors

        # Retrieve cookies of the response
        cookies = response.cookies

        # Send cookies to the template for display
        return render_template('cookies.html', cookies=cookies)
    
    except requests.exceptions.RequestException as e:
        return f"Error making Google Analytics Cookies request: {str(e)}"

# Fetch data from Google analytics api
@app.route('/api-google-analytics-data', methods=['GET'])
def api_google_analytics_data():

    # Set the path to the Google Cloud credentials file
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'maximal-emitter-401822-371705b00b77.json'
    # Define Google Analytics property ID, and a period of time with starting date and ending date
    GA_property_ID = "286538006"
    start_date = "2023-10-01"
    end_date = "today"

    # Initialize a client for the Google Analytics Data API
    client = BetaAnalyticsDataClient(credentials=credentials)
    
    # Function that gets the number of visitors
    def get_visitors_number(client, property_id):
        # Define the request to retrieve active users metric
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[{"start_date": start_date, "end_date": end_date}],
            metrics=[{"name": "activeUsers"}]
        )

        response = client.run_report(request)
        # return active_users_metric
        return response

    # Get the visitor number using the function
    response = get_visitors_number(client, GA_property_ID)

    # Check if there's a valid response with data
    if response and response.row_count > 0:
        # Extract the value of the active users metric from the response
        metric_value = response.rows[0].metric_values[0].value
    else:
        metric_value = "N/A"  # Handle the case where there is no data

    return f'Number of visitors: {metric_value}'
    


# Run the Flask application if this script is the main program
if __name__ == '__main__':
    app.run(debug=True)
