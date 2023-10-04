from flask import Flask, render_template, request
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

def hello_world():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=G-93Q4V"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-93Q4VXGGMQ');
    </script>
    """
    return prefix_google + "Hello World"

@app.route('/')
def home():
    return hello_world()

@app.route('/logger', methods=['GET', 'POST'])
def logger():
    if request.method == 'POST':
        message = request.form['log_message']

        # Log to Python
        logging.info(message)

        # Log to the browser
 #       return f'<p>Logged: {message}</p>'

    return render_template('logger.html')

if __name__ == '__main__':
    app.run(debug=True)
