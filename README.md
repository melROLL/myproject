# Lab TP1: Building and Deploying Your Python Web App with Flask, GitHub, Deta, and Google Analytics

Welcome to an exciting lab session where you'll learn to create a Python web application, version your code with GitHub, deploy it with Deta, and track its usage using Google Analytics. By the end of this tutorial, you will have a fully functional web app and a deeper understanding of these essential development tools.

## Part 1: Creating a Sample Python App on Deta

1. **Log in or Sign up in Deta:** Start by visiting [Deta](https://www.deta.sh/) and creating an account if you haven't already.

2. **Getting Started with Deta Micro:** Follow the "Getting Started" guide for Deta Micro. You don't need to create a Micro under a specific project at this point.

3. **Deploy Your App:** Once your app is ready, deploy it on Deta.

4. **Access Your Dashboard:** Visit your Deta dashboard, where you will find the app you created.

5. **Launch Your App:** Access your app through the generated URL, which should look like this: `https://your-deta-app-name.deta.dev`.

## Part 2: Versioning Your Code with GitHub

1. **Log in to GitHub:** Visit [GitHub](https://github.com/) and either log in or create a new account if you don't have one.

2. **Create a New Repository:** Create a new GitHub repository with a name of your choice.

3. **Initialize Git in Your App Directory:** Open your terminal and navigate to the directory where your app is located. Run the following commands:
    - `git init`
    - `git add app.py`
    - `git commit -m "first commit"`
    - `git branch -M main`
    - `git remote add origin https://github.com/your_username/your_repo_name.git`
    - `git push -u origin main`

4. **Create Required Files:** In your GitHub repository, create the following files:
    - `README.md` (You can add a description of your app here).
    - `.gitignore` (Add the line `venv` to this file to exclude the virtual environment from versioning).
    - `requirements.txt` (Add the only dependency: flask).

5. **Commit and Push Files to GitHub:** In your terminal, execute the following commands:
    - `git add --all`
    - `git commit -m "second commit"`
    - `git push origin main`

## Part 3: Tracking Your Application Usage with Google Analytics

1. **Log in to Google Analytics:** Visit [Google Analytics](https://analytics.google.com/) and log in with your Google account. If you don't have one, create an account.

2. **Create an Account and Property:** In the Google Analytics admin section, create an account. Under this account, create a property and provide the URL of your Deta app. Select "Create a Universal Analytics property."

3. **Generate a Tracking ID:** An ID in the format "UA-XXXXXXXXX-4" will be generated for your property.

4. **Add Google Analytics Code to Your App:** In your `app.py` file, add the following code (replace `YOUR_GA_CODE` with your generated Google Analytics ID):
   
   ```python
   def hello_world():
       prefix_google = """
       <!-- Google tag (gtag.js) -->
       <script async
       src="https://www.googletagmanager.com/gtag/js?id=YOUR_GA_CODE"></script>
       <script>
       window.dataLayer = window.dataLayer || [];
       function gtag(){dataLayer.push(arguments);}
       gtag('js', new Date());
       gtag('config', ' YOUR_GA_CODE');
       </script>
       """
       return prefix_google + "Hello World"
   ```

5. **Commit and Push Code to GitHub:** Commit and push the updated code to your GitHub repository.

6. **Redeploy Your App to Deta:** Deploy your app again on Deta to ensure the Google Analytics code is integrated.

7. **Testing Google Analytics:** Grab a coffee, finish it, and test Google Analytics by visiting your app from another browser and using the private mode of your browser. You can also use a VPN or the Tor browser to check how Google Analytics behaves in different scenarios.

8. **View Google Analytics Dashboard:** Visit your Google Analytics Dashboard to view user activity on your app. You should see users connecting.

## Reporting

Create a PDF report with the following information:

- Your full name.
- The URL of your web app.
- A screenshot of your Google Analytics panel.
- The URL of your GitHub project (should be public, but only you should have push access).

## Extras

- Add a button to your app that is connected to Google Analytics. When users press it, a new event should be recorded in Google Analytics.
- For an extra challenge, complete the lab using Streamlit and GitHub instead of Flask and Deta.

Congratulations! You've successfully completed this lab, and you now have a fully functional web app, version control with GitHub, hosting with Deta, and analytics tracking with Google Analytics. These skills will be valuable in your future projects and development endeavors. Enjoy exploring and enhancing your app further!