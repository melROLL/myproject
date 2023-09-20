from flask import Flask

# Create a Flask web application
app = Flask(__name__)

# Define a route for the homepage
@app.route('/')
def hello_world(): 
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async 
    src="https://www.googletagmanager.com/gtag/js?id=G-93Q4VXGGMQ"></script>
    <script>
        window.dataLayer = window.dataLayer || []; 
        function gtag(){dataLayer.push(arguments);} 
        gtag('js', new Date());
        gtag('config', 'G-QY0W6CSL6X'); 
    </script>
      """
    return prefix_google + "Hello World"

def hello_world():
    return 'Hello World'

# Run the application
if __name__ == '__main__':
    app.run(debug=True)