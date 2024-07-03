# Lecture Notes: Building APIs with Flask

## Setting Up the Flask App

- **Staging our Flask App**: [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/)
  - Create virtual environment (venv): 
    ```sh
    python -m venv venv
    ```
    or 
    ```sh
    python3 -m venv venv
    ```
  - Activate virtual environment: 
    ```sh
    venv\Scripts\activate
    ```
    or 
    ```sh
    source venv/bin/activate
    ```
  - Install Flask: 
    ```sh
    pip install flask
    ```
    (Check pip list to ensure installation)

## Building a Basic Flask App

1. Create `app.py` file and import Flask:
    ```python
    from flask import Flask
    app = Flask(__name__)
    ```
2. Define a simple “home” route:
    ```python
    @app.route('/')
    def home():
        return "Hello, Flask!"
    ```
3. Create a runner and configure your app to run in debug mode:
    ```python
    if __name__ == '__main__':
        app.run(debug=True)
    ```

## Our Flask Server

In the Client → Server model, when we run our Flask app locally, we are turning our computer into a server that we can use a client (like a browser) to make requests to. We access the server by making requests to the address `localhost` (127.0.0.1) which refers to the current device our server is running. Port 5000 specifies the internal address or specific channel we can tune into to access this particular server. Using different Ports allows us to have multiple servers running on our localhost at the same time.

## Routing and Resource Handling

- **Routing** is the process of creating URL paths to direct specific functions.
  - The ‘/’ route defines the root of the web application and is the most basic and essential route that often represents the home page.
  - Routes can be general and paint a broad stroke of functionalities, relying on endpoints for specific actions.

## Endpoints

- Endpoints are the specific targets.
  - Typical naming convention will give an accurate description of what the endpoint does, e.g., `add_customer`, `update_customer`, `delete_customer`.
  - In Flask, you can specify the endpoint; if not specified, the name of the function serves as the endpoint.

## Flask-Marshmallow

- [Flask-Marshmallow Documentation](https://flask-marshmallow.readthedocs.io/en/latest/)
- Flask-Marshmallow is a Flask extension that allows for the validation of incoming requests and data to ensure that it fits the structure of a predefined schema.
  - Install Flask-Marshmallow:
    ```sh
    pip install flask-marshmallow
    ```
  - Import Marshmallow and fields into the `app.py`:
    ```python
    from flask_marshmallow import Marshmallow
    from marshmallow import fields
    ```

## Integrating our Database

1. Establish a connection to our MySQL database (create a function to return a connection as done in Module 5).
2. Create a route for a GET request that runs a function querying our database and returns a JSON object validated by our Marshmallow schema.
3. Test the request in your browser.

## Setting up Postman

- Install Postman: [Postman Download](https://www.postman.com/downloads/)
- Create an account (optional, but recommended).
- Open a Workspace and click the “+” to create a new connection.

## Sending POST Request using Postman

1. Set the Request Type: In the request tab, select 'POST' from the dropdown menu. This tells Postman that you’re sending data.
2. Enter the URL: Input the URL of your Flask application's endpoint that handles new customer registrations. It would look something like:
    ```
    http://127.0.0.1:5000/customers
    ```
3. Include JSON Data: Switch to the 'Body' tab, select 'raw', and then choose 'JSON' from the dropdown. Here, you'll input the details of the new guest in JSON format. For example:
    ```json
    {
        "customer_name": "Jane Doe",
        "email": "jane.doe@example.com",
        "phone": "1234567890"
    }
    ```
4. Send the Request: Click the 'Send' button to dispatch your invitation. Postman will communicate with your Flask app, attempting to register the new guest.

---

### Additional Information

- **Debugging**: Always run your Flask app in debug mode during development to get helpful error messages.
- **Environment Variables**: Use environment variables to manage sensitive information like database credentials.
- **RESTful API Principles**: Familiarize yourself with REST principles to design APIs that are easy to understand and use.
- **Testing**: Use tools like Postman or automated tests to ensure your API behaves as expected.
