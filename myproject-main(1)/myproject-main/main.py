from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.oauth2 import service_account
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
import logging,requests,sys
from html import unescape
from flask import Flask, render_template, request



# Create a Flask web application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)
logs = []


credentials = service_account.Credentials.from_service_account_file(
    'datasource-401810-74bb7cd3e835.json', scopes=['https://www.googleapis.com/auth/analytics.readonly']
)


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

# Define a route for the homepage
@app.route('/')
def root():
    return render_template("index.html")

@app.route('/logger', methods=['GET', 'POST'])
def logger_page():
    log_message ='This a log message'
    logger.info('This is a log message!')
    response_message = "This is a response"
    user_count = sample_run_report()
    
    if request.method == 'POST' and 'log_message' in request.form:
        log_message = request.form.get('log_message')
        logger.info(log_message)
        # return render_template('logger.html', logs=log_message)
    
    if request.method == 'POST' and request.form.get('action') == 'Google':
            response = requests.get("https://www.google.com")  
            if response.status_code == 200:
                response_message = response.cookies.get_dict()
            else:
                response_message = "Request to Google failed."
            
            # return render_template("logger.html", logs=log_message,response_message=response_message)
    
    if request.method == 'POST' and request.form.get('action') == 'ganalytics':
        response = requests.get("https://analytics.google.com/analytics/web/#/p407490614/reports/intelligenthome")
        if response.status_code == 200:
            response_message = response.text
        else:
            response_message = "Request to Google failed."

        # return render_template("logger.html", logs=log_message,response_message=response_message)
    
    return render_template("logger.html", logs=log_message,response_message=response_message, user_count=user_count)
# Run the application
if __name__ == '__main__':
    app.run(debug=True)
